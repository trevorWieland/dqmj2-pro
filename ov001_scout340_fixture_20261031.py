import hashlib
import random
import struct
import match_runtime
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ_UNMAPPED,UC_ERR_READ_UNMAPPED,UcError
from unicorn.arm_const import *
ENTRY,CTX,TEMPLATE,SLOT=0x021F9608,0x02239A14,0x02239ABC,0x0222ED29
FLAG,PARAM,STACK,STOP=0x020F69E4,0x02460000,0x027F0000,0x027FF800
REGS=[UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_R12]
NATIVE={0x021DB438:124,0x02044424:48,0x02008D78:148}
PROVIDERS={0x021F1294:[16,2],0x0202AC08:[0x02239A8C],0x02063C00:[13,1]}

def encoded(value):
    import json
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def sha(raw):return hashlib.sha256(raw).hexdigest()

def recipes():
    result=[]
    for slot in range(3):
        for bonus in[False,True]:
            for raw in range(256):
                result.append(dict(slot=slot,
                        bonus=bonus,
                        raw=raw,
                        alias=False,
                        seed=340000+len(result),
                        invalid=False))
            for raw in[0,1,127,128,255]:
                result.append(dict(slot=slot,
                        bonus=bonus,
                        raw=raw,
                        alias=True,
                        seed=340000+len(result),
                        invalid=False))
    for slot in range(3,256):
        result.append(dict(slot=slot,bonus=False,raw=93,alias=False,seed=340000+len(result),invalid=True))
    return result

