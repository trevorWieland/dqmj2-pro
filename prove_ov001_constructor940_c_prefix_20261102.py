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
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
import ov001_template349_fixture_20261031 as F
import ov001_template349_models_20261031 as G
import probe_ov000_birth329_20261031 as B
CACHE=0x021C6758
TABLE=0x02580000
STOP_AT=0x0207C8FC
ACTIVE_BODY=None
LEVEL_SHA='8cedd8c498e8ae8444db268fb301e25c43f38ad8c1d9f435fc0f3cac9b112b03'

class Machine(F.Machine):
    def __init__(self,*args):
        super().__init__(*args)
        if ACTIVE_BODY is not None:self.u.mem_write(F.ENTRY,ACTIVE_BODY)

    def observe(self,u,address,size,data):
        if ACTIVE_BODY is not None and F.ENTRY<=address<F.ENTRY+1352 and address>=F.ENTRY+len(ACTIVE_BODY):raise ValueError('940 source escaped its compiled own-code span')
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
        if not self.reached or self.u.reg_read(UC_ARM_REG_PC)!=STOP_AT or len(self.frames)!=1 or self.frames[0]['entry']!=F.ENTRY:raise ValueError('940 unfinished prefix endpoint/frame differs')
        if self.stopWords[0]!=1:raise ValueError('940 clear-cache heap word differs')


