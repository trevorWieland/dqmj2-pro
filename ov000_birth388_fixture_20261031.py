import struct
import match_runtime as c
from link_runtime_unit import measured_module
from probe_ov000_birth329_20261031 import BirthMachine,REGS,STACK,STOP,CAPS,inputs
import ov000_birth330_models_20261031 as B
from unicorn.arm_const import *
BASE,ENTRY,CONTEXT,VIEW,OUT,PAIR=0x02000000,0x0221B624,0x022460D4,0x02246090,0x02630000,0x02610000
SCRATCH,CHOICE,SPECIES,VARIANT,BONUS=0x022474C8,0x022463B0,0x022463DC,0x02246424,0x02246420
PROVIDED={0x0205E7A8:2,0x020273C8:0,0x020404F0:1,0x020407A8:0,0x0221E7E8:1,0x021EADD0:0,0x02220680:1,0x02220714:1,0x0221C8DC:6,0x02049008:5,0x020C48D0:3,0x020C48BC:0,0x020C48E8:1,0x0221FBB8:0,0x02221154:3,0x0221C000:1,0x02220278:0,0x0221EBF4:0,0x0221E6CC:2,0x020620E8:2,0x02041538:3,0x0204157C:1,0x020698F4:1,0x0206A04C:0,0x02068F60:1,0x0221C6E4:0,0x0206DCD0:1,0x021EAD88:2,0x020634CC:1}
WATCH={ENTRY,0x022207A0,0x022298EC,0x02229100,0x02221344,0x02221358,0x022212F0,0x022212B8,0x02220778,0x02062A10,0x02044CDC,0x0203D128,0x02063B40,0x0203D294,0x02008E0C,0x02048F7C,0x020C484C,0x0206BF44,*CAPS}


def profiles():
    rows=[]
    for phase in range(256):
        if phase not in[0,1,2,3,8,9,10,11]:rows.append(dict(phase=phase,action=0,option=0,policy=0,ready=0,scene=6,index=0,scratch33=phase,rawByte=phase,seed=388000+phase))
    for phase in[0,1,2,3,8,9,10,11]:
        for action in[0,1,2,3]:
            for variant in range(4):rows.append(dict(phase=phase,action=action,option=variant&1,policy=(variant>>1)&1,ready=[-1,0,1,2][variant],scene=6 if variant&1 else 0,index=0,scratch33=[0,1,127,255][variant],rawByte=[0,127,128,255][variant],seed=388300+len(rows)))
    for category in[False,True]:
        for feature in[0,1]:
            for level in[9,10]:
                for option in[0,1]:rows.append(dict(phase=1,action=3,option=option,policy=1,ready=0,scene=6,index=0,scratch33=255,rawByte=255,seed=389000+len(rows),categoryTwo=category,feature=feature,level=level))
    for action in[0,1,2,3]:rows.append(dict(phase=10,action=action,option=0,policy=1,ready=0,menu=2,scene=6,index=0,scratch33=127,rawByte=128,seed=389400+len(rows)))
    for alias in['phase','action']:
        for phase in[0,1,3,8,9,10,11,255]:rows.append(dict(phase=phase,action=1,option=1,policy=1,ready=1,scene=6,index=0,scratch33=127,rawByte=128,seed=389500+len(rows),outAlias=alias))
    return rows


