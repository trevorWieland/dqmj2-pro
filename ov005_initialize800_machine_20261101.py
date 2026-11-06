import hashlib
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR

REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
ENTRY = 0x021DA9E4
SP = 0x027F0000
STOP = 0x027FF000
CONTEXT = 0x021E9818
ROW_TABLE = 0x021E7134
VRAM = 0x06000000
OBJECTS = [0x021E9EA8, 0x021E9CF8, 0x021E9BD8, 0x021E9B48, 0x021E9AB8, 0x021E9A28]
OBJECTS += [base + index * 0x90 for index in range(3) for base in [0x021EA298, 0x021EA0E8, 0x021E9F38]]
PROVIDERS = {0x02002C98: 3, 0x0201D444: 2, 0x0203CC2C: 2, 0x0202A8E0: 1, 0x020481B8: 3, 0x02048308: 0, 0x0202A498: 2, 0x02004E58: 3, 0x02004CD8: 3, 0x02004B58: 3, 0x021DA824: 0, 0x021DDD60: 2, 0x021DA838: 1, 0x02048A9C: 2, 0x02048A94: 2, 0x02048A60: 3, 0x02048644: 3, 0x021DB09C: 3, 0x021DD834: 0, 0x021DB95C: 1, 0x021DDF24: 0}
FORMAT_ADDRESSES = [0x021E722C, 0x021E7240, 0x021E7254, 0x021E7268]


