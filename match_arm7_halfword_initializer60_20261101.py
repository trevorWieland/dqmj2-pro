import gzip
import json
import hashlib
from pathlib import Path
import match_runtime
import probe_arm7_profiles_20261030 as compiler
import link_arm7_bulk_20261030 as linker
import arm7_halfword_initializer60_native_20261101 as native
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-cache-halfword60'
WORK=ROOT/'work/arm7-bulk-20261030/lane-halfword-initializer60-final-20261101'
REPORT=ROOT/'evidence/matches/arm7-halfword-initializer60-20261101.json'
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
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Required halfword source/runtime/module input missing or changed')
    seed=json.loads((SOURCE/'final-seed.json').read_text());row,link,body=compile_unit(seed,ROOT/seed['source'],WORK/'caller')
    original=(ROOT/row['binary']).read_bytes()
    if sha256(ROOT/row['binary'])!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Host WRAM input differs')
    own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+60];records=[];visited=set()
    for index in range(256):
        first=native.execute(original,own,index);second=native.execute(original,body,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/fresh C initializer full-state/model differs')
        records.append(first);visited.update(first['visited'])
    if visited!=set(range(native.ENTRY,native.ENTRY+52,4)):raise ValueError('Complete initializer code coverage differs')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    symbols={name:hex(int(value['address'],0))for name,value in link['bindings'].items()}
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],
        sourceDependencies=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
        sourceAbiContract=dict(physicalArgumentWords=0,observedReturnWord=hex(native.STATE+4),historicalReturnTypeProven=False),
        oracle=dict(vectors=256,actualOriginalAndCompiledReturns=512,providerReplacements=[],independentFullMappedMemoryAndOrderedStoreModel=True,
            completeCodeBytesVisited=52,literalBytes=8,actualOriginalHelperReturns=0,rawRegistersFlagsStackModeAndMappedMemoryCompared=True,
            trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),
            maxInstructionsPerRun=2000,wholeSceneOrHardwareContextProven=False))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',
        romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in json.loads(PINS.read_text())['files']})],
        pinnedGeneratorAndRuntimeDependencies=json.loads(PINS.read_text())['files'],
        matchedInitializedBytes=60,matchedCodeBytes=52,generatedLiteralBytes=8,newOrdinaryFunctionCount=1,
        initializedDenominatorDelta=0,originalDataHelperAssemblyOrExtentCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=512)),flush=True)


if __name__=='__main__':main()
