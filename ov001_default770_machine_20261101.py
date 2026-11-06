import struct
import match_runtime as c
import trace_ov001_reward252_20261031 as F
import ov001_stat_initialization_fixture_20261029 as S
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_LR
VIEW_BASE = 35393300
VIEWS = [VIEW_BASE + index * 528 for index in [0, 1, 2, 6, 7, 8]]

class Machine(F.TraceMachine):

    def __init__(self, main, save, assets, overlay, expected_flag202=0):
        self.expectedFlag202 = expected_flag202
        self.flag202Writes = []
        self.statPending = None
        self.rngPending = None
        self.statResults = []
        self.rngResults = []
        super().__init__(main, save, assets, overlay)
        self.u.hook_add(UC_HOOK_CODE, self.stat_observe)

    def invoke(self, stage, address, args=()):
        self.stage = stage
        result = self.call(address, args, limit=800000)
        self.finish_frames(F.STOP)
        self.division_total += len(self.divisions)
        if self.frames or self.statPending is not None or self.rngPending is not None:
            raise ValueError('770 native entry did not finish')
        self.stages.append(dict(stage=stage, address=hex(address), actualReturn=True, result=result))
        return result

    def write(self, u, access, address, size, value, data):
        super().write(u, access, address, size, value, data)
        for view in VIEWS:
            target = view + 514
            if address <= target < address + size:
                self.flag202Writes.append(dict(stage=self.stage, pc=hex(u.reg_read(UC_ARM_REG_PC)), view=hex(view), writeAddress=hex(address), writeWidth=size, byteValue=value >> 8 * (target - address) & 255))

    def stat_observe(self, u, pc, width, data):
        if self.rngPending is not None and pc == self.rngPending['returnPc']:
            observed = self.rngPending
            self.rngPending = None
            expected = observed['expected']
            if u.reg_read(F.REGS[0]) != expected['value'] or self.read_word(34562116) != expected['stateAfter']:
                raise ValueError('770 native RNG return/state differs')
            self.rngResults.append(dict(stage=self.stage, **expected, actuallyReturned=True))
        if self.statPending is not None and pc == self.statPending['returnPc']:
            pending = self.statPending
            self.statPending = None
            if bytes(u.mem_read(pending['actor'], 1088)) != pending['expectedActor'] or self.read_word(34562116) != pending['expectedSeed'] or u.reg_read(F.REGS[0]) != pending['expectedR0']:
                raise ValueError('770 independent native stat formation model differs')
            if len(self.rngResults) - pending['rngStart'] != len(pending['draws']):
                raise ValueError('770 native stat draw count differs')
            self.statResults.append(dict(stage=self.stage, view=hex(pending['view']), actor=hex(pending['actor']), view202=pending['flag202'], actualFeatureBytes=pending['features'], specialMask=pending['mask'], baseStats=pending['base'], currentHp=pending['hp'], currentMp=pending['mp'], rngBefore=pending['seed'], rngAfter=pending['expectedSeed'], actualRngReturns=len(pending['draws']), recordDerivedActor1ffBefore=pending['actorBefore'][511], recordDerivedActor1ffAfter=u.mem_read(pending['actor'] + 511, 1)[0], actor31cBefore=pending['actorBefore'][796], actor31cAfterStat=u.mem_read(pending['actor'] + 796, 1)[0], rawR0=pending['expectedR0'], independentActorModel=True, actuallyReturned=True))
        if pc == 35494404:
            if self.statPending is not None:
                raise ValueError('770 unexpected recursive modifier initializer')
            view, actor = [u.reg_read(r) for r in F.REGS[:2]]
            record = bytes(u.mem_read(view, 528))
            before = bytes(u.mem_read(actor, 1088))
            featureBytes = record[74:138]
            features = list(featureBytes[:featureBytes.index(0)] if 0 in featureBytes else featureBytes)
            mask = sum((1 << i for i in range(8) if 79 + i in features))
            stats = list(struct.unpack_from('<8h', before, 492))
            base = [stats[0], stats[1], *stats[4:]]
            seed = self.read_word(34562116)
            flag = record[514]
            if flag != self.expectedFlag202 or flag not in [0, 1] or any((value < 0 for value in base)):
                raise ValueError('770 expected native-cleared default modifier path and nonnegative bases')
            output, nextSeed, raw, draws = S.model(before, record, base, stats[2], stats[3], dict(supplied=bool(flag), traitsMask=mask, rngState=seed))
            if flag:
                raw = view + 452
            self.statPending = dict(returnPc=u.reg_read(UC_ARM_REG_LR) & ~1, view=view, actor=actor, expectedActor=output, expectedSeed=nextSeed, expectedR0=raw, draws=draws, rngStart=len(self.rngResults), flag202=flag, features=features, mask=mask, base=base, hp=stats[2], mp=stats[3], seed=seed, actorBefore=before)
        if pc == 33804948:
            if self.statPending is None or self.rngPending is not None:
                raise ValueError('770 RNG outside the qualified default modifier path')
            pending = self.statPending
            ordinal = len(self.rngResults) - pending['rngStart']
            if ordinal >= len(pending['draws']):
                raise ValueError('770 unexpected native RNG invocation')
            expected = pending['draws'][ordinal]
            if u.reg_read(F.REGS[0]) != expected['bound'] or self.read_word(34562116) != expected['stateBefore']:
                raise ValueError('770 native RNG bound/order/seed differs')
            self.rngPending = dict(returnPc=u.reg_read(UC_ARM_REG_LR) & ~1, expected=expected)
