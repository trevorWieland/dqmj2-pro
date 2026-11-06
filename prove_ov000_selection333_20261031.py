import gc
import gzip
import json
import struct
import sys
from pathlib import Path
import match_runtime as compiler
import unicorn
import probe_ov000_birth329_20261031 as B
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from project import ROOT,configuration,sha256,write_json
from unicorn.arm_const import *
ENTRY=0x0222976C
WATCH={ENTRY,0x02065D88,0x02044D60,0x0203D294}
WORK=ROOT/'work/ol333-proof'
SOURCE=ROOT/'src/runtime/ov000-drafts01/native_ov000_0222976c.c'

class Machine(B.BirthMachine):
    def __init__(self,*args):
        self.observed=set()
        super().__init__(*args)
    def observe(self,uc,address,size,data):
        self.steps+=1
        if ENTRY<=address<ENTRY+232:self.observed.update(range(address,address+size))
        self.close_returns(uc,address)
        if address in WATCH:
            sp=uc.reg_read(UC_ARM_REG_SP)
            self.trace.append(dict(entry=hex(address),
                    arguments=[uc.reg_read(r)for r in B.REGS[:4]],
                    sp=hex(sp),
                    provider=False))
            self.frames.append(dict(entry=address,
                    returnAddress=uc.reg_read(UC_ARM_REG_LR)&~1,
                    returnThumb=bool(uc.reg_read(UC_ARM_REG_LR)&1),
                    sp=sp,
                    preserved=[uc.reg_read(r)for r in B.REGS[4:12]]))
    def call_selection(self,args):
        self.u.mem_write(B.STACK-0x10000,bytes(0x11000))
        self.u.reg_write(UC_ARM_REG_CPSR,0x10)
        values=[0xBA000000+i*0x100 for i in range(len(B.REGS))]
        for r,v in zip(B.REGS,values):self.u.reg_write(r,v)
        for r,v in zip(B.REGS[:3],args):self.u.reg_write(r,v)
        self.u.reg_write(UC_ARM_REG_SP,B.STACK)
        self.u.reg_write(UC_ARM_REG_LR,B.STOP)
        self.u.emu_start(ENTRY,B.STOP,count=10000)
        self.close_returns(self.u,self.u.reg_read(UC_ARM_REG_PC))
        if self.frames or self.u.reg_read(UC_ARM_REG_PC)!=B.STOP or self.u.reg_read(UC_ARM_REG_SP)!=B.STACK or self.u.reg_read(UC_ARM_REG_CPSR)&0x3F!=0x10 or[self.u.reg_read(r)for r in B.REGS[4:12]]!=values[4:12]:
            raise ValueError('Selection333 actual return/frame differs')
        return self.u.reg_read(UC_ARM_REG_R0)

def word(raw,offset,value):raw[offset:offset+4]=struct.pack('<I',value)
def next_state(seed):return(seed*0x41C64E6D+0x3039)&0xFFFFFFFF

def model(a,b,seed,forced):
    value=9
    if a==1:value=0
    if a==2:value=1
    if b==1:value=9 if value==1 else 0
    if b==2:value=9 if value==0 else 1
    draws=[]
    if value==9:
        seed=next_state(seed)
        first=(seed>>16)%17
        draws.append(dict(limit=17,state=seed,result=first))
        if first==0:value=2
        else:
            seed=next_state(seed)
            second=(seed>>16)%1024
            draws.append(dict(limit=1024,state=seed,result=second))
            value=second&1
    return(2 if forced else value),seed,draws

def recipes(assets):
    table=assets['EnmyKindTbl.bin'][8:]
    species={flag:next(i for i in range(1,
                len(table)//100)if bool(int.from_bytes(table[i*100+4:i*100+6],
                    'little')&0x8000)==flag)for flag in[False,
            True]}
    return[dict(itemA=a,
            itemB=b,
            seed=seed,
            species=species[forced],
            forced=forced)for a in[0,
            13,
            14,
            181,
            182]for b in[0,
            13,
            14,
            181,
            182]for seed in[0,
            1,
            0xFFFFFFFF,
            0x12345678]for forced in[False,
            True]]

