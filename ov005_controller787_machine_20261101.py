import hashlib
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
ENTRY = 35507320
CONTEXT = 35559448
REFERENCE = 38862848
STACK = 41877504
STOP = 41940992

def writeword(u, address, value):
    u.mem_write(address, struct.pack('<I', value & 4294967295))

class BaseMachine:

    def __init__(self, main, overlay, images, providers, profile):
        self.u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(33554432, 8388608)
        self.u.mem_map(67108864, 4096)
        self.u.mem_write(33554432, main)
        self.u.mem_write(35484224, overlay)
        for address, body in images.items():
            self.u.mem_write(address, body)
        self.profile = profile
        self.providers = {x['address']: x['mode'] for x in providers}
        self.trace = []
        self.writes = []
        self.rawCalls = []
        self.instructions = 0
        self.getterPending = None
        self.getterReturns = 0
        self.returned = False
        self.u.mem_write(CONTEXT, bytes(128))
        self.u.mem_write(CONTEXT + 4, bytes([profile['state']]))
        self.u.mem_write(CONTEXT + 3, bytes([profile['selector']]))
        self.u.mem_write(CONTEXT + 103, bytes([profile['branch']]))
        self.u.mem_write(CONTEXT + 100, bytes([profile['counter'], profile['delta'] & 255]))
        self.u.mem_write(CONTEXT + 10, struct.pack('<H', profile['mask']))
        self.u.mem_write(CONTEXT + 16, struct.pack('<h', profile['position']))
        for offset in [20, 48, 104]:
            writeword(self.u, CONTEXT + offset, profile['branch'])
        writeword(self.u, CONTEXT + 72, 305397760 + profile['ordinal'])
        writeword(self.u, CONTEXT + 44, 32)
        writeword(self.u, CONTEXT + 52, 16)
        writeword(self.u, CONTEXT + 108, 0)
        for address, value in [(35560984 + 124, 4294967295), (35560552 + 124, 2147483648)]:
            writeword(self.u, address, value)
        self.u.mem_write(34562306, bytes([profile['mode']]))
        self.u.mem_write(REFERENCE, struct.pack('<8H', 0, profile['mask'], 0, 0, 0, 0, 0, 0))
        self.u.mem_write(67108864, bytes([165]) * 4096)
        self.beforeContext = bytes(self.u.mem_read(CONTEXT, 128))
        self.beforeMmio = bytes(self.u.mem_read(67108864, 4096))
        self.u.hook_add(UC_HOOK_CODE, self.code)
        self.u.hook_add(UC_HOOK_MEM_WRITE, self.write)

    def write(self, u, access, address, size, value, data):
        if not (33554432 <= address and address + size <= 41943040 or (67108864 <= address and address + size <= 67112960)):
            raise ValueError('784 write outside supplied RAM/MMIO shadow')
        self.writes.append((address, size, value))

    def code(self, u, pc, width, data):
        self.instructions += 1
        if self.instructions > 100000:
            raise ValueError('784 instruction bound')
        if self.getterPending == pc:
            if u.reg_read(REGS[0]) != self.profile['mode']:
                raise ValueError('784 original raw byte getter differs')
            self.getterPending = None
            self.getterReturns += 1
        if pc == STOP:
            self.returned = True
            u.emu_stop()
            return
        if pc == 33822720:
            self.getterPending = u.reg_read(UC_ARM_REG_LR) & ~1
        if pc in self.providers and pc != 33822720:
            mode = 'thumb' if u.reg_read(UC_ARM_REG_CPSR) & 32 else 'arm'
            if mode != self.providers[pc]:
                raise ValueError('784 supplied target mode differs')
            lr = u.reg_read(UC_ARM_REG_LR)
            sp = u.reg_read(UC_ARM_REG_SP)
            args = [u.reg_read(r) for r in REGS[:4]]
            result = REFERENCE if pc == 35523204 else self.profile['serviceWord']
            self.trace.append((pc, result))
            self.rawCalls.append(dict(target=hex(pc), mode=mode, arguments=args, stackWords=list(struct.unpack('<4I', u.mem_read(sp, 16))), returnPc=hex(lr & ~1)))
            for index in [1, 2, 3, 12]:
                u.reg_write(REGS[index], 3774873600 + index * 257 + len(self.trace))
            u.reg_write(REGS[0], result)
            u.reg_write(UC_ARM_REG_CPSR, u.reg_read(UC_ARM_REG_CPSR) & ~4026531872 | self.profile['flags'] | (32 if lr & 1 else 0))
            u.reg_write(UC_ARM_REG_PC, lr & ~1)
            return
        if ENTRY <= pc < ENTRY + 2328 or 40173568 <= pc < 40206336 or 33822720 <= pc < 33822740 or (33822712 <= pc < 33822720):
            return
        raise ValueError(('784 unprovided native execution escaped own body/getter', hex(pc)))

    def run(self, entry, args=()):
        self.u.reg_write(UC_ARM_REG_CPSR, 31)
        for index, register in enumerate(REGS):
            self.u.reg_write(register, 2684354560 + index * 65793)
        for register, value in zip(REGS, args):
            self.u.reg_write(register, value)
        preserved = [self.u.reg_read(r) for r in REGS[4:12]]
        self.u.reg_write(UC_ARM_REG_SP, STACK)
        self.u.reg_write(UC_ARM_REG_LR, STOP)
        self.u.emu_start(entry, 0, count=100000)
        if not self.returned or self.getterPending is not None or self.u.reg_read(UC_ARM_REG_SP) != STACK or ([self.u.reg_read(r) for r in REGS[4:12]] != preserved):
            raise ValueError('784 actual top return/frame failed')
        return dict(rawR0=self.u.reg_read(REGS[0]), providedCalls=self.trace, rawCalls=self.rawCalls, getterReturns=self.getterReturns, ownContext=bytes(self.u.mem_read(CONTEXT, 128)), mmio=bytes(self.u.mem_read(67108864, 4096)), state=bytes(self.u.mem_read(33554432, 8257536)), topRam=bytes(self.u.mem_read(41877760, 65280)), writes=[row for row in self.writes if not 41811968 <= row[0] < 41877760], instructions=self.instructions, actuallyReturned=True)

