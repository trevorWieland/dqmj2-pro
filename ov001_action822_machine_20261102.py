import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR

REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
ENTRY = 0x021F2878
CONTEXT = 0x0223989C
GATE = 0x0222ED14
MOVES = 0x02510000
DESCRIPTORS = 0x02520000
FRAME = 0x02530000
SP = 0x027F0000
STOP = 0x027FF000
ACTOR_BASES = [0x02236F6C, 0x022362AC, 0x022355EC, 0x02237C2C]
TRAITS = [0x23C, 0x23E, 0x254, 0x23D, 0x255, 0x266]
HELPERS = {0x0207AFEC: 24, 0x0207B004: 40, 0x0207B02C: 44, 0x0207B244: 172, 0x021DB438: 124, 0x021DB8D0: 72, 0x021DBD30: 12, 0x021DB834: 132, 0x021DB7CC: 104, 0x021E29E8: 16}
PROVIDERS = {0x021F1354: 4, 0x021F1414: 1, 0x021F1438: 1, 0x021F1D54: 1, 0x021D9494: 3, 0x02202528: 2, 0x0202AC08: 1, 0x021EEA10: 2, 0x0205C904: 1, 0x0205D790: 1, 0x021EEC7C: 3, 0x021F94D8: 2, 0x021D9534: 4, 0x0205D718: 1, 0x021EEB70: 1, 0x0202AC4C: 1, 0x021F14A4: 0, 0x021DCA54: 3, 0x02202540: 2, 0x021DD02C: 3, 0x022024D4: 3, 0x0207CE3C: 3, 0x021DBCF0: 1}


def pack(words):
    return struct.pack('<' + 'I' * len(words), *[value & 0xFFFFFFFF for value in words])


