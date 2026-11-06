import gzip
import hashlib
import json
import struct
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import match_runtime
import ndspy.rom
from unicorn.arm_const import *
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import measured_module
import ov001_template349_fixture_20261031 as F
import ov001_template349_models_20261031 as G
import probe_ov000_birth329_20261031 as B
CACHE=0x021C6758
TABLE=0x02580000
STOP_AT=0x0207C8FC
LEVEL_SHA='8cedd8c498e8ae8444db268fb301e25c43f38ad8c1d9f435fc0f3cac9b112b03'

class Machine(F.Machine):
    def observe(self,u,address,size,data):
        if address==STOP_AT:
            self.reached=True
            self.stopWords=[u.reg_read(r)for r in B.REGS[:4]]
            u.emu_stop()
            return
        super().observe(u,address,size,data)
        if address in [0x0207C8A4,0x0207C948,0x0207C9B8]:
            self.trace.append(dict(entry=hex(address),arguments=[u.reg_read(r)for r in B.REGS[:4]],sp=hex(u.reg_read(UC_ARM_REG_SP))))

    def prefix(self):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xAB450000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_R0,G.ACTOR)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.steps=0
        self.frames=[]
        self.returned=[]
        self.trace=[]
        self.writes=[]
        self.reached=False
        self.u.emu_start(F.ENTRY,B.STOP,count=200000)
        if not self.reached or self.u.reg_read(UC_ARM_REG_PC)!=STOP_AT or len(self.frames)!=1 or self.frames[0]['entry']!=F.ENTRY:raise ValueError('938 unfinished prefix endpoint/frame differs')
        if self.stopWords[0]!=1:raise ValueError('938 clear-cache heap word differs')


