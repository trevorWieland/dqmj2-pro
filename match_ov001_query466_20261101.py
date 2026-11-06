import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_query466_machine_20261101 as M
import ov001_query466_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov001_20261101_query466/source.c'
WORK=ROOT/'work/ol466-proof'
PINS=ROOT/'evidence/verification/ov001-query466-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov001','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('466 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('466 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('466 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='ov001'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('466 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=176
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns']:raise ValueError(('466 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=176:raise ValueError(('466 incomplete own code',len(observed)*4))
    for tag in ['threshold','blocked']:
        source=ROOT/'nonmatching/overlay-lane/20261101-query466-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=profiles[-2]if tag=='threshold'else profiles[-1]
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('466 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/ov001-query466-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=original['module']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=176,isolatedLinkedBytes=176,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=0,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=176,functions=functions,cases=cases,wholeNonstackUnchanged=True,independentPredicate=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov001_query466_machine_20261101.py'),modelSha256=sha256(ROOT/'ov001_query466_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov001_query466_20261101.py',limitations=['Ordinary caller and genuine isolated MWLD bytes match; module acceptance is separate','All four original helpers execute with zero provider bodies and zero new helper source credit','Supplied pointer arrays,actor/descriptor bytes,command tables and signed count/list state are synthetic; no ordinary scene reachability or lifecycle is inferred','Context+0x14 is a measured nonzero32-bit gate; actor+0x31C/+0x1FF/descriptor+0xAC validity and descriptor+0x97<=3 are raw byte predicates','Native0x77 remains a raw unsigned16 action ID; no ability name or application restriction is inferred','Command-pair bytes are read signed; actor side/slot bytes are unsigned; raw0xFF side and raw0x80/0xFF counts retain that distinction','Accepted helpers and source interfaces remain unchanged; full substituted code extents dominate entry watches in controls'])
    write_json(ROOT/'evidence/matches/ov001-20261101-query466.json',report)
    print(json.dumps(dict(matchedBytes=176,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=0,negativeActualTopReturns=2)))
if __name__=='__main__':run()
