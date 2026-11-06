import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS as REGS
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ,UcError
from unicorn.arm_const import UC_CPU_ARM_946,UC_ARM_REG_CPSR,UC_ARM_REG_PC
from main_frame_heap_wrappers108_native_20261101 import DATA,GLOBAL,STACK,STOP,CREATOR,ALLOCATOR,HELPERS,creator_case,allocation_case

CORE={0x0202B54C:72,0x0202B594:128,0x0202B614:124}
CORE_CODE={0x0202B54C:68,0x0202B594:128,0x0202B614:124}


def execute(image,entry,body,index,budget=20000,core_code_lengths=None):
    maker=creator_case if entry==CREATOR else allocation_case
    pages,expected,initial,result,rng,spec=maker(image,index)
    cpu=Uc(UC_ARCH_ARM,UC_MODE_ARM);cpu.ctl_set_cpu_model(UC_CPU_ARM_946)
    cpu.mem_map(0x02000000,0x800000);cpu.mem_write(0x02000000,image);cpu.mem_write(entry,body)
    for address,page in zip([DATA,GLOBAL],pages):cpu.mem_write(address,bytes(page))
    cpu.mem_map(STACK,4096);cpu.mem_write(STACK,bytes([0xA5])*4096);cpu.mem_map(STOP,4096)
    initial[-2:]=[STACK+0x800,STOP|(index&1)];control=0x10|(index%4<<6);cpu.reg_write(UC_ARM_REG_CPSR,index%16<<28|control)
    for reg,value in zip(REGS,initial):cpu.reg_write(reg,value)
    pending=[];returned=[];core_returns=[];calls=[];reads=[];writes=[];visited=[];stopped=False
    def code(machine,address,width,user):
        nonlocal stopped
        while pending and pending[-1][1]==address:
            done=pending.pop();returned.append(done[0])
            if done[0]in CORE:
                if [machine.reg_read(r)for r in REGS[4:12]]!=done[2]or machine.reg_read(REGS[-2])!=done[3]:
                    raise ValueError('Owned core helper callee-save/stack ABI differs at actual return')
                core_returns.append(dict(address=hex(done[0]),registers=[machine.reg_read(r)for r in REGS],
                    cpsr=machine.reg_read(UC_ARM_REG_CPSR),pagesSha256=hashlib.sha256(b''.join(bytes(machine.mem_read(a,4096))for a in(DATA,GLOBAL))).hexdigest()))
        if address==STOP:stopped=True;machine.emu_stop();return
        if address in HELPERS:
            sp=machine.reg_read(REGS[-2]);calls.append([address,[machine.reg_read(r)for r in REGS[:4]],struct.unpack('<I',machine.mem_read(sp,4))[0]])
            pending.append((address,machine.reg_read(REGS[-1])&~1,[machine.reg_read(r)for r in REGS[4:12]],machine.reg_read(REGS[-2])))
        for start,total in CORE.items():
            if start<=address<start+total:
                code_length=(core_code_lengths or CORE_CODE)[start]
                if address>=start+code_length:raise ValueError('Owned core entered a literal/original tail outside freshly generated code')
        if not(entry<=address<entry+len(body)or any(a<=address<a+n for a,n in HELPERS.items())):raise ValueError('Frame heap instruction escaped qualified native/source scope')
        visited.append(address)
    def write(machine,access,address,width,value,user):
        if not(any(a<=address and address+width<=a+4096 for a in(DATA,GLOBAL))or STACK+0x600<=address and address+width<=STACK+0x800):
            raise ValueError('Frame heap write crossed disposable backing boundary')
        writes.append([address,width,value&((1<<(8*width))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    cpu.hook_add(UC_HOOK_MEM_READ,lambda machine,access,address,width,value,user:reads.append([address,width]))
    failure=None
    try:cpu.emu_start(entry,STOP+4,count=budget)
    except (UcError,ValueError) as error:failure=dict(type=type(error).__name__,reason=str(error),pc=hex(cpu.reg_read(UC_ARM_REG_PC)))
    if not stopped:
        return dict(case=spec,actualOwnReturn=False,postStateExcluded=True,failure=failure or dict(type='InstructionCapOrBoundary',reason='No actual return'),
            instructionCount=len(visited),observedCompletedHelperReturnsBeforeStop=returned,sourceCredit=0)
    if pending or cpu.reg_read(REGS[-2])!=STACK+0x800:raise ValueError('Frame heap return stack/nested return evidence differs')
    if any(cpu.reg_read(REGS[i])!=initial[i]for i in range(4,12))or cpu.reg_read(UC_ARM_REG_CPSR)&0xDF!=control:raise ValueError('Frame heap callee-save/control ABI differs')
    if bytes(cpu.mem_read(STACK,0x600))!=bytes([0xA5])*0x600 or bytes(cpu.mem_read(STACK+0x800,0x800))!=bytes([0xA5])*0x800:raise ValueError('Frame heap outer stack guards differ')
    actual=[bytes(cpu.mem_read(a,4096))for a in(DATA,GLOBAL)];value=cpu.reg_read(REGS[0])
    return dict(case=spec,actualOwnReturn=True,actualOwnedCoreReturns=core_returns,modelPassed=spec['modelDomain']and actual==expected and value==result,
        expectedResult=result,result=value,rawRegisters=[cpu.reg_read(r)for r in REGS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
        mappedMemorySha256=hashlib.sha256(bytes(cpu.mem_read(0x02000000,0x800000))).hexdigest(),
        stackSha256=hashlib.sha256(bytes(cpu.mem_read(STACK,4096))).hexdigest(),pagesSha256=hashlib.sha256(b''.join(actual)).hexdigest(),expectedPagesSha256=hashlib.sha256(b''.join(expected)).hexdigest(),
        orderedReads=reads,orderedWrites=writes,typedCallObservations=calls,actualOriginalHelperReturnsSeparate=returned,
        visited=sorted(set(visited)),instructionCount=len(visited),providerReplacements=[])
