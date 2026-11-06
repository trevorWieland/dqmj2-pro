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
import ov000_birth395_fixture_20261031 as G
F=G.F
import ov000_birth395_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov000_20261031_birth395/source.c'
WORK=ROOT/'work/ol395-proof'
PINS=ROOT/'evidence/verification/ov000-birth395-inputs-20261031.json'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov000','2','off',True,thumb=False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('Birth395 compiler failed')
    row=rows[0];row['sourceDependencies']=[dict(path=str(source.with_name('context.h').relative_to(ROOT)),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    if exact:proof=validate(row,qualified_bindings(row),directory)
    else:
        try:proof=validate(row,qualified_bindings(row),directory)
        except ValueError as error:
            proof=error.args[0]
            if not isinstance(proof,dict)or proof.get('caller')!=row['name']:raise
    return row,proof,(directory/'caller.bin').read_bytes()


def execute(arm,save,assets,overlay,p,body=None):
    obj=G.Machine(arm,save,assets,overlay,p,body);result=obj.run();result['model']=M.check(obj,result)
    after=bytes(obj.u.mem_read(F.BASE,0x800000));cut=F.STACK-0x10000-F.BASE;end=F.STACK+0x1000-F.BASE
    result['_ram']=after[:cut]+after[end:]
    del obj
    return result


def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Birth395 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Birth395 frozen input/source differs')
    arm,save,assets=F.inputs();metadata,overlay,unused=measured_module('ov000')
    row,proof,body=compile_unit(SOURCE,'caller',True);row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=1460
    if len(body)!=1460:raise ValueError('Birth395 entire native caller extent differs')
    cases=[];observed=set()
    for index,p in enumerate(G.profiles(save)):
        original=execute(arm,save,assets,overlay,p);candidate=execute(arm,save,assets,overlay,p,body)
        if original!=candidate:raise ValueError(('Birth395 complete original/source effect/trace differs',p))
        original.pop('_ram');observed.update(original['observedCodeBytes'])
        raw=encoded(original);zipped=gzip.compress(raw,mtime=0);path=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(zipped)
        cases.append(dict(profile=p,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=2*original['providedCalls'],maximumInstructions=original['steps'],preparationActualReturns=2*original['preparation']['actualReturns'],preparationNativeDependencyActualReturns=2*original['preparation']['nativeDependencyActualReturns'],preparationProvidedCalls=2*original['preparation']['providedCalls'],raw33Lifecycle=original['lifecycle'],independentModel=original['model'],scratch33Writes=0,rawTraceArtifact=dict(path=str(path.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate;gc.collect()
        if index%100==0:print(json.dumps(dict(completedPairs=index+1)),flush=True)
    controls=[]
    recipes=G.profiles(save)
    gui_case=next(p for p in recipes if p['controller']==1 and p['phase']==2 and p.get('kind')==0)
    for name,old,new,p in[('return-word','return 1U;','return 0U;',recipes[0]),('required-zero-option','native_fn_ov000_02220160(native_data_ov000_022460d4, 0);','native_fn_ov000_02220160(native_data_ov000_022460d4, 1);',gui_case)]:
        folder=ROOT/'nonmatching/overlay-lane/20261031-birth395-negative'/name;folder.mkdir(parents=True,exist_ok=True)
        source=SOURCE.read_text();header=SOURCE.with_name('context.h').read_text()
        if source.count(old)!=1:raise ValueError('Birth395 compiled control pattern differs')
        source=source.replace(old,new)
        for path,text in[(folder/'source.c',source),(folder/'context.h',header)]:
            if path.exists()and path.read_bytes()!=text.encode():raise ValueError('Birth395 preserve frozen compiled controls')
            path.write_bytes(text.encode())
        bad,bad_proof,bad_body=compile_unit(folder/'source.c','negative-'+name,False)
        try:execute(arm,save,assets,overlay,p,bad_body)
        except (ValueError,unicorn.UcError)as error:
            failure=str(error)
            if name=='return-word'and'Birth395 independent controller return differs'not in failure:raise
            if name=='required-zero-option'and'Birth395 required GUI context/zero option differs'not in failure:raise
        else:raise ValueError('Birth395 compiled control unexpectedly passed')
        controls.append(dict(name=name,profile=p,compilation=bad,genuineLinkComparison=bad_proof,rejected=True,failure=failure,sourceCredit=0))
    oracle=dict(pairs=len(cases),actualReturns=2*len(cases),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in cases),providedCalls=sum(r['providedCalls']for r in cases),preparationActualReturns=sum(r['preparationActualReturns']for r in cases),preparationNativeDependencyActualReturns=sum(r['preparationNativeDependencyActualReturns']for r in cases),preparationProvidedCalls=sum(r['preparationProvidedCalls']for r in cases),observedCodeBytes=len(observed),maximumInstructions=max(r['maximumInstructions']for r in cases),cpu='ARM946',instructionBound=2000000,freshMachinePerExecution=True,fullOriginalSourceNonstackRamAndTraceEquality=True,independentCallerFieldsAndNativeCommit=True,independentFullCallerNonstackRam=False,independentPreparationBuilderFullNonstackRam=True,compiledNegativeControls=controls,results=cases,limits=['All256 raw controller dispatch bytes,phase/menu/kind/list-count branches and supported original replacement paths are synthetic inputs;real UI reachability remains unproven','Original commit22900C,record/sort/skill/stat/tally/gold functions execute;UI/file/audio callbacks remain explicit supplied no-effects providers,with required zeroR1 contracts','Preparation runs original builder only for dispatch6;its returns/providers are separately counted andnever added to caller proof totals','Independent models cover caller return/state/loop inputs,alllive records/groups/counter/RNG atoriginal commit boundary,reverse packed skill slots,gold/tally andraw33 writer;full final RAM is paired original/source,butremaining stat/bitmap/UI interpretations are not independently semantically modeled','Scratch+33 is supplied and preserved;original commit copies it to new saved record,then accepted main633C8 clears saved+33 withoriginal STRB at0206341C;this is no scratch initializer or universal lifecycle claim','Existingmain633C8/100 isalready accepted saved_record_derived_refresh,so newsource credit excludes it;accepted94-v2 overlap barriers findbothbirth callersclear','Positive skill counts0..3,negative rawcounts128/255,distinct validparents,validallocation/counter andmappedUI pointers are exercised;largerpositivecounts,null/brokenrecords,exhaustion,UIDwrapandduplicateparents remain unsupported','No byte patches,assembly,volatile,register forcing,shared registry or accepted-source edits'])
    row['oracle']=oracle
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=metadata['sha256'],matches=[row],proposedSourceBytes=1460,acceptedSourceCredit=0,inputPins=pins['files'],generatorSha256=sha256(__file__),reproductionCommand='python match_ov000_birth395_20261031.py')
    write_json(ROOT/'evidence/matches/ov000-20261031-birth395.json',report)
    print(json.dumps({key:oracle[key]for key in['actualReturns','nativeDependencyActualReturns','providedCalls','preparationActualReturns','observedCodeBytes','maximumInstructions']}))

if __name__=='__main__':run()
