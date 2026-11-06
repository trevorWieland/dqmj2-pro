import gc
import re
import struct
import match_runtime
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import *
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_JUMP, CS_GRP_CALL
BASE, OVERLAY, STACK, STOP = 0x02000000, 0x021D7240, 0x027F0000, 0x027FF800
ACTOR, DESCRIPTOR, DELTA, TABLE = 0x02700000, 0x02701000, 0x02702000, 0x02600000
ROSTER = 0x021BD674
SUBJECTS = {0x021E4500: 472, 0x021E46D8: 388}
LIMITS = [0x021E8E34, 0x021E8EBC, 0x021E8F44, 0x021E8FCC, 0x021E9054, 0x021E90DC]
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]

def inputs():
    metadata, arm, symbols = measured_module('main')
    module, overlay, overlaySymbols = measured_module('ov001')
    functions = {}
    for name, text in [('main', symbols), ('ov001', overlaySymbols)]:
        for line in text.splitlines():
            found = re.search(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', line)
            if found:
                functions[int(found[3], 0)] = dict(module=name, mode=found[1], bytes=int(found[2], 0))
    ranges = {}
    queue = list(SUBJECTS)
    while queue:
        a = queue.pop()
        if a in ranges:
            continue
        row = functions[a]
        ranges[a] = row
        data, base = (arm, BASE) if row['module'] == 'main' else (overlay, OVERLAY)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if row['mode'] == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for ins in decoder.disasm(data[a-base:a-base+row['bytes']], a):
            if not (ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_CALL)) or not ins.op_str.startswith('#0x'):
                continue
            target = int(ins.op_str[1:], 0) & ~1
            if not a <= target < a + row['bytes'] and target in functions:
                queue.append(target)
    tableObject = struct.unpack_from('<I', arm, 0x020449E8-BASE)[0]
    modeObject = struct.unpack_from('<I', arm, 0x02044450-BASE)[0]
    return dict(main=metadata, module=module, arm=arm, overlay=overlay, ranges=ranges, tableObject=tableObject, modeObject=modeObject)

