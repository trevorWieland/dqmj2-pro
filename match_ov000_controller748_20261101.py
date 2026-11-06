import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_controller748_machine_20261101 as M
import ov000_controller748_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov000_20261101_controller748/source.c'
WORK=ROOT/'work/ol748-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()
def compile_unit(source,name,private=False):
    c.WORK=WORK/name/'compile';rows,u=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('748 compilation failed',rows))
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
def compact(result):return{key:result[key]for key in['profile','coreRegistersAndCpsr','calls','watchedNativeReturns','nonstackWrites','ownObserved','nativeObserved']}

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('748 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov000-controller748-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('748 pinned input differs',item['path']))
    accepted=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov000'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in accepted):raise ValueError('748 accepted overlap')
    original=M.inputs()
    if original['module']['sha256']!=pins['ov000Sha256']:raise ValueError('748 module image differs')
    packet,body=compile_unit(SOURCE,'positive')
    if len(body)!=M.SIZE:raise ValueError('748 matched body has wrong size')
    profiles=P.profiles();traces,cases=[],[];seen=set();dependencies=0;provided=0;branches={}
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body if candidate else None).run()for candidate in[False,True]];nm,cm=P.model(native),P.model(candidate)
        if nm!=cm or native['before']!=candidate['before']or native['after']!=candidate['after']or native['coreRegistersAndCpsr']!=candidate['coreRegistersAndCpsr']or native['calls']!=candidate['calls']or native['watchedNativeReturns']!=candidate['watchedNativeReturns']or native['nonstackWrites']!=candidate['nonstackWrites']:raise ValueError('748 complete physical comparison differs')
        count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns']);dependencies+=count;provided+=nm['providedCalls']+cm['providedCalls'];branches[nm['branch']]=branches.get(nm['branch'],0)+1;seen.update(native['ownObserved']);trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,bothActuallyReturned=True,fullRamIncludingStackAndAllRegistersEqual=True,allRawCallsAndOrderedWritesEqual=True);traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualWatchedNativeDependencyReturns=count,providedCalls=nm['providedCalls']+cm['providedCalls'],traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+652,4)):raise ValueError('748 own code coverage differs')
    template=SOURCE.read_text();controls=[]
    variants=[('wrong-minimum-width',template.replace('<= 0x20U','< 0x20U'),next(p for p in profiles if p['recordFlag']==0 and p['width']==32 and p['height']==24)),('wrong-signed-coordinate',template.replace('M2C_FIELD(temp_r4, u8 *, 1)','M2C_FIELD(temp_r4, s8 *, 1)'),next(p for p in profiles if p['touch'][0]==1 and p['mode']==5 and p['touch'][1]>=128)),('wrong-secondary-one',template.replace('field28 == 0','field28 != 1'),next(p for p in profiles if p['secondary']==0x80000000 and p['touch'][0]==0 and p['buttons']==0))]
    for name,text,profile in variants:
        if text==template:raise ValueError('748 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-controller748-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=text:raise ValueError('748 frozen wrong control differs')
        source.write_text(text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wrong,wrong_body=compile_unit(source,name,True);result=M.Machine(original,profile,wrong_body,True).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('748 returning wrong control escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actuallyReturned=True,actualTopReturns=1,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov000-controller748-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=[packet],canonicalMatchedFunctions=1,canonicalMatchedBytes=660,sourceCreditPendingIntegrator=660,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=provided,branchPairCounts=branches,allOwnCodeObserved=dict(codeBytes=652,literalBytes=8,unclassifiedBytes=0),allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allRawCallsAndOrderedWritesEqual=True,cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['One genuine660-byte ordinary C controller. Parent module/ROM/regression acceptance remains required.', 'Original native constant getters02066C3C/0202A634,index/row021DF1F0/021DF3BC,signed mode getter020404E0,byte setters020404F0/0221993C and140-byte02219CE4 clamp execute. Dependency return totals exclude all explicitly supplied service boundaries.', 'Supplied02218800 query,02041510/02041560,021E7B9C notification and020418E8 boundaries preserve callee-saved registers,clobber caller-saved registers/flags and perform zero RAM writes. No actual UI,audio,query reachability or full-scene behavior claim.', 'Synthetic row/status/mode/buttons/current vector/reference vector,gates20/28,signed16 offsets/cache and service returns are explicit input state. Field names remain raw; scene initialization/lifecycle/semantic meanings remain unresolved.', 'Native clamp receives a private12-byte aggregate copy; whole-vector C assignment and two native-SP0-qualified first-component expressions repair the raw frontend. No generic unsupported-expression coercion or assembly.', 'Supported sums fit signed32; signed16 conversion follows the pinned compiler low16 representation. Clamp dimensions and bounded reference comparisons avoid signed32 overflow. Other arithmetic overflow,aliasing/malformed pointers and unseen service side effects are unsupported.', 'Void source preserves measured physical R0 for every branch without asserting a semantic public return. Full registers/CPSR/RAM including stack,ordered writes and raw call words agree in each native/C pair.', 'No accepted source edits,application changes,host/device execution or public SDK adoption.'])
    write_json(ROOT/'evidence/matches/ov000-20261101-controller748.json',report);print(dict(matchedBytes=660,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=provided,wrongActualReturns=len(controls)),flush=True)
if __name__=='__main__':execute()
