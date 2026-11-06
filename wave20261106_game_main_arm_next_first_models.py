import hashlib
import struct
from project import native_dependencies,configuration
native_dependencies(configuration())
import unicorn
from unicorn import arm_const as R
import match_runtime as C

CONTEXT,SP,STOP=0x02400000,0x027f0000,0x027d0000
NAMES=['020720a4','020725e8','020726d8']
TABLES={'020725e8':[0,3,2,1,3,6,0,5,4,7,8,9,10,11,12,13,14,0,15],
        '020726d8':[0,3,2,4,8,7,5,9,10,11,12,13,14,0,0,18]}


def fixtures(name):
    if name in TABLES:
        values=list(range(32))+[0x7fffffff,0x80000000,0xffffffff,0xfffffffe,0x12345678]
        return [dict(value=value) for value in values]
    return [dict(index=index,duplicate=duplicate,predicate=predicate,first=[0,1,0xffffffff,0x80000000][index%4],second=[0xffffffff,0,0x12345678,0x7fffffff][index%4]) for index in range(10) for duplicate in [0,1] for predicate in [0,1]]


def run(row,body,fixture,main,ordinal):
    name=format(int(row['address'],0),'08x');vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,main);address=int(row['address'],0);vm.mem_write(address,body)
    context=bytes((i*17+ordinal)&255 for i in range(512));vm.mem_write(CONTEXT,context)
    initial=[0x11220000+n*0x100+ordinal for n in range(15)];initial[-2:]=[SP,STOP]
    initial[:4]=[fixture['value'],0xa5a55a5a,0xdeadbeef,0xcafe1234] if name in TABLES else [fixture['index'],fixture['duplicate'],fixture['first'],fixture['second']]
    vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for register,value in zip(C.REGISTERS,initial):vm.reg_write(register,value)
    calls=[];writes=[];returned=False;imports={int(b['address'],0):symbol for symbol,b in row['nativeSymbolEntries'].items()}
    def memory(uc,access,location,size,value,user):writes.append(dict(address=location,size=size,value=value))
    def code(uc,location,size,user):
        nonlocal returned
        if location==STOP:returned=True;uc.emu_stop();return
        if location not in imports:return
        if uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('ARM provider entered as Thumb')
        symbol=imports[location];words=[uc.reg_read(r) for r in C.REGISTERS[:4]];calls.append(dict(symbol=symbol,address=location,words=words,stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP),16)).hex()))
        result=0x90000000+len(calls)
        if symbol=='native_fn_02061944':result=CONTEXT
        elif symbol=='native_fn_020625bc':result=fixture['predicate']
        elif symbol=='native_fn_0207211c':uc.mem_write(CONTEXT+16,struct.pack('<I',0xface0000+ordinal))
        for n,register in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(register,0xcafe0000+len(calls)*16+n)
        uc.reg_write(R.UC_ARM_REG_R0,result);uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10);uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(address,STOP+4,count=5000)
    if not returned:raise ValueError('Actual caller did not return')
    registers=[vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Callee-saved registers or SP differ')
    failures=[]
    if name in TABLES:
        value=fixture['value'];expected=TABLES[name][value] if value<len(TABLES[name]) else 0
        if registers[0]!=expected or calls:failures.append('Independent unsigned switch mapping/default')
    else:
        symbols=['native_fn_02061944','native_fn_020625bc','native_fn_0207211c','native_fn_02065818']+(['native_fn_02065818'] if fixture['duplicate'] else [])
        if [c['symbol'] for c in calls]!=symbols:failures.append('Fresh getter/predicate/provider call order')
        if len(calls)>=4:
            if calls[2]['words'][:3]!=[2 if fixture['predicate'] else 1,fixture['first'],fixture['second']]:failures.append('Required three-argument provider ABI')
            if calls[3]['words'][:3]!=[CONTEXT+16+12*fixture['index'],fixture['first'],fixture['second']]:failures.append('Independent twelve-byte record displacement and forwarding')
            if fixture['duplicate'] and (len(calls)<5 or calls[4]['words'][:3]!=[CONTEXT+16,fixture['first'],fixture['second']]):failures.append('Duplicate updates record zero')
        expected=bytearray(context);struct.pack_into('<I',expected,16,0xface0000+ordinal)
        if bytes(vm.mem_read(CONTEXT,512))!=bytes(expected):failures.append('Minimum provider memory effect')
    return dict(actualTopReturn=True,modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())
