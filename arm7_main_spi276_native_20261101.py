import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
BASE=0x027e0000
CONTROL=0x040001c0
DATA=CONTROL+2
STACK=0x03030000
OUTPUT=0x03040000
STOP=0x0f000000
SPECS={0x027f54b0:(64,8,'command',6),0x027f54f0:(36,4,'helper',None),0x027f5514:(64,8,'command',4),0x027f5554:(112,8,'output',5)}

def cases(entry):
    kind=SPECS[entry][2]
    if kind=='helper':
        values=[0x1234ab00|i for i in range(256)]+[0,1,127,128,255,256,0x12345678,0x80000000,0xffffffff]
        return [dict(selector=value,busy=[busy],sticky=[sticky])for value,busy,sticky in itertools.product(values,(0,1,3),(0,0x8802,0xff7f))]
    if kind=='command':return [dict(busy=[a,b],sticky=[c,d])for a,b,c,d in itertools.product((0,1,3),(0,1,3),(0,0x8802,0xff7f),(0,0x8802,0xff7f))]
    edges=[dict(receivedWord=value,busy=list(busy),sticky=[0xff7f,0x8802,0x4002])for value,busy in itertools.product((0,1,127,128,255,256,0x1234,0x8000,0xffff),((0,0,0),(1,2,3),(3,0,1),(0,3,2)))]
    return edges+[dict(receivedWord=((73*i+19)&255)|(((29*i)&255)<<8),busy=[i%3,(i//3)%4,(i//7)%4],sticky=[0xff7f,0x8802,0x4002])for i in range(256)]

def execute(original,entry,code,case,index,budget=5000,allow_no_return=False):
    expected_size,pool,kind,command=SPECS[entry];rng=random.Random(entry*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(BASE,0x20000);cpu.mem_write(BASE,original);cpu.mem_write(entry,code);before=bytes(cpu.mem_read(BASE,0x20000))
    cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(OUTPUT,4096);cpu.mem_write(OUTPUT,rng.randbytes(4096));output_before=bytes(cpu.mem_read(OUTPUT,4096));cpu.mem_map(STOP,4096)
    destination=OUTPUT+(0,1,4,255,511,4095)[index%6];mode=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|mode);initial=[rng.getrandbits(32)for unused in REGISTERS]
    if kind=='helper':initial[0]=case['selector']
    elif kind=='output':initial[0]=destination
    initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    phase=0;poll=0;returned=False;visited=[];writes=[];reads=[];supplied=[]
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if not entry<=address<entry+len(code)-pool:raise ValueError('Main SPI routine fetched a pool, original tail or external provider')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        nonlocal phase,poll
        if address in(CONTROL,DATA)and width==2:
            writes.append([address,width,value&65535])
            if address==DATA:phase+=1;poll=0
        elif kind=='output'and OUTPUT<=address<OUTPUT+4096 and width==1:writes.append([address,width,value&255])
        else:raise ValueError('Main SPI routine write escaped two halfwords or bounded output page')
    def read(machine,access,address,width,value,user):
        nonlocal poll
        reads.append([address,width])
        if address==CONTROL and width==2:
            p=0 if kind=='helper'else phase
            if p>=len(case['busy']):raise ValueError('Unexpected control polling phase')
            raw=(case['sticky'][p]&~0x80)|(0x80 if poll<case['busy'][p]or case.get('stuck')==p else 0);poll+=1;supplied.append(dict(phase=p,value=raw));machine.mem_write(CONTROL,struct.pack('<H',raw))
        elif address==DATA and width==2:
            if kind!='output'or phase!=2:raise ValueError('Unexpected received-halfword read')
            machine.mem_write(DATA,struct.pack('<H',case['receivedWord']))
        elif not(entry+len(code)-pool<=address and address+width<=entry+len(code)and width==4):raise ValueError('Main SPI routine read escaped literal or halfword ports')
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(entry,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,instructionCount=len(visited),postStateCredit=0,returnCredit=0)
        raise ValueError('Bounded main SPI routine did not return')
    expected_io=bytearray(io_before);expected_output=bytearray(output_before)
    if kind=='helper':
        result=case['sticky'][0]&~0x80;expected_writes=[[DATA,2,case['selector']&255]];struct.pack_into('<HH',expected_io,0x1c0,result,case['selector']&255)
    elif kind=='command':
        result=case['sticky'][1]&~0x80;expected_writes=[[CONTROL,2,0x8100],[DATA,2,command]];struct.pack_into('<HH',expected_io,0x1c0,result,command)
    else:
        result=destination;expected_output[destination-OUTPUT]=case['receivedWord']&255;expected_writes=[[CONTROL,2,0x8900],[DATA,2,5],[CONTROL,2,0x8100],[DATA,2,0],[destination,1,case['receivedWord']&255]];struct.pack_into('<HH',expected_io,0x1c0,case['sticky'][2]&~0x80,case['receivedWord'])
    expected_supply=[dict(phase=p,value=(sticky&~0x80)|(0x80 if i<busy else 0))for p,(busy,sticky)in enumerate(zip(case['busy'],case['sticky']))for i in range(busy+1)]
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    checks=dict(abi=abi,writes=writes==expected_writes,supplied=supplied==expected_supply,ram=bytes(cpu.mem_read(BASE,0x20000))==before,stack=bytes(cpu.mem_read(STACK,4096))==bytes([0xa5])*4096,io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io),output=bytes(cpu.mem_read(OUTPUT,4096))==bytes(expected_output),observedR0=cpu.reg_read(REGISTERS[0])==result)
    return dict(actualOwnReturn=True,modelPassed=all(checks.values()),modelChecks=checks,observedR0=cpu.reg_read(REGISTERS[0]),semanticReturnClaim=kind!='output',rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(cpu.mem_read(BASE,0x20000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),outputSha256=hashlib.sha256(cpu.mem_read(OUTPUT,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedHalfwordInputs=supplied,visited=sorted(set(visited)),instructionCount=len(visited),providerReplacements=[],physicalPeripheralExecution=False,sourceCreditAssignedByHarness=0)
