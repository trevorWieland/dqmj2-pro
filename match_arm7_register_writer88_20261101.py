import gzip
import json
import hashlib
from pathlib import Path
import match_runtime
import probe_arm7_profiles_20261030 as compiler
import link_arm7_bulk_20261030 as linker
import arm7_register_writer88_native_20261101 as native
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-register-writer88-final'
WORK=ROOT/'work/arm7-bulk-20261030/lane-register-writer88-final-20261101'
REPORT=ROOT/'evidence/matches/arm7-register-writer88-20261101.json'
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
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Required register-writer source/runtime/module input missing or changed')
    seed=json.loads((SOURCE/'final-seed.json').read_text());row,link,body=compile_unit(seed,ROOT/seed['source'],WORK/'caller')
    original=(ROOT/row['binary']).read_bytes()
    if sha256(ROOT/row['binary'])!='e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c':raise ValueError('Host WRAM input differs')
    own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+88];records=[];visited=set();lower_visited=set();cases=native.cases()
    if len(cases)!=580 or {x['selector']&255 for x in cases}!=set(range(256))or {x['value']&255 for x in cases}!=set(range(256)):raise ValueError('Complete byte-input domains differ')
    for index,case in enumerate(cases):
        first=native.execute(original,own,case,index);second=native.execute(original,body,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/fresh C register writer full-state/model differs')
        records.append(dict(case=case,execution=first));visited.update(first['visitedOwn']);lower_visited.update(first['visitedNested'])
    if visited!=set(range(native.ENTRY,native.ENTRY+76,4))or lower_visited!=set(range(native.HELPER,native.HELPER+32,4)):raise ValueError('Complete owned/original-helper code coverage differs')
    unsupported=[]
    for name,case,budget in [('stuck-before',dict(cases[0],stuck='Before'),500),('stuck-nested',dict(cases[0],stuck='Nested'),500),('one-instruction',cases[0],1)]:
        first=native.execute(original,own,case,0,budget=budget,allow_no_return=True);second=native.execute(original,body,case,0,budget=budget,allow_no_return=True)
        if first!=second or first.get('actualOwnReturn')or first.get('actualNestedReturns'):raise ValueError('Unsupported busy/budget path acquired a return')
        unsupported.append(dict(name=name,originalAndCompiled=first,supportedErrorPathCredit=0))
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
    symbols={name:hex(int(value['address'],0))for name,value in link['bindings'].items()}
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],sourceDependencies=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
        sourceAbiContract=dict(physicalArgumentWords=2,sourceWordParameters=True,observedResult='second input word & 255',historicalTypesProven=False),
        oracle=dict(vectors=580,actualOriginalAndCompiledReturns=1160,actualOriginalHelperReturns=1160,completeCodeBytesVisited=76,literalBytes=12,originalHelperCodeBytesVisited=32,originalHelperEntry=hex(native.HELPER),originalHelperBytes=36,originalHelperSha256=hashlib.sha256(original[native.HELPER-native.BASE:native.HELPER-native.BASE+36]).hexdigest(),originalHelperSourceCredit=0,
            providerReplacements=[],syntheticBusReadContract=dict(addresses=[hex(native.CONTROL)],width=2,finiteBusyCounts=[0,1,2,3],allByteSelectorsAndValuesCovered=True,stickyStatusWords=[0,0x4002,0xff7f,0x8802,0x7f7f],physicalPeripheralExecution=False),
            independentFullMappedMemoryStackAndOrderedStoreModel=True,rawRegistersFlagsStackModeAndMappedMemoryCompared=True,nativeCallArgumentAndReturnObserved=True,
            trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),unsupported=unsupported,maxInstructionsPerRun=5000,wholeSceneOrHardwareContextProven=False))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,
        matchedInitializedBytes=88,matchedCodeBytes=76,generatedLiteralBytes=12,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,originalDataHelperAssemblyOrExtentCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=1160,originalHelperReturnsSeparate=1160)),flush=True)
if __name__=='__main__':main()
