import copy
import arm7_lane_card_pages_engine_20261031 as engine
from unicorn import UC_HOOK_CODE,UC_HOOK_MEM_READ,UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC
BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
COMMON,COMMAND,TRANSFER,IO=0x038090c0,0x038096c0,0x038096c4,0x040001a0
ARGUMENT,SOURCE,DESTINATION=DATA,DATA+0x200,DATA+0x400
SIZES,CODES=engine.SIZES,engine.CODES
MASK=0xffffffff


def cases(address):
    if address not in SIZES:raise ValueError('Unqualified page caller')
    return [dict(size=size,address=start,length=length,width=width,result=result,passes=1)
        for size in (1,4,16) for start,length in ((0,0),(0,1),(size-1,size+1),(0xffffffff,size+1))
        for width in (1,2,3) for result in (0,3,4)]



def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    cpu=machine['cpu']
    cpu.mem_write(COMMON,ARGUMENT.to_bytes(4,'little'))
    cpu.mem_write(ARGUMENT,bytes(0x100))
    def put(target,value):cpu.mem_write(target,(value&MASK).to_bytes(4,'little'))
    put(ARGUMENT,case.get('result',0))
    put(ARGUMENT+0x24,case['size'])
    put(ARGUMENT+0x28,case.get('width',3))
    put(ARGUMENT+0x40,0)
    put(ARGUMENT+0x44,0)
    put(TRANSFER,case.get('count',0))
    cpu.mem_write(SOURCE,bytes((0,1,0x80,0xff,0x55,0xaa,0x33,0xcc)))
    args=(case['address'],SOURCE,case['length'])
    ownwrites,visited,sleeps,responses,commands,transfers,waits=[],[],[],[],[],[],[]
    state=dict(lastpc=None,statusIndex=0)
    def code(uc,pc,size,unused):
        state['lastpc']=pc
        if address<=pc<address+CODES[address]:visited.append(pc)
        if pc==0x03802860 and address<=uc.reg_read(engine.match_runtime.REGISTERS[14])<address+CODES[address]:
            transfers.append([uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:4]])
        if pc==0x0380272c:
            waits.append([uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:2]])
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
    machine.update(case=case,args=args,ownWrites=ownwrites,ownVisited=visited,sleeps=sleeps,responses=responses,commands=commands,transfers=transfers,waits=waits)
    return machine


def model(address,case):
    if case['result']==4:return [],[],[],[[0,50]],6
    commands=[];transfers=[];stores=[];waits=[[0,50]]
    current=case['address'];remaining=case['length'];offset=0;mask=case['size']-1
    while remaining:
        amount=min(case['size']-(current&mask),remaining)
        stores.append([COMMAND+4,4,case['width']+1+amount])
        commands.append([current,2 if address==0x03802b70 else 10])
        transfers.append([SOURCE+offset,0,amount,0x03802924])
        waits.append([0,0])
        if case['result']:break
        current=(current+amount)&MASK;offset+=amount;remaining-=amount
    return stores,commands,transfers,waits,case['result']


def execute(address,body,case,seed,budget=20000):
    machine=setup(address,body,case,seed)
    before=engine.snapshot(machine)
    execution=machine['invoke'](address,machine['args'],True,budget)
    if not execution['actualReturn']:
        return dict(execution=execution,actualReturn=False,postFaultStateExcluded=True)
    stores,commands,transfers,waits,status=model(address,case)
    if machine['ownWrites']!=stores or machine['commands']!=commands or machine['transfers']!=transfers or machine['waits']!=waits or machine['sleeps']:
        raise ValueError('Independent page caller ordered stores/full-word addresses/source chunks/waits differ')
    if int.from_bytes(machine['cpu'].mem_read(ARGUMENT,4),'little')!=status:
        raise ValueError('Independent preflight/result-stop state differs')
    cpu=machine['cpu']
    result=dict(execution=execution,actualReturn=True,
        orderedNonstackWrites=[row for row in machine['writes'] if not STACK<=row[0]<STACK+0x4000],
        nonstackReads=[row for row in machine['reads'] if not STACK<=row[0]<STACK+0x4000],
        memorySha256={hex(first):engine.digest(bytes(cpu.mem_read(first,len(data)))) for first,data in machine['regions'].items()},
        actualNestedReturns={hex(entry):count for entry,count in sorted(machine['helperReturns'].items())})
    result.update(ownOrderedWrites=stores,actualSleepProviderCalls=machine['sleeps'],actualStatusResponses=machine['responses'],
        ownVisited=sorted(set(machine['ownVisited'])),actualAddressCommandCalls=commands,actualTransferArguments=transfers,actualWaitArguments=waits,independentOwnWritesAndBranchModel=True,
        independentCompleteMemoryEffectsModel=False,
        staticMappedMmioOnly=not machine['sleeps'] and not any(machine['responses']),hardwareExecutionCredit=0,
        originalSleepFunctionExecutionCredit=0)
    return result
