import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
ENTRY=0x027f6074
MAIN=0x027e0000
PACKER=0x037fe410
SENDER=0x037fe448
DISABLE=0x037fdd00
RESTORE=0x037fdd14
WRAM=0x037f8000
CONTROL=0x04000184
PORT=CONTROL+4
STACK=0x03030000
STOP=0x0f000000
VALUES=(0,1,127,128,255,256,0x12345678,0x80000000,0xffffffff)
SEQUENCES=((0,),(2,0),(0x4000,0),(2,2,0),(0x4000,2,0x4000,0))

def cases():
    rows=[dict(selector=a,value=b,statuses=list(states))for a,b,states in itertools.product(VALUES,VALUES,SEQUENCES)]
    return rows+[dict(selector=0x12340000|i,value=0x80000000|((73*i+19)&255),statuses=list(SEQUENCES[i%5]))for i in range(256)]

def execute(main,wram,own,pack,send,case,index,budget=10000,allow_no_return=False):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T);cpu.mem_map(MAIN,0x20000);cpu.mem_write(MAIN,main);cpu.mem_write(ENTRY,own);main_before=bytes(cpu.mem_read(MAIN,0x20000));cpu.mem_map(WRAM,0x18000);cpu.mem_write(WRAM,wram);cpu.mem_write(PACKER,pack);cpu.mem_write(SENDER,send);wram_before=bytes(cpu.mem_read(WRAM,0x18000));cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));io_before=bytes(cpu.mem_read(0x04000000,4096));cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(STOP,4096)
    mode=0x1f|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|mode);initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:2]=[case['selector'],case['value']];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    spans={ENTRY:len(own),PACKER:56,SENDER:92,DISABLE:20,RESTORE:24};visits={a:[]for a in spans};writes=[];reads=[];supplied=[];pending=[];returns=[];attempts=[];attempt=-1;returned=False
    def instruction(machine,address,width,user):
        nonlocal returned,attempt
        if address==STOP:returned=True;machine.emu_stop();return
        if pending and address==pending[-1]['lr']:
            frame=pending.pop();frame['result']=machine.reg_read(REGISTERS[0]);frame['actualReturn']=True;frame['abiPreserved']=machine.reg_read(REGISTERS[-2])==frame['sp']and[machine.reg_read(x)for x in REGISTERS[4:12]]==frame['saved'];returns.append(frame)
        if address in(PACKER,SENDER,DISABLE,RESTORE):
            if address==PACKER:attempt+=1;attempts.append([machine.reg_read(x)for x in REGISTERS[:4]])
            pending.append(dict(entry=address,attempt=attempt,arguments=[machine.reg_read(x)for x in REGISTERS[:(3 if address==PACKER else 1)]],lr=machine.reg_read(REGISTERS[-1]),sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(x)for x in REGISTERS[4:12]]))
        for start,size in spans.items():
            if start<=address<start+size:visits[start].append(address);return
        raise ValueError('PXI retry chain fetched pool or unqualified original provider')
    def write(machine,access,address,width,value,user):
        if not((address==CONTROL and width==2)or(address==PORT and width==4)or(STACK+0x7e0<=address and address+width<=STACK+0x800 and width==4)):raise ValueError('PXI retry write escaped bounded frames or two ports')
        writes.append([address,width,value&((1<<(8*width))-1)])
    def read(machine,access,address,width,value,user):
        reads.append([address,width])
        if address==CONTROL and width==2:
            if attempt<0:raise ValueError('FIFO read without actual packer call')
            if attempt>=len(case['statuses'])and not case.get('repeatLast'):raise ValueError('Retry exceeded supplied finite status sequence')
            status=case['statuses'][min(attempt,len(case['statuses'])-1)];supplied.append(dict(attempt=attempt,value=status));machine.mem_write(CONTROL,struct.pack('<H',status))
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualPackerReturns=sum(x['entry']==PACKER for x in returns),actualSenderReturns=sum(x['entry']==SENDER for x in returns),actualIrqReturns=sum(x['entry']in(DISABLE,RESTORE)for x in returns),attemptsStarted=len(attempts),postStateCredit=0,returnCredit=0)
        raise ValueError('Finite PXI retry chain did not return')
    payload=((case['selector']<<8)&0x7f00)|0x8000|(case['value']&255);packed=5|((payload&0x3ffffff)<<6);statuses=case['statuses'];n=len(statuses);expected_attempts=[[5,payload,0,initial[3]if i==0 else packed]for i in range(n)];expected_writes=[[STACK+0x7f0+4*j,4,initial[i]]for j,i in enumerate((4,5,6,14))];expected_returns=[]
    for i,status in enumerate(statuses):
        expected_writes.extend([[STACK+0x7e8,4,initial[3]if i==0 else packed],[STACK+0x7ec,4,ENTRY+48],[STACK+0x7e8,4,packed],[STACK+0x7e0,4,0],[STACK+0x7e4,4,PACKER+48]])
        if status&0x4000:expected_writes.append([CONTROL,2,status|0xc000]);result=0xffffffff
        else:
            expected_returns.extend([(DISABLE,mode&0x80),(RESTORE,0x80)])
            if status&2:result=0xfffffffe
            else:expected_writes.append([PORT,4,packed]);result=0
        expected_returns.extend([(SENDER,result),(PACKER,result)])
    expected_stack=bytearray(bytes([0xa5])*4096);struct.pack_into('<IIIIIIII',expected_stack,0x7e0,0,PACKER+48,packed,ENTRY+48,initial[4],initial[5],initial[6],initial[-1]);expected_io=bytearray(io_before);struct.pack_into('<H',expected_io,0x184,0);struct.pack_into('<I',expected_io,0x188,packed);expected_supplied=[dict(attempt=i,value=status)for i,status in enumerate(statuses)for unused in range(2)]
    lower=[(x['entry'],x['result'])for x in returns]==expected_returns and all(x['abiPreserved']for x in returns)and all(x['arguments']==[packed]for x in returns if x['entry']==SENDER)and all(x['arguments']==[mode&0x80]for x in returns if x['entry']==RESTORE)and not pending
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==mode
    checks=dict(abi=abi,nested=lower,arguments=attempts==expected_attempts,writes=writes==expected_writes,supplied=supplied==expected_supplied,main=bytes(cpu.mem_read(MAIN,0x20000))==main_before,wram=bytes(cpu.mem_read(WRAM,0x18000))==wram_before,stack=bytes(cpu.mem_read(STACK,4096))==bytes(expected_stack),io=bytes(cpu.mem_read(0x04000000,4096))==bytes(expected_io),result=cpu.reg_read(REGISTERS[0])==0,scratchR3=cpu.reg_read(REGISTERS[3])==packed,finalFlags=cpu.reg_read(UC_ARM_REG_CPSR)>>28==6)
    return dict(modelPassed=all(checks.values()),modelChecks=checks,actualOwnReturn=True,actualPackerReturns=sum(x['entry']==PACKER for x in returns),actualSenderReturns=sum(x['entry']==SENDER for x in returns),actualIrqReturns=sum(x['entry']in(DISABLE,RESTORE)for x in returns),result=cpu.reg_read(REGISTERS[0]),rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),mainSha256=hashlib.sha256(cpu.mem_read(MAIN,0x20000)).hexdigest(),wramSha256=hashlib.sha256(cpu.mem_read(WRAM,0x18000)).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),ioSha256=hashlib.sha256(cpu.mem_read(0x04000000,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,suppliedFifoHalfwords=supplied,attemptArguments=attempts,nestedReturns=returns,visits={hex(a):sorted(set(v))for a,v in visits.items()},providerReplacements=[],physicalPeripheralExecution=False)
