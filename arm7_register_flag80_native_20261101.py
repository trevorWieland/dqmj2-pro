import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x037f8000
CONTROL=0x040001c0
DATA=CONTROL+2
STACK=0x03030000
STOP=0x0f000000
READER=0x03804c7c
WRITER=0x03804c00
HELPER=0x03804c58
ENTRIES=(0x03804cf0,0x03804d14)
VALUES=(0,1,127,128,255,256,0x12345678,0x80000000,0xffffffff)

def cases():
    result=[dict(mask=x,receivedWord=y,busy=[n%4,(n+1)%4,0,(n+2)%4,(n+3)%4],sticky=[0xff7f,0x8802,0x4002,0x4444,0x7f7f])for n,(x,y)in enumerate((x,y)for x in VALUES for y in(0,1,127,128,255,256,0x1234,0x8000,0xffff))]
    return result+[dict(mask=0x1234ab00|i,receivedWord=((73*i+19)&255)|(((29*i)&255)<<8),busy=[i%3,(i//3)%4,(i//7)%4,(i//11)%4,(i//13)%4],sticky=[0xff7f,0x8802,0x4002,0x4444,0x7f7f])for i in range(256)]

def execute(original,bodies,entry,case,index,budget=5000,allow_no_return=False):
    rng=random.Random(entry*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x18000);cpu.mem_write(BASE,original)
    for address,code in bodies.items():cpu.mem_write(address,code)
    before=bytes(cpu.mem_read(BASE,0x18000));cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(STOP,4096)
    mode=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[0]=case['mask'];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    returned=False;writes=[];reads=[];supplied=[];visits={address:[]for address in bodies};nested=[];pending=[];phase=0;poll=0
    pools={entry:0,READER:16,WRITER:12,HELPER:4}
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if pending and address==pending[-1]['lr']:
            value=pending.pop();value['result']=machine.reg_read(REGISTERS[0]);value['actualReturn']=True;value['abiPreserved']=machine.reg_read(REGISTERS[-2])==value['sp']and[machine.reg_read(x)for x in REGISTERS[4:12]]==value['saved'];nested.append(value)
        if address in (READER,WRITER,HELPER):pending.append(dict(entry=address,arguments=[machine.reg_read(x)for x in REGISTERS[:(2 if address==WRITER else 1)]],lr=machine.reg_read(REGISTERS[-1]),sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(x)for x in REGISTERS[4:12]]))
        owners=[start for start,body in bodies.items()if start<=address<start+len(body)-pools[start]]
        if len(owners)!=1:raise ValueError('Flag chain escaped fresh code, fetched pool or entered original provider')
        visits[owners[0]].append(address)
    def write(machine,access,address,width,value,user):
        nonlocal phase,poll
        if address in(CONTROL,DATA)and width==2:
            writes.append([address,width,value&65535])
            if address==DATA:phase+=1;poll=0
        elif STACK+0x7e0<=address and address+width<=STACK+0x800 and width==4:writes.append([address,width,value&0xffffffff])
        else:raise ValueError('Flag chain write escaped stack or two halfword ports')
    def read(machine,access,address,width,value,user):
        nonlocal phase,poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            if phase>4:raise ValueError('Unexpected late control poll')
            raw=(case['sticky'][phase]&~0x80)|(0x80 if poll<case['busy'][phase]or case.get('stuck')==phase else 0);poll+=1;supplied.append(dict(phase=phase,value=raw));machine.mem_write(CONTROL,struct.pack('<H',raw))
        elif address==DATA and width==2:
            if phase!=2:raise ValueError('Unexpected received data read')
            machine.mem_write(DATA,struct.pack('<H',case['receivedWord']));phase=3;poll=0
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=len(nested),instructionCount=sum(map(len,visits.values())),returnCredit=0,postStateCredit=0)
        raise ValueError('Bounded flag chain did not return')
    clear=entry==ENTRIES[1];mask=case['mask'];register_value=case['receivedWord']&255;write_argument=(register_value&~mask)&255 if clear else register_value|mask;result=write_argument&255;held=mask
    expected_stack=bytearray(bytes([0xa5])*4096);struct.pack_into('<IIII',expected_stack,0x7f0,held,entry+(36 if clear else 28),initial[4],initial[-1]);expected_io=bytearray(io_before);struct.pack_into('<HH',expected_io,0x1c0,0x8002,result)
    expected_writes=[[STACK+0x7f8,4,initial[4]],[STACK+0x7fc,4,initial[-1]],[STACK+0x7f0,4,initial[3]],[STACK+0x7f4,4,entry+16],[CONTROL,2,0x8202],[CONTROL,2,0x8802],[DATA,2,0x80],[CONTROL,2,0x8002],[DATA,2,0],[STACK+0x7f0,4,held],[STACK+0x7f4,4,entry+(36 if clear else 28)],[CONTROL,2,0x8202],[CONTROL,2,0x8802],[DATA,2,0],[CONTROL,2,0x8002],[DATA,2,result]]
    expected_supply=[dict(phase=p,value=(case['sticky'][p]&~0x80)|(0x80 if i<case['busy'][p]else 0))for p in range(5)for i in range(case['busy'][p]+1)]
    lower=[(x['entry'],x['arguments'],x['result'])for x in nested];expected_lower=[(HELPER,[0x80],case['sticky'][1]&~0x80),(READER,[0],register_value),(HELPER,[0],case['sticky'][4]&~0x80),(WRITER,[0,write_argument],result)]
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    checks=dict(abi=abi,lower=lower==expected_lower and all(x['abiPreserved']for x in nested)and not pending,writes=writes==expected_writes,supplied=supplied==expected_supply,ram=bytes(cpu.mem_read(BASE,0x18000))==before,stack=bytes(cpu.mem_read(STACK,4096))==bytes(expected_stack),io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io),result=cpu.reg_read(REGISTERS[0])==result)
    return dict(modelPassed=all(checks.values()),modelChecks=checks,actualOwnReturn=True,actualNestedReturns=len(nested),result=cpu.reg_read(REGISTERS[0]),nested=nested,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x18000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedHalfwordInputs=supplied,visits={hex(x):sorted(set(v))for x,v in visits.items()},functionProvidersReplaced=[],physicalPeripheralExecution=False,sourceCreditAssignedByHarness=0)