class Machine:
    def __init__(self, original, profile, entry, body=None):
        self.i, self.p, self.entry = original, profile, entry
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE, 0x800000)
        self.u.mem_write(BASE, original['arm'])
        self.u.mem_write(OVERLAY, original['overlay'])
        self.extent = len(body) if body is not None else SUBJECTS[entry]
        if body is not None:
            self.u.mem_write(entry, body)
        self.frames, self.returns, self.calls, self.observed = [], [], [], set()
        self.instructions = 0
        self.subject = ACTOR if entry == 0x021E4500 else ROSTER + 0x84 * profile['recordIndex']
        self.delta = DELTA if profile['alias'] == 'none' else self.subject + (0x1EC if entry == 0x021E4500 else 0x20)
        self.word(original['tableObject'] + 4, TABLE)
        self.word(original['modeObject'] + 0x20, profile['feature'])
        record = ROSTER + 0x84 * profile['recordIndex']
        self.u.mem_write(ROSTER, bytes(0x84 * 100))
        self.word(record + 0x14, 0x12345678)
        self.u.mem_write(ACTOR, bytes(0x440))
        self.u.mem_write(DESCRIPTOR, bytes(0x200))
        self.u.mem_write(DELTA, bytes(0x40))
        self.word(ACTOR + 0x1E8, DESCRIPTOR)
        self.word(DESCRIPTOR, 0x12345678)
        self.half(DESCRIPTOR + 0x2A, profile['kind'])
        self.byte(DESCRIPTOR + 0x2C, profile['tag'])
        self.half(record + 0x18, profile['kind'])
        self.byte(record + 0x1A, profile['tag'])
        for address, value, size in [(0x40, profile['parents'][0], 2), (0x4C, profile['parents'][1], 1), (0x42, profile['parents'][2], 2), (0x4D, profile['parents'][3], 1)]:
            self.u.mem_write(record + address, (value & ((1 << size * 8)-1)).to_bytes(size, 'little'))
        row = TABLE + profile['kind'] * 100
        self.u.mem_write(row, bytes(100))
        self.half(row + 4, profile['kindWord'])
        for index, value in enumerate(profile['bases']):
            self.half(row + 0x10 + index * 2, value)
        for index, value in enumerate(profile['abilities']):
            self.byte(row + 0x3F + index, value)
        offsets = [0x1EC, 0x1EE, 0x1F4, 0x1F6, 0x1F8, 0x1FA] if entry == 0x021E4500 else [0x20, 0x22, 0x28, 0x2A, 0x2C, 0x2E]
        for index, value in enumerate(profile['deltas']):
            self.half(self.delta + index * 2, value)
        for offset, value in zip(offsets, profile['stats']):
            self.half(self.subject + offset, value)
        if entry == 0x021E4500:
            self.half(self.subject + 0x208, profile['raw208'])
        self.before = bytes(self.u.mem_read(BASE, 0x800000))
        self.initial = [0xA0440000 + index * 0x100 for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR, 0x10)
        for reg, value in zip(REGS, self.initial):
            self.u.reg_write(reg, value)
        self.u.reg_write(UC_ARM_REG_R0, self.subject)
        self.u.reg_write(UC_ARM_REG_R1, self.delta)
        self.u.reg_write(UC_ARM_REG_SP, STACK)
        self.u.reg_write(UC_ARM_REG_LR, STOP)
        self.u.hook_add(UC_HOOK_CODE, self.observe)

    def byte(self, a, v):
        self.u.mem_write(a, bytes([v & 255]))

    def half(self, a, v):
        self.u.mem_write(a, struct.pack('<H', v & 65535))

    def word(self, a, v):
        self.u.mem_write(a, struct.pack('<I', v & 0xFFFFFFFF))

    def observe(self, u, a, length, data):
        self.instructions += 1
        while self.frames and a == self.frames[-1]['lr'] & ~1 and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(r) for r in REGS[4:12]] != frame['preserved'] or bool(u.reg_read(UC_ARM_REG_CPSR) & 32) != bool(frame['lr'] & 1):
                raise ValueError('453 native frame differs')
            self.returns.append(dict(entry=frame['entry'], aliases=frame['aliases'], returnedR0=u.reg_read(UC_ARM_REG_R0)))
        if self.entry <= a < self.entry + self.extent:
            self.observed.add(a)
            return
        if a in self.i['ranges']:
            frame = dict(entry=a, sp=u.reg_read(UC_ARM_REG_SP), lr=u.reg_read(UC_ARM_REG_LR), preserved=[u.reg_read(r) for r in REGS[4:12]], aliases=[])
            if self.frames and frame['sp'] == self.frames[-1]['sp'] and frame['lr'] == self.frames[-1]['lr']:
                self.frames[-1]['aliases'].append(a)
            else:
                self.frames.append(frame)
            if a in LIMITS:
                words = [u.reg_read(r) for r in REGS[:4]] + list(struct.unpack('<2I', bytes(u.mem_read(frame['sp'], 8))))
                self.calls.append(dict(entry=a, preparedWords=words))
        if not any(start <= a < start + row['bytes'] for start, row in self.i['ranges'].items()):
            raise ValueError(('453 unexpected PC', hex(a)))

    def run(self):
        self.u.emu_start(self.entry, STOP, count=20000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(r) for r in REGS[4:12]] != self.initial[4:12] or self.frames:
            raise ValueError('453 top return/frame failed')
        result = dict(profile=self.p, entry=self.entry, subject=self.subject, delta=self.delta, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), calls=self.calls, nativeReturns=self.returns, ownObserved=sorted(self.observed), instructions=self.instructions, returnedR0=self.u.reg_read(UC_ARM_REG_R0))
        self.u = None
        gc.collect()
        return result
