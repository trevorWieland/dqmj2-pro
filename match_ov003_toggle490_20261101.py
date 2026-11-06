import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov003_toggle490_machine_20261101 as M
import ov003_toggle490_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov003_20261101_toggle490/source.c'
WORK=ROOT/'work/ol490-proof'
PINS=ROOT/'evidence/verification/ov003-toggle490-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov003','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('490 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('490 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('490 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='ov003'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('490 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=84
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    totalProviders=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns'] or native['providedEvents']!=candidate['providedEvents'] or native['helperWords']!=candidate['helperWords']:raise ValueError(('490 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        totalProviders+=nm['providedCalls']*2
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'],helperWords=native['helperWords'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=72:raise ValueError(('490 incomplete own code',len(observed)*4))
    for tag in ['mask','word']:
        source=ROOT/'nonmatching/overlay-lane/20261101-toggle490-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=next(p for p in profiles if p['flag']==0x100 and not p['alias'] and p['state']==0)
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('490 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/ov003-toggle490-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov003',moduleSha256=original['module']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=84,isolatedLinkedBytes=84,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=72,functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,typedViewsAndFullWordPredicate=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov003_toggle490_machine_20261101.py'),modelSha256=sha256(ROOT/'ov003_toggle490_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov003_toggle490_20261101.py',limits=['One ordinary typed C function is genuinely isolated linked; module acceptance remains separate','All256 low-byte values plus eight full32-bit words,including upper-only nonzero values,are independently checked with zero providers','The native CMP tests the complete incoming word while STRB stores its low byte; no narrower original formal type is inferred','The object pointer may alias the raw-byte flag word in synthetic tests; the model preserves store/load ordering','Physical R0 is the raw signal base; the void source assigns no semantic return meaning','All72 own instruction bytes and12 literal bytes match; both native conditional paths execute','Complete nonstack effects,actual return,stack,ARM mode andcallee-saved registers are checked','Compiled controls change the bit mask or truncate the predicate; both return andfail the independent model','Mapped synthetic objects do not establish real resource ownership,scene reachability or initialization provenance'])
    write_json(ROOT/'evidence/matches/ov003-20261101-toggle490.json',report)
    print(json.dumps(dict(matchedBytes=84,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=2)))
if __name__=='__main__':run()
