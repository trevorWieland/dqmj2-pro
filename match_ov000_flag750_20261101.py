import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_flag750_machine_20261101 as M
import ov000_flag750_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov000_20261101_flag750/source.c'
WORK=ROOT/'work/ol750-proof'
def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def compile_unit(source,name,private=False):
    c.WORK=WORK/name/'compile';rows,u=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('750 compilation failed',rows))
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
def compact(result):return{key:result[key]for key in['profile','coreRegistersAndCpsr','nativeCalls','watchedNativeReturns','nonstackWrites','ownObserved','nativeObserved']}
def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('750 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov000-flag750-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('750 pinned input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(r['processor']=='arm9'and r['module']=='ov000'and not r.get('program')and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in accepted):raise ValueError('750 selected overlap')
    original=M.inputs();packet,body=compile_unit(SOURCE,'positive')
    if len(body)!=80:raise ValueError('750 matched size changed')
    profiles=P.profiles();traces,cases=[],[];seen=set();dependencies=0
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body if flag else None).run()for flag in[False,True]];nm,cm=P.model(native),P.model(candidate)
        if nm!=cm or native['before']!=candidate['before']or native['after']!=candidate['after']or native['coreRegistersAndCpsr']!=candidate['coreRegistersAndCpsr']or native['nativeCalls']!=candidate['nativeCalls']or native['watchedNativeReturns']!=candidate['watchedNativeReturns']or native['nonstackWrites']!=candidate['nonstackWrites']:raise ValueError('750 complete physical comparison differs')
        count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns']);dependencies+=count;seen.update(native['ownObserved']);trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,fullRegistersCpsrAndRamIncludingStackEqual=True,allCallsAndOrderedWritesEqual=True);traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualWatchedNativeDependencyReturns=count,providedCalls=0,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+72,4)):raise ValueError('750 own code coverage differs')
    template=SOURCE.read_text();variants=[('wrong-sentinel',template.replace('value!=127','value!=126'),next(p for p in profiles if p['resourceWord']==127 and p['pointer']!=0 and p['flag']==1 and p['word']==0)),('wrong-flag-one',template.replace('opaque00[1]!=0','opaque00[1]==1'),next(p for p in profiles if p['resourceWord']==0 and p['pointer']!=0 and p['flag']==128 and p['word']==0)),('wrong-bit',template.replace('field7c|=2','field7c|=1').replace('field7c&=~2U','field7c&=~1U'),next(p for p in profiles if p['resourceWord']==0 and p['pointer']!=0 and p['flag']==1 and p['word']==0))];controls=[]
    for name,text,profile in variants:
        if text==template:raise ValueError('750 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-flag750-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('750 frozen wrong source differs')
        source.write_text(text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wrong,wrong_body=compile_unit(source,name,True);result=M.Machine(original,profile,wrong_body,True).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('750 returning wrong control escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actualTopReturns=1,actuallyReturned=True,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov000-flag750-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=[packet],canonicalMatchedFunctions=1,canonicalMatchedBytes=80,sourceCreditPendingIntegrator=80,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=0,requiredIncomingArgumentWords=0,allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allRawCallsAndOrderedWritesEqual=True,ownCoverage=dict(codeBytes=72,literalBytes=8,unclassifiedBytes=0),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['One genuine80B ordinary C unit; parent module/ROM/regression acceptance remains required.', 'Original main0205F98C/12 executes with exactly the existing u32(s32,s32) facade and index0. No provider or extra helper source credit.', 'Globals and synthetic nonnull128B object/word7C are explicit inputs. Sentinel127 and null paths are measured,without asserting resource meaning,current scene or allocation lifecycle.', 'IncomingR0/R1 are overwritten before use; R2 is never consumed and is overwritten inside the only leaf call; R3 is only saved/restored. Poisoned raw words are recorded. This establishes zero required physical input words,not the original unused formal parameter count.', 'u32 raw return facade is retained from the old12B veneer. Measured word is127 on the sentinel path,0 on null path or the object address on active path; no semantic return meaning.', 'The old accepted12B four-word veneer/source is unchanged. Its optional zero-input source alternative is separate zero-credit research,not a positive dependency or adopted preference here.', 'Malformed/nonaligned/aliased pointers and other object extents remain unsupported. No application,Windows/Android,device or external SDK adoption claim.'])
    write_json(ROOT/'evidence/matches/ov000-20261101-flag750.json',report);print(dict(matchedBytes=80,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=0,wrongActualReturns=len(controls)),flush=True)
if __name__=='__main__':execute()
