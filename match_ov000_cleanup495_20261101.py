import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT, configuration, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov000_cleanup495_machine_20261101 as M
import ov000_cleanup495_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov000_20261101_cleanup495/source.c'
WORK=ROOT/'work/ol495-proof'
PINS=ROOT/'evidence/verification/ov000-cleanup495-inputs-20261101.json'

def encoded(v):
    return json.dumps(v,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov000','2','off',False)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('495 compiler failed')
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()

def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('495 pinned runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('495 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort99-identities-v2-20261101.json'
    selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r['program']and r['module']=='ov000'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('495 subject already selected')
    original=M.inputs()
    row,proof,body=compile_unit(SOURCE,'caller',True)
    row['genuineLinkComparison']=freeze_link(proof)
    row['exactBytes']=284
    profiles=P.profiles()
    traces,cases,controls,observed=[],[],[],set()
    totalReturns=0
    totalProviders=0
    for p in profiles:
        native=M.Machine(original,p).run()
        nm=P.model(native)
        candidate=M.Machine(original,p,body).run()
        cm=P.model(candidate)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns'] or native['providedEvents']!=candidate['providedEvents'] or native['helperWords']!=candidate['helperWords']:raise ValueError(('495 original/source contract differs',p['name']))
        observed.update(native['ownObserved'])
        deps=len(native['nativeReturns'])+len(candidate['nativeReturns'])
        totalReturns+=deps
        totalProviders+=nm['providedCalls']*2
        result=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'],helperWords=native['helperWords'])
        traces.append(result)
        cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,traceSha256=c.sha(encoded(result))))
    if len(observed)*4!=276:raise ValueError(('495 incomplete own code',len(observed)*4))
    for tag in ['mask','predicate']:
        source=ROOT/'nonmatching/overlay-lane/20261101-cleanup495-controls'/tag/'source.c'
        bad,bp,code=compile_unit(source,tag,False)
        p=profiles[-1]if tag=='mask'else profiles[0]
        result=M.Machine(original,p,code).run()
        rejection=None
        try:P.model(result)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('495 compiled wrong C passed model',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),rejected=True,rejection=rejection))
    payload=encoded(traces)
    archive=ROOT/'evidence/generated/ov000-cleanup495-native-traces-20261101.json.gz'
    archive.write_bytes(gzip.compress(payload,mtime=0))
    functions=[]
    for a,r in sorted(original['ranges'].items()):
        image,base=(original['arm'],M.BASE)if r['module']=='main'else(original['overlay'],M.OVERLAY)
        functions.append(dict(address=hex(a),**r,sha256=c.sha(image[a-base:a-base+r['bytes']])))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=284,isolatedLinkedBytes=284,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=20000,maxInstructions=max(max(r['nativeInstructions'],r['sourceInstructions'])for r in traces),observedOwnCodeBytes=276,functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,fullWordFreeInputsAndAddressPredicate=True,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=2,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov000_cleanup495_machine_20261101.py'),modelSha256=sha256(ROOT/'ov000_cleanup495_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov000_cleanup495_20261101.py',limits=['One ordinary C caller genuinely links all284 bytes; module acceptance remains separate','Actual 2A498 arena1 empty-entry paths,84F4C/84F60 tail wrappers and88578 byte setter execute; lower84F9C release is an explicit provider','The final predicate compares literal address0223852B itself against zero; it does not read the byte stored at that address','Arbitrary full R1 pointer words are preserved,but live heap release2B4E8 is guarded unsupported','Provider mutation of the second global pointer exercises latest loads and resource aliasing; supplied callback effects are test contracts,not observed original release behavior','Own four-word zeroing and provider-entry word snapshots are independently checked,including aliasing of both resources','Empty-entry failure writes constant status byte020EDD56 regardless of arena index; the initial wrong model offset is retained','All276 instruction bytes plus8 literal bytes match,with complete nonstack effects and actual preserved-frame returns','Returning compiled controls change the accumulated bit or change the address predicate to a byte read; full negative evidence stays top-level','No successful heap free,hardware,scene or resource ownership claim is made'])
    write_json(ROOT/'evidence/matches/ov000-20261101-cleanup495.json',report)
    print(json.dumps(dict(matchedBytes=284,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=2)))
if __name__=='__main__':run()
