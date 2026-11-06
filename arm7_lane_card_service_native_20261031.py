import copy
import arm7_lane_card_service_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
COMMON,COMMAND,TRANSFER,IO=0x038090c0,0x038096c0,0x038096c4,0x040001a0
ARGUMENT,SOURCE,DESTINATION=DATA,DATA+0x200,DATA+0x400
SIZES,CODES=engine.SIZES,engine.CODES
MASK=0xffffffff


def cases(address):
    if address==0x03802860:
        return [dict(count=count,length=length,callback=0x03802924,passes=1)
            for count in (0,1,2,4,0xffffffff) for length in (0,1,2,3,4)]
    if address==0x0380272c:
        rows=[dict(minimum=0,maximum=0,statuses=[0],passes=1),
            dict(minimum=0xffffffff,maximum=1,statuses=[1],passes=1)]
        rows.extend(dict(minimum=a,maximum=b,statuses=list(s),passes=1)
            for a,b in ((0,1),(0,5),(0,6),(0,10),(1,0),(1,1),(2,8),(8,2))
            for s in ((0,),(1,),(1,0,0),(1,1,0,1)))
        return rows
    if address==0x03802d70:
        return [dict(size=size,address=address,length=length,width=width,result=result,statuses=[0],passes=1)
            for size in (1,4,256) for address,length in ((0,0),(0,size),(size,size*2),(1,size),(size,size+1))
            for width in (1,2,3) for result in (0,3,4)]
    raise ValueError('Unqualified CARD service entry')


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    cpu=machine['cpu']
    cpu.mem_write(COMMON,ARGUMENT.to_bytes(4,'little'))
    cpu.mem_write(ARGUMENT,bytes(0x100))
    def put(target,value):cpu.mem_write(target,(value&MASK).to_bytes(4,'little'))
    put(ARGUMENT,case.get('result',0))
    put(ARGUMENT+0x1c,case.get('size',4))
    put(ARGUMENT+0x28,case.get('width',3))
    put(ARGUMENT+0x40,0)
    put(ARGUMENT+0x44,0)
    put(TRANSFER,case.get('count',0))
    cpu.mem_write(SOURCE,bytes((0,1,0x80,0xff,0x55,0xaa,0x33,0xcc)))
    if address==0x03802860:
        args=(SOURCE,DESTINATION,case['length'],case['callback'])
    elif address==0x0380272c:
        args=(case['minimum'],case['maximum'])
    else:args=(case['address'],case['length'])
    ownwrites,visited,sleeps,responses,commands=[],[],[],[],[]
    state=dict(lastpc=None,statusIndex=0)
    def code(uc,pc,size,unused):
        state['lastpc']=pc
        if address<=pc<address+CODES[address]:visited.append(pc)
        if pc==0x03802a0c:
            commands.append([uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:2]])
        if pc==0x037fc468:
            value=uc.reg_read(engine.match_runtime.REGISTERS[0])
            sleeps.append(value)
            if len(sleeps)>64:raise ValueError('Bounded lower sleep contract exhausted')
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(engine.match_runtime.REGISTERS[14]))
    def read(uc,access,target,size,value,unused):
        if target==IO+2 and state['lastpc']==0x03802908:
            sequence=case.get('statuses',[0])
            index=state['statusIndex'];response=sequence[min(index,len(sequence)-1)]
            state['statusIndex']+=1
            responses.append(response)
            if response!=0:uc.mem_write(IO+2,response.to_bytes(2,'little'))
    def write(uc,access,target,size,value,unused):
        if address<=state['lastpc']<address+CODES[address] and not STACK<=target<STACK+0x4000:
            ownwrites.append([target,size,value&((1<<(size*8))-1)])
    cpu.hook_add(UC_HOOK_CODE,code)
    cpu.hook_add(UC_HOOK_MEM_READ,read)
    cpu.hook_add(UC_HOOK_MEM_WRITE,write)
    machine.update(case=case,args=args,ownWrites=ownwrites,ownVisited=visited,sleeps=sleeps,responses=responses,commands=commands)
    return machine


