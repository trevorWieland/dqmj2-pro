import hashlib
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946
import ov001_action822_machine_20261102 as R

BASE = 0x021D7240
SP = 0x027F0000
STOP = 0x027FF000
CONTEXT = 0x02500000
MESH = 0x02501000
INDICES = 0x02502000
OUTPUT = 0x02503000
TREE = 0x02504000
POINT = 0x02505000
TRIANGLES = 0x02506000
PROVIDER = 0x021DB968
EXTENTS = {0x021DA4D4: 76, 0x021DA57C: 104, 0x021DBB50: 104}


def word(value):
    return value & 0xFFFFFFFF


def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value


def half(value):
    value &= 0xFFFF
    return value - 0x10000 if value & 0x8000 else value


def pack(values):
    return struct.pack('<' + 'I' * len(values), *map(word, values))


def response(profile, step):
    values = profile['responses']
    return word(values[min(step, len(values) - 1)])


def suppliedWrite(profile, step):
    return ((profile['index'] * 13 + step * 0x1235 + profile.get('seed', profile['ordinal']) * 17) ^ 0xA55A) & 0xFFFF


class Machine:
    def __init__(self, main, overlay, images, profile):
        self.p = profile
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000, 0x00800000)
        self.u.mem_write(0x02000000, main)
        self.u.mem_write(BASE, overlay)
        self.ranges = dict(EXTENTS)
        self.ranges[0x021DA484] = 80
        for address, body in images.items():
            self.u.mem_write(address, body)
            self.ranges[address] = len(body)
        self.beforeContext = bytes((i * 37 + profile.get('seed', profile['ordinal'])) & 255 for i in range(0x80))
        self.beforeOutput = bytes([0xA5]) * 64
        self.beforeIndices = b''.join(struct.pack('<H', (i * 0x123 + profile.get('seed', profile['ordinal'])) & 0xFFFF) for i in range(64))
        self.beforeMesh = bytearray(0x200)
        if profile['kind'] == 'context':
            struct.pack_into('<h', self.beforeMesh, 8, profile['blocks'])
            for index, value in enumerate(profile['sizes']):
                struct.pack_into('<I', self.beforeMesh, 0x10 + index * 12, word(value))
        self.beforeMesh = bytes(self.beforeMesh)
        for address, body in [(CONTEXT, self.beforeContext), (OUTPUT, self.beforeOutput), (INDICES, self.beforeIndices), (MESH, self.beforeMesh)]:
            self.u.mem_write(address, body)
        self.instructions = 0
        self.calls = []
        self.writes = []
        self.ownPcs = set()
        self.helperPcs = set()
        self.helperFrames = []
        self.helperReturns = []
        self.returned = False
        self.lastPc = None
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, unused):
        if not 0x02000000 <= address < address + size <= 0x02800000:
            raise ValueError(('885 outside RAM write', hex(address), size))
        if not SP - 0x1000 <= address < SP:
            self.writes.append([address, size, value])

    def code(self, u, pc, width, unused):
        self.instructions += 1
        if self.instructions > 65000:
            raise ValueError('885 instruction bound')
        if self.helperFrames and pc == self.helperFrames[-1]['lr']:
            frame = self.helperFrames.pop()
            if u.reg_read(R.UC_ARM_REG_SP) != frame['sp'] or [u.reg_read(reg) for reg in R.REGS[4:12]] != frame['saved']:
                raise ValueError('885 original A484 helper ABI failure')
            if self.lastPc != 0x021DA4CC:
                raise ValueError('885 expected native A484 return opcode missing')
            self.helperReturns.append(dict(address='0x21da484', input=frame['input'], returnInstruction=hex(self.lastPc), returnedWord=u.reg_read(R.REGS[0])))
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if any(address <= pc < address + size for address, size in EXTENTS.items()):
            self.ownPcs.add(pc)
        if 0x021DA484 <= pc < 0x021DA4D4:
            self.helperPcs.add(pc)
        if pc == 0x021DA484:
            ordinal = u.reg_read(R.REGS[0])
            if ordinal >= 49:
                raise ValueError('885 unsupported lookup ordinal')
            self.helperFrames.append(dict(input=ordinal, lr=u.reg_read(R.UC_ARM_REG_LR), sp=u.reg_read(R.UC_ARM_REG_SP), saved=[u.reg_read(reg) for reg in R.REGS[4:12]]))
        if pc == PROVIDER:
            step = len(self.calls)
            stack = u.reg_read(R.UC_ARM_REG_SP)
            args = [u.reg_read(reg) for reg in R.REGS[:4]] + list(struct.unpack('<III', bytes(u.mem_read(stack, 12))))
            if step >= 16:
                raise ValueError('885 supplied walk bound')
            result = response(self.p, step)
            mutation = suppliedWrite(self.p, step)
            u.mem_write(INDICES + 2 * (step + 1), struct.pack('<H', mutation))
            self.calls.append(dict(target=hex(PROVIDER), callerWords=args, suppliedReturn=result, suppliedWrite=dict(address=INDICES + 2 * (step + 1), value=mutation)))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(R.REGS[index], 0xE0E00000 + index * 257 + self.p.get('seed', self.p['ordinal']))
            flags = u.reg_read(R.UC_ARM_REG_CPSR)
            u.reg_write(R.UC_ARM_REG_CPSR, (flags & 0x0FFFFFFF) | ((self.p.get('seed', self.p['ordinal']) & 15) << 28))
            u.reg_write(R.REGS[0], result)
            u.reg_write(R.UC_ARM_REG_PC, u.reg_read(R.UC_ARM_REG_LR))
            self.lastPc = pc
            return
        if not any(address <= pc < address + size for address, size in self.ranges.items()):
            raise ValueError(('885 unsupported edge', hex(pc)))
        self.lastPc = pc

    def run(self, address):
        u = self.u
        u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
        for index, reg in enumerate(R.REGS):
            u.reg_write(reg, 0x81810000 + index * 257)
        saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
        p = self.p
        if p['kind'] == 'order':
            args, stack = [OUTPUT, word(p['offset']), word(p['count']), 0x13579BDF], []
        elif p['kind'] == 'context':
            args, stack = [CONTEXT, word(p['index']), TRIANGLES, MESH], []
        else:
            args, stack = [word(p['index']), TREE, INDICES, word(p['ignored'])], [TRIANGLES, POINT, word(p['limit'])]
        for reg, value in zip(R.REGS[:4], args):
            u.reg_write(reg, value)
        u.reg_write(R.UC_ARM_REG_SP, SP)
        u.reg_write(R.UC_ARM_REG_LR, STOP)
        if stack:
            u.mem_write(SP, pack(stack))
        u.emu_start(address, STOP + 4, count=65001)
        if not self.returned or self.helperFrames or u.reg_read(R.UC_ARM_REG_SP) != SP or [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
            raise ValueError('885 proper return/SP/callee-saved failure')
        memory = bytes(u.mem_read(0x02000000, 0x00800000))
        return dict(registers=[u.reg_read(reg) for reg in R.REGS], cpsr=u.reg_read(R.UC_ARM_REG_CPSR), actuallyReturned=True, contextHex=bytes(u.mem_read(CONTEXT, 0x80)).hex(), meshHex=bytes(u.mem_read(MESH, 0x200)).hex(), outputHex=bytes(u.mem_read(OUTPUT, 64)).hex(), indicesHex=bytes(u.mem_read(INDICES, 128)).hex(), memory=memory, memorySha256=hashlib.sha256(memory).hexdigest(), calls=self.calls, writes=self.writes, originalHelperReturns=self.helperReturns, ownPcs=sorted(self.ownPcs), helperPcs=sorted(self.helperPcs), instructions=self.instructions)
