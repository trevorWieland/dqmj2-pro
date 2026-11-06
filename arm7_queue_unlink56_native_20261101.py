import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
ENTRY=0x037FD84C
BASE=0x037F8000
QUEUE=0x038078B4
NODE=0x03809100
PREVIOUS=0x03809200
NEXT=0x03809300
STACK=0x03030000
STOP=0x0F000000

def execute(original,code,index,budget=2000):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE,0x18000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,code)
    cpu.mem_write(QUEUE,rng.randbytes(32));cpu.mem_write(NODE-32,rng.randbytes(0x300))
    kind=index%5;node=0 if kind==0 else NODE
    previous=PREVIOUS if kind in (2,4) else 0;following=NEXT if kind in (3,4) else 0
    if kind==4 and index//5%8==0:following=previous
    if kind==4 and index//5%8==1:previous=following=NODE
    def put(address,value):cpu.mem_write(address,struct.pack('<I',value))
    if node:
        put(NODE+20,previous);put(NODE+24,following)
        put(QUEUE+12,previous or NODE);put(QUEUE+16,following or NODE)
        if previous and previous!=NODE:put(previous+24,NODE)
        if following and following!=NODE:put(following+20,NODE)
    before=bytes(cpu.mem_read(BASE,0x18000));expected=bytearray(before);expected_writes=[];expected_reads=[]
    def store(address,value):struct.pack_into('<I',expected,address-BASE,value);expected_writes.append([address,4,value])
    if node:
        expected_reads=[[NODE+24,4],[NODE+20,4]]
        if following:store(following+20,previous)
        else:expected_reads.append([ENTRY+52,4]);store(QUEUE+16,previous)
        if previous:store(previous+24,following)
        else:expected_reads.append([ENTRY+52,4]);store(QUEUE+12,following)
    residue=0 if not node else QUEUE if not following or not previous else NODE
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xA5])*4096);cpu.mem_map(STOP,4096)
    control=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=node;initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    writes=[];reads=[];visited=[];stopped=False
    allowed={QUEUE+12,QUEUE+16}|{p+offset for p in (NODE,PREVIOUS,NEXT)for offset in (20,24)}
    def instruction(machine,address,width,user):
        nonlocal stopped
        if address==STOP:stopped=True;machine.emu_stop();return
        if not ENTRY<=address<ENTRY+len(code)-4:raise ValueError('Unlink entered an original tail, literal or external provider')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        if width!=4 or address not in allowed:raise ValueError('Unlink store escaped the explicitly mapped prefix fields')
        writes.append([address,width,value&0xffffffff])
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda machine,access,address,width,value,user:reads.append([address,width]))
    cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not stopped or cpu.reg_read(REGISTERS[-2])!=STACK+0x800:raise ValueError('Unlink did not return')
    if any(cpu.reg_read(REGISTERS[i])!=initial[i]for i in range(4,12))or cpu.reg_read(UC_ARM_REG_CPSR)&0xDF!=control:raise ValueError('Unlink callee-save/control ABI differs')
    if bytes(cpu.mem_read(STACK,4096))!=bytes([0xA5])*4096:raise ValueError('Leaf unlink changed its stack')
    actual=bytes(cpu.mem_read(BASE,0x18000));observed=cpu.reg_read(REGISTERS[0])
    return dict(modelPassed=actual==bytes(expected)and writes==expected_writes and reads==expected_reads and observed==residue,
        kind=kind,syntheticAliases=kind==4 and index//5%8 in (0,1),actualOwnReturn=True,observedR0Residue=observed,semanticCReturnValueClaimed=False,
        rawRegisters=[cpu.reg_read(reg)for reg in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
        mappedMemorySha256=hashlib.sha256(actual).hexdigest(),expectedMappedMemorySha256=hashlib.sha256(expected).hexdigest(),
        orderedWrites=writes,orderedReads=reads,visited=sorted(set(visited)),instructionCount=len(visited),providerReplacements=[])