def base_model(machine, result):
    p = machine.profile
    if p['state'] not in [19, 25, 28, 29, 255]:
        return False
    expected = bytearray(machine.beforeContext)
    mmio = bytearray(machine.beforeMmio)
    if p['branch'] == 1:
        expected[10:12] = bytes(2)
    if p['state'] == 28:
        if result['rawR0'] != 2:
            raise ValueError('784 independent state28 return differs')
    else:
        expected[10:12] = struct.pack('<H', p['mask'])
        if p['state'] == 25 and p['delta']:
            value = p['counter']
            struct.pack_into('<I', mmio, 16, value & 511 | value << 16 & 33488896)
            expected[100] = value + p['delta'] & 255
        if result['rawR0'] != 9:
            raise ValueError('784 independent common return differs')
    if struct.unpack_from('<I', result['state'], 1044520)[0] != (0 if p['state'] == 28 else 1):
        raise ValueError('787 independent global word write differs')
    if result['ownContext'] != bytes(expected) or result['mmio'] != bytes(mmio):
        raise ValueError('784 independent selected-state effect model differs')
    return True
from project import ROOT
import re
NATIVE_EXTRA = [33822564, 33728052, 33941524, 33945356, 33945248, 33942872, 33784136, 33782212, 33851972, 33771868, 33770856, 33664900]
ANIMATION = {33851972, 33771868, 33770856, 33664900}
SLOT = 35359504
OBJECT = 38993920
CONTROLLER = 35560992
FRAME = 38928384

