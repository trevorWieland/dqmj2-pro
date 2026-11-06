import hashlib
import struct
from project import configuration,native_dependencies
native_dependencies(configuration())
import unicorn
from unicorn import arm_const as R
import match_runtime as C

NAMES=['02072568','020728ec','02072de8']
OBJECT,WIDGET,SP,STOP=0x02400000,0x02410000,0x027f0000,0x027d0000


def fixtures(name):
    if name=='02072568':return [dict(index=i,same=same,value=value) for i in range(8) for same in [False,True] for value in [0,1,0x80000000,0xffffffff]]
    if name=='020728ec':return [dict(index=i,first=first,second=0x7f,after=after) for i in range(8) for first in [0,0x7f,0x80,0xff] for after in [0x80,0xff]]
    return [dict(index=i,option=option,x=[0,1,127,255][i%4],y=[255,128,8,0][i%4]) for i in range(8) for option in [0,1,0xffffffff,0x80000000]]


def run(row,body,fixture,main,ordinal):
    name=format(int(row['address'],0),'08x');vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,main);address=int(row['address'],0);vm.mem_write(address,body)
    vm.mem_write(0x021c4f78,bytes((i*17+ordinal)&255 for i in range(128)));vm.mem_write(0x021c5a00,bytes((i*31+ordinal)&255 for i in range(256)));vm.mem_write(OBJECT,bytes((i*19+ordinal)&255 for i in range(512)));vm.mem_write(WIDGET,bytes((i*23+ordinal)&255 for i in range(512)))
    index=fixture['index'];initial=[0x11220000+n*0x100+ordinal for n in range(15)];initial[-2:]=[SP,STOP];initial[:4]=[index,0xa5a55a5a,0xdeadbeef,0xcafe1234]
    if name=='02072568':initial[1]=fixture['value'];vm.mem_write(0x021c4f78+index*4,struct.pack('<I',fixture['value'] if fixture['same'] else fixture['value']^0xffffffff))
    elif name=='020728ec':vm.mem_write(0x021c5a11+index*9,bytes([fixture['first']]));vm.mem_write(0x021c5a12+index*9,bytes([fixture['second']]))
    else:
        initial[:2]=[OBJECT,fixture['option']];vm.mem_write(OBJECT+2,bytes([index]));vm.mem_write(0x021c5a13+index*9,bytes([fixture['x']]));vm.mem_write(0x021c5a14+index*9,bytes([fixture['y']]))
    vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for register,value in zip(C.REGISTERS,initial):vm.reg_write(register,value)
    imports={int(b['address'],0):symbol for symbol,b in row['nativeSymbolEntries'].items() if b['kind']=='function'};calls=[];writes=[];returned=False
    def memory(uc,access,location,size,value,user):writes.append(dict(address=location,size=size,value=value))
    def code(uc,location,size,user):
        nonlocal returned
        if location==STOP:returned=True;uc.emu_stop();return
        if location not in imports:return
        if uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('ARM data caller provider entered as Thumb')
        symbol=imports[location];words=[uc.reg_read(r) for r in C.REGISTERS[:4]];call=dict(symbol=symbol,address=location,words=words,stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP),16)).hex());result=0x90000000+len(calls)+1
        if name=='020728ec':result=WIDGET;uc.mem_write(0x021c5a12+index*9,bytes([fixture['after']]))
        elif name=='02072de8' and symbol=='native_fn_0204b53c':call['point']=list(struct.unpack('<hh',bytes(uc.mem_read(words[1],4))));uc.mem_write(OBJECT+2,bytes([(index+1)%8]));uc.mem_write(OBJECT+0x50,struct.pack('<I',0xface0000+ordinal))
        calls.append(call)
        for n,register in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(register,0xcafe0000+len(calls)*16+n)
        uc.reg_write(R.UC_ARM_REG_R0,result);uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10);uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(address,STOP+4,count=5000)
    if not returned:raise ValueError('Actual original/data caller did not return')
    registers=[vm.reg_read(r) for r in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Data caller callee-saved/SP contract differs')
    failures=[]
    if name=='02072568':
        expected=[] if fixture['same'] else ['native_fn_0206de44']
        if [c['symbol'] for c in calls]!=expected or (calls and calls[0]['words'][0]!=1):failures.append('Independent changed-word invalidation boundary')
        if struct.unpack('<I',bytes(vm.mem_read(0x021c4f78+index*4,4)))[0]!=fixture['value']:failures.append('Independent full32-bit table update')
    elif name=='020728ec':
        if len(calls)!=1 or calls[0]['symbol']!='native_fn_02049ad0' or calls[0]['words'][0]!=(fixture['first']-256 if fixture['first']&128 else fixture['first'])&0xffffffff:failures.append('Independent signed-byte provider argument')
        if registers[0]!=WIDGET or bytes(vm.mem_read(WIDGET+5,1))!=bytes([fixture['after']]):failures.append('Fresh post-provider signed field and returned pointer')
    else:
        expected=['native_fn_0204b53c','native_fn_0204b5b0','native_fn_0204b380','native_fn_0204b61c','native_fn_0205f9e4']
        if [c['symbol'] for c in calls]!=expected:failures.append('Independent position/configuration call sequence')
        if len(calls)==5:
            if calls[0]['words'][0]!=OBJECT+0x50 or calls[0].get('point')!=[fixture['x']*8,fixture['y']*8]:failures.append('Independent byte-column9 and signed-halfword point scaling')
            if calls[1]['words'][:2]!=[OBJECT+0x50,64] or calls[2]['words'][:2]!=[OBJECT+8,0] or calls[3]['words'][:2]!=[OBJECT+0x50,0 if fixture['option'] else 1] or calls[4]['words'][0]!=OBJECT+0x50:failures.append('Opaque component offsets and option inversion')
            if registers[0]!=0x90000005:failures.append('Final opaque provider result forwarding')
    return dict(actualTopReturn=True,modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())
