import arm7_lane_card_control_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
COMMON,ARGUMENT,OTHER=0x038090c0,DATA,DATA+0x100
IO=0x040001a0
MASK=0xffffffff


def cases(address):
    if address==0x03802824:
        return [dict(old=old,new=new,swap=swap)
            for old in (0,3,4,0xffffffff) for new in (0,3,4,0xffffffff) for swap in (False,True)]
    if address==0x03803094:
        return [dict(control=control,received=value)
            for control in (0x00800000,0x00801fff,0xa4f53c89,0xffffffff)
            for value in (0,1,0x12345678,0x80000000,0xffffffff)]
    if address==0x03803114:
        return [dict(flags=flags,callback=callback,argument=argument)
            for flags in (0,1,2,8,0x10,0x20,0x40,0x80000000,0xfffffffb)
            for callback in (0,0x038028e4,0x03802924,0x03802974)
            for argument in (0,ARGUMENT,0x12345678,0xffffffff)]
    raise ValueError('Unqualified CARD control entry')


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed);cpu=machine['cpu']
    def put(target,value):cpu.mem_write(target,(value&MASK).to_bytes(4,'little'))
    ownwrites,visited,sleeps,responses=[],[],[],[];state=dict(pc=None,index=0,swapped=False)
    if address==0x03802824:
        cpu.mem_write(COMMON,bytes(0x100));cpu.mem_write(ARGUMENT,bytes(0x200))
        put(COMMON,ARGUMENT);put(ARGUMENT,case['old']);put(OTHER,case['new']);put(0x038096c4,0)
        args=[]
    elif address==0x03803094:
        cpu.mem_map(0x04100000,0x1000);cpu.mem_write(0x04100000,bytes(0x1000));put(0x04100010,case['received'])
        machine['regions'][0x04100000]=bytes(cpu.mem_read(0x04100000,0x1000));put(0x027ffe60,case['control']);args=[]
    else:
        put(COMMON+0xfc,case['flags']);args=[COMMON,case['callback'],case['argument']]
    def code(uc,pc,size,unused):
        state['pc']=pc
        if address<=pc<address+engine.CODES[address]:visited.append(pc)
        if pc==0x037fc468:
            sleeps.append(uc.reg_read(engine.match_runtime.REGISTERS[0]))
            if len(sleeps)>51:raise ValueError('Bounded wait sleep provider exhausted')
            if case.get('swap') and not state['swapped']:put(COMMON,OTHER);state['swapped']=True
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(engine.match_runtime.REGISTERS[14]))
    def read(uc,access,target,size,value,unused):
        if address==0x03802824 and target==IO+2 and state['pc']==0x03802908:
            response=1 if case['swap'] and state['index']==0 else 0
            state['index']+=1;responses.append(response);uc.mem_write(IO+2,response.to_bytes(2,'little'))
    def write(uc,access,target,size,value,unused):
        if address<=state['pc']<address+engine.CODES[address] and not STACK<=target<STACK+0x4000:
            ownwrites.append([target,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.update(case=case,args=args,ownWrites=ownwrites,ownVisited=visited,sleeps=sleeps,responses=responses,scenarioState=state)
    return machine


def execute(address,body,case,seed,budget=20000):
    machine=setup(address,body,case,seed);cpu=machine['cpu'];expected=engine.snapshot(machine)
    execution=machine['invoke'](address,machine['args'],True,budget)
    if not execution['actualReturn']:return dict(execution=execution,actualReturn=False,postFaultStateExcluded=True)
    wanted=[];complete=False;returned=None
    if address==0x03802824:
        latest=OTHER if case['swap'] else ARGUMENT;value=case['new'] if case['swap'] else case['old']
        returned=int(value!=4)
        if value==4:wanted=[[latest,4,6]]
        if int.from_bytes(cpu.mem_read(COMMON,4),'little')!=latest:raise ValueError('Wait provider latest-argument pointer differs')
        for target,before in ((ARGUMENT,case['old']),(OTHER,case['new'])):
            actual=int.from_bytes(cpu.mem_read(target,4),'little')
            if actual!=(6 if target==latest and value==4 else before):raise ValueError('Independent preflight latest/old argument status differs')
        if machine['sleeps']!=([5] if case['swap'] else []):raise ValueError('Actual bounded wait/swap provider differs')
    elif address==0x03803094:
        returned=case['received'];control=((case['control']&~0x07000000)|0xa7000000)&~0x1fff
        wanted=[[IO+4,4,control]]
        actualCommand=bytes(cpu.mem_read(IO+8,8))
        if actualCommand!=bytes((0xb8,0,0,0,0,0,0,0)):raise ValueError('Original ROM operation command word/byte order differs')
        if int.from_bytes(cpu.mem_read(IO+4,4),'little')!=control:raise ValueError('Independent masked control word differs')
    else:
        wanted=[[COMMON+0xfc,4,case['flags']|4],[COMMON+0x3c,4,case['callback']],[COMMON+0x40,4,case['argument']]]
        writes=[]
        for target,width,value in wanted:engine.store(expected,target,value,writes)
        if any(bytes(cpu.mem_read(first,len(data)))!=data for first,data in expected.items()):
            raise ValueError('Independent begin-task complete nonstack memory model differs')
        complete=True
    if returned is not None and execution['registers'][0]!=returned:raise ValueError('Independent full-word return model differs')
    if machine['ownWrites']!=wanted:raise ValueError('Independent own ordered stores/widths differ')
    return dict(execution=execution,actualReturn=True,ownOrderedWrites=wanted,ownVisited=sorted(set(machine['ownVisited'])),
        independentOwnOrderedStoresAndReturn=True,independentCompleteMemoryEffectsModel=complete,
        actualSleepProviderCalls=machine['sleeps'],actualStatusResponses=machine['responses'],
        boundedArgumentPointerSwap=bool(case.get('swap')),physicalHardwareCredit=0,originalSleepExecutionCredit=0,
        orderedNonstackWrites=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        actualNestedReturns={hex(entry):count for entry,count in sorted(machine['helperReturns'].items())})
