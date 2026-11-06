import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import main_dispatch481_machine_20261101 as M
import main_dispatch481_models_20261101 as P
SOURCE=ROOT/'src/overlays/main_20261101_dispatch481/source.c'
WORK=ROOT/'work/ol481-proof'
PINS=ROOT/'evidence/verification/main-dispatch481-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'main','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('481 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('481 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('481 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='main'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('481 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=152
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    totalProviders=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native,original)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate,original)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns'] or native['providedEvents']!=candidate['providedEvents']:raise ValueError(('481 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        totalProviders+=nm['providedCalls']*2
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=144:raise ValueError(('481 incomplete own code',len(observed)*4))
    for tag in ['flag-bit','unlock-gate']:
        source=ROOT/'nonmatching/overlay-lane/20261101-dispatch481-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=dict(profiles[0],flags=2,flags24=1,afterB=0) if tag=='flag-bit' else profiles[0]
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result,original)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('481 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/main-dispatch481-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=original['main']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=152,isolatedLinkedBytes=152,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=144,literalBytes=8,functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,flagCallbackAndGlobalRereadOrder=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'main_dispatch481_machine_20261101.py'),modelSha256=sha256(ROOT/'main_dispatch481_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_main_dispatch481_20261101.py',limits=['Ordinary caller and genuine isolated MWLD match; full module acceptance is separate','Unsigned left shifts replace generated signed-left-shift UB while preserving target bytes; signed conversion/right shift follow pinned compiler target semantics','Original3B854 and3A5EC wrappers execute; lock/unlock,lower update/queues andcallback bodies are explicit providers','Provider mutations test rereads ofobject+0x110 flags andglobal0x020F4C88 pointer between callbacks andbefore release; supplied effects do not establish ordinary callback behavior','Physical R0 can be0 orlast supplied unlock result; no original semantic return orreal synchronization claim','Known input pointer words/order andall nonstack writes are independently modeled; raw extra registers retained without invented formal arities','No thread scheduling,hardware lock/interrupt,scene lifecycle orapplication policy claim','Two wrong controls normally return andfail independent model; top-level negativeEvidence is separate'])
    write_json(ROOT/'evidence/matches/main-20261101-dispatch481.json',report)
    print(json.dumps(dict(matchedBytes=152,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=2)))
if __name__=='__main__':run()
