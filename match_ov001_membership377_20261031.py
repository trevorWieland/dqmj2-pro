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
import ov001_membership377_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov001_20261031_membership377/source.c'
WORK=ROOT/'work/ol377-proof'
PINS=ROOT/'evidence/verification/ov001-membership377-inputs-20261031.json'

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

def execute(arm,save,assets,overlay,recipe,kind,unit=None,refresh=None,caller=None):
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    if kind=='direct':
        argument=M.setup(obj,recipe)
        entry,args=F.ENTRY,[argument]
    else:
        M.OLD.setup(obj,recipe)
        entry,args=(0x02209B4C,[])if kind=='refresh'else(0x02209CC0,[])
    if unit is not None:
        obj.u.mem_write(F.ENTRY,unit)
        obj.subjectEntry=F.ENTRY
        obj.subjectEnd=F.ENTRY+len(unit)
    if refresh is not None:obj.u.mem_write(0x02209B4C,refresh)
    if caller is not None:obj.u.mem_write(0x02209CC0,caller)
    before=bytes(obj.u.mem_read(0x02000000,0x800000))
    value=obj.call(entry,args)
    after=bytes(obj.u.mem_read(0x02000000,0x800000))
    if kind=='direct':
        M.OLD.compare_nonstack(before,after,before)
        if value!=M.expected(before,argument)or obj.provided:raise ValueError('Membership377 independent result/provider differs')
        model=dict(absentFromResolvedGroups=value,argument=hex(argument),independentNoNonstackWrites=True)
    elif kind=='refresh':
        expected=bytearray(before)
        changes=M.OLD.refresh_image(expected)
        M.OLD.compare_nonstack(before,after,expected)
        if obj.provided:raise ValueError('Membership377 standalone refresh provider unexpectedly used')
        model=dict(refreshedActors=changes,semanticReturn='unproven void; physicalR0 paired')
    else:model=M.OLD.connected_model(before,after,value,obj.provided,assets,recipe)
    result=dict(kind=kind,recipe=recipe,model=model,actualReturns=1,physicalReturnWord=value,observedMembershipCodeBytes=sorted(getattr(obj,'membershipObserved',set())),nativeDependencyActualReturns=len(obj.returned)-1,providedCalls=len(obj.provided),instructions=obj.steps,trace=obj.trace,nativeReturns=obj.returned,writes=obj.writes,ramSha256=c.sha(after),_ram=after)
    del obj
    return result