def wait_model(minimum,maximum,sequence):
    index=0;sleeps=[]
    def ready():
        nonlocal index
        response=sequence[min(index,len(sequence)-1)]
        index+=1
        return not(response&1)
    if ((minimum+maximum)&MASK)==0:return False,sleeps,0
    if minimum:sleeps.append(minimum)
    if maximum:
        remaining=engine.signed((maximum-minimum)&MASK)
        while not ready() and remaining>0:
            interval=min(remaining,5)
            sleeps.append(interval)
            remaining-=interval
    failed=not ready()
    return failed,sleeps,index


def expected_own(address,case):
    if address==0x0380272c:
        failed,sleeps,responses=wait_model(case['minimum'],case['maximum'],case['statuses'])
        return ([[ARGUMENT,4,4]] if failed else []),sleeps,responses
    if address==0x03802d70:
        if (case['address']|case['length'])&((case['size']-1)&MASK):return [[ARGUMENT,4,2]],[],0
        if case['result']==4:return [],[],2
        iterations=case['length']//case['size'] if case['result']==0 else bool(case['length'])
        return [[COMMAND+4,4,case['width']+1] for unused in range(iterations)],[],2
    trace=[[TRANSFER+4,4,SOURCE],[TRANSFER+8,4,DESTINATION],[IO,2,0xa040]]
    count=case['count']
    for i in range(case['length']):
        count=(count-1)&MASK
        trace.append([TRANSFER,4,count])
        if count==0:trace.append([IO,2,0xa000])
    if count==0:trace.append([IO,2,0])
    return trace,[],0


def modeled_transfer(memory,case):
    trace=[]
    def put(target,size,value):
        for first,data in memory.items():
            if first<=target and target+size<=first+len(data):
                data[target-first:target-first+size]=value.to_bytes(size,'little')
                return
        raise ValueError('Transfer model store escaped backing')
    put(TRANSFER+4,4,SOURCE);put(TRANSFER+8,4,DESTINATION);put(IO,2,0xa040)
    count=case['count']
    for i in range(case['length']):
        count=(count-1)&MASK;put(TRANSFER,4,count)
        if count==0:put(IO,2,0xa000)
        sourcebyte=memory[DATA][SOURCE-DATA+i]
        put(IO+2,2,sourcebyte);put(TRANSFER+4,4,SOURCE+i+1)
    if count==0:put(IO,2,0)
    return memory


def execute(address,body,case,seed,budget=20000):
    machine=setup(address,body,case,seed)
    before=engine.snapshot(machine)
    execution=machine['invoke'](address,machine['args'],True,budget)
    if not execution['actualReturn']:
        return dict(execution=execution,actualReturn=False,postFaultStateExcluded=True)
    stores,sleeps,responses=expected_own(address,case)
    if machine['ownWrites']!=stores or machine['sleeps']!=sleeps or len(machine['responses'])!=responses:
        raise ValueError('Independent CARD own-store/delay/status-flow model differs: '+str((hex(address),case,machine['ownWrites'],stores,machine['sleeps'],sleeps,machine['responses'],responses)))
    if address==0x03802d70:
        expected_commands=[[(case['address']+i*case['size'])&MASK,0xd8] for i in range(len(stores))] if not ((case['address']|case['length'])&((case['size']-1)&MASK)) else []
        if machine['commands']!=expected_commands:raise ValueError('Independent sector address/command argument sequence differs')
    if address==0x03802860:
        expected=modeled_transfer(before,case)
        if any(bytes(machine['cpu'].mem_read(first,len(data)))!=data for first,data in expected.items()):
            raise ValueError('Independent complete transfer mapped-memory model differs')
    cpu=machine['cpu']
    result=dict(execution=execution,actualReturn=True,
        orderedNonstackWrites=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        actualNestedReturns={hex(entry):count for entry,count in sorted(machine['helperReturns'].items())})
    result.update(ownOrderedWrites=stores,actualSleepProviderCalls=sleeps,actualStatusResponses=machine['responses'],
        ownVisited=sorted(set(machine['ownVisited'])),actualAddressCommandCalls=machine['commands'],independentOwnWritesAndBranchModel=True,
        independentCompleteMemoryEffectsModel=address==0x03802860,
        staticMappedMmioOnly=not sleeps and not any(machine['responses']),hardwareExecutionCredit=0,
        originalSleepFunctionExecutionCredit=0)
    return result
