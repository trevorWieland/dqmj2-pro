import arm7_lane_card_priority_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
ADDRESS,SIZE,CODE=0x038026e0,64,60
COMMON,THREAD=0x038090c0,0x03809108
MASK=0xffffffff


def cases(address):
    if address!=ADDRESS:raise ValueError('Unqualified CARD priority setter')
    return [dict(previous=old,priority=new) for old in (0,4,0xffffffff)
        for new in (0,1,3,4,5,16,31,32,0x80000000,0xffffffff)]


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed);cpu=machine['cpu'];cpu.mem_write(0x03807678,bytes(0x0380b4e4-0x03807678))
    prerequisites=[]
    for entry,args in ((0x037fbf64,()),(0x037fc558,()),(0x03802624,())):
        result=machine['invoke'](entry,args)
        if not result['actualReturn']:raise ValueError('Original kernel/scheduler/CARD prerequisite did not return')
        prerequisites.append(dict(entry=hex(entry),arguments=args,actualReturn=True))
    cpu.mem_write(COMMON+0xf0,case['previous'].to_bytes(4,'little'))
    ownwrites,prioritycalls,visited=[],[],[];state=dict(pc=None)
    def code(uc,pc,size,unused):
        state['pc']=pc
        if ADDRESS<=pc<ADDRESS+CODE:visited.append(pc)
        if pc in (0x037fc64c,0x037fc680):raise ValueError('Disabled priority fixture unexpectedly switched context')
        if pc==0x037fc3c0:prioritycalls.append([uc.reg_read(engine.match_runtime.REGISTERS[index]) for index in range(2)])
    def write(uc,access,target,size,value,unused):
        if ADDRESS<=state['pc']<ADDRESS+CODE and not STACK<=target<STACK+0x4000:
            ownwrites.append([target,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.update(case=case,prerequisites=prerequisites,ownWrites=ownwrites,priorityCalls=prioritycalls,ownVisited=visited)
    return machine


def execute(address,body,case,seed,budget=20000):
    machine=setup(address,body,case,seed);execution=machine['invoke'](address,[case['priority']],True,budget)
    if not execution['actualReturn']:return dict(actualReturn=False,execution=execution,postFaultStateExcluded=True)
    expected=[[COMMON+0xf0,4,case['priority']]]
    if machine['ownWrites']!=expected or machine['priorityCalls']!=[[THREAD,case['priority']]]:
        raise ValueError('Independent full-word priority store/helper argument differs')
    cpu=machine['cpu'];actual=[int.from_bytes(cpu.mem_read(target,4),'little') for target in (COMMON+0xf0,THREAD+0x54)]
    if actual!=[case['priority'],case['priority']] or execution['registers'][0]!=case['previous']:
        raise ValueError('Independent full-word previous return/current priority effects differ')
    if machine['helperReturns'][0x037fc3c0]!=1:raise ValueError('Actual original SetThreadPriority did not return once')
    return dict(actualReturn=True,execution=execution,ownOrderedWrites=expected,actualPriorityHelperArguments=machine['priorityCalls'],
        ownVisited=sorted(set(machine['ownVisited'])),finalPriorityWords=actual,originalPrerequisites=machine['prerequisites'],
        schedulerDisabled=True,actualContextTransfers=0,lowerProviders=[],
        independentOwnOrderedStoreAndPriorityReturnModel=True,independentCompleteMemoryEffectsModel=False,
        syntheticCommonPriorityOverride=case['previous']!=4,over31PriorityIsRawSyntheticDomain=case['priority']>31,
        orderedNonstackWrites=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        actualNestedReturns={hex(entry):count for entry,count in sorted(machine['helperReturns'].items())},
        ordinarySchedulingOrGameMeaning=None)