def batch(arm,save,assets,overlay,recipes,kind,unit,refresh=None,caller=None):
    summaries=[]
    observed=set()
    for recipe in recipes:
        original=execute(arm,save,assets,overlay,recipe,kind)
        candidate=execute(arm,save,assets,overlay,recipe,kind,unit,refresh,caller)
        if original!=candidate:raise ValueError(('Membership377 complete original/source evidence differs',kind,recipe))
        original.pop('_ram')
        observed.update(original['observedMembershipCodeBytes'])
        raw=encoded(original)
        zipped=gzip.compress(raw,mtime=0)
        artifact=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz')
        artifact.parent.mkdir(parents=True,exist_ok=True)
        artifact.write_bytes(zipped)
        summaries.append(dict(recipe=recipe,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=2*original['providedCalls'],instructions=original['instructions'],physicalReturnWord=original['physicalReturnWord'],model=original['model'],rawTraceArtifact=dict(path=str(artifact.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate
        gc.collect()
    return dict(pairs=len(summaries),actualReturns=2*len(summaries),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in summaries),providedCalls=sum(r['providedCalls']for r in summaries),maximumInstructions=max(r['instructions']for r in summaries),observedSubjectCodeBytes=len(observed),results=summaries)

def null_stop(arm,save,assets,overlay,unit=None):
    from unicorn import UcError,UC_ERR_READ_UNMAPPED
    from unicorn.arm_const import UC_ARM_REG_PC
    recipe=dict(M.recipes()[-1],active=[101],reserve=[],nullActor=True)
    obj=F.Machine(arm,save,assets,overlay,recipe['seed'])
    M.setup(obj,recipe)
    if unit is not None:obj.u.mem_write(F.ENTRY,unit)
    try:obj.call(F.ENTRY,[0])
    except UcError as error:
        if error.errno!=UC_ERR_READ_UNMAPPED:raise
        result=dict(actualReturns=0,expectedStopped=True,pc=hex(obj.u.reg_read(UC_ARM_REG_PC)),steps=obj.steps,failure=repr(error),providedCalls=len(obj.provided))
    else:raise ValueError('Membership377 null actor with resolved group unexpectedly returned')
    del obj
    return result

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Membership377 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Membership377 frozen source/model/input differs')
    arm,save,assets=B.inputs()
    metadata,overlay,unused=measured_module('ov001')
    row,proof,unit=compile_unit(SOURCE,'membership',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=140
    refresh,refresh_proof,refresh_body=compile_unit(ROOT/'src/overlays/ov001_20261031_recruit373/source.c','accepted-refresh',True)
    caller,caller_proof,caller_body=compile_unit(ROOT/'src/overlays/ov001_20261031_recruit373/caller-interface/source.c','zero-credit-caller',True)
    if len(unit)!=140 or len(refresh_body)!=232 or len(caller_body)!=1092:raise ValueError('Membership377 source extents differ')
    direct=batch(arm,save,assets,overlay,M.recipes(),'direct',unit)
    connected_refresh=batch(arm,save,assets,overlay,M.OLD.standalone_recipes(),'refresh',unit,refresh_body)
    connected_caller=batch(arm,save,assets,overlay,M.OLD.OLD.recipes(),'connected',unit,refresh_body,caller_body)
    stopped=null_stop(arm,save,assets,overlay)
    if stopped!=null_stop(arm,save,assets,overlay,unit):raise ValueError('Membership377 null prerequisite stop differs')
    controls=[]
    for name,old,new,case in[('result','return found == 0;','return found != 0;',0),('reserve-query','native_fn_02062a88(reserve_index)','native_fn_02062a50(reserve_index)',next(i for i,r in enumerate(M.recipes())if r['actorUid']==101 and not r['active']and r['reserve']==[101]))]:
        folder=ROOT/'nonmatching/overlay-lane/20261031-membership377-negative'/name
        folder.mkdir(parents=True,exist_ok=True)
        text=SOURCE.read_text()
        if text.count(old)!=1:raise ValueError('Membership377 control source pattern differs')
        text=text.replace(old,new)
        for path,value in[(folder/'source.c',text),(folder/'context.h',SOURCE.with_name('context.h').read_text())]:
            if path.exists()and path.read_bytes()!=value.encode():raise ValueError('Membership377 preserve control')
            path.write_bytes(value.encode())
        bad,bad_proof,bad_body=compile_unit(folder/'source.c','negative-'+name,False)
        try:execute(arm,save,assets,overlay,M.recipes()[case],'direct',bad_body)
        except ValueError as error:
            if str(error)!='Membership377 independent result/provider differs':raise
            failure=str(error)
        else:raise ValueError('Membership377 compiled control unexpectedly passed')
        controls.append(dict(name=name,compilation=bad,genuineLinkComparison=bad_proof,expectedRejected=True,failure=failure,sourceCredit=0))
    oracle=dict(directAllNative=direct,connectedRefresh=connected_refresh,connectedCaller=connected_caller,actualReturns=direct['actualReturns']+connected_refresh['actualReturns']+connected_caller['actualReturns'],nativeDependencyActualReturns=direct['nativeDependencyActualReturns']+connected_refresh['nativeDependencyActualReturns']+connected_caller['nativeDependencyActualReturns'],providedCalls=connected_caller['providedCalls'],freshMachinePerExecution=True,cpu='ARM946',instructionBound=200000,independentCompleteNonstackRamComparison=True,completeOriginalSourceRamTraceEquality=True,nullResolvedGroupPrerequisite=dict(executions=2,actualReturns=0,evidence=stopped),compiledNegativeControls=controls,limits=['Only new9AC0/140 receives proposed source credit; fresh232/1092 rebuilds are existing or zero-credit interface inputs','Direct membership and connected232 execute all-native with no function providers; connected1092 keeps explicit UI/input/window boundaries','Membership resolves each saved slot through actual record lookup; raw groupUID0/999 do not count if they resolve no record','Actor pointer/parameterUID are supplied. Null actor returns1 when every slot resolves null,but stops on unmapped read when a slot resolves a record; no normal-game error return or broad null-safety is inferred','Every nonstack RAM byte and return is independently modeled in each scope; full original/source RAM and traces agree','The group predicate still performs all six lookups after a match. Separate natural per-loop index lifetimes match140/140 without register declarations,assembly or opcode patch','Constructor/lifecycle/current scene,persistence and game field meanings remain unproven beyond the separately qualified native transition evidence'])
    row['oracle']=oracle
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=metadata['sha256'],matches=[row],proposedSourceBytes=140,acceptedSourceCredit=0,zeroCreditRebuilds=[dict(compilation=refresh,genuineLinkComparison=refresh_proof,sourceCredit=0),dict(compilation=caller,genuineLinkComparison=caller_proof,sourceCredit=0)],inputPins=pins['files'],mainInputSha256=c.sha(arm),assetHashes={k:c.sha(v)for k,v in assets.items()},generatorSha256=sha256(__file__),reproductionCommand='python match_ov001_membership377_20261031.py')
    write_json(ROOT/'evidence/matches/ov001-20261031-membership377.json',report)
    print(json.dumps(dict(exactBytes=140,directReturns=direct['actualReturns'],directNative=direct['nativeDependencyActualReturns'],refreshReturns=connected_refresh['actualReturns'],refreshNative=connected_refresh['nativeDependencyActualReturns'],callerReturns=connected_caller['actualReturns'],callerNative=connected_caller['nativeDependencyActualReturns'],callerProviders=connected_caller['providedCalls'])))

if __name__=='__main__':run()
