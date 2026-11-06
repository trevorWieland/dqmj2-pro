import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import main_dispatch756_machine_20261101 as M
SOURCE=ROOT/'src/overlays/main_20261101_dispatch756/source.c'
WORK=ROOT/'work/ol756-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,private=False):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'main','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('756 compilation failed',rows))
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'canonical-link';bindings=qualified_bindings(row)
    if private:
        try:proof=validate(row,bindings,directory)
        except ValueError as error:
            if not isinstance(error.args[0],dict):raise
            proof=error.args[0]
        relocated,body=link_private(row,bindings,directory,WORK/name/'private-link',M.PRIVATE)
        return dict(source=row,canonicalComparison=proof,privateLink=relocated),body
    proof=validate(row,bindings,directory)
    return dict(**row,realLink=proof),(directory/'caller.bin').read_bytes()

def compact(result):
    return{key:result[key]for key in['profile','coreRegistersAndCpsr','nativeCalls','actualNativeReturnEvents','nonstackWrites','callbackEntries','callbackReturns','dispatcherObserved']}

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('756 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/main-dispatch756-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('756 pinned input differs',item['path']))
    selected=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor']=='arm9'and not row.get('program')and row['module']=='main'and max(row['address'],M.ENTRY)<min(row['address']+row['bytes'],M.ENTRY+M.SIZE)for row in selected):raise ValueError('756 selected overlap')
    original=M.B.inputs();packet,body=compile_unit(SOURCE,'positive');profiles=M.profiles();traces,cases=[],[];seen=set();helpers,callbacks,completed=0,0,0
    if len(body)!=72:raise ValueError('756 source size differs')
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body if flag else None).run()for flag in[False,True]];nm,cm=M.model(native),M.model(candidate)
        for key in['before','after','ioBefore','ioAfter','coreRegistersAndCpsr','nativeCalls','actualNativeReturnEvents','nonstackWrites','callbackEntries','callbackReturns']:
            if native[key]!=candidate[key]:raise ValueError(('756 complete physical comparison differs',key,profile['name']))
        if nm!=cm:raise ValueError('756 callback/node independent model differs')
        hc=nm['actualNativeHelperReturnInstructions']+cm['actualNativeHelperReturnInstructions'];cc=nm['callbackReturns']+cm['callbackReturns'];ec=nm['completedNativeHelperEntries']+cm['completedNativeHelperEntries'];helpers+=hc;callbacks+=cc;completed+=ec;seen.update(native['dispatcherObserved'])
        trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,allCoreRegistersCpsrRamIncludingStackAndIoShadowEqual=True,actuallyReturned=True);traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualNativeCallbackReturns=cc,actualNativeHelperReturnInstructions=hc,completedNativeHelperEntries=ec,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+68,4)):raise ValueError('756 own code coverage differs')
    text=SOURCE.read_text();controls=[]
    variants=[('wrong-precondition-loop',text.replace('    do {','    while ((rs->flag & 0x20U) == 0) {').replace('    } while ((rs->flag & 0x20U) == 0);','    }'),next(p for p in profiles if p['flags']==0x20)),('wrong-prepared-option-mask',text.replace('command & 0xE0U','command & 0x1FU'),profiles[1]),('wrong-cleared-bit',text.replace('~0x40U','~0x20U'),next(p for p in profiles if p['flags']==0x40))]
    for name,wrong_text,profile in variants:
        if wrong_text==text:raise ValueError('756 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-dispatch756-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=wrong_text:raise ValueError('756 frozen wrong source differs')
        source.write_text(wrong_text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wrong,wrong_body=compile_unit(source,name,True);result=M.Machine(original,profile,wrong_body,True).run()
        try:M.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('756 returning wrong source escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actualTopReturns=1,actuallyReturned=True,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/main-dispatch756-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=original['main']['sha256'],matches=[packet],canonicalMatchedFunctions=1,canonicalMatchedBytes=72,sourceCreditPendingIntegrator=72,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=helpers+callbacks,actualNativeCallbackReturns=callbacks,actualNativeHelperReturnInstructions=helpers,completedNativeEntryInvocations=completed+callbacks,providedCalls=0,allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackAndIoShadowEqual=True,allRawCallsAndOrderedWritesEqual=True,ownCoverage=dict(codeBytes=68,literalBytes=4,unclassifiedBytes=0),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['One genuine72-byte ordinary dispatcher source. Original NODEMIX1884,RET40,hardware/memory helpers and original14-entry table execute unchanged and receive zero duplicate source/data credit.', 'Actual original table lookup and BLX prepare R0=rs,R1=unsigned command byte&0xE0 for NODEMIX. All8 option classes and flags0/40/20/60/FFFFFFFF/80000000 are explicit synthetic inputs. NODEMIX overwrites incomingR1 before use; preparation does not establish it as a required callee input.', 'Original NODEMIX and optional following RET execute with no supplied calls. Node helper return instructions and callback returns are counted separately; tail-linked helper entries may complete on one instruction and are not added twice.', 'Independent754 matrix/nonstack/bus model runs on snapshots at actual NODEMIX entry and return,using actual dispatcher-produced R4/R5/R6 saved words. Outer flags and absence of other outer RAM/MMIO effects are checked independently.', 'RET callback slot at rs+0x10 is explicitly zero. Other commands/callbacks,malformed pointers,overflow,zero matrix count,busy/dirty hardware and full render/game-scene reachability are unsupported.', 'MMIO uses static ready clip/vector shadows. Three incidental matrix-send stack words remain physical storage evidence,not portable C matrix fields or semantic arguments. No GPU coherence or device execution claim.', 'Parent source/module/ROM/regression acceptance is still required; no existing source or preferences changed.'])
    write_json(ROOT/'evidence/matches/main-20261101-dispatch756.json',report);print(dict(matchedBytes=72,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeCallbackReturns=callbacks,actualNativeHelperReturnInstructions=helpers,totalActualNativeReturns=helpers+callbacks,completedNativeEntries=completed+callbacks,providedCalls=0,wrongActualReturns=len(controls)),flush=True)

if __name__=='__main__':execute()
