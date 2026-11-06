import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov006_list535_machine_20261101 as M
import ov006_list535_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov006_20261101_list535/list.c'
WORK=ROOT/'work/ol535-proof'
PINS=ROOT/'evidence/verification/ov006-list535-inputs-20261101.json'


def encoded(v):return json.dumps(v,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov006','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('535 compiler failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def run():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('535 runtime differs')
    for item in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('535 frozen input differs',item['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort103-identities-v2-20261101.json';selected=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov006'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in selected):raise ValueError('535 accepted overlap')
    original=M.inputs()
    if original['main']['sha256']!='ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'or original['module']['sha256']!='fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341':raise ValueError('535 module identity differs')
    row,proof,body=compile_unit(SOURCE,'caller',True);row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=M.SIZE;profiles=P.profiles();traces=[];cases=[];controls=[];observed=set();totalReturns=0;totalProviders=0
    if body!=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]:raise ValueError('535 genuine current image differs')
    for p in profiles:
        native=M.Machine(original,p).run();nm=P.model(native,original);candidate=M.Machine(original,p,body).run();cm=P.model(candidate,original)
        if nm!=cm or native['nativeReturns']!=candidate['nativeReturns']or native['providedEvents']!=candidate['providedEvents']or native['nonstackWrites']!=candidate['nonstackWrites']or native['after']!=candidate['after']:raise ValueError(('535 original/C complete state differs',p['name']))
        observed.update(native['ownObserved']);deps=len(native['nativeReturns'])+len(candidate['nativeReturns']);totalReturns+=deps;totalProviders+=len(native['providedEvents'])+len(candidate['providedEvents']);trace=dict(profile=p,model=nm,nativeReturns=native['nativeReturns'],nativeInstructions=native['instructions'],sourceInstructions=candidate['instructions'],providedEvents=native['providedEvents'],nonstackWrites=native['nonstackWrites'],clearPreparedWords=native['clearWords'],completeRamSha256=c.sha(native['after']),ownObserved=native['ownObserved']);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualNativeDependencyReturns=deps,providedCalls=nm['providedCalls']*2,traceSha256=c.sha(encoded(trace))))
    if len(observed)*4!=216:raise ValueError(('535 own code coverage differs',len(observed)*4))
    for tag,profileName in[('id','prefix-1'),('stride','prefix-64'),('signed','after--1')]:
        source=ROOT/'nonmatching/overlay-lane/20261101-list535-controls'/tag/'list.c';bad,bp,code=compile_unit(source,tag,False);p=next(p for p in profiles if p['name']==profileName);result=M.Machine(original,p,code).run();rejection=None
        try:P.model(result,original)
        except ValueError as error:rejection=str(error)
        if rejection is None:raise ValueError(('535 wrong returning C passed',tag))
        controls.append(dict(tag=tag,source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source),compilation=bad,link=bp,profile=p['name'],actualTopReturns=1,actualNativeDependencyReturns=len(result['nativeReturns']),providedCalls=len(result['providedEvents']),rejected=True,rejection=rejection))
    functions=[]
    for address,meta in sorted(original['ranges'].items()):
        functions.append(dict(address=hex(address),processor='arm9',program='',moduleSha256=original['main']['sha256'],**meta,sha256=c.sha(original['arm'][address-M.BASE:address-M.BASE+meta['bytes']]),sourceCredit=0))
    payload=encoded(traces);archive=ROOT/'evidence/generated/ov006-list535-native-traces-20261101.json.gz';archive.write_bytes(gzip.compress(payload,mtime=0));report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov006',moduleSha256=original['module']['sha256'],matches=[row],matchedFunctions=1,matchedBytes=M.SIZE,isolatedLinkedBytes=M.SIZE,wholeModuleLinked=False,oracle=dict(pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,actualReturnAndFrameRequired=True,freshMachinePerExecution=True,cpu='ARM946',instructionBound=50000,maxInstructions=max(max(t['nativeInstructions'],t['sourceInstructions'])for t in traces),observedOwnCodeBytes=216,observedOwnInstructionAddresses=[hex(a)for a in sorted(observed)],nativeLiteralWords=[dict(address='0x02204F20',value='0x0221C1F0',bytes=4)],functions=functions,cases=cases,wholeNonstackEffectsIndependentlyModeled=True,wholeRamOriginalSourceEqual=True,originalRecordClassificationsIndependentlyModeled=True,sourceRecordBase=hex(original['table']),recordBytes=12,recordCount=64,traceArchive=dict(path=archive.relative_to(ROOT).as_posix(),sha256=sha256(archive),decodedSha256=c.sha(payload))),negativeEvidence=dict(compiledReturningControls=controls,actualTopReturns=3,acceptedSourceCredit=0),generatorSha256=sha256(__file__),fixtureSha256=sha256(ROOT/'ov006_list535_machine_20261101.py'),modelSha256=sha256(ROOT/'ov006_list535_models_20261101.py'),inputPins=dict(path=PINS.relative_to(ROOT).as_posix(),sha256=sha256(PINS)),acceptedSnapshot=dict(path=snapshot.relative_to(ROOT).as_posix(),sha256=sha256(snapshot)),reproductionCommand='python match_ov006_list535_20261101.py',limits=['One ordinaryC unit genuinely links all220 bytes; full module acceptance remains separate','Measured256-byte stack array has64 words; omitted generated declaration is repaired withoutpadding orbyte encoding','The actual original clear,classifier,bounded recordlookup andall ARM/Thumb predicate helpers execute; onlytheallocator call is supplied','685C8 validates signed indices0..63 via68594 andcomputes63EA4 base+12*index; recordbase021BB2B8 is initialized withdeterministic synthetic12-byte records','Independent native flags are(word0>>11)&1FFFFF; rawkind isflags&3,with additional masks0x04,0x08,0x10 selecting rawclassifier results3/4/5; no identifier orability semantics inferred','The caller selects every nonzero rawclassification andwrites ordinalindex+1 at outputrecord offset0x08,stride0x0C,leaving otherbytes unchanged','Zero selected count skips allocation andphysically returns0221C1F0; nonzero paths return thepostallocation signedcountword,including0/FFFFFFFF inexplicit mutation profiles','Allocator prepares threefull words1,count*12,4; returned buffers andcount mutations are declared testcontracts,not observed original allocator behavior','The supplied allocator returns at least768 mappedbytes evenwhenrequested size issmaller; postallocation count islimited to-1 or0..64 andmay consumezero-padded localarray entries','Aliased output into theinputrecord table is tested after all64 classifications; each run has isolated full machine state','Null allocation,counts above64,arbitrary heap ownership andoriginal allocation failures remain unsupported; no hardware error-path claim','Thumb96D9C tail-veneer and96CF8 share one physical return frame; aliasentries are retained withoutdouble-counting','All216 native instructionbytes areobserved and4 literalbytes match; profilecoverage isnot exhaustive game reachability','Three compiled returningcontrols alter theordinalID,stride,or signedpostallocation guard; full negative evidence stays top-level','No original assets,saved records,scene state,application meanings orUI changes are claimed'])
    write_json(ROOT/'evidence/matches/ov006-20261101-list535.json',report);print(json.dumps(dict(matchedBytes=M.SIZE,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=totalReturns,providedCalls=totalProviders,negativeActualTopReturns=3)))

if __name__=='__main__':run()
