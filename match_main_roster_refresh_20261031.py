import gzip
import hashlib
import json
import re
from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_roster_refresh_native_20261031 import execute,cases,ENTRY,NATIVE,PROVIDERS
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_roster_refresh/native_main_020d1154.c'
BINDINGS={f'native_fn_{address:08x}':dict(module='main',processor='arm9',kind='function',mode='arm',address=hex(address)) for address in NATIVE+PROVIDERS if address not in [0x02049AD0,0x020875B4,0x02087E44]}
BINDINGS.update({f'native_data_{address:08x}':dict(module='main',processor='arm9',kind='data',mode='data',address=hex(address)) for address in [0x021D6BB4,0x021D6BC0]})


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main')
    sizes={int(address,0):int(size,0) for size,address in re.findall(r'^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$',config,re.M) if int(address,0) in NATIVE}
    assert len(sizes)==7
    compiler.WORK=ROOT/'work/main-roster-refresh-source-20261031/compile';rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',True)
    assert len(rows)==1 and rows[0]['exactAfterDeclaredRelocation'];row=rows[0]
    directory=compiler.WORK.parent/'linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes']
    rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+380]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=372,literalPoolBytes=8,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();maximum=0;returns=0;providers=0;native_returns={};tails={}
    for tag,case in enumerate(cases()):
        a=execute(original,sizes,case,tag);b=execute(bytes(rebuilt),sizes,case,tag);assert a==b
        results.append(dict(case=case,result=a));observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions']);returns+=2;providers+=2*a['state']['providedCompletions']
        for key,value in a['nativeActualReturns'].items():native_returns[hex(key)]=native_returns.get(hex(key),0)+2*value
        for key,value in a['tailTransfers'].items():tails[key]=tails.get(key,0)+2*value
    text=(ROOT/SOURCE).read_text(encoding='utf-8-sig');wrong=text.replace('native_fn_02062a10(native_data_021d6bc0[var_r10])','native_fn_02062a10((u8)native_data_021d6bc0[var_r10])');assert wrong!=text
    path=ROOT/'nonmatching/main-runtime/20261031/roster-refresh/wrong-byte-ids.c';path.write_text(wrong,encoding='utf-8')
    compiler.WORK=ROOT/'work/main-roster-refresh-control-20261031/compile';bad,_=compiler.compare(path,'main',2,'off',True);directory=compiler.WORK.parent/'linked'
    try:validate(bad[0],BINDINGS,directory=directory)
    except ValueError as error:refusal=str(error)
    else:raise AssertionError('Wrong whole C matched')
    payload=(directory/'caller.bin').read_bytes();mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+len(payload)]=payload
    controls=[]
    for tag,ids in enumerate([[0,0,0],[1,1,1],[257,65537,256],[0x80000101,0xFFFFFFFF,257]]):
        case=dict(selected=tag,first=ids,second=[1,257,65537],nibble=tag*3)
        a=execute(original,sizes,case,tag);b=execute(bytes(mutant),sizes,case,tag,check=False,parent_code_bytes=len(payload)-8)
        controls.append(dict(case=case,actualReturns=2,rejected=not b['modelPassed'],positiveControl=b['modelPassed']))
    assert sum(item['rejected'] for item in controls)==2 and sum(item['positiveControl'] for item in controls)==2
    assert len(observed)==93 and returns==2048 and verify_inputs(configuration())==inputs
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();vectors=ROOT/'evidence/vectors/main-roster-refresh-20261031.json.gz';vectors.write_bytes(gzip.compress(raw,mtime=0));assert gzip.decompress(vectors.read_bytes())==raw
    artifact=dict(path=vectors.relative_to(ROOT).as_posix(),sha256=sha256(vectors),uncompressedSha256=hashlib.sha256(raw).hexdigest(),compressedBytes=vectors.stat().st_size,uncompressedBytes=len(raw),cases=len(results),gzipMtime=0)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',matches=rows,matchedFunctions=1,matchedBytes=380,nativeSymbolEntries={},
        generatorSources=[dict(path=p,sha256=sha256(ROOT/p)) for p in code_closure(['match_main_roster_refresh_20261031.py'])],
        oracle=dict(pairs=len(results),actualTopReturns=returns,originalHelperActualReturns=native_returns,originalTailTransfers=tails,providedCompletions=providers,
            ownInstructionPcs=len(observed),maximumInstructions=maximum,instructionLimit=18000,vectorArtifact=artifact,verifiedReturn=True,isolatedState=True,wholeArenaCompared=True,
            calleeSavedRegistersCompared=True,completeFinalRegistersCompared=True,stackOutsideFramePreserved=True),
        negativeControls=dict(wholeCompiledCRealLinked=True,source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),byteRefusal=refusal,actualReturns=8,cases=controls),
        replayDependencies=[dict(path=artifact['path'],sha256=artifact['sha256'])],inputsUnchanged=True,wholeModuleLinked=False,sourceCreditAcceptedByThisScript=0,
        returnContract=dict(sourceDeclaration='void',observedRawR0='0x03000000',directCaller='main:0x020D0CEC',qualification='Inventoried direct caller immediately reloads R0; this is a constrained source-level view, not proof of every address-taken caller'),
        limitations=['Default selector byte is bounded to0..3; six100-record search IDs plus null, stale and duplicate IDs use synthetic contexts',
            'Native context/holder/record/category routines execute; six-bit/bitfield storage meanings beyond the measured nibble are unproved',
            '875B4,87E44 and602EC are explicit six/two/six-word provider boundaries with legal volatile-register clobbers, no SDK body or display/hardware claim',
            '61DCC tail-transfers to actual49AD0;49FFC tail-transfers to supplied87E44; those transfers are separate from actual native returns',
            'The initial six holders are valid nonnull wrappers; null wrappers, malformed records, provider reentrancy and mutable globals are unsupported',
            'Fullword IDs at21D6BC0 and three selected context words are measured; inferred roster/UI meanings remain separate from byte-level behavior',
            'The original saved-record search resolves duplicate IDs to the first matching row; this proves no ownership, save chronology or game progression',
            'No additional helper source, complete module, source-only ROM or complete Windows game is credited'])
    write_json(ROOT/'evidence/matches/main-roster-refresh-20261031.json',report)
    print(dict(bytes=380,pairs=len(results),actualTopReturns=returns,originalHelperActualReturns=native_returns,originalTailTransfers=tails,providedCompletions=providers,ownInstructionPcs=len(observed),maximumInstructions=maximum))


if __name__=='__main__':main()
