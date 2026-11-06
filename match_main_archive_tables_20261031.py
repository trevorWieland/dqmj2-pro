import gzip
import hashlib
import json
import re
from project import ROOT,configuration,verify_inputs,write_json,sha256
import match_runtime as compiler
from link_runtime_unit import validate,measured_module
from match_main_overlap_copy_20261030 import main_references
from main_archive_tables_native_20261031 import execute,cases,ENTRY,INIT,FILL
from seal_recovery_evidence_20261031 import code_closure

SOURCE='src/runtime/20261031_archive_tables/native_main_0200b97c.c'
BINDINGS={f'native_fn_{address}':dict(module='main',processor='arm9',kind='function',mode='arm',address='0x'+address) for address in ['02008d78','0200b200','0200bd04','0200bf2c','0200c02c','0200c180']}


def main():
    inputs=verify_inputs(configuration());metadata,original,config=measured_module('main')
    helper_sizes={int(address,0):int(size,0) for size,address in re.findall(r'^\S+ kind:function\(arm,size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)$',config,re.M) if int(address,0) in [INIT,FILL]}
    assert len(helper_sizes)==2
    compiler.WORK=ROOT/'work/main-archive-tables-source-20261031/compile';rows,_=compiler.compare(ROOT/SOURCE,'main',2,'off',True);row=rows[0];assert len(rows)==1 and row['exactAfterDeclaredRelocation']
    directory=compiler.WORK.parent/'linked';proof=validate(row,BINDINGS,directory=directory);assert proof['exactCallerBytes'];rebuilt=bytearray(original);rebuilt[ENTRY-0x02000000:ENTRY-0x02000000+292]=(directory/'caller.bin').read_bytes()
    row.update(sourceLanguage='C',ordinaryFunctionCredit=1,originalObjectScaffolding=False,realMainLink=proof,exactAfterRealMwLink=True,sourceDependencies=[])
    row['boundaries']=dict(main_references(row,original,config),instructionBytes=288,literalPoolBytes=4,generatedLiteralOrPaddingBytes=0)
    results=[];observed=set();maximum=0;counts={key:0 for key in ['actualTopReturns','originalInitializerReturns','originalFillReturns','providedCompletions']}
    for tag,case in enumerate(cases()):
        a=execute(original,helper_sizes,case,tag);b=execute(bytes(rebuilt),helper_sizes,case,tag);assert a==b
        results.append(dict(case=case,result=a));observed.update(a['pcs']);maximum=max(maximum,a['state']['instructions'])
        for key in counts:counts[key]+=2*a['state'][key]
    text=(ROOT/SOURCE).read_text(encoding='utf-8-sig');wrong=text.replace('| 4);','| 8);');assert wrong!=text
    path=ROOT/'nonmatching/main-runtime/20261031/archive-tables/wrong-flag.c';path.parent.mkdir(parents=True,exist_ok=True);path.write_text(wrong,encoding='utf-8');compiler.WORK=ROOT/'work/main-archive-tables-control-20261031/compile';bad,_=compiler.compare(path,'main',2,'off',True);directory=compiler.WORK.parent/'linked'
    try:validate(bad[0],BINDINGS,directory=directory)
    except ValueError as error:refusal=str(error)
    else:raise AssertionError('Wrong whole C matched')
    payload=(directory/'caller.bin').read_bytes();assert len(payload)==292;mutant=bytearray(original);mutant[ENTRY-0x02000000:ENTRY-0x02000000+292]=payload
    controls=[];base=dict(a=31,b=33,shift=1,capacity=96,opened=(True,True),results=(0xFFFFFFFF,0x80000000))
    for tag,(flags,capacity) in enumerate([(0,95),(0x80000000,0),(12,96),(0,96),(4,96),(8,96)]):
        case=dict(base,flags=flags,capacity=capacity);a=execute(original,helper_sizes,case,tag);b=execute(bytes(mutant),helper_sizes,case,tag,check=False)
        controls.append(dict(case=case,actualReturns=2,rejected=not b['modelPassed'],positiveControl=b['modelPassed']))
    assert sum(x['rejected'] for x in controls)==3 and sum(x['positiveControl'] for x in controls)==3
    assert verify_inputs(configuration())==inputs
    raw=json.dumps(results,sort_keys=True,separators=(',',':')).encode();compressed=gzip.compress(raw,mtime=0);vectors=ROOT/'evidence/vectors/main-archive-tables-20261031.json.gz';vectors.parent.mkdir(parents=True,exist_ok=True);vectors.write_bytes(compressed);assert gzip.decompress(vectors.read_bytes())==raw
    artifact=dict(path=vectors.relative_to(ROOT).as_posix(),sha256=sha256(vectors),uncompressedSha256=hashlib.sha256(raw).hexdigest(),compressedBytes=len(compressed),uncompressedBytes=len(raw),cases=len(results),gzipMtime=0)
    report=dict(schemaVersion=1,romSha256=configuration()['romSha256'],processor='arm9',module='main',matches=rows,matchedFunctions=1,matchedBytes=292,nativeSymbolEntries={},generatorSources=[dict(path=p,sha256=sha256(ROOT/p)) for p in code_closure(['match_main_archive_tables_20261031.py'])],oracle=dict(pairs=len(results),**counts,ownInstructionPcs=len(observed),maximumInstructions=maximum,instructionLimit=4000,vectorArtifact=artifact,verifiedReturn=True,isolatedState=True,wholeArenaCompared=True,calleeSavedRegistersCompared=True,stackOutsideFramePreserved=True),negativeControls=dict(wholeCompiledCRealLinked=True,source=path.relative_to(ROOT).as_posix(),sourceSha256=sha256(path),byteRefusal=refusal,actualReturns=12,cases=controls),replayDependencies=[dict(path=artifact['path'],sha256=artifact['sha256'])],inputsUnchanged=True,wholeModuleLinked=False,sourceCreditAcceptedByThisScript=0,limitations=[
        'Two disjoint bounded synthetic chunks and a nonoverlapping raw metadata record; ordinary filesystem/archive reachability is unproved',
        'Original initializer and byte fill execute and return; open/read/close are explicit supplied boundaries with separate completion counts',
        'A supplied read can write a short prefix before a negative result; the caller then clears the full requested length through the original fill',
        'Raw offsets2C/30/34/38/44/50/1C and callback0200B200 are measured; no save serialization, asset identity or live filesystem behavior is inferred',
        'The72-byte local storage restores the native76-byte allocation plus20-byte register save; it is an opaque buffer rather than a recovered complete file structure',
        'Capacity rejection includes unsigned sum wrap without dereferencing huge segments; successful large segments, invalid pointers, overlapping chunks and mutable metadata providers are unsupported',
        'No original open/read/close/callback source, complete module, source-only ROM or complete Windows game is credited'])
    write_json(ROOT/'evidence/matches/main-archive-tables-20261031.json',report);print(dict(bytes=292,pairs=len(results),**counts,ownInstructionPcs=len(observed),maximumInstructions=maximum))


if __name__=='__main__':main()
