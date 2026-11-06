import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x027e0000
ENTRY=0x027f5bf4
CONTROL=0x040001c0
DATA=CONTROL+2
STACK=0x03030000
OUTPUT=0x03040000
STOP=0x0f000000


def cases():
    values=[(0,0),(1,65535),(65535,0),(0x1234,0x8000),(0x8000,0x1234),(0xff80,0x80),(255,0xff00),(0xaa55,0x55aa),(65535,65535)]+[((((31*i)&255)<<8)|i,(((73*i)&255)<<8)|((29*i+11)&255))for i in range(256)]
    return [dict(words=list(words),busyPattern=list(busy),stickyPattern=[0xff7f,0x8802,0x4002])for words,busy in itertools.product(values,((0,),(1,2,3,1),(3,0,1,2)))]


def execute(original,code,case,index,budget=2000,allow_no_return=False):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,code);before=bytes(cpu.mem_read(BASE,0x20000));cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,rng.randbytes(4096));stack_before=bytes(cpu.mem_read(STACK,4096));cpu.mem_map(OUTPUT,4096);cpu.mem_write(OUTPUT,rng.randbytes(4096));output_before=bytes(cpu.mem_read(OUTPUT,4096));cpu.mem_map(STOP,4096);pointer=OUTPUT+(0,1,64,255,511,4094)[index%6]
    mode=0x10|((index%4)<<6);flags=index%16;cpu.reg_write(UC_ARM_REG_CPSR,(flags<<28)|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=pointer;initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    returned=False;writes=[];reads=[];supplied=[];received=[];visited=[];phase=0;poll=0
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if not ENTRY<=address<ENTRY+148 or address%4:raise ValueError('Two-byte reader fetched outside complete ARM code')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        nonlocal phase,poll
        if address in(CONTROL,DATA)and width==2:
            writes.append([address,width,value&65535])
            if address==DATA:phase+=1;poll=0
        elif pointer<=address<pointer+2 and width==1:writes.append([address,width,value&255])
        elif STACK+0x7f8<=address and address+width<=STACK+0x800 and width==4:writes.append([address,width,value&0xffffffff])
        else:raise ValueError('Two-byte reader wrote outside measured halfword ports/output pair')
    def read(machine,access,address,width,value,user):
        nonlocal poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            busy=case['busyPattern'][phase%len(case['busyPattern'])];sticky=case['stickyPattern'][phase%len(case['stickyPattern'])];raw=(sticky&~0x80)|(0x80 if poll<busy or case.get('stuck')==phase else 0);poll+=1;supplied.append(dict(phase=phase,value=raw));machine.mem_write(CONTROL,struct.pack('<H',raw))
        elif address==DATA and width==2:
            if phase not in(2,3):raise ValueError('Unexpected received data phase')
            word=case['words'][phase-2];received.append(dict(phase=phase,value=word));machine.mem_write(DATA,struct.pack('<H',word))
        elif ENTRY+148<=address and address+width<=ENTRY+156 and width==4:pass
        elif STACK+0x7f8<=address and address+width<=STACK+0x800 and width==4:pass
        else:raise ValueError('Two-byte reader read outside measured ports/pools')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=0,instructionCount=len(visited),lastPhase=phase,stuckPhaseReached=case.get('stuck')==phase,postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded two-byte reader did not actually return')
    expected_stack=bytearray(stack_before);struct.pack_into('<II',expected_stack,0x7f8,initial[3],initial[-1]);expected_writes=[[STACK+0x7f8,4,initial[3]],[STACK+0x7fc,4,initial[-1]],[CONTROL,2,0x8900],[DATA,2,0x9f],[DATA,2,0],[pointer,1,case['words'][0]&255],[CONTROL,2,0x8100],[DATA,2,0],[pointer+1,1,case['words'][1]&255]];expected_io=bytearray(io_before);status=case['stickyPattern'][3%len(case['stickyPattern'])]&~0x80;struct.pack_into('<HH',expected_io,0x1c0,status,case['words'][1]);expected_output=bytearray(output_before);expected_output[pointer-OUTPUT:pointer-OUTPUT+2]=bytes([x&255 for x in case['words']]);expected_supply=[]
    for p in range(4):
        busy=case['busyPattern'][p%len(case['busyPattern'])];sticky=case['stickyPattern'][p%len(case['stickyPattern'])]&~0x80;expected_supply.extend(dict(phase=p,value=sticky|(0x80 if i<busy else 0))for i in range(busy+1))
    abi=cpu.reg_read(REGISTERS[-2])==initial[-2]and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode;checks=dict(abi=abi,result=cpu.reg_read(REGISTERS[0])==pointer,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==((flags&3)|4),writes=writes==expected_writes,supply=supplied==expected_supply,received=received==[dict(phase=i+2,value=w)for i,w in enumerate(case['words'])],ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==bytes(expected_stack),r3Restored=cpu.reg_read(REGISTERS[3])==initial[3],io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io),output=bytes(cpu.mem_read(OUTPUT,4096))==bytes(expected_output))
    return dict(actualOwnReturn=True,actualNestedReturns=0,modelPassed=all(checks.values()),modelChecks=checks,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x20000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),outputSha256=hashlib.sha256(cpu.mem_read(OUTPUT,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedHalfwords=supplied,receivedHalfwords=received,visited=sorted(set(visited)),providerReplacements=[],physicalPeripheralExecution=False)
