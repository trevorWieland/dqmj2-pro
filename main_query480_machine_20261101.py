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
ENTRY, SIZE, OUTPUT, FLAGS, RNG = 0x02039208,132,0x02608000,0x020F4C44,0x020F6044
PROVIDERS = {0x0203928C,0x02039458}
UNSUPPORTED = set()
SUBJECTS = {ENTRY: SIZE}
LIMITS = []
RNG_ENTRY = 0x0203D294
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]

def inputs():
    metadata, arm, symbols = measured_module('main')
    module,overlay,overlaySymbols=metadata,b'', ''
    functions = {}
    for name, text in [('main', symbols), ('unused', overlaySymbols)]:
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
    return dict(main=metadata,module=module,arm=arm,overlay=overlay,ranges=ranges,tableObject=tableObject,modeObject=modeObject)

class Machine:
    def __init__(self,original,profile,body=None):
        self.i,self.p,self.entry=original,profile,ENTRY
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE,0x800000)
        self.u.mem_write(BASE,original['arm'])
        self.extent=len(body)if body is not None else SIZE
        if body is not None:self.u.mem_write(ENTRY,body)
        self.frames,self.returns,self.calls,self.observed=[],[],[],set()
        self.events,self.freeWords=[],[]
        self.instructions=0
        self.lastPc=None
        self.word(FLAGS,0x02600000)
        self.u.mem_write(0x02600000,bytes(0x100))
        self.u.mem_write(0x02601000,bytes(0x1000))
        self.u.mem_write(0x02603000,bytes(0x1000))
        self.word(0x02600084,0x02603000)
        self.word(0x0260008C,0x02601000)
        self.word(0x02601008,0 if profile['lookup']=='no-table'else 0x100)
        self.word(0x02601100,0 if profile['lookup']=='count0'else 3)
        for index in range(3):
            self.word(0x02601104+index*4,0 if profile['lookup']=='empty-row'else 0x200+index*0x20)
            self.word(0x02601200+index*0x20,profile['objectIndex'])
            self.half(0x02601204+index*0x20,profile['type'])
        self.word(0x02603008,3)
        for index,value in enumerate(profile['cached']):self.word(0x02603014+index*16,value)
        self.word(OUTPUT,0xA5A5A5A5)
        self.out=0 if profile['out']=='null'else 0x02601200 if profile['out']=='row'else 0x02603014 if profile['out']=='cache'else OUTPUT
        self.word(STACK,self.out)
        self.before=bytes(self.u.mem_read(BASE,0x800000))
        self.initial=[0xA0800000+index*0x100 for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        for reg,value in zip(REGS[:4],[profile['handle'],profile['flags'],profile['arg2'],profile['arg3']]):self.u.reg_write(reg,value&0xFFFFFFFF)
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
        previous=self.lastPc
        self.lastPc=a
        while self.frames and a == self.frames[-1]['lr'] & ~1 and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(r) for r in REGS[4:12]] != frame['preserved'] or bool(u.reg_read(UC_ARM_REG_CPSR) & 32) != bool(frame['lr'] & 1):
                raise ValueError('480 native frame differs')
            self.returns.append(dict(entry=frame['entry'], aliases=frame['aliases'], returnedR0=u.reg_read(UC_ARM_REG_R0)))
        if a in UNSUPPORTED:
            raise ValueError('480 live-entry heap path is unsupported')
        if a in PROVIDERS and self.entry <= a < self.entry+self.extent:
            incoming=False
            if previous is not None:
                opcode=struct.unpack('<I',bytes(u.mem_read(previous,4)))[0]
                delta=opcode&0xFFFFFF
                if delta&0x800000:delta-=0x1000000
                incoming=(opcode&0x0F000000)==0x0B000000 and previous+8+delta*4==a and u.reg_read(UC_ARM_REG_LR)==previous+4
            if not incoming:
                self.observed.add(a)
                return
        if a in PROVIDERS:
            words=[u.reg_read(r)for r in REGS[:4]]+[struct.unpack('<I',bytes(u.mem_read(u.reg_read(UC_ARM_REG_SP),4)))[0]]
            self.events.append(dict(address=a,rawCallerWords=words))
            value=self.p['validation'] if a==0x0203928C else self.p['created']
            if a==0x0203928C and self.p['mutate']:
                for index in range(3):self.word(0x02601200+index*0x20,self.p['newIndex'])
            u.reg_write(UC_ARM_REG_R0,value)
            for reg,number in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE000000|len(self.events)<<8|number)
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            return
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
                raise ValueError('480 wrong native mode')
            if a == RNG_ENTRY:
                self.calls.append(dict(bound=u.reg_read(UC_ARM_REG_R0), stateBefore=struct.unpack('<I', bytes(u.mem_read(RNG, 4)))[0]))
        if not any(start <= a < start + row['bytes'] for start, row in self.i['ranges'].items()):
            raise ValueError(('480 unexpected PC', hex(a)))

    def run(self):
        self.u.emu_start(self.entry, STOP, count=20000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(r) for r in REGS[4:12]] != self.initial[4:12] or self.frames:
            raise ValueError('480 top return/frame failed')
        result = dict(profile=self.p, entry=self.entry, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), calls=self.calls, nativeReturns=self.returns, ownObserved=sorted(self.observed), providedEvents=self.events, freePreparedWords=self.freeWords, outputPointer=self.out, instructions=self.instructions, returnedR0=self.u.reg_read(UC_ARM_REG_R0))
        self.u = None
        gc.collect()
        return result
