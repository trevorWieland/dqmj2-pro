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
import ov001_recruit373_fixture_20261031 as F
import ov001_recruit373_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov001_20261031_recruit373/source.c'
NEAR=ROOT/'nonmatching/overlay-lane/20261031-recruit373-near/source.c'
WORK=ROOT/'work/ol373-proof'
PINS=ROOT/'evidence/verification/ov001-recruit373-inputs-20261031.json'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov001','2','off',True,thumb=False)
    row=rows[0]
    row['sourceDependencies']=[dict(path=str(source.with_name('context.h').relative_to(ROOT)),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    if exact:proof=validate(row,qualified_bindings(row),directory)
    else:
        try:proof=validate(row,qualified_bindings(row),directory)
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=row['name']:raise
    return row,proof,(directory/'caller.bin').read_bytes()

def execute(arm,save,assets,overlay,recipe,kind,body=None,caller=None):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    M.setup(obj,recipe)
    entry=F.REFRESH if kind=='direct'else F.ELIGIBILITY if kind=='near'else F.OLD.ENTRY
    if body is not None:
        obj.u.mem_write(F.ELIGIBILITY if kind=='near'else F.REFRESH,body)
        obj.subjectEntry=F.ELIGIBILITY if kind=='near'else F.REFRESH
        obj.subjectEnd=obj.subjectEntry+len(body)
    if caller is not None:obj.u.mem_write(F.OLD.ENTRY,caller)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    value=obj.call(entry)
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    if kind=='direct':
        expected=bytearray(before)
        refreshed=M.refresh_image(expected)
        M.compare_nonstack(before,after,expected)
        model=dict(refreshedActors=refreshed,semanticReturn='unproven; Cvoid,paired physicalR0 separately checked')
    elif kind=='near':
        M.compare_nonstack(before,after,before)
        if value!=M.eligibility_model(before)or obj.provided:raise ValueError('Recruit373 independent near eligibility differs')
        model=dict(eligibility=value,sourceCredit=0,listCapacity=3)
    else:model=M.connected_model(before,after,value,obj.provided,assets,recipe)
    if kind!='connected'and obj.provided:raise ValueError('Recruit373 standalone provider unexpectedly used')
    outside=after[:F.ELIGIBILITY-0x02000000]+after[F.ELIGIBILITY-0x02000000+140:]if kind=='near'else after
    result=dict(recipe=recipe,kind=kind,model=model,actualReturns=1,physicalReturnWord=value,nativeDependencyActualReturns=len(obj.returned)-1,providedCalls=len(obj.provided),instructions=obj.steps,trace=obj.trace,nativeReturns=obj.returned,writes=obj.writes,targetCodeBytes={hex(k):sorted(v)for k,v in obj.targetObserved.items()},ramSha256=c.sha(outside),_ram=outside)
    del obj
    return result

def batch(arm,save,assets,overlay,recipes,kind,body,caller=None):
    summaries=[]
    observed=set()
    for recipe in recipes:
        original=execute(arm,save,assets,overlay,recipe,kind)
        candidate=execute(arm,save,assets,overlay,recipe,kind,body,caller)
        if original!=candidate:raise ValueError(('Recruit373 complete original/source paired evidence differs',kind,recipe))
        original.pop('_ram')
        raw=encoded(original)
        zipped=gzip.compress(raw,mtime=0)
        artifact=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz')
        artifact.parent.mkdir(parents=True,exist_ok=True)
        artifact.write_bytes(zipped)
        observed.update(original['targetCodeBytes'][hex(F.ELIGIBILITY if kind=='near'else F.REFRESH)])
        summaries.append(dict(recipe=recipe,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=2*original['providedCalls'],instructions=original['instructions'],physicalReturnWord=original['physicalReturnWord'],model=original['model'],rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate
        gc.collect()
    return dict(pairs=len(summaries),actualReturns=2*len(summaries),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=sum(r['providedCalls']for r in summaries),maximumInstructions=max(r['instructions']for r in summaries),observedSubjectCodeBytes=len(observed),results=summaries)

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Recruit373 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Recruit373 frozen source/model/input differs')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov001')
    row,proof,body=compile_unit(SOURCE,'refresh',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=232
    caller,caller_proof,caller_body=compile_unit(SOURCE.parent/'caller-interface/source.c','caller-interface',True)
    caller['genuineLinkComparison']=freeze_link(caller_proof)
    near,near_proof,near_body=compile_unit(NEAR,'near-eligibility',False)
    if len(body)!=232 or len(caller_body)!=1092 or len(near_body)!=140:raise ValueError('Recruit373 source extents differ')
    direct=batch(arm,save,assets,overlay,M.standalone_recipes(),'direct',body)
    connected=batch(arm,save,assets,overlay,M.OLD.recipes(),'connected',body,caller_body)
    near_oracle=batch(arm,save,assets,overlay,M.eligibility_recipes(),'near',near_body)
    controls=[]
    for name,old,new in[('raw1ff',', s8 *, 0x1FF) = 0;',', s8 *, 0x1FF) = 1;'),('mp-add','native_fn_ov001_021dbcf0(current_actor)','0')]:
        folder=ROOT/'nonmatching/overlay-lane/20261031-recruit373-negative'/name
        folder.mkdir(parents=True,exist_ok=True)
        text=SOURCE.read_text()
        if text.count(old)!=(2 if name=='raw1ff'else 1):raise ValueError('Recruit373 negative source pattern differs')
        text=text.replace(old,new)
        for path,value in[(folder/'source.c',text),(folder/'context.h',SOURCE.with_name('context.h').read_text())]:
            if path.exists()and path.read_bytes()!=value.encode():raise ValueError('Recruit373 preserve control')
            path.write_bytes(value.encode())
        bad,bad_proof,bad_body=compile_unit(folder/'source.c','negative-'+name,False)
        try:execute(arm,save,assets,overlay,M.standalone_recipes()[1],'direct',bad_body)
        except ValueError as error:
            failure=error.args[0]
            if not isinstance(failure,tuple)or failure[0]!='Recruit373 independent nonstack RAM differs':raise
        else:raise ValueError('Recruit373 compiled control unexpectedly passed')
        controls.append(dict(name=name,compilation=bad,genuineLinkComparison=bad_proof,expectedRejected=True,failure=failure,sourceCredit=0))
    oracle=dict(directAllNative=direct,connectedCaller=connected,actualReturns=direct['actualReturns']+connected['actualReturns'],nativeDependencyActualReturns=direct['nativeDependencyActualReturns']+connected['nativeDependencyActualReturns'],providedCalls=connected['providedCalls'],freshMachinePerExecution=True,cpu='ARM946',instructionBound=200000,independentCompleteNonstackRamComparison=True,completeOriginalSourceRamTraceEquality=True,semanticReturn='Unproven; voidC,physicalR0 checked in original/source pairs',compiledNegativeControls=controls,limits=['Standalone refresh232 and eligibility140 execute entirely native with zero function providers; connected1092 retains only explicitly declared UI/input/window providers','Source232 alone receives proposed credit; caller1092 return-declaration alternative and near140 retain zero additional coverage','Native clearing1FD/1FF is a transient actor mutation when enabled actorUID is absent from resolved saved groups; no record33 mutation or current/future scene is inferred','Raw HP/MP,feature list,paramUID,enabled/block flags and actor bindings are supplied; full constructor and loaded-scene lifecycle are not proved','CurrentMP>=10000 bypasses mutation,while maximum calculation clamps at9999; both sides of the literal threshold and signed/extreme inputs are modeled','Original collectors can emit15 IDs while caller arrays hold3; supported recipes enforce<=3qualifying rows and never silently truncate','Native group-membership helper and stat helpers are original scaffolding and get no new source credit; their actual returning calls are measured separately from providers','Near eligibility remains139/140 due nativeBLS versus CBEQ; no instruction patch or byte credit is allowed'])
    row['oracle']=oracle
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=metadata['sha256'],matches=[row],proposedSourceBytes=232,acceptedSourceCredit=0,zeroCreditCallerInterface=dict(compilation=caller,bytes=1092,sourceCredit=0,preferredSourceChanged=False,scope='Only9B4C return declaration becomesvoid; fresh caller source genuine-links identically and executes in connected pairs'),nearEligibility=dict(compilation=near,genuineLinkComparison=near_proof,sourceCredit=0,exact=False,oracle=near_oracle),inputPins=pins['files'],mainInputSha256=c.sha(arm),assetHashes={k:c.sha(v)for k,v in assets.items()},generatorSha256=sha256(__file__),reproductionCommand='python match_ov001_recruit373_20261031.py')
    write_json(ROOT/'evidence/matches/ov001-20261031-recruit373.json',report)
    print(json.dumps(dict(exactBytes=232,directReturns=direct['actualReturns'],directNative=direct['nativeDependencyActualReturns'],connectedReturns=connected['actualReturns'],connectedNative=connected['nativeDependencyActualReturns'],connectedProviders=connected['providedCalls'],nearReturns=near_oracle['actualReturns'],nearNative=near_oracle['nativeDependencyActualReturns'],nearProviders=near_oracle['providedCalls'])))

if __name__=='__main__':run()
