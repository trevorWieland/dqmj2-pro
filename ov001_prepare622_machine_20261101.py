import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE, OVERLAY, ENTRY, SIZE = 0x02000000, 0x021D7240, 0x0222CD84, 308
STACK, STOP, ROWS, IDS = 0x027F0000, 0x027FF800, 0x022498FC, 0x02249830
MODE, META, RNGSTATE = 0x02249828, 0x02610000, 0x020F6044
INITIALIZER, LOOKUP, RNG, UDIV = 0x02044FF4, 0x020449D4, 0x0203D294, 0x02026350
REGS = c.REGISTERS[:13]
NATIVE = {RNG: 72, UDIV: 484}


def inputs():
    main, arm, unused = measured_module('main')
    module, overlay, unused = measured_module('ov001')
    if main['sha256'] != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f' or module['sha256'] != '39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92':
        raise ValueError('622 measured image identity differs')
    return dict(main=main, arm=arm, module=module, overlay=overlay)


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
        self.u.mem_write(ROWS, b'\xCC' * 396)
        for index in range(3):
            self.word(IDS + index * 4, (profile['id'] + index * 0x10001) & 0xFFFFFFFF)
        self.word(IDS + profile['row'] * 4, profile['id'])
        self.u.mem_write(MODE, bytes([profile['mode']]))
        self.u.mem_write(META, b'\xA5' * 128)
        self.u.mem_write(META + 4, struct.pack('<H', profile['header']))
        self.word(RNGSTATE, profile['seed'])
        self.initial = [0xA6220000 + (index << 8) for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR, 0x10)
        for register, value in zip(REGS, self.initial):
            self.u.reg_write(register, value)
        self.u.reg_write(UC_ARM_REG_R0, profile['row'])
        self.u.reg_write(UC_ARM_REG_SP, STACK)
        self.u.reg_write(UC_ARM_REG_LR, STOP)
        self.before = bytes(self.u.mem_read(BASE, 0x800000))
        self.u.hook_add(UC_HOOK_CODE, self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def word(self, address, value):
        self.u.mem_write(address, struct.pack('<I', value & 0xFFFFFFFF))

    def write(self, u, access, address, size, value, data):
        if not STACK - 65536 <= address < STACK + 4096:
            self.writes.append([u.reg_read(UC_ARM_REG_PC), address, size, value & ((1 << (size * 8)) - 1)])

    def observe(self, u, address, length, data):
        self.instructions += 1
        while self.frames and address == self.frames[-1]['lr'] and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(register) for register in REGS[4:12]] != frame['preserved'] or u.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('622 native dependency return frame differs')
            self.returns.append(dict(entry=frame['entry'], preparedWords=frame['words'], returnedWords=[u.reg_read(register) for register in REGS[:4]]))
        if ENTRY <= address < ENTRY + self.extent:
            self.own.add(address)
            return
        if address in [INITIALIZER, LOOKUP]:
            words = [u.reg_read(register) for register in REGS[:4]]
            value = META if address == LOOKUP else 0xE6220001
            self.providers.append(dict(entry=address, preparedWords=words[:1 if address == LOOKUP else 3], rawRegisterWords=words, providedR0=value, ramEffects=[]))
            u.reg_write(UC_ARM_REG_R0, value)
            for register, index in zip([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12], [1, 2, 3, 12]):
                u.reg_write(register, 0xDE220000 | index)
            u.reg_write(UC_ARM_REG_CPSR, (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0xA0000000)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        if address in NATIVE:
            self.frames.append(dict(entry=address, lr=u.reg_read(UC_ARM_REG_LR), sp=u.reg_read(UC_ARM_REG_SP), preserved=[u.reg_read(register) for register in REGS[4:12]], words=[u.reg_read(register) for register in REGS[:4]]))
        if any(entry <= address < entry + size for entry, size in NATIVE.items()):
            self.native.add(address)
            return
        raise ValueError(('622 PC outside own/native/provided scopes', hex(address)))

    def run(self):
        self.u.emu_start(ENTRY, STOP, count=10000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(register) for register in REGS[4:12]] != self.initial[4:12] or self.frames:
            raise ValueError('622 top did not actually return preserving frame')
        result = dict(profile=self.p, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), coreRegistersAndCpsr=[self.u.reg_read(register) for register in REGS + [UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR]], nativeReturns=self.returns, providedCalls=self.providers, nonstackWrites=self.writes, ownObserved=sorted(self.own), nativeObserved=sorted(self.native), instructions=self.instructions)
        self.u = None
        gc.collect()
        return result
