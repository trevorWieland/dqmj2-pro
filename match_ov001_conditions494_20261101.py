import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_conditions494_machine_20261101 as M
import ov001_conditions494_models_20261101 as P
WORK=ROOT/'work/ol494-proof'
PINS=ROOT/'evidence/verification/ov001-conditions494-inputs-20261101.json'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov001','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('494 compile failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    out=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),out)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(out/'caller.bin').read_bytes()


def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('494 runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('494 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json';selected=json.loads(snapshot.read_text())['functions'];original=M.inputs();matches=[];traces=[];cases=[];controls=[];observed={};deps=0
    profiles=P.profiles()
    for entry,size in M.SUBJECTS.items():
        if any(r['processor']=='arm9'and not r['program']and r['module']=='ov001'and max(r['address'],entry)<min(r['address']+r['bytes'],entry+size)for r in selected):raise ValueError('494 already selected')
        source=ROOT/'src/overlays/ov001_20261101_conditions494'/format(entry,'08x')/'source.c'
        row,proof,body=compile_unit(source,format(entry,'08x'),True);row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=size;matches.append(row);observed[entry]=set()
        for p in profiles:
            native=M.Machine(original,p,entry).run();nm=P.model(native);candidate=M.Machine(original,p,entry,body).run();cm=P.model(candidate)
            if nm!=cm or native['nativeReturns']!=candidate['nativeReturns']or native['helperWords']!=candidate['helperWords']:raise ValueError(('494 native/source differs',p['name']))
            observed[entry].update(native['ownObserved']);count=len(native['nativeReturns'])+len(candidate['nativeReturns']);deps+=count
            result=dict(entry=hex(entry),profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],policyInputWords=native['helperWords']);traces.append(result);cases.append(dict(entry=hex(entry),profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=count,traceSha256=c.sha(encoded(result))))
        if len(observed[entry])*4!=size:raise ValueError(('494 incomplete own code',hex(entry),len(observed[entry])*4,size))
        for tag in['tag','selector']:
            wrong=ROOT/'nonmatching/overlay-lane/20261101-conditions494-controls'/format(entry,'08x')/tag/'source.c';bad,bp,code=compile_unit(wrong,format(entry,'08x')+'-'+tag,False);p=next(p for p in profiles if p['name']==('base'if tag=='selector'else'tag-slot1-n1-at0'));result=M.Machine(original,p,entry,code).run();rejection=None
            try:P.model(result)
            except ValueError as error:rejection=str(error)
            if rejection is None:raise ValueError('494 wrong returning control passed')
            controls.append(dict(entry=hex(entry),tag=tag,source=wrong.relative_to(ROOT).as_posix(),sourceSha256=sha256(wrong),compilation=bad,link=bp,actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces);archive=ROOT/'evidence/generated/ov001-conditions494-native-traces-20261101.json.gz';archive.write_bytes(gzip.compress(payload,mtime=0));functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY);functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=original['module']['sha256'],matches=matches,matchedFunctions=2,matchedBytes=400,isolatedLinkedBytes=400,wholeModuleLinked=False,oracle=dict(pairs=len(profiles)*2,actualTopReturns=len(profiles)*4,actualNativeDependencyReturns=deps,providedCalls=0,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(x['nativeInstructions'],x['sourceInstructions'])for x in traces),observedOwnCodeBytes={hex(k):len(v)*4 for k,v in observed.items()},functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=4,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov001_conditions494_machine_20261101.py'),modelSha256=sha256(ROOT/'ov001_conditions494_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov001_conditions494_20261101.py',limits=['Two ordinary C callers are isolated genuine linked matches; shared module acceptance remains separate','All original policy,validity,status andraw-global helpers execute,with zero providers andzero additional source credit','Synthetic context+4 supplies a three-actor base with0x440 stride; no ordinary battle reachability orloaded formation is inferred','Initial native policy reads signed bytes at actor+0x232 or+0x235; its result is modeled independently fromnative state','The raw0x39/0x3A tag scans andstatus bytes retain address-qualified meanings; no ability names orbusiness semantics areassigned','Count0..255 tests include deliberately mapped cross-record read spans for malformed high counts; no game-valid maximum is inferred','No concurrent mutation orinterrupt paths are tested; repeated status reads remain in exactsource','Four compiled returning controls alter target tags orpolicy selector inputs; full metadata stays top-level negativeEvidence','All400 instruction bytes,actual return,stack,ARM mode,callee-saved registers andunchanged nonstack memory are required'])
    write_json(ROOT/'evidence/matches/ov001-20261101-conditions494.json',report);print(json.dumps(dict(matchedBytes=400,pairs=len(profiles)*2,actualTopReturns=len(profiles)*4,actualNativeDependencyReturns=deps,providedCalls=0,negativeActualTopReturns=4)))

if __name__=='__main__':run()
