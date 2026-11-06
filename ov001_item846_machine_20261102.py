import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946
import ov001_action822_machine_20261102 as R

ENTRY = 0x0220BFC0
STATE = 0x0223E088
TABLE = 0x02510000
SP = 0x027F0000
STOP = 0x027FF000
HELPERS = {0x0220B770: 16, 0x0220B74C: 16, 0x0220B794: 16, 0x021DB438: 124, 0x02065D88: 24}
PROVIDERS = {0x0220B9E0: 0, 0x021E3544: 2, 0x0202AC08: 1, 0x021EEA10: 2, 0x0205C904: 1, 0x0220BBB8: 1, 0x0220BD30: 4, 0x0220BF30: 2, 0x0205D6F4: 1, 0x0220BDE8: 3, 0x021EEB70: 1, 0x0202AC4C: 1, 0x021F14A4: 0}


def word(value):
    return value & 0xFFFFFFFF


def pack(values):
    return struct.pack('<' + 'I' * len(values), *map(word, values))


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(0x021D7240, overlay)
        self.ranges = dict(HELPERS) | {ENTRY: 696}
        for address, image in images.items():
            self.u.mem_write(address, image)
            self.ranges[address] = len(image)
        self.p = profile
        self.tableGlobal = struct.unpack_from('<I', main, 0x65D9C)[0]
        self.u.mem_write(self.tableGlobal, pack([TABLE]))
        self.u.mem_write(TABLE, bytes(256 * 88))
        self.row = TABLE + profile['item'] * 88
        self.u.mem_write(self.row + 0x1A, struct.pack('<H', profile['resource']))
        self.u.mem_write(self.row + 0x29, bytes([profile['subtype']]))
        self.u.mem_write(self.row + 0x2C, bytes([profile['kind']]))
        self.beforeTable = bytes(self.u.mem_read(TABLE, 256 * 88))
        state = bytearray([0xA5] * 48)
        state[0x15] = profile['phase']
        state[0x14] = profile['oldToken']
        state[0x1A] = profile['side']
        state[0x1B] = profile['item']
        state[0x1C] = profile['slot']
        struct.pack_into('<H', state, 0x18, profile['oldHalf'])
        self.beforeState = bytes(state)
        self.u.mem_write(STATE, self.beforeState)
        self.calls = []
        self.rawCalls = []
        self.nativeEntries = []
        self.completed = []
        self.pending = []
        self.actualReturns = 0
        self.instructions = 0
        self.writes = []
        self.ownPcs = set()
        self.returned = False
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, unused):
        if not 0x02000000 <= address < address + size <= 0x02800000:
            raise ValueError(('846 outside RAM write', hex(address), size))
        if not 0x027E0000 <= address < 0x027F0100:
            self.writes.append((address, size, value))

    def provider(self, pc, args):
        if pc == 0x0220BBB8:
            return self.p['tokenWord']
        if pc == 0x0220BF30:
            return self.p['halfWord']
        if pc == 0x0205D6F4:
            return self.p['timerWord']
        return 0xA7310000 + self.p['ordinal']

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 10000:
            raise ValueError('846 instruction bound')
        if self.pending and pc == self.pending[-1][1]:
            self.actualReturns += 1
            address, lr = self.pending.pop()
            self.completed.append(dict(address=hex(address), rawR0=u.reg_read(R.REGS[0]), actuallyReturned=True))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if ENTRY <= pc < ENTRY + 688:
            self.ownPcs.add(pc)
        if pc in HELPERS:
            self.pending.append((pc, u.reg_read(R.UC_ARM_REG_LR)))
            self.nativeEntries.append(dict(address=hex(pc), rawWords=[u.reg_read(reg) for reg in R.REGS[:4]]))
        if pc in PROVIDERS:
            words = [u.reg_read(reg) for reg in R.REGS[:4]]
            stack = list(struct.unpack('<4I', bytes(u.mem_read(u.reg_read(R.UC_ARM_REG_SP), 16))))
            args = (words + stack)[:PROVIDERS[pc]]
            result = word(self.provider(pc, args))
            self.calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=result))
            self.rawCalls.append(dict(target=hex(pc), registers=words, stackWords=stack))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(R.REGS[index], word(0xFACE0000 + index * 0x101 + self.p['ordinal']))
            cpsr = u.reg_read(R.UC_ARM_REG_CPSR)
            u.reg_write(R.UC_ARM_REG_CPSR, (cpsr & 0x0FFFFFFF) | ((self.p['ordinal'] & 15) << 28))
            u.reg_write(R.REGS[0], result)
            u.reg_write(R.UC_ARM_REG_PC, u.reg_read(R.UC_ARM_REG_LR))
            return
        if not any(address <= pc < address + count for address, count in self.ranges.items()):
            raise ValueError(('846 unsupported native edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
        for index, register in enumerate(R.REGS):
            u.reg_write(register, 0x81810000 + index * 0x101 + self.p['ordinal'])
        saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
        u.reg_write(R.UC_ARM_REG_SP, SP)
        u.reg_write(R.UC_ARM_REG_LR, STOP)
        u.emu_start(entry, STOP + 4, count=10001)
        if not self.returned or self.pending or u.reg_read(R.UC_ARM_REG_SP) != SP:
            raise ValueError('846 proper top/helper return missing')
        if [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
            raise ValueError('846 callee-saved registers differ')
        return dict(registers=[u.reg_read(reg) for reg in R.REGS], cpsr=u.reg_read(R.UC_ARM_REG_CPSR), actuallyReturned=True, calls=self.calls, rawCalls=self.rawCalls, nativeEntries=self.nativeEntries, nativeCompletions=self.completed, actualNativeReturnInstructions=self.actualReturns, instructions=self.instructions, writes=self.writes, ownPcs=sorted(self.ownPcs), table=bytes(u.mem_read(TABLE, 256 * 88)), state=bytes(u.mem_read(STATE, 48)), memory=bytes(u.mem_read(0x02000000, 0x00800000)))
