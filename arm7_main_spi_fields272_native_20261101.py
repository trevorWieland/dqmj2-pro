import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x027e0000
HELPER=0x027f54f0
COMMANDS={0x027f5a24:0xdb,0x027f5aac:0xd8}
CONTROL=0x040001c0
DATA=CONTROL+2
STACK=0x03030000
STOP=0x0f000000
VALUES=(0,1,255,256,65535,65536,0x12345678,0x80000000,0xffffffff)

def cases():
    return [dict(address=a,busyPattern=list(pattern),stickyPattern=[0xff7f,0x8802,0x4002])for a in VALUES for pattern in((0,),(1,2,3),(3,0,1))]+[dict(address=0xa5000000|(((73*i+19)&255)<<16)|(((29*i+11)&255)<<8)|i,busyPattern=[i%3,(i//3)%4,(i//7)%4],stickyPattern=[0xff7f,0x8802,0x4002])for i in range(256)]

def execute(original,entry,code,helper_code,case,index,budget=5000,allow_no_return=False):
    rng=random.Random(entry*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(entry,code);cpu.mem_write(HELPER,helper_code);before=bytes(cpu.mem_read(BASE,0x20000));cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(STOP,4096)
    mode=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=case['address'];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    returned=False;phase=0;poll=0;reads=[];writes=[];supplied=[];own_visited=[];helper_visited=[];pending=None;nested=[]
    def instruction(machine,address,width,user):
        nonlocal returned,pending
        if address==STOP:returned=True;machine.emu_stop();return
        if pending is not None and address==pending['lr']:
            pending['result']=machine.reg_read(REGISTERS[0]);pending['actualReturn']=True;pending['abiPreserved']=machine.reg_read(REGISTERS[-2])==pending['sp']and[machine.reg_read(x)for x in REGISTERS[4:12]]==pending['saved'];nested.append(pending);pending=None
        if address==HELPER:pending=dict(argument=machine.reg_read(REGISTERS[0]),lr=machine.reg_read(REGISTERS[-1]),sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(x)for x in REGISTERS[4:12]])
        if entry<=address<entry+len(code)-8:own_visited.append(address)
        elif HELPER<=address<HELPER+len(helper_code)-4:helper_visited.append(address)
        else:raise ValueError('Address-field chain fetched pool, original tail or provider')
    def write(machine,access,address,width,value,user):
        nonlocal phase,poll
        if address in(CONTROL,DATA)and width==2:
            writes.append([address,width,value&65535])
            if address==DATA:phase+=1;poll=0
        elif STACK+0x7f0<=address and address+width<=STACK+0x800 and width==4:writes.append([address,width,value&0xffffffff])
        else:raise ValueError('Address-field write escaped frame or halfword ports')
    def read(machine,access,address,width,value,user):
        nonlocal poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            if phase>4:raise ValueError('Unexpected address-field control phase')
            b=case['busyPattern'][phase%len(case['busyPattern'])];s=case['stickyPattern'][phase%len(case['stickyPattern'])];raw=(s&~0x80)|(0x80 if poll<b or case.get('stuck')==phase else 0);poll+=1;supplied.append(dict(phase=phase,value=raw));machine.mem_write(CONTROL,struct.pack('<H',raw))
        elif (entry+len(code)-8<=address and address+width<=entry+len(code)and width==4)or(HELPER+len(helper_code)-4<=address and address+width<=HELPER+len(helper_code)and width==4):pass
        elif STACK+0x7f0<=address and address+width<=STACK+0x800 and width==4:pass
        else:raise ValueError('Address-field read escaped pools, saved frame or control halfword')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=len(nested),lastPhase=phase,stuckPhaseReached=case.get('stuck')==phase,instructionCount=len(own_visited)+len(helper_visited),postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded address-field chain did not return')
    a=case['address'];parts=[(a>>16)&255,(a>>8)&255,a&255];expected_stack=bytearray(bytes([0xa5])*4096);struct.pack_into('<IIII',expected_stack,0x7f0,*[initial[i]for i in(3,4,5,14)]);expected_writes=[[STACK+0x7f0+4*j,4,initial[i]]for j,i in enumerate((3,4,5,14))]+[[CONTROL,2,0x8900],[DATA,2,COMMANDS[entry]],[DATA,2,parts[0]],[DATA,2,parts[1]],[CONTROL,2,0x8100],[DATA,2,parts[2]]];expected_supply=[]
    for p in range(5):
        b=case['busyPattern'][p%len(case['busyPattern'])];s=case['stickyPattern'][p%len(case['stickyPattern'])];expected_supply.extend(dict(phase=p,value=(s&~0x80)|(0x80 if i<b else 0))for i in range(b+1))
    result=case['stickyPattern'][4%len(case['stickyPattern'])]&~0x80;expected_io=bytearray(io_before);struct.pack_into('<HH',expected_io,0x1c0,result,parts[2]);expected_nested=[(parts[i],case['stickyPattern'][(i+2)%len(case['stickyPattern'])]&~0x80)for i in range(3)];lower=[(x['argument'],x['result'])for x in nested]==expected_nested and all(x['abiPreserved']for x in nested)and pending is None
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    checks=dict(abi=abi,nested=lower,writes=writes==expected_writes,supplied=supplied==expected_supply,ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==bytes(expected_stack),io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io),result=cpu.reg_read(REGISTERS[0])==result,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==((index%16)&3)|4)
    return dict(actualOwnReturn=True,actualNestedReturns=len(nested),modelPassed=all(checks.values()),modelChecks=checks,result=cpu.reg_read(REGISTERS[0]),nested=nested,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x20000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedHalfwordInputs=supplied,visitedOwn=sorted(set(own_visited)),visitedHelper=sorted(set(helper_visited)),providerReplacements=[],physicalPeripheralExecution=False,sourceCreditAssignedByHarness=0)
