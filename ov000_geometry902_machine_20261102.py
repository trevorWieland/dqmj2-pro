import hashlib
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_MEM_READ
import ov001_action822_machine_20261102 as R
import ov000_geometry877_machine_20261102 as B
from blend_math_hardware_20261102 import BlendMathHardware

ENTRY = B.ENTRY
SP = B.SP
MESH = B.MESH
RECORD = B.RECORD
CONTEXT = B.CONTEXT
NATIVE = {0x0200235C: (16, 2), 0x02002458: (40, 2), 0x020023C4: (56, 0), 0x021DBBB8: (96, 2), 0x021DBB50: (104, 7), 0x021DB968: (488, 7), 0x021DB92C: (60, 3), 0x021DA57C: (104, 4)}
PROVIDERS = {}
DIS = Cs(CS_ARCH_ARM, CS_MODE_ARM)


class Machine(B.Machine):
    def __init__(self, main, overlay, images, profile):
        super().__init__(main, overlay, images, profile)
        self.frames = []
        self.nativeReturns = []
        self.nativeEntries = []
        self.nativePcs = set()
        self.deviceWrites = []
        self.lastPc = None
        self.u.mem_map(0x04000000, 0x1000)
        self.hardware = BlendMathHardware(self.u)
        for address, (size, unused) in NATIVE.items():
            self.ranges[address] = size
        self.u.hook_add(UC_HOOK_MEM_READ, self.read)
        mesh = bytearray(self.beforeMesh)
        struct.pack_into('<h', mesh, 8, 1)
        struct.pack_into('<I', mesh, 0x10, 1)
        struct.pack_into('<II', mesh, 0x198, 0x180, 1)
        mesh[0x180:0x186] = bytes([255]) * 6
        self.beforeMesh = bytes(mesh)
        self.u.mem_write(MESH, self.beforeMesh)
        context = bytearray(self.beforeContext)
        struct.pack_into('<I', context, 8, profile.get('indexWord', 0))
        context[0x10] = profile.get('capacityRaw', 1)
        struct.pack_into('<H', context, 0x12, 0x7FFE)
        self.beforeContext = bytes(context)
        self.u.mem_write(CONTEXT, self.beforeContext)


    def read(self, u, access, address, size, value, unused):
        if 0x04000000 <= address < address + size <= 0x04001000:
            self.hardware.read(address, size)

    def write(self, u, access, address, size, value, unused):
        if 0x04000000 <= address < address + size <= 0x04001000:
            self.hardware.write(address, size, value)
            self.deviceWrites.append([address, size, value])
            return
        super().write(u, access, address, size, value, unused)

    def returnedFrame(self, u, pc):
        if not self.frames or pc != self.frames[-1]['lr']:
            return
        frame = self.frames.pop()
        if u.reg_read(R.UC_ARM_REG_SP) != frame['sp'] or [u.reg_read(reg) for reg in R.REGS[4:12]] != frame['saved']:
            raise ValueError('902 native helper return/SP/callee-saved failure')
        instructions = list(DIS.disasm(bytes(u.mem_read(self.lastPc, 4)), self.lastPc))
        if len(instructions) != 1:
            raise ValueError('902 return opcode unavailable')
        instruction = instructions[0]
        isReturn = (instruction.mnemonic == 'bx' and instruction.op_str == 'lr') or (instruction.mnemonic.startswith(('pop', 'ldm')) and 'pc' in instruction.op_str)
        if not isReturn:
            raise ValueError(('902 nonreturn completion', hex(self.lastPc), instruction.mnemonic, instruction.op_str))
        result = u.reg_read(R.REGS[0])
        self.nativeReturns.append(dict(entry=hex(frame['entry']), returnInstruction=hex(self.lastPc), disassembly=instruction.mnemonic + ' ' + instruction.op_str, actualReturnWord=result))
        if frame['boundary'] is not None:
            self.calls[frame['boundary']]['actualReturnWord'] = result

    def code(self, u, pc, width, unused):
        self.instructions += 1
        self.minSp = min(self.minSp, u.reg_read(R.UC_ARM_REG_SP))
        if self.instructions > 20000:
            raise ValueError('902 instruction bound')
        self.returnedFrame(u, pc)
        if pc == 0x027FF000:
            self.returned = True
            u.emu_stop()
            return
        if ENTRY <= pc < ENTRY + 1884:
            self.ownPcs.add(pc)
        if any(address <= pc < address + size for address, (size, unused) in NATIVE.items()):
            self.nativePcs.add(pc)
        if pc in NATIVE:
            size, arity = NATIVE[pc]
            args = [u.reg_read(reg) for reg in R.REGS[:min(4, arity)]]
            if arity > 4:
                args += list(struct.unpack("<" + "I" * (arity - 4), bytes(u.mem_read(u.reg_read(R.UC_ARM_REG_SP), 4 * (arity - 4)))))
            lr = u.reg_read(R.UC_ARM_REG_LR)
            boundary = None
            if pc in [0x0200235C, 0x021DBBB8, 0x021DA57C]:
                boundary = len(self.calls)
                self.calls.append(dict(target=hex(pc), callerWords=args, nativeExecution=True))
                self.callSites.append(dict(target=hex(pc), callerReturnPc=hex(lr)))
            self.nativeEntries.append(dict(entry=hex(pc), callerWords=args, callerReturnPc=hex(lr)))
            self.frames.append(dict(entry=pc, lr=lr, sp=u.reg_read(R.UC_ARM_REG_SP), saved=[u.reg_read(reg) for reg in R.REGS[4:12]], boundary=boundary))
        if pc in PROVIDERS:
            args = [u.reg_read(reg) for reg in R.REGS[:PROVIDERS[pc]]]
            self.lastProviderAttempt = dict(target=hex(pc), callerWords=args)
            self.callSites.append(dict(target=hex(pc), callerReturnPc=hex(u.reg_read(R.UC_ARM_REG_LR))))
            result = self.provider(pc, args)
            self.calls.append(dict(target=hex(pc), callerWords=args, suppliedReturn=B.word(result)))
            for index in [0, 1, 2, 3, 12]:
                u.reg_write(R.REGS[index], 0xF0F00000 + index * 257 + self.p['ordinal'])
            flags = u.reg_read(R.UC_ARM_REG_CPSR)
            u.reg_write(R.UC_ARM_REG_CPSR, (flags & 0x0FFFFFFF) | ((self.p['ordinal'] & 15) << 28))
            u.reg_write(R.REGS[0], B.word(result))
            u.reg_write(R.UC_ARM_REG_PC, u.reg_read(R.UC_ARM_REG_LR))
            self.lastPc = pc
            return
        if not any(address <= pc < address + size for address, size in self.ranges.items()):
            raise ValueError(('902 unsupported native edge', hex(pc)))
        self.lastPc = pc

    def run(self, entry):
        u = self.u
        u.reg_write(R.UC_ARM_REG_CPSR, 0xD3)
        for index, reg in enumerate(R.REGS):
            u.reg_write(reg, 0x81810000 + index * 257)
        saved = [u.reg_read(reg) for reg in R.REGS[4:12]]
        for reg, value in zip(R.REGS[:4], [B.POINT, CONTEXT, 0 if self.p['nullOutput'] else B.OUTPUT, 1]):
            u.reg_write(reg, value)
        u.reg_write(R.UC_ARM_REG_SP, SP)
        u.reg_write(R.UC_ARM_REG_LR, 0x027FF000)
        u.mem_write(SP, B.pack([self.p['mask']]))
        u.emu_start(entry, 0x027FF000 + 4, count=20001)
        if not self.returned or u.reg_read(R.UC_ARM_REG_SP) != SP or [u.reg_read(reg) for reg in R.REGS[4:12]] != saved:
            raise ValueError('872 proper return/SP/callee-saved ABI missing')
        result = dict(registers=[u.reg_read(reg) for reg in R.REGS], cpsr=u.reg_read(R.UC_ARM_REG_CPSR), actuallyReturned=True, outputHex=bytes(u.mem_read(B.OUTPUT, 12)).hex(), meshHex=bytes(u.mem_read(MESH, 0x200)).hex(), contextHex=bytes(u.mem_read(CONTEXT, 0x20)).hex(), calls=self.calls, callSites=self.callSites, writes=self.writes, instructions=self.instructions, ownPcs=sorted(self.ownPcs), privateStackStart=self.minSp, memory=bytes(u.mem_read(0x02000000, 0x00800000)))
        if self.frames:
            raise ValueError('902 unreturned native frames')
        self.hardware.verify()
        result.update(nativeHelperPhysicalReturns=self.nativeReturns, nativeHelperEntries=self.nativeEntries, nativeHelperPcs=sorted(self.nativePcs), deviceWrites=self.deviceWrites, hardwareOperations=self.hardware.operations, hardwareSha256=hashlib.sha256(bytes(self.u.mem_read(0x04000000, 4096))).hexdigest())
        return result