def word(u, address, value):
    u.mem_write(address, struct.pack('<I', value & 0xFFFFFFFF))


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_map(0x04000000, 0x1000)
        self.u.mem_map(VRAM, 0x80000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(0x021D7240, overlay)
        for address, body in images.items():
            self.u.mem_write(address, body)
        self.ranges = {ENTRY: 1720, 0x02008C58: 0x4C}
        self.ranges.update({address: len(body) for address, body in images.items()})
        self.p = profile
        self.instructions = 0
        self.pending = []
        self.nativeReturns = 0
        self.completed = []
        self.returned = False
        self.calls = []
        self.rawCalls = []
        self.writes = []
        self.vramNext = VRAM
        self.vramHash = hashlib.sha256()
        self.fillArguments = []
        self.u.mem_write(0x04000000, bytes([profile['mmioByte']]) * 0x1000)
        self.beforeMmio = bytes(self.u.mem_read(0x04000000, 0x1000))
        self.u.mem_write(VRAM, bytes([0xA5]) * 0x80000)
        self.u.mem_write(CONTEXT, bytes([0xA5]) * 0x100)
        word(self.u, CONTEXT + 0x54, 0x02510000 + profile['ordinal'] * 0x100)
        self.rows = [(profile['x'] + index * 32, profile['y'] + index, profile['x'] - index * 16, profile['y'] + 20 + index) for index in range(7)]
        self.u.mem_write(ROW_TABLE, b''.join(struct.pack('<4i', *row) for row in self.rows))
        self.formats = [self.string(address) for address in FORMAT_ADDRESSES]
        if any(b'%' in text or len(text) >= 32 for text in self.formats):
            raise ValueError('800 only fixed filenames below32 bytes supported')
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def string(self, address):
        body = bytes(self.u.mem_read(address, 64))
        end = body.find(b'\0')
        if end < 0:
            raise ValueError('800 bounded string lacks terminator')
        return body[:end]

    def write(self, u, access, address, size, value, unused):
        if VRAM <= address < VRAM + 0x80000:
            if address != self.vramNext or size != 4 or value != 0:
                raise ValueError(('800 unexpected native VRAM-shadow fill sequence', hex(address), size, value))
            self.vramHash.update(struct.pack('<III', address, size, value))
            self.vramNext += 4
        elif not 0x027E0000 <= address < 0x027F0100:
            self.writes.append((address, size, value))

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 200000:
            raise ValueError('800 instruction bound')
        if self.pending and pc == self.pending[-1]:
            self.pending.pop()
            self.nativeReturns += 1
            self.completed.append(dict(address='0x02008c58', rawR0=u.reg_read(REGS[0]), actuallyReturned=True))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if pc == 0x02008C58:
            arguments = [u.reg_read(reg) for reg in REGS[:3]]
            self.fillArguments.append(arguments)
            if not (arguments == [0, VRAM, 0x80000] or arguments[0] == 0 and arguments[1] in OBJECTS and arguments[2] == 4):
                raise ValueError(('800 unsupported actual fill arguments', arguments))
            self.pending.append(u.reg_read(UC_ARM_REG_LR))
        if pc in PROVIDERS:
            raw = [u.reg_read(reg) for reg in REGS[:4]]
            args = raw[:PROVIDERS[pc]]
            logical = args[:]
            result = 0
            if pc == 0x0201D444:
                text = self.string(args[1])
                if text not in self.formats:
                    raise ValueError('800 unexpected format input')
                u.mem_write(args[0], text + b'\0')
                logical = [text.hex()]
                result = len(text)
            elif pc in [0x0203CC2C, 0x0202A8E0]:
                text = self.string(args[0])
                if text not in self.formats:
                    raise ValueError('800 unexpected filename input')
                logical = [text.hex()] + args[1:]
                index = self.formats.index(text)
                result = 0x02520000 + index * 0x1000 if pc == 0x0203CC2C else 32 * (index + 1) + self.p['ordinal']
            elif pc == 0x021DA838:
                if args[0] not in OBJECTS:
                    raise ValueError('800 unsupported supplied constructor')
                u.mem_write(args[0], bytes([self.p['objectByte']]) * 0x90)
                word(u, args[0] + 0x7C, self.p['flags'])
            elif pc == 0x021DDF24:
                result = self.p['returnWord']
            self.calls.append(dict(target=hex(pc), callerPreparedView=logical, suppliedReturn=result))
            self.rawCalls.append(dict(target=hex(pc), registers=raw, stackWords=list(struct.unpack('<4I', bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), 16))))))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(REGS[index], (0xCACE0000 + index * 0x101 + self.p['ordinal']) & 0xFFFFFFFF)
            u.reg_write(REGS[0], result)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        if not any(address <= pc < address + size for address, size in self.ranges.items()):
            raise ValueError(('800 unsupported native edge', hex(pc)))

    def run(self, entry):
        u = self.u
        u.reg_write(UC_ARM_REG_CPSR, 0xD3)
        for index, reg in enumerate(REGS):
            u.reg_write(reg, 0x51510000 + index * 0x101)
        saved = [u.reg_read(reg) for reg in REGS[4:12]]
        u.reg_write(UC_ARM_REG_SP, SP)
        u.reg_write(UC_ARM_REG_LR, STOP)
        u.emu_start(entry, STOP + 4, count=200001)
        if not self.returned or self.pending or u.reg_read(UC_ARM_REG_SP) != SP:
            raise ValueError('800 improper top/native return')
        if [u.reg_read(reg) for reg in REGS[4:12]] != saved:
            raise ValueError('800 callee-saved corruption')
        if self.vramNext != VRAM + 0x80000:
            raise ValueError('800 incomplete ordered native VRAM-shadow fill')
        return dict(rawR0=u.reg_read(REGS[0]), actuallyReturned=True, calls=self.calls, rawCalls=self.rawCalls, writes=self.writes, nativeReturns=self.nativeReturns, nativeCompletions=self.completed, fillArguments=self.fillArguments, vramWrites=0x80000 // 4, vramWriteTraceSha256=self.vramHash.hexdigest(), instructions=self.instructions, memory=bytes(u.mem_read(0x02000000, 0x007E0000)) + bytes(u.mem_read(0x027F0100, 0xFF00)), mmio=bytes(u.mem_read(0x04000000, 0x1000)), vram=bytes(u.mem_read(VRAM, 0x80000)))


def model(vm, result):
    p = vm.p
    failures = []
    if result['rawR0'] != p['returnWord']:
        failures.append('physical R0')
    for index, address in enumerate(OBJECTS):
        expected = p['flags'] | 2 if index == 0 or index >= 6 else p['flags'] & 0xFFFFFFFD
        actual = struct.unpack('<I', bytes(vm.u.mem_read(address + 0x7C, 4)))[0]
        if actual != expected:
            failures.append('object flags ' + hex(address))
    if bytes(vm.u.mem_read(CONTEXT + 8, 1)) != b'\1' or bytes(vm.u.mem_read(CONTEXT + 0x50, 4)) != bytes(4):
        failures.append('controller raw fields')
    expectedTiles = []
    for x, y, otherX, otherY in vm.rows:
        expectedTiles += [[x + shift, y, 0x79] for shift in [0, 8, 16, 24]]
        expectedTiles += [[otherX + shift, otherY, tile] for shift, tile in [(0, 0x79), (8, 0x79), (40, 0x73), (24, 0x79), (32, 0x79)]]
    expectedTiles = [[word & 0xFFFFFFFF for word in row] for row in expectedTiles]
    actualTiles = [row['callerPreparedView'] for row in result['calls'] if row['target'] == '0x21db09c']
    if actualTiles != expectedTiles:
        failures.append('63 ordered row/tile calls')
    expectedMmio = bytearray(vm.beforeMmio)
    for offset, bits, priority in [(8, 0x4004, 2), (10, 0x4210, 1), (12, 0x404, 3), (14, 0x518, 0)]:
        before = struct.unpack_from('<H', expectedMmio, offset)[0]
        struct.pack_into('<H', expectedMmio, offset, ((before & 0x43) | bits) & 0xFFFC | priority)
    expectedMmio[16:32] = bytes(16)
    before = struct.unpack_from('<I', expectedMmio, 0)[0]
    struct.pack_into('<I', expectedMmio, 0, before | 0x1F00)
    if result['mmio'] != expectedMmio:
        failures.append('MMIO shadow')
    if result['vram'] != bytes(0x80000) or len(result['fillArguments']) != 16 or result['nativeReturns'] != 16:
        failures.append('actual native fills')
    return failures
