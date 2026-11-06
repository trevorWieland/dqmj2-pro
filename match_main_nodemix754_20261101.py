import gzip
import json
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,sha256,write_json
from link_runtime_unit import validate
from link_private_overlay_hypothesis_20261101 import link_private
import main_nodemix754_machine_20261101 as M
import main_nodemix754_models_20261101 as P
SOURCE=ROOT/'src/overlays/main_20261101_nodemix754/source.c'
WORK=ROOT/'work/ol754-proof'

def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()

def compile_unit(source,name,private=False):
    settings=json.loads((ROOT/'evidence/verification/main-nodemix754-bindings-20261101.json').read_text());flags=c.FLAGS[:];c.FLAGS+=settings['compilerExtraFlags'];c.WORK=WORK/name/'compile'
    try:rows,unused=c.compare(source,'main','2','off',False)
    finally:c.FLAGS=flags
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError(('754 compilation failed',rows))
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'canonical-link';bindings=settings['bindings']
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
    return{key:result[key]for key in['coreRegistersAndCpsr','nativeCalls','actualNativeReturnEvents','nonstackWrites','ownObserved','nativeObserved']}

def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('754 runtime differs')
    pins=json.loads((ROOT/'evidence/verification/main-nodemix754-inputs-20261101.json').read_text())
    for item in pins['files']:
        if sha256(ROOT/item['path'])!=item['sha256']:raise ValueError(('754 pinned input differs',item['path']))
    selected=json.loads((ROOT/pins['acceptedSnapshot']).read_text())['functions']
    if any(row['processor']=='arm9'and not row.get('program')and row['module']=='main'and max(row['address'],M.ENTRY)<min(row['address']+row['bytes'],M.ENTRY+M.SIZE)for row in selected):raise ValueError('754 accepted overlap')
    original=M.inputs();packet,body=compile_unit(SOURCE,'positive')
    if len(body)!=M.SIZE:raise ValueError('754 canonical size differs')
    profiles=P.profiles();traces,cases=[],[];seen=set();returns,entries=0,0;oracles={}
    for profile in profiles:
        native,candidate=[M.Machine(original,profile,body if flag else None).run()for flag in[False,True]];nm,cm=P.model(native),P.model(candidate)
        for key in['before','after','ioBefore','ioAfter','coreRegistersAndCpsr','nativeCalls','actualNativeReturnEvents','nonstackWrites']:
            if native[key]!=candidate[key]:raise ValueError(('754 complete physical comparison differs',key,profile['name']))
        if nm!=cm:raise ValueError('754 independent matrix model differs')
        oracles[profile['name']]=nm
        count=nm['actualNativeReturnInstructions']+cm['actualNativeReturnInstructions'];completed=nm['completedNativeEntries']+cm['completedNativeEntries'];returns+=count;entries+=completed;seen.update(native['ownObserved'])
        trace=dict(profile=profile,native=compact(native),candidate=compact(candidate),independentModel=nm,actuallyReturned=True,allCoreRegistersCpsrFullRamAndIoShadowEqual=True)
        traces.append(trace);cases.append(dict(profile=profile['name'],matrices=len(profile['entries']),actualTopReturns=2,actualNativeReturnInstructions=count,completedNativeEntries=completed,providedCalls=0,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+1868,4)):raise ValueError(('754 code coverage differs',len(seen)))
    text=SOURCE.read_text();controls=[]
    variants=[('wrong-weight-scale',text.replace('w = *(p + 2) << 4;','w = *(p + 2) << 3;'),next(p for p in profiles if p['entries'][0][2]==255 and p['cachedWords'][0]!=0)),('wrong-final-command-stride',text.replace('3 + *(rs->c + 2) * 3','3 + *(rs->c + 2) * 2'),profiles[1]),('wrong-ignore-cache',text.replace('BOOL evpCached = NNSi_G3dBitVecCheck(&rs->isEvpCached[0], idxJnt);','BOOL evpCached = 0;'),profiles[3])]
    for name,wrong_text,profile in variants:
        if wrong_text==text:raise ValueError(('754 wrong source unchanged',name))
        directory=ROOT/'nonmatching/overlay-lane/20261101-nodemix754-word-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=wrong_text:raise ValueError('754 frozen wrong source differs')
        source.write_text(wrong_text);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wrong,wrong_body=compile_unit(source,name,True);result=M.Machine(original,profile,wrong_body,True).run()
        try:P.model(result)
        except ValueError as error:failure=str(error)
        else:raise ValueError(('754 returning wrong source escaped model',name))
        reference=oracles[profile['name']];matrices=[row['matrixWordsAtEntry']for row in result['nativeCalls']if row['entry']==0x0200434C]
        meaningful=matrices[0][:9]!=reference['sumN']or matrices[1]!=reference['sumM']
        stride=int.from_bytes(result['after'][M.RS-M.BASE:M.RS-M.BASE+4],'little')!=M.COMMAND+3+len(profile['entries'])*3
        if not(stride if name=='wrong-final-command-stride'else meaningful):raise ValueError('754 wrong control lacked an independently meaningful difference')
        trace=dict(result=compact(result),actuallyReturned=True,failure=failure,meaningfulMatrixDifference=meaningful,commandPointerDifference=stride);traces.append(dict(negativeEvidence=name,**trace));controls.append(dict(name=name,**wrong,actualTopReturns=1,actuallyReturned=True,failure=failure,traceSha256=c.sha(encoded(trace))))
    raw=encoded(dict(cases=traces));artifact=ROOT/'evidence/generated/main-nodemix754-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',program='',module='main',moduleSha256=original['main']['sha256'],matches=[packet],canonicalMatchedFunctions=1,canonicalMatchedBytes=1884,sourceCreditPendingIntegrator=1884,callerPairs=len(profiles),actualTopReturns=len(profiles)*2,actualWatchedNativeDependencyReturns=returns,actualNativeReturnInstructions=returns,completedNativeEntryInvocations=entries,providedCalls=0,allCoreRegistersAndCpsrEqual=True,completeRamIncludingStackAndIoShadowEqual=True,allRawCallsAndOrderedWritesEqual=True,ownCoverage=dict(codeBytes=1868,literalBytes=16,unclassifiedBytes=0),cases=cases,negativeEvidence=controls,generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw)),limits=['One genuine1884-byte ordinary C SDK-derived NODEMIX unit; integrator module/ROM/regression gates remain required. Other routines/global BSS receive zero source credit.', 'All clear/flush/matrix-transfer/clip/vector helpers execute original native code with no providers. Return counts count actual native return instructions once,even when one tail return completes two watched entry frames. Entry-completion count is separate.', 'numMtx is1..64,joint indices0..63,source/destination matrix slots0..31,weights unsigned bytes and every weighted signed32 sum stays in range. Zero count,overflow,malformed pointers and invalid indices are unsupported.', 'Clip/vector registers are explicit static read shadows with busy bit clear; MMIO writes are recorded bus transactions. No GPU emulation,hardware coherence,real matrix-state/readback or device claim. Flush dirty word is0; explicit queue may be null,empty or bounded nonempty.', 'The first final load sends nine meaningful N words plus three adjacent canonical saved-register stack words. Full physical state/bus writes compare exactly; those three incidental words are not invented matrix fields,semantic inputs or portable C values. External original hardware transfer boundaries retain their measured storage footprint.', 'Selected0200434C/02004368/02004384 retain their existing u32(u32) raw-word facades with local pointer-to-word casts; no aggregate extent is asserted by those declarations.', 'Second u32 source formal is kept for the SDK command callback-table signature although this body overwrites incoming R1 before use. Body has no indirect callback invocation. Full reference structures remain hypotheses outside the measured accessed fields.', 'Reference unsigned bit-vector masks use1U to keep bit31 defined; local renaming,header split and removal of the trailing uncredited BSS definition preserve genuine bytes. No assembly/opcode patch/application edits or host execution claim.'])
    write_json(ROOT/'evidence/matches/main-20261101-nodemix754.json',report)
    print(dict(matchedBytes=1884,pairs=len(profiles),actualTopReturns=len(profiles)*2,actualNativeReturnInstructions=returns,completedNativeEntries=entries,providedCalls=0,wrongActualReturns=len(controls)),flush=True)

if __name__=='__main__':execute()
