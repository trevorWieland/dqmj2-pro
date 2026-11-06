import gzip
import json
import re
import sys
import match_runtime as c
import unicorn
from project import ROOT,configuration,write_json,sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from save_link_snapshots import freeze_link
import ov001_float574_machine_20261101 as M
import ov001_float574_models_20261101 as P
SOURCE=ROOT/'src/overlays/ov001_20261101_float575/digits.c'
WORK=ROOT/'work/ol575-proof'
PINS=ROOT/'evidence/verification/ov001-float575-inputs-20261101.json'


def encoded(value):return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def compile_unit(source,name,exact):
    previous=c.symbol_address
    def resolver(symbol):
        if symbol=='_s32_div_f':return M.DIV
        if re.fullmatch(r'_(?:[us](?:32|64)|f|d)_\w+',symbol):raise RuntimeError('575 unqualified compiler intrinsic rejected: '+symbol)
        return previous(symbol)
    c.symbol_address=resolver;c.WORK=WORK/name/'compile'
    try:rows,unused=c.compare(source,'ov001','2','off',True)
    finally:c.symbol_address=previous
    if len(rows)!=1 or rows[0].get('compileFailed'):raise ValueError('575 compiler failed')
    row=rows[0];row['sourceDependencies']=[dict(path=source.with_name('context.h').relative_to(ROOT).as_posix(),sha256=sha256(source.with_name('context.h')))];directory=WORK/name/'link'
    try:proof=validate(row,qualified_bindings(row),directory)
    except ValueError as error:
        if exact or not isinstance(error.args[0],dict):raise
        proof=error.args[0]
    return row,proof,(directory/'caller.bin').read_bytes()


