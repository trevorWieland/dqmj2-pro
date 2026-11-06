import gzip
import json
import hashlib
from pathlib import Path
import match_runtime
import probe_arm7_profiles_20261030 as compiler
import link_arm7_bulk_20261030 as linker
import arm7_byte_initializer56_native_20261101 as native
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-byte-initializer56-final'
WORK=ROOT/'work/arm7-bulk-20261030/lane-byte-initializer56-final-20261101'
REPORT=ROOT/'evidence/matches/arm7-byte-initializer56-20261101.json'
PINS=SOURCE/'generator-pins.json'


def compile_unit(seed,source,directory,strict=True):
    directory.mkdir(parents=True,exist_ok=True);match_runtime.WORK=directory/'isolated-runtime'
    compiler.COMPILER=ROOT/'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe';compiler.COMPILER_HASH=sha256(compiler.COMPILER)
    origin=dict(source=source.relative_to(ROOT).as_posix(),sourceSha256=sha256(source))
    row=compiler.compile_source(seed,origin,source,(2,'off',False,True),directory)
    try:link=linker.validate(row,directory/'real-link')
    except ValueError as error:
        import ast
        if strict:raise
        link=ast.literal_eval(str(error))
        if not isinstance(link,dict)or not all(key in link for key in('nativeBytes','linkedBytes','matchingBytes')):raise ValueError('Unqualified wrong-C link failure')
    return row,link,(directory/'real-link/caller.bin').read_bytes()


def main():
    for item in json.loads(PINS.read_text())['files']:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Required byte source/runtime/module input missing or changed')
    seed=json.loads((SOURCE/'final-seed.json').read_text());row,link,body=compile_unit(seed,ROOT/seed['source'],WORK/'caller')
    original=(ROOT/row['binary']).read_bytes()
    if sha256(ROOT/row['binary'])!='ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416':raise ValueError('Host ARM7 main input differs')
    own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+56];records=[];visited=set()
    for index in range(512):
        first=native.execute(original,own,index);second=native.execute(original,body,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/fresh C initializer full-state/model differs')
        records.append(first);visited.update(first['visited'])
    if visited!=set(range(native.ENTRY,native.ENTRY+48,4)):raise ValueError('Complete initializer code coverage differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    symbols={name:hex(int(value['address'],0))for name,value in link['bindings'].items()}
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],
        sourceDependencies=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
        sourceAbiContract=dict(physicalArgumentWords=1,incomingUnsignedByteDomain=[0,255],observedReturnWord=hex(0x027F8884),historicalSignednessAndReturnTypeProven=False),
        oracle=dict(vectors=512,actualOriginalAndCompiledReturns=1024,providerReplacements=[],independentFullMappedMemoryAndOrderedStoreModel=True,
            completeCodeBytesVisited=48,literalBytes=8,actualOriginalHelperReturns=0,rawRegistersFlagsStackModeAndMappedMemoryCompared=True,
            trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),
            maxInstructionsPerRun=2000,wholeSceneOrHardwareContextProven=False))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',
        romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in json.loads(PINS.read_text())['files']})],
        pinnedGeneratorAndRuntimeDependencies=json.loads(PINS.read_text())['files'],
        matchedInitializedBytes=56,matchedCodeBytes=48,generatedLiteralBytes=8,newOrdinaryFunctionCount=1,
        initializedDenominatorDelta=0,originalDataHelperAssemblyOrExtentCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=1024)),flush=True)


if __name__=='__main__':main()
