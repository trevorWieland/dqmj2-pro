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
import ov000_birth388_fixture_20261031 as F
import ov000_birth388_models_20261031 as M
SOURCE=ROOT/'src/overlays/ov000_20261031_birth388/source.c'
WORK=ROOT/'work/ol388-proof'
PINS=ROOT/'evidence/verification/ov000-birth388-inputs-20261031.json'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov000','2','off',True,thumb=False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('Birth388 compiler failed')
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
    obj=F.Machine(arm,save,assets,overlay,p,body);result=obj.run();result['model']=M.check(obj,result,assets)
    after=bytes(obj.u.mem_read(F.BASE,0x800000));cut=F.STACK-0x10000-F.BASE;end=F.STACK+0x1000-F.BASE
    result['_ram']=after[:cut]+after[end:]
    del obj
    return result


def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('Birth388 pinned runtime differs')
    pins=json.loads(PINS.read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError('Birth388 frozen input/source differs')
    arm,save,assets=F.inputs();metadata,overlay,unused=measured_module('ov000')
    row,proof,body=compile_unit(SOURCE,'caller',True);row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=1244
    if len(body)!=1244:raise ValueError('Birth388 entire native caller extent differs')
    cases=[];observed=set()
    for index,p in enumerate(F.profiles()):
        original=execute(arm,save,assets,overlay,p);candidate=execute(arm,save,assets,overlay,p,body)
        if original!=candidate:raise ValueError(('Birth388 complete original/source effect/trace differs',p))
        original.pop('_ram');observed.update(original['observedCodeBytes'])
        raw=encoded(original);zipped=gzip.compress(raw,mtime=0);path=WORK/'raw-traces'/(c.sha(zipped)+'.json.gz');path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(zipped)
        cases.append(dict(profile=p,actualReturns=2,nativeDependencyActualReturns=2*original['nativeDependencyActualReturns'],providedCalls=2*original['providedCalls'],maximumInstructions=original['steps'],nestedBuilderActualReturns=2*len(original['builderChecks']),independentModel=original['model'],scratch33Writes=0,rawTraceArtifact=dict(path=str(path.relative_to(ROOT)),sha256=c.sha(zipped),uncompressedSha256=c.sha(raw),bytes=len(zipped),gzipMtime=0)))
        del original,candidate;gc.collect()
        if index%100==0:print(json.dumps(dict(completedPairs=index+1)),flush=True)
    controls=[]
    recipes=F.profiles()
    erased_case=next(p for p in recipes if p['phase']==1 and p['action']==2 and p['option']==1 and not p.get('outAlias'))
    for name,old,new,p in[('output-word','*arg0 = 0;','*arg0 = 1;',recipes[0]),('erased-predicate-input','native_fn_ov000_022207a0(native_data_ov000_022460d4, M2C_FIELD(native_data_ov000_02246090, s32 *, 0x20));','native_fn_ov000_022207a0();',erased_case)]:
        folder=ROOT/'nonmatching/overlay-lane/20261031-birth388-negative'/name;folder.mkdir(parents=True,exist_ok=True)
        source=SOURCE.read_text();header=SOURCE.with_name('context.h').read_text()
        if source.count(old)!=1:raise ValueError('Birth388 compiled control pattern differs')
        source=source.replace(old,new)
        if name=='erased-predicate-input':header=header.replace('extern u32 native_fn_ov000_022207a0(void *, s32);','extern u32 native_fn_ov000_022207a0();')
        for path,text in[(folder/'source.c',source),(folder/'context.h',header)]:
            if path.exists()and path.read_bytes()!=text.encode():raise ValueError('Birth388 preserve frozen compiled controls')
            path.write_bytes(text.encode())
        bad,bad_proof,bad_body=compile_unit(folder/'source.c','negative-'+name,False)
        try:execute(arm,save,assets,overlay,p,bad_body)
        except (ValueError,unicorn.UcError)as error:
            failure=str(error)
            if name=='output-word'and'Birth388 independent caller field differs'not in failure:raise
            if name=='erased-predicate-input'and'UC_ERR_READ_UNMAPPED'not in failure and'required predicate input contract differs'not in failure:raise
        else:raise ValueError('Birth388 compiled control unexpectedly passed')
        controls.append(dict(name=name,profile=p,compilation=bad,genuineLinkComparison=bad_proof,rejected=True,failure=failure,sourceCredit=0))
    oracle=dict(pairs=len(cases),actualReturns=2*len(cases),nativeDependencyActualReturns=sum(r['nativeDependencyActualReturns']for r in cases),providedCalls=sum(r['providedCalls']for r in cases),nestedBuilderActualReturns=sum(r['nestedBuilderActualReturns']for r in cases),observedCodeBytes=len(observed),maximumInstructions=max(r['maximumInstructions']for r in cases),cpu='ARM946',instructionBound=500000,freshMachinePerExecution=True,fullOriginalSourceNonstackRamAndTraceEquality=True,independentCallerFieldsAndPredicate=True,independentFullCallerNonstackRam=False,independentNestedBuilderFullNonstackRam=True,compiledNegativeControls=controls,results=cases,limits=['All256 signed-byte dispatch patterns,normal actions0..3,ready/policy values,bit16/category2,level9/10 branches and aligned output aliases are synthetic supported inputs;larger action indices,null output and broken records remain unsupported','Original022207A0 consumesctxR0 and conditionalR1;main48F7C cleanu8 andC484C byte effect are separately measured bybyte385,not global type migrations','UI/file/window/input/audio callbacks are explicitly supplied with no effects;native frame and ordinary scene reachability are not established','Original skill-selection022298EC and builder02229100 execute;caller forwards observed native selection result,whose skill contents are not independently semantically modeled','Every nested builder effect is independently modeled using frozen330 mathematical/stat/field model;all whole-caller nonstackRAM and traces compare original/source,but native skill-output/rebuild bitmap meanings are not independently modeled','Scratch+33 is deliberately supplied and no original write is observed in this scope;unknown real UI callback initialization/lifecycle remains unresolved;this does not infer a default,gender,validity oreligibility label','100saved record+33 bytes remain unchanged;the separate336 destructive-copy proof is not initialization evidence','Tail aliases sharing one physical return frame are recorded without extra native-return counts;providers receive zero native/source credit'])
    row['oracle']=oracle
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=metadata['sha256'],matches=[row],proposedSourceBytes=1244,acceptedSourceCredit=0,inputPins=pins['files'],generatorSha256=sha256(__file__),reproductionCommand='python match_ov000_birth388_20261031.py')
    write_json(ROOT/'evidence/matches/ov000-20261031-birth388.json',report)
    print(json.dumps({key:oracle[key]for key in['actualReturns','nativeDependencyActualReturns','providedCalls','nestedBuilderActualReturns','observedCodeBytes','maximumInstructions']}))

if __name__=='__main__':run()
