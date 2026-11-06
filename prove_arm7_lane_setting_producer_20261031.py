import random
import arm7_lane_setting_native_20261031 as fixture
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from project import ROOT,sha256,write_json

CTOR,STOP,FILL=0x027E89EC,0x027E8A10,0x037FE014
WRAM=0x037F8000


def execute(value,offset,seed):
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    if fixture.digest(main)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416' or fixture.digest(wram)!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':
        raise ValueError('Measured host producer modules differ')
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={fixture.BASE:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),
        fixture.DATA:random.Random(seed+19).randbytes(0x4000),fixture.STACK:random.Random(seed+218).randbytes(0x4000),
        fixture.RETURN:bytes(0x1000),fixture.HARDWARE:random.Random(seed+219).randbytes(0x1000)}
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    descriptor=fixture.DATA+0x3000
    target=fixture.DATA+offset
    cpu.mem_write(descriptor,target.to_bytes(4,'little'))
    expected={base:bytearray(cpu.mem_read(base,len(data))) for base,data in regions.items()}
    visited,writes=[],[]
    state={'phase':'prefix'}
    def code(machine,pc,size,unused):
        allowed=(CTOR<=pc<STOP or FILL<=pc<FILL+92) if state['phase']=='prefix' else fixture.ADDRESS<=pc<fixture.ADDRESS+fixture.CODE
        if not allowed or machine.reg_read(UC_ARM_REG_CPSR)&32:
            raise ValueError('Connected work-pointer proof escaped qualified original ARM instructions')
        visited.append(pc)
    def write(machine,access,address,size,word,unused):
        writes.append([address,size,word&((1 << size*8)-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    registers=[random.Random(seed*19+i).getrandbits(32) for i in range(15)]
    registers[0]=descriptor
    registers[-2:]=[fixture.STACK+0x3F00,fixture.RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR,seed%16 << 28 | 0xD3)
    for register,word in zip(match_runtime.REGISTERS,registers):
        cpu.reg_write(register,word)
    cpu.emu_start(CTOR,STOP,count=10000,timeout=100000)
    if cpu.reg_read(UC_ARM_REG_PC)!=STOP or visited[-1]!=FILL+88 or cpu.reg_read(match_runtime.REGISTERS[-1])!=STOP:
        raise ValueError('Original producer did not reach its natural helper-return prefix boundary')
    if int.from_bytes(cpu.mem_read(fixture.POINTER,4),'little')!=target:
        raise ValueError('Original descriptor word0 was not stored into absolute work-pointer storage')
    nonstack=[row for row in writes if not fixture.STACK<=row[0]<fixture.STACK+0x4000]
    expected_writes=[[fixture.POINTER,4,target]]+[[target+index,4,0] for index in range(0,0x694,4)]
    if nonstack!=expected_writes:
        raise ValueError('Actual constructor pointer/whole-context clear store order differs')
    expected[WRAM][fixture.POINTER-WRAM:fixture.POINTER-WRAM+4]=target.to_bytes(4,'little')
    expected[fixture.DATA][offset:offset+0x694]=bytes(0x694)
    for base,data in regions.items():
        if base!=fixture.STACK and bytes(cpu.mem_read(base,len(data)))!=bytes(expected[base]):
            raise ValueError('Producer prefix changed unmodeled non-stack bytes')
    prefix=dict(boundaryStop=hex(STOP),outerActualReturn=False,outerReturnCredit=0,actualOriginalFillReturns=1,
        descriptor=hex(descriptor),descriptorWord0=hex(target),producedWord=hex(fixture.POINTER),clearBytes=0x694,
        instructionCount=len(visited),orderedNonstackWritesSha256=fixture.digest(repr(nonstack).encode()),
        registers=[cpu.reg_read(register) for register in match_runtime.REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR))
    state['phase']='setter'
    first=len(writes)
    cpu.reg_write(match_runtime.REGISTERS[0],value)
    cpu.reg_write(match_runtime.REGISTERS[-1],fixture.RETURN)
    cpu.emu_start(fixture.ADDRESS,fixture.RETURN,count=500,timeout=100000)
    if cpu.reg_read(UC_ARM_REG_PC)!=fixture.RETURN:
        raise ValueError('Setter did not actually return after measured producer prefix')
    expected_setter=[]
    if value<=255:
        expected_setter=[[target+0x32A,2,value],[fixture.REGISTER,2,value]]
        expected[fixture.DATA][offset+0x32A:offset+0x32C]=value.to_bytes(2,'little')
        expected[fixture.HARDWARE][fixture.REGISTER-fixture.HARDWARE:fixture.REGISTER-fixture.HARDWARE+2]=value.to_bytes(2,'little')
    if writes[first:]!=expected_setter or cpu.reg_read(match_runtime.REGISTERS[0])!=(0 if value<=255 else 5):
        raise ValueError('Connected setter guard/return/ordered stores differ')
    if any(bytes(cpu.mem_read(base,len(data)))!=bytes(expected[base]) for base,data in regions.items() if base!=fixture.STACK):
        raise ValueError('Connected setter changed unmodeled memory')
    return dict(value=value,target=hex(target),seed=seed,prefix=prefix,setterActualReturn=True,
        setterRegisters=[cpu.reg_read(register) for register in match_runtime.REGISTERS],setterWrites=writes[first:],
        finalRegions={hex(base):fixture.digest(bytes(cpu.mem_read(base,len(data)))) for base,data in regions.items()},sourceCredit=0)


def main():
    records=[execute(value,offset,seed) for seed,(value,offset) in enumerate((value,offset)
        for value in (0,1,255,256,0x80000000,0xFFFFFFFF) for offset in (0x40,0x800))]
    report=dict(generator='prove_arm7_lane_setting_producer_20261031.py',generatorSha256=sha256(__file__),
        inputMainSha256=sha256(ROOT/'extract/arm7/runtime/arm7-main.bin'),inputWramSha256=sha256(ROOT/'extract/arm7/runtime/arm7-wram.bin'),
        program='',processor='arm7',module='arm7-main',mode='arm',producer='0x027e89ec',storage='0x0380fff4',storageBytes=4,
        origin='incoming descriptor word0',realContextClearBytes=0x694,records=records,scenarios=len(records),
        actualSetterReturns=len(records),actualOriginalFillReturns=len(records),constructorActualReturns=0,
        constructorReturnCredit=0,sourceCredit=0,moduleBssOwnership=False,originalDataSourceCredit=0,
        limitations=['Natural prefix boundary after real context clearing; the464-byte constructor does not return or finish in this proof',
            'Setter is invoked explicitly using produced context; no natural caller/scene/thread reachability claim',
            'External absolute runtime pointer storage is not initialized module data or BSS; physical hardware remains unverified'])
    destination=ROOT/'evidence/attempts/arm7-lane-setting-producer-20261031.json'
    write_json(destination,report)
    print(dict(report=destination.relative_to(ROOT).as_posix(),sha256=sha256(destination),scenarios=len(records),setterReturns=len(records),outerConstructorReturns=0))


if __name__=='__main__':
    main()
