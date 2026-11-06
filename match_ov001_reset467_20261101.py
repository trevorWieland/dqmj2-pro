import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_reset467_machine_20261101 as M
import ov001_reset467_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov001_20261101_reset467/source.c'
WORK=ROOT/'work/ol467-proof'
PINS=ROOT/'evidence/verification/ov001-reset467-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov001','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('467 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('467 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('467 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='ov001'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('467 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=172
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    totalProviders=0
    totalEmptyFree=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns'] or native['providedEvents']!=candidate['providedEvents'] or native['freePreparedWords']!=candidate['freePreparedWords']:raise ValueError(('467 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        totalProviders+=nm['providedCalls']*2
        totalEmptyFree+=nm['actualEmptyEntryFreeReturns']*2
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'],freePreparedWords=native['freePreparedWords'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=168:raise ValueError(('467 incomplete own code',len(observed)*4))
    for tag in ['second-word','gate']:
        source=ROOT/'nonmatching/overlay-lane/20261101-reset467-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=profiles[-1]
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('467 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/ov001-reset467-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    arm=original['arm']
    flow=dict(schemaVersion=1,processor='arm9',program='',generatorSha256=sha256(__file__),reproductionCommand='python match_ov001_reset467_20261101.py',rawGetterByte=dict(module='main',mode='arm',addressHex='0x02041814',objectHex='0x020F60EC',offsetHex='0x02',fieldHex='0x020F60EE',widthBytes=1,signedness='unsigned8 LDRB,zeroextended R0'),romSha256=configuration()['romSha256'],mainSha256=original['main']['sha256'],overlaySha256=original['module']['sha256'],caller=dict(module='ov001',mode='arm',addressHex='0x02203E7C',bytes=172,sourceWord=dict(baseHex='0x0223D8EC',offsetHex='0x04',widthBytes=4,signedness='raw unsigned32 physical bits; original typedef unasserted'),nativeLoadPcHex='0x02203EE8',register='R1',callee='main:arm:0x0202A498',callerPreparedWords=[2,'word4']),conditionalForwarding=dict(module='main',entryHex='0x0202A498',bytes=132,sha256=c.sha(arm[0x2A498:0x2A51C]),callPcHex='0x0202A4CC',calleeHex='0x0202B4E8',incomingR1UnchangedBeforeCall=True,pathCondition='Selected arena table entry is nonzero; this live path is NOT executed by the fixture'),leafConsumption=dict(module='main',entryHex='0x0202B4E8',bytes=60,sha256=c.sha(arm[0x2B4E8:0x2B524]),firstReadPcHex='0x0202B4F0',instruction='SUB R4,R1,#0x10',instructionHex=arm[0x2B4F0:0x2B4F4].hex(),executionStatus='Static measured input use only; live free remains unsupported'),scope='Explicit caller-specific ARM32 two-word drafting view; no original formal type, general API extent or successful heap-cleanup claim',sourceCredit=0)
    flowPath=ROOT/'evidence/verification/ov001-reset467-transitive-word-20261101.json'
    write_json(flowPath,flow)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov001',moduleSha256=original['module']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=172,isolatedLinkedBytes=172,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,actualEmptyArenaFreeReturnsWithinDependencyTotal=totalEmptyFree,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=168,literalBytes=4,functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,callerSpecificSecondWordIndependentlyRequired=True,all256RawGetterByteValues=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),transitiveInputEvidence=dict(path=flowPath.relative_to(ROOT).as_posix(),sha256=sha256(flowPath)),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov001_reset467_machine_20261101.py'),modelSha256=sha256(ROOT/'ov001_reset467_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov001_reset467_20261101.py',limitations=['Ordinary caller and genuine isolated MWLD bytes match; module acceptance is separate','Actual original raw getter41814/helper417F8 and main2A498 empty-entry error path execute; live2B4E8 free is guarded unsupported','Five unique resource/UI/preparation services are explicit no-body providers,ten calls per normal context; unknown formal arities remain unasserted and physical words retained','All256 synthetic raw bytes execute; exactly1 returns0 before services,others return1 under supplied provider behavior','Context+0x01 raw byte clears and context+0x04 raw word clears; actual empty-entry allocator writes unsigned8 value1 at0x020EDD54+0x02 when called; other nonstack effects are forbidden','The measured caller prepares R1 even though the tested empty-entry callee does not consume it; static live-path forwarding/leaf read supports preserving it,without claiming tested live cleanup','No ordinary scene,RNG future state,successful heap release,invalid-pointer validity or application policy claim','Whole substituted-code intervals dominate entry watches; wrong controls are separate top-level negative evidence'])
    write_json(ROOT/'evidence/matches/ov001-20261101-reset467.json',report)
    print(json.dumps(dict(matchedBytes=172,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=2)))
if __name__=='__main__':run()
