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
ENTRY, SIZE, OUTPUT, FLAGS, RNG = 0x021DE9F0, 72, 0x02600000, 0x020F60EE, 0x020F6044
PROVIDERS = {0x020875B4,0x020470E4,0x0205DC70,0x027FE400}
UNSUPPORTED = set()
SUBJECTS = {ENTRY: SIZE}
LIMITS = []
RNG_ENTRY = 0x0203D294
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]

def inputs():
    metadata, arm, symbols = measured_module('main')
    module, overlay, overlaySymbols = measured_module('ov003')
    functions = {}
    for name, text in [('main', symbols), ('ov003', overlaySymbols)]:
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
        if a in PROVIDERS or a in UNSUPPORTED:
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
    holderBase=struct.unpack_from('<I',arm,0x02049AE0-BASE)[0]
    return dict(main=metadata,module=module,arm=arm,overlay=overlay,ranges=ranges,tableObject=tableObject,modeObject=modeObject,holderBase=holderBase)

class Machine:
    def __init__(self, original, profile, body=None):
        self.i,self.p,self.entry=original,profile,ENTRY
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE,0x800000)
        self.u.mem_write(BASE,original['arm'])
        self.u.mem_write(OVERLAY,original['overlay'])
        self.extent=len(body)if body is not None else SIZE
        if body is not None:self.u.mem_write(ENTRY,body)
        self.frames,self.returns,self.calls,self.observed=[],[],[],set()
        self.events,self.freeWords,self.setterWords=[],[],[]
        self.instructions=0
        self.holder=original['holderBase']+profile['index']*12
        self.word(self.holder,0x02600000)
        self.u.mem_write(0x02600000,bytes(0x100))
        self.u.mem_write(0x02600400,bytes(0x100))
        self.word(0x02600004,0x02601000)
        self.word(0x02600008,0x02601400)
        self.word(0x02600404,0x02601400)
        for number,resource in enumerate([0x02601000,0x02601400]):
            virtual=0x02602000+number*0x100
            self.u.mem_write(resource,bytes([0xA5])*0x100)
            self.u.mem_write(virtual,bytes(0x40))
            self.word(resource+0x44,virtual)
            self.word(virtual+0x14,0x02603000)
            self.word(0x02603004,0x027FE400)
            self.word(resource+0x58,profile['texture'])
            for offset,value in zip([0x5D,0x5E,0x5F,0x5C],profile['bytes']):self.byte(resource+offset,value)
            self.word(resource+0x64,0x02605000 if profile['cache'] else 0)
            self.word(resource+0x18,profile['flags'])
            self.word(resource+0x0C,profile['oldState'])
        self.word(STACK,profile['stackWord'])
        self.before=bytes(self.u.mem_read(BASE,0x800000))
        self.initial=[0xA0770000+index*0x100 for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        for reg,value in zip(REGS[:4],[profile['index']]+profile['words']):self.u.reg_write(reg,value&0xFFFFFFFF)
        self.u.reg_write(UC_ARM_REG_SP,STACK)
        self.u.reg_write(UC_ARM_REG_LR,STOP)
        self.u.hook_add(UC_HOOK_CODE,self.observe)

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
                raise ValueError('477 native frame differs')
            self.returns.append(dict(entry=frame['entry'], aliases=frame['aliases'], returnedR0=u.reg_read(UC_ARM_REG_R0)))
        if a in UNSUPPORTED:
            raise ValueError('477 live-entry heap path is unsupported')
        if a in PROVIDERS:
            words=[u.reg_read(r)for r in REGS[:4]]
            if a==0x020875B4:words+=list(struct.unpack('<2I',bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP),8))))
            self.events.append(dict(address=a,rawCallerWords=words))
            counter=len(self.events)
            value=0x90000000|counter
            if a==0x020875B4 and self.p['mutate']:
                self.word(self.holder,0x02600400)
                self.word(0x02600004,0x02601400)
            if a==0x0205DC70:value=self.p['mapped']
            u.reg_write(UC_ARM_REG_R0,value)
            for reg,number in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE000000|counter<<8|number)
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            return
        if a==0x02085270:self.setterWords.append([u.reg_read(r)for r in REGS[:3]])
        if self.entry <= a < self.entry + self.extent:
            self.observed.add(a)
            return
        if a in self.i['ranges']:
            frame = dict(entry=a, sp=u.reg_read(UC_ARM_REG_SP), lr=u.reg_read(UC_ARM_REG_LR), preserved=[u.reg_read(r) for r in REGS[4:12]], aliases=[])
            if self.frames and frame['sp'] == self.frames[-1]['sp'] and frame['lr'] == self.frames[-1]['lr']:
                self.frames[-1]['aliases'].append(a)
            else:
                self.frames.append(frame)
            if bool(u.reg_read(UC_ARM_REG_CPSR) & 32) != (self.i['ranges'][a]['mode'] == 'thumb'):
                raise ValueError('477 wrong native mode')
            if a == RNG_ENTRY:
                self.calls.append(dict(bound=u.reg_read(UC_ARM_REG_R0), stateBefore=struct.unpack('<I', bytes(u.mem_read(RNG, 4)))[0]))
        if not any(start <= a < start + row['bytes'] for start, row in self.i['ranges'].items()):
            raise ValueError(('477 unexpected PC', hex(a)))

    def run(self):
        self.u.emu_start(self.entry, STOP, count=20000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(r) for r in REGS[4:12]] != self.initial[4:12] or self.frames:
            raise ValueError('477 top return/frame failed')
        result = dict(profile=self.p, entry=self.entry, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), calls=self.calls, nativeReturns=self.returns, ownObserved=sorted(self.observed), providedEvents=self.events, freePreparedWords=self.freeWords, setterWords=self.setterWords, holder=self.holder, instructions=self.instructions, returnedR0=self.u.reg_read(UC_ARM_REG_R0))
        self.u = None
        gc.collect()
        return result
