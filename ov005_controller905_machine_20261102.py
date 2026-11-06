import struct
import match_runtime as C
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
ENTRY = 0x021D8900
DESCRIPTOR = 0x021D7480
OBJECT = 0x02510000
CONTROLLER = OBJECT + 0x5760
REQUEST = 0x02520000
METHODS = 0x02530000
CALLBACK = 0x0260F000
SELECT = 0x0260F200
SP = 0x027F0000
STOP = 0x026FF000
GLOBAL = 0x021E78CC
REGS = C.REGISTERS

def pack(values):
    return struct.pack('<' + 'I' * len(values), *[v & 0xFFFFFFFF for v in values])

class Machine:
    def __init__(self, main, overlay, images, profile):
        self.p = profile
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(0x021D7240, overlay)
        self.ranges = {ENTRY: 1500, DESCRIPTOR: 196}
        for address, body in images.items():
            self.u.mem_write(address, body)
            self.ranges[address] = len(body)
        self.u.mem_write(GLOBAL, pack([OBJECT, 3]))
        self.u.mem_write(OBJECT + 4, pack([CALLBACK]))
        self.request = REQUEST + profile['requestOffset']
        self.u.mem_write(self.request + 0x44, pack([profile['key']]))
        self.entries = [CONTROLLER + 0x24 + i * 0x30 for i in range(16)]
        for i, key in enumerate(profile['rowKeys']):
            self.u.mem_write(self.entries[i] + 4, pack([key]))
            self.u.mem_write(self.entries[i] + 0xC, pack([METHODS]))
        self.u.mem_write(CONTROLLER + 0x20, pack([self.entries[15]]))
        self.u.mem_write(CONTROLLER + 0x324, pack([0xABCD7890]))
        self.u.mem_write(METHODS + 8, pack([SELECT]))
        self.u.mem_write(OBJECT + 0xE8, pack([0xAABBCCDD]))
        for address in [CALLBACK, SELECT]:
            self.u.mem_write(address, bytes.fromhex('1eff2fe1'))
        self.beforeObject = bytes(self.u.mem_read(OBJECT, 0x6000))
        self.frames = []
        self.calls = []
        self.nativeEntries = []
        self.nativeReturns = []
        self.writes = []
        self.pcs = set()
        self.previous = None
        self.steps = 0
        self.privateStackStart = SP
        self.decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def words(self, address, count):
        return list(struct.unpack('<' + 'I' * count, self.u.mem_read(address, count * 4)))

    def write(self, u, access, address, size, value, unused):
        if not SP - 0x1000 <= address < SP:
            self.writes.append([address, size, value & ((1 << (size * 8)) - 1)])

    def provider(self, pc):
        args = [self.u.reg_read(r) for r in REGS[:2]]
        if pc == SELECT:
            if args != [CONTROLLER, self.request]:
                raise ValueError(('905 select ABI', args))
            event = dict(target=hex(pc), consumedWords=args, returnWord=self.p['selectReturn'])
        else:
            if args[0] != 6 or not SP - 0x1000 <= args[1] <= SP - 8:
                raise ValueError(('905 callback ABI', args))
            before = self.words(args[1], 2)
            if self.p['override'] is not None:
                self.u.mem_write(args[1], pack([self.p['override']]))
            event = dict(target=hex(pc), eventWord=args[0], payloadBefore=before, payloadAfter=self.words(args[1], 2), rawPayloadAddress=args[1], returnWord=0x12345678)
        self.calls.append(event)
        for i in [0, 1, 2, 3, 12]:
            self.u.reg_write(REGS[i], (0xC0DE1000 + len(self.calls) * 0x100 + i * 17) & 0xFFFFFFFF)
        self.u.reg_write(REGS[0], event['returnWord'])
        flags = self.u.reg_read(UC_ARM_REG_CPSR)
        self.u.reg_write(UC_ARM_REG_CPSR, (flags & 0x0FFFFFFF) | ((self.p['ordinal'] & 15) << 28))
        self.u.reg_write(UC_ARM_REG_PC, self.u.reg_read(REGS[14]) & ~1)

    def code(self, u, pc, size, unused):
        self.steps += 1
        if self.steps > 50000:
            raise ValueError('905 instruction bound')
        self.privateStackStart = min(self.privateStackStart, u.reg_read(REGS[13]))
        if self.frames and pc == self.frames[-1]['lr']:
            frame = self.frames.pop()
            instruction = next(self.decoder.disasm(bytes(u.mem_read(self.previous, 4)), self.previous))
            if not (DESCRIPTOR <= self.previous < DESCRIPTOR + 196 and instruction.mnemonic.startswith('pop') and 'pc' in instruction.op_str):
                raise ValueError(('905 native return instruction', instruction.mnemonic, instruction.op_str))
            if u.reg_read(REGS[13]) != frame['sp'] or [u.reg_read(r)for r in REGS[4:12]] != frame['saved']:
                raise ValueError('905 native return frame differs')
            self.nativeReturns.append(dict(entry=hex(DESCRIPTOR), returnPc=hex(self.previous), returnInstruction=instruction.mnemonic + ' ' + instruction.op_str, actualReturnWord=u.reg_read(REGS[0])))
        if pc == STOP:
            self.returnPc = self.previous
            u.emu_stop()
            return
        if pc in [CALLBACK, SELECT]:
            self.provider(pc)
            return
        if pc == DESCRIPTOR:
            words = [u.reg_read(r)for r in REGS[:2]]
            self.nativeEntries.append(dict(entry=hex(pc), callerWords=words, callerReturnPc=hex(u.reg_read(REGS[14]))))
            self.frames.append(dict(lr=u.reg_read(REGS[14]) & ~1, sp=u.reg_read(REGS[13]), saved=[u.reg_read(r)for r in REGS[4:12]]))
        if not any(start <= pc < start + length for start, length in self.ranges.items()):
            raise ValueError(('905 unexpected native PC', hex(pc)))
        if ENTRY <= pc < ENTRY + 1500:
            self.pcs.add(pc)
        self.previous = pc

    def run(self, entry):
        self.u.reg_write(UC_ARM_REG_CPSR, 0xD3)
        for i, reg in enumerate(REGS[:13]):
            self.u.reg_write(reg, 0x11110000 + i * 0x101)
        self.u.reg_write(REGS[0], 6)
        self.u.reg_write(REGS[1], self.request)
        self.u.reg_write(REGS[13], SP)
        self.u.reg_write(REGS[14], STOP)
        self.initial = [self.u.reg_read(r)for r in REGS]
        self.u.emu_start(entry, STOP + 4, count=50000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.frames:
            raise ValueError('905 actual top return absent')
        if self.u.reg_read(REGS[13]) != SP or [self.u.reg_read(r)for r in REGS[4:12]] != self.initial[4:12]:
            raise ValueError('905 top callee-saved frame differs')
        instruction = next(self.decoder.disasm(bytes(self.u.mem_read(self.returnPc, 4)), self.returnPc))
        if not instruction.mnemonic.startswith('pop') or 'pc' not in instruction.op_str:
            raise ValueError('905 top proper return instruction absent')
        return dict(registers=[self.u.reg_read(r)for r in REGS[:13]], cpsr=self.u.reg_read(UC_ARM_REG_CPSR), memory=bytes(self.u.mem_read(0x02000000,0x800000)), objectHex=bytes(self.u.mem_read(OBJECT,0x6000)).hex(), calls=self.calls, writes=self.writes, nativeHelperEntries=self.nativeEntries, nativeHelperPhysicalReturns=self.nativeReturns, privateStackStart=self.privateStackStart, ownPcs=sorted(self.pcs), actualTopReturnPc=hex(self.returnPc), steps=self.steps)
