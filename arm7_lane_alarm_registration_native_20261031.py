import random
import arm7_lane_thread_init_engine_20261031 as engine
from unicorn import UC_HOOK_CODE

BASE,DATA,STACK,RETURN=engine.BASE,engine.DATA,engine.STACK,engine.RETURN
ADDRESS,SIZE,CODE=0x037FE5C0,156,140
FLAG,ALARM,IO=0x03807950,0x03807954,0x04000000
digest=engine.digest


def cases(address):
    if address!=ADDRESS:
        raise ValueError('Unqualified alarm registration entry')
    rows=[dict(tick=tick,alarm=alarm,enabled=enabled,counter=0,timer=0,request=0,passes=2)
        for tick in (False,True) for alarm in (False,True) for enabled in (0,1,2,0x80000000,0xFFFFFFFF)]
    rows.extend(dict(tick=True,alarm=True,enabled=0,counter=counter,timer=timer,request=request,passes=2)
        for counter in (0,1,0xFFFFFFFF,0x123456789ABC) for timer in (0,1,0x7FFF,0x8000,0xFFFF)
        for request in (0,8,0xFFFFFFFF))
    return rows


def setup(address,body,case,seed):
    if address!=ADDRESS or len(body)!=SIZE:
        raise ValueError('Complete registration source extent differs')
    raw=(engine.ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    machine=engine.setup(0x037FBF64,raw[0x3F64:0x4054],seed)
    cpu=machine['cpu']
    cpu.mem_write(address,body)
    cpu.mem_write(0x03807678,bytes(0x0380B4E4-0x03807678))
    cpu.mem_map(IO,0x1000)
    cpu.mem_write(IO,bytes(0x1000))
    machine['regions'][IO]=bytes(0x1000)
    prerequisites=[]
    for enabled,entry in ((case['tick'],0x037FD128),(case['alarm'],0x037FD34C)):
        if enabled:
            result=machine['invoke'](entry)
            if not result['actualReturn']:
                raise ValueError('Original tick/alarm initialization prerequisite failed')
            prerequisites.append(dict(entry=hex(entry),actualReturn=True))
    cpu.mem_write(ALARM,random.Random(seed+733).randbytes(44))
    cpu.mem_write(FLAG,case['enabled'].to_bytes(4,'little'))
    cpu.mem_write(0x038078A0,case['counter'].to_bytes(8,'little'))
    cpu.mem_write(IO+0x100,case['timer'].to_bytes(2,'little'))
    cpu.mem_write(IO+0x214,case['request'].to_bytes(4,'little'))
    visited,calls=[],[]
    def code(uc,pc,size,unused):
        if ADDRESS<=pc<ADDRESS+CODE:
            visited.append(pc)
        if pc==0x037FE65C or pc==0x037FD648:
            raise ValueError('Registration fixture executed its stored callback or timer interrupt handler')
        if pc==0x037FD54C:
            args=[uc.reg_read(register) for register in engine.match_runtime.REGISTERS[:4]]
            sp=uc.reg_read(engine.match_runtime.REGISTERS[13])
            args.extend(int.from_bytes(uc.mem_read(sp+4*i,4),'little') for i in range(3))
            calls.append(args)
    cpu.hook_add(UC_HOOK_CODE,code)
    machine.update(case=case,ownVisited=visited,periodicCalls=calls,prerequisites=prerequisites)
    return machine


def model(memory,case):
    trace=[]
    put=lambda target,value:engine.store(memory,target,value,trace)
    read=lambda target:engine.word(memory,target)
    def half(target,value):
        for base,data in memory.items():
            if base<=target and target+2<=base+len(data):
                data[target-base:target-base+2]=(value&0xFFFF).to_bytes(2,'little')
                return
        raise ValueError('Alarm model halfword write escaped backing')
    if not case['tick'] or not case['alarm'] or read(FLAG):
        return 0,[]
    high=case['counter']&0xFFFFFFFFFFFF
    high+=int(bool(case['request']&8) and not case['timer']&0x8000)
    now=((high<<16)|case['timer'])&0xFFFFFFFFFFFFFFFF
    start=(now+0x82E)&0xFFFFFFFFFFFFFFFF
    put(ALARM,0x037FE65C)
    put(ALARM+4,0)
    put(ALARM+8,0)
    for offset,value in ((0xC,start&0xFFFFFFFF),(0x10,start>>32),(0x14,0),(0x18,0),
        (0x1C,0x82E),(0x20,0),(0x24,start&0xFFFFFFFF),(0x28,start>>32)):
        put(ALARM+offset,value)
    put(0x038078AC,ALARM)
    put(0x038078B0,ALARM)
    put(0x038076BC,0x037FD648)
    put(0x038076C0,1)
    half(IO+0x104,-0x82F)
    half(IO+0x106,0xC1)
    put(IO+0x210,read(IO+0x210)|0x10)
    put(FLAG,1)
    return 1,[[ALARM,start&0xFFFFFFFF,start>>32,0x82E,0,0x037FE65C,0]]


def execute(machine,budget=20000):
    states=[]
    for iteration in range(machine['case']['passes']):
        expected=engine.snapshot(machine)
        value,calls=model(expected,machine['case'])
        machine['periodicCalls'].clear()
        result=machine['invoke'](ADDRESS,[],True,budget)
        if not result['actualReturn']:
            states.append(dict(execution=result,actualReturn=False,postBoundaryStateExcluded=True))
            break
        checked=engine.result(machine,result,expected,value,None)
        if machine['periodicCalls']!=calls:
            raise ValueError('Original periodic-alarm seven physical words differ from independent64-bit clock model')
        states.append(dict(checked,periodicAlarmArguments=machine['periodicCalls'][:],
            actualOriginalHelperReturns={hex(key):count for key,count in sorted(machine['helperReturns'].items())}))
    return dict(case=machine['case'],states=states,visited=sorted(set(machine['ownVisited'])),originalPrerequisites=machine['prerequisites'])
