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
import ov001_recruit353_fixture_20261031 as F
import ov001_recruit353_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov001_20261031_recruit353/source.c'
WORK=ROOT/'work/ol353-proof'
PINS=ROOT/'evidence/verification/ov001-recruit353-inputs-20261031.json'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def execute(arm,save,assets,overlay,recipe,body=None):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    template=M.setup(obj,recipe)
    if body is not None:obj.u.mem_write(F.ENTRY,body)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    value=obj.recruit([recipe['contextWord'],recipe['callerWord']])
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    model=M.model(before,after,assets,recipe,template,value)
    if any(r['entry']=='0x203d294'for r in obj.trace):raise ValueError('Recruit353 unexpected RNG call')
    result=dict(recipe=recipe,model=model,instructions=obj.steps,actualReturns=1,nativeDependencyActualReturns=len(obj.returned)-1,providedCalls=0,trace=obj.trace,nativeReturns=obj.returned,writes=obj.writes,observedOriginalCodeBytes=sorted(obj.observed),ramSha256=c.sha(after),_ram=after)
    del obj
    return result

def stopped(arm,save,assets,overlay,body,kind):
    from unicorn import UcError,UC_ERR_READ_UNMAPPED
    from unicorn.arm_const import UC_ARM_REG_PC
    recipe=M.recipes(assets)[0]
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    M.setup(obj,recipe)
    if body is not None:obj.u.mem_write(F.ENTRY,body)
    if kind=='not-ready':obj.u.mem_write(F.TEMPLATE+0x67,bytes([0]))
    else:
        for i in range(100):obj.word(B.RECORDS+132*i+20,100+i)
    try:obj.recruit([recipe['contextWord'],recipe['callerWord']])
    except UcError as error:
        if error.errno!=UC_ERR_READ_UNMAPPED:raise
        result=dict(kind=kind,actualReturns=0,expectedStopped=True,pc=hex(obj.u.reg_read(UC_ARM_REG_PC)),steps=obj.steps,failure=repr(error),unfinishedNativeFrames=[hex(f['entry'])for f in obj.frames],providedCalls=0)
    else:raise ValueError('Recruit353 invalid prerequisite unexpectedly returned')
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Recruit353 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Recruit353 frozen source/fixture/model differs')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov001')
    c.WORK=WORK/'compile'
    rows,unused=c.compare(SOURCE,'ov001','2','off',True,thumb=False)
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(SOURCE.with_name('context.h').relative_to(ROOT)),sha256=sha256(SOURCE.with_name('context.h')))]
    proof=validate(row,qualified_bindings(row),WORK/'link')
    frozen_proof=freeze_link(proof)
    row['genuineLinkComparison']=frozen_proof
    row['exactBytes']=400
    body=(WORK/'link/caller.bin').read_bytes()
    if len(body)!=400:raise ValueError('Recruit353 complete source extent differs')
    summaries=[]
    observed=set()
    for recipe in M.recipes(assets):
        original=execute(arm,save,assets,overlay,recipe)
        candidate=execute(arm,save,assets,overlay,recipe,body)
        if original!=candidate:raise ValueError('Recruit353 complete original/source RAM or trace differs')
        original.pop('_ram')
        raw=encoded(original)
        zipped=gzip.compress(raw,mtime=0)
        artifact=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz')
        artifact.parent.mkdir(parents=True,exist_ok=True)
        artifact.write_bytes(zipped)
        observed.update(original['observedOriginalCodeBytes'])
        summaries.append(dict(recipe=recipe,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=0,instructions=original['instructions'],model=original['model'],rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate
        gc.collect()
        print(json.dumps(dict(case=len(summaries),actualReturns=2,instructions=summaries[-1]['instructions'])),flush=True)
    invalid=[]
    for kind in['not-ready','full-roster']:
        original=stopped(arm,save,assets,overlay,None,kind)
        candidate=stopped(arm,save,assets,overlay,body,kind)
        if original!=candidate:raise ValueError('Recruit353 prerequisite stops differ')
        invalid.append(original)
    controls=[]
    for name,old,new,case in[('context-word',' = arg0;',' = arg0 + 1;',0),('loop-step','var_r5 += 1;','var_r5 += 2;',2)]:
        folder=ROOT/'nonmatching/overlay-lane/20261031-recruit353-negative'/name
        folder.mkdir(parents=True,exist_ok=True)
        text=SOURCE.read_text()
        if text.count(old)!=1:raise ValueError('Recruit353 negative pattern differs')
        text=text.replace(old,new)
        for path,value in[(folder/'source.c',text),(folder/'context.h',SOURCE.with_name('context.h').read_text())]:
            if path.exists()and path.read_bytes()!=value.encode():raise ValueError('Recruit353 preserve control')
            path.write_bytes(value.encode())
        c.WORK=WORK/'negative'/name/'compile'
        bad_rows,unused=c.compare(folder/'source.c','ov001','2','off',True,thumb=False)
        directory=WORK/'negative'/name/'link'
        try:bad_proof=validate(bad_rows[0],qualified_bindings(bad_rows[0]),directory)
        except ValueError as error:
            bad_proof=error.args[0]
            if not isinstance(bad_proof,dict)or bad_proof.get('caller')!=bad_rows[0]['name']:raise
        try:execute(arm,save,assets,overlay,M.recipes(assets)[case],(directory/'caller.bin').read_bytes())
        except ValueError as error:
            failure=str(error)
            if failure!='Recruit353 independent live-record/context/return model differs':raise
        else:raise ValueError('Recruit353 compiled control unexpectedly passed')
        controls.append(dict(name=name,compilation=bad_rows,genuineLinkComparison=bad_proof,expectedRejected=True,failure=failure,sourceCredit=0))
    oracle=dict(pairs=len(summaries),actualReturns=2*len(summaries),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=0,freshMachinePerExecution=True,cpu='ARM946',instructionBound=2000000,maximumInstructions=max(r['instructions']for r in summaries),independentLiveRecordAndCallerModel=True,completeOriginalSourceRamTraceEquality=True,observedOriginalCallerInstructionBytes=len(observed),nativeCodeBytes=396,literalBytes=4,invalidPrerequisiteExecutions=4,invalidPrerequisiteReturns=0,invalidPrerequisites=invalid,compiledNegativeControls=controls,results=summaries,limits=['The supplied ready132-byte template,already-loaded SkillTbl,raw mode/flags and synthetic roster are prerequisites; ordinary scene reachability and table loader initialization are not established','All original helper code executes without function providers; selected helper frames have strict actual-return checks,not exhaustive frames for every leaf','The model independently checks every live record,caller context/counter,group/template immutability,three-byte state and feature-derived stat halfwords; bitmap flags and unused-row permutation are compared completely original/source but not independently interpreted','Raw template13 is supplied0/1/127/255 and copied to record33; no nonzero initializer,game label,ordinary newborn default or persistence is inferred','Both record capacity exhaustion and not-ready template stop for unmapped reads; they are unsupported prerequisite states,not returning game error paths or app restrictions','No active/reserve insertion occurs in this entry; the supplied groups remain unchanged and further ordinary caller behavior is separate','The helperFBE70 pointer view and32-bit loop/signed8 outgoing slot repair are measured source hypotheses,not original typedef or formal-arity proof'])
    row['oracle']=oracle
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='ov001',moduleSha256=metadata['sha256'],processor='arm9',program='',matches=[row],proposedSourceBytes=400,acceptedSourceCredit=0,preferredSourceChanges=False,mainInputSha256=c.sha(arm),assetHashes={k:c.sha(v)for k,v in assets.items()},inputPins=pins['files'],generatorSha256=sha256(__file__),reproductionCommand='python match_ov001_recruit353_20261031.py')
    write_json(ROOT/'evidence/matches/ov001-20261031-recruit353.json',report)
    print(json.dumps(dict(exactBytes=400,actualReturns=oracle['actualReturns'],nativeDependencyActualReturns=oracle['nativeDependencyActualReturns'],providedCalls=0,observedCodeBytes=len(observed))))

if __name__=='__main__':run()
