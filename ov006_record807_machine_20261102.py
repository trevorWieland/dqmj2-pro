import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR

REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
ENTRY = 0x021DD5CC
SP = 0x027F0000
STOP = 0x027FF000
TEMPLATE = 0x021B9EA8
RECORDS = 0x021BD674
RECORD = RECORDS + 3 * 132
RNG = 0x020F6044
BASE_GETTERS = [0x02044E34, 0x02044E70, 0x02044EAC, 0x02044EE8, 0x02044F24, 0x02044F60]
CAP_GETTERS = [address + 16 for address in BASE_GETTERS]
CALLBACKS = [0x02044A14 + index * 0x44 for index in range(6)]
HELPERS = {0x020642F8: 12, 0x02062A10: 64, 0x02062E44: 136, 0x02063038: 24, 0x02008D78: 148, 0x0203D294: 72, 0x02026350: 484, 0x021DD57C: 80}
PROVIDERS = {0x0206271C: 2, 0x021D83C8: 0, 0x021DA654: 0, 0x021DD4C0: 1, 0x021DD4F0: 7, 0x021DD4D8: 2, 0x021DD3C0: 3, 0x021DD420: 2, 0x021DD3A8: 2, 0x021DD434: 3, 0x0207AEBC: 3, 0x021DDF58: 2, 0x021D83E4: 0}
PROVIDERS.update({address: 2 for address in BASE_GETTERS})
PROVIDERS.update({address: 6 for address in CAP_GETTERS})


def pack(words):
    return struct.pack('<' + 'I' * len(words), *[value & 0xFFFFFFFF for value in words])


