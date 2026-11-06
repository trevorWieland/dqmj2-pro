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
import ov001_membership377_fixture_20261031 as F
import ov001_recruit373_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov001_20261031_eligibility381/source.c'
WORK=ROOT/'work/ol381-proof'
PINS=ROOT/'evidence/verification/ov001-eligibility381-inputs-20261031.json'
ENTRY=0x02209C34

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

def execute(arm,save,assets,overlay,recipe,kind,unit=None,others=()):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    M.setup(obj,recipe)
    if unit is not None:
        obj.u.mem_write(ENTRY,unit)
        obj.subjectEntry=ENTRY
        obj.subjectEnd=ENTRY+len(unit)
    for address,code in others:obj.u.mem_write(address,code)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    value=obj.call(ENTRY if kind=='direct'else 0x02209CC0)
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    if kind=='direct':
        M.compare_nonstack(before,after,before)
        if value!=M.eligibility_model(before)or obj.provided:raise ValueError('Eligibility381 independent result/provider differs')
        model=dict(eligibility=value,listCapacity=3,independentNoNonstackWrites=True)
    else:model=M.connected_model(before,after,value,obj.provided,assets,recipe)
    result=dict(kind=kind,recipe=recipe,model=model,actualReturns=1,returnWord=value,nativeDependencyActualReturns=len(obj.returned)-1,providedCalls=len(obj.provided),instructions=obj.steps,trace=obj.trace,nativeReturns=obj.returned,writes=obj.writes,observedPredicateCodeBytes=sorted(obj.targetObserved[ENTRY]),ramSha256=c.sha(after),_ram=after)
    del obj
    return result

def batch(arm,save,assets,overlay,recipes,kind,unit,others=()):
    results=[]
    observed=set()
    for recipe in recipes:
        original=execute(arm,save,assets,overlay,recipe,kind)
        candidate=execute(arm,save,assets,overlay,recipe,kind,unit,others)
        if original!=candidate:raise ValueError(('Eligibility381 complete original/source evidence differs',kind,recipe))
        original.pop('_ram')
        observed.update(original['observedPredicateCodeBytes'])
        raw=encoded(original);zipped=gzip.compress(raw,mtime=0)
        artifact=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz');artifact.parent.mkdir(parents=True,exist_ok=True);artifact.write_bytes(zipped)
        results.append(dict(recipe=recipe,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=2*original['providedCalls'],instructions=original['instructions'],model=original['model'],rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate;gc.collect()
    return dict(pairs=len(results),actualReturns=2*len(results),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in results),providedCalls=sum(r['providedCalls']for r in results),maximumInstructions=max(r['instructions']for r in results),observedPredicateCodeBytes=len(observed),results=results)

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Eligibility381 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Eligibility381 frozen source/input differs')
    arm,save,assets=B.inputs();metadata,overlay,unused=measured_module('ov001')
    row,proof,unit=compile_unit(SOURCE,'predicate',True);row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=140
    others=[];rebuilds=[]
    for name,address,path in[('membership',0x02209AC0,'src/overlays/ov001_20261031_membership377/source.c'),('refresh',0x02209B4C,'src/overlays/ov001_20261031_recruit373/source.c'),('caller',0x02209CC0,'src/overlays/ov001_20261031_recruit373/caller-interface/source.c')]:
        other,other_proof,code=compile_unit(ROOT/path,'zero-credit-'+name,True)
        rebuilds.append(dict(compilation=other,genuineLinkComparison=other_proof,sourceCredit=0));others.append((address,code))
    if len(unit)!=140:raise ValueError('Eligibility381 complete extent differs')
    direct=batch(arm,save,assets,overlay,M.eligibility_recipes(),'direct',unit)
    connected=batch(arm,save,assets,overlay,M.OLD.recipes(),'connected',unit,others)
    controls=[]
    for name,old,new,case in[('initial-index','index = 0;','index = 1;',next(i for i,r in enumerate(M.eligibility_recipes())if r['selectedUids']==[200]and r['actorEnabled']==0)),('uid-fallback','field_1c == ids[index]','field_1c != ids[index]',next(i for i,r in enumerate(M.eligibility_recipes())if r['selectedUids']==[999]and r['actorEnabled']==0))]:
        folder=ROOT/'nonmatching/overlay-lane/20261031-eligibility381-negative'/name;folder.mkdir(parents=True,exist_ok=True)
        text=SOURCE.read_text()
        if text.count(old)!=1:raise ValueError('Eligibility381 control pattern differs')
        text=text.replace(old,new)
        for path,value in[(folder/'source.c',text),(folder/'context.h',SOURCE.with_name('context.h').read_text())]:
            if path.exists()and path.read_bytes()!=value.encode():raise ValueError('Eligibility381 preserve control')
            path.write_bytes(value.encode())
        bad,bad_proof,bad_body=compile_unit(folder/'source.c','negative-'+name,False)
        try:execute(arm,save,assets,overlay,M.eligibility_recipes()[case],'direct',bad_body)
        except ValueError as error:
            if str(error)!='Eligibility381 independent result/provider differs':raise
            failure=str(error)
        else:raise ValueError('Eligibility381 compiled control unexpectedly passed')
        controls.append(dict(name=name,compilation=bad,genuineLinkComparison=bad_proof,expectedRejected=True,failure=failure,sourceCredit=0))
    oracle=dict(directAllNative=direct,connectedCaller=connected,actualReturns=direct['actualReturns']+connected['actualReturns'],nativeDependencyActualReturns=direct['nativeDependencyActualReturns']+connected['nativeDependencyActualReturns'],providedCalls=connected['providedCalls'],freshMachinePerExecution=True,cpu='ARM946',instructionBound=200000,independentCompleteNonstackRamComparison=True,completeOriginalSourceRamTraceEquality=True,compiledNegativeControls=controls,limits=['Only new9C34/140 receives proposed credit;373 near139 remains immutable historical zero-credit evidence','Initial guard compares unsigned count to its actual initialized zero index; no invented variable or blanket replacement of literal0 comparisons is used','Original collectors can emit15 words but this caller owns only3; supported fixtures require<=3qualifying rows and do not silently truncate malformed excess','Actor enabled/block/parameter flags and UIDs are supplied; raw predicate success does not establish ordinary game eligibility or current scene','Direct predicate executes all native without providers; connected1092 retains explicit UI/input/window boundaries,with fresh ordinary-C membership140/refresh232/caller1092 rebuilt at zero extra credit','Every nonstack RAM byte and result is independently modeled and full original/source traces agree; no byte patch,assembly,volatile or accepted-source edit'])
    row['oracle']=oracle
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=metadata['sha256'],matches=[row],proposedSourceBytes=140,acceptedSourceCredit=0,zeroCreditRebuilds=rebuilds,inputPins=pins['files'],mainInputSha256=c.sha(arm),generatorSha256=sha256(__file__),reproductionCommand='python match_ov001_eligibility381_20261031.py')
    write_json(ROOT/'evidence/matches/ov001-20261031-eligibility381.json',report)
    print(json.dumps(dict(exactBytes=140,directReturns=direct['actualReturns'],directNative=direct['nativeDependencyActualReturns'],directProviders=direct['providedCalls'],connectedReturns=connected['actualReturns'],connectedNative=connected['nativeDependencyActualReturns'],connectedProviders=connected['providedCalls'],observedCode=direct['observedPredicateCodeBytes'])))

if __name__=='__main__':run()
