import hashlib
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946
import ov001_action822_machine_20261102 as R

BASE = 0x021D7240
SP = 0x027F0000
STOP = 0x027FF000
INDICES = 0x02500000
TREE = 0x02501000
POINT = 0x02502000
TRIANGLES = 0x02510000
FIND = 0x021DB92C
ENTRY = 0x021DB968


def word(value):
    return value & 0xFFFFFFFF


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


def pack(values):
    return struct.pack('<' + 'I' * len(values), *map(word, values))


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.p = profile
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(BASE, overlay)
        self.ranges = {FIND: 60, ENTRY: 488}
        for address, body in images.items():
            self.u.mem_write(address, body)
            self.ranges[address] = len(body)
        self.beforeIndices = b''.join(struct.pack('<H', value & 0xFFFF) for value in profile['indices'])
        self.u.mem_write(INDICES, self.beforeIndices)
        self.u.mem_write(POINT, pack(profile['point']))
        self.u.mem_write(TREE + profile['node'] * 8, struct.pack('<hhhH', *profile['neighbors'], 0xA55A))
        for index, delta in profile['deltas'].items():
            address = TRIANGLES + int(index) * 0x44 + 0x30
            if any(max(address, code) < min(address + 12, code + len(body)) for code, body in images.items()):
                raise ValueError('892 synthetic center overlaps private code')
            center = [word(point - difference) for point, difference in zip(profile['point'], delta)]
            self.u.mem_write(address, pack(center))
        self.instructions = 0
        self.ownPcs = set()
        self.helperPcs = set()
        self.calls = []
        self.returns = []
        self.frames = []
        self.writes = []
        self.minSp = SP
        self.lastPc = None
        self.returned = False
        self.top = None
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, unused):
        if not 0x02000000 <= address < address + size <= 0x02800000:
            raise ValueError(('892 write outside RAM', hex(address), size))
        if not SP - 0x1000 <= address < SP:
            self.writes.append([address, size, value])

    def code(self, u, pc, size, unused):
        self.instructions += 1
        self.minSp = min(self.minSp, u.reg_read(R.UC_ARM_REG_SP))
        if self.instructions > 20000:
            raise ValueError('892 instruction bound')
        if self.frames and pc == self.frames[-1]['lr']:
            frame = self.frames.pop()
            if self.lastPc != 0x021DB964 or u.reg_read(R.UC_ARM_REG_SP) != frame['sp'] or [u.reg_read(reg) for reg in R.REGS[4:12]] != frame['saved']:
                raise ValueError('892 native lookup physical return/ABI failure')
            self.returns.append(dict(returnInstruction='0x21db964', returnedWord=u.reg_read(R.REGS[0])))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if ENTRY <= pc < ENTRY + 488:
            self.ownPcs.add(pc)
        if FIND <= pc < FIND + 60:
            self.helperPcs.add(pc)
        if pc == FIND and self.top != FIND:
            args = [u.reg_read(reg) for reg in R.REGS[:3]]
            self.calls.append(dict(target=hex(FIND), callerWords=args))
            self.frames.append(dict(lr=u.reg_read(R.UC_ARM_REG_LR), sp=u.reg_read(R.UC_ARM_REG_SP), saved=[u.reg_read(reg) for reg in R.REGS[4:12]]))
        if not any(address <= pc < address + length for address, length in self.ranges.items()):
            raise ValueError(('892 unsupported edge', hex(pc)))
        self.lastPc = pc

    def run(self, start, top=ENTRY):
        self.top = top
        u = self.u
        p = self.p
        u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
        for i, reg in enumerate(R.REGS):
            u.reg_write(reg, 0x81810000 + i * 257)
        saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
        args = [word(p['needle']), INDICES, word(p['count']), 0x13579BDF] if top == FIND else [p['node'], TREE if not p.get('invalidUnused') else 0, INDICES, word(p['count'])]
        for reg, value in zip(R.REGS[:4], args):
            u.reg_write(reg, value)
        u.reg_write(R.UC_ARM_REG_SP, SP)
        u.reg_write(R.UC_ARM_REG_LR, STOP)
        u.mem_write(SP, pack([TRIANGLES, POINT if not p.get('invalidUnused') else 0, p['limit']]))
        u.emu_start(start, STOP + 4, count=20001)
        if not self.returned or self.frames or u.reg_read(R.UC_ARM_REG_SP) != SP or [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
            raise ValueError('892 proper return/SP/callee-saved failure')
        memory = bytes(u.mem_read(0x02000000, 0x00800000))
        return dict(registers=[u.reg_read(reg) for reg in R.REGS], cpsr=u.reg_read(R.UC_ARM_REG_CPSR), actuallyReturned=True, indicesHex=bytes(u.mem_read(INDICES, len(self.beforeIndices))).hex(), calls=self.calls, originalHelperPhysicalReturns=self.returns, writes=self.writes, ownPcs=sorted(self.ownPcs), helperPcs=sorted(self.helperPcs), privateStackStart=self.minSp, memory=memory, memorySha256=hashlib.sha256(memory).hexdigest(), instructions=self.instructions)
