import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import main_query480_machine_20261101 as M
import main_query480_models_20261101 as P
SOURCE=ROOT/'src/overlays/main_20261101_query480/source.c'
WORK=ROOT/'work/ol480-proof'
PINS=ROOT/'evidence/verification/main-query480-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'main','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('480 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('480 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('480 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='main'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('480 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=132
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    totalProviders=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native,original)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate,original)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns'] or native['providedEvents']!=candidate['providedEvents']:raise ValueError(('480 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        totalProviders+=nm['providedCalls']*2
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'],outputPointer=native['outputPointer'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=132:raise ValueError(('480 incomplete own code',len(observed)*4))
    for tag in ['flag-bit','late-load']:
        source=ROOT/'nonmatching/overlay-lane/20261101-query480-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=profiles[-4] if tag=='flag-bit' else dict(profiles[1],mutate=True,cached=[0x02610000,0x02611000,0x02613000],flags=0)
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result,original)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('480 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/main-query480-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=original['main']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=132,isolatedLinkedBytes=132,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=132,functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,handleRelativeTableAndCacheOriginalHelpers=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'main_query480_machine_20261101.py'),modelSha256=sha256(ROOT/'main_query480_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_main_query480_20261101.py',limits=['Ordinary caller and genuine isolated MWLD match; full module acceptance is separate','Original handle lookup38D88,cache getter3917C,creation wrapper394F8,environment getter38D78 andcache setter391A4 execute; no new helper source credit','Validation3928C andlower factory39458 are explicit providers; their internal policies/construction are unsupported','Handle table counts/relative offsets,cache data,records,output pointers andprovider changes are supplied; no ordinary scene orAPI meaning is inferred','Return2 onlookup miss,nonzero validation code forwarding,return6 onzero creation result,andreturn0 oncached zero withoutput0 are separately modeled','Validation can change the record value; original caller reloads aftervalidation; writable output aliases row/cache/separate/null are qualified','Full input words andzero fifth validator word are retained; original formal typedefs andunexplored malformed table/pointer paths remain unresolved','Negative controls reside top-level; wrong-image extents dominate entry watches'])
    write_json(ROOT/'evidence/matches/main-20261101-query480.json',report)
    print(json.dumps(dict(matchedBytes=132,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=2)))
if __name__=='__main__':run()