def trunc100(value):
    return -(abs(value)//100)if value<0 else value//100


def execute():
    main,save,assets=B.inputs()
    moduleInfo,overlay,unused=measured_module('ov001')
    mainInfo=measured_module('main')[0]
    asset=bytes(ndspy.rom.NintendoDSRom((ROOT/'inputs/game.nds').read_bytes()).getFileByName('LevelUpTbl.bin'))
    if len(asset)!=7200 or hashlib.sha256(asset).hexdigest()!=LEVEL_SHA:raise ValueError('938 measured level asset differs')
    rows=[]
    inverse=pow(0x41C64E6D,-1,1<<32)
    template=G.recipes(assets)[0]
    kind=assets['EnmyKindTbl.bin'][8:]
    for draw in [0,1,10,19]:
        for level in [0,1,99,100,255]:
            for stat,add in [(-32768,-1),(100,0),(32767,1)]:
                recipe=dict(template,mode=0,stat=stat,add=add,variant=0,skillPrefix=0,skillGap=False,null=False)
                vm=Machine(main,save,assets,overlay,recipe['seed'])
                actor,parameter=G.setup(vm,recipe)
                actor=bytearray(actor)
                actor[0x1FC]=level
                vm.u.mem_write(G.ACTOR,bytes(actor))
                sourceSpecies=G.read(parameter,0x2A,2)
                alternative=G.read(kind,sourceSpecies*100+8,2)
                species=alternative if alternative else sourceSpecies
                index=kind[species*100+0x43]
                if not index<18:raise ValueError('938 measured cache row outside asset')
                vm.u.mem_write(TABLE,asset)
                vm.u.mem_write(CACHE,bytes(80))
                vm.word(CACHE+index*4,TABLE+index*400)
                seed=(((draw<<16)-0x3039)*inverse)&0xFFFFFFFF
                vm.word(0x020F6044,seed)
                before=bytes(vm.u.mem_read(0x02000000,0x800000))
                vm.prefix()
                output=bytearray(132)
                G.put(output,0x64,2,species)
                output[0x66]=parameter[0x2C]
                output[0x67]=1
                output[0x69]=actor[0x31F]
                for a,p,t in zip(G.ASTAT,G.PSTAT,G.TSTAT):
                    value=G.read(actor,a,2,True)+G.read(parameter,p,2,True)
                    G.put(output,t,2,trunc100(value*(draw+90)))
                output[4:8]=output[:4]
                output[0x10]=level
                current=struct.unpack_from('<I',asset,index*400+(level-1)*4)[0]if 1<=level<=100 else 0
                nextLevel=level+1
                following=struct.unpack_from('<I',asset,index*400+(nextLevel-1)*4)[0]if 1<=nextLevel<=100 else 0
                G.put(output,0x14,4,current)
                G.put(output,0x18,4,following)
                expected=bytearray(before)
                expected[G.TEMPLATE-0x02000000:G.TEMPLATE-0x02000000+132]=output
                G.put(expected,0x020F6044-0x02000000,4,draw<<16)
                after=bytes(vm.u.mem_read(0x02000000,0x800000))
                lo=B.STACK-0x10000-0x02000000
                hi=B.STACK+0x1000-0x02000000
                if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]:
                    bad=next(i for i,(a,b)in enumerate(zip(after,expected))if a!=b and not lo<=i<hi)
                    raise ValueError(('938 independent prefix model differs',hex(0x02000000+bad),after[bad],expected[bad],draw,level,stat,add))
                if vm.providers or vm.divisions:raise ValueError('938 unexpected provider/hardware read')
                rng=[r for r in vm.trace if r['entry']=='0x203d294']
                if len(rng)!=1 or rng[0]['arguments'][0]!=20:raise ValueError('938 actual RNG20 entry differs')
                load=[r for r in vm.trace if r['entry']=='0x207c8a4']
                if len(load)!=1 or load[0]['arguments'][:2]!=[1,index]:raise ValueError('938 actual cache caller words differ')
                rows.append(dict(draw=draw,level=level,stat=stat,add=add,cacheIndex=index,cachePointer=hex(TABLE+index*400),actualTopReturns=0,unfinishedCheckpoint=hex(STOP_AT),stopWords=vm.stopWords,selectedHelperFrameCompletions=len(vm.returned),trace=vm.trace,writes=vm.writes,expectedTemplate=output.hex(),actualTemplate=bytes(vm.u.mem_read(G.TEMPLATE,132)).hex(),rngState=draw<<16,nonstackRamSha256=hashlib.sha256(after[:lo]+after[hi:]).hexdigest(),allPassed=True))
    raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    path=ROOT/'evidence/generated/ov001-constructor938-warm-prefix-traces-20261102.json.gz'
    path.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],prefixCheckpoints=len(rows),actualTopReturns=0,suppliedCalls=0,asset=dict(name='LevelUpTbl.bin',bytes=len(asset),sha256=LEVEL_SHA,complete400ByteBlocks=18,cacheSlots=20),generatedTrace=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Original normal-mode FB214 prefix only, stopped BEFORE actual7C8FC cache cleanup executes. Every case has an unfinished constructor frame; no top/function/source/module/ROM completion credit.','Only measured cache index from native species row+43 is warmed with its real400-byte LevelUpTbl block. The7200-byte asset has18blocks, distinct from20holder capacity. Cache preloading is explicit synthetic input, not file-loading/heap ownership. Cleanup would free this pointer, so the probe deliberately does not claim a valid allocator/free lifecycle.','Actual RNG(20) advances once and sets90..109 stat scaling; actual cache getter and raw level-word lookups run without allocator/read/free providers. All six stat sums narrow to16bits after signed truncation/100; current HP/MP copies and two table words are independently modeled.','Raw level bytes0/1/99/100/255 and signed stat/addend extremes are supplied, with four known RNG outputs. Game-valid level/species/variant, file-loading lifecycle, later extra-skill/RNG paths and final normal-mode record remain unresolved.','All nonstack8MiB RAM matches independently; inherited fixed stack window is explicitly excluded as in frozen349, with unfinished checkpoint status retained. Zero hardware reads/providers, no original file or accepted-source edits.'])
    write_json(ROOT/'evidence/application/ov001-constructor938-warm-prefix-20261102.json',report)
    print(dict(prefixCheckpoints=len(rows),actualTopReturns=0,suppliedCalls=0,sourceCredit=0),flush=True)

if __name__=='__main__':execute()
