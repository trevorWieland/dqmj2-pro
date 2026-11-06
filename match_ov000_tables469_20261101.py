import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov000_tables469_machine_20261101 as M
import ov000_tables469_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov000_20261101_tables469/source.c'
WORK=ROOT/'work/ol469-proof'
PINS=ROOT/'evidence/verification/ov000-tables469-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('469 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('469 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('469 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='ov000'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('469 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=196
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    totalProviders=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns'] or native['providedEvents']!=candidate['providedEvents'] or native['freePreparedWords']!=candidate['freePreparedWords']:raise ValueError(('469 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        totalProviders+=nm['providedCalls']*2
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'],freePreparedWords=native['freePreparedWords'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=184:raise ValueError(('469 incomplete own code',len(observed)*4))
    for tag in ['word-width','null-filter']:
        source=ROOT/'nonmatching/overlay-lane/20261101-tables469-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=profiles[3]
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('469 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/ov000-tables469-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=196,isolatedLinkedBytes=196,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=184,literalBytes=12,functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,explicitResourceAndFreeCallWordsChecked=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),pointerTables=[dict(module='ov000',addressHex='0x02246348',elementCount=22,elementWidthBytes=4,view='opaque ARM32 data addresses',nativeLoopBound=22),dict(module='ov000',addressHex='0x0224632C',elementCount=5,elementWidthBytes=4,view='opaque ARM32 data addresses',nativeLoopBound=5)],generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov000_tables469_machine_20261101.py'),modelSha256=sha256(ROOT/'ov000_tables469_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov000_tables469_20261101.py',limitations=['Ordinary caller and isolated genuine MWLD bytes match; full module gate is separate','Actual main2A498 empty-entry error path executes for every attempted release; live2B4E8 path is guarded unsupported','Four unique resource handlers are explicit providers; their bodies and real ownership/lifetime effects are not counted','First22 nonzero pointers are dereferenced only at unsigned byte0x81 before recorded calls; null first entries are skipped; second5 entries call handlers even for zero','Pointer tables are supplied synthetic BSS values; no initialized-data source credit or ordinary allocation/scene state is claimed','Physical final R0 equals the last native empty-entry result in this domain; semantic original return meaning remains unproved','Complete table word clears,full call words,other nonstack effects and preserved register returns are independently checked','Wrong controls reside at top-level negativeEvidence; entire substituted images dominate native entry watches'])
    write_json(ROOT/'evidence/matches/ov000-20261101-tables469.json',report)
    print(json.dumps(dict(matchedBytes=196,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=2)))
if __name__=='__main__':run()
