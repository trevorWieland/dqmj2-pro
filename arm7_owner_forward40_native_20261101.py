import hashlib
import itertools
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_TI925T,UC_ARM_REG_CPSR
ENTRY=0x03806390
BASE=0x037F8000
CONTEXT=0x03809800
LOCK=0x027FFFE8
STACK=0x03030000
STOP=0x0F000000
TAIL=0x037FBB78
CALLBACK=0x037FBBA8
SPANS={ENTRY:40,TAIL:8,0x037FBB58:20,0x037FBA18:124,CALLBACK:4,0x037FDD2C:20,0x037FDD40:24,0x037FDD14:24}
def cases():
    return [dict(owner=o,held=h,state=s,saved=m,control=c)for o,h,s,m,c in itertools.product((0,1,2,0x7fff,0xffff,0x10000,0xffffffff),(0,1,2,0x7fff,0xffff),(0,1,0xffffffff),(0,0x80),(0,0x40,0x80,0xc0))]
def execute(original,code,case,index,budget=2000,allow_no_return=False):
    rng=random.Random(ENTRY*10000+index);cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE,0x18000);cpu.mem_write(BASE,original);cpu.mem_write(ENTRY,code);cpu.mem_write(CONTEXT-32,rng.randbytes(96));cpu.mem_write(CONTEXT,struct.pack('<II',case['state'],case['saved']));ram_before=bytes(cpu.mem_read(BASE,0x18000))
    cpu.mem_map(0x027ff000,4096);cpu.mem_write(0x027ff000,rng.randbytes(4096));cpu.mem_write(LOCK,struct.pack('<IH',rng.getrandbits(32),case['held']));shared_expected=bytearray(cpu.mem_read(0x027ff000,4096))
    called=case['state']==0;success=called and case['owner']==case['held']
    if success:struct.pack_into('<I',shared_expected,LOCK-0x027ff000,0);struct.pack_into('<H',shared_expected,LOCK+4-0x027ff000,0)
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xa5])*4096);cpu.mem_map(STOP,4096);control=0x1f|case['control'];cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    initial=[rng.getrandbits(32)for unused in REGISTERS];initial[:2]=[case['owner'],CONTEXT];initial[-2:]=[STACK+0x800,STOP|(index&1)]
    for register,value in zip(REGISTERS,initial):cpu.reg_write(register,value)
    reads=[];writes=[];visited={};forwarded=[];tail_result=[];irq_returns=[];pending=[];callbacks=0;returned=False;tail_pending=False;callback_pending=False
    def instruction(machine,address,width,user):
        nonlocal callbacks,returned,tail_pending,callback_pending
        if address==STOP:returned=True;machine.emu_stop();return
        if pending and address==pending[-1]['lr']:
            frame=pending.pop();frame['result']=machine.reg_read(REGISTERS[0]);frame['actualReturn']=True;irq_returns.append(frame)
        if tail_pending and address==ENTRY+24:tail_result.append(machine.reg_read(REGISTERS[0]));tail_pending=False
        if callback_pending and address==0x037fba68:callbacks+=1;callback_pending=False
        if address==TAIL:forwarded.append(machine.reg_read(REGISTERS[0]));tail_pending=True
        if address==CALLBACK:callback_pending=True
        if address in(0x037fdd2c,0x037fdd40,0x037fdd14):pending.append(dict(entry=address,argument=machine.reg_read(REGISTERS[0]),lr=machine.reg_read(REGISTERS[-1])))
        for start,size in SPANS.items():
            if start<=address<start+size:visited.setdefault(hex(start),set()).add(address);return
        raise ValueError('Owner-forward chain entered a literal or unqualified function')
    def write(machine,access,address,width,value,user):
        if not((STACK+0x7e0<=address and address+width<=STACK+0x800 and width==4)or(address==LOCK and width==4)or(address==LOCK+4 and width==2)):raise ValueError('Owner-forward write escaped modeled frame/lock fields')
        writes.append([address,width,value&((1<<(width*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,instruction);cpu.hook_add(UC_HOOK_MEM_WRITE,write);cpu.hook_add(UC_HOOK_MEM_READ,lambda m,a,p,w,v,u:reads.append([p,w]));cpu.emu_start(ENTRY,STOP+4,count=budget)
    if not returned:
        if allow_no_return:return dict(actualOwnReturn=False,actualIrqReturns=len(irq_returns),actualTailChainReturns=len(tail_result),postStateCredit=0,returnCredit=0)
        raise ValueError('Owner-forward context did not return')
    lock_writes=[w for w in writes if LOCK<=w[0]<LOCK+8];expected_lock_writes=[[LOCK+4,2,0],[LOCK,4,0]]if success else[]
    actual_ram=bytes(cpu.mem_read(BASE,0x18000));actual_shared=bytes(cpu.mem_read(0x027ff000,4096));final_control=(control&~0x80)|case['saved']
    abi=cpu.reg_read(REGISTERS[-2])==STACK+0x800 and cpu.reg_read(REGISTERS[-1])==initial[-1]and all(cpu.reg_read(REGISTERS[i])==initial[i]for i in range(4,12))and cpu.reg_read(UC_ARM_REG_CPSR)&0xdf==final_control
    tail_ok=forwarded==([case['owner']]if called else[])and tail_result==([0 if success else 0xfffffffe]if called else[])and callbacks==int(success)
    expected_irq_count=3 if success else 1
    model=abi and tail_ok and len(irq_returns)==expected_irq_count and cpu.reg_read(REGISTERS[0])==control&0x80 and actual_ram==ram_before and actual_shared==bytes(shared_expected)and lock_writes==expected_lock_writes
    return dict(modelPassed=model,actualOwnReturn=True,actualTailChainReturns=len(tail_result),actualOriginalIrqReturns=len(irq_returns),actualOriginalCallbackReturns=callbacks,forwardedOwner=forwarded,tailResults=tail_result,result=cpu.reg_read(REGISTERS[0]),rawRegisters=[cpu.reg_read(x)for x in REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),ramSha256=hashlib.sha256(actual_ram).hexdigest(),sharedPageSha256=hashlib.sha256(actual_shared).hexdigest(),stackSha256=hashlib.sha256(cpu.mem_read(STACK,4096)).hexdigest(),orderedWrites=writes,orderedReads=reads,irqReturns=irq_returns,visited={k:sorted(v)for k,v in visited.items()},providersReplaced=[],physicalDeviceExecution=False)
