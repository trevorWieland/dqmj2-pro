import gc
import gzip
import json
import sys
from pathlib import Path
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import measured_module,validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import probe_ov000_birth329_20261031 as B
import ov001_recruit364_fixture_20261031 as F
import ov001_recruit364_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov001_20261031_recruit364/source.c'
WORK=ROOT/'work/ol364-proof'
PINS=ROOT/'evidence/verification/ov001-recruit364-inputs-20261031.json'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def execute(arm,save,assets,overlay,recipe,body=None):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    M.setup(obj,recipe)
    if body is not None:obj.u.mem_write(F.ENTRY,body)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    value=obj.controller()
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    model=M.model(before,after,value,obj.provided,assets,recipe)
    result=dict(recipe=recipe,model=model,actualReturns=1,nativeDependencyActualReturns=len(obj.returned)-1,providedCalls=len(obj.provided),instructions=obj.steps,trace=obj.trace,nativeReturns=obj.returned,writes=obj.writes,observedCodeBytes=sorted(obj.observed),ramSha256=c.sha(after),_ram=after)
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Recruit364 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Recruit364 frozen source/fixture/model differs')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov001')
    c.WORK=WORK/'compile'
    rows,unused=c.compare(SOURCE,'ov001','2','off',True,thumb=False)
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)),sha256=sha256(SOURCE.with_name('context.h')))]
    proof=validate(row,qualified_bindings(row),WORK/'link')
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=1092
    body=(WORK/'link/caller.bin').read_bytes()
    if len(body)!=1092:raise ValueError('Recruit364 complete source extent differs')
    summaries=[]
    observed=set()
    for recipe in M.recipes():
        original=execute(arm,save,assets,overlay,recipe)
        candidate=execute(arm,save,assets,overlay,recipe,body)
        if original!=candidate:raise ValueError('Recruit364 complete original/source RAM or trace differs')
        original.pop('_ram')
        raw=encoded(original)
        zipped=gzip.compress(raw,mtime=0)
        artifact=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz')
        artifact.parent.mkdir(parents=True,exist_ok=True)
        artifact.write_bytes(zipped)
        observed.update(original['observedCodeBytes'])
        summaries.append(dict(recipe=recipe,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=2*original['providedCalls'],instructions=original['instructions'],model=original['model'],rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate
        gc.collect()
    controls=[]
    control_cases=[('capacity','(3 - var_r4_2)','(4 - var_r4_2)',next(i for i,r in enumerate(M.recipes())if r['phase']==0 and r['active']==[101]and r['childSpecies']==31)),('required-uid','native_fn_ov001_021dc2f8(temp_r0_5);','native_fn_ov001_021dc2f8(temp_r0_5 + 1);',next(i for i,r in enumerate(M.recipes())if r['phase']==1 and r['drag']and r['candidate']==101 and r['previous']==0)),('unconditional-getter','native_fn_02062a10(native_fn_0206bf34())','native_fn_02062a10(temp_r0_5)',next(i for i,r in enumerate(M.recipes())if r['phase']==1 and r['drag']and r['candidate']==101 and r['previous']==101))]
    for name,old,new,case in control_cases:
        folder=ROOT/'nonmatching/overlay-lane/20261031-recruit364-negative'/name
        folder.mkdir(parents=True,exist_ok=True)
        text=SOURCE.read_text()
        if text.count(old)!=1:raise ValueError('Recruit364 control pattern differs')
        text=text.replace(old,new)
        for path,value in[(folder/'source.c',text),(folder/'context.h',SOURCE.with_name('context.h').read_text())]:
            if path.exists()and path.read_bytes()!=value.encode():raise ValueError('Recruit364 preserve control')
            path.write_bytes(value.encode())
        c.WORK=WORK/'negative'/name/'compile'
        bad_rows,unused=c.compare(folder/'source.c','ov001','2','off',True,thumb=False)
        directory=WORK/'negative'/name/'link'
        try:bad_proof=validate(bad_rows[0],qualified_bindings(bad_rows[0]),directory)
        except ValueError as error:
            bad_proof=error.args[0]
            if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad_rows[0]['name']:raise
        try:execute(arm,save,assets,overlay,M.recipes()[case],(directory/'caller.bin').read_bytes())
        except ValueError as error:
            failure=error.args[0]
            prefix=failure[0]if isinstance(failure,tuple)else failure
            if prefix not in['Recruit364 independent complete nonstack RAM/return model differs','Recruit364 independent provider contract differs','Recruit364 provider event count differs']:raise
        else:raise ValueError('Recruit364 compiled control unexpectedly passed')
        controls.append(dict(name=name,compilation=bad_rows,genuineLinkComparison=bad_proof,expectedRejected=True,failure=failure,sourceCredit=0))
    oracle=dict(pairs=len(summaries),actualReturns=2*len(summaries),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=sum(r['providedCalls']for r in summaries),freshMachinePerExecution=True,cpu='ARM946',instructionBound=200000,maximumInstructions=max(r['instructions']for r in summaries),independentCompleteNonstackRamComparison=True,completeOriginalSourceRamTraceEquality=True,observedOriginalCallerInstructionBytes=len(observed),nativeCodeBytes=1088,literalBytes=4,compiledNegativeControls=controls,results=summaries,limits=['UI/input/window operations use explicit side-effect-free boundary providers; ordinary UI initialization,event timing and whole-scene reachability remain unestablished','All record/name copy,active/reserve capacity and rebuilding,actual list collectors,actor search/eligibility,category getters,tracker/unconditional UID getter and raw flag setters execute original code; providers are separately counted','Native6BC80/6BD24 can emit15 words,while these original callers have three-word arrays; supported fixtures explicitly have at most3 qualifying rows per group,without silently clipping outputs','Drag-local setup ports raw fields from the frozen tracker recipe; row14 is deliberately disabled for collection but still selected by original drag tracker. No-drag force-zero setup needs no sprite backing or row-position inference','Native21DC2F8 searches side0 then side2; actor31C,actor1FF,parameterAC and all actor/UID bindings are supplied raw fields,not measured current battle state','The complete independent model covers every nonstack RAM byte,including original6BF44 record31 clears and primary14/15 transitions with conditional secondary/flag76 marks; record33 stays unchanged in this caller corpus','Caller state pointers and name20 bytes are raw measured layouts; no original game field names,text encoding,ordinary eligibility policy or disk persistence is inferred','RequiredR0 inputs are restored in fresh contexts for491F8/B21C/A97C and21DC2F8; formal/transitive ABI remains qualified and accepted contexts stay unchanged','Zero tracker return does not erase current candidate: real6BF34 executes in the unchanged branch. Cases include candidate101 unchanged and candidate0 despite changed previous word'])
    row['oracle']=oracle
    facts=[]
    import re
    for module,addresses in[('main',[0x020491F8,0x0206BE2C,0x0206BF34,0x0206BC80,0x0206BD24,0x0206BF44]),('ov001',[0x021DC2F8,0x02209C34,0x0220B21C,0x0220A97C])]:
        native_meta,native_image,symbols=measured_module(module)
        base=0x02000000 if module=='main'else 0x021D7240
        for address in addresses:
            found=re.search(r'kind:function\(arm,size=0x([0-9a-f]+)\) addr:0x'+f'{address:08x}',symbols)
            size=int(found[1],16)
            facts.append(dict(module=module,address=hex(address),mode='arm',bytes=size,nativeSpanSha256=c.sha(native_image[address-base:address-base+size])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='ov001',moduleSha256=metadata['sha256'],processor='arm9',program='',matches=[row],proposedSourceBytes=1092,acceptedSourceCredit=0,preferredSourceChanges=False,nativeInterfaceFacts=facts,mainInputSha256=c.sha(arm),assetHashes={k:c.sha(v)for k,v in assets.items()},inputPins=pins['files'],generatorSha256=sha256(__file__),reproductionCommand='python match_ov001_recruit364_20261031.py')
    write_json(ROOT/'evidence/matches/ov001-20261031-recruit364.json',report)
    print(json.dumps(dict(exactBytes=1092,actualReturns=oracle['actualReturns'],nativeDependencyActualReturns=oracle['nativeDependencyActualReturns'],providedCalls=oracle['providedCalls'],observedCodeBytes=len(observed))))

if __name__=='__main__':run()
