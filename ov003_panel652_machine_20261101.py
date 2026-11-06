import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE, OVERLAY, ENTRY, SIZE = 0x02000000, 0x021D7240, 0x021DF6AC, 388
STACK, STOP, CONTEXT, SLOTS = 0x027F0000, 0x027FF800, 0x02610000, 0x02102A18
RESOURCES, METADATA, MAPDATA, DESCRIPTORS = 0x02620000, 0x02630000, 0x021E03D7, 0x021E0A9C
COORDINATES = [0x021E0A6C, 0x021E0A70, 0x021E0A68]
GETTER, MAPPER, CONSTRUCTOR = 0x02049AD0, 0x021DE71C, 0x02049008
CLEANUPS, LOW = [0x020851D4, 0x02085200], 0x0208522C
PROVIDERS = [0x0206B324, 0x0206006C, 0x02045DC4, LOW]
NATIVE = {GETTER: 20, MAPPER: 76, CONSTRUCTOR: 296, 0x02048F5C: 16, CLEANUPS[0]: 44, CLEANUPS[1]: 44}
REGS = c.REGISTERS[:13]


def inputs():
    main, arm, unused = measured_module('main')
    module, overlay, unused = measured_module('ov003')
    if main['sha256'] != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f' or module['sha256'] != 'efbcc417d3e4b22c11f87bb58ee9fbbf3df4b12c285122d322eb3f9257607260':
        raise ValueError('652 measured images differ')
    return dict(main=main, arm=arm, module=module, overlay=overlay, mapping=overlay[MAPDATA - OVERLAY:MAPDATA - OVERLAY + 63])


class Machine:
    def __init__(self, original, profile, body=None):
        self.p, self.extent = profile, len(body) if body is not None else SIZE
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE, 0x800000)
        self.u.mem_write(BASE, original['arm'])
        self.u.mem_write(OVERLAY, original['overlay'])
        if body is not None:
            self.u.mem_write(ENTRY, body)
        self.frames, self.returns, self.providers, self.writes = [], [], [], []
        self.own, self.native, self.instructions = set(), set(), 0
        self.u.mem_write(CONTEXT, bytes(32))
        self.u.mem_write(CONTEXT + 0x10, bytes([profile['mode']]))
        self.u.mem_write(SLOTS, b'\xA5' * 432)
        for index, slot in enumerate(profile['slots']):
            address, resource, metadata = SLOTS + 12 * index, RESOURCES + 16 * index, METADATA + 128 * index
            self.word(address, resource if slot['present'] else 0)
            self.u.mem_write(address + 5, bytes([slot['tag']]))
            self.u.mem_write(resource, b'\xCC' * 16)
            self.word(resource + 4, metadata)
            self.u.mem_write(metadata, b'\xA7' * 128)
            self.word(metadata + 0x18, slot['flags'])
            self.u.mem_write(metadata + 0x5C, bytes(slot['coordinates']))
        for address, values in zip(COORDINATES, profile['firstCoordinates']):
            self.u.mem_write(address, bytes(values))
        self.initial = [0xA6520000 + (index << 8) for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR, 0x10)
        for register, value in zip(REGS, self.initial):
            self.u.reg_write(register, value)
        self.u.reg_write(UC_ARM_REG_R0, CONTEXT)
        self.u.reg_write(UC_ARM_REG_SP, STACK)
        self.u.reg_write(UC_ARM_REG_LR, STOP)
        self.before = bytes(self.u.mem_read(BASE, 0x800000))
        self.u.hook_add(UC_HOOK_CODE, self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def word(self, address, value):
        self.u.mem_write(address, struct.pack('<I', value & 0xFFFFFFFF))

    def write(self, u, access, address, size, value, data):
        if STACK - 65536 <= address < STACK + 256:
            return
        if size != 1 or not SLOTS <= address < SLOTS + 432 or (address - SLOTS) % 12 != 5:
            raise ValueError(('652 unexpected nonstack effect', hex(address), size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC), address, size, value & 255])

    def observe(self, u, address, length, data):
        self.instructions += 1
        while self.frames and address == self.frames[-1]['lr'] and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(register) for register in REGS[4:12]] != frame['preserved'] or u.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('652 native helper frame differs')
            self.returns.append(dict(entry=frame['entry'], preparedWords=frame['words'], returnedWords=[u.reg_read(register) for register in REGS[:4]]))
        if ENTRY <= address < ENTRY + self.extent:
            self.own.add(address)
            return
        if address in PROVIDERS:
            words = [u.reg_read(register) for register in REGS[:4]]
            arity = {0x0206B324: 1, 0x0206006C: 5, 0x02045DC4: 6, LOW: 2}[address]
            prepared = words[:min(4, arity)]
            if arity > 4:
                prepared += list(struct.unpack('<' + 'I' * (arity - 4), bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), (arity - 4) * 4))))
            value = 0xE6520000 | (address & 0xFFFF)
            self.providers.append(dict(entry=address, preparedWords=prepared, rawRegisterWords=words, providedR0=value, ramEffects=[]))
            u.reg_write(UC_ARM_REG_R0, value)
            for register, index in zip([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12], [1, 2, 3, 12]):
                u.reg_write(register, 0xDE520000 | index)
            u.reg_write(UC_ARM_REG_CPSR, (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0xA0000000)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        if address in NATIVE:
            words = [u.reg_read(register) for register in REGS[:4]]
            if address == CONSTRUCTOR:
                words.append(int.from_bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), 4), 'little'))
            self.frames.append(dict(entry=address, lr=u.reg_read(UC_ARM_REG_LR), sp=u.reg_read(UC_ARM_REG_SP), words=words, preserved=[u.reg_read(register) for register in REGS[4:12]]))
        if any(entry <= address < entry + size for entry, size in NATIVE.items()):
            self.native.add(address)
            return
        raise ValueError(('652 PC outside own/native/provided scopes', hex(address)))

    def run(self):
        self.u.emu_start(ENTRY, STOP, count=100000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(register) for register in REGS[4:12]] != self.initial[4:12] or self.frames:
            raise ValueError('652 top did not actually return preserving frame')
        result = dict(profile=self.p, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), coreRegistersAndCpsr=[self.u.reg_read(register) for register in REGS + [UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR]], nativeReturns=self.returns, providedCalls=self.providers, nonstackWrites=self.writes, ownObserved=sorted(self.own), nativeObserved=sorted(self.native), instructions=self.instructions)
        self.u = None
        gc.collect()
        return result
