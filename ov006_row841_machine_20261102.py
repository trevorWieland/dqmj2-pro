import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946
import ov001_action822_machine_20261102 as R

ENTRY = 0x021DBE64
STATE = 0x0220F3B8
ROWS = 0x021BCC0C
SP = 0x027F0000
STOP = 0x027FF000
HELPERS = {0x02063EEC: 12, 0x02067D54: 128}
PROVIDERS = {0x021D7E34: 0, 0x02067BD4: 1, 0x02048094: 2, 0x021D79E4: 4, 0x02046AF4: 6, 0x021D7AD0: 2, 0x020643FC: 1, 0x021D7EBC: 3, 0x021DE1A8: 1, 0x021DE228: 1, 0x02067B48: 2, 0x021DC08C: 3}


def pack(words):
    return struct.pack('<' + 'I' * len(words), *[word & 0xFFFFFFFF for word in words])


def signed(word):
    word &= 0xFFFFFFFF
    return word - 0x100000000 if word & 0x80000000 else word


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(0x021D7240, overlay)
        if struct.unpack_from('<I', main, 0x63EF4)[0] != ROWS:
            raise ValueError('841 actual fixed getter differs')
        self.p = profile
        self.ranges = dict(HELPERS)
        self.ranges[ENTRY] = 532
        for address, body in images.items():
            self.u.mem_write(address, body)
            self.ranges[address] = len(body)
        self.u.mem_write(STATE, bytes(32))
        self.u.mem_write(STATE + 0x14, pack([profile['index']]))
        self.u.mem_write(ROWS, bytes(8 * 48 + 32))
        self.row = ROWS + profile['index'] * 48
        self.u.mem_write(self.row + 0x2C, pack([profile['word2C']]))
        self.u.mem_write(self.row + 0x30, pack([profile['word30']]))
        self.u.mem_write(self.row + 0x34, pack([profile['word34']]))
        self.u.mem_write(self.row + 0x3E, struct.pack('<H', profile['half3E']))
        self.before = bytes(self.u.mem_read(ROWS, 8 * 48 + 32))
        self.buffer = bytes((profile['ordinal'] * 17 + index * 29) & 255 for index in range(64))
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
            raise ValueError(('841 outside RAM write', hex(address), size))
        if not 0x027E0000 <= address < 0x027F0100:
            self.writes.append((address, size, value))

    def provider(self, pc, args):
        if pc == 0x021DE1A8:
            return self.p['quantityWord']
        if pc == 0x020643FC:
            return self.p['lookupWord']
        if pc == 0x02067B48:
            return self.p['valueWord']
        if pc == 0x021DC08C:
            return self.p['returnWord'] if args[0] == 14 else self.p['priorReturnWord']
        return 0x98AB0000 + self.p['ordinal']

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 10000:
            raise ValueError('841 instruction bound')
        if self.pending and pc == self.pending[-1][1]:
            self.actualReturns += 1
            address, lr = self.pending.pop()
            self.completed.append(dict(address=hex(address), rawR0=u.reg_read(R.REGS[0]), rawR1=u.reg_read(R.REGS[1]), actuallyReturned=True))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if ENTRY <= pc < ENTRY + 524:
            self.ownPcs.add(pc)
        if pc in HELPERS:
            self.pending.append((pc, u.reg_read(R.UC_ARM_REG_LR)))
            self.nativeEntries.append(dict(address=hex(pc), rawWords=[u.reg_read(reg) for reg in R.REGS[:4]]))
        if pc in PROVIDERS:
            words = [u.reg_read(reg) for reg in R.REGS[:4]]
            stack = list(struct.unpack('<4I', bytes(u.mem_read(u.reg_read(R.UC_ARM_REG_SP), 16))))
            args = (words + stack)[:PROVIDERS[pc]]
            extra = {}
            if pc == 0x02046AF4:
                if args[4] < SP - 128 or args[4] + 64 > SP:
                    raise ValueError('841 supplied producer outside reserved stack object')
                u.mem_write(args[4], self.buffer)
                extra['suppliedOutputHex'] = self.buffer.hex()
            if pc == 0x021D7AD0:
                extra['observed64ByteBufferHex'] = bytes(u.mem_read(args[1], 64)).hex()
            result = self.provider(pc, args) & 0xFFFFFFFF
            self.calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=result, **extra))
            self.rawCalls.append(dict(target=hex(pc), registers=words, stackWords=stack))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(R.REGS[index], (0xFACE0000 + index * 0x101 + self.p['ordinal']) & 0xFFFFFFFF)
            cpsr = u.reg_read(R.UC_ARM_REG_CPSR)
            u.reg_write(R.UC_ARM_REG_CPSR, (cpsr & 0x0FFFFFFF) | ((self.p['ordinal'] & 15) << 28))
            u.reg_write(R.REGS[0], result)
            u.reg_write(R.UC_ARM_REG_PC, u.reg_read(R.UC_ARM_REG_LR))
            return
        if not any(address <= pc < address + count for address, count in self.ranges.items()):
            raise ValueError(('841 unsupported native edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
        for index, register in enumerate(R.REGS):
            u.reg_write(register, 0x81810000 + index * 0x101)
        saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
        u.reg_write(R.UC_ARM_REG_SP, SP)
        u.reg_write(R.UC_ARM_REG_LR, STOP)
        u.emu_start(entry, STOP + 4, count=10001)
        if not self.returned or self.pending or u.reg_read(R.UC_ARM_REG_SP) != SP:
            raise ValueError('841 proper top/helper return missing')
        if [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
            raise ValueError('841 callee-saved registers differ')
        return dict(registers=[u.reg_read(reg) for reg in R.REGS], cpsr=u.reg_read(R.UC_ARM_REG_CPSR), actuallyReturned=True, calls=self.calls, rawCalls=self.rawCalls, nativeEntries=self.nativeEntries, nativeCompletions=self.completed, actualNativeReturnInstructions=self.actualReturns, instructions=self.instructions, writes=self.writes, ownPcs=sorted(self.ownPcs), rows=bytes(u.mem_read(ROWS, 8 * 48 + 32)), state=bytes(u.mem_read(STATE, 32)), memory=bytes(u.mem_read(0x02000000, 0x00800000)))
