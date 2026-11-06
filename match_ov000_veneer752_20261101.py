import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_veneer752_machine_20261101 as M
SOURCE=ROOT/'src/overlays/ov000_20261101_veneer752/source.c'
WORK=ROOT/'work/ol752-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,private=False):
    c.WORK=WORK/name/'compile'
    rows,unused=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('752 compilation failed',rows))
    row=rows[0]
    row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))]
    directory=WORK/name/'canonical-link';bindings=qualified_bindings(row)
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
    return{key:result[key]for key in['profile','coreRegistersAndCpsr','nativeCalls','watchedNativeReturns','nonstackWrites','veneerObserved','targetObserved','nativeObserved']}

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('752 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov000-veneer752-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('752 pinned input differs',item['path']))
    selected=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    previous=[row for row in selected if row['processor']=='arm9'and not row.get('program')and row['module']=='ov000'and row['address']==M.ENTRY and row['mode']=='arm']
    if len(previous)!=1 or previous[0]['bytes']!=12:raise ValueError('752 requires existing selected12-byte entry')
    original=M.B.inputs();packet,body=compile_unit(SOURCE,'positive')
    if len(body)!=12:raise ValueError('752 matched veneer size differs')
    profiles=M.profiles();traces,cases=[],[];seen,target=set(),set();dependencies=0;state_signatures={}
    lo,hi=M.B.STACK-256-M.BASE,M.B.STACK+32-M.BASE
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body if flag else None).run()for flag in[False,True]]
        nm,cm=M.P.model(native),M.P.model(candidate)
        for key in['before','after','coreRegistersAndCpsr','nativeCalls','watchedNativeReturns','nonstackWrites']:
            if native[key]!=candidate[key]:raise ValueError(('752 complete physical comparison differs',key,profile['name']))
        if nm!=cm:raise ValueError('752 independent model differs')
        signature=[native['coreRegistersAndCpsr'][0],c.sha(native['after'][:lo]+native['after'][hi:])]
        prior=state_signatures.setdefault(profile['seed'],signature)
        if prior!=signature:raise ValueError('752 return/nonstack effects depend on poisoned entry words')
        seen.update(native['veneerObserved']);target.update(native['targetObserved'])
        count=len(native['watchedNativeReturns'])+len(candidate['watchedNativeReturns']);dependencies+=count
        trace=dict(native=compact(native),candidate=compact(candidate),independentModel=nm,actuallyReturned=True,allCoreRegistersAndCpsrAndFullRamEqual=True,nonstackPoisonSignature=signature)
        traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualWatchedNativeDependencyReturns=count,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+8,4))or target!=set(range(M.B.ENTRY,M.B.ENTRY+72,4)):raise ValueError('752 native veneer/target code coverage differs')
    text=SOURCE.read_text();controls=[]
    variants=[('wrong-return-add-one',text.replace('return native_fn_ov000_022198ec();','return native_fn_ov000_022198ec()+1U;'),next(p for p in profiles if p['resourceWord']==127)),('wrong-skip-target',text.replace('return native_fn_ov000_022198ec();','return 0;'),next(p for p in profiles if p['resourceWord']==0 and p['pointer']!=0 and p['flag']==128 and p['word']==0))]
    for name,wrong_text,profile in variants:
        if wrong_text==text:raise ValueError('752 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-veneer752-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=wrong_text:raise ValueError('752 frozen wrong source differs')
        source.write_text(wrong_text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes())
        wrong,wrong_body=compile_unit(source,name,True);result=M.Machine(original,profile,wrong_body,True).run()
        try:M.P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('752 returning wrong control escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace))
        controls.append(dict(name=name,**wrong,actualTopReturns=1,actuallyReturned=True,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov000-veneer752-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=[packet],existingSelectedIdentity=previous[0],sourceAlternative=True,canonicalMatchedBytes=12,newFunctionCredit=0,newInitializedSourceByteCredit=0,sourceCredit=0,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=0,requiredIncomingArgumentWords=0,rawU32ReturnFacadePreserved=True,allCoreRegistersAndCpsrAndFullRamIncludingStackEqual=True,allRawCallsAndOrderedWritesEqual=True,poisonMetamorphicStates=len(state_signatures),poisonRotationsPerState=4,rawReturnAndNonstackEffectsIndependentOfPoison=True,ownCoverage=dict(codeBytes=8,literalBytes=4),nativeTargetCoverage=dict(address=hex(M.B.ENTRY),codeBytes=72,literalBytes=8,additionalTerminalReturnCredit=0),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['Existing12-byte veneer source alternative only; zero new function or source-byte credit. Old accepted four-word source and frozen750 files remain unchanged. Integrator owns preference/interface compatibility and module/ROM acceptance.', '160 explicit global/object states times4 rotations of R0-R3 over0,1,0x80000000,0xFFFFFFFF. Each pair compares complete registers/CPSR/RAM including stack and ordered raw calls/writes. Across rotations only R0 and nonstack effects are asserted input-independent; unused caller-saved registers and stack saves may carry poison.', 'Original80-byte022198EC and main0205F98C execute without providers. The veneer tail return is one top return; the target terminal return is not counted again. Main leaf returns are counted separately.', 'This qualifies zero required physical input words,not the original number of unused source formals. The explicit u32(void) C facade retains the old raw-word return representation and names no semantic meaning.', 'Malformed pointers,aliasing,current scene,resource allocation/lifecycle,host/device behavior and unseen callers remain unsupported. No application or shared registry changes.'])
    write_json(ROOT/'evidence/matches/ov000-20261101-veneer752.json',report)
    print(dict(existingMatchedBytes=12,newCredit=0,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=dependencies,providedCalls=0,wrongActualReturns=len(controls)),flush=True)

if __name__=='__main__':execute()
