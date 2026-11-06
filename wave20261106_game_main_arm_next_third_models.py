import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
import unicorn
from unicorn import arm_const as R
import match_runtime as C

NAMES=['0207211c','02071b28','02073090','0207313c']
CONTEXT,DETAIL,ALTERNATE,OBJECT,WIDGET,CATEGORY=0x02400000,0x02410000,0x02411000,0x02420000,0x02430000,0x02440000
SP,STOP=0x027f0000,0x027d0000
COUNTER,PAGE,INDEX,ROUTE=0x021c50e8,0x021c5a24,0x021c6124,0x021c5b20


def fixtures(name):
    if name=='0207211c':
        rows=[dict(index=i,flags=f,swap=False,first=0xffffffff,second=0x80000000) for i in list(range(11))+[0xffffffff] for f in [0,255]]
        rows += [dict(index=i,flags=f,swap=bool(i&1),first=0x12345678,second=0) for i in range(3,10) for f in [0x55,0xaa]]
        return rows
    if name=='02071b28':return [dict(flags=f,counter=c,mutate=bool(n&1),ids=[0,0x7f,0x80,0xff,3,0x81,1,2,0xfe]) for n,(f,c) in enumerate([(0,0),(1,1),(0x80,0xffffffff),(0x81,0x80000000),(0xff,0x12345678)])]
    if name=='02073090':return [dict(option=o,query=q) for o,q in [(0,0),(0,1),(1,0),(1,0xffffffff)]]
    return [dict(flags=f,kind=k,index=[-32768,-1,0,32767][k%4]) for f in [0,0x10] for k in [1,2,26,3]]+[dict(flags=f,kind=26,index=-1) for f in [1,15]]


