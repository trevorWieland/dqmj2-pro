import hashlib
import itertools
import struct
from project import ROOT
import wave20261104_main_front_eighth_common as H
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR

SMALL = 0x021d6620
STATE = 0x021d6630
PHASE = 0x021d6714
REGIONS = [(SMALL,4),(STATE,0xd2),(PHASE,1)]


class Machine(H.Machine):
    def __init__(self,address,code,args):
        super().__init__(address,code,bytearray(0x8000),args)
        for base,count in REGIONS:
            self.uc.mem_write(base,bytes((index*13+0x35)&255 for index in range(count)))

    def store(self,uc,kind,where,size,value,unused):
        if any(base <= where and where + size <= base + count for base,count in REGIONS):
            self.writes.append(('caller',where,size,value))
        else:
            super().store(uc,kind,where,size,value,unused)

    def snapshot(self,returned):
        result = super().snapshot(returned)
        result['globals'] = [(base,bytes(self.uc.mem_read(base,count))) for base,count in REGIONS]
        return result

    def word(self,where):
        return struct.unpack('<I',self.uc.mem_read(where,4))[0]

    def byte(self,where):
        return self.uc.mem_read(where,1)[0]


def run(address,code,case):
    kind = case['kind']
    machine = Machine(address,code,[H.RAM] if kind == 'append' else [case['value']] if kind == 'setter' else [])
    uc = machine.uc
    uc.reg_write(UC_ARM_REG_CPSR,case.get('cpsr',0x60000010))
    if kind == 'phase':
        uc.mem_write(PHASE,bytes([case['phase']]))
    if kind in ('setter','pump'):
        uc.mem_write(SMALL,bytes([case['count'],0x45,0x67,0x89]))
        uc.mem_write(STATE+0xd1,bytes([case['flags']]))
    if kind == 'append':
        uc.mem_write(H.RAM,struct.pack('<8i',*case['fields']))
    counters = dict(append=0,step=0,finish=0)
    initial = {base:bytes(uc.mem_read(base,count)) for base,count in REGIONS}
    flags = case.get('flags',0)
    count = case.get('count',0)
    expected_count = count
    expected_flags = flags
    if kind == 'pump':
        steps = 1 if flags & 8 else case['break']+1 if case['break'] >= 0 else 3
        expected_count = (count + sum(case['delta']+index for index in range(steps)))&255
        if flags & 8 or case['break'] >= 0:
            expected_flags &= ~8
        expected_flags = (expected_flags & ~4)|2
    stopped = []

    def hook(uc,pc,size,unused):
        if pc == H.STOP:
            stopped.append(pc)
            uc.emu_stop()
            return
        args = machine.arguments()
        if kind == 'phase' and pc in (0x020cd4e8,0x020c48f8):
            index = len(machine.calls)
            expected = [(0x020cd4e8,[0x26 if case['phase']==2 else 0x27,0x57]),(0x020c48f8,[3 if case['phase']==2 else 1])]
            assert case['phase'] in (2,3) and index < 2
            target,words = expected[index]
            assert pc == target and args[:len(words)] == words
            machine.calls.append(dict(address=hex(pc),arguments=args[:len(words)]))
            machine.finish_call(0x12340000+index)
        elif kind == 'append' and pc == 0x02048f6c:
            assert not machine.calls and args[0] == 1
            machine.calls.append(dict(address=hex(pc),arguments=args[:1]))
            machine.finish_call(case['slot'])
        elif kind == 'append' and pc == 0x02065730:
            index = counters['append']
            assert index < 4
            expected_data = [0x021d65f0,0x021d65fc,0x021d6608,0x021d6614]
            expected_fields = [3,4,0,1]
            assert args == [expected_data[index],expected_fields[index],1,case['slot']]
            stack = uc.reg_read(H.REGISTERS[13])
            incoming = machine.word(stack)
            expected_value = case['fields'][case['slot']] + sum(case['delta']+n for n in range(index))
            assert H.signed(incoming) == expected_value
            assert incoming == machine.word(H.RAM+4*case['slot'])
            machine.calls.append(dict(address=hex(pc),arguments=args+[incoming]))
            counters['append'] += 1
            machine.finish_call(case['delta']+index)
        elif kind == 'pump' and pc == 0x020cb42c:
            assert args[0] == counters['step'] and args[0] < 3
            machine.calls.append(dict(address=hex(pc),arguments=args[:1]))
            machine.finish_call(0x3542)
        elif kind == 'pump' and pc == 0x020cb5c4:
            index = counters['step']
            assert args[0] == index
            stack = uc.reg_read(H.REGISTERS[13])
            assert args[1:] == [stack+2,stack+1,stack]
            before = [machine.byte(where) for where in args[1:]]
            assert before == [((value+index*3)&255) for value in [6,8,6]]
            machine.calls.append(dict(address=hex(pc),arguments=args,pointeeBytes=before))
            for where,value in zip(args[1:],before):
                machine.provide(where,bytes([(value+3)&255]))
            if case['break'] == index:
                machine.provide(STATE+0xd1,bytes([machine.byte(STATE+0xd1)|8]))
            counters['step'] += 1
            machine.finish_call(case['delta']+index)
        elif kind == 'pump' and pc == 0x020cb2fc:
            assert counters['finish'] == 0 and machine.byte(STATE+0xd1)&8 == 0
            counters['finish'] += 1
            machine.calls.append(dict(address=hex(pc),flags=machine.byte(STATE+0xd1),count=machine.byte(SMALL)))
            machine.finish_call(0x2435)
        elif not address <= pc < address+len(code):
            raise AssertionError(('Unexpected caller/provider boundary',hex(pc)))

    uc.hook_add(UC_HOOK_CODE,hook)
    uc.emu_start(address,H.STOP+4,count=5000)
    assert stopped == [H.STOP] and uc.reg_read(UC_ARM_REG_PC) == H.STOP
    snapshot = machine.snapshot(True)
    if kind == 'phase':
        active = case['phase'] in (2,3)
        assert snapshot['registers'][0] == int(active)
        assert len(machine.calls) == (2 if active else 0)
        assert machine.byte(PHASE) == (3 if case['phase']==2 else 0 if case['phase']==3 else case['phase'])
    elif kind == 'append':
        assert counters['append'] == 4
        expected = list(case['fields'])
        expected[case['slot']] += sum(case['delta']+index for index in range(4))
        assert list(struct.unpack('<8i',uc.mem_read(H.RAM,32))) == expected
        assert H.signed(snapshot['registers'][0]) == expected[case['slot']]
    elif kind == 'setter':
        expected = bytearray(initial[SMALL]);expected[1] = case['value']&255
        assert bytes(uc.mem_read(SMALL,4)) == bytes(expected)
        assert machine.byte(STATE+0xd1) == (flags|8)
        assert not machine.calls
    else:
        assert counters['step'] == steps
        assert counters['finish'] == int(bool(flags&8) or case['break'] >= 0)
        assert machine.byte(SMALL) == expected_count
        assert machine.byte(STATE+0xd1) == expected_flags
        assert snapshot['registers'][0] == STATE
    for base,old in initial.items():
        changed = bytearray(old)
        if base == PHASE and kind == 'phase':
            changed[0] = machine.byte(PHASE)
        if base == SMALL and kind == 'setter':
            changed[1] = case['value']&255
        if base == SMALL and kind == 'pump':
            changed[0] = expected_count
        if base == STATE and kind in ('setter','pump'):
            changed[0xd1] = (flags|8) if kind == 'setter' else expected_flags
        assert bytes(uc.mem_read(base,len(old))) == bytes(changed)
    return snapshot


