import json
import random
import struct
import sys
from pathlib import Path
import match_runtime
from project import ROOT,write_json,sha256
from link_runtime_unit import measured_module
sys.path.insert(0,str(ROOT/'evidence/application'))
from preparation_machine_20261029 import Machine,inputs,REGS,RECORDS,STACK,STOP,SAVED_START,SAVED_END
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_HOOK_CODE,UC_HOOK_MEM_WRITE,UC_HOOK_MEM_READ
from unicorn.arm_const import *
ENTRY=0x02229100
CAPS=[0x02044E44,0x02044E80,0x02044EBC,0x02044EF8,0x02044F34,0x02044F70]
WATCHED={ENTRY,0x02062A10,0x02008E0C,0x0203D294,*CAPS}

class BirthMachine(Machine):
    def __init__(self,arm,save,assets,overlay,seed):
        self.frames=[]
        self.returned=[]
        self.steps=0
        self.seed=seed
        super().__init__(arm,save,assets,patches={0x021D7240:overlay},providers={0x020634CC:self.xp})
        previous=self.u
        self.u=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        self.u.ctl_set_cpu_model(UC_CPU_ARM_946)
        for address,length in[(0x02000000,0x800000),(0x04000000,0x1000)]:
            self.u.mem_map(address,length)
            self.u.mem_write(address,bytes(previous.mem_read(address,length)))
        self.u.hook_add(UC_HOOK_CODE,self.observe)
        self.u.hook_add(UC_HOOK_MEM_WRITE,self.write)
        self.u.hook_add(UC_HOOK_MEM_READ,self.divide)
        self.u.mem_write(0x02247480,random.Random(seed).randbytes(0xE0))
    def xp(self,obj,args):
        return 0xABC000+self.seed
    def write(self,uc,access,address,size,value,data):
        if 0x02247480<=address and address+size<=0x02247560:
            self.writes.append([hex(address),size,value])
            return
        super().write(uc,access,address,size,value,data)
    def close_returns(self,uc,address):
        while self.frames and address==self.frames[-1]['returnAddress']and uc.reg_read(UC_ARM_REG_SP)==self.frames[-1]['sp']:
            frame=self.frames.pop()
            if [uc.reg_read(r)for r in REGS[4:12]]!=frame['preserved']or bool(uc.reg_read(UC_ARM_REG_CPSR)&0x20)!=frame['returnThumb']:
                raise ValueError('Birth329 native preserved registers differ')
            self.returned.append(dict(entry=hex(frame['entry']),
                    result=uc.reg_read(UC_ARM_REG_R0),
                    actualReturn=True))
    def observe(self,uc,address,size,data):
        self.steps+=1
        self.close_returns(uc,address)
        if address in WATCHED or address in self.providers:
            sp=uc.reg_read(UC_ARM_REG_SP)
            args=[uc.reg_read(r)for r in REGS[:4]]
            stack=list(struct.unpack('<II',uc.mem_read(sp,8)))
            self.trace.append(dict(entry=hex(address),
                    arguments=args,
                    stackWords=stack,
                    provider=address in self.providers,
                    sp=hex(sp)))
            if address in WATCHED:
                self.frames.append(dict(returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),entry=address,
                        returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,
                        sp=sp,
                        preserved=[uc.reg_read(r)for r in REGS[4:12]]))
        if address in self.providers:
            result=self.providers[address](self,[uc.reg_read(r)for r in REGS[:4]])
            uc.reg_write(UC_ARM_REG_R0,result)
            for i in[1,2,3,12]:
                uc.reg_write(REGS[i],0xAB000000+i+self.seed)
            uc.reg_write(UC_ARM_REG_PC,uc.reg_read(UC_ARM_REG_LR))
    def birth(self,args,limit=200000):
        self.u.mem_write(STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xA0020000+i*0x100 for i in range(len(REGS))]
        for r,v in zip(REGS,values):self.u.reg_write(r,v)
        for r,v in zip(REGS[:4],args[:4]):self.u.reg_write(r,v&0xFFFFFFFF)
        self.u.mem_write(STACK,struct.pack('<I',args[4]&0xFFFFFFFF))
        self.u.reg_write(UC_ARM_REG_SP,STACK)
        self.u.reg_write(UC_ARM_REG_LR,STOP)
        self.trace,self.writes,self.returned,self.frames=[],[],[],[]
        self.u.emu_start(ENTRY,STOP,count=limit)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or self.u.reg_read(UC_ARM_REG_PC)!=STOP or self.u.reg_read(UC_ARM_REG_SP)!=STACK or self.frames or[ self.u.reg_read(r)for r in REGS[4:12]]!=values[4:12]:
            raise ValueError(('Birth329 actual return/frame differs',
                    hex(self.u.reg_read(UC_ARM_REG_PC)),
                    hex(self.u.reg_read(UC_ARM_REG_SP)),
                    self.frames,
                    [hex(self.u.reg_read(r))for r in REGS[4:12]],
                    [hex(v)for v in values[4:12]]))
        return self.u.reg_read(UC_ARM_REG_R0)

def run():
    arm,save,assets=inputs()
    overlay=measured_module('ov000')[1]
    rows=[save[0x1E8+i*132:0x1E8+(i+1)*132]for i in range(100)]
    chosen=[r for r in rows if int.from_bytes(r[20:24],'little')][:2]
    args=[int.from_bytes(chosen[0][20:24],
            'little'),
        int.from_bytes(chosen[1][20:24],
            'little'),
        int.from_bytes(chosen[0][24:26],
            'little'),
        chosen[0][26],
        0]
    obj=BirthMachine(arm,save,assets,overlay,329)
    before_saved=bytes(obj.u.mem_read(SAVED_START,SAVED_END-SAVED_START))
    before33=bytes(obj.u.mem_read(0x022474C8+0x33,1))
    result=obj.birth(args)
    report=dict(sourceCredit=0,
        entry=hex(ENTRY),
        actualReturns=1,
        returnWord=hex(result),
        steps=obj.steps,
        arguments=args,
        trace=obj.trace,
        nativeObservedReturns=obj.returned,
        writes=obj.writes,
        record33Before=before33.hex(),
        record33After=bytes(obj.u.mem_read(0x022474C8+0x33,
                1)).hex(),
        savedRegionUnchanged=bytes(obj.u.mem_read(SAVED_START,
                SAVED_END-SAVED_START))==before_saved,
        rngCalls=sum(r['entry']=='0x203d294'for r in obj.trace),
        xpProviderCalls=sum(r['provider']for r in obj.trace),
        hardwareDivisionReads=len(obj.divisions),
        generatorSha256=sha256(__file__))
    write_json(ROOT/'evidence/attempts/ov000-birth329-native-smoke-20261031.json',report)
    print(json.dumps({k:report[k]for k in['actualReturns',
                    'returnWord',
                    'steps',
                    'record33Before',
                    'record33After',
                    'savedRegionUnchanged',
                    'rngCalls',
                    'xpProviderCalls',
                    'hardwareDivisionReads']}))

if __name__=='__main__':run()
