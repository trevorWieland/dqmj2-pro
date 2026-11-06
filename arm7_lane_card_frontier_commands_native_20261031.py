import arm7_lane_card_frontier_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
COMMON,COMMAND,TRANSFER,IO=0x038090c0,0x038096c0,0x038096c4,0x040001a0
ARGUMENT,SOURCE,DESTINATION=DATA,DATA+0x200,DATA+0x400
MASK=0xffffffff


def cases(address):
    if address==0x03802e0c:
        return [dict(size=size,address=start,length=length,width=width,result=result)
            for size in (1,4,16) for start,length in ((0,0),(0,1),(size-1,size+1),(0xffffffff,size+1),(size*2,size*2),((0x100000000-size)&MASK,size*2))
            for width in (1,2,3) for result in (0,3,4)]
    if address==0x03802f04:
        return [dict(value=value,result=result,statuses=statuses)
            for value in (0,1,0x7f,0xff,0x100,0x12345678,0x80000000,0xffffffff)
            for result in (0,3,4) for statuses in ([0],[0,0,1],[0,0,1,0])]
    raise ValueError('Unqualified frontier command')


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    cpu=machine['cpu']
    def put(target,value):cpu.mem_write(target,(value&MASK).to_bytes(4,'little'))
    cpu.mem_write(COMMON,bytes(0x100));put(COMMON,ARGUMENT)
    cpu.mem_write(ARGUMENT,bytes(0x100));put(ARGUMENT,case['result'])
    put(ARGUMENT+0x20,case.get('size',4));put(ARGUMENT+0x28,case.get('width',3))
    put(TRANSFER,0)
    cpu.mem_write(SOURCE,bytes((0,1,0x80,0xff,0x55,0xaa,0x33,0xcc)))
    args=(case['address'],case['length']) if address==0x03802e0c else (case['value'],)
    ownwrites,visited,sleeps,responses,commands,transfers,waits,payloads=[],[],[],[],[],[],[],[]
    state=dict(lastpc=None,statusIndex=0)
    def code(uc,pc,size,unused):
        state['lastpc']=pc
        if address<=pc<address+engine.CODES[address]:visited.append(pc)
        lr=uc.reg_read(engine.match_runtime.REGISTERS[14])
        if pc==0x03802860 and address<=lr<address+engine.CODES[address]:
            words=[uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:4]]
            transfers.append(words)
            if address==0x03802f04:payloads.append(bytes(uc.mem_read(words[0],words[2])).hex())
        if pc==0x0380272c:waits.append([uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:2]])
        if pc==0x03802a0c:commands.append([uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:2]])
        if pc==0x037fc468:
            sleeps.append(uc.reg_read(engine.match_runtime.REGISTERS[0]))
            if len(sleeps)>64:raise ValueError('Bounded lower sleep contract exhausted')
            uc.reg_write(UC_ARM_REG_PC,lr)
    def read(uc,access,target,size,value,unused):
        if target==IO+2 and state['lastpc']==0x03802908:
            sequence=case.get('statuses',[0]);index=state['statusIndex']
            response=sequence[min(index,len(sequence)-1)];state['statusIndex']+=1
            responses.append(response);uc.mem_write(IO+2,response.to_bytes(2,'little'))
    def write(uc,access,target,size,value,unused):
        if address<=state['lastpc']<address+engine.CODES[address] and not STACK<=target<STACK+0x4000:
            ownwrites.append([target,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code);cpu.hook_add(UC_HOOK_MEM_READ,read);cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.update(case=case,args=args,ownWrites=ownwrites,ownVisited=visited,sleeps=sleeps,responses=responses,
        commands=commands,transfers=transfers,waits=waits,payloads=payloads)
    return machine


def model(address,case):
    if address==0x03802e0c:
        size=case['size'];remaining=case['length'];current=case['address']
        if (current|remaining)&(size-1):return [[ARGUMENT,4,2]],[],[],[],2,[],[],[]
        if case['result']==4:return [],[],[],[[0,50]],6,[],[],[]
        stores=[];commands=[];waits=[[0,50]]
        while remaining:
            stores.append([TRANSFER,4,case['width']+1]);commands.append([current,0x20]);waits.append([0,0])
            if case['result']:break
            current=(current+size)&MASK;remaining=(remaining-size)&MASK
        return stores,commands,[],waits,case['result'],[],[],[]
    if case['result']==4:return [],[],[],[[0,50]],6,[],[],[]
    stores=[];waits=[[0,50]];payloads=[];sleeps=[];transfers=[]
    status=case['result'];sequence=case.get('statuses',[0]);index=2
    for attempt in range(10):
        stores.append([TRANSFER,4,2]);payloads.append(bytes((1,case['value']&255)).hex())
        transfers.append([STACK+0x3000-40,0,2,0x03802924]);waits.append([5,0]);sleeps.append(5)
        response=sequence[min(index,len(sequence)-1)];index+=1
        if response&1:status=4
        if status!=4:break
    return stores,[],transfers,waits,status,sleeps,payloads,[]


def execute(address,body,case,seed,budget=20000):
    machine=setup(address,body,case,seed)
    execution=machine['invoke'](address,machine['args'],True,budget)
    if not execution['actualReturn']:return dict(execution=execution,actualReturn=False,postFaultStateExcluded=True)
    stores,commands,transfers,waits,status,sleeps,payloads,unused=model(address,case)
    if machine['ownWrites']!=stores or machine['commands']!=commands or machine['transfers']!=transfers or machine['waits']!=waits:
        raise ValueError('Independent frontier stores/commands/transfers/waits differ')
    if machine['sleeps']!=sleeps or machine['payloads']!=payloads:
        raise ValueError('Independent bounded sleep/retry/two-byte payload model differs')
    cpu=machine['cpu']
    if int.from_bytes(cpu.mem_read(ARGUMENT,4),'little')!=status:raise ValueError('Independent argument result model differs')
    return dict(execution=execution,actualReturn=True,
        orderedNonstackWrites=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        actualNestedReturns={hex(entry):count for entry,count in sorted(machine['helperReturns'].items())},
        ownOrderedWrites=stores,actualSleepProviderCalls=sleeps,actualStatusResponses=machine['responses'],
        ownVisited=sorted(set(machine['ownVisited'])),actualAddressCommandCalls=commands,actualTransferArguments=transfers,
        actualWaitArguments=waits,actualPayloads=payloads,independentOwnWritesAndBranchModel=True,
        independentCompleteMemoryEffectsModel=False,staticMappedMmioOnly=not sleeps and not any(machine['responses']),
        hardwareExecutionCredit=0,originalSleepFunctionExecutionCredit=0)