def trunc100(value):
    return -(abs(value)//100)if value<0 else value//100


def execute(negative=False):
    global ACTIVE_BODY
    import match_runtime as C
    tag='942'if negative else'940'
    source=ROOT/('nonmatching/overlay-lane/20261102-template942/wrong-first-stat/source.c'if negative else'nonmatching/overlay-lane/20261102-template940/ordinary-c/source.c')
    C.WORK=ROOT/f'work/ol{tag}/compile'
    sourceRows,unused=C.compare(source,'ov001','2','off',True)
    row=sourceRows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    try:
        proof=validate(row,qualified_bindings(row),ROOT/f'work/ol{tag}/genuine')
    except ValueError as error:
        if not error.args or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    ACTIVE_BODY=(ROOT/f'work/ol{tag}/genuine/caller.bin').read_bytes()
    if len(ACTIVE_BODY)>1352 or proof.get('exactCallerBytes'):raise ValueError('940 unexpected source span; review separately')
    main,save,assets=B.inputs()
    moduleInfo,overlay,unused=measured_module('ov001')
    mainInfo=measured_module('main')[0]
    asset=bytes(ndspy.rom.NintendoDSRom((ROOT/'inputs/game.nds').read_bytes()).getFileByName('LevelUpTbl.bin'))
    if len(asset)!=7200 or hashlib.sha256(asset).hexdigest()!=LEVEL_SHA:raise ValueError('940 measured level asset differs')
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
                if not index<18:raise ValueError('940 measured cache row outside asset')
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
                normalExpected=bytes(expected)
                if negative:
                    incorrect=(int.from_bytes(output[:2],'little')+1)&0xFFFF
                    G.put(expected,G.TEMPLATE-0x02000000,2,incorrect)
                    G.put(expected,G.TEMPLATE-0x02000000+4,2,incorrect)
                    if after[:lo]==normalExpected[:lo]and after[hi:]==normalExpected[hi:]:raise ValueError('942 wrong-source checkpoint not rejected')
                if after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]:
                    bad=next(i for i,(a,b)in enumerate(zip(after,expected))if a!=b and not lo<=i<hi)
                    raise ValueError(('940 independent prefix model differs',hex(0x02000000+bad),after[bad],expected[bad],draw,level,stat,add))
                if vm.providers or vm.divisions:raise ValueError('940 unexpected provider/hardware read')
                rng=[r for r in vm.trace if r['entry']=='0x203d294']
                if len(rng)!=1 or rng[0]['arguments'][0]!=20:raise ValueError('940 actual RNG20 entry differs')
                load=[r for r in vm.trace if r['entry']=='0x207c8a4']
                if len(load)!=1 or load[0]['arguments'][:2]!=[1,index]:raise ValueError('940 actual cache caller words differ')
                rows.append(dict(negativeControl=negative,normalModelRejected=negative,draw=draw,level=level,stat=stat,add=add,cacheIndex=index,cachePointer=hex(TABLE+index*400),actualTopReturns=0,unfinishedCheckpoint=hex(STOP_AT),stopWords=vm.stopWords,selectedHelperFrameCompletions=len(vm.returned),trace=vm.trace,writes=vm.writes,expectedTemplate=output.hex(),actualTemplate=bytes(vm.u.mem_read(G.TEMPLATE,132)).hex(),rngState=draw<<16,nonstackRamSha256=hashlib.sha256(after[:lo]+after[hi:]).hexdigest(),allPassed=True))
    raw=json.dumps(rows,sort_keys=True,separators=(',',':')).encode()
    path=ROOT/f'evidence/generated/ov001-constructor{tag}-warm-prefix-traces-20261102.json.gz'
    path.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,allPassed=True,sourceCredit=0,negativeControl=negative,normalModelRejections=len(rows)if negative else 0,sourceHypothesis=dict(source=row,genuineLink=proof),nativeReference=dict(path='evidence/application/ov001-constructor938-warm-prefix-20261102.json',sha256=sha256(ROOT/'evidence/application/ov001-constructor938-warm-prefix-20261102.json')),romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',mode='arm',moduleSha256=moduleInfo['sha256'],mainSha256=mainInfo['sha256'],prefixCheckpoints=len(rows),actualTopReturns=0,suppliedCalls=0,asset=dict(name='LevelUpTbl.bin',bytes=len(asset),sha256=LEVEL_SHA,complete400ByteBlocks=18,cacheSlots=20),generatedTrace=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path),uncompressedSha256=hashlib.sha256(raw).hexdigest()),limits=['Genuine-linked nonmatching complete C source runs its normal-mode prefix, stopped BEFORE actual7C8FC cache cleanup executes. Native caller span1352 remains unmatched; no ordinary-C function-match credit. Every case has an unfinished constructor frame; no top/function/source/module/ROM completion credit.','Only measured cache index from native species row+43 is warmed with its real400-byte LevelUpTbl block. The7200-byte asset has18blocks, distinct from20holder capacity. Cache preloading is explicit synthetic input, not file-loading/heap ownership. Cleanup would free this pointer, so the probe deliberately does not claim a valid allocator/free lifecycle.','Actual RNG(20) advances once and sets90..109 stat scaling; actual cache getter and raw level-word lookups run without allocator/read/free providers. All six stat sums narrow to16bits after signed truncation/100; current HP/MP copies and two table words are independently modeled.','Raw level bytes0/1/99/100/255 and signed stat/addend extremes are supplied, with four known RNG outputs. Game-valid level/species/variant, file-loading lifecycle, later extra-skill/RNG paths and final normal-mode record remain unresolved.','All nonstack8MiB RAM matches independently; inherited fixed stack window is explicitly excluded as in frozen349, with unfinished checkpoint status retained. Zero hardware reads/providers, no original file or accepted-source edits.'])
    if negative:report['limits'].insert(0,'Whole wrong C adds one to the first signed result before16-bit narrowing and its later HP copy. Sixty unfinished checkpoints reach the same bounded endpoint, each independently agrees only with the explicitly wrong effect and rejects the original prefix model. These are not proper top returns or exact-source credit.')
    write_json(ROOT/f'evidence/application/ov001-constructor{tag}-warm-prefix-20261102.json',report)
    print(dict(prefixCheckpoints=len(rows),actualTopReturns=0,suppliedCalls=0,sourceCredit=0,compiledBytes=len(ACTIVE_BODY)),flush=True)

if __name__=='__main__':execute()
