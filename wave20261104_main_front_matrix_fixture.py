import hashlib
import struct
import sys
from project import ROOT
sys.path.insert(0,str(ROOT/'deps/native'))
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR,UC_CPU_ARM_946

REGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR]
OBJECT=0x03002000
NORMALIZE=0x02028158
IDENTITY=0x02000ce8
CONCAT=0x02000e1c
ROTATIONS=[0x020280a0,0x02028044,0x02027fe8]


def signed(value):return (value+0x80000000)%0x100000000-0x80000000


def normalize(value):
    value=signed(value)
    while value>0xb4000:value-=0x168000
    while value< -0xb4000:value+=0x168000
    return value&0xffffffff


def rotation(target,angle,seed):
    return [((angle&0xffffffff)*7+(target&0xff)*13+seed*17+i*257)&0xffffffff for i in range(9)]


def combine(left,right):
    return [(left[i]*3+right[(i+1)%9]*5+i*11)&0xffffffff for i in range(9)]


def expected(address,v,wrong=False):
    output=bytearray(v['object'])
    values=list(struct.unpack_from('<3I',output,0x88))
    old=values[1]
    calls=[]
    if address==0x0204202c:
        values=v['args'][:3]
        output[9]|=1
    elif address==0x02042104:
        values[1]=normalize(old+v['args'][0])
        calls.append(dict(address=NORMALIZE,input=(old+v['args'][0])&0xffffffff))
        output[9]|=int(old!=v['args'][0])
    else:
        values=[normalize(a+b) for a,b in zip(values,v['args'][:3])]
        calls.extend(dict(address=NORMALIZE,input=(a+b)&0xffffffff) for a,b in zip(struct.unpack_from('<3I',output,0x88),v['args'][:3]))
        output[9]|=1
    struct.pack_into('<3I',output,0x88,*values)
    if v['update'] and output[9]:
        calls.append(dict(address=IDENTITY))
        calls.extend(dict(address=target,input=values[index]) for target,index in zip(ROTATIONS,[2,1,0]))
        b=rotation(ROTATIONS[0],values[2],v['seed'])
        c=rotation(ROTATIONS[1],values[1],v['seed'])
        d=rotation(ROTATIONS[2],values[0],v['seed'])
        a=combine(b,c) if wrong else combine(c,b)
        result=combine(d,a)
        calls.append(dict(address=CONCAT,left=c,right=b))
        calls.append(dict(address=CONCAT,left=d,right=a))
        struct.pack_into('<9I',output,0x94,*result)
        output[9]=0
    return bytes(output),calls,old


def vector(seed,address):
    angles=[0,1,-1,0x7ff,0x800,-0x800,0xb4000,0xb4001,-0xb4000,-0xb4001,0x168000,-0x168000]
    initial=bytearray((i*17+seed*29)&255 for i in range(0x200))
    initial[9]=[0,1,0x80,0xff][seed%4]
    args=[angles[seed%12]&0xffffffff,angles[(seed+3)%12]&0xffffffff,angles[(seed+7)%12]&0xffffffff]
    struct.pack_into('<3I',initial,0x88,*[(x+seed*7)&0xffffffff for x in args])
    if address==0x02042104 and seed in [1,5]:
        initial[9]=0
        struct.pack_into('<I',initial,0x8c,args[0])
    update=0 if seed%4==0 else 1
    registers=[(0x18230101*(i+1)+seed*257)&0xffffffff for i in range(15)]
    registers[:4]=[OBJECT,*args]
    if address==0x02042104:registers[:3]=[OBJECT,args[0],update]
    registers[-2:]=[0x0301fff0,0x03018000]
    return dict(seed=seed,object=bytes(initial),args=args,update=update,registers=registers,flags=((seed&15)<<28)|0x1f)


