import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
ENTRY=0x037FE410
SENDER=0x037FE448
DISABLE=0x037FDD00
RESTORE=0x037FDD14
BASE=0x037F8000
CONTROL=0x04000184
OUTPUT=CONTROL+4
STACK=0x03030000
STOP=0x0F000000

def cases():
    result=[];edges=[(0,0,0),(31,0x3ffffff,1),(32,0x4000000,2),(0xffffffff,0xffffffff,0xffffffff),(0x80000000,0x80000000,0x80000000)]
    for group in range(128):
        rng=random.Random(ENTRY+group);tag,payload,error=edges[group]if group<len(edges)else tuple(rng.getrandbits(32)for unused in range(3))
        for state in range(3):
            for scratch in (0,0xffffffff,1<<(group%32),rng.getrandbits(32)):
                result.append(dict(group=group,state=state,tag=tag,payload=payload,error=error,scratch=scratch))
    return result

def execute(original,pack,send,case,budget=2000,allow_no_return=False):
    group=case['group'];state=case['state'];rng=random.Random(ENTRY*10000+group*3+state);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE,0x18000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,pack);cpu.mem_write(SENDER,send);ram_before=bytes(cpu.mem_read(BASE,0x18000))
    cpu.mem_map(0x04000000,4096);cpu.mem_write(0x04000000,rng.randbytes(4096));status=(0,2,0x4000)[state];cpu.mem_write(CONTROL,struct.pack('<H',status));io_expected=bytearray(cpu.mem_read(0x04000000,4096))
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(STOP,4096)
    control=0x1f|(group%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,group%16<<28|control)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:4]=[case['tag'],case['payload'],case['error'],case['scratch']];initial[-2:]=[STACK+0x800,STOP|(group&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    packed=(case['tag']&31)|((case['error']&1)<<5)|((case['payload']&0x3ffffff)<<6);expected_result=(0,0xfffffffe,0xffffffff)[state]
    if state==0:struct.pack_into('<I',io_expected,0x188,packed)
    if state==2:struct.pack_into('<H',io_expected,0x184,status|0xc000)
    stack_expected=bytearray(bytes([0xa5])*4096);struct.pack_into('<IIII',stack_expected,0x7f0,initial[4],ENTRY+48,packed,initial[-1])
    writes=[];reads=[];visited={ENTRY:[],SENDER:[],DISABLE:[],RESTORE:[]};pending=[];returns=[];returned=False;forwarded=[]
    spans={ENTRY:56,SENDER:92,DISABLE:20,RESTORE:24}
    def instruction(machine,address,width,user):
        nonlocal returned
        if address==STOP:returned=True;machine.emu_stop();return
        if pending and address==pending[-1]['lr']:
            frame=pending.pop();frame['result']=machine.reg_read(REGISTERS[0]);frame['actualReturn']=True
            frame['abiPreserved']=machine.reg_read(REGISTERS[-2])==frame['sp']and [machine.reg_read(x)for x in REGISTERS[4:12]]==frame['saved'];returns.append(frame)
        if address in (SENDER,DISABLE,RESTORE):
            pending.append(dict(entry=address,argument=machine.reg_read(REGISTERS[0]),lr=machine.reg_read(REGISTERS[-1]),sp=machine.reg_read(REGISTERS[-2]),saved=[machine.reg_read(x)for x in REGISTERS[4:12]]))
            if address==SENDER:forwarded.append(machine.reg_read(REGISTERS[0]))
        for start,size in spans.items():
            if start<=address<start+size:visited[start].append(address);return
        raise ValueError('PXI chain entered an unqualified function or literal')
    def write(machine,access,address,width,value,user):
        if not((address==CONTROL and width==2)or(address==OUTPUT and width==4)or(STACK+0x7f0<=address and address+width<=STACK+0x800 and width==4)):raise ValueError('PXI chain store escaped modeled frame/port fields')
        writes.append([address,width,value&((1<<(width*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,lambda m,a,p,w,v,u:reads.append([p,w]))
    cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOuterReturn=False,actualNestedReturns=len(returns),postStateCredit=0,returnCredit=0)
        raise ValueError('PXI chain did not return')
    expected_writes=[[STACK+0x7f8,4,case['scratch']],[STACK+0x7fc,4,initial[-1]],[STACK+0x7f8,4,packed],[STACK+0x7f0,4,initial[4]],[STACK+0x7f4,4,ENTRY+48]]
    if state==0:expected_writes.append([OUTPUT,4,packed])
    if state==2:expected_writes.append([CONTROL,2,status|0xc000])
    send_returns=[x for x in returns if x['entry']==SENDER];irq_returns=[x for x in returns if x['entry']!=SENDER]
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==control
    lower=len(send_returns)==1 and send_returns[0]['result']==expected_result and all(x['abiPreserved']for x in returns)and len(irq_returns)==(0 if state==2 else 2)
    if state!=2:lower=lower and irq_returns[0]['entry']==DISABLE and irq_returns[0]['result']==control&0x80 and irq_returns[1]['entry']==RESTORE and irq_returns[1]['argument']==control&0x80
    actual_ram=bytes(cpu.mem_read(BASE,0x18000));actual_stack=bytes(cpu.mem_read(STACK,4096));actual_io=bytes(cpu.mem_read(0x04000000,4096))
    passed=abi and lower and forwarded==[packed]and cpu.reg_read(REGISTERS[0])==expected_result and cpu.reg_read(REGISTERS[3])==packed and writes==expected_writes and actual_ram==ram_before and actual_stack==bytes(stack_expected)and actual_io==bytes(io_expected)
    return dict(modelPassed=passed,actualOuterReturn=True,actualOwnedSenderReturns=len(send_returns),actualOriginalIrqReturns=len(irq_returns),forwarded=forwarded,result=cpu.reg_read(REGISTERS[0]),rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(actual_ram).hexdigest(),stackSha256=hashlib.sha256(actual_stack).hexdigest(),ioSha256=hashlib.sha256(actual_io).hexdigest(),orderedWrites=writes,orderedReads=reads,nestedReturns=returns,visited={hex(k):sorted(set(v))for k,v in visited.items()},functionProvidersReplaced=[],physicalPeripheralExecution=False)
