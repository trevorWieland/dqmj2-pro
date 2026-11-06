import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946
import ov001_action822_machine_20261102 as R

ENTRY = 0x021DBC18
SP = 0x027F0000
STOP = 0x027FF000
MESH = 0x02500000
RECORD = MESH + 0x100
POINT = 0x02520000
CONTEXT = 0x02521000
OUTPUT = 0x02522000
PROVIDERS = {0x0200235C: 2, 0x021DBBB8: 2, 0x021DA57C: 4}


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
        self.u.mem_write(0x021D7240, overlay)
        self.ranges = {ENTRY: 1884}
        for address, body in images.items():
            self.u.mem_write(address, body)
            self.ranges[address] = len(body)
        self.u.mem_write(0x0223142C + 0x79C, pack([MESH]))
        mesh = bytearray(0x200)
        struct.pack_into('<I', mesh, 0xC, 0x100)
        vertices = [(-8192, 0, -8192), (8192, 0, -8192), (0, 0, 8192)]
        if profile['reverse']:
            vertices[1], vertices[2] = vertices[2], vertices[1]
        words = [0, profile.get('normalMagnitude', 4096) if profile['reverse'] else -profile.get('normalMagnitude', 4096), 0]
        if profile['zeroNormal']:
            words[1] = 0
        words += [value for vertex in vertices for value in vertex]
        mesh[0x100:0x100 + 48] = pack(words)
        mesh[0x100 + 0x42] = profile['flag']
        self.beforeMesh = bytes(mesh)
        self.u.mem_write(MESH, self.beforeMesh)
        self.u.mem_write(POINT, pack(profile['point']))
        context = bytearray(0x20)
        context[0x11] = profile['count'] & 255
        self.beforeContext = bytes(context)
        self.u.mem_write(CONTEXT, self.beforeContext)
        self.beforeOutput = pack([0xA5A51234, 0x76543210, 0x87654321])
        self.u.mem_write(OUTPUT, self.beforeOutput)
        self.calls = []
        self.callSites = []
        self.writes = []
        self.instructions = 0
        self.ownPcs = set()
        self.returned = False
        self.minSp = SP
        self.lastProviderAttempt = None
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, unused):
        if not 0x02000000 <= address < address + size <= 0x02800000:
            raise ValueError(('872 outside RAM write', hex(address), size))
        if not SP - 0x1000 <= address < SP:
            self.writes.append((address, size, value))

    def provider(self, address, args):
        if address == 0x0200235C:
            numerator, denominator = signed(args[0]) * 0x100000000, signed(args[1])
            if not denominator:
                raise ValueError('872 unsupported zero divisor')
            quotient = abs(numerator) // abs(denominator)
            if (numerator < 0) != (denominator < 0):
                quotient = -quotient
            return word(((quotient & 0xFFFFFFFFFFFFFFFF) + 0x80000) >> 20)
        return 0xA5000000 + self.p['ordinal']

    def code(self, u, pc, width, unused):
        self.instructions += 1
        self.minSp = min(self.minSp, u.reg_read(R.UC_ARM_REG_SP))
        if self.instructions > 20000:
            raise ValueError('872 instruction bound')
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if ENTRY <= pc < ENTRY + 1884:
            self.ownPcs.add(pc)
        if pc in PROVIDERS:
            args = [u.reg_read(reg) for reg in R.REGS[:PROVIDERS[pc]]]
            self.lastProviderAttempt = dict(target=hex(pc), callerWords=args)
            self.callSites.append(dict(target=hex(pc), callerReturnPc=hex(u.reg_read(R.UC_ARM_REG_LR))))
            result = self.provider(pc, args)
            self.calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=word(result)))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(R.REGS[index], 0xF0F00000 + index * 257 + self.p['ordinal'])
            flags = u.reg_read(R.UC_ARM_REG_CPSR)
            u.reg_write(R.UC_ARM_REG_CPSR, (flags & 0x0FFFFFFF) | ((self.p['ordinal'] & 15) << 28))
            u.reg_write(R.REGS[0], word(result))
            u.reg_write(R.UC_ARM_REG_PC, u.reg_read(R.UC_ARM_REG_LR))
            return
        if not any(address <= pc < address + size for address, size in self.ranges.items()):
            raise ValueError(('872 unsupported native edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
        for index, reg in enumerate(R.REGS):
            u.reg_write(reg, 0x81810000 + index * 257)
        saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
        for reg, value in zip(R.REGS[:4], [POINT, CONTEXT, 0 if self.p['nullOutput'] else OUTPUT, 0]):
            u.reg_write(reg, value)
        u.reg_write(R.UC_ARM_REG_SP, SP)
        u.reg_write(R.UC_ARM_REG_LR, STOP)
        u.mem_write(SP, pack([self.p['mask']]))
        u.emu_start(entry, STOP + 4, count=20001)
        if not self.returned or u.reg_read(R.UC_ARM_REG_SP) != SP or [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
            raise ValueError('872 proper return/SP/callee-saved ABI missing')
        return dict(registers=[u.reg_read(reg) for reg in R.REGS], cpsr=u.reg_read(R.UC_ARM_REG_CPSR), actuallyReturned=True, outputHex=bytes(u.mem_read(OUTPUT, 12)).hex(), meshHex=bytes(u.mem_read(MESH, 0x200)).hex(), contextHex=bytes(u.mem_read(CONTEXT, 0x20)).hex(), calls=self.calls, callSites=self.callSites, writes=self.writes, instructions=self.instructions, ownPcs=sorted(self.ownPcs), privateStackStart=self.minSp, memory=bytes(u.mem_read(0x02000000, 0x00800000)))


def profiles():
    output = []
    for x, z in [(0, 0), (4096, 0), (-4096, 0), (0, 4096), (32768, 0), (0, 32768)]:
        for reverse in [False, True]:
            n = len(output)
            output.append(dict(ordinal=n, point=(x, 0, z), reverse=reverse, zeroNormal=False, flag=1, mask=1, count=1, nullOutput=False))
    return output
