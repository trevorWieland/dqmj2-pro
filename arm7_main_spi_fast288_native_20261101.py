import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x027e0000
ENTRY=0x027f56ec
HELPER=0x027f56c8
CONTROL=0x040001c0
DATA=CONTROL+2
STACK=0x03030000
OUTPUT=0x03040000
STOP=0x0f000000
VALUES=(0,1,255,256,65535,65536,0x12345678,0x80000000,0xffffffff)

def cases():
    rows=[dict(address=a,count=n,busyPattern=list(busy),stickyPattern=[0xff7f,0x8802,0x4002],words=[(0,1,255,256,0x1234,0x8000,0xffff)[(i+j)%7]for j in range(16)])for i,(a,n,busy)in enumerate(itertools.product(VALUES,(0,1,2,3,4,8,16),((0,),(1,2,3),(3,0,1))))]
    return rows+[dict(address=0xa5000000|(((73*i+19)&255)<<16)|(((29*i+11)&255)<<8)|i,count=1,busyPattern=[i%3,(i//3)%4,(i//7)%4],stickyPattern=[0xff7f,0x8802,0x4002],words=[((53*i+29)&255)|(((31*i)&255)<<8)])for i in range(256)]

def helper_cases():return [dict(busy=b,sticky=s,scratch=x)for b,s,x in itertools.product((0,1,3),(0,0x8802,0xff7f),VALUES)]

def execute(original,own_code,helper_code,case,index,direct=False,budget=5000,allow_no_return=False):
    start=HELPER if direct else ENTRY;rng=random.Random(start*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,own_code);cpu.mem_write(HELPER,helper_code);before=bytes(cpu.mem_read(BASE,0x20000))
    cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(OUTPUT,4096);cpu.mem_write(OUTPUT,rng.randbytes(4096));output_before=bytes(cpu.mem_read(OUTPUT,4096));cpu.mem_map(STOP,4096)
    destination=OUTPUT+(0,1,64,255,511,4000)[index%6];mode=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|mode);initial=[rng.getrandbits(32)for unused in REGISTERS]
    if direct:initial[0]=case['scratch']
    else:initial[:3]=[case['address'],case['count'],destination]
    initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    returned=False;phase=0;poll=0;writes=[];reads=[];supplied=[];received=[];own_visited=[];helper_visited=[];nested=[];pending=None
    def instruction(machine,address,width,user):
        nonlocal returned,pending
        if address==STOP:returned=True;machine.emu_stop();return
        if pending is not None and address==pending['lr']:
            pending['result']=machine.reg_read(REGISTERS[0]);pending['actualReturn']=True;pending['abiPreserved']=machine.reg_read(REGISTERS[-2])==pending['sp']and[machine.reg_read(x)for x in REGISTERS[4:12]]==pending['saved'];nested.append(pending);pending=None
        if address==HELPER and not direct:pending=dict(lr=machine.reg_read(REGISTERS[-1]),sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(x)for x in REGISTERS[4:12]])
        if ENTRY<=address<ENTRY+len(own_code)-8 and not direct:own_visited.append(address)
        elif HELPER<=address<HELPER+len(helper_code)-4:helper_visited.append(address)
        else:raise ValueError('Read chain fetched a pool, original tail or provider')
    def write(machine,access,address,width,value,user):
        nonlocal phase,poll
        if address in(CONTROL,DATA)and width==2:
            writes.append([address,width,value&65535])
            if address==DATA:phase+=1;poll=0
        elif not direct and STACK+0x7e8<=address and address+width<=STACK+0x800 and width in(2,4):writes.append([address,width,value&((1<<(8*width))-1)])
        elif not direct and OUTPUT<=address<OUTPUT+4096 and width==1:writes.append([address,width,value&255])
        else:raise ValueError('Read chain write escaped bounded stack/output or ports')
    def read(machine,access,address,width,value,user):
        nonlocal poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            b=case['busy']if direct else case['busyPattern'][phase%len(case['busyPattern'])];s=case['sticky']if direct else case['stickyPattern'][phase%len(case['stickyPattern'])];raw=(s&~0x80)|(0x80 if poll<b or case.get('stuck')==phase else 0);poll+=1;supplied.append(dict(phase=phase,value=raw));machine.mem_write(CONTROL,struct.pack('<H',raw))
        elif address==DATA and width==2:
            if direct or phase<6:raise ValueError('Unexpected received-halfword phase')
            i=phase-6
            if i>=case['count']:raise ValueError('Received more words than requested')
            word=case['words'][i%len(case['words'])];received.append(dict(index=i,value=word));machine.mem_write(DATA,struct.pack('<H',word))
        elif (ENTRY+len(own_code)-8<=address and address+width<=ENTRY+len(own_code)and width==4)or(HELPER+len(helper_code)-4<=address and address+width<=HELPER+len(helper_code)and width==4):pass
        elif not direct and STACK+0x7e8<=address and address+width<=STACK+0x800 and width in(2,4):pass
        else:raise ValueError('Read chain read escaped its own pools, stack or ports')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(start,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=len(nested),instructionCount=len(own_visited)+len(helper_visited),lastPhase=phase,stuckPhaseReached=case.get('stuck')==phase,postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded read chain did not return')
    expected_io=bytearray(io_before);expected_output=bytearray(output_before);expected_stack=bytearray(bytes([0xa5])*4096);expected_writes=[];expected_supply=[];expected_received=[]
    if direct:
        result=case['sticky']&~0x80;expected_writes=[[DATA,2,0]];struct.pack_into('<HH',expected_io,0x1c0,result,0);expected_supply=[dict(phase=1,value=(case['sticky']&~0x80)|(0x80 if i<case['busy']else 0))for i in range(case['busy']+1)];lower=not nested
    else:
        count=case['count'];address=case['address'];result=address;struct.pack_into('<IIII',expected_stack,0x7f0,*[initial[i]for i in(3,4,5,14)]);expected_writes=[[STACK+0x7f0+4*j,4,initial[i]]for j,i in enumerate((3,4,5,14))];lower=not nested
        if count:
            high=(address>>16)&255;middle=(address>>8)&255;low=address&255;struct.pack_into('<HHH',expected_stack,0x7e8,high,middle,low);expected_writes.extend([[STACK+0x7ea,2,middle],[STACK+0x7e8,2,high],[STACK+0x7ec,2,low],[CONTROL,2,0x8900],[DATA,2,0xb],[DATA,2,high],[DATA,2,middle],[DATA,2,low],[DATA,2,0]])
            for i in range(count):
                word=case['words'][i%len(case['words'])]
                if i==count-1:expected_writes.append([CONTROL,2,0x8100])
                expected_writes.extend([[DATA,2,0],[destination+i,1,word&255]]);expected_output[destination-OUTPUT+i]=word&255;expected_received.append(dict(index=i,value=word))
            result=case['words'][(count-1)%len(case['words'])];last=count+5;status=case['stickyPattern'][last%len(case['stickyPattern'])]&~0x80;struct.pack_into('<HH',expected_io,0x1c0,status,result)
            for p in range(last+1):
                b=case['busyPattern'][p%len(case['busyPattern'])];s=case['stickyPattern'][p%len(case['stickyPattern'])];expected_supply.extend(dict(phase=p,value=(s&~0x80)|(0x80 if i<b else 0))for i in range(b+1))
            lower=len(nested)==1 and nested[0]['result']==status and nested[0]['abiPreserved']
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    checks=dict(abi=abi,nested=lower,writes=writes==expected_writes,supply=supplied==expected_supply,received=received==expected_received,ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==bytes(expected_stack),io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io),output=bytes(cpu.mem_read(OUTPUT,4096))==bytes(expected_output),result=cpu.reg_read(REGISTERS[0])==result)
    return dict(actualOwnReturn=True,actualNestedReturns=len(nested),modelPassed=all(checks.values()),modelChecks=checks,result=cpu.reg_read(REGISTERS[0]),nested=nested,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x20000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),outputSha256=hashlib.sha256(cpu.mem_read(OUTPUT,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedHalfwordInputs=supplied,receivedHalfwords=received,visitedOwn=sorted(set(own_visited)),visitedHelper=sorted(set(helper_visited)),providerReplacements=[],physicalPeripheralExecution=False,sourceCreditAssignedByHarness=0)
