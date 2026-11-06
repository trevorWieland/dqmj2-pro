import struct
import match_runtime as c
import ov000_birth388_fixture_20261031 as F
from capstone import Cs,CS_ARCH_ARM,CS_MODE_ARM
from unicorn.arm_const import *
ENTRY=0x0221B070
NATIVE={0x02221344,0x02221358,0x022212F0,0x0222900C,0x0221F384,0x0207AA98,0x02062E44,0x020633C8,0x02063D7C,0x0222136C,0x02062B34,0x0222130C}
EXTRA_WATCH={0x0222900C,0x0222976C,0x0222985C,0x0206271C,0x020627A0,0x02062828,0x020628B0,0x02062980,0x02062A50,0x02062A88,0x02062D24,0x02062FD4,0x02063038,0x02063050,0x02063068,0x02063080,0x02063098,0x0221F384,0x0207AA98,0x02062E44,0x020633C8,0x02063D7C,0x0222136C,0x02062B34,0x0222130C}
UI_ARITY={0x0221CF14:0,0x0221CF60:0,0x02062378:0,0x0221FA70:2,0x02220160:2}


def profiles(save):
    result=[]
    def add(controller,**values):
        row=dict(phase=0,controller=controller,action=0,option=0,policy=0,ready=0,scene=6,index=0,scratch33=127,rawByte=128,seed=395000+len(result))
        row.update(values);result.append(row)
    known=[0,1,2,3,6,8,9,10,11]
    for controller in range(256):
        if controller not in known:add(controller)
    for phase in[0,1,255]:
        for count in[0,1,4,0xFFFFFFFF]:
            for option in[0,1]:add(0,phase=phase,listCount=count,option=option)
    for phase in[0,1,2,3,8,9,11,255]:
        for kind in[0,2,8,11]:
            for menu in[0,2,6,8,16]:add(1,phase=phase,kind=kind,menu=menu,option=(kind//2)&1,listCount=3)
    for phase in[0,1,2,3,8,9,11,255]:
        for menu in[2,6,16]:add(1,phase=phase,kind=8,menu=menu,option=1,listCount=3)
    for available in[0,1]:add(8,phase=3,menu=2,available=available)
    for controller in[2,3,10,11]:
        for kind in[0,8,255]:add(controller,kind=kind)
    for phase in[0,9]:
        for menu in[0,8]:
            for count in[0,3]:add(8,phase=phase,menu=menu,listCount=count)
    for count in[0,1,3,0xFFFFFFFF]:add(9,listCount=count)
    ids=[int.from_bytes(save[0x1E8+i*132+20:0x1E8+i*132+24],'little')for i in range(100)]
    a,b,other=[x for x in ids if x][:3]
    for role,groups in[('active',[a,other,b,0,0,0]),('reserve',[0,0,0,a,other,b]),('stored',[0]*6)]:
        for index,raw in enumerate([0,1,127,255]):add(6,phase=6,scratch33=raw,skills=[0,1,2,3][index],cost=[-1,0,5,20][index],tally=[0,9998,9999,65535][index],gold=[0,10,10,10][index],groups=groups,role=role)
    add(6,skills=0,scratch33=127,groups=[0]*6,role='stored-menu-one',cost=-1,tally=0,menu=1)
    for raw in[128,255]:add(6,skills=raw,scratch33=255,groups=[0]*6,role='stored-negative-count',cost=-1,tally=10000)
    return result


class Machine(F.Machine):
    def __init__(self,arm,save,assets,overlay,p,body=None):
        super().__init__(arm,save,assets,overlay,p,None)
        self.subjectEnd=ENTRY+(len(body)if body is not None else 1460)
        self.assets=assets;self.lifecycle=[];self.commitChecks=[]
        if body is not None:self.u.mem_write(ENTRY,body)
        calls={int(i.op_str[1:],16)for i in Cs(CS_ARCH_ARM,CS_MODE_ARM).disasm(overlay[ENTRY-0x021D7240:ENTRY-0x021D7240+1448],ENTRY)if i.mnemonic in['bl','blx']and i.op_str.startswith('#')}
        self.providers.update({entry:self.provider for entry in calls-NATIVE})
        args=[int.from_bytes(row[20:24],'little')for row in self.parents]+[self.species,0,0]
        if p['controller']==6:self.invoke(0x02229100,args)
        else:self.trace,self.returned,self.builderChecks=[],[],[]
        self.preparation=dict(actualReturns=int(p['controller']==6),nativeDependencyActualReturns=max(0,len(self.returned)-1),providedCalls=sum(r['provider']for r in self.trace),scratch33=self.profile['scratch33'],builderChecks=self.builderChecks)
        self.u.mem_write(F.VIEW+3,bytes([p['controller']]))
        self.u.mem_write(F.VIEW,bytes([p.get('kind',0)]))
        self.word(F.VIEW+36,0x02620000)
        entries=b''.join(bytes([i+1,0])for i in range(3))
        self.u.mem_write(0x02620000,entries)
        self.u.mem_write(0x022463A1,bytes([p.get('skills',0)&255]));self.word(0x022463A4,0x02620000)
        self.word(F.CHOICE+32,p.get('cost',-1))
        self.word(0x020F6044,p['seed'])
        self.counterAddress=int.from_bytes(arm[0x63DA0:0x63DA4],'little')+80
        self.counterLimit=int.from_bytes(arm[0x63DA4:0x63DA8],'little')
        self.goldAddress=int.from_bytes(arm[0x62B60:0x62B64],'little')+28
        self.goldLimit=int.from_bytes(arm[0x62B64:0x62B68],'little')
        self.u.mem_write(self.counterAddress,struct.pack('<H',p.get('tally',0)))
        self.word(self.goldAddress,p.get('gold',10))
        if p.get('groups') is not None:self.u.mem_write(0x021BD540,struct.pack('<6I',*p['groups']))
        self.before=bytes(self.u.mem_read(F.BASE,0x800000))
    def provider(self,obj,args):
        entry=self.currentEntry
        if entry==0x0221CF14:return self.profile.get('listCount',2)&0xFFFFFFFF
        if entry==0x02062378:return self.profile.get('menu',16)&0xFFFFFFFF
        if entry==0x02061294:return self.profile.get('available',0)
        if entry in[0x0221FA70,0x02220160]and args[:2]!=[F.CONTEXT,0]:raise ValueError('Birth395 required GUI context/zero option differs')
        return super().provider(obj,args)
    def observe(self,uc,address,size,data):
        if address==ENTRY or address in EXTRA_WATCH or ENTRY<=address<self.subjectEnd:
            self.steps+=1;self.close_returns(uc,address)
            if ENTRY<=address<self.subjectEnd:self.targetObserved.update(range(address-ENTRY,address-ENTRY+size))
            if address!=ENTRY and ENTRY<=address<self.subjectEnd:return
            sp=uc.reg_read(UC_ARM_REG_SP)
            self.trace.append(dict(entry=hex(address),arguments=[uc.reg_read(r)for r in F.REGS[:4]],stackWords=list(struct.unpack('<II',uc.mem_read(sp,8))),provider=False,sp=hex(sp)))
            frame=dict(entry=address,returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),sp=sp,preserved=[uc.reg_read(r)for r in F.REGS[4:12]])
            if address==0x0222900C:
                frame['commitSnapshot']=dict(rows=bytes(uc.mem_read(0x021BD674,13200)),scratch=bytes(uc.mem_read(F.SCRATCH,132)),groups=list(struct.unpack('<6I',uc.mem_read(0x021BD540,24))),counter=self.read_word(0x021BD520),rng=self.read_word(0x020F6044),parents=[uc.reg_read(r)for r in F.REGS[:2]])
            if address==0x020633C8:self.lifecycle.append(dict(stage='before-refresh',uid=uc.reg_read(UC_ARM_REG_R0),raw33=bytes(uc.mem_read(self.record(uc.reg_read(UC_ARM_REG_R0))+51,1))[0]))
            if self.frames and all(frame[k]==self.frames[-1][k]for k in['returnAddress','returnThumb','sp','preserved']):self.frames[-1].setdefault('tailAliases',[]).append(hex(address))
            else:self.frames.append(frame)
            return
        super().observe(uc,address,size,data)
    def close_returns(self,uc,address):
        if self.frames and address==self.frames[-1]['returnAddress']and uc.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp'] and self.frames[-1]['entry']==0x0222900C:
            import ov000_birth395_models_20261031 as M
            event=M.commit_model(self,self.frames[-1]['commitSnapshot'],uc.reg_read(UC_ARM_REG_R0))
            self.commitChecks.append(event);self.lifecycle.append(dict(stage='after-commit',uid=event['returnedUid'],raw33=event['raw33']))
        super().close_returns(uc,address)
    def write(self,uc,access,address,size,value,data):
        if ENTRY<address+size and address<self.subjectEnd:raise ValueError('Birth395 self-modifying subject')
        if uc.reg_read(UC_ARM_REG_PC)==0x0206341C:
            record=uc.reg_read(UC_ARM_REG_R4);uid=self.read_word(record+20)
            if address!=record+51 or size!=1 or value!=0:raise ValueError('Birth395 original raw33 writer shape differs')
            self.lifecycle.append(dict(stage='native-write',pc='0x0206341c',address=hex(address),uid=uid,before=bytes(uc.mem_read(address,1))[0],value=value,size=size))
        super().write(uc,access,address,size,value,data)
    def invoke(self,entry,args=()):
        self.u.mem_write(F.STACK-0x10000,bytes(0x11000));self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xA0395000+i*0x100 for i in range(13)]
        for register,value in zip(F.REGS,values):self.u.reg_write(register,value)
        for register,value in zip(F.REGS[:4],args):self.u.reg_write(register,value&0xFFFFFFFF)
        if len(args)>4:self.word(F.STACK,args[4])
        self.u.reg_write(UC_ARM_REG_SP,F.STACK);self.u.reg_write(UC_ARM_REG_LR,F.STOP)
        self.trace,self.writes,self.returned,self.frames=[],[],[],[];self.steps=0;self.targetObserved=set();self.builderChecks=[];self.scratch33Writes=[]
        self.u.emu_start(entry,F.STOP,count=2000000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.u.reg_read(UC_ARM_REG_PC)!=F.STOP or self.u.reg_read(UC_ARM_REG_SP)!=F.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or self.frames or[self.u.reg_read(r)for r in F.REGS[4:12]]!=values[4:12]:raise ValueError('Birth395 top actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)
    def run(self):
        value=self.invoke(ENTRY)
        after=bytes(self.u.mem_read(F.BASE,0x800000));cut=F.STACK-0x10000-F.BASE;end=F.STACK+0x1000-F.BASE
        return dict(profile=self.profile,returnWord=value,actualReturns=1,nativeDependencyActualReturns=len(self.returned)-1,providedCalls=sum(r['provider']for r in self.trace),preparation=self.preparation,nonstackSha256=c.sha(after[:cut]+after[end:]),trace=self.trace,nativeReturns=self.returned,writes=self.writes,scratch33Writes=self.scratch33Writes,scratch33Before=self.profile['scratch33'],scratch33After=after[F.SCRATCH-F.BASE+51],lifecycle=self.lifecycle,commitChecks=self.commitChecks,steps=self.steps,observedCodeBytes=sorted(self.targetObserved))