def execute(arm,save,assets,overlay,recipe,body=None):
    obj=Machine(arm,save,assets,overlay,recipe['seed'])
    if body is not None:obj.u.mem_write(ENTRY,body)
    p,q=0x021BD674,0x021BD6F8
    obj.u.mem_write(p+0x31,bytes([recipe['itemA']]))
    obj.u.mem_write(q+0x31,bytes([recipe['itemB']]))
    obj.word(0x020F6044,recipe['seed'])
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    table=assets['ItemTbl.bin'][8:]
    a,b=table[88*recipe['itemA']+0x2A],table[88*recipe['itemB']+0x2A]
    value,state,draws=model(a,b,recipe['seed'],recipe['forced'])
    expected=bytearray(before)
    word(expected,0x02247484-0x02000000,p)
    word(expected,0x02247488-0x02000000,q)
    word(expected,0x020F6044-0x02000000,state)
    expected[0x022474E3-0x02000000]=value
    result=obj.call_selection([p,q,recipe['species']])
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    lo,hi=B.STACK-0x10000-0x02000000,B.STACK+0x1000-0x02000000
    if result!=value or after[:lo]!=expected[:lo]or after[hi:]!=expected[hi:]:raise ValueError('Selection333 independent return/RAM differs')
    observed=[r for r in obj.trace if r['entry']=='0x203d294']
    returned=[r for r in obj.returned if r['entry']=='0x203d294']
    if[ r['arguments'][0]for r in observed]!=[r['limit']for r in draws]or[r['result']for r in returned]!=[r['result']for r in draws]:raise ValueError('Selection333 independent RNG sequence differs')
    if sum(r['entry']=='0x2065d88'for r in obj.trace)!=4:raise ValueError('Selection333 native item lookup count differs')
    result=dict(returnWord=result,
        finalRngState=state,
        rngDraws=draws,
        rawItemField2A=[a,
            b],
        instructions=obj.steps,
        nativeDependencyActualReturns=len(obj.returned)-1,
        rngActualReturns=len(draws),
        providedCalls=0,
        observedCallerBytes=sorted(obj.observed),
        trace=obj.trace,
        returns=obj.returned,
        writes=obj.writes,
        ramOutsideStackSha256=compiler.sha(after[:lo]+after[hi:]))
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,
        13,
        5)or unicorn.__version__!='2.1.4':raise ValueError('Selection333 pinned Python/Unicorn differs')
    if sha256(SOURCE)!='e0e5d7548b30290261523685fb0d8532a6064bbf14cd405014265b30af4573a1':raise ValueError('Selection333 accepted source differs')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov000')
    compiler.WORK=WORK/'compile'
    rows,unused=compiler.compare(SOURCE,'ov000','2','off',True,thumb=False)
    proof=validate(rows[0],qualified_bindings(rows[0]),WORK/'link')
    body=(WORK/'link/caller.bin').read_bytes()
    if body!=overlay[ENTRY-0x021D7240:ENTRY-0x021D7240+240]:raise ValueError('Selection333 frozen source/native bytes differ')
    results=[]
    for recipe in recipes(assets):
        original=execute(arm,save,assets,overlay,recipe)
        candidate=execute(arm,save,assets,overlay,recipe,body)
        if original!=candidate:raise ValueError('Selection333 complete original/C execution differs')
        results.append(dict(recipe=recipe,result=original))
        gc.collect()
    control=ROOT/'nonmatching/overlay-lane/20261031-selection333-negative/source.c'
    control.parent.mkdir(parents=True,exist_ok=True)
    original=SOURCE.read_text()
    changed=original.replace('native_fn_0203d294(0x11)','native_fn_0203d294(0x10)')
    if original==changed:raise ValueError('Selection333 ordinary RNG control missing')
    if control.exists()and control.read_bytes()!=changed.encode():raise ValueError('Selection333 preserve frozen control')
    control.write_bytes(changed.encode())
    compiler.WORK=WORK/'negative/compile'
    bad,unused=compiler.compare(control,'ov000','2','off',True,thumb=False)
    bad_directory=WORK/'negative/link'
    try:bad_proof=validate(bad[0],qualified_bindings(bad[0]),bad_directory)
    except ValueError as error:
        bad_proof=error.args[0]
        if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad[0]['name']:raise
    try:execute(arm,save,assets,overlay,recipes(assets)[0],(bad_directory/'caller.bin').read_bytes())
    except ValueError as error:
        rejection=error.args[0]
        if rejection!='Selection333 independent RNG sequence differs':raise
    else:raise ValueError('Selection333 ordinary source control unexpectedly passed')
    rejected=dict(compilation=bad,
        genuineLinkComparison=bad_proof,
        source=str(control.relative_to(ROOT)),
        sourceSha256=sha256(control),
        expectedRejected=True,
        failure=rejection,
        sourceCredit=0)
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode()
    zipped=gzip.compress(raw,mtime=0)
    artifact=WORK/'raw-traces'/(compiler.sha(zipped)+'.json.gz')
    artifact.parent.mkdir(parents=True,exist_ok=True)
    artifact.write_bytes(zipped)
    report=dict(schemaVersion=1,
        romSha256=configuration()['romSha256'],
        processor='arm9',
        program='',
        module='ov000',
        mode='arm',
        address=hex(ENTRY),
        bytes=240,
        moduleSha256=metadata['sha256'],
        acceptedSourceCredit=0,
        duplicateMatchCredit=0,
        usesExistingAcceptedSource=dict(path=str(SOURCE.relative_to(ROOT)),
            sha256=sha256(SOURCE)),
        compilation=rows,
        realLinkProof=proof,
        pairs=len(results),
        actualReturns=2*len(results),
        nativeDependencyActualReturns=2*sum(r['result']['nativeDependencyActualReturns']for r in results),
        rngActualReturns=2*sum(r['result']['rngActualReturns']for r in results),
        providedCalls=0,
        freshMachinePerExecution=True,
        cpu='ARM946',
        instructionBound=10000,
        maximumInstructions=max(r['result']['instructions']for r in results),
        fullIndependentNonstackRam=True,
        rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),
            sha256=compiler.sha(zipped),
            uncompressedSha256=compiler.sha(raw),
            bytes=len(zipped),
            gzipMtime=0),
        results=[dict(recipe=r['recipe'],
                returnWord=r['result']['returnWord'],
                finalRngState=r['result']['finalRngState'],
                rngDraws=r['result']['rngDraws'],
                rawItemField2A=r['result']['rawItemField2A'],
                nativeDependencyActualReturns=r['result']['nativeDependencyActualReturns'],
                resultSha256=compiler.sha(json.dumps(r['result'],
                        sort_keys=True,
                        separators=(',',
                            ':')).encode()))for r in results],
        limits=['Already accepted240-byte ordinary C is reused unchanged; zero duplicate source/function coverage',
            'Only0222976C is entered directly;0222900C record removal/allocation and ordinary scene callers are not executed',
            'Parent raw item byte31, child species and initial RNG state are supplied deterministic fixtures; no observed future scene state or real lifecycle is claimed',
            'Original native65D88 ItemTbl lookups and44D60 species flag test execute with actual measured assets; raw2A values and child bit15 remain raw fields, without game/item-name semantics',
            'Native RNG calls17 and conditional1024 actually execute; RNG returns are included in the native dependency total, not additional coverage',
            'Forced child bit15 may replace output with2 after RNG advances; absence of different output does not imply absence of draws',
            'Full nonstack RAM model permits only cached parent pointers, scratch1B and RNG state changes; stack and input setup remain separate',
            'No app, accepted source, registry or shared framework is edited'],
        rejectedOrdinarySourceControl=rejected,
        observedCallerInstructionBytes=len({a for r in results for a in r['result']['observedCallerBytes']}),
        inputFiles=[dict(path=p,
                sha256=sha256(ROOT/p))for p in['probe_ov000_birth329_20261031.py',
                'evidence/application/preparation_machine_20261029.py']],
        assetHashes={k:compiler.sha(v)for k,
            v in assets.items()},
        generatorSha256=sha256(__file__),
        reproductionCommand='python prove_ov000_selection333_20261031.py')
    write_json(ROOT/'evidence/application/ov000-selection333-native-20261031.json',report)
    print(json.dumps({k:report[k]for k in['pairs',
                    'actualReturns',
                    'nativeDependencyActualReturns',
                    'rngActualReturns',
                    'providedCalls',
                    'maximumInstructions']}))

if __name__=='__main__':run()