def signed16(value):
    value &= 0xFFFF
    return value - 65536 if value & 0x8000 else value


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(0x021D7240, overlay)
        for address, body in images.items():
            self.u.mem_write(address, body)
        if list(struct.unpack_from('<3I', main, 0x642F8)) != [0xE59F0000, 0xE12FFF1E, TEMPLATE]:
            raise ValueError('807 original template getter differs')
        self.p = profile
        self.ranges = dict(HELPERS)
        self.ranges[ENTRY] = 1092
        self.ranges.update({address: len(body) for address, body in images.items()})
        self.uid = 0x88000000 + profile['ordinal'] + 1
        self.features = [([1, 127, 128, 255, 42][index] if profile['mask'] & (1 << index) else 0) for index in range(5)]
        template = bytearray([0xA5] * 12)
        struct.pack_into('<h', template, 2, profile['species'])
        template[5] = profile['level']
        template[6] = profile['variant']
        template[7:12] = bytes(self.features)
        self.u.mem_write(TEMPLATE, bytes(template))
        self.u.mem_write(RECORDS, bytes(100 * 132))
        record = bytearray([0xA5] * 132)
        struct.pack_into('<I', record, 0x14, self.uid)
        struct.pack_into('<h', record, 0x18, profile['species'])
        record[0x1A] = profile['variant']
        self.u.mem_write(RECORD, bytes(record))
        self.beforeRecord = bytes(record)
        self.u.mem_write(RNG, pack([profile['seed']]))
        self.calls = []
        self.rawCalls = []
        self.nativeEntries = []
        self.completed = []
        self.pending = []
        self.actualReturns = 0
        self.instructions = 0
        self.writes = []
        self.returned = False
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, unused):
        if not 0x02000000 <= address < address + size <= 0x02800000:
            raise ValueError(('807 outside RAM write', hex(address), size))
        if not 0x027E0000 <= address < 0x027F0100:
            self.writes.append((address, size, value))

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 30000:
            raise ValueError('807 instruction bound')
        if self.pending and pc == self.pending[-1][1]:
            self.actualReturns += 1
            address, lr = self.pending.pop()
            self.completed.append(dict(address=hex(address), rawR0=u.reg_read(REGS[0]), rawR1=u.reg_read(REGS[1]), actuallyReturned=True))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if pc in HELPERS:
            self.pending.append((pc, u.reg_read(UC_ARM_REG_LR)))
            words = [u.reg_read(reg) for reg in REGS[:4]]
            entry = dict(address=hex(pc), incomingWords=words)
            if pc == 0x02062E44:
                entry['twoByteInput'] = bytes(u.mem_read(words[2], 2)).hex()
            self.nativeEntries.append(entry)
        if pc in PROVIDERS:
            words = [u.reg_read(reg) for reg in REGS[:4]]
            stack = list(struct.unpack('<4I', bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), 16))))
            args = (words + stack)[:PROVIDERS[pc]]
            result = 0
            if pc == 0x0206271C:
                result = self.uid
            elif pc == 0x021DD4C0:
                result = 0x02510020
            elif pc in BASE_GETTERS:
                result = self.p['baseWords'][BASE_GETTERS.index(pc)]
            elif pc in CAP_GETTERS:
                result = self.p['capWords'][CAP_GETTERS.index(pc)]
            elif pc == 0x021DD4F0:
                if args[6] not in CALLBACKS:
                    raise ValueError('807 unsupported callback identity')
                result = self.p['statWords'][CALLBACKS.index(args[6])]
            elif pc == 0x021DD3C0:
                result = 0x02520020
            elif pc == 0x021DD420:
                result = 0x11000000 + args[1]
            elif pc == 0x021DD434:
                result = 0xABC00000 + args[0] * 5 + args[1]
            elif pc == 0x021D83E4:
                result = self.p['returnWord']
            self.calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=result))
            self.rawCalls.append(dict(target=hex(pc), registers=words, stackWords=stack))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(REGS[index], (0xCACE0000 + index * 0x101 + self.p['ordinal']) & 0xFFFFFFFF)
            u.reg_write(REGS[0], result & 0xFFFFFFFF)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        if not any(address <= pc < address + size for address, size in self.ranges.items()):
            raise ValueError(('807 unsupported native edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(UC_ARM_REG_CPSR, 0xD3)
        for index, reg in enumerate(REGS):
            u.reg_write(reg, 0x51510000 + index * 0x101)
        saved = [u.reg_read(reg) for reg in REGS[4:12]]
        u.reg_write(REGS[0], self.p['controlWord'])
        u.reg_write(UC_ARM_REG_SP, SP)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.emu_start(entry, STOP + 4, count=30001)
        if not self.returned or self.pending or u.reg_read(UC_ARM_REG_SP) != SP:
            raise ValueError('807 missing proper top/native return')
        if [u.reg_read(reg) for reg in REGS[4:12]] != saved:
            raise ValueError('807 callee-saved corruption')
        return dict(rawR0=u.reg_read(REGS[0]), actuallyReturned=True, calls=self.calls, rawCalls=self.rawCalls, nativeEntries=self.nativeEntries, nativeCompletions=self.completed, actualNativeReturnInstructions=self.actualReturns, instructions=self.instructions, writes=self.writes, record=bytes(u.mem_read(RECORD, 132)), rng=struct.unpack('<I', bytes(u.mem_read(RNG, 4)))[0], memory=bytes(u.mem_read(0x02000000, 0x007E0000)) + bytes(u.mem_read(0x027F0100, 0xFF00)))


def model(vm, result):
    p = vm.p
    count = sum(bool(value) for value in vm.features)
    record = bytearray(vm.beforeRecord)
    level = p['level']
    record[0x30] = level
    record[0x1C] = 10 if level > 75 else 4 if level > 50 else 0
    for offset, value in zip([0x20, 0x22, 0x28, 0x2A, 0x2C, 0x2E], p['statWords']):
        struct.pack_into('<H', record, offset, value & 0xFFFF)
    record[0x24:0x26] = record[0x20:0x22]
    record[0x26:0x28] = record[0x22:0x24]
    struct.pack_into('<II', record, 0x34, 0x11000000 + level, 0x11000001 + level)
    struct.pack_into('<H', record, 0x3C, (level * 5 + count) & 0xFFFF)
    for index in range(count):
        record[0x7A + index * 2:0x7C + index * 2] = bytes([vm.features[index], 0])
    rng = (p['seed'] * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
    draw = (rng >> 16) % 17
    record[0x1B] = 0 if draw < 8 else 1 if draw > 8 else 2
    failures = []
    if result['record'] != record:
        failures.append('132-byte supplied-record view')
    if result['rng'] != rng or sum(row['address'] == '0x203d294' for row in result['nativeEntries']) != 1:
        failures.append('actual single RNG17 draw')
    if result['rawR0'] != p['returnWord']:
        failures.append('physical R0')
    for index, callback in enumerate(CALLBACKS):
        rows = [row for row in result['calls'] if row['target'] == '0x21dd4f0' and row['callerWords'][6] == callback]
        expected = [0x02510020, p['species'] & 0xFFFFFFFF, p['variant'], level, signed16(p['baseWords'][index]) & 0xFFFFFFFF, signed16(p['capWords'][index]) & 0xFFFFFFFF, callback]
        if len(rows) != 1 or rows[0]['callerWords'] != expected:
            failures.append('seven-word stat provider ' + hex(callback))
    copies = [row for row in result['nativeEntries'] if row['address'] == '0x2062e44']
    expectedPairs = [bytes([vm.features[index], 0]).hex() for index in range(count)]
    if [row['twoByteInput'] for row in copies] != expectedPairs:
        failures.append('native prefix-count two-byte forwarding')
    return failures