def ranges_and_lines():
    config = (ROOT / 'config/arm9/symbols.txt').read_text()
    ranges = {}
    for mode, size, address in re.findall('kind:function\\((arm|thumb),size=(0x[0-9a-f]+)\\) addr:(0x[0-9a-f]+)', config):
        a = int(address, 0)
        if a in NATIVE_EXTRA:
            if mode != 'arm':
                raise ValueError('787 extra native mode differs')
            ranges[a] = (a + int(size, 0), mode)
    if len(ranges) != len(NATIVE_EXTRA):
        raise ValueError('787 native boundary missing')
    overlayConfig = (ROOT / 'config/arm9/overlays/ov005/symbols.txt').read_text()
    if not re.search('kind:function\\(arm,size=0xc\\) addr:0x021e0a84', overlayConfig):
        raise ValueError('787 overlay getter boundary differs')
    ranges[35523204] = (35523216, 'arm')
    text = (ROOT / 'asm/_dsd_gap@main_3.s').read_text()
    lines = {}
    for address in ANIMATION:
        start = text.index('    arm_func_start func_' + f'{address:08x}')
        end = text.index('    arm_func_end func_' + f'{address:08x}', start)
        pc = address
        for line in text[start:end].splitlines()[1:]:
            line = line.split(';')[0].strip()
            if ':' in line:
                line = line.split(':', 1)[1].strip()
            if not line:
                continue
            if line.startswith('.'):
                if line.startswith('.word'):
                    pc += 4
                else:
                    raise ValueError(('787 unexpected animation assembly directive', line))
            else:
                lines[pc] = line
                pc += 4
        if pc != ranges[address][0]:
            raise ValueError('787 assembly/binary boundary differs')
    return (ranges, lines)

