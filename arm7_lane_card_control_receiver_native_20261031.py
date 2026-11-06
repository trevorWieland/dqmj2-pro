import arm7_lane_card_control_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
ADDRESS,SIZE,CODE=0x038031d4,228,224
COMMON,ARGUMENT,SECOND=0x038090c0,DATA,DATA+0x1000
THREAD=COMMON+0x48
MASK=0xffffffff


def cases(address):
    if address!=ADDRESS:raise ValueError('Unqualified protocol receiver')
    rows=[]
    for phase,request,data_values in [(0,0,(0,1,2,15,16,32,0xffffffff,ARGUMENT))]+[(phase,request,(0,ARGUMENT,0xffffffff)) for phase in (1,2,0xffffffff) for request in (0,2,15,16,0xffffffff)]:
        for data in data_values:
            for flags in (0,1,4,0x10,0x14,0xffffffff):
                for other in (False,True):rows.append(dict(tag=11,enabled=1,phase=phase,request=request,data=data,flags=flags,other=other))
    rows.extend(dict(tag=11,enabled=0xffffffff,phase=0,request=0,data=request,flags=0,other=False) for request in range(32))
    rows.extend(dict(tag=tag,enabled=enabled,phase=1,request=0,data=0xffffffff,flags=0x14,other=True)
        for tag,enabled in ((10,1),(12,1),(0xffffffff,1),(11,0)))
    return rows


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed);cpu=machine['cpu'];cpu.mem_write(0x03807678,bytes(0x0380b4e4-0x03807678))
    prerequisites=[]
    for entry,args in ((0x037fbf64,()),(0x037fc558,()),(0x03802624,()),
        (0x037fc054,(SECOND,0x038032b8,0,DATA+0x6000,1024,3))):
        result=machine['invoke'](entry,args)
        if not result['actualReturn']:raise ValueError('Original kernel/CARD/second-thread prerequisite did not return')
        prerequisites.append(dict(entry=hex(entry),arguments=args,actualReturn=True))
    def put(target,value):cpu.mem_write(target,(value&MASK).to_bytes(4,'little'))
    cpu.mem_write(ARGUMENT,bytes(0x100));put(COMMON,ARGUMENT)
    put(COMMON+4,case['request']);put(COMMON+8,case['phase']);put(COMMON+0xfc,case['flags'])
    put(COMMON+0xec,SECOND if case['other'] else THREAD)
    ownwrites,wakecalls,visited=[],[],[];state=dict(pc=None)
    def code(uc,pc,size,unused):
        state['pc']=pc
        if ADDRESS<=pc<ADDRESS+CODE:visited.append(pc)
        if pc in (0x037fc64c,0x037fc680):raise ValueError('Disabled receiver fixture unexpectedly switched context')
        if pc==0x037fc36c:wakecalls.append(uc.reg_read(engine.match_runtime.REGISTERS[0]))
    def write(uc,access,target,size,value,unused):
        if ADDRESS<=state['pc']<ADDRESS+CODE and not STACK<=target<STACK+0x4000:
            ownwrites.append([target,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.update(case=case,prerequisites=prerequisites,ownWrites=ownwrites,wakeCalls=wakecalls,ownVisited=visited)
    return machine


def model(case):
    request=case['request'];phase=case['phase'];flags=case['flags'];argument=ARGUMENT;stores=[];wakes=[]
    if case['tag']==11 and case['enabled']:
        if phase==0:request=case['data'];stores.append([COMMON+4,4,request])
        if request==0 and phase==1:
            argument=case['data'];stores.append([COMMON,4,argument]);flags|=0x10;stores.append([COMMON+0xfc,4,flags])
        elif 2<=request<=15:flags|=0x10;stores.append([COMMON+0xfc,4,flags])
        if not flags&0x10:phase=(phase+1)&MASK;stores.append([COMMON+8,4,phase])
        else:
            phase=0;stores.append([COMMON+8,4,0]);wakes.append(SECOND if flags&4 and case['other'] else THREAD)
    return stores,wakes,request,phase,flags,argument


def execute(address,body,case,seed,budget=20000):
    machine=setup(address,body,case,seed);execution=machine['invoke'](address,[case['tag'],case['data'],case['enabled']],True,budget)
    if not execution['actualReturn']:return dict(actualReturn=False,execution=execution,postFaultStateExcluded=True)
    stores,wakes,request,phase,flags,argument=model(case)
    if machine['ownWrites']!=stores or machine['wakeCalls']!=wakes:raise ValueError('Independent receiver ordered protocol writes/wake target differ')
    cpu=machine['cpu'];actual=[int.from_bytes(cpu.mem_read(COMMON+offset,4),'little') for offset in (4,8,0xfc,0)]
    if actual!=[request,phase,flags,argument]:raise ValueError('Independent receiver final full-word state differs')
    return dict(actualReturn=True,execution=execution,ownOrderedWrites=stores,actualWakeTargets=wakes,ownVisited=sorted(set(machine['ownVisited'])),
        finalProtocolWords=actual,originalPrerequisites=machine['prerequisites'],schedulerDisabled=True,actualContextTransfers=0,
        independentOwnOrderedStoreAndProtocolModel=True,independentCompleteMemoryEffectsModel=False,
        orderedNonstackWrites=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        actualNestedReturns={hex(entry):count for entry,count in sorted(machine['helperReturns'].items())},
        physicalFifoOrIrqExecutionCredit=0,gameAccessOrValidityMeaning=None)
