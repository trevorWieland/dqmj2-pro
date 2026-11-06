import hashlib
import random

from ov001_ability28_fixture_20261031 import REGS
from ov006_prepare236_models_20261031 import CONTEXT,construct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY,STOP,SP=0x021E2F68,0x08000000,0x0301FF00
NATIVE={0x02063EE0:12,0x02063EEC:12,0x02067B58:12,0x02008D78:148,0x021E2F58:16}


def execute(main,overlay,recipe,candidate=None):
    machine=Uc(UC_ARCH_ARM,UC_MODE_ARM);machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for a,n in [(0x02000000,0x400000),(0x03000000,0x20000),(STOP,0x1000)]:machine.mem_map(a,n)
    machine.mem_write(0x02000000,main);machine.mem_write(0x021D7240,overlay)
    if candidate is not None:
        if len(candidate)!=252:raise ValueError('Prepare236 preserve252 caller bytes')
        machine.mem_write(ENTRY,candidate)
    rng=random.Random(recipe['seed']);machine.mem_write(0x03000000,rng.randbytes(0x20000))
    initial,expected,services,native,result=construct(recipe)
    for a,b in initial:machine.mem_write(a,b)
    expected_ram=bytearray(machine.mem_read(0x02000000,0x400000))
    for a,b in expected:expected_ram[a-0x02000000:a-0x02000000+len(b)]=b
    values=[rng.getrandbits(32)for r in REGS]
    for r,v in zip(REGS,values):machine.reg_write(r,v)
    machine.reg_write(UC_ARM_REG_CPSR,rng.getrandbits(4)<<28|0x10);machine.reg_write(UC_ARM_REG_SP,SP);machine.reg_write(UC_ARM_REG_LR,STOP)
    calls,entries,frames,returned,trace,writes,observed=[],[],[],[],[],[],set()
    def before(engine,event):
        if any(bytes(engine.mem_read(a,len(b)))!=b for a,b in event['before']):raise ValueError('Prepare236 independent ordered state differs')
    def step(engine,pc,width,data):
        while frames and pc==frames[-1]['returnAddress']:
            frame=frames.pop()
            if engine.reg_read(UC_ARM_REG_SP)!=frame['sp']or[engine.reg_read(r)for r in REGS[4:12]]!=frame['preserved']or engine.reg_read(REGS[0])!=frame['result']:
                raise ValueError('Prepare236 actual native return/frame differs')
            returned.append(dict(address=hex(frame['address']),result=engine.reg_read(REGS[0])))
        if pc==STOP:engine.emu_stop();return
        trace.append(pc)
        if len(trace)>1000 or engine.reg_read(UC_ARM_REG_CPSR)&255!=0x10:raise ValueError('Prepare236 bounded ARM mode differs')
        if pc in NATIVE:
            i=len(entries)
            if i>=len(native)or native[i]['address']!=pc:raise ValueError('Prepare236 native entry order differs')
            event=native[i];before(engine,event)
            arguments=[engine.reg_read(REGS[k])for k in range(len(event['arguments']))]
            if arguments!=event['arguments']:raise ValueError('Prepare236 native helper arguments differ')
            entries.append(dict(address=hex(pc),arguments=arguments))
            frames.append(dict(address=pc,returnAddress=engine.reg_read(UC_ARM_REG_LR)&~1,result=event['result'],sp=engine.reg_read(UC_ARM_REG_SP),preserved=[engine.reg_read(r)for r in REGS[4:12]]))
        if ENTRY<=pc<ENTRY+244:observed.update(range(pc,pc+width));return
        if any(a<=pc<a+n for a,n in NATIVE.items()):return
        i=len(calls)
        if i>=len(services)or pc!=services[i]['address']:raise ValueError(('Prepare236 independent provider order differs',hex(pc),i))
        event=services[i];before(engine,event)
        arguments=[engine.reg_read(REGS[k])for k in range(len(event['arguments']))]
        if arguments!=event['arguments']:raise ValueError(('Prepare236 independent provider arguments differ',arguments,event['arguments']))
        calls.append(dict(address=hex(pc),arguments=arguments,result=event['result'],effects=[dict(address=hex(a),bytesHex=b.hex())for a,b in event['effects']]))
        for a,b in event['effects']:engine.mem_write(a,b)
        engine.reg_write(REGS[0],event['result'])
        for k in [1,2,3,12]:engine.reg_write(REGS[k],(recipe['seed']*0x9E3779B9+i*13+k)&0xFFFFFFFF)
        engine.reg_write(UC_ARM_REG_PC,engine.reg_read(UC_ARM_REG_LR))
    def written(engine,access,a,n,value,data):
        if not(0x03000000<=a<=SP-n or any(base<=a and a+n<=base+len(b)for base,b in initial)):raise ValueError('Prepare236 unexpected native write region')
        writes.append((a,n,value))
    machine.hook_add(UC_HOOK_CODE,step);machine.hook_add(UC_HOOK_MEM_WRITE,written)
    machine.emu_start(ENTRY,STOP+4,count=1001)
    actual=[machine.reg_read(r)for r in REGS]
    expected_returns=[dict(address=hex(n['address']),result=n['result'])for n in native]
    if machine.reg_read(UC_ARM_REG_PC)!=STOP or machine.reg_read(UC_ARM_REG_SP)!=SP or frames or actual[0]!=result or actual[4:12]!=values[4:12]or returned!=expected_returns or len(calls)!=len(services):raise ValueError('Prepare236 actual caller/native return protocol differs')
    ram=bytes(machine.mem_read(0x02000000,0x400000))
    if ram!=expected_ram:raise ValueError('Prepare236 complete independent RAM differs')
    return dict(actualReturn=True,returnWord=actual[0],restoredSP=True,preservedRegisters=actual[4:12],nativeDependencyActualReturns=returned,providedCalls=calls,instructions=len(trace)-len(calls),observedCallerInstructionBytes=sorted(observed),ramSha256=hashlib.sha256(ram).hexdigest(),stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000,0x20000))).hexdigest(),pcTrace=trace,writes=writes)
