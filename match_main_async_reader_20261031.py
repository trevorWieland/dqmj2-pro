import gzip
import hashlib
import json
from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import measured_module,validate
from match_main_overlap_copy_20261030 import main_references
from main_async_reader_native_20261031 import execute,ENTRY
from main_async_reader_models_20261031 import recipes
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_async_reader/native_main_0202a954.c'
BINDINGS={f'native_fn_{address:08x}':dict(processor='arm9',module='main',mode='arm',kind='function',address=hex(address))for address in [0x0200BD04,0x0200BFE4,0x0200C170,0x0200C190]}
BINDINGS.update({f'native_data_{address:08x}':dict(processor='arm9',module='main',mode='data',kind='data',address=hex(address))for address in [0x020EDEC8,0x020EDECC]})


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main')
    compiler.WORK=ROOT/'work/main-async-reader-source-20261031/compile';rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',True)
    assert len(rows)==1 and rows[0]['exactAfterDeclaredRelocation'];row=rows[0]
    directory=compiler.WORK.parent/'linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes'];payload=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=252,literalPoolBytes=8,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();counts={key:0 for key in ['actualTopReturns','actualInitializerReturns','providedCompletions']};maximum=0
    for case in recipes():
        a=execute(original,case);b=execute(original,case,payload);assert a==b
        results.append(dict(case=case,result=a));observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions'])
        for key in counts:counts[key]+=2*a['state'][key]
    text=(ROOT/SOURCE).read_text(encoding='utf-8-sig');wrong=text.replace('native_data_020edec8 = 2;','native_data_020edec8 = 3;');assert wrong!=text
    path=ROOT/'nonmatching/main-runtime/20261031/async-reader/wrong-read-status.c';path.write_text(wrong,encoding='utf-8');compiler.WORK=ROOT/'work/main-async-reader-control-20261031/compile'
    bad,_=compiler.compare(path,'main',2,'off',True);directory=compiler.WORK.parent/'linked'
    try:validate(bad[0],BINDINGS,directory=directory)
    except ValueError as error:refusal=str(error)
    else:raise AssertionError('Wrong whole C matched')
    bad_payload=(directory/'caller.bin').read_bytes();controls=[]
    chosen=[]
    for negative in [False,True]:
        filtered=[case for case in recipes()if bool(not case['busy']and not case['flags']&1 and case['opened']and not case['read'])==negative]
        chosen.extend(filtered[:8])
    for case in chosen:
        a=execute(original,case);b=execute(original,case,bad_payload,check=False)
        controls.append(dict(case=case,rejected=not b['modelPassed'],positiveControl=b['modelPassed'],actualReturns=2))
    assert sum(case['rejected']for case in controls)==8 and sum(case['positiveControl']for case in controls)==8
    assert len(observed)==63 and counts['actualTopReturns']==2880 and verify_inputs(configuration())==inputs
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();vectors=ROOT/'evidence/vectors/main-async-reader-20261031.json.gz';vectors.write_bytes(gzip.compress(raw,mtime=0))
    assert gzip.decompress(vectors.read_bytes())==raw
    artifact=dict(path=vectors.relative_to(ROOT).as_posix(),sha256=sha256(vectors),uncompressedSha256=hashlib.sha256(raw).hexdigest(),compressedBytes=vectors.stat().st_size,uncompressedBytes=len(raw),cases=len(results),gzipMtime=0)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',matches=rows,matchedFunctions=1,matchedBytes=260,nativeSymbolEntries={},
        generatorSources=[dict(path=p,sha256=sha256(ROOT/p))for p in code_closure(['match_main_async_reader_20261031.py'])],
        oracle=dict(pairs=len(results),**counts,ownInstructionPcs=len(observed),maximumInstructions=maximum,instructionLimit=1500,
            vectorArtifact=artifact,verifiedReturn=True,isolatedState=True,wholeRamCompared=True,completeFinalRegistersCompared=True,stackOutsideFramePreserved=True),
        negativeControls=dict(wholeCompiledCRealLinked=True,source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),byteRefusal=refusal,actualReturns=32,cases=controls),
        replayDependencies=[dict(path=artifact['path'],sha256=artifact['sha256'])],inputsUnchanged=True,wholeModuleLinked=False,sourceCreditAcceptedByThisScript=0,
        limitations=['Null input selects the original default context; valid disjoint84-byte contexts, opaque path/buffer words and stable pre-call state are bounded synthetic inputs',
            'Original40-byte file initialization executes; open,seek and asynchronous-read acceptance are explicit providers, with file/error mutations and legal volatile-register/flag clobbers',
            'Request length is cached before a supplied seek mutates file bounds; full32-bit unsigned bound subtraction wraps exactly without a signed-overflow hypothesis',
            'Busy nonzero and flagbit0 rejection order, five measured error/status values and final busy/length/buffer stores are tested; no real file IO, async completion or ordinary scene is inferred',
            'No malformed context pointers, overlapping context/code, unbounded hardware waits, later completion callbacks or concurrent writes are claimed',
            'Declaration initialization reproduces the native immediate-zero selection without forced registers, assembly or instruction patching',
            'No additional initializer/service source, complete module, source-only ROM or complete Windows game is credited'])
    write_json(ROOT/'evidence/matches/main-async-reader-20261031.json',report);print(dict(bytes=260,pairs=len(results),**counts,ownInstructionPcs=len(observed),maximumInstructions=maximum))


if __name__=='__main__':main()
