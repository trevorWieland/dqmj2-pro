import gc
import re
import struct
import match_runtime
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_JUMP, CS_GRP_CALL
BASE, OVERLAY, STACK, STOP = 0x02000000, 0x021D7240, 0x027F0000, 0x027FF800
ACTOR, DESCRIPTOR, DELTA, TABLE = 0x02700000, 0x02701000, 0x02702000, 0x02600000
ROSTER = 0x021BD674
ENTRY, SIZE, OUTPUT, FLAGS, RNG = 0x021DA9E4, 1720, 0x02600000, 0x020F60EE, 0x020F6044
PROVIDERS = set()
UNSUPPORTED = set()
SUBJECTS = {ENTRY: SIZE}
OBJECTS=[0x021E9EA8,0x021E9CF8,0x021E9BD8,0x021E9B48,0x021E9AB8,0x021E9A28]+[base+i*0x90 for base in[0x021EA298,0x021EA0E8,0x021E9F38]for i in range(3)]
LIMITS = []
RNG_ENTRY = 0x0203D294
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]

def inputs():
    metadata, arm, symbols = measured_module('main')
    module, overlay, overlaySymbols = measured_module('ov005')
    functions = {}
    for name, text in [('main', symbols), ('ov005', overlaySymbols)]:
        for line in text.splitlines():
            found = re.search(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', line)
            if found:
                functions[int(found[3], 0)] = dict(module=name, mode=found[1], bytes=int(found[2], 0))
    decoder=Cs(CS_ARCH_ARM,CS_MODE_ARM)
    calls={}
    for ins in decoder.disasm(overlay[ENTRY-OVERLAY:ENTRY-OVERLAY+SIZE],ENTRY):
        if ins.mnemonic in ['bl','blx']and ins.op_str.startswith('#0x'):
            target=int(ins.op_str[1:],0)&~1
            calls[target]=functions[target]
    return dict(main=metadata,module=module,arm=arm,overlay=overlay,ranges={ENTRY:functions[ENTRY]},providers=calls)

class Machine:
    def __init__(self, original, profile, body=None):
        self.i,self.p,self.entry=original,profile,ENTRY
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(BASE,0x800000)
        self.u.mem_write(BASE,original['arm'])
        self.u.mem_write(OVERLAY,original['overlay'])
        self.u.mem_map(0x04000000,0x1000)
        self.u.mem_map(0x06000000,0x80000)
        self.extent=len(body)if body is not None else SIZE
        if body is not None:self.u.mem_write(ENTRY,body)
        self.frames,self.returns,self.calls,self.observed=[],[],[],set()
        self.events,self.helperWords,self.writes=[],[],[]
        self.instructions=0
        self.u.mem_write(0x04000000,bytes([profile['ioByte']])*0x1000)
        self.u.mem_write(0x06000000,bytes([0xA5])*0x80000)
        self.u.mem_write(0x021E9818,bytes([0xA5])*0x80)
        self.word(0x021E986C,0x02600000)
        for index,address in enumerate(OBJECTS):
            self.u.mem_write(address,bytes([profile['objectByte']])*0x90)
            self.word(address+0x7C,(profile['flags']+index*0x10203)&0xFFFFFFFF)
        self.ioBefore=bytes(self.u.mem_read(0x04000000,0x1000))
        self.vramBefore=bytes(self.u.mem_read(0x06000000,0x80000))
        self.strings,self.loads,self.sizes=0,0,0
        self.before=bytes(self.u.mem_read(BASE,0x800000))
        self.initial=[0xA0770000+index*0x100 for index in range(13)]
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        for reg,value in zip(REGS,self.initial):self.u.reg_write(reg,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK)
        self.u.reg_write(UC_ARM_REG_LR,STOP)
        self.u.hook_add(UC_HOOK_CODE,self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE,self.observe_write)

    def byte(self, a, v):
        self.u.mem_write(a, bytes([v & 255]))

    def half(self, a, v):
        self.u.mem_write(a, struct.pack('<H', v & 65535))

    def word(self, a, v):
        self.u.mem_write(a, struct.pack('<I', v & 0xFFFFFFFF))

    def observe_write(self,u,access,address,size,value,data):
        if not STACK-65536<=address<STACK+4096:self.writes.append([address,size,value&((1<<(8*size))-1)])

    def observe(self, u, a, length, data):
        self.instructions += 1
        while self.frames and a == self.frames[-1]['lr'] & ~1 and u.reg_read(UC_ARM_REG_SP) == self.frames[-1]['sp']:
            frame = self.frames.pop()
            if [u.reg_read(r) for r in REGS[4:12]] != frame['preserved'] or bool(u.reg_read(UC_ARM_REG_CPSR) & 32) != bool(frame['lr'] & 1):
                raise ValueError('509 native frame differs')
            self.returns.append(dict(entry=frame['entry'], aliases=frame['aliases'], returnedR0=u.reg_read(UC_ARM_REG_R0)))
        if a in UNSUPPORTED:
            raise ValueError('509 live-entry heap path is unsupported')
        if a in self.i['providers']:
            words=[u.reg_read(r)for r in REGS[:4]]
            self.events.append(dict(address=a,rawCallerWords=words))
            if bool(u.reg_read(UC_ARM_REG_CPSR)&32)!=(self.i['providers'][a]['mode']=='thumb'):raise ValueError('509 provider mode differs')
            value=0
            if a==0x02008C58:
                if words[0]!=0 or(words[1]!=0x06000000 and words[1]not in OBJECTS)or words[2]!=(0x80000 if words[1]==0x06000000 else 4):raise ValueError('509 supplied clear range differs')
                u.mem_write(words[1],bytes(words[2]))
            if a==0x0201D444:
                if words[0]!=STACK-72:raise ValueError('509 native32-byte descriptor address differs')
                content=struct.pack('<8I',self.strings,words[1],self.p['sizes'][self.strings],0xD0000000+self.strings,0,0,0,0)
                u.mem_write(words[0],content);self.strings+=1
            if a==0x0203CC2C:
                if words[:2]!=[STACK-72,2]:raise ValueError('509 descriptor load words differ')
                value=0x02610000+self.loads*0x1000;self.loads+=1
            if a==0x0202A8E0:
                if words[0]!=STACK-72:raise ValueError('509 size descriptor address differs')
                value=self.p['sizes'][self.sizes];self.sizes+=1
            if a==0x021DDF24:value=self.p['returnWord']
            u.reg_write(UC_ARM_REG_R0,value&0xFFFFFFFF)
            for reg,number in zip([UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R12],[1,2,3,12]):u.reg_write(reg,0xDE000000|len(self.events)<<8|number)
            u.reg_write(UC_ARM_REG_PC,u.reg_read(UC_ARM_REG_LR))
            return
        if self.entry <= a < self.entry + self.extent:
            self.observed.add(a)
            return
        if ENTRY<=a<ENTRY+SIZE:raise ValueError('509 escaped substituted own extent')
        if a in self.i['ranges']:
            frame = dict(entry=a, sp=u.reg_read(UC_ARM_REG_SP), lr=u.reg_read(UC_ARM_REG_LR), preserved=[u.reg_read(r) for r in REGS[4:12]], aliases=[])
            if self.frames and frame['sp'] == self.frames[-1]['sp'] and frame['lr'] == self.frames[-1]['lr']:
                self.frames[-1]['aliases'].append(a)
            else:
                self.frames.append(frame)
            if bool(u.reg_read(UC_ARM_REG_CPSR) & 32) != (self.i['ranges'][a]['mode'] == 'thumb'):
                raise ValueError('509 wrong native mode')
            if a == RNG_ENTRY:
                self.calls.append(dict(bound=u.reg_read(UC_ARM_REG_R0), stateBefore=struct.unpack('<I', bytes(u.mem_read(RNG, 4)))[0]))
        if not any(start <= a < start + row['bytes'] for start, row in self.i['ranges'].items()):
            raise ValueError(('509 unexpected PC', hex(a)))

    def run(self):
        self.u.emu_start(self.entry, STOP, count=20000)
        if self.u.reg_read(UC_ARM_REG_PC) != STOP or self.u.reg_read(UC_ARM_REG_SP) != STACK or self.u.reg_read(UC_ARM_REG_CPSR) & 63 != 16 or [self.u.reg_read(r) for r in REGS[4:12]] != self.initial[4:12] or self.frames:
            raise ValueError('509 top return/frame failed')
        if bytes(self.u.mem_read(self.entry,self.extent))!=self.before[self.entry-BASE:self.entry-BASE+self.extent]:raise ValueError('509 own source image changed')
        result = dict(profile=self.p, entry=self.entry, before=self.before, after=bytes(self.u.mem_read(BASE, 0x800000)), calls=self.calls, nativeReturns=self.returns, ownObserved=sorted(self.observed), providedEvents=self.events, helperWords=self.helperWords, nonstackWrites=self.writes, ioBefore=self.ioBefore, ioAfter=bytes(self.u.mem_read(0x04000000,0x1000)), vramBefore=self.vramBefore,vramAfter=bytes(self.u.mem_read(0x06000000,0x80000)),strings=self.strings,loads=self.loads,sizes=self.sizes, instructions=self.instructions, returnedR0=self.u.reg_read(UC_ARM_REG_R0))
        self.u = None
        gc.collect()
        return result
