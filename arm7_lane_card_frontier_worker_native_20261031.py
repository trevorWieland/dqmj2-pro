import arm7_lane_card_frontier_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UcError
from unicorn.arm_const import UC_ARM_REG_CPSR,UC_ARM_REG_PC
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
ADDRESS,SIZE,CODE=0x038032b8,564,560
COMMON,ARGUMENT,SOURCE,DESTINATION=0x038090c0,DATA,DATA+0x200,DATA+0x400
PARENT,THREAD=0x038077c8,COMMON+0x48
MASK=0xffffffff


def cases(address):
    if address!=ADDRESS:raise ValueError('Unqualified nonreturning CARD worker')
    return [dict(request=request,allowed=allowed,length=length,task=False)
        for request in range(32) for allowed in (False,True) for length in (0,1)]+[dict(request=0,allowed=False,length=0,task=True)]+[dict(request=request,allowed=True,length=1,task=False,producer=True) for request in range(2,16)]


def setup(address,body,case,seed):
    if not 0<=case['request']<32:raise ValueError('Compiled source shift contract requires a request below32')
    machine=engine.setup(address,body,seed);cpu=machine['cpu']
    cpu.mem_map(0x04100000,0x1000);cpu.mem_write(0x04100000,bytes(0x1000))
    cpu.mem_write(0x04100010,(0xdeadbeef).to_bytes(4,'little'));machine['regions'][0x04100000]=bytes(cpu.mem_read(0x04100000,0x1000))
    cpu.mem_write(0x03807678,bytes(0x0380b4e4-0x03807678))
    cpu.mem_write(0x027ffe60,(0x00800000).to_bytes(4,'little'))
    cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(engine.match_runtime.REGISTERS[13],0)
    prerequisites=[]
    for entry in (0x037fbf64,0x037fc558,0x03802624,0x037fc590):
        call=machine['invoke'](entry)
        if not call['actualReturn']:raise ValueError('Original kernel/CARD/scheduling prerequisite did not return')
        prerequisites.append(dict(entry=hex(entry),actualReturn=True))
    def put(target,value):cpu.mem_write(target,(value&MASK).to_bytes(4,'little'))
    cpu.mem_write(ARGUMENT,bytes(0x100));put(COMMON,ARGUMENT)
    put(COMMON+4,case['request']);put(COMMON+0x3c,0);put(COMMON+0x40,0);put(COMMON+0x44,0x03802ffc)
    put(COMMON+0xfc,0xc if case['task'] else 0x10)
    for offset,value in ((0,0xffffffff),(0xc,SOURCE),(0x10,DESTINATION),(0x14,case['length']),
        (0x1c,1),(0x20,1),(0x24,1),(0x28,3),(0x58,(1<<case['request']) if case['allowed'] else 0)):
        put(ARGUMENT+offset,value)
    cpu.mem_write(SOURCE,bytes((0x55,0xaa,0x80,0xff)))
    if case.get('producer'):
        put(COMMON+0xfc,0);put(COMMON+8,0);put(COMMON+4,0)
        for entry,args in ((0x037fc558,()),(0x038031d4,(11,case['request'],1)),(0x037fc590,())):
            call=machine['invoke'](entry,args)
            if not call['actualReturn']:raise ValueError('Original PXI receiver prerequisite did not return')
            prerequisites.append(dict(entry=hex(entry),arguments=args,actualReturn=True))
        if int.from_bytes(cpu.mem_read(COMMON+4,4),'little')!=case['request'] or int.from_bytes(cpu.mem_read(COMMON+0xfc,4),'little')!=0x10:
            raise ValueError('Original receiver did not produce the qualified request/flag context')
    machine.update(case=case,prerequisites=prerequisites)
    return machine


