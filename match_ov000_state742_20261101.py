import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_state742_machine_20261101 as M
import ov000_state742_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov000_20261101_state742/source.c'
WORK=ROOT/'work/ol742-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def compile_unit(source,name,private=False):
    c.WORK=WORK/name/'compile';rows,u=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('742 compilation failed',rows))
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];bindings=qualified_bindings(row);directory=WORK/name/'canonical-link'
    if private:
        try:proof=validate(row,bindings,directory)
        except ValueError as error:
            if not isinstance(error.args[0],dict):raise
            proof=error.args[0]
        linked,body=link_private(row,bindings,directory,WORK/name/'private-link',M.PRIVATE)
        return dict(source=row,canonicalComparison=proof,privateLink=linked),body
    proof=validate(row,bindings,directory)
    return dict(**row,realLink=proof),(directory/'caller.bin').read_bytes()
def compact(result):return{key:result[key]for key in['profile','coreRegistersAndCpsr','nativeCalls','watchedNativeReturns','nonstackWrites','ownObserved','nativeObserved','instructions']}|dict(finalState=result['finalState'].hex())

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('742 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov000-state742-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('742 pinned input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov000'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in accepted):raise ValueError('742 accepted overlap')
    original=M.B.inputs()
    if original['module']['sha256']!=pins['ov000Sha256']:raise ValueError('742 module image differs')
    packet,body=compile_unit(SOURCE,'positive')
    if len(body)!=M.SIZE:raise ValueError('742 matched body has wrong size')
    profiles=P.profiles();traces,cases=[],[];seen=set();dependencies=0
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body if candidate else None).run()for candidate in[False,True]];nm,cm=P.model(native),P.model(candidate)
        if nm!=cm or native['before']!=candidate['before']or native['after']!=candidate['after']or native['coreRegistersAndCpsr']!=candidate['coreRegistersAndCpsr']or native['nativeCalls']!=candidate['nativeCalls']or native['watchedNativeReturns']!=candidate['watchedNativeReturns']or native['nonstackWrites']!=candidate['nonstackWrites']:raise ValueError('742 complete physical comparison differs')
        count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns']);dependencies+=count;seen.update(native['ownObserved']);trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,fullRamIncludingStackAndAllRegistersEqual=True,allRawCallsAndOrderedWritesEqual=True);traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualWatchedNativeDependencyReturns=count,providedCalls=0,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+192,4)):raise ValueError('742 own code coverage differs')
    template=SOURCE.read_text();controls=[];variants=[('wrong-active-only-one',template.replace('field20!=0','field20==1'),next(p for p in profiles if p['active']==0x80000000)),('wrong-negative-rounding',template.replace(')>>3',')/8'),next(p for p in profiles if p['active']==0 and p['secondary']==1)),('wrong-global-clamp',template.replace('native_fn_ov000_02219ce4(&target);','native_fn_ov000_02219ce4(&native_data_ov000_02245e54.field4c);'),profiles[0])]
    for name,text,profile in variants:
        if text==template:raise ValueError('742 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-state742-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('742 frozen wrong control differs')
        source.write_text(text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wrong,wrong_body=compile_unit(source,name,True);result=M.Machine(original,profile,wrong_body,True).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('742 returning wrong control escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actuallyReturned=True,actualTopReturns=1,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov000-state742-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=[packet],canonicalMatchedFunctions=1,canonicalMatchedBytes=200,sourceCreditPendingIntegrator=200,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=0,allOwnCodeObserved=dict(codeBytes=192,literalBytes=8,unclassifiedBytes=0),allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allRawCallsAndOrderedWritesEqual=True,cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['One genuine200-byte ordinary C caller; parent module/ROM/regression acceptance still required.', 'Original native02219CE4/140,021DF1F0/16 and021DF3BC/20 execute; three watched dependency returns per machine and0 providers. No new credit for existing helpers or738 bodies.', 'Synthetic current vector,reference vector,raw gates20/28,selected byte and14B row are initialized explicitly. No actual scene,field meaning,legal table extent or current state assertion.', 'All differences/additions fit signed32 in the supported corpus; signed negative right shift is the measured pinned-CW arithmetic shift. Broader signed overflow/aliasing/malformed pointers remain unsupported.', 'Clamp operates on a private12B local copy. Only words40/48 update; original4C/50/54 vector and other bytes remain unchanged. RawR0 is the state base address,not an asserted semantic return.', 'New context names fields28 and40 inside the same0x58-byte prefix while keeping frozen738 source/header unchanged. Separate zero-credit header compatibility experiments may inform an integrator migration; they are not dependencies/adopted matches here.', 'No source byte patch,assembly,host/device execution,application changes or public SDK adoption.'])
    write_json(ROOT/'evidence/matches/ov000-20261101-state742.json',report);print(dict(matchedBytes=200,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=0,wrongActualReturns=len(controls)),flush=True)
if __name__=='__main__':execute()