class Machine:
    def __init__(self,main,overlay,recipe,body=None):
        self.recipe=recipe
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        self.u.mem_map(0x02000000,0x800000)
        self.u.mem_write(0x02000000,main)
        self.u.mem_write(0x021D7240,overlay)
        if body is not None:self.u.mem_write(ENTRY,body)
        rng=random.Random(recipe['seed'])
        self.u.mem_write(CTX,rng.randbytes(0x200))
        self.u.mem_write(SLOT,bytes([recipe['slot']]))
        flag=(rng.getrandbits(32)&~0x40000)|(0x40000 if recipe['bonus']else 0)
        self.u.mem_write(FLAG,struct.pack('<I',flag))
        self.actor=0x022362AC+(recipe['slot']if recipe['slot']<3 else 0)*0x440
        parameter=CTX+0x26-0xB0 if recipe['alias']else PARAM
        self.u.mem_write(self.actor+0x1E8,struct.pack('<I',parameter))
        self.u.mem_write(parameter+0xB0,bytes([recipe['raw']]))
        self.frames,self.trace,self.returns,self.writes,self.invalid=[],[],[],[],[]
        self.observed=set()
        self.steps=0
        self.u.hook_add(UC_HOOK_CODE,self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
        self.u.hook_add(UC_HOOK_MEM_READ_UNMAPPED,self.unmapped)
    def unmapped(self,uc,access,address,size,value,data):
        self.invalid.append(dict(address=hex(address),bytes=size))
        return False
    def write(self,uc,access,address,size,value,data):
        if not STACK-0x10000<=address<STACK:self.writes.append([hex(address),size,value])
    def close(self,address):
        while self.frames and address==self.frames[-1]['returnAddress']and self.u.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            frame=self.frames.pop()
            if[self.u.reg_read(r)for r in REGS[4:12]]!=frame['preserved']or bool(self.u.reg_read(UC_ARM_REG_CPSR)&0x20)!=frame['thumb']:
                raise ValueError('Scout340 native return registers/mode differ')
            self.returns.append(dict(address=hex(frame['entry']),
                    actualReturn=True,
                    result=self.u.reg_read(UC_ARM_REG_R0)))
    def observe(self,uc,address,size,data):
        self.steps+=1
        self.close(address)
        if ENTRY<=address<ENTRY+156:self.observed.update(range(address,address+size))
        if address in NATIVE or address==ENTRY or address in PROVIDERS:
            args=[uc.reg_read(r)for r in REGS[:4]]
            event=dict(address=hex(address),
                arguments=args,
                provider=address in PROVIDERS,
                sp=hex(uc.reg_read(UC_ARM_REG_SP)))
            self.trace.append(event)
            if address in PROVIDERS:
                expected=PROVIDERS[address]
                if args[:len(expected)]!=expected:raise ValueError('Scout340 provided arguments differ')
                seed=self.recipe['seed']
                for index in[0,1,2,3,12]:uc.reg_write(REGS[index],(0xA3400000+index+seed)&0xFFFFFFFF)
                uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
            else:
                self.frames.append(dict(entry=address,
                        returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,
                        thumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),
                        sp=uc.reg_read(UC_ARM_REG_SP),
                        preserved=[uc.reg_read(r)for r in REGS[4:12]]))
    def run(self):
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xBC400000+i*0x100 for i in range(len(REGS))]
        for register,value in zip(REGS,values):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_SP,STACK)
        self.u.reg_write(UC_ARM_REG_LR,STOP)
        before=bytes(self.u.mem_read(0x02000000,0x800000))
        error=None
        try:self.u.emu_start(ENTRY,STOP,count=3000)
        except UcError as e:
            if e.errno!=UC_ERR_READ_UNMAPPED:raise
            error='UC_ERR_READ_UNMAPPED'
        self.close(self.u.reg_read(UC_ARM_REG_PC))
        expected=bytearray(before)
        offset=CTX-0x02000000
        pointer=0 if self.recipe['invalid']else self.actor
        expected[offset+0x40:offset+0x44]=struct.pack('<I',pointer)
        signed=self.recipe['raw']-256 if self.recipe['raw']>=128 else self.recipe['raw']
        value=(0 if self.recipe['alias']else signed)*10+(400 if self.recipe['bonus']else 0)
        expected[offset+0x26:offset+0x28]=struct.pack('<h',0 if self.recipe['invalid']else value)
        if not self.recipe['invalid']:
            expected[TEMPLATE-0x02000000:TEMPLATE-0x02000000+132]=bytes(132)
            expected[offset+0xA]=1
        after=bytes(self.u.mem_read(0x02000000,0x800000))
        lo,hi=STACK-0x10000-0x02000000,STACK+0x1000-0x02000000
        if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]:raise ValueError('Scout340 complete independent nonstack RAM differs')
        if self.recipe['invalid']:
            if error!='UC_ERR_READ_UNMAPPED'or self.invalid!=[dict(address='0x1e8',
                    bytes=4)]or len(self.frames)!=1 or self.u.reg_read(UC_ARM_REG_PC)!=0x021F9640:
                raise ValueError('Scout340 unsupported state observation differs')
            actual=0
        else:
            if error or self.frames or self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in REGS[4:12]]!=values[4:12]or self.u.reg_read(UC_ARM_REG_R0)!=0:
                raise ValueError('Scout340 actual return/frame differs')
            actual=1
        resolver=[r for r in self.trace if r['address']=='0x21db438']
        wanted_slot=self.recipe['slot']if self.recipe['slot']<128 else self.recipe['slot']-256
        if len(resolver)!=1 or resolver[0]['arguments'][:2]!=[1,
            wanted_slot&0xFFFFFFFF]:raise ValueError('Scout340 actual resolver signed input differs')
        expected_order=[0x021F1294,
            0x0202AC08,
            0x021DB438]+([]if self.recipe['invalid']else[0x02044424,
                0x02008D78,
                0x02063C00])
        if[int(r['address'],
                0)for r in self.trace[1:]]!=expected_order:raise ValueError('Scout340 native/provided call order differs')
        return dict(actualReturns=actual,
            unsupportedInvalidReads=len(self.invalid),
            nativeDependencyActualReturns=sum(int(r['address'],
                    0)in NATIVE for r in self.returns),
            providedCalls=sum(r['provider']for r in self.trace),
            instructions=self.steps,
            trace=self.trace,
            returns=self.returns,
            writes=self.writes,
            invalid=self.invalid,
            observedCallerBytes=sorted(self.observed),
            ramSha256=sha(after),
            stackSha256=sha(after[lo:hi]),
            flagWord=int.from_bytes(before[FLAG-0x02000000:FLAG-0x02000000+4],
                'little'),
            expectedSignedField26=value if not self.recipe['invalid']else 0,
            rawTemplateReady=after[TEMPLATE+0x67-0x02000000])

def execute(main,overlay,recipe,body=None):return Machine(main,overlay,recipe,body).run()
