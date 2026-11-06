import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from link_private_overlay_hypothesis_20261101 import link_private
import ov000_controller764_machine_20261101 as M
import ov000_controller764_models_20261101 as P
SOURCE=ROOT/'nonmatching/overlay-lane/20261101-controller764/near/source.c'
WORK=ROOT/'work/ol764-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name):
    c.WORK=WORK/name/'compile';rows,unused=c.compare(source,'ov000','2','off',True)
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('764 compilation failed',rows))
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'canonical-link';bindings=qualified_bindings(row)
    try:proof=validate(row,bindings,directory)
    except ValueError as error:
        if not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    relocated,body=link_private(row,bindings,directory,WORK/name/'private-link',M.PRIVATE)
    return dict(source=row,canonicalComparison=proof,privateLink=relocated),body,(directory/'caller.bin').read_bytes()

def compact(result):return{key:result[key]for key in['profile','coreRegistersAndCpsr','calls','actualNativeReturnEvents','nonstackWrites','ownObserved','nativeObserved','ownInvocations']}

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('764 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/ov000-controller764-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('764 pinned input differs',item['path']))
    original=M.inputs();packet,body,canonical=compile_unit(SOURCE,'positive');native=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]
    matching=sum(a==b for a,b in zip(native,canonical))
    if len(canonical)!=1500 or matching!=1494:raise ValueError(('764 frozen near frontier differs',len(canonical),matching))
    profiles=P.profiles();traces,cases=[],[];nativeReturns,providers,writeOrderFailures=0,0,0
    lo,hi=M.STACK-65536-M.BASE,M.STACK+256-M.BASE
    for profile in profiles:
        originalRun,candidate=[M.Machine(original,profile,body,flag).run()for flag in[False,True]];nm,cm=P.model(originalRun),P.model(candidate,False)
        if originalRun['before']!=candidate['before']or originalRun['after'][:lo]!=candidate['after'][:lo]or originalRun['after'][hi:]!=candidate['after'][hi:]:raise ValueError('764 complete nonstack native/C comparison differs')
        if nm['rawR0']!=cm['rawR0']or nm['ownInvocations']!=cm['ownInvocations']:raise ValueError('764 semantic return/recursion differs')
        ordered=cm['orderedWritesEqual'];writeOrderFailures+=not ordered
        if not ordered:
            nw=[r[1:]for r in originalRun['nonstackWrites']];cw=[r[1:]for r in candidate['nonstackWrites']];diff=[i for i,(a,b)in enumerate(zip(nw,cw))if a!=b]
            if len(diff)!=2 or diff[1]!=diff[0]+1 or nw[diff[0]]!=cw[diff[1]]or nw[diff[1]]!=cw[diff[0]]or{nw[diff[0]][0],nw[diff[1]][0]}!={M.SLOTS+1,M.STATE+3}:raise ValueError('764 unexpected ordered-write residual')
        count=len(originalRun['actualNativeReturnEvents'])+len(candidate['actualNativeReturnEvents']);nativeReturns+=count;providers+=nm['providedCalls']+cm['providedCalls']
        trace=dict(original=compact(originalRun),candidate=compact(candidate),independentOriginalModel=nm,independentCandidateModel=cm,bothActuallyReturned=True,completeNonstackMemoryEqual=True,privateCodeMappedIdenticallyInBoth=True,orderedWritesExact=ordered);traces.append(trace);cases.append(dict(profile=profile['name'],actualTopReturns=2,actualNativeReturnInstructions=count,providedCalls=nm['providedCalls']+cm['providedCalls'],orderedWritesEqual=ordered,traceSha256=c.sha(encoded(trace))))
    text=SOURCE.read_text();variants=[('wrong-seven-word-constructor',text.replace('(u32)native_fn_ov000_0221938c, 0, 0x12','(u32)native_fn_ov000_0221938c, 0x12'),next(p for p in profiles if p['state']==0 and p['constructorGate']==1)),('wrong-byte-sentinel-255',text.replace('temp_r0_4 != -1U','temp_r0_4 != 255U'),next(p for p in profiles if p['state']==2 and p['exitGate']==0 and p['cleanup14']and p['spriteCount']==1 and p['spriteIds'][0]==255))];controls=[]
    for name,wrong_text,profile in variants:
        if wrong_text==text:raise ValueError('764 wrong source unchanged')
        directory=ROOT/'nonmatching/overlay-lane/20261101-controller764-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=wrong_text:raise ValueError('764 frozen wrong source differs')
        source.write_text(wrong_text);header=SOURCE.with_name('context.h').read_text()
        if name=='wrong-seven-word-constructor':header=header.replace('native_fn_0205fc10(u32,u32,u32,u32,u32,u32,s32,u32)','native_fn_0205fc10(u32,u32,u32,u32,u32,s32,u32)')
        source.with_name('context.h').write_text(header);wrong,wrong_body,unused=compile_unit(source,name);result=M.Machine(original,profile,wrong_body,True).run()
        try:P.model(result,False)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('764 returning wrong source escaped model',name))
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actualTopReturns=1,actuallyReturned=True,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/ov000-controller764-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='ov000',moduleSha256=original['module']['sha256'],sourceCredit=0,functionCredit=0,byteCredit=0,canonicalNativeBytes=1500,canonicalLinkedBytes=len(canonical),canonicalMatchingBytes=matching,exact=False,nearCandidate=packet,callerPairs=len(profiles),actualTopReturns=2*len(profiles),actualNativeReturnInstructions=nativeReturns,providedCalls=providers,completeNonstackMemoryEqual=True,codeStorageMappedIdenticallyInBoth=True,writeOrderFailurePairs=writeOrderFailures,cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['Zero exact/source/function/byte credit. Canonical1500-byte C differs by six bytes: only the two adjacent byte stores at02218FB4/02218FB8 are reversed.','Private execution uses a genuine origin-only MWLD relink of the unchanged split object/relocations/bindings. Identical private code is mapped in both machines; original canonical executable and neighboring callbacks are unchanged.','Complete nonstack RAM,independent final-state/raw-R0/recursive-control model and explicit meaningful call words agree. Stack/full caller-saved register/CPSR/PC/LR equivalence is not asserted; raw physical observations remain in traces.','The two reversed stores target distinct measured bytes0222FA09 and02245E57. No provider executes between them. Native ordered writes are independently checked; candidate order failures stay explicit,not normalized into an exact claim. Interrupt/concurrent observers are not modeled.','Most UI/resource/scheduler/render/motion calls are supplied zero-RAM boundaries with caller-saved register/flag clobbers. Their native semantics,scene entry,graphics/audio/resource lifetime and downstream callbacks are not claimed. Actual native getters,clear,clamp,flag veneer/target execute and receive no duplicate credit.','Constructor0205FC10 prepares8 words includingR3=0 and4 stack words. Its original native prologue consumesR3 and all4 stack slots. This is a caller-specific word contract,not a historical source prototype/type claim.','Native unsigned-byte compare toFFFFFFFF is preserved; it does not skip byte255. Wrong255-sentinel source is a returning rejection.','Profiles bound sprite count at8 and recursive dispatch at16; negative counts skip the loop. Unknown states follow default behavior. Invalid pointers/aliases,larger or wrapping sprite loops,unprovided effects and full game/host/device execution are unsupported.'])
    write_json(ROOT/'evidence/matches/ov000-20261101-controller764-functional-near.json',report);print(dict(sourceCredit=0,canonicalMatchingBytes=matching,canonicalBytes=1500,pairs=len(profiles),actualTopReturns=2*len(profiles),nativeReturnInstructions=nativeReturns,providedCalls=providers,writeOrderFailurePairs=writeOrderFailures,wrongActualReturns=len(controls)),flush=True)

if __name__=='__main__':execute()