class Machine(BirthMachine):
    def __init__(self,arm,save,assets,overlay,p,body=None):
        self.profile=p;self.assetsInput=assets;self.outAddress=CONTEXT+16 if p.get('outAlias')=='phase'else CONTEXT if p.get('outAlias')=='action'else OUT;self.subjectEnd=ENTRY+(len(body)if body is not None else 1244);self.builderChecks=[];self.scratch33Writes=[];self.targetObserved=set()
        super().__init__(arm,save,assets,overlay,p['seed'])
        self.providers={entry:self.provider for entry in PROVIDED}
        if body is not None:self.u.mem_write(ENTRY,body)
        self.u.mem_write(CONTEXT,bytes(32));self.word(CONTEXT,p['action']);self.u.mem_write(CONTEXT+16,bytes([p['phase']]))
        self.u.mem_write(VIEW,bytes(64));self.word(VIEW+32,p['option']);self.u.mem_write(VIEW+7,bytes([0x7E]))
        self.word(OUT,0xDA388BAD)
        rows=[save[0x1E8+i*132:0x1E8+(i+1)*132]for i in range(100)]
        chosen=[r for r in rows if B.word(r,20,4)][:2]
        self.parents=chosen;self.u.mem_write(PAIR,b''.join(chosen));self.word(CHOICE+28,PAIR);self.u.mem_write(CHOICE+3,bytes([p['index']]))
        payload=assets['EnmyKindTbl.bin'][8:]
        species=B.word(chosen[0],24,2)
        if p.get('categoryTwo'):
            species=next(i for i in range(len(payload)//100)if((B.word(payload,100*i+4,2)>>8)&15)//3==2)
        self.species=species
        for side in range(2):
            address=self.record(B.word(chosen[side],20,4));self.u.mem_write(address+48,bytes([p.get('level',10)]));self.u.mem_write(PAIR+132*side+48,bytes([p.get('level',10)]))
        for index in range(8):
            self.u.mem_write(SPECIES+index*2,struct.pack('<h',species));self.u.mem_write(VARIANT+index,bytes([0]));self.u.mem_write(BONUS+index,bytes([0]))
        self.u.mem_write(SCRATCH+51,bytes([p['scratch33']]))
        getter=arm[0x48F88:0x48F8C];setter=arm[0xC4858:0xC485C]
        self.rawArray=int.from_bytes(getter,'little');self.rawState=int.from_bytes(setter,'little')
        self.u.mem_write(self.rawArray+1,bytes([p['rawByte']]));self.u.mem_write(self.rawState+1,bytes([0x69]))
        flagbase=int.from_bytes(arm[0x63B5C:0x63B60],'little');self.flagbase=flagbase
        self.word(flagbase,(self.read_word(flagbase)&~0x10000)|(0x10000 if p.get('feature',p['policy'])else 0))
        self.before=bytes(self.u.mem_read(BASE,0x800000))
    def provider(self,obj,args):
        entry=self.currentEntry
        if entry in[0x02220680,0x02220714]:return self.profile['policy']
        if entry in[0x0221FBB8,0x02220278,0x0221EBF4,0x020698F4]:return self.profile['ready']&0xFFFFFFFF
        if entry==0x0206A04C:return self.profile.get('menu',self.profile['ready'])&0xFFFFFFFF
        if entry==0x020273C8:return self.profile['scene']
        if entry==0x020634CC:return 0xABC000+self.seed
        return 0
    def write(self,uc,access,address,size,value,data):
        if not BASE<=address<=address+size<=BASE+0x800000 and not 0x04000280<=address<=address+size<=0x040002C0:raise ValueError(('Birth388 write outside supportedRAM',hex(address)))
        if ENTRY<address+size and address<self.subjectEnd:raise ValueError('Birth388 self-modifying subject')
        if address<=SCRATCH+51<address+size:self.scratch33Writes.append(dict(pc=hex(uc.reg_read(UC_ARM_REG_PC)),address=hex(address),size=size,value=value))
        if not STACK-0x10000<=address<STACK+0x1000:self.writes.append([hex(address),size,value])
    def close_returns(self,uc,address):
        while self.frames and address==self.frames[-1]['returnAddress']and uc.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            frame=self.frames.pop()
            if [uc.reg_read(r)for r in REGS[4:12]]!=frame['preserved']or bool(uc.reg_read(UC_ARM_REG_CPSR)&0x20)!=frame['returnThumb']:raise ValueError('Birth388 native preserved registers differ')
            result=uc.reg_read(UC_ARM_REG_R0)
            self.returned.append(dict(entry=hex(frame['entry']),result=result,actualReturn=True,tailAliases=frame.get('tailAliases',[])))
            if frame['entry']==0x02229100:
                before,args,pointers,parents=frame['builder']
                expected,caps=B.model(before,args,pointers,parents,self.assets,self.seed)
                after=bytes(uc.mem_read(BASE,0x800000));cut=STACK-0x10000-BASE;end=STACK+0x1000-BASE
                if after[:cut]!=expected[:cut]or after[end:]!=expected[end:]or result!=SCRATCH:raise ValueError('Birth388 independent nested builder model differs')
                self.builderChecks.append(dict(returnPointer=result,scratch33=after[SCRATCH-BASE+51],independentFullNonstackRam=True,caps=list(caps)))
    def observe(self,uc,address,size,data):
        self.steps+=1;self.close_returns(uc,address)
        if ENTRY<=address<self.subjectEnd:self.targetObserved.update(range(address-ENTRY,address-ENTRY+size))
        if address!=ENTRY and ENTRY<=address<self.subjectEnd:return
        if address in WATCH or address in self.providers:
            sp=uc.reg_read(UC_ARM_REG_SP);args=[uc.reg_read(r)for r in REGS[:4]];stack=list(struct.unpack('<II',uc.mem_read(sp,8)))
            self.trace.append(dict(entry=hex(address),arguments=args,stackWords=stack,provider=address in self.providers,sp=hex(sp)))
            if address in WATCH and address not in self.providers:
                frame=dict(entry=address,returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),sp=sp,preserved=[uc.reg_read(r)for r in REGS[4:12]])
                if address==0x02229100:
                    pointers=[self.record(uid)for uid in args[:2]];parents=[bytes(uc.mem_read(p,132))for p in pointers]
                    frame['builder']=(bytes(uc.mem_read(BASE,0x800000)),args+[stack[0]],pointers,parents)
                if self.frames and all(frame[k]==self.frames[-1][k]for k in['returnAddress','returnThumb','sp','preserved']):self.frames[-1].setdefault('tailAliases',[]).append(hex(address))
                else:self.frames.append(frame)
            if address in self.providers:
                self.currentEntry=address;result=self.providers[address](self,args)
                uc.reg_write(UC_ARM_REG_R0,result&0xFFFFFFFF)
                for index in[1,2,3,12]:uc.reg_write(REGS[index],0xAB388000+index)
                uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def record(self,uid):
        return next(0x021BD674+132*i for i in range(100)if self.read_word(0x021BD674+132*i+20)==uid)
    def run(self):
        self.assets=self.assetsInput
        self.u.mem_write(STACK-0x10000,bytes(0x11000));self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xA0388000+i*0x100 for i in range(13)]
        for register,value in zip(REGS,values):self.u.reg_write(register,value)
        self.u.reg_write(UC_ARM_REG_R0,self.outAddress);self.u.reg_write(UC_ARM_REG_SP,STACK);self.u.reg_write(UC_ARM_REG_LR,STOP)
        self.trace,self.writes,self.returned,self.frames=[],[],[],[]
        self.u.emu_start(ENTRY,STOP,count=500000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or self.frames or[self.u.reg_read(r)for r in REGS[4:12]]!=values[4:12]:raise ValueError('Birth388 top actual return/frame differs')
        after=bytes(self.u.mem_read(BASE,0x800000));cut=STACK-0x10000-BASE;end=STACK+0x1000-BASE
        return dict(profile=self.profile,returnWord=self.u.reg_read(UC_ARM_REG_R0),outWord=self.read_word(self.outAddress),actualReturns=1,nativeDependencyActualReturns=len(self.returned)-1,providedCalls=sum(row['provider']for row in self.trace),nonstackSha256=c.sha(after[:cut]+after[end:]),trace=self.trace,nativeReturns=self.returned,writes=self.writes,scratch33Writes=self.scratch33Writes,scratch33Before=self.profile['scratch33'],scratch33After=after[SCRATCH-BASE+51],builderChecks=self.builderChecks,steps=self.steps,observedCodeBytes=sorted(self.targetObserved))