def vectors(address):
    if address == 0x020cc220:
        return [dict(kind='phase',phase=value,cpsr=((value&15)<<28)|0x10) for value in range(256)]
    if address == 0x020cadb4:
        return [dict(kind='append',slot=slot,delta=delta,fields=[initial+index*7 for index in range(8)]) for slot,delta,initial in itertools.product(range(8),[-4,0,7],[-48,0,1000])]
    if address == 0x020cba50:
        words = [-257,-128,-1,0,1,127,128,255,256,0x12345678]
        return [dict(kind='setter',flags=flags,value=words[flags%len(words)],count=(flags*17)&255) for flags in range(256)] + [dict(kind='setter',flags=flags,value=value,count=0x55) for flags,value in itertools.product([0,0x80,0xff],words)]
    assert address == 0x020cba74
    cases = [dict(kind='pump',flags=flags,break_=-1,count=(flags*17)&255,delta=3) for flags in range(256)]
    cases += [dict(kind='pump',flags=flags,break_=stop,count=count,delta=delta) for flags,stop,count,delta in itertools.product([0,2,4,8,0x80,0x8f,0xff],[-1,0,1,2],[0,0xff],[-300,-1,0,255])]
    for case in cases:
        case['break'] = case.pop('break_')
    return cases


def prove(address,native,source):
    results = []
    cases = vectors(address)
    for case in cases:
        original = run(address,native,case)
        rebuilt = run(address,source,case)
        assert original == rebuilt
        results.append(hashlib.sha256(repr(original).encode()).hexdigest())
    return dict(function=hex(address),cases=len(cases),actualNativeCallerReturns=len(cases),actualSourceCallerReturns=len(cases),
        actualNativeAndSourceCallerReturns=2*len(cases),independentRawFieldAndArgumentOraclesPassed=True,allGprsCpsrCalleeSavedStackAndOrderedWritesCompared=True,
        suppliedNativeCalleeBodiesExecuted=0,sourceOrExecutionCreditForSuppliedCallees=0,hardwareOrGameExecutionCredit=0,semanticStateSha256=results,
        oracleScope='Raw phase values, byte/bit positions, repeated signed-byte output pointers, explicit word/stack inputs, caller-local mutation and bounded state transitions only')
