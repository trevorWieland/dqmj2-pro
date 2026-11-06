import gc
import struct
import probe_main_float592_native_20261101 as Q
from link_runtime_unit import measured_module
from unicorn.arm_const import *
BASE, STACK, STOP, REGS = Q.BASE, Q.STACK, Q.STOP, Q.REGS
OVERLAY, ENTRY, SIZE, ROWS = 0x021D7240, 0x0222CEB8, 124, 0x022498FC
U32DOUBLE, MULTIPLY, ADD, TRUNCATE = 0x02024504, 0x02024540, 0x02023F78, 0x020243E0
WATCH = [U32DOUBLE, MULTIPLY, ADD, TRUNCATE]


def inputs():
    main, arm, unused = measured_module('main')
    module, overlay, unused = measured_module('ov001')
    if main['sha256'] != 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f' or module['sha256'] != '39fc7aab33ce02b1910cb8fac58dd9e19936c468f3d03d1ec17dfdc8fe40ce92':
        raise ValueError('626 measured images differ')
    return dict(main=main, arm=arm, module=module, overlay=overlay)


class Machine(Q.Machine):
    def __init__(self, original, profile, body=None):
        self.p = profile
        self.extent = len(body) if body is not None else SIZE
        super().__init__(original['arm'], profile['case'])
        self.u.mem_write(OVERLAY, original['overlay'])
        if body is not None:
            self.u.mem_write(ENTRY, body)
        self.u.mem_write(ROWS, b'\xCC' * 396)
        self.before = bytes(self.u.mem_read(BASE, 0x800000))
        self.own, self.main, self.frames, self.returns, self.writes = set(), set(), [], [], []

    def code(self, u, address, length, data):
        self.instructions += 1
        while self.frames and address == self.frames[-1]['lr'] and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(register) for register in REGS[4:12]] != frame['preserved'] or u.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('626 native helper return frame differs')
            self.returns.append(dict(entry=frame['entry'], preparedWords=frame['words'], returnedWords=[u.reg_read(register) for register in REGS[:4]]))
        if ENTRY <= address < ENTRY + self.extent:
            self.own.add(address)
            return
        if not BASE <= address < BASE + self.armLength:
            raise ValueError(('626 PC outside own/measured initialized main', hex(address)))
        if address in WATCH:
            self.frames.append(dict(entry=address, lr=u.reg_read(UC_ARM_REG_LR), sp=u.reg_read(UC_ARM_REG_SP), words=[u.reg_read(register) for register in REGS[:4]], preserved=[u.reg_read(register) for register in REGS[4:12]]))
        self.main.add(address)

    def write(self, u, access, address, size, value, data):
        if STACK - 65536 <= address < STACK + 256:
            return
        if address != ROWS + self.p['row'] * 132 + 0x30 or size != 1:
            raise ValueError(('626 unexpected nonstack native effect', hex(address), size))
        self.writes.append([u.reg_read(UC_ARM_REG_PC), address, size, value & 255])

    def run(self):
        returned = self.call(ENTRY, [self.p['row'], self.p['scalar']])
        if self.frames:
            raise ValueError('626 native helper frame remained after top return')
        result = dict(profile=self.p, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), coreRegistersAndCpsr=[self.u.reg_read(register) for register in REGS + [UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR]], nativeReturns=self.returns, nonstackWrites=self.writes, ownObserved=sorted(self.own), mainObserved=sorted(self.main), instructions=self.instructions, actualTopReturnedWords=returned)
        self.u = None
        gc.collect()
        return result
