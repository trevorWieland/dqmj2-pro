import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from match_runtime import REGISTERS
MAIN,WRAM,DATA,STACK,IO,STOP,WORD=0x027e0000,0x037f8000,0x023c0000,0x03030000,0x04808000,0x0f000000,0x0380fff4
TOP,SIZE,CODE=0x027ea1b8,504,496
UPDATES=[(0x1b0,0,0x58c),(0x1b2,8,0x588),(0x1b2,0,0x598),(0x1b4,8,0x594),(0x1b4,0,0x590),(0x1b6,8,0x59c),(0x1b6,0,0x574),(0x1b8,0,0x584),(0x1ba,0,0x55c),(0x1bc,8,0x56c),(0x1bc,0,0x580),(0x1be,0,0x578),(0x1be,8,0x57c),(0x1c0,0,0x548),(0x1d0,8,0x5b4)]+[(0x1d2+2*(i//2),8*(i%2),0x5b8+4*i)for i in range(14)]

def cases():
    return[dict(byte=byte,pattern=pattern,contextOffset=(0,4,8,12,0x100,0x104)[(byte+pattern)%6])for pattern in range(4)for byte in range(256)]

def run(main,wram,case,index,body=None,budget=1000):
    if body is not None:
        if len(body)!=SIZE:raise ValueError('Counter compiled extent differs')
        main=main[:TOP-MAIN]+body+main[TOP-MAIN+SIZE:]
    rng=random.Random(0x149000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    regions={MAIN:main+bytes(0x20000-len(main)),WRAM:wram+bytes(0x18000-len(wram)),DATA:rng.randbytes(0x8000),STACK:rng.randbytes(0x4000),IO:rng.randbytes(0x1000),STOP:bytes(0x1000)}
    for address,raw in regions.items():cpu.mem_map(address,len(raw));cpu.mem_write(address,raw)
    context=DATA+case['contextOffset'];cpu.mem_write(DATA+0x7000,struct.pack('<I',context));phase='prefix';prefix=[];reads=[];writes=[];visited=[];fill_entries=[];returned=[False]
    def code(machine,pc,size,user):
        if phase=='prefix':
            if not(0x027e89ec<=pc<0x027e8a10 or 0x037fe014<=pc<0x037fe014+92):raise ValueError('Counter producer escaped qualified original prefix/fill')
            if pc==0x037fe014:fill_entries.append([machine.reg_read(REGISTERS[-1]),machine.reg_read(REGISTERS[-2])])
            return
        if pc==STOP:returned[0]=True;machine.emu_stop();return
        if size!=4 or machine.reg_read(UC_ARM_REG_CPSR)&32 or not TOP<=pc<TOP+CODE:raise ValueError('Counter fetched outside complete ARM body')
        visited.append(pc)
    def write(machine,access,address,width,value,user):
        row=[address,width,value&((1<<(width*8))-1)]
        if phase=='prefix':prefix.append(row);return
        if width!=4 or address-context not in{r[2]for r in UPDATES}:raise ValueError('Counter store escaped qualified29 fields')
        writes.append(row)
    def read(machine,access,address,width,value,user):
        if phase=='prefix':return
        if not(address in(TOP+CODE,TOP+CODE+4,WORD)and width==4 or address-context in{r[2]for r in UPDATES}and width==4 or address-IO in{r[0]for r in UPDATES}and width==2):raise ValueError('Counter read escaped pools/runtime word/counters/ports')
        reads.append([address,width])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(REGISTERS[0],DATA+0x7000);cpu.reg_write(REGISTERS[-2],STACK+0x3f00);cpu.reg_write(REGISTERS[-1],STOP)
    cpu.emu_start(0x027e89ec,0x027e8a10,count=10000)
    outside=[r for r in prefix if not STACK<=r[0]<STACK+0x4000]
    if cpu.reg_read(UC_ARM_REG_PC)!=0x027e8a10 or outside!=[[WORD,4,context]]+[[context+i,4,0]for i in range(0,0x694,4)]or len(fill_entries)!=1:raise ValueError('Actual pointer producer/fill return or clear extent differs')
    pattern=case['pattern'];byte=case['byte'];ports={}
    for slot,port in enumerate(sorted({r[0]for r in UPDATES})):
        low=(byte if pattern%2==0 else(byte+slot*17)&255);high=((255-byte)if pattern<2 else(byte+slot*31)&255);ports[port]=low|(high<<8);cpu.mem_write(IO+port,struct.pack('<H',ports[port]))
    before={}
    for slot,unused in enumerate(UPDATES):
        off=UPDATES[slot][2];value=(0,0xffffffff,0xffffff00,rng.getrandbits(32))[pattern];before[off]=value;cpu.mem_write(context+off,struct.pack('<I',value))
    expected={address:bytearray(cpu.mem_read(address,len(raw)))for address,raw in regions.items()};expected_reads=[[TOP+CODE,4],[TOP+CODE+4,4],[WORD,4]];expected_writes=[];last_port=None
    for port,shift,off in UPDATES:
        if port!=last_port:expected_reads.append([IO+port,2]);last_port=port
        expected_reads.append([context+off,4]);value=(before[off]+((ports[port]>>shift)&255))&0xffffffff;expected_writes.append([context+off,4,value]);struct.pack_into('<I',expected[DATA],context-DATA+off,value)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[-2:]=[STACK+0x3800,STOP|(index&1)];cpsr=((index%16)<<28)|0x13|((index%4)<<6)
    cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    if case.get('wrongRuntimePointer'):cpu.mem_write(WORD,bytes(4))
    phase='target';cpu.emu_start(TOP,STOP+4,count=budget)
    if not returned[0]:raise ValueError('Counter did not actually return within the bounded instruction budget')
    registers=[cpu.reg_read(r)for r in REGISTERS];expected_registers=list(initial);expected_registers[:4]=[(before[0x5ec]+(ports[0x1de]>>8))&0xffffffff,context,before[0x5e8],ports[0x1de]];expected_registers[12]=ports[0x1dc]
    checks=dict(allRawRegisters=registers==expected_registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR)==cpsr|((index&1)<<5),orderedReads=reads==expected_reads,orderedWrites=writes==expected_writes,allMappedMemory=all(bytes(cpu.mem_read(address,len(raw)))==bytes(raw)for address,raw in expected.items()),completeOwnCode=visited==list(range(TOP,TOP+CODE,4)),actualRuntimeWord=int.from_bytes(cpu.mem_read(WORD,4),'little')==context)
    return dict(case=case,actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),orderedReads=reads,orderedWrites=writes,visited=visited,instructions=len(visited),producer=dict(actualFillReturns=1,constructorActualReturns=0,incomingDescriptor=context,observedClearBytes=0x694),providers=[],physicalDeviceConcurrencyAndReadSideEffectsUnproved=True,semanticVoidApiRawR0Incidental=True,memorySha256={hex(address):hashlib.sha256(cpu.mem_read(address,len(raw))).hexdigest()for address,raw in regions.items()})
