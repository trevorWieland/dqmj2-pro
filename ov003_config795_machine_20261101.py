import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR

REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
ENTRY = 0x021DD300
SP = 0x027F0000
STOP = 0x027FF000
STATE = 0x021E06B8
INPUT = 0x020EDEB8
SETTINGS = 0x021D4CF4
CUSTOM = 0x021D4D10
TABLE = 0x021E038C
FLAGS = 0x021E0A18
COPY = 0x021E0A30
VALUES = 0x021E0678
DIRTY = 0x021E0670
HELPERS = {0x0202A634: 12, 0x020C36AC: 12, 0x021DAD9C: 12, 0x021DA3E4: 24, 0x021DA3D0: 20, 0x02008E0C: 0x130}
HELPERS.update({address: 16 for address in range(0x020C35EC, 0x020C36AC, 32)})
PROVIDERS = {0x0205E7A8: 2, 0x021DEAF8: 1, 0x021DEA38: 6}
PRESETS = {0: [0, 2, 0, 2, 1, 2], 1: [1, 2, 1, 1, 1, 2], 2: [2, 2, 1, 2, 2, 0]}


def pack(words):
    return struct.pack('<' + 'I' * len(words), *[word & 0xFFFFFFFF for word in words])


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(0x021D7240, overlay)
        for address, body in images.items():
            self.u.mem_write(address, body)
        self.images = images
        self.p = profile
        self.ranges = dict(HELPERS, **{})
        self.ranges[ENTRY] = 756
        self.ranges.update({address: len(body) for address, body in images.items()})
        self.instructions = 0
        self.frames = []
        self.completed = []
        self.actualReturns = 0
        self.returned = False
        self.calls = []
        self.rawCalls = []
        self.arrayInputs = []
        self.writes = []
        self.u.mem_write(STATE, pack([profile['state']]))
        self.u.mem_write(INPUT, struct.pack('<HH', 0xA55A, profile['mask']))
        self.u.mem_write(SETTINGS, pack([0x80000000 + index for index in range(7)]))
        self.u.mem_write(CUSTOM, pack(profile['custom']))
        self.table = [((index * 257 + profile['salt']) & 0xFFFF) for index in range(256)]
        self.u.mem_write(TABLE, struct.pack('<256H', *self.table))
        for address, size in [(FLAGS, 16), (COPY, 24), (VALUES, 24), (DIRTY, 8)]:
            self.u.mem_write(address, bytes([0xA5]) * size)
        self.before = {address: bytes(self.u.mem_read(address, size)) for address, size in [(FLAGS, 16), (COPY, 24), (VALUES, 24), (DIRTY, 8), (SETTINGS, 28), (CUSTOM, 24)]}
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, unused):
        if not 0x02000000 <= address < address + size <= 0x02800000:
            raise ValueError(('795 outside mapped write', hex(address), size))
        if not 0x027E0000 <= address < 0x027F0100:
            self.writes.append((address, size, value))

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 20000:
            raise ValueError('795 instruction bound')
        if self.frames and pc == self.frames[-1][1]:
            self.actualReturns += 1
            while self.frames and self.frames[-1][1] == pc:
                address, lr = self.frames.pop()
                self.completed.append(dict(address=hex(address), rawR0=u.reg_read(REGS[0]), actuallyReturned=True))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if pc in PROVIDERS:
            words = [u.reg_read(reg) for reg in REGS[:4]]
            stack = list(struct.unpack('<4I', bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), 16))))
            arguments = (words + stack)[:PROVIDERS[pc]]
            self.calls.append(dict(target=hex(pc), callerPreparedWords=arguments))
            self.rawCalls.append(dict(target=hex(pc), registers=words, stackWords=stack))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(REGS[index], (0xCACE0000 + index * 0x101 + self.p['ordinal']) & 0xFFFFFFFF)
            u.reg_write(REGS[0], self.p['serviceReturn'])
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        if pc in HELPERS:
            self.frames.append((pc, u.reg_read(UC_ARM_REG_LR)))
            if pc == 0x021DA3E4:
                self.arrayInputs.append(list(struct.unpack('<6I', bytes(u.mem_read(u.reg_read(REGS[0]), 24)))))
        if not any(address <= pc < address + size for address, size in self.ranges.items()):
            raise ValueError(('795 unsupported original edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(UC_ARM_REG_CPSR, 0xD3)
        for index, reg in enumerate(REGS):
            u.reg_write(reg, 0x51510000 + index * 0x101)
        saved = [u.reg_read(reg) for reg in REGS[4:12]]
        u.reg_write(UC_ARM_REG_SP, SP)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.emu_start(entry, STOP + 4, count=20001)
        if not self.returned or self.frames or u.reg_read(UC_ARM_REG_SP) != SP:
            raise ValueError('795 no proper top return')
        if [u.reg_read(reg) for reg in REGS[4:12]] != saved:
            raise ValueError('795 callee-saved corruption')
        return dict(rawR0=u.reg_read(REGS[0]), actuallyReturned=True, calls=self.calls, rawCalls=self.rawCalls, arrayInputs=self.arrayInputs, writes=self.writes, actualNativeReturnInstructions=self.actualReturns, nativeCompletions=self.completed, instructions=self.instructions, memory=bytes(u.mem_read(0x02000000, 0x007E0000)) + bytes(u.mem_read(0x027F0100, 0xFF00)))


def model(vm, result):
    p = vm.p
    mode = p['state']
    low = mode & 255
    mask = p['mask']
    expected = dict(vm.before)
    values = PRESETS.get(mode, [3] + p['custom'][1:] if mode == 3 else None)
    if values is not None:
        expected[VALUES] = pack(values)
        dirty = bytearray(expected[DIRTY])
        dirty[4:8] = pack([1])
        expected[DIRTY] = bytes(dirty)
    calls = []
    flags = bytearray(expected[FLAGS])
    expectedR0 = mask
    if mask & 1:
        if low in PRESETS:
            expected[SETTINGS] = expected[SETTINGS][:4] + pack(PRESETS[low])
            flags[12:16] = pack([4])
        elif low == 3:
            custom = [3] + p['custom'][1:]
            expected[CUSTOM] = pack(custom)
            expected[COPY] = pack(custom)
            flags[4:8] = pack([1])
            flags[1] = 1
            flags[12:16] = pack([1])
            flags[0] = 0
        calls.append(dict(target=hex(0x0205E7A8), callerPreparedWords=[0xFFFFFFFF, 0x52]))
        expectedR0 = p['serviceReturn']
    elif mask & 2:
        flags[12:16] = pack([4])
        calls.append(dict(target=hex(0x0205E7A8), callerPreparedWords=[0xFFFFFFFF, 0x53]))
        expectedR0 = p['serviceReturn']
    elif mask & 0x800:
        calls += [dict(target=hex(0x021DEAF8), callerPreparedWords=[STATE]), dict(target=hex(0x021DEA38), callerPreparedWords=[20, 1, vm.table[low], 1, 1, 0x57])]
        flags[12:16] = pack([3])
        expectedR0 = FLAGS
    expected[FLAGS] = bytes(flags)
    failures = [hex(address) for address, value in expected.items() if bytes(vm.u.mem_read(address, len(value))) != value]
    if result['calls'] != calls:
        failures.append('caller-prepared service words')
    if result['arrayInputs'] != ([values] if values is not None else []):
        failures.append('contiguous six-word input')
    if result['rawR0'] != expectedR0:
        failures.append('physical R0')
    return failures
