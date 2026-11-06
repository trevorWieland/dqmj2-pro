import hashlib
import itertools
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
from match_runtime import REGISTERS
MAIN,WRAM,DATA,STACK,STOP=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x0f000000
READ,WRITE=0x027ead5c,0x027ead30
def cases():
    result=[]
    for parity,byte,pattern in itertools.product((0,1),range(256),range(4)):
        old=(0,65535,(byte^0xa5)|(byte<<8),byte|((255-byte)<<8))[pattern]
        result.append(dict(parity=parity,data=byte,oldHalfword=old))
    return result
def run(main,wram,entry,case,index,body=None,budget=100):
    if hashlib.sha256(main).hexdigest()!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'or hashlib.sha256(wram).hexdigest()!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Original host ARM7 main/WRAM input hashes differ')
    size=28 if entry==READ else 44 if entry==WRITE else 0
    if not size:raise ValueError('Byte helper entry unqualified')
    if body is not None:
        if len(body)!=size:raise ValueError('Byte helper source extent differs')
        main=main[:entry-MAIN]+body+main[entry-MAIN+size:]
    rng=random.Random(0x159000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x4000),STACK:rng.randbytes(0x4000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    backing=DATA+0x1000;pointer=0 if case.get('invalidBacking')else backing+case['parity'];cpu.mem_write(backing,struct.pack('<H',case['oldHalfword']));expected={a:bytearray(cpu.mem_read(a,len(raw)))for a,raw in regions.items()};reads=[];writes=[];visited=[];returned=[False]
    def code(machine,pc,width,user):
        if pc==STOP:returned[0]=True;machine.emu_stop();return
        if width!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not entry<=pc<entry+size:raise ValueError('Byte helper escaped complete ARM body')
        visited.append(pc)
    def read(machine,access,address,width,value,user):
        if(address,width)!=(backing,2):raise ValueError('Byte helper read outside readable aligned halfword')
        reads.append([address,width])
    def write(machine,access,address,width,value,user):
        if entry!=WRITE or(address,width)!=(backing,2):raise ValueError('Byte helper wrote outside single aligned halfword')
        writes.append([address,width,value&65535])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=pointer
    if entry==WRITE:initial[1]=case['data']
    initial[-2:]=[STACK+0x3f00,STOP|(index&1)];cpsr=((index%16)<<28)|0x13|((index%4)<<6);cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    cpu.emu_start(entry,STOP+4,count=budget)
    if not returned[0]:raise ValueError('Byte helper did not actually return in bounded execution')
    expected_registers=list(initial);old=case['oldHalfword']
    if entry==READ:expected_registers[0]=(old>>(8*case['parity']))&255;expected_writes=[]
    else:
        half=(old&255)|(case['data']<<8)if case['parity']else(old&65280)|case['data'];expected_registers[1]=half;expected_registers[2]=old&(255 if case['parity']else 65280);struct.pack_into('<H',expected[DATA],0x1000,half);expected_writes=[[backing,2,half]]
    expected_cpsr=(cpsr&~0xc0000000)|(0 if case['parity']else 0x40000000)|((index&1)<<5)
    checks=dict(allRawRegisters=[cpu.reg_read(r)for r in REGISTERS]==expected_registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR)==expected_cpsr,oneAlignedHalfwordRead=reads==[[backing,2]],orderedWrites=writes==expected_writes,allMappedMemory=all(bytes(cpu.mem_read(a,len(raw)))==bytes(raw)for a,raw in expected.items()),completeCode=visited==list(range(entry,entry+size,4)))
    return dict(entry=hex(entry),case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=[cpu.reg_read(r)for r in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,visited=visited,memorySha256={hex(a):hashlib.sha256(cpu.mem_read(a,len(raw))).hexdigest()for a,raw in regions.items()},providers=[],physicalBusAndInvalidBackingUnproved=True)
