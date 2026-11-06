import hashlib
import random
from pathlib import Path
import match_runtime
from unicorn import Uc,UcError,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC

ROOT=Path(__file__).resolve().parent
BASE,DATA,STACK,RETURN,WORK,HARDWARE=0x027E0000,0x023C0000,0x023E0000,0x023FF000,0x0380F000,0x04808000
ADDRESS,CODE,SIZE=0x027E8EC8,44,52
POINTER,REGISTER=0x0380FFF4,0x0480802C


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    result=[dict(value=value,pointer=DATA+offset,passes=2) for value in range(256) for offset in (0x40,0x800)]
    result.extend(dict(value=value,pointer=pointer,passes=2) for value in (256,511,65535,0x7FFFFFFF,0x80000000,0xFFFFFFFF)
        for pointer in (0,0x03000000,DATA+0x40))
    return result


def execute(body,case,seed,budget=500):
    raw=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes()
    if digest(raw)!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416' or len(body)!=SIZE:
        raise ValueError('Setting measured ARM7 module/complete body differs')
    main=bytearray(0x20000)
    main[:len(raw)]=raw
    main[ADDRESS-BASE:ADDRESS-BASE+SIZE]=body
    regions={BASE:bytes(main),DATA:random.Random(seed+193).randbytes(0x2000),STACK:random.Random(seed+292).randbytes(0x4000),
        RETURN:bytes(0x1000),WORK:random.Random(seed+222).randbytes(0x1000),HARDWARE:random.Random(seed+999).randbytes(0x1000)}
    regions[WORK]=regions[WORK][:POINTER-WORK]+case['pointer'].to_bytes(4,'little')+regions[WORK][POINTER-WORK+4:]
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for base,data in regions.items():
        cpu.mem_map(base,len(data))
        cpu.mem_write(base,data)
    visited,writes,reads=set(),[],[]
    def code(machine,pc,size,unused):
        if not ADDRESS<=pc<ADDRESS+CODE or machine.reg_read(UC_ARM_REG_CPSR)&32:
            raise ValueError('Setting escaped complete qualified original ARM body')
        visited.add(pc)
    def write(machine,access,target,size,value,unused):
        writes.append([target,size,value&((1 << size*8)-1)])
    def read(machine,access,target,size,value,unused):
        reads.append([target,size])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    records=[]
    expected={base:bytearray(data) for base,data in regions.items()}
    for phase in range(case['passes']):
        registers=[random.Random(seed*31+phase*119+i).getrandbits(32) for i in range(15)]
        registers[0]=case['value']
        registers[-2:]=[STACK+0x3F00,RETURN]
        cpu.reg_write(UC_ARM_REG_CPSR,seed%16 << 28 | 0xD3)
        for register,value in zip(match_runtime.REGISTERS,registers):
            cpu.reg_write(register,value)
        first_write,first_read=len(writes),len(reads)
        fault=None
        try:
            cpu.emu_start(ADDRESS,RETURN,count=budget,timeout=100000)
        except UcError as error:
            fault=error.errno
        returned=cpu.reg_read(UC_ARM_REG_PC)==RETURN
        observed=[cpu.reg_read(r) for r in match_runtime.REGISTERS]
        if returned:
            if case['value']>255:
                expected_result,expected_writes,expected_reads=5,[],[]
            else:
                expected_result=0
                target=case['pointer']+0x32A
                expected_writes=[[target,2,case['value']],[REGISTER,2,case['value']]]
                expected_reads=[[ADDRESS+44,4],[ADDRESS+48,4],[POINTER,4]]
                expected[DATA][target-DATA:target-DATA+2]=case['value'].to_bytes(2,'little')
                expected[HARDWARE][REGISTER-HARDWARE:REGISTER-HARDWARE+2]=case['value'].to_bytes(2,'little')
            if writes[first_write:]!=expected_writes or reads[first_read:]!=expected_reads or observed[0]!=expected_result:
                raise ValueError('Independent full-word guard/read/order/halfword-store/return model differs')
            if any(bytes(cpu.mem_read(base,len(data)))!=bytes(expected[base]) for base,data in regions.items()):
                raise ValueError('Setting changed an unmodeled data/guard/stack/code byte')
            if observed[4:12]!=registers[4:12] or observed[-2:]!=registers[-2:]:
                raise ValueError('Setting actual-return ABI differs')
        records.append(dict(actualReturn=returned,fault=fault,pc=cpu.reg_read(UC_ARM_REG_PC),registers=observed,
            cpsr=cpu.reg_read(UC_ARM_REG_CPSR),writes=writes[first_write:],reads=reads[first_read:],
            regions={hex(base):digest(bytes(cpu.mem_read(base,len(data)))) for base,data in regions.items()}))
        if not returned:
            break
    return dict(states=records,visited=sorted(visited),providerCalls=0,sourceCredit=0)
