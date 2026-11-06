import arm7_lane_scheduler_counter_engine_20261031 as engine

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
SIZES,CODES=engine.SIZES,engine.CODES
ADDRESS,COUNTER=0x037FC558,0x038076F4
digest=engine.digest


def cases(address):
    values=(0,1,2,7,0x7FFFFFFF,0x80000000,0xFFFFFFFD,0xFFFFFFFE)
    return [dict(counter=value,passes=1 if value==0xFFFFFFFE else 2,flagsSeed=seed) for value in values for seed in range(16)]


def setup(address,body,case,seed):
    machine=engine.setup(address,body,seed)
    machine['cpu'].mem_write(COUNTER,case['counter'].to_bytes(4,'little'))
    machine['case']=case
    return machine


def execute(machine,budget=100000):
    states=[]
    for iteration in range(machine['case']['passes']):
        expected=engine.snapshot(machine)
        old=engine.word(expected,COUNTER)
        if old==0xFFFFFFFF:
            raise ValueError('Undefined-source saturated counter is outside compiled supported return domain')
        stores=[]
        engine.store(expected,COUNTER,old+1,stores)
        execution=machine['invoke'](machine['address'],[],True,budget)
        states.append(engine.result(machine,execution,expected,old,stores))
        if not execution['actualReturn']:
            break
    return dict(case=machine['case'],states=states,visited=sorted(machine['visited']))


def original_saturation(body,seed):
    machine=setup(ADDRESS,body,dict(counter=0xFFFFFFFF,passes=1),seed)
    before=engine.snapshot(machine)
    execution=machine['invoke'](ADDRESS,[],True)
    if not execution['actualReturn']:
        raise ValueError('Original-only saturated scheduler did not actually return')
    current=engine.snapshot(machine)
    inherited=(seed*0x10203+4*0x1030507+0x7129)&0xFFFFFFFF
    if current!=before or execution['registers'][0]!=inherited:
        raise ValueError('Original-only saturation no-write/inherited-R4 observation differs')
    return dict(seed=seed,actualOriginalReturn=True,observedR0=hex(execution['registers'][0]),observedIncomingR4=hex(inherited),
        counterUnchanged=True,otherMappedNonstackMemoryUnchanged=True,compiledReturnCredit=0,portableCReturnMeaning=None,
        limitation='Verified public source leaves localcount uninitialized on saturation; native inherited-R4 bits are recorded without inventing a C formal or supported portable result')
