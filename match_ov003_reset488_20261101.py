import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov003_reset488_machine_20261101 as M
import ov003_reset488_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov003_20261101_reset488/source.c'
WORK=ROOT/'work/ol488-proof'
PINS=ROOT/'evidence/verification/ov003-reset488-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov003','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('488 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('488 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('488 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='ov003'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('488 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=76
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    totalProviders=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns'] or native['providedEvents']!=candidate['providedEvents'] or native['helperWords']!=candidate['helperWords']:raise ValueError(('488 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        totalProviders+=nm['providedCalls']*2
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'],helperWords=native['helperWords'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=76:raise ValueError(('488 incomplete own code',len(observed)*4))
    for tag in ['loop','bit']:
        source=ROOT/'nonmatching/overlay-lane/20261101-reset488-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=profiles[-1]
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('488 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/ov003-reset488-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov003',moduleSha256=original['module']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=76,isolatedLinkedBytes=76,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=76,functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,callerOrderAndAliasedResourceFlags=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov003_reset488_machine_20261101.py'),modelSha256=sha256(ROOT/'ov003_reset488_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov003_reset488_20261101.py',limits=['One ordinary caller is an isolated genuine MWLD match; whole module acceptance remains separate','All five caller helper invocations and original lower SDK bodies execute,including4B61C indirect tail to4B380; no providers or extra helper source credit','Synthetic mapped context/resources cover null groupA,array aliases,preview alias and arbitrary full flag words; no loaded-scene,resource ownership or hardware claim','Original first SDK group walks exactly three0x90-byte records when nonnull; the second accesses two records through actual5F98C index arithmetic','Physical R0 is measured as0x02000000 after loop termination; the reconstructed void signature does not assign semantic meaning','All76 own instruction bytes,complete nonstack effects,caller/helper input words and actual preserved-frame returns are required','Counter initialization before setup calls remains a53/76-byte negative compiler experiment; late initialization yields genuine76/76','Compiled returning controls change loop bound and one flag argument; controls remain top-level negativeEvidence'])
    write_json(ROOT/'evidence/matches/ov003-20261101-reset488.json',report)
    print(json.dumps(dict(matchedBytes=76,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=2)))
if __name__=='__main__':run()