def run(code,address,bindings,v):
    uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000,0x100000)
    uc.mem_map(0x03000000,0x20000)
    uc.mem_write(address,code)
    uc.mem_write(OBJECT,v['object'])
    uc.mem_write(v['registers'][-2],struct.pack('<I',v['update']))
    uc.reg_write(UC_ARM_REG_CPSR,v['flags'])
    for register,value in zip(REGS,v['registers']):uc.reg_write(register,value)
    targets={int(b['address'],0) for b in bindings.values() if b['kind']=='function'}
    calls=[];writes=[];returned=False

    def store(pointer,values):
        data=struct.pack('<9I',*values)
        uc.mem_write(pointer,data)
        writes.append(dict(origin='provided-matrix-contract',address=pointer,bytes=36,valueSha256=hashlib.sha256(data).hexdigest()))

    def on_code(machine,pc,size,user):
        nonlocal returned
        if pc==v['registers'][-1]:
            returned=True;machine.emu_stop();return
        if pc in targets:
            r0,r1,r2=[machine.reg_read(r) for r in REGS[:3]]
            if pc==NORMALIZE:
                calls.append(dict(address=pc,input=r0));result=normalize(r0)
            elif pc==IDENTITY:
                calls.append(dict(address=pc));store(r0,[0x1000,0,0,0,0x1000,0,0,0,0x1000]);result=0x55110000+v['seed']
            elif pc in ROTATIONS:
                calls.append(dict(address=pc,input=r1));store(r0,rotation(pc,r1,v['seed']));result=0x66220000+v['seed']
            elif pc==CONCAT:
                left=list(struct.unpack('<9I',bytes(machine.mem_read(r0,36))))
                right=list(struct.unpack('<9I',bytes(machine.mem_read(r1,36))))
                calls.append(dict(address=pc,left=left,right=right));store(r2,combine(left,right));result=0x77330000+v['seed']
            else:raise AssertionError('Unmodeled matrix import')
            lr=machine.reg_read(UC_ARM_REG_LR)
            for index,register in enumerate([UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12]):machine.reg_write(register,(0xdeb00000+v['seed']*31+index*257)&0xffffffff)
            machine.reg_write(UC_ARM_REG_R0,result)
            machine.reg_write(UC_ARM_REG_CPSR,(((v['seed']+5)&15)<<28)|0x1f)
            machine.reg_write(UC_ARM_REG_PC,lr)
            return
        assert address<=pc<address+len(code)

    def on_write(machine,access,target,size,value,user):writes.append(dict(origin='caller',address=target,bytes=size,value=value&((1<<(size*8))-1)))
    uc.hook_add(UC_HOOK_CODE,on_code)
    uc.hook_add(UC_HOOK_MEM_WRITE,on_write)
    uc.emu_start(address,0,count=1000,timeout=200000)
    assert returned
    final=[uc.reg_read(r) for r in REGS]
    assert final[4:12]==v['registers'][4:12] and final[-2]==v['registers'][-2]
    return dict(calls=calls,object=bytes(uc.mem_read(OBJECT,0x200)).hex(),registers=final,cpsr=uc.reg_read(UC_ARM_REG_CPSR),writes=writes,ramSha256=hashlib.sha256(bytes(uc.mem_read(0x03000000,0x20000))).hexdigest())


def execute(address,native,source,bindings):
    cases=[]
    rejected=0
    equivalent=0
    for seed in range(12):
        v=vector(seed,address)
        original=run(native,address,bindings,v)
        rebuilt=run(source,address,bindings,v)
        assert original==rebuilt
        memory,calls,old=expected(address,v)
        assert original['object']==memory.hex() and original['calls']==calls
        if address==0x02042104:assert original['registers'][0]==old
        altered=expected(address,v,True)[0]
        if altered!=memory:
            assert original['object']!=altered.hex()
            rejected+=1
        else:equivalent+=1
        cases.append(dict(seed=seed,stateSha256=hashlib.sha256(repr(original).encode()).hexdigest()))
    return dict(modelCases=12,actualOriginalCallerReturns=12,actualSourceCallerReturns=12,actualNativeAndSourceCallerReturns=24,allGprsCpsrOrderedCallerAndProvidedWritesRamCompared=True,calleeSavedAndStackAbiChecked=True,wrongOperandModelControlsRejected=rejected,equivalentSkippedUpdateControls=equivalent,providedMatrixContractIsNotNativeMatrixExecution=True,providedCombineOperation='Noncommutative tagged nine-word output; not a matrix-math correctness claim',providedNormalizerWordContract=True,nativeCalleeBodiesExecuted=0,gameHardwareOrTrigonometryExecutionCredit=0,cases=cases)