class Machine(BaseMachine):

    def __init__(self, main, overlay, images, providers, profile):
        self.extraRanges, self.assembly = ranges_and_lines()
        self.nativeFrames = []
        self.nativeCompletions = []
        self.nativeEntries = []
        self.returnCandidate = None
        self.actualExtraReturnInstructions = 0
        self.slotModels = []
        self.animationModels = []
        self.modelFailures = []
        self.r3StackReads = 0
        self.r3SemanticReads = []
        super().__init__(main, overlay, images, providers, profile)
        for address in NATIVE_EXTRA + [35523204]:
            self.providers.pop(address, None)
        self.providers[33782252] = 'arm'
        if struct.unpack_from('<2I', main, 268132) != (3818913792, 3778019102) or struct.unpack_from('<3I', main, 173620) != (3852402688, 3778019102, 34528952) or struct.unpack_from('<3I', overlay, 35523204 - 35484224) != (3852451840, 3778019100, 33728052):
            raise ValueError('787 zero-input constant helpers differ')
        self.u.mem_write(34528952, struct.pack('<8H', 0, profile['mask'], 0, 0, 0, 0, 0, 0))
        writeword(self.u, SLOT, OBJECT)
        self.u.mem_write(SLOT + 4, struct.pack('<hBB', 0, 37, 0))
        self.u.mem_write(35359457, b'U')
        self.u.mem_write(OBJECT, bytes(48))
        writeword(self.u, CONTROLLER, FRAME)
        writeword(self.u, CONTROLLER + 12, profile['branch'])
        writeword(self.u, CONTROLLER + 16, 0)
        writeword(self.u, CONTROLLER + 20, 4294963200 if profile['flags'] else 4096)
        self.u.mem_write(FRAME, struct.pack('<4H', 0, 0, 10, 0))
        self.animationInitial = bytes(self.u.mem_read(CONTROLLER, 48))

    def code(self, u, pc, width, data):
        if self.returnCandidate is not None:
            if pc == self.returnCandidate:
                self.actualExtraReturnInstructions += 1
            self.returnCandidate = None
        while self.nativeFrames and pc == self.nativeFrames[-1]['returnPc']:
            frame = self.nativeFrames.pop()
            if u.reg_read(UC_ARM_REG_SP) != frame['sp'] or [u.reg_read(r) for r in REGS[4:12]] != frame['preserved']:
                raise ValueError('787 original native frame differs')
            event = dict(address=hex(frame['address']), rawR0=u.reg_read(REGS[0]), actuallyReturned=True)
            if frame['address'] == 33941524:
                actual = bytes(u.mem_read(OBJECT + 28, 16))
                expected = struct.pack('<4I', self.profile['serviceWord'], 0, 0, 10)
                valid = frame['args'][:3] == [0, 0, 10] and u.reg_read(REGS[0]) == frame['oldValue'] and (u.mem_read(SLOT + 6, 1)[0] == 0) and (u.mem_read(35359457, 1)[0] == 0) and (actual == expected)
                self.slotModels.append(dict(incomingWords=frame['args'][:3], previousByte=frame['oldValue'], rawR0=u.reg_read(REGS[0]), finalCommandWords=list(struct.unpack('<4I', actual)), expectedCommandWords=list(struct.unpack('<4I', expected)), valid=valid))
                if not valid:
                    self.modelFailures.append('787 slot forwarding/input/actual command write model failed')
            if frame['address'] == 33770856:
                expected = bytearray(frame['before'])
                rate = struct.unpack_from('<i', expected, 20)[0]
                elapsed = struct.unpack_from('<I', expected, 16)[0]
                if struct.unpack_from('<I', expected, 12)[0] == 1:
                    elapsed = elapsed + abs(rate * frame['args'][1] + 2048 >> 12) & 4294967295
                    struct.pack_into('<I', expected, 16, elapsed)
                valid = u.reg_read(REGS[0]) == 0 and bytes(u.mem_read(CONTROLLER, 48)) == bytes(expected) and (elapsed < 10 * 4096)
                self.animationModels.append(dict(incomingWords=frame['args'], fieldC=struct.unpack_from('<I', frame['before'], 12)[0], field14=rate, field10Before=struct.unpack_from('<I', frame['before'], 16)[0], field10After=elapsed, actualR0=u.reg_read(REGS[0]), valid=valid))
                if not valid:
                    self.modelFailures.append('787 active/inactive no-advance field model failed')
            self.nativeCompletions.append(event)
        owner = next((a for a, (end, mode) in self.extraRanges.items() if a <= pc < end), None)
        if owner is not None:
            if u.reg_read(UC_ARM_REG_CPSR) & 32:
                raise ValueError('787 actual native target mode differs')
            self.instructions += 1
            if self.instructions > 100000:
                raise ValueError('787 native instruction bound')
            if pc == owner:
                args = [u.reg_read(r) for r in REGS[:4]]
                frame = dict(address=owner, args=args, returnPc=u.reg_read(UC_ARM_REG_LR) & ~1, sp=u.reg_read(UC_ARM_REG_SP), preserved=[u.reg_read(r) for r in REGS[4:12]])
                if owner == 33941524:
                    frame['oldValue'] = u.mem_read(SLOT + 6, 1)[0]
                if owner == 33770856:
                    frame['before'] = bytes(u.mem_read(CONTROLLER, 48))
                self.nativeFrames.append(frame)
                self.nativeEntries.append(dict(address=hex(owner), arguments=args))
            if owner in ANIMATION:
                line = self.assembly[pc]
                if re.search('\\br3\\b', line):
                    if line.startswith('stm') and 'sp!' in line:
                        self.r3StackReads += 1
                    elif not (line.startswith('ldm') and 'sp!' in line):
                        self.r3SemanticReads.append(dict(pc=hex(pc), instruction=line))
            word = struct.unpack('<I', u.mem_read(pc, 4))[0]
            if word & 268435455 == 19922718 or (word >> 25 & 7 == 4 and word & 1 << 20 and (word >> 16 & 15 == 13) and word & 32768):
                if self.nativeFrames:
                    self.returnCandidate = self.nativeFrames[-1]['returnPc']
            return
        super().code(u, pc, width, data)

    def run(self, entry, args=()):
        result = super().run(entry, args)
        if self.nativeFrames:
            raise ValueError('787 actual native chain did not complete')
        result.update(nativeEntries=self.nativeEntries, nativeCompletions=self.nativeCompletions, actualExtraReturnInstructions=self.actualExtraReturnInstructions, slotModels=self.slotModels, animationModels=self.animationModels, modelFailures=self.modelFailures, r3StackReads=self.r3StackReads, r3SemanticReads=self.r3SemanticReads)
        return result

def model(machine, result):
    known = base_model(machine, result)
    if result['modelFailures'] or result['r3SemanticReads']:
        raise ValueError(('787 original helper/liveness models failed', result['modelFailures'], result['r3SemanticReads']))
    return known