def execute(address,body,case,seed,budget=60000):
    machine=setup(address,body,case,seed);cpu=machine['cpu']
    state=dict(active=PARENT,serviceSp=0,pendingSave=None,pendingLoad=None,resumePc=None,
        saveReturns=0,resumed=0,loads=0,steps=0,pc=None)
    expectedContexts={};visited,events,ownwrites,sleeps,calls=[],[],[],[],[]
    task_calls=[];pendingCalls=[];returns={}
    dispatch={2:0x03802aac,3:0x03803094,6:0x03802b04,7:0x03802c28,8:0x03802b70,
        9:0x03802ce0,11:0x03802d70,15:0x03802e0c,12:0x03802ea8,13:0x038027d0,14:0x03802f04}
    def code(uc,pc,size,unused):
        state['steps']+=1;state['pc']=pc
        if ADDRESS<=pc<ADDRESS+CODE:visited.append(pc)
        loading=state['pendingLoad']
        if loading and pc==loading['pc']:
            actual=[uc.reg_read(register) for register in engine.match_runtime.REGISTERS]
            if actual!=loading['registers'] or uc.reg_read(UC_ARM_REG_CPSR)!=loading['cpsr']:
                raise ValueError('Original nonlocal load differs from complete context ABI model')
            state.update(active=loading['context'],serviceSp=loading['serviceSp'],loads=state['loads']+1,pendingLoad=None)
            if loading['context']==PARENT:state['resumePc']=actual[14]
        saving=state['pendingSave']
        if saving and pc==saving['lr']:
            if bytes(uc.mem_read(saving['context'],72))!=expectedContexts[saving['context']] or uc.reg_read(engine.match_runtime.REGISTERS[0])!=0:
                raise ValueError('Original save-context normal return/record differs')
            state.update(saveReturns=state['saveReturns']+1,pendingSave=None)
        elif state['resumePc'] is not None and pc==state['resumePc']:
            if uc.reg_read(engine.match_runtime.REGISTERS[0])!=1:raise ValueError('Resumed outer sleep continuation lost discriminator1')
            state.update(resumed=state['resumed']+1,resumePc=None)
        while pendingCalls and pendingCalls[-1][1]==pc:
            entry,lr=pendingCalls.pop();returns[entry]=returns.get(entry,0)+1
        if pc==0x037fc64c:
            values=[uc.reg_read(register) for register in engine.match_runtime.REGISTERS];flags=uc.reg_read(UC_ARM_REG_CPSR)
            context=values[0]
            if context!=state['active'] or context not in (PARENT,THREAD):raise ValueError('Unexpected context saved')
            words=[flags,1,context+4,flags,*values[3:13],values[13],values[14],0x037fc680,state['serviceSp']]
            expectedContexts[context]=b''.join(word.to_bytes(4,'little') for word in words)
            state['pendingSave']=dict(context=context,lr=values[14])
        if pc==0x037fc680:
            context=uc.reg_read(engine.match_runtime.REGISTERS[0]);expected=[THREAD,PARENT]
            if state['loads']>=2 or context!=expected[state['loads']]:raise ValueError('Unexpected scheduled context/order')
            record=bytes(uc.mem_read(context,72));values=[int.from_bytes(record[i:i+4],'little') for i in range(0,72,4)]
            if context==THREAD:
                predicted=[0x1f,*([0]*13),(0x038096c0-4-0x40)&~7,0x037fc15c,ADDRESS+4,0x038096bc]
                if values!=predicted:raise ValueError('Original created CARD thread register/stack/entry record differs')
            elif record!=expectedContexts[PARENT]:raise ValueError('Parent saved record changed before resume')
            state['pendingLoad']=dict(context=context,pc=values[16]-4,registers=values[1:16],cpsr=values[0],serviceSp=values[17])
        lr=uc.reg_read(engine.match_runtime.REGISTERS[14])
        if pc in dispatch.values() and ADDRESS<=lr<ADDRESS+CODE:
            words=[uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:3]]
            calls.append([pc,words]);pendingCalls.append([pc,lr])
        if pc==0x03802ffc and ADDRESS<=lr<ADDRESS+CODE:
            task_calls.append([pc,uc.reg_read(engine.match_runtime.REGISTERS[0])]);pendingCalls.append([pc,lr])
        if pc==0x037fc468:
            sleeps.append(uc.reg_read(engine.match_runtime.REGISTERS[0]))
            if len(sleeps)>64:raise ValueError('Bounded tick-sleep contract exhausted')
            uc.reg_write(UC_ARM_REG_PC,lr)
        if pc in (ADDRESS,0x037fc290,0x037fc2e4,0x037fc64c,0x037fc680):
            events.append([pc,uc.reg_read(engine.match_runtime.REGISTERS[0]),uc.reg_read(engine.match_runtime.REGISTERS[13])])
    def write(uc,access,target,size,value,unused):
        if ADDRESS<=state['pc']<ADDRESS+CODE and not COMMON+0x204<=target<0x038096bc:
            ownwrites.append([target,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    initial=[(seed*0x10305+0x12345678+i*0x1020304)&MASK for i in range(15)]
    initial[0]=COMMON+0xf4;initial[13:]=[0x0380fb78,RETURN]
    cpsr=0x1f|((seed&1)*128)|((seed&2)*32)|((seed&15)<<28)
    cpu.reg_write(UC_ARM_REG_CPSR,0xd3);cpu.reg_write(engine.match_runtime.REGISTERS[13],0)
    cpu.reg_write(UC_ARM_REG_CPSR,cpsr)
    for register,value in zip(engine.match_runtime.REGISTERS,initial):cpu.reg_write(register,value)
    machine['state']['caller']=True;machine['reads'].clear();machine['writes'].clear()
    fault=None
    try:cpu.emu_start(0x037fc290,RETURN,timeout=500000,count=budget)
    except (UcError,ValueError) as error:fault=str(error)
    actual=cpu.reg_read(UC_ARM_REG_PC)==RETURN and fault is None
    result=dict(address=hex(address),case=case,seed=seed,actualOwnedNormalReturns=0,actualResumedOuterSleepReturn=actual,
        pc=hex(cpu.reg_read(UC_ARM_REG_PC)),fault=fault,instructions=state['steps'],originalPrerequisites=machine['prerequisites'],
        ownVisited=sorted(set(visited)),events=events)
    if not actual:return dict(result,postBoundaryStateExcluded=True,returnCredit=0)
    registers=[cpu.reg_read(register) for register in engine.match_runtime.REGISTERS]
    if registers[4:12]!=initial[4:12] or registers[13:]!=initial[13:] or cpu.reg_read(UC_ARM_REG_CPSR)&255!=cpsr&255:
        raise ValueError('Resumed original caller register/stack/mode ABI differs')
    if (state['loads'],state['saveReturns'],state['resumed'])!=(2,2,1):raise ValueError('Actual load/save/resume counts differ')
    if any(state[key] is not None for key in ('pendingLoad','pendingSave','resumePc')) or pendingCalls:
        raise ValueError('Context/API calls did not complete')
    expectedOwn=[]
    if not case['task']:
        expectedOwn=[[COMMON+0xfc,4,0x14],[COMMON+0xfc,4,4],[ARGUMENT,4,0]]
        if not case['allowed'] or case['request'] in (4,5,10) or case['request']>=16:expectedOwn.append([ARGUMENT,4,3])
        elif case['request']==3:expectedOwn.append([ARGUMENT+8,4,0xdeadbeef])
        elif case['request']==13:expectedOwn.append([DESTINATION,1,0])
        expectedOwn.append([COMMON+0xfc,4,0])
    expectedOwn.append([COMMON+0xec,4,THREAD])
    if ownwrites!=expectedOwn:raise ValueError('Independent complete own ordered stores/widths/flags differ')
    status=int.from_bytes(cpu.mem_read(ARGUMENT,4),'little')
    flags=int.from_bytes(cpu.mem_read(COMMON+0xfc,4),'little')
    if flags!=0:raise ValueError('Original worker/task completion did not clear supported flags')
    expectedCalls=[]
    if not case['task'] and case['allowed'] and case['request'] in dispatch:expectedCalls=[dispatch[case['request']]]
    if [row[0] for row in calls]!=expectedCalls:raise ValueError('Independent request/capability dispatch differs')
    if calls:
        words=calls[0][1];req=case['request']
        count=3 if req in (6,7,8,9) else 2 if req in (11,15) else 1 if req==14 else 0
        wanted=[SOURCE,DESTINATION,case['length']] if req==6 else [DESTINATION,SOURCE,case['length']] if req in (7,8,9) else [DESTINATION,case['length']] if req in (11,15) else [0x55] if req==14 else []
        if words[:count]!=wanted:raise ValueError('Named native dispatch API physical argument widths/order differ')
    if case['task']:
        if task_calls!=[[0x03802ffc,COMMON]] or status!=0:raise ValueError('Actual task callback/current-state contract differs')
    elif task_calls:raise ValueError('Unexpected task callback')
    elif status!=(3 if not case['allowed'] or case['request'] in (4,5,10) or case['request']>=16 else 1 if case['request']==9 and case['length'] else 0):
        raise ValueError('Independent supported/default capability result differs')
    return dict(result,registers=registers,cpsr=cpu.reg_read(UC_ARM_REG_CPSR),actualNonlocalContextTransfers=2,
        ordinarySaveReturns=2,ordinaryLoadReturns=0,resumedSavedContinuations=1,actualTaskCalls=task_calls,
        actualDispatchCalls=calls,actualDispatchReturns={hex(key):value for key,value in sorted(returns.items())},
        actualSleepProviderCalls=sleeps,ownOrderedNonstackWrites=ownwrites,finalArgumentStatus=status,
        independentRequestDispatchAndContextAbiModel=True,independentCompleteMemoryEffectsModel=False,
        orderedReads=machine['reads'],orderedWrites=machine['writes'],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        hardwareExecutionCredit=0,originalTickSleepExecutionCredit=0,compiledShiftInputDomain=[0,31],
        syntheticHeaderControlWord=0x00800000,staticCartridgeReceiveWord=0xdeadbeef,physicalHeaderOrCartridgeConfigurationCredit=0)
