import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946
import ov001_action822_machine_20261102 as R

ENTRY = 0x02200D54
STATE = 0x02239C10
ROWS = 0x0223A25C
CACHE = 0x0222EDCC
ACTORS = 0x02236F6C
SP = 0x027F0000
STOP = 0x027FF000
HELPERS = {0x02202360: 20, 0x021DB438: 124}
PROVIDERS = {0x022028C8: 1, 0x021FE74C: 1, 0x021FE2B8: 2, 0x022023C4: 1}



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
        self.ranges = dict(HELPERS) | {ENTRY: 1132}
        for address, image in images.items():
            self.u.mem_write(address, image)
            self.ranges[address] = len(image)
        self.p = profile
        if struct.unpack_from('<I', overlay, 0x02202370 - 0x021D7240)[0] != ROWS:
            raise ValueError('859 measured fixed row getter differs')
        self.row = ROWS + 2 * 0xF0
        rows = bytearray([0xA5] * (6 * 0xF0))
        rows[2 * 0xF0 + 8] = profile['slot']
        self.beforeRows = bytes(rows)
        self.u.mem_write(ROWS, self.beforeRows)
        state = bytearray([0xA5] * 0x30)
        state[0x0C] = 2
        self.beforeState = bytes(state)
        self.u.mem_write(STATE, self.beforeState)
        self.beforeCache = bytes([0xA5] * 3)
        self.u.mem_write(CACHE, self.beforeCache)
        self.actor = ACTORS + profile['slot'] * 0x440
        actors = bytearray([0xA5] * (3 * 0x440))
        actors[profile['slot'] * 0x440 + 0x35C] = profile['prior']
        actors[profile['slot'] * 0x440 + 0x35D] = profile['flags']
        self.beforeActors = bytes(actors)
        self.u.mem_write(ACTORS, self.beforeActors)
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
            raise ValueError(('859 outside RAM write', hex(address), size))
        if not 0x027E0000 <= address < 0x027F0100:
            self.writes.append((address, size, value))

    def provider(self, pc, args):
        return 0xA7310000 + self.p['ordinal']

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 10000:
            raise ValueError('859 instruction bound')
        if self.pending and pc == self.pending[-1][1]:
            self.actualReturns += 1
            address, lr = self.pending.pop()
            self.completed.append(dict(address=hex(address), rawR0=u.reg_read(R.REGS[0]), actuallyReturned=True))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if ENTRY <= pc < ENTRY + 1132:
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
            raise ValueError(('859 unsupported native edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
        for index, register in enumerate(R.REGS):
            u.reg_write(register, 0x81810000 + index * 0x101 + self.p['ordinal'])
        saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
        u.reg_write(R.UC_ARM_REG_SP, SP)
        u.reg_write(R.UC_ARM_REG_LR, STOP)
        u.reg_write(R.REGS[0], self.p['selector'])
        u.emu_start(entry, STOP + 4, count=10001)
        if not self.returned or self.pending or u.reg_read(R.UC_ARM_REG_SP) != SP:
            raise ValueError('859 proper top/helper return missing')
        if [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
            raise ValueError('859 callee-saved registers differ')
        memory = bytearray(u.mem_read(0x02000000, 0x00800000))
        memory[ENTRY - 0x02000000:ENTRY - 0x02000000 + 1132] = bytes(1132)
        memory[SP - 0x02000000 - 0x100:SP - 0x02000000] = bytes(0x100)
        return dict(registers=[u.reg_read(reg) for reg in R.REGS], cpsr=u.reg_read(R.UC_ARM_REG_CPSR), actuallyReturned=True, calls=self.calls, rawCalls=self.rawCalls, nativeEntries=self.nativeEntries, nativeCompletions=self.completed, actualNativeReturnInstructions=self.actualReturns, instructions=self.instructions, writes=self.writes, ownPcs=sorted(self.ownPcs), rows=bytes(u.mem_read(ROWS, 6 * 0xF0)), state=bytes(u.mem_read(STATE, 0x30)), actors=bytes(u.mem_read(ACTORS, 3 * 0x440)), cache=bytes(u.mem_read(CACHE, 3)), observableMemory=bytes(memory))
