import hashlib
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
NATIVE = {0x0200235C: (16, 2), 0x02002458: (40, 2), 0x020023C4: (56, 0)}
PROVIDERS = {0x021DBBB8: 2, 0x021DA57C: 4}
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
            raise ValueError('880 native helper return/SP/callee-saved failure')
        instructions = list(DIS.disasm(bytes(u.mem_read(self.lastPc, 4)), self.lastPc))
        if len(instructions) != 1:
            raise ValueError('880 return opcode unavailable')
        instruction = instructions[0]
        isReturn = (instruction.mnemonic == 'bx' and instruction.op_str == 'lr') or (instruction.mnemonic.startswith(('pop', 'ldm')) and 'pc' in instruction.op_str)
        if not isReturn:
            raise ValueError(('880 nonreturn completion', hex(self.lastPc), instruction.mnemonic, instruction.op_str))
        result = u.reg_read(R.REGS[0])
        self.nativeReturns.append(dict(entry=hex(frame['entry']), returnInstruction=hex(self.lastPc), disassembly=instruction.mnemonic + ' ' + instruction.op_str, actualReturnWord=result))
        if frame['boundary'] is not None:
            self.calls[frame['boundary']]['actualReturnWord'] = result

    def code(self, u, pc, width, unused):
        self.instructions += 1
        self.minSp = min(self.minSp, u.reg_read(R.UC_ARM_REG_SP))
        if self.instructions > 20000:
            raise ValueError('880 instruction bound')
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
            args = [u.reg_read(reg) for reg in R.REGS[:arity]]
            lr = u.reg_read(R.UC_ARM_REG_LR)
            boundary = None
            if pc == 0x0200235C:
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
            raise ValueError(('880 unsupported native edge', hex(pc)))
        self.lastPc = pc

    def run(self, entry):
        result = super().run(entry)
        if self.frames:
            raise ValueError('880 unreturned native frames')
        self.hardware.verify()
        result.update(nativeHelperPhysicalReturns=self.nativeReturns, nativeHelperEntries=self.nativeEntries, nativeHelperPcs=sorted(self.nativePcs), deviceWrites=self.deviceWrites, hardwareOperations=self.hardware.operations, hardwareSha256=hashlib.sha256(bytes(self.u.mem_read(0x04000000, 4096))).hexdigest())
        return result