def run(row,body,fixture,main,ordinal):
    name=format(int(row['address'],0),'08x');vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,main);address=int(row['address'],0);vm.mem_write(address,body)
    for location,size in [(CONTEXT,512),(DETAIL,256),(ALTERNATE,256),(OBJECT,512),(WIDGET,0x1000),(CATEGORY,128),(COUNTER,0xe4),(PAGE,0x804)]:vm.mem_write(location,bytes((i*17+ordinal)&255 for i in range(size)))
    vm.mem_write(0x021c4f80,struct.pack('<I',DETAIL));initial=[0x11220000+n*0x100+ordinal for n in range(15)];initial[-2:]=[SP,STOP]
    if name=='0207211c':
        initial[:3]=[fixture['index'],fixture['first'],fixture['second']];vm.mem_write(DETAIL+0x1d,bytes([fixture['flags']]));vm.mem_write(ALTERNATE+0x1d,bytes([fixture['flags']^0x55]))
    elif name=='02071b28':
        vm.mem_write(COUNTER+0xd1,bytes([fixture['flags']]));vm.mem_write(COUNTER+0xe0,struct.pack('<I',fixture['counter']))
        for i,value in enumerate(fixture['ids']):vm.mem_write(0x020daf42+2*i,bytes([value]))
    elif name=='02073090':initial[0]=fixture['option']
    else:
        vm.mem_write(INDEX+0xd8,struct.pack('<h',fixture['index']));vm.mem_write(PAGE+0x7da,bytes([fixture['flags']]));vm.mem_write(CATEGORY+0x28,bytes([fixture['kind']]))
    vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for register,value in zip(C.REGISTERS,initial):vm.reg_write(register,value)
    imports={int(b['address'],0):symbol for symbol,b in row['nativeSymbolEntries'].items() if b['kind']=='function'};calls=[];writes=[];returned=False;debits=[];widgets=[]
    def put(location,data):vm.mem_write(location,data);writes.append(dict(provider=True,address=location,hex=data.hex()))
    def memory(uc,access,location,size,value,user):writes.append(dict(provider=False,address=location,size=size,value=value))
    def code(uc,location,size,user):
        nonlocal returned
        if location==STOP:returned=True;uc.emu_stop();return
        if location not in imports:return
        if uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('Measured ARM provider entered as Thumb')
        symbol=imports[location];words=[uc.reg_read(r) for r in C.REGISTERS[:4]];call=dict(symbol=symbol,address=location,words=words,stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP),16)).hex());result=0x90000000+len(calls)+1
        if symbol=='native_fn_02061944':
            result=CONTEXT
            if name=='0207211c' and fixture['swap']:put(0x021c4f80,struct.pack('<I',ALTERNATE))
        elif name=='02071b28':
            if symbol=='native_fn_02072030':put(COUNTER+0xe0,struct.pack('<I',fixture['counter']^0xa55aa55a))
            elif symbol=='native_fn_02065d28':
                index=len(debits)
                if index>=9:raise ValueError('Unexpected tenth debit provider')
                result=[0,1,0xffffffff,0x80000000,7,2,3,0x7fffffff,9][index];debits.append(result)
                if fixture['mutate']:
                    value=struct.unpack('<I',bytes(uc.mem_read(COUNTER+0xe0,4)))[0];put(COUNTER+0xe0,struct.pack('<I',(value+0x100*(index+1))&0xffffffff))
        elif name=='02073090':
            if symbol=='native_fn_ov000_02215698':result=OBJECT
            elif symbol=='native_fn_02049ad0':result=WIDGET+len(widgets)*0x100;widgets.append(result)
            elif symbol=='native_fn_02062378':result=fixture['query']
            elif symbol=='native_fn_ov000_02216664':put(ROUTE+8,struct.pack('<I',0xface0000+ordinal))
        elif name=='0207313c':
            if symbol=='native_fn_02065d88':result=CATEGORY;put(PAGE+0x7d7,bytes([0x55]))
            if symbol=='native_fn_ov000_021e7b9c':call['pageStatusAtCall']=bytes(uc.mem_read(PAGE+0x7d7,1))[0]
        calls.append(call)
        for n,register in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(register,0xcafe0000+len(calls)*16+n)
        uc.reg_write(R.UC_ARM_REG_R0,result);uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10);uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(address,STOP+4,count=10000)
    if not returned:raise ValueError('Actual grouped UI caller did not return')
    registers=[vm.reg_read(r) for r in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Grouped caller callee-saved/SP differs')
    failures=[];symbols=[c['symbol'] for c in calls]
    if name=='0207211c':
        index=fixture['index'];expected=['native_fn_02061944']
        if index in [1,2]:expected+=['native_fn_02065818']
        elif 3<=index<=9:expected+=['native_fn_020720a4']
        if symbols!=expected:failures.append('Independent dispatcher range/provider choice')
        if len(calls)==2:
            flags=fixture['flags']^(0x55 if fixture['swap'] else 0);words=[CONTEXT+16+12*index,fixture['first'],fixture['second']] if index in [1,2] else [index,flags&(1<<(index-3)),fixture['first'],fixture['second']]
            if calls[1]['words'][:len(words)]!=words:failures.append('Fresh detail pointer, record12 or raw bitmask forwarding')
    elif name=='02071b28':
        expected=['native_fn_02061944']+(['native_fn_02072030'] if fixture['flags']&1 else [])+['native_fn_020622ec']+['native_fn_02065d28']*9
        if symbols!=expected:failures.append('Independent selected-bit invalidation and nine debits')
        command=next((c for c in calls if c['symbol']=='native_fn_020622ec'),None)
        if command is None or command['words'][:3]!=[6,11,0]:failures.append('Fixed command ABI')
        found=[c['words'][0] for c in calls if c['symbol']=='native_fn_02065d28'];ids=[(v-256 if v&128 else v)&0xffffffff for v in fixture['ids']]
        if found!=ids:failures.append('Nine signed bytes at stride2')
        value=fixture['counter']^(0xa55aa55a if fixture['flags']&1 else 0)
        for i,amount in enumerate([0,1,0xffffffff,0x80000000,7,2,3,0x7fffffff,9]):value=(value+(0x100*(i+1) if fixture['mutate'] else 0)-amount)&0xffffffff
        if registers[0]!=value or struct.unpack('<I',bytes(vm.mem_read(COUNTER+0xe0,4)))[0]!=value:failures.append('Fresh post-provider counter read/modulo32 result')
    elif name=='02073090':
        expected=['native_fn_ov000_02215698','native_fn_02049ad0','native_fn_ov000_022162c0','native_fn_ov000_02216664','native_fn_0204b61c','native_fn_020756e4','native_fn_02062378']+(['native_fn_020619b0'] if fixture['query'] else [])
        for i in range(4):expected+=['native_fn_02049ad0','native_fn_ov000_022162c0']
        expected+=['native_fn_ov000_02215078']+(['native_fn_ov000_021e7b9c'] if fixture['option'] else [])
        if symbols!=expected:failures.append('Independent qualified overlay/main call order')
        getters=[c for c in calls if c['symbol']=='native_fn_02049ad0'];providers=[c for c in calls if c['symbol']=='native_fn_ov000_022162c0']
        if [c['words'][0] for c in getters]!=[1,24,25,27,28] or [c['words'][0] for c in providers]!=[WIDGET+i*0x100 for i in range(5)]:failures.append('Each fresh widget pointer forwarded to actual ov000 provider')
        requirements={'native_fn_ov000_02216664':[ROUTE],'native_fn_0204b61c':[OBJECT+16,0],'native_fn_020756e4':[0,0xffffffff,0xffffffff],'native_fn_020619b0':[0],'native_fn_ov000_02215078':[ROUTE+0xa8,1],'native_fn_ov000_021e7b9c':[83]}
        if any(c['words'][:len(requirements[c['symbol']])]!=requirements[c['symbol']] for c in calls if c['symbol'] in requirements):failures.append('Measured opaque offsets/query/option arguments')
    else:
        queried=fixture['flags']&15==0;expected=(['native_fn_02065d88'] if queried else [])+['native_fn_ov000_021e7b9c','native_fn_020756e4']
        if symbols!=expected:failures.append('Low nibble gating/provider sequence')
        if queried and (not calls or calls[0]['words'][0]!=(fixture['index']&0xffffffff)):failures.append('Signed16 index forwarding')
        status=(15 if fixture['kind']==26 else 0x55) if queried else 0
        callbacks=[c for c in calls if c['symbol']=='native_fn_ov000_021e7b9c']
        if len(callbacks)!=1 or callbacks[0]['words'][0]!=84 or callbacks[0].get('pageStatusAtCall')!=status or bytes(vm.mem_read(PAGE+0x7d7,1))!=bytes([status]):failures.append('Default/1/2/26 category status and callback observation')
        if not calls or calls[-1]['words'][:3]!=[0xffffffff,0xffffffff,4]:failures.append('Final three-word command ABI')
    return dict(actualTopReturn=True,modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())
