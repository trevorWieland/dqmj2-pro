import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x027e0000
HELPER=0x027f54f0
COMMANDS={0x027f580c:0xa,0x027f5918:2}
CONTROL=0x040001c0
DATA=CONTROL+2
STACK=0x03030000
INPUT=0x03040000
STOP=0x0f000000
ADDRESSES=(0,1,255,256,65535,65536,0x12345678,0x80000000,0xffffffff,0x12fe,0x12ff,0xfffffffe)
COUNTS=(0,1,2,3,4,16,255,256,257,0x80000001,0xffffffff)

def transfer_count(address,count):
    if not count:return 0,count,-1
    effective=count
    if (((address+count-1)&0xffffffff)>>8)>(address>>8):effective=(0x100-(address&255))&65535
    bound=(effective-1)&0xffffffff
    if bound&0x80000000:bound-=0x100000000
    return max(bound,0)+1,effective,bound

def cases():
    rows=[dict(address=a,count=n,busyPattern=list(p),stickyPattern=[0xff7f,0x8802,0x4002])for a,n,p in itertools.product(ADDRESSES,COUNTS,((0,),(1,2,3),(3,0,1)))]
    return rows+[dict(address=0xa5000000|(((73*i+19)&255)<<16)|(((29*i+11)&255)<<8)|i,count=1,firstByte=i,busyPattern=[i%3,(i//3)%4,(i//7)%4],stickyPattern=[0xff7f,0x8802,0x4002])for i in range(256)]

def execute(original,entry,code,helper_code,case,index,budget=15000,allow_no_return=False):
    rng=random.Random(entry*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(entry,code);cpu.mem_write(HELPER,helper_code);before=bytes(cpu.mem_read(BASE,0x20000));cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(INPUT,4096);data=bytearray(rng.randbytes(4096));pointer=INPUT+(0,1,64,255,511,3800)[index%6]
    if 'firstByte'in case:data[pointer-INPUT]=case['firstByte']
    cpu.mem_write(INPUT,bytes(data));mode=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:3]=[case['address'],case['count'],pointer];initial[-2:]=[STACK+0x800,STOP|(index&1)];cpu.mem_map(STOP,4096)
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    phase=0;poll=0;returned=False;writes=[];reads=[];supplied=[];own_visited=[];helper_visited=[];pending=None;nested=[]
    def instruction(machine,address,width,user):
        nonlocal returned,pending
        if address==STOP:returned=True;machine.emu_stop();return
        if pending is not None and address==pending['lr']:
            pending['result']=machine.reg_read(REGISTERS[0]);pending['actualReturn']=True;pending['abiPreserved']=machine.reg_read(REGISTERS[-2])==pending['sp']and[machine.reg_read(x)for x in REGISTERS[4:12]]==pending['saved'];nested.append(pending);pending=None
        if address==HELPER:pending=dict(argument=machine.reg_read(REGISTERS[0]),lr=machine.reg_read(REGISTERS[-1]),sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(x)for x in REGISTERS[4:12]])
        if entry<=address<entry+len(code)-8:own_visited.append(address)
        elif HELPER<=address<HELPER+len(helper_code)-4:helper_visited.append(address)
        else:raise ValueError('Write chain fetched pool, original tail or provider')
    def write(machine,access,address,width,value,user):
        nonlocal phase,poll
        if address in(CONTROL,DATA)and width==2:
            writes.append([address,width,value&65535])
            if address==DATA:phase+=1;poll=0
        elif STACK+0x7f0<=address and address+width<=STACK+0x800 and width in(2,4):writes.append([address,width,value&((1<<(8*width))-1)])
        else:raise ValueError('Write chain store escaped frame or halfword ports')
    def read(machine,access,address,width,value,user):
        nonlocal poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            b=case['busyPattern'][phase%len(case['busyPattern'])];s=case['stickyPattern'][phase%len(case['stickyPattern'])];raw=(s&~0x80)|(0x80 if poll<b or case.get('stuck')==phase else 0);poll+=1;supplied.append(dict(phase=phase,value=raw));machine.mem_write(CONTROL,struct.pack('<H',raw))
        elif(entry+len(code)-8<=address and address+width<=entry+len(code)and width==4)or(HELPER+len(helper_code)-4<=address and address+width<=HELPER+len(helper_code)and width==4):pass
        elif STACK+0x7f0<=address and address+width<=STACK+0x800 and width in(2,4):pass
        elif INPUT<=address and address+width<=INPUT+4096 and width==1:pass
        else:raise ValueError('Write chain read escaped input, stack, pools or control')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualNestedReturns=len(nested),lastPhase=phase,stuckPhaseReached=case.get('stuck')==phase,instructionCount=len(own_visited)+len(helper_visited),postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded write chain did not return')
    count,effective,bound=transfer_count(case['address'],case['count']);expected_stack=bytearray(bytes([0xa5])*4096);struct.pack_into('<II',expected_stack,0x7f8,initial[4],initial[-1]);expected_writes=[[STACK+0x7f8,4,initial[4]],[STACK+0x7fc,4,initial[-1]]];expected_io=bytearray(io_before);expected_supply=[];result=case['address'];lower=not nested;expected_flags=8
    if count:
        a=case['address'];high=(a>>16)&255;middle=(a>>8)&255;low=a&255;struct.pack_into('<HHH',expected_stack,0x7f0,high,middle,low);expected_writes.extend([[STACK+0x7f2,2,middle],[STACK+0x7f0,2,high],[STACK+0x7f4,2,low],[CONTROL,2,0x8900],[DATA,2,COMMANDS[entry]],[DATA,2,high],[DATA,2,middle],[DATA,2,low]])
        if pointer-INPUT+count>4096:raise ValueError('Unsupported expected input extent')
        for i in range(count):
            if i==count-1:expected_writes.append([CONTROL,2,0x8100])
            expected_writes.append([DATA,2,data[pointer-INPUT+i]])
        last=count+4;result=case['stickyPattern'][last%len(case['stickyPattern'])]&~0x80;struct.pack_into('<HH',expected_io,0x1c0,result,data[pointer-INPUT+count-1]);lower=len(nested)==1 and nested[0]['argument']==data[pointer-INPUT+count-1]and nested[0]['result']==result and nested[0]['abiPreserved']
        for p in range(last+1):
            b=case['busyPattern'][p%len(case['busyPattern'])];s=case['stickyPattern'][p%len(case['stickyPattern'])];expected_supply.extend(dict(phase=p,value=(s&~0x80)|(0x80 if i<b else 0))for i in range(b+1))
        expected_flags=6 if bound>=0 else 5 if bound==-0x80000000 else 4
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    projection=bytearray(cpu.mem_read(BASE,0x20000));projection[entry-BASE:entry-BASE+len(code)]=original[entry-BASE:entry-BASE+len(code)]
    checks=dict(abi=abi,nested=lower,orderedPortWrites=[x for x in writes if x[0]in(CONTROL,DATA)]==[x for x in expected_writes if x[0]in(CONTROL,DATA)],supplied=supplied==expected_supply,ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==bytes(expected_stack),io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io),input=bytes(cpu.mem_read(INPUT,4096))==bytes(data),result=cpu.reg_read(REGISTERS[0])==result,flags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==expected_flags)
    return dict(nonCodeRamSha256=hashlib.sha256(projection).hexdigest(),callerCodeRangeExcludedOnlyFromCrossBuildRamHash=True,actualOwnReturn=True,actualNestedReturns=len(nested),functionalModelPassed=all(checks.values()),nativeStackWriteOrderPassed=writes==expected_writes,modelChecks=checks,rawResult=cpu.reg_read(REGISTERS[0]),effectiveCount=effective,signedLoopBound=bound,transferredBytes=count,nested=nested,rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x20000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),inputSha256=hashlib.sha256(cpu.mem_read(INPUT,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedHalfwords=supplied,visitedOwn=sorted(set(own_visited)),visitedHelper=sorted(set(helper_visited)),providerReplacements=[],physicalPeripheralExecution=False,sourceCreditAssignedByHarness=0)
