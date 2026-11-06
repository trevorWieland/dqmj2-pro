import gc
import re
import struct
import match_runtime as c
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
BASE, OVERLAY, ENTRY, SIZE, PRIVATE = 0x02000000, 0x021D7240, 0x021E6704, 1000, 0x02650000
STACK, STOP = 0x027F0000, 0x027FF800
INPUT, OUTPUT, META, POINTS, CURVE, GLOBAL = 0x02610000, 0x02620000, 0x02630000, 0x02640000, 0x02642000, 0x021ED438
PROVIDERS = {0x020CF620, 0x020CF658, 0x020CF590, 0x020CF6A4, 0x020449D4, 0x021E65EC, 0x0203CC2C, 0x0203CF9C, 0x0202A498}
WATCH = {0x02008C58, 0x02008D78, 0x02008E0C, 0x0206485C, 0x02025A70, 0x02024E0C, 0x02025578, 0x02025AB8, 0x020259B4, 0x021E1014, 0x021E664C, 0x021E6660, 0x021E6678, 0x021E6AEC, 0x021E6B20}
REGS = c.REGISTERS[:13]


def inputs():
    main, arm, main_symbols = measured_module('main')
    module, overlay, symbols = measured_module('ov005')
    if main['sha256'] != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f' or module['sha256'] != 'efd21cd223735980e3f83f95c796725b0abd677043c40ca26d9762e4ea9a97c8':
        raise ValueError('670 input identity differs')
    ranges = {}
    for address in WATCH:
        text = main_symbols if address < OVERLAY else symbols
        match = re.search(r'^\S+ kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:0x' + f'{address:08x}' + r'$', text, re.M)
        if not match:
            raise ValueError(('670 watched configured function missing', hex(address)))
        ranges[address] = dict(mode=match[1], bytes=int(match[2], 16))
    return dict(main=main, arm=arm, module=module, overlay=overlay, ranges=ranges)


