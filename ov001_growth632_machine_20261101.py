import gc
import struct
import probe_main_float592_native_20261101 as Q
from link_runtime_unit import measured_module
from unicorn.arm_const import *
BASE, STACK, STOP, REGS = Q.BASE, Q.STACK, Q.STOP, Q.REGS
OVERLAY, ENTRY, SIZE = 0x021D7240, 0x0222D240, 1696
ROWS, IDS, OUTPUT, META, RNGSTATE = 0x022498FC, 0x02249830, 0x0224983C, 0x02610000, 0x020F6044
CALLBACKS = [0x02044A14, 0x02044A58, 0x02044A9C, 0x02044AE0, 0x02044B24, 0x02044B68]
FEATURES = [0x0207C2B8, 0x0207C3D8, 0x0207C424, 0x0207C52C, 0x0207C634, 0x0207C73C]
PROVIDERS = [0x0222D8E0, 0x0222D91C, 0x0222D93C, 0x0222D964, 0x02044CDC, 0x020449D4] + CALLBACKS + FEATURES
FLOATS = [0x02025A28, 0x02025A70, 0x02024E0C, 0x02025578, 0x02025AB8, 0x020259B4]
WATCH = FLOATS + [0x02008D78, 0x0203D294, 0x02026350]


def inputs():
    main, arm, unused = measured_module('main')
    module, overlay, unused = measured_module('ov001')
    if main['sha256'] != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f' or module['sha256'] != '39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92':
        raise ValueError('632 measured images differ')
    return dict(main=main, arm=arm, module=module, overlay=overlay)


class Machine(Q.Machine):
    def __init__(self, original, profile, body=None):
        if profile['category'] not in [0, 1, 2]:
            raise ValueError('632 inherited-register category path is unsupported')
        self.p, self.extent = profile, len(body) if body is not None else SIZE
        super().__init__(original['arm'], profile['case'])
        self.u.mem_write(OVERLAY, original['overlay'])
        if body is not None:
            self.u.mem_write(ENTRY, body)
        self.u.mem_write(ROWS, b'\xCC' * 396)
        self.u.mem_write(OUTPUT, b'\xA5' * 192)
        self.u.mem_write(ROWS + profile['row'] * 132 + 0x1A, bytes([profile['variant']]))
        self.u.mem_write(ROWS + profile['row'] * 132 + 0x30, bytes([profile['level']]))
        self.u.mem_write(META, b'\xA7' * 128)
        self.u.mem_write(META + 0x1C, struct.pack('<6H', *profile['bases']))
        self.u.mem_write(IDS + profile['row'] * 4, struct.pack('<I', profile['id']))
        self.u.mem_write(RNGSTATE, struct.pack('<I', profile['seed']))
        self.before = bytes(self.u.mem_read(BASE, 0x800000))
        self.frames, self.returns, self.providers, self.writes = [], [], [], []
        self.own, self.main, self.previous = set(), set(), None

    def provide(self, address):
        u, p = self.u, self.p
        words = [u.reg_read(register) for register in REGS[:4]]
        arity, value = 0, 0xE6320001
        if address == 0x0222D8E0:
            value = int(p['growthPresent'])
        elif address == 0x02044CDC:
            arity, value = 1, p['category']
        elif address == 0x020449D4:
            arity, value = 1, META
        elif address in CALLBACKS:
            arity, value = 3, (CALLBACKS.index(address) + words[2] + p['salt']) % 4
        elif address == 0x0222D91C:
            arity, value = 2, (words[0] * 3 + words[1] + p['salt']) % 7
        elif address == 0x0222D964:
            arity, value = 2, (words[0] + 2 * words[1] + 1) % 9
        elif address in FEATURES:
            arity, value = 2, p['featureWords'][FEATURES.index(address)]
        event = dict(entry=address, preparedWords=words[:arity], rawRegisterWords=words, providedR0=value, ramEffects=[])
        if address in FEATURES:
            event['observedRowStatHalfwordsBeforeCall'] = list(struct.unpack('<8H', bytes(u.mem_read(ROWS + p['row'] * 132 + 0x20, 16))))
        self.providers.append(event)
        u.reg_write(UC_ARM_REG_R0, value)
        for register, index in zip([UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12], [1, 2, 3, 12]):
            u.reg_write(register, 0xDE320000 | index)
        u.reg_write(UC_ARM_REG_CPSR, (u.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | 0xA0000000)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    def code(self, u, address, length, data):
        previous, self.previous = self.previous, address
        self.instructions += 1
        while self.frames and address == self.frames[-1]['lr'] and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(register) for register in REGS[4:12]] != frame['preserved'] or u.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('632 native dependency frame differs')
            self.returns.append(dict(entry=frame['entry'], preparedWords=frame['words'], returnedWords=[u.reg_read(register) for register in REGS[:4]]))
        if address in PROVIDERS and previous is not None:
            opcode = int.from_bytes(u.mem_read(previous, 4), 'little')
            displacement = opcode & 0xFFFFFF
            if displacement & 0x800000:
                displacement -= 0x1000000
            if opcode & 0xFF000000 == 0xEB000000 and (previous + 8 + 4 * displacement) & 0xFFFFFFFF == address and u.reg_read(UC_ARM_REG_LR) == previous + 4:
                self.provide(address)
                return
        if ENTRY <= address < ENTRY + self.extent:
            self.own.add(address)
            return
        if not BASE <= address < BASE + self.armLength:
            raise ValueError(('632 PC outside own/measured main/provided call edges', hex(address)))
        if address in WATCH:
            self.frames.append(dict(entry=address, lr=u.reg_read(UC_ARM_REG_LR), sp=u.reg_read(UC_ARM_REG_SP), words=[u.reg_read(register) for register in REGS[:4]], preserved=[u.reg_read(register) for register in REGS[4:12]]))
        self.main.add(address)

    def write(self, u, access, address, size, value, data):
        if STACK - 65536 <= address < STACK + 256:
            return
        row = ROWS + self.p['row'] * 132
        if not (address == RNGSTATE and size == 4 or row <= address and address + size <= row + 132):
            raise ValueError(('632 unexpected nonstack effect', hex(address), size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC), address, size, value & ((1 << (size * 8)) - 1)])

    def run(self):
        returned = self.call(ENTRY, [self.p['row'], self.p['modifier']])
        if self.frames:
            raise ValueError('632 native frame remained after actual top return')
        result = dict(profile=self.p, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), coreRegistersAndCpsr=[self.u.reg_read(register) for register in REGS + [UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR]], actualTopReturnedWords=returned, nativeReturns=self.returns, providedCalls=self.providers, nonstackWrites=self.writes, ownObserved=sorted(self.own), mainObserved=sorted(self.main), instructions=self.instructions)
        self.u = None
        gc.collect()
        return result
