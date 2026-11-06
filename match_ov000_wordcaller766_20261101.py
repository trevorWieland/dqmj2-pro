import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_wordcaller766_machine_20261101 as M
SOURCE=ROOT/'src/overlays/ov000_20261101_wordcaller766/source.c'
OLD=ROOT/'src/runtime/ov000-calls01/native_ov000_02204dec_01da6dc55929.c'
WORK=ROOT/'work/ol766-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,private=False):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('766 compilation failed',rows))
    row=rows[0];directory=WORK/name/'canonical-link';bindings=qualified_bindings(row)
    if private:
        try:proof=validate(row,bindings,directory)
        except ValueError as error:
            if not isinstance(error.args[0],dict):raise
            proof=error.args[0]
        relocated,body=link_private(row,bindings,directory,WORK/name/'private-link',M.PRIVATE)
        return dict(source=row,canonicalComparison=proof,privateLink=relocated),body
    proof=validate(row,bindings,directory)
    return dict(**row,realLink=proof),(directory/'caller.bin').read_bytes()

def compact(result):return{key:result[key]for key in['profile','coreRegistersAndCpsr','calls','actualNativeReturns','nonstackWrites','ownObserved']}

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('766 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov000-wordcaller766-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('766 pinned input differs',item['path']))
    if SOURCE.read_text()!=OLD.read_text().replace('extern void native_fn_0206e634();','extern u32 native_fn_0206e634(u32);'):raise ValueError('766 alternative changed more than the qualified setter declaration')
    selected=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions'];previous=[r for r in selected if r['processor']=='arm9'and not r.get('program')and r['module']=='ov000'and r['mode']=='arm'and r['address']==M.ENTRY]
    if len(previous)!=1 or previous[0]['bytes']!=292:raise ValueError('766 existing selected identity differs')
    original=M.inputs();packet,body=compile_unit(SOURCE,'positive');profiles=M.profiles();traces,cases=[],[];seen=set();dependencies,providers=0,0
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body if flag else None).run()for flag in[False,True]];nm,cm=M.model(native),M.model(candidate)
        for key in['before','after','coreRegistersAndCpsr','calls','actualNativeReturns','nonstackWrites']:
            if native[key]!=candidate[key]:raise ValueError(('766 full physical pair differs',key,profile['name']))
        if nm!=cm:raise ValueError('766 independent caller model differs')
        count=nm['nativeReturns']+cm['nativeReturns'];provided=nm['providedCalls']+cm['providedCalls'];dependencies+=count;providers+=provided;seen.update(native['ownObserved']);trace=dict(original=compact(native),candidate=compact(candidate),independentModel=nm,actuallyReturned=True,allCoreRegistersCpsrFullRamIncludingStackRawCallsAndOrderedWritesEqual=True);traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualNativeSetterReturns=count,providedCalls=provided,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+288,4)):raise ValueError('766 own code coverage differs')
    text=SOURCE.read_text();controls=[]
    for name,wrong_text in[('wrong-setter-constant',text.replace('native_fn_0206e634(2);','native_fn_0206e634(3);')),('wrong-initialized-byte',text.replace('u8 *, 6) = 1U;','u8 *, 6) = 2U;'))]:
        if wrong_text==text:raise ValueError('766 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-wordcaller766-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=wrong_text:raise ValueError('766 frozen wrong source differs')
        source.write_text(wrong_text);wrong,wrong_body=compile_unit(source,name,True);result=M.Machine(original,profiles[128],wrong_body,True).run()
        try:M.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('766 returning wrong source escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actualTopReturns=1,actuallyReturned=True,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov000-wordcaller766-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],matches=[packet],existingSelectedIdentity=previous[0],sourceAlternative=True,sourceCredit=0,newFunctionCredit=0,newInitializedSourceByteCredit=0,canonicalMatchedBytes=292,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeSetterReturns=dependencies,providedCalls=providers,allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackEqual=True,allRawCallsAndOrderedWritesEqual=True,ownCoverage=dict(codeBytes=288,literalBytes=4),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['Already selected292-byte function; only the0206E634 declaration changes to u32(u32). No source,function or initialized-byte credit and no preferences/old source edits.', 'Caller actually invokes0206E634 directly with constant2,not the0206E644 wrapper. Native setter writes byte021C4FC1 and retains rawR0=2. Wider setter/wrapper word-return contract is independently owned by save/core.', 'All256 unsigned caller byte7 values and all256 previous setter bytes are exercised on active path; gate byte6 classes0/1/128/255 cover first-time versus early-return behavior. State remains synthetic with no UI/resource/lifecycle meaning asserted.', 'Eight other explicit caller-prepared views are supplied zero-RAM boundaries with legal caller-saved register/flag clobbers. Their actual native semantics/formal types are not established here. No fake native provider returns are counted.', 'Raw caller result is the state address when initialized and unsigned nonzero gate byte otherwise; no semantic return meaning is inferred. Every positive pair compares full registers/CPSR/RAM including stack/raw calls/ordered writes.', 'Coordinated main setter/wrapper/caller adoption and module/ROM/regression acceptance are integrator-owned. No application changes or host/device/full-scene claim.'])
    write_json(ROOT/'evidence/matches/ov000-20261101-wordcaller766-zero-credit.json',report);print(dict(existingMatchedBytes=292,newCredit=0,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeSetterReturns=dependencies,providedCalls=providers,wrongActualReturns=len(controls)),flush=True)

if __name__=='__main__':execute()
