import hashlib
import struct
from project import native_dependencies,configuration
native_dependencies(configuration())
import unicorn
from unicorn import arm_const as R
import match_runtime as C

NAMES=['0207154c']
CONTEXT,SP,STOP=0x02400000,0x027f0000,0x027d0000


def fixtures(name):
    return [dict(initial=initial,opened=opened,allocated=allocated,amount=amount) for initial,opened,allocated,amount in [(0,1,2,3),(19,31,43,0),(0xffffffff,0,0xffffffff,1),(0,0xffffffff,0x80000000,0x80000000),(0x7fffffff,0x80000000,0x7fffffff,2),(1,0x12345678,0x87654321,0x24681357),(77,88,99,0xffffffff),(0xffffffff,1,0,0)]]


def run(row,body,fixture,main,ordinal):
    vm=unicorn.Uc(unicorn.UC_ARCH_ARM,unicorn.UC_MODE_ARM);vm.ctl_set_cpu_model(R.UC_CPU_ARM_946);vm.mem_map(0x02000000,0x800000);vm.mem_write(0x02000000,main);address=int(row['address'],0);vm.mem_write(address,body)
    seed=bytearray((i*17+ordinal)&255 for i in range(0x260));struct.pack_into('<I',seed,0x25c,fixture['initial']);vm.mem_write(CONTEXT,bytes(seed));prefix=main[0xde394:0xde394+22]
    initial=[0x11220000+n*0x100+ordinal for n in range(15)];initial[-2:]=[SP,STOP];vm.reg_write(R.UC_ARM_REG_CPSR,(ordinal%16)<<28|0x10)
    for register,value in zip(C.REGISTERS,initial):vm.reg_write(register,value)
    imports={int(b['address'],0):symbol for symbol,b in row['nativeSymbolEntries'].items() if b['kind']=='function'};calls=[];writes=[];returned=False
    def memory(uc,access,location,size,value,user):writes.append(dict(address=location,size=size,value=value))
    def code(uc,location,size,user):
        nonlocal returned
        if location==STOP:returned=True;uc.emu_stop();return
        if location not in imports:return
        if uc.reg_read(R.UC_ARM_REG_CPSR)&32:raise ValueError('Initializer provider entered in wrong mode')
        symbol=imports[location];words=[uc.reg_read(r) for r in C.REGISTERS[:4]];stack=bytes(uc.mem_read(uc.reg_read(R.UC_ARM_REG_SP),16));call=dict(symbol=symbol,address=location,words=words,stack=stack.hex());result=0x90000000+len(calls)
        if symbol=='native_fn_02061944':result=CONTEXT
        elif symbol=='native_fn_0201d444':
            call['sourceBytes']=bytes(uc.mem_read(words[1],22)).hex();uc.mem_write(words[0],bytes(uc.mem_read(words[1],22)));result=words[0]
        elif symbol=='native_fn_0205ff80':
            call['resourceName']=bytes(uc.mem_read(words[0],22)).hex();uc.mem_write(CONTEXT+0x25c,struct.pack('<I',fixture['opened']))
        elif symbol=='native_fn_02065730':
            call['cursorArgument']=struct.unpack_from('<I',stack)[0];uc.mem_write(CONTEXT+0x25c,struct.pack('<I',fixture['allocated']));result=fixture['amount']
        calls.append(call)
        for n,register in enumerate(C.REGISTERS[:4]+[R.UC_ARM_REG_R12]):uc.reg_write(register,0xcafe0000+len(calls)*16+n)
        uc.reg_write(R.UC_ARM_REG_R0,result);uc.reg_write(R.UC_ARM_REG_CPSR,((ordinal+len(calls))%16)<<28|0x10);uc.reg_write(R.UC_ARM_REG_PC,uc.reg_read(R.UC_ARM_REG_LR))
    vm.hook_add(unicorn.UC_HOOK_CODE,code);vm.hook_add(unicorn.UC_HOOK_MEM_WRITE,memory);vm.emu_start(address,STOP+4,count=1000)
    if not returned:raise ValueError('Actual initializer did not return')
    registers=[vm.reg_read(r) for r in C.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13]!=SP:raise ValueError('Initializer callee-saved/SP differs')
    expected=['native_fn_02061944','native_fn_0201d444','native_fn_0205ff80','native_fn_02065730','native_fn_0205ff9c'];failures=[]
    if [c['symbol'] for c in calls]!=expected:failures.append('Independent resource initializer provider order')
    else:
        if calls[1]['words'][1]!=0x20de394 or calls[1].get('sourceBytes')!=prefix.hex() or calls[2].get('resourceName')!=prefix.hex():failures.append('Exact copied terminated resource name')
        if calls[3]['words']!=[CONTEXT+0x1c,59,0,2] or calls[3]['cursorArgument']!=fixture['opened']:failures.append('Row1 and exact allocator arguments after resource-open mutation')
    struct.pack_into('<I',seed,0x25c,(fixture['allocated']+fixture['amount'])&0xffffffff)
    if bytes(vm.mem_read(CONTEXT,len(seed)))!=bytes(seed):failures.append('Fresh post-provider cursor plus amount modulo32; untouched context bytes')
    return dict(actualTopReturn=True,modelFailures=failures,registers=registers,cpsr=vm.reg_read(R.UC_ARM_REG_CPSR),calls=calls,writes=writes,fullRamSha256=hashlib.sha256(bytes(vm.mem_read(0x02000000,0x800000))).hexdigest())
