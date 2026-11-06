import hashlib
import struct
from project import native_dependencies,configuration
native_dependencies(configuration())
import unicorn
from unicorn import arm_const as R
import match_runtime as C

NAMES=['02072b74']
SAMPLE,HIT,STATUS,SP,STOP=0x02400000,0x02410000,0x02420000,0x027f0000,0x027d0000
TABLE=0x021c5a11


def fixtures(name):
    positions=[(32,24),(31,24),(95,39),(96,24),(32,23),(32,40),(96,64),(159,79),(160,64),(0,0)]
    rows=[dict(mask=mask,x=x,y=y,allowed=(i//2)&1,notify=i&1,alias=False,overlap=False) for mask in range(4) for i,(x,y) in enumerate(positions)]
    rows += [dict(mask=3,x=x,y=y,allowed=allowed,notify=notify,alias=False,overlap=False) for x,y in [(32,24),(96,64)] for allowed in [0,1] for notify in [0,1]]
    rows += [dict(mask=mask,x=32,y=24,allowed=0,notify=1,alias=True,overlap=True) for mask in [2,3]]
    rows += [dict(mask=3,x=32,y=24,allowed=0xffffffff,notify=0x80000000,alias=False,overlap=False)]
    return rows


def run(row,body,fixture,main,ordinal):
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,main);address=int(row['address'],0);vm.mem_write(address,body)
    records=bytearray((i*17+ordinal)&255 for i in range(18));rectangles=[(4,3),(4,3) if fixture['overlap'] else (12,8)]
    for i,(x,y) in enumerate(rectangles):records[i*9+2:i*9+4]=bytes([x,y]);records[i*9+5]=int(bool(fixture['mask']&(1<<i)))
    vm.mem_write(TABLE,bytes(records));vm.mem_write(SAMPLE,bytes([0xaa,fixture['x'],fixture['y']]));hit=bytearray((0xa0+i)&255 for i in range(16));vm.mem_write(HIT,bytes(hit));vm.mem_write(STATUS,b'\x77');statusPointer=HIT if fixture['alias'] else STATUS
    initial=[0x11220000+n*0x100+ordinal for n in range(15)];initial[:4]=[0xdeadbeef,HIT,fixture['notify'],statusPointer];initial[-2:]=[SP,STOP];vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for register,value in zip(C.REGISTERS,initial):vm.reg_write(register,value)
    imports={int(b['address'],0):symbol for symbol,b in row['nativeSymbolEntries'].items() if b['kind']=='function'};calls=[];writes=[];returned=False
    def memory(uc,access,location,size,value,user):writes.append(dict(address=location,size=size,value=value))
    def code(uc,location,size,user):
        nonlocal returned
        if location==STOP:returned=True;uc.emu_stop();return
        if location not in imports:return
        if uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('Rectangle provider entered in wrong mode')
        symbol=imports[location];words=[uc.reg_read(r) for r in C.REGISTERS[:4]];call=dict(symbol=symbol,address=location,words=words,stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP),16)).hex());result=SAMPLE if symbol=='native_fn_02066c3c' else fixture['allowed'] if symbol=='native_fn_02072ed4' else 0x90000000+len(calls)
        if symbol=='native_fn_02072ed4':call['hitBeforePredicate']=bytes(uc.mem_read(HIT,16)).hex()
        calls.append(call)
        for n,register in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(register,0xcafe0000+len(calls)*16+n)
        uc.reg_write(R.UC_ARM_REG_R0,result);uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10);uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(address,STOP+4,count=5000)
    if not returned:raise ValueError('Actual rectangle caller did not return')
    registers=[vm.reg_read(r) for r in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Rectangle callee-saved/SP differs')
    selected=next((i for i,(x,y) in enumerate(rectangles) if fixture['mask']&(1<<i) and x*8<=fixture['x']<(x+8)*8 and y*8<=fixture['y']<(y+2)*8),None);expected=['native_fn_02066c3c'];failures=[];status=0x77
    if selected is not None:
        expected+=['native_fn_02072ed4'];hit[0]=255;hit[2]=selected;hit[6]=0
        if len(calls)<2 or calls[1]['words'][0]!=selected or calls[1].get('hitBeforePredicate')!=bytes(hit).hex():failures.append('Required byte index and hit fields committed before predicate')
        if not fixture['allowed']:
            if fixture['alias']:hit[0]=2
            else:status=2
        if fixture['notify']:
            expected+=['native_fn_0205e7a8'];message=(82 if selected==0 else 83) if fixture['allowed'] else 84
            if not calls or calls[-1]['words'][:2]!=[0xffffffff,message]:failures.append('Independent optional response word')
    if [c['symbol'] for c in calls]!=expected:failures.append('Half-open rectangle bounds/priority/provider order')
    result=selected if selected is not None and fixture['allowed'] else 0xffffffff
    if registers[0]!=result:failures.append('Independent signed index or minus-one result')
    if bytes(vm.mem_read(HIT,16))!=bytes(hit) or bytes(vm.mem_read(STATUS,1))!=bytes([status]):failures.append('Full hit state/status including aliased byte output')
    return dict(actualTopReturn=True,modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())