def execute():
    if sys.version_info[:3]!=(3,13,5)or unicorn.__version__!='2.1.4':raise ValueError('575 runtime differs')
    for row in json.loads(PINS.read_text())['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError(('575 pinned input differs',row['path']))
    snapshot=ROOT/'evidence/verification/accepted-cohort107-identities-v2-20261101.json';accepted=json.loads(snapshot.read_text())['functions']
    if any(r['processor']=='arm9'and not r.get('program')and r['module']=='ov001'and max(r['address'],M.ENTRY)<min(r['address']+r['bytes'],M.ENTRY+M.SIZE)for r in accepted):raise ValueError('575 accepted overlap')
    original=M.inputs();row,proof,body=compile_unit(SOURCE,'caller',True)
    if body!=original['overlay'][M.ENTRY-M.OVERLAY:M.ENTRY-M.OVERLAY+M.SIZE]:raise ValueError('575 genuine current bytes differ')
    row['genuineLinkComparison']=freeze_link(proof);row['exactBytes']=M.SIZE;profiles=P.profiles();traces=[];cases=[];controls=[];seen=set();watched=0;direct=0;provided=0;forwarded=0;intmin=0
    for p in profiles:
        n=M.Machine(original,p).run();nm=P.model(n);candidate=M.Machine(original,p,body).run();cm=P.model(candidate)
        if nm!=cm or n['allArmCoreRegistersAndCpsr']!=candidate['allArmCoreRegistersAndCpsr']or n['nativeReturns']!=candidate['nativeReturns']or n['callEvents']!=candidate['callEvents']or n['nonstackWrites']!=candidate['nonstackWrites']or n['after']!=candidate['after']:raise ValueError(('575 complete original/C execution differs',p['name']))
        seen.update(n['ownObserved']);count=len(n['nativeReturns'])*2;watched+=count;direct+=nm['directNativeReturns']*2;provided+=nm['providedCalls']*2;forwarded+=len(n['powerTargetWords'])*2;intmin+=int(nm['intMinLimitCase']);trace=dict(profile=p,model=nm,allArmCoreRegistersAndCpsr=n['allArmCoreRegistersAndCpsr'],returnedWords=n['returnedWords'],nativeReturns=n['nativeReturns'],callEvents=n['callEvents'],powerTargetWords=n['powerTargetWords'],nonstackWrites=n['nonstackWrites'],completeRamSha256=c.sha(n['after']),nativeInstructions=n['instructions'],candidateInstructions=candidate['instructions'],ownObserved=n['ownObserved']);traces.append(trace);cases.append(dict(profile=p['name'],actualTopReturns=2,actualWatchedNativeDependencyReturns=count,directCallerNativeReturnsSubset=nm['directNativeReturns']*2,providedCalls=nm['providedCalls']*2,traceSha256=c.sha(encoded(trace))))
    if seen!=set(range(M.ENTRY,M.ENTRY+232,4)):raise ValueError(('575 own code coverage differs',len(seen)*4))
    text=SOURCE.read_text();old='native_fn_020244c4((s32) var_r8)';unsigned='var_r6 = (s32) var_r6 / 10;';flag='M2C_FIELD(temp_r4, s32 *, 0x7C) | 2';wrong=[('zero-exponent',text.replace(old,'native_fn_020244c4(0)'),dict(limit=11,number=12345)),('unsigned-count',text.replace(unsigned,'var_r6 = var_r6 / 10;'),dict(limit=11,number=0xFFFFFFFF)),('clear-bit',text.replace(flag,'M2C_FIELD(temp_r4, s32 *, 0x7C) & ~2'),dict(limit=11,number=123))]
    for name,sourceText,p in wrong:
        if sourceText==text:raise ValueError('575 wrong-source recipe failed')
        directory=ROOT/'nonmatching/overlay-lane/20261101-ov001-float575-controls'/name;directory.mkdir(parents=True,exist_ok=True);source=directory/'source.c'
        if source.exists()and source.read_text()!=sourceText:raise ValueError('575 frozen wrong source differs')
        source.write_text(sourceText);source.with_name('context.h').write_bytes(SOURCE.with_name('context.h').read_bytes());wrongRow,wrongProof,wrongBody=compile_unit(source,'wrong-'+name,False);p['name']='wrong-'+name;r=M.Machine(original,p,wrongBody).run()
        try:P.model(r)
        except ValueError as error:failure=str(error)
        else:raise ValueError('575 wrong source escaped independent model')
        trace=dict(profile=p,actualReturned=True,returnedWords=r['returnedWords'],nativeReturns=r['nativeReturns'],callEvents=r['callEvents'],powerTargetWords=r['powerTargetWords'],nonstackWrites=r['nonstackWrites'],instructions=r['instructions'],failure=failure);controls.append(dict(name=name,actualReturned=True,source=wrongRow,genuineLinkComparison=wrongProof,traceSha256=c.sha(encoded(trace)),failure=failure,trace=trace))
    raw=encoded(dict(cases=traces,wrongSources=[r['trace']for r in controls]));artifact=ROOT/'evidence/generated/ov001-float575-native-traces-20261101.json.gz';artifact.write_bytes(gzip.compress(raw,mtime=0))
    for item in controls:del item['trace']
    row['oracle']=dict(cases=len(profiles),actualTopReturns=len(profiles)*2,actualNativeDependencyReturns=watched,directCallerNativeReturnsSubset=direct,nestedWatchedNativeReturns=watched-direct,providedCalls=provided,actualPowerTargetForwardings=forwarded,intMinLimitPairs=intmin,allInputPairsUseDefinedLimitWrap=True,fullRamCoreRegistersCpsrAndOrderedWritesEqual=True,observedOwnInstructionBytes=232,referencedLiteralBytes=8,unclassifiedBytes=0,casesEvidence=cases,counting='Watched native entries244C4/2298C/24394/26144 only; direct-caller and nested watched returns are subsets of total. Underlying212F8 tail forwarding is not a second return. Other internal math returns are not counted.')
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],module='ov001',moduleInputSha256=original['module']['sha256'],emulationModel='UC_CPU_ARM_946',matches=[row],nativeSymbols={r['symbol']:r['target']for r in row['relocations']},nativeSymbolEntries=qualified_bindings(row),negativeEvidence=controls,literalEvidence=[dict(address=hex(M.ENTRY+232),value='0x66666667',derivation='Compiler strength reduction of ordinary signed division by10'),dict(address=hex(M.ENTRY+236),value='0x40240000',derivation='High word of binary64 constant10.0; low word generated as0')],nativeMathContract=dict(path='evidence/abi/main-float-word-contracts-20261101.json',sha256=sha256(ROOT/'evidence/abi/main-float-word-contracts-20261101.json')),generatedTrace=dict(path=artifact.relative_to(ROOT).as_posix(),sha256=sha256(artifact),uncompressedSha256=c.sha(raw),uncompressedBytes=len(raw)),wholeModuleLinked=False,sourceReconstructionComplete=False,limitations=['Synthetic object/target flags and two provided zero-RAM-effect UI services; no ordinary widget or scene reachability claim.','Actual original conversion/power/division code executes only within frozen finite native math paths plus canonical signed-divide range.','Finite native word contracts do not establish original public C typedefs or general math-library semantics.','Only the240-byte caller is reconstructed; all native dependency code and tail forwarding add zero source credit.','Provided getter/setter calls are reported separately, poison caller-saved registers and condition flags, and are never counted as actual native returns.','Raw output selectors and target+0x7C bit1 effects have no inferred application or gameplay meaning.']);write_json(ROOT/'evidence/matches/ov001-20261101-float575.json',report);print(dict(matchedBytes=240,functions=1,pairs=len(profiles),topReturns=len(profiles)*2,watchedNativeReturns=watched,directNativeSubset=direct,nestedWatched=watched-direct,providedCalls=provided,powerForwardings=forwarded,intMinLimitPairs=intmin,wrongActualReturns=len(controls)),flush=True)


if __name__=='__main__':execute()
