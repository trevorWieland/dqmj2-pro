import prove_arm7_lock_bitmap_region_20261031_v2 as region
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR

PROGRAM='dwc/utility.bin/move/child.srl'
ADDRESS,SIZE,CODE=0x037fc0b8,136,120


def cases():
    return [dict(flag=flag,owner=owner,words=words,passes=passes)
        for flag in (0,1,2,0xffffffff) for owner in (0,1,0x7f,0xffff)
        for words in ((0,0),(0xffffffff,0xffffffff),(0x12345678,0x80000001)) for passes in (1,2)]


def setup(body,case,seed):
    if len(body)!=SIZE:raise ValueError('Full child lock initializer extent differs')
    machine=region.setup(PROGRAM,seed);cpu=machine['cpu'];cpu.mem_write(ADDRESS,body)
    cpu.mem_write(region.BITS,b''.join(w.to_bytes(4,'little') for w in case['words']))
    reads,writes,visited=[],[],set()
    def code(uc,pc,size,unused):
        if not ADDRESS<=pc<ADDRESS+CODE:raise ValueError('Child initializer escaped owned code; wait/Bios execution is forbidden')
        visited.add(pc)
    def read(uc,access,address,size,value,unused):reads.append([address,size])
    def write(uc,access,address,size,value,unused):writes.append([address,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.update(case=case,reads=reads,writes=writes,visited=visited)
    original_invoke=machine['invoke']
    def observed(*args,**kwargs):
        result=original_invoke(*args,**kwargs);machine['lastExecution']=result
        return result
    machine['invoke']=observed
    return machine


def execute(machine,budget=5000):
    cpu=machine['cpu'];case=machine['case'];steps=[];flag=case['flag'];owner=case['owner']
    for index in range(case['passes']):
        machine['reads'].clear();machine['writes'].clear();machine['visited'].clear()
        if budget==1:
            cpu.mem_write(machine['config']['flag'],flag.to_bytes(4,'little'));cpu.mem_write(region.LOCK+4,owner.to_bytes(2,'little'))
            result=machine['invoke']('init',budget=budget)
            if result['actualReturn']:raise ValueError('Prologue exhaustion gained return')
            return dict(actualReturn=False,execution=result,returnCredit=0,postBoundaryStateExcluded=True)
        result=region.initialize(machine,flag,owner);machine['lastExecution']=result['execution']
        if not result['execution']['actualReturn']:
            return dict(actualReturn=False,actualWaitBoundary=result['execution']['actualWaitBoundary'],execution=result['execution'],
                ownInstructionsBeforeBoundary=sorted(machine['visited']),returnCredit=0,originalWaitOrBiosExecutionCredit=0,postBoundaryStateExcluded=True)
        steps.append(dict(nativeModel=result,registers=[cpu.reg_read(r) for r in region.match_runtime.REGISTERS],cpsr=cpu.reg_read(UC_ARM_REG_CPSR),
            orderedReads=machine['reads'][:],orderedWrites=machine['writes'][:],ownVisited=sorted(machine['visited']),
            completeMemorySha256={hex(first):region.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()}))
        flag=int.from_bytes(cpu.mem_read(machine['config']['flag'],4),'little');owner=0
    return dict(actualReturn=True,actualEntryReturns=len(steps),steps=steps,waitOrBiosCalls=0,constructorOrKernelReachabilityClaim=False,
        sharedBitmapDataSourceCredit=0,independentCompleteNonstackMemoryAndOrderedWriteModel=True,meaningfulReturnType='void; incidental R0 and full register effects compared')