class Machine:
    def __init__(self, original, profile, candidate_body, candidate=False):
        self.p, self.original, self.candidate = profile, original, candidate
        self.entry = PRIVATE if candidate else ENTRY
        self.extent = len(candidate_body) if candidate else SIZE
        if not PRIVATE + len(candidate_body) <= 0x02670000 or any(PRIVATE <= address < PRIVATE + len(candidate_body) for address in WATCH | PROVIDERS):
            raise ValueError('670 private code mapping overlap')
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE, 0x800000)
        self.u.mem_write(BASE, original['arm'])
        self.u.mem_write(OVERLAY, original['overlay'])
        self.u.mem_write(PRIVATE, candidate_body)
        self.u.mem_write(INPUT, bytes(profile['input']))
        self.u.mem_write(OUTPUT, bytes(profile['output']))
        self.u.mem_write(POINTS, bytes(profile['points']))
        self.u.mem_write(CURVE, struct.pack('<257I', *profile['curve']))
        for index, metadata in enumerate(profile['metadata']):
            self.u.mem_write(META + index * 64, bytes(metadata))
        for offset, value in zip([0x4C, 0x50, 0x54], profile['globalWords']):
            self.u.mem_write(GLOBAL + offset, struct.pack('<I', value))
        self.initial = [0xA6700000 + index * 256 for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR, 0xA0000010)
        for register, value in zip(REGS, self.initial):
            self.u.reg_write(register, value)
        self.u.reg_write(UC_ARM_REG_R0, INPUT)
        self.u.reg_write(UC_ARM_REG_R1, OUTPUT)
        self.u.reg_write(UC_ARM_REG_SP, STACK)
        self.u.reg_write(UC_ARM_REG_LR, STOP)
        self.frames, self.returns, self.providers, self.writes = [], [], [], []
        self.own, self.native, self.instructions, self.metadata_index, self.curve_index = set(), set(), 0, 0, 0
        self.checksum_snapshot = None
        self.before = bytes(self.u.mem_read(BASE, 0x800000))
        self.u.hook_add(UC_HOOK_CODE, self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, data):
        if STACK - 65536 <= address < STACK + 256:
            return
        if not OUTPUT <= address or address + size > OUTPUT + len(self.p['output']):
            raise ValueError(('670 unexpected nonstack effect', hex(address), size, hex(u.reg_read(UC_ARM_REG_PC)), value))
        self.writes.append([u.reg_read(UC_ARM_REG_PC), address, size, value & ((1 << (size * 8)) - 1)])

    def service(self, u, address):
        words = [u.reg_read(register) for register in REGS[:4]]
        effects, contract, value = [], [], 0
        if address == 0x020CF620:
            contract = words[:1]
            if contract != [1]:
                raise ValueError('670 enter contract differs')
            value = 0xE6700001
        elif address == 0x020CF658:
            value = 0xE670F00D
        elif address == 0x020CF590:
            contract = words[:3]
            raw = words[0] - 0x100000000 if words[0] & 0x80000000 else words[0]
            normalized, variant = ((raw * 3 + 7) & 0xFFFF), ((raw ^ 5) & 3)
            sp = u.reg_read(UC_ARM_REG_SP)
            if words[1:3] != [sp + 2, sp]:
                raise ValueError('670 native normalizer output slots differ')
            for target, payload in [(words[1], struct.pack('<H', normalized)), (words[2], bytes([variant]))]:
                u.mem_write(target, payload)
                effects.append(dict(address=target, bytes=payload.hex(), storage='native helper stack'))
            value = 0xE6700002
        elif address == 0x020CF6A4:
            contract = words[:2]
            if words[0] != words[1] or not any(OUTPUT + 0xC4 + row * 0x84 + 0x7A <= words[0] < OUTPUT + 0xC4 + row * 0x84 + 0x84 for row in range(3)):
                raise ValueError('670 pair alias contract differs')
            value = 0xE6700003
        elif address == 0x020449D4:
            contract = words[:1]
            value = META + self.metadata_index * 64
            self.metadata_index += 1
        elif address == 0x021E65EC:
            contract = words[:3]
            value = CURVE + 4 if self.p['curvePresent'][self.curve_index] else 0
            self.curve_index += 1
        elif address == 0x0203CC2C:
            contract = words[:2]
            if contract != [0x021E7894, 1]:
                raise ValueError('670 point opener contract differs')
            value = POINTS if self.p['pointsOpened'] else 0
        elif address == 0x0202A498:
            contract = words[:2]
            if words[0] != 1 or words[1] not in [0, CURVE + 4]:
                raise ValueError('670 supplied general-release words differ')
            value = 0xE6700005
        elif address == 0x0203CF9C:
            contract = words[:2]
            if words[0] != 1 or words[1] != POINTS:
                raise ValueError('670 closer contract differs')
            value = 0xE6700004
        self.providers.append(dict(entry=address, preparedWords=contract, rawRegisterWords=words, providedR0=value, ramEffects=effects))
        u.reg_write(UC_ARM_REG_R0, value)
        for register, index in zip([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12], [1, 2, 3, 12]):
            u.reg_write(register, 0xDE700000 | index)
        u.reg_write(UC_ARM_REG_CPSR, (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0x60000000)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    def observe(self, u, address, length, data):
        self.instructions += 1
        while self.frames and address == (self.frames[-1]['lr'] & ~1) and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(register) for register in REGS[4:12]] != frame['preserved'] or bool(u.reg_read(UC_ARM_REG_CPSR) & 32) != bool(frame['lr'] & 1):
                raise ValueError(('670 watched helper return frame differs', hex(frame['entry'])))
            self.returns.append(dict(entry=frame['entry'], preparedWords=frame['words'], returnedWords=[u.reg_read(register) for register in REGS[:4]], actualReturn=True))
        if self.entry <= address < self.entry + self.extent:
            self.own.add(address)
            return
        if address in PROVIDERS:
            self.service(u, address)
            return
        if address in WATCH:
            words = [u.reg_read(register) for register in REGS[:4]]
            self.frames.append(dict(entry=address, lr=u.reg_read(UC_ARM_REG_LR), sp=u.reg_read(UC_ARM_REG_SP), words=words, preserved=[u.reg_read(register) for register in REGS[4:12]]))
            if address == 0x021E1014:
                self.checksum_snapshot = bytes(u.mem_read(OUTPUT, 0x268))
        if BASE <= address < BASE + len(self.original['arm']) or any(start <= address < start + item['bytes'] for start, item in self.original['ranges'].items() if start >= OVERLAY):
            self.native.add(address)
            return
        raise ValueError(('670 PC outside own/native/provided scopes', hex(address)))

    def run(self):
        self.u.emu_start(self.entry, STOP, count=500000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(register) for register in REGS[4:12]] != self.initial[4:12] or self.frames or self.metadata_index != 3 or self.curve_index != 3:
            raise ValueError('670 top did not actually return preserving frame/contracts')
        result = dict(profile=self.p, candidate=self.candidate, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), output=bytes(self.u.mem_read(OUTPUT, len(self.p['output']))), checksumSnapshot=self.checksum_snapshot, coreRegistersAndCpsr=[self.u.reg_read(register) for register in REGS + [UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR]], watchedNativeReturns=self.returns, providedCalls=self.providers, nonstackWrites=self.writes, ownObserved=sorted(self.own), nativeObserved=sorted(self.native), instructions=self.instructions)
        self.u = None
        gc.collect()
        return result