def s16(word):
    word &= 0xFFFF
    return word - 0x10000 if word & 0x8000 else word


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(0x021D7240, overlay)
        self.ranges = dict(HELPERS)
        self.ranges[ENTRY] = 1540
        for address, body in images.items():
            self.u.mem_write(address, body)
            self.ranges[address] = len(body)
        self.p = profile
        self.current = ACTOR_BASES[profile['currentSide']] + profile['currentSlot'] * 0x440
        self.policyGlobal = struct.unpack_from('<I', overlay, 0x021E29F4 - 0x021D7240)[0]
        self.moveGlobal = struct.unpack_from('<I', main, 0x7B000)[0]
        self.u.mem_write(self.moveGlobal + 4, pack([MOVES]))
        move = bytearray(40)
        struct.pack_into('<I', move, 0, profile['moveFlags'])
        struct.pack_into('<H', move, 4, profile['halfFlags'])
        struct.pack_into('<h', move, 6, profile['costField'])
        struct.pack_into('<H', move, 8, profile['moveNibbles'])
        struct.pack_into('<h', move, 10, profile['effect'])
        move[0x21] = profile['moveByte21']
        self.u.mem_write(MOVES + profile['moveId'] * 40, bytes(move))
        self.beforeActors = {}
        for side, base in enumerate(ACTOR_BASES):
            for index in range(3):
                pointer = base + index * 0x440
                ordinal = side * 3 + index
                descriptor = DESCRIPTORS + ordinal * 0x100
                actor = bytearray(0x440)
                actor[0x31C] = profile['enabled'][index]
                actor[0x1FF] = profile['markers'][index]
                actor[0x31E] = profile['lookupSide'] if pointer == self.current else side
                actor[0x31F] = index
                struct.pack_into('<I', actor, 0x1E8, descriptor)
                struct.pack_into('<h', actor, 0x1F2, profile['values'][index])
                struct.pack_into('<I', actor, 0x60, FRAME)
                for offset, value in zip(TRAITS, profile['traits']):
                    actor[offset] = value & 0xFF if pointer == self.current else 0
                self.u.mem_write(pointer, bytes(actor))
                self.u.mem_write(descriptor, bytes(0x100))
                self.u.mem_write(descriptor + 0xAC, bytes([profile['descriptorFlags'][index]]))
                self.beforeActors[pointer] = bytes(actor)
        context = bytearray([0xA5] * 0x90)
        context[0xF] = profile['phase']
        context[0xE] = 0x81
        context[0x23] = 0xFE
        context[0x15] = profile['selection'] & 0xFF
        context[0x35] = profile['special']
        context[0x1B] = 0x77
        context[6] = profile['priorToken']
        struct.pack_into('<I', context, 0x5C, 0xA5A55A5A)
        struct.pack_into('<H', context, 0x4E, 0x8123)
        struct.pack_into('<H', context, 0x50, profile['moveId'])
        struct.pack_into('<I', context, 0x84, self.current)
        self.beforeContext = bytes(context)
        self.u.mem_write(CONTEXT, bytes(context))
        self.u.mem_write(GATE, bytes([profile['gate']]))
        self.u.mem_write(self.policyGlobal + 0x10, bytes([profile['policy']]))
        self.u.mem_write(FRAME, pack([profile['frameWord']]))
        self.calls = []
        self.rawCalls = []
        self.nativeEntries = []
        self.completed = []
        self.pending = []
        self.physicalReturns = 0
        self.instructions = 0
        self.writes = []
        self.ownPcs = set()
        self.returned = False
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, unused):
        if not 0x02000000 <= address < address + size <= 0x02800000:
            raise ValueError(('822 outside RAM write', hex(address), size))
        if not 0x027E0000 <= address < 0x027F0100:
            self.writes.append((address, size, value))

    def provider(self, pc, args):
        p = self.p
        if pc == 0x021F1414:
            return p['selectedWord']
        if pc == 0x0205D790:
            return 0x02540020
        if pc == 0x021EEC7C:
            return p['tokenWord']
        if pc == 0x021D9534:
            if args[2] not in [6, 8]:
                raise ValueError('822 unsupported threshold selector')
            return p['threshold6' if args[2] == 6 else 'threshold8']
        if pc == 0x021DD02C:
            return p['allowedWord']
        if pc == 0x0207CE3C:
            return p['lowerCostWord']
        if pc == 0x021DBCF0:
            return p['maximumWord']
        return 0x94530000 + p['ordinal']

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 20000:
            raise ValueError('822 instruction bound')
        if self.pending and pc == self.pending[-1][1]:
            self.physicalReturns += 1
            target, lr = self.pending.pop()
            self.completed.append(dict(address=hex(target), rawR0=u.reg_read(REGS[0]), rawR1=u.reg_read(REGS[1]), actuallyReturned=True))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if ENTRY <= pc < ENTRY + 1524:
            self.ownPcs.add(pc)
        if pc in HELPERS:
            self.pending.append((pc, u.reg_read(UC_ARM_REG_LR)))
            self.nativeEntries.append(dict(address=hex(pc), incomingWords=[u.reg_read(reg) for reg in REGS[:4]]))
        if pc in PROVIDERS:
            words = [u.reg_read(reg) for reg in REGS[:4]]
            stack = list(struct.unpack('<4I', bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), 16))))
            args = (words + stack)[:PROVIDERS[pc]]
            result = self.provider(pc, args) & 0xFFFFFFFF
            self.calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=result))
            self.rawCalls.append(dict(target=hex(pc), registers=words, stackWords=stack))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(REGS[index], (0xCACE0000 + index * 0x101 + self.p['ordinal']) & 0xFFFFFFFF)
            cpsr = u.reg_read(UC_ARM_REG_CPSR)
            u.reg_write(UC_ARM_REG_CPSR, (cpsr & 0x0FFFFFFF) | ((self.p['ordinal'] & 15) << 28))
            u.reg_write(REGS[0], result)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        if not any(address <= pc < address + size for address, size in self.ranges.items()):
            raise ValueError(('822 unsupported native edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(UC_ARM_REG_CPSR, 0xD3)
        for index, reg in enumerate(REGS):
            u.reg_write(reg, 0x51510000 + index * 0x101)
        saved = [u.reg_read(reg) for reg in REGS[4:12]]
        u.reg_write(UC_ARM_REG_SP, SP)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.emu_start(entry, STOP + 4, count=20001)
        if not self.returned or self.pending or u.reg_read(UC_ARM_REG_SP) != SP:
            raise ValueError('822 missing proper top/native return')
        if [u.reg_read(reg) for reg in REGS[4:12]] != saved:
            raise ValueError('822 callee-saved corruption')
        return dict(registers=[u.reg_read(reg) for reg in REGS], cpsr=u.reg_read(UC_ARM_REG_CPSR), rawR0=u.reg_read(REGS[0]), actuallyReturned=True, calls=self.calls, rawCalls=self.rawCalls, nativeEntries=self.nativeEntries, nativeCompletions=self.completed, actualNativeReturnInstructions=self.physicalReturns, instructions=self.instructions, writes=self.writes, context=bytes(u.mem_read(CONTEXT, 0x90)), actors={pointer: bytes(u.mem_read(pointer, 0x440)) for pointer in self.beforeActors}, ownPcs=sorted(self.ownPcs), memory=bytes(u.mem_read(0x02000000, 0x00800000)))
