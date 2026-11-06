import gc
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE, OVERLAY, ENTRY, SIZE = 0x02000000, 0x021D7240, 0x021DD5CC, 1092
STACK, STOP, INFO, RECORD = 0x027F0000, 0x027FF800, 0x021B9EA8, 0x02610000
ABILITY, CURVE, POINTS = 0x02620000, 0x02630004, 0x02640000
CONTEXT, RNGSTATE, UID = 0x0220F4E8, 0x020F6044, 0xD6100042
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
        UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
        UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11,
        UC_ARM_REG_R12]
NATIVE = {0x020642F8: 12, 0x02008D78: 148, 0x0203D294: 72,
          0x02026350: 484, 0x02062E44: 136, 0x02063038: 24,
          0x021DD3A8: 24, 0x021DD420: 20, 0x021DD434: 140,
          0x021DD4C0: 24, 0x021DD4D8: 24, 0x021DD4F0: 140,
          0x021DD57C: 80, 0x021DDF58: 20}
BASE_GETTERS = [0x02044E34, 0x02044E70, 0x02044EAC, 0x02044EE8,
                0x02044F24, 0x02044F60]
CAP_GETTERS = [0x02044E44, 0x02044E80, 0x02044EBC, 0x02044EF8,
               0x02044F34, 0x02044F70]
CALLBACKS = [0x02044A14, 0x02044A58, 0x02044A9C, 0x02044AE0,
             0x02044B24, 0x02044B68]
PROVIDERS = [0x021D83C8, 0x021DA654, 0x021D83E4, 0x0206271C,
             0x02062A10, 0x021DD3C0, 0x02044CDC, 0x0203CC2C,
             0x0203CF9C, 0x0202A498, 0x0207AEBC] + BASE_GETTERS + CAP_GETTERS + CALLBACKS


def inputs():
    main, arm, unused = measured_module('main')
    module, overlay, unused = measured_module('ov006')
    if main['sha256'] != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f' or module['sha256'] != 'fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341':
        raise ValueError('610 measured image identity differs')
    return dict(main=main, arm=arm, module=module, overlay=overlay)


def ability_bytes():
    return bytes((index * 37 + index // 11 + 3) & 255 for index in range(1024))


def point_bytes():
    return bytes((index * 13 + 7) % 251 for index in range(256))


def curve_words():
    return [((index + 3) * 0x10203 + 0x81700000) & 0xFFFFFFFF for index in range(257)]


class Machine:
    def __init__(self, original, profile, body=None):
        self.p = profile
        self.extent = len(body) if body is not None else SIZE
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE, 0x800000)
        self.u.mem_write(BASE, original['arm'])
        self.u.mem_write(OVERLAY, original['overlay'])
        if body is not None:
            self.u.mem_write(ENTRY, body)
        self.frames, self.returns, self.events, self.writes = [], [], [], []
        self.own, self.native, self.instructions = set(), set(), 0
        self.u.mem_write(INFO, b'\xA5' * 32)
        self.u.mem_write(INFO + 2, struct.pack('<h', profile['species']))
        self.u.mem_write(INFO + 5, bytes([profile['level'], profile['variant']] + profile['rawFive']))
        self.u.mem_write(RECORD, b'\xCC' * 256)
        self.u.mem_write(RECORD + 0x18, struct.pack('<hB', profile['species'], profile['variant']))
        self.u.mem_write(CONTEXT, b'\xA7' * 32)
        self.u.mem_write(ABILITY, ability_bytes())
        self.u.mem_write(POINTS, point_bytes())
        self.u.mem_write(CURVE - 4, struct.pack('<257I', *curve_words()))
        self.word(RNGSTATE, profile['seed'])
        self.initial = [0xA6100000 + (index << 8) for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR, 0x10)
        for register, value in zip(REGS, self.initial):
            self.u.reg_write(register, value)
        self.u.reg_write(UC_ARM_REG_R0, profile['argument'])
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

    def provide(self, address):
        u, p = self.u, self.p
        words = [u.reg_read(register) for register in REGS[:4]]
        arity = 0
        value = 0xE6100000 | (address & 0xFFFF)
        if address == 0x0206271C:
            arity, value = 2, UID
        elif address == 0x02062A10:
            arity, value = 1, RECORD
        elif address == 0x021DD3C0:
            arity, value = 3, CURVE if p['curvePresent'] else 0
        elif address == 0x02044CDC:
            arity, value = 1, p['category']
        elif address in BASE_GETTERS:
            arity, value = 2, p['bases'][BASE_GETTERS.index(address)]
        elif address in CAP_GETTERS:
            arity, value = 6, p['caps'][CAP_GETTERS.index(address)]
        elif address in CALLBACKS:
            arity = 3
            value = (CALLBACKS.index(address) + words[2] + p['callbackSalt']) % 3
        elif address == 0x0203CC2C:
            arity = 2
            path = bytes(u.mem_read(words[0], 32)).split(b'\0')[0]
            if path == b'AbilityTbl.bin':
                value = ABILITY if p['abilityPresent'] else 0
            elif path == b'SkillPointTbl.bin':
                value = POINTS if p['pointsPresent'] else 0
            else:
                raise ValueError(('610 unknown supplied file boundary', path))
        elif address in [0x0203CF9C, 0x0202A498]:
            arity = 2
        elif address == 0x0207AEBC:
            arity = 3
        prepared = words[:min(arity, 4)]
        if arity > 4:
            prepared += list(struct.unpack('<2I', bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), 8))))
        self.events.append(dict(entry=address, preparedWords=prepared, rawRegisterWords=words, providedR0=value))
        u.reg_write(UC_ARM_REG_R0, value)
        for register, index in zip([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12], [1, 2, 3, 12]):
            u.reg_write(register, 0xDE100000 | index)
        u.reg_write(UC_ARM_REG_CPSR, (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0xA0000000)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    def observe(self, u, address, length, data):
        self.instructions += 1
        while self.frames and address == self.frames[-1]['lr'] and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(register) for register in REGS[4:12]] != frame['preserved'] or u.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('610 native helper did not preserve its frame')
            self.returns.append(dict(entry=frame['entry'], preparedWords=frame['words'], returnedWords=[u.reg_read(register) for register in REGS[:4]]))
        if ENTRY <= address < ENTRY + self.extent:
            self.own.add(address)
            return
        if address in PROVIDERS:
            self.provide(address)
            return
        if address in NATIVE:
            words = [u.reg_read(register) for register in REGS[:4]]
            if address == 0x021DD4F0:
                words += list(struct.unpack('<3I', bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP), 12))))
            self.frames.append(dict(entry=address, lr=u.reg_read(UC_ARM_REG_LR), sp=u.reg_read(UC_ARM_REG_SP), preserved=[u.reg_read(register) for register in REGS[4:12]], words=words))
        if any(entry <= address < entry + size for entry, size in NATIVE.items()):
            self.native.add(address)
            return
        raise ValueError(('610 PC outside own/native/provided paths', hex(address)))

    def run(self):
        self.u.emu_start(ENTRY, STOP, count=300000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(register) for register in REGS[4:12]] != self.initial[4:12] or self.frames:
            raise ValueError('610 top did not actually return with preserved frame')
        result = dict(profile=self.p, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), coreRegistersAndCpsr=[self.u.reg_read(register) for register in REGS + [UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR]], nativeReturns=self.returns, providedCalls=self.events, nonstackWrites=self.writes, ownObserved=sorted(self.own), nativeObserved=sorted(self.native), instructions=self.instructions)
        self.u = None
        gc.collect()
        return result
