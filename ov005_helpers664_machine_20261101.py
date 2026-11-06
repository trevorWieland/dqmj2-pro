import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import *
BASE, OVERLAY, STACK, STOP, DATA = 0x02000000, 0x021D7240, 0x027F0000, 0x027FF800, 0x02610000
SIZES = {0x021E664C: 20, 0x021E6678: 140}
OPEN, CLOSE, NAME = 0x0203CC2C, 0x0203CF9C, 0x021E7894
REGS = c.REGISTERS[:13]


def inputs():
    module, image, unused = measured_module('ov005')
    if module['sha256'] != 'efd21cd223735980e3f83f95c796725b0abd677043c40ca26d9762e4ea9a97c8':
        raise ValueError('664 module differs')
    return dict(module=module, image=image)


class Machine:
    def __init__(self, original, profile, body=None):
        self.p, self.entry = profile, profile['entry']
        self.extent = len(body) if body is not None else SIZES[self.entry]
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE, 0x800000)
        self.u.mem_write(OVERLAY, original['image'])
        if body is not None:
            self.u.mem_write(self.entry, body)
        self.payload = bytes(profile['data'])
        self.u.mem_write(DATA, self.payload)
        self.initial = [0xA6640000 + index * 256 for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR, 0xA0000010)
        for register, value in zip(REGS, self.initial):
            self.u.reg_write(register, value)
        words = profile['words']
        for register, value in zip(REGS, words):
            self.u.reg_write(register, value & 0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP, STACK)
        self.u.reg_write(UC_ARM_REG_LR, STOP)
        self.before = bytes(self.u.mem_read(BASE, 0x800000))
        self.providers, self.reads, self.own, self.instructions = [], [], set(), 0
        self.u.hook_add(UC_HOOK_CODE, self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)
        self.u.hook_add(UC_HOOK_MEM_READ, self.read)

    def write(self, u, access, address, size, value, data):
        if not STACK - 65536 <= address < STACK + 256:
            raise ValueError(('664 unexpected nonstack write', hex(address), size))

    def read(self, u, access, address, size, value, data):
        if DATA <= address < DATA + 4096:
            if address + size > DATA + len(self.payload):
                raise ValueError('664 payload read outside supplied extent')
            self.reads.append([address - DATA, size, bytes(u.mem_read(address, size)).hex()])

    def observe(self, u, address, length, data):
        self.instructions += 1
        if self.entry <= address < self.entry + self.extent:
            self.own.add(address)
            return
        if address in (OPEN, CLOSE) and self.entry == 0x021E6678:
            words = [u.reg_read(register) for register in REGS[:4]]
            expected = [NAME, self.p['words'][2] & 0xFFFFFFFF] if address == OPEN else [self.p['words'][2] & 0xFFFFFFFF, DATA]
            if words[:2] != expected:
                raise ValueError(('664 service contract differs', hex(address), words[:2], expected))
            result = (DATA if self.p['opened'] else 0) if address == OPEN else 0xE664F00D
            self.providers.append(dict(entry=address, preparedWords=words[:2], rawRegisterWords=words, providedR0=result, ramEffects=[]))
            u.reg_write(UC_ARM_REG_R0, result)
            for register, index in zip([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12], [1, 2, 3, 12]):
                u.reg_write(register, 0xDE640000 | index)
            u.reg_write(UC_ARM_REG_CPSR, (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0x60000000)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))
            return
        raise ValueError(('664 PC outside own/provided scopes', hex(address)))

    def run(self):
        self.u.emu_start(self.entry, STOP, count=10000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(register) for register in REGS[4:12]] != self.initial[4:12]:
            raise ValueError('664 did not actually return preserving frame')
        result = dict(profile=self.p, coreRegistersAndCpsr=[self.u.reg_read(register) for register in REGS + [UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR]], providedCalls=self.providers, payloadReads=self.reads, ownObserved=sorted(self.own), instructions=self.instructions, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)))
        self.u = None
        gc.collect()
        return result
