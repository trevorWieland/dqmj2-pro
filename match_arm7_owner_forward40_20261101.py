import gzip
import json
import hashlib
from pathlib import Path
import match_runtime
import probe_arm7_profiles_20261030 as compiler
import link_arm7_bulk_20261030 as linker
import arm7_owner_forward40_native_20261101 as native
from project import ROOT,sha256,write_json

SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-owner-forward40-final'
WORK=ROOT/'work/arm7-bulk-20261030/lane-owner-forward40-final-20261101'
REPORT=ROOT/'evidence/matches/arm7-owner-forward40-20261101.json'
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
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Required owner-forward source/runtime/module missing or changed')
    seed=json.loads((SOURCE/'seed.json').read_text());row,link,body=compile_unit(seed,ROOT/seed['source'],WORK/'caller');original=(ROOT/row['binary']).read_bytes();own=original[native.ENTRY-native.BASE:native.ENTRY-native.BASE+40];records=[];own_visited=set();tail_returns=irq_returns=callbacks=0
    if int.from_bytes(original[0x3b80:0x3b84],'little')!=0x037fbb58 or tuple(int.from_bytes(original[o:o+4],'little')for o in(0x3b6c,0x3b70,0x3b74))!=(0x037fba18,0x027fffe8,0x037fbba8):raise ValueError('Actual complete original tail/owner-field/callback setup differs')
    for index,case in enumerate(native.cases()):
        first=native.execute(original,own,case,index);second=native.execute(original,body,case,index)
        if first!=second or not first['modelPassed']:raise ValueError('Original/fresh C actual owner ABI/lock/IRQ/full-state model differs')
        records.append(dict(case=case,execution=first));own_visited.update(first['visited'][hex(native.ENTRY)]);tail_returns+=2*first['actualTailChainReturns'];irq_returns+=2*first['actualOriginalIrqReturns'];callbacks+=2*first['actualOriginalCallbackReturns']
    if len(records)!=840 or own_visited!=set(range(native.ENTRY,native.ENTRY+40,4))or(tail_returns,irq_returns,callbacks)!=(560,1840,80):raise ValueError('Complete owner-forward own coverage/nested boundary counts differ')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));symbols={name:hex(int(value['address'],0))for name,value in link['bindings'].items()}
    row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols=symbols,nativeSymbolEntries=link['bindings'],sourceDependencies=[],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,
        sourceAbiContract=dict(physicalArgumentWords=2,firstWordForwardedToQualifiedTailChain=True,contextPrefixBytes=8,ordinaryRamNotVolatile=True,callerResult='previous IRQ I-bit'),
        oracle=dict(vectors=840,actualOriginalAndCompiledReturns=1680,actualTailChainReturnsSeparateZeroCredit=560,actualOriginalIrqReturnsSeparateZeroCredit=1840,actualOriginalCallbackReturnsSeparateZeroCredit=80,completeCodeBytesVisited=40,literalBytes=0,providerReplacements=[],allNativeTailCallbackAndIrqCodeRetained=True,
            independentSharedPageOwnerCompareAndOrderedLockStoreModel=True,rawRegistersFlagsStackModeAndMappedMemoryCompared=True,ownerWords=[0,1,2,0x7fff,0xffff,0x10000,0xffffffff],heldUnsignedHalfwords=[0,1,2,0x7fff,0xffff],contextStateWords=[0,1,0xffffffff],savedIrqMasks=[0,0x80],initialIrqFiqMasks=[0,0x40,0x80,0xc0],syntheticSharedLockAddress='0x27fffe8',
            tailWitness=dict(qualifyingEntry='0x37fbb78',forwardingEntry='0x37fbb58',actualCommonEntry='0x37fba18',fixedCallback='0x37fbba8',fixedFlag=1,ownerFieldOffset=4,ownerFieldReadWidth=2,callerWordComparedWithoutNarrowing=True,originalModuleSha256=row['inputModuleSha256'],calleeSourceDataOrExtentCredit=0,completeCommonHelperOtherBranchesProven=False),
            trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),maxInstructionsPerRun=2000,wholeSceneOrHardwareContextProven=False))
    report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=[row],nativeSymbols=symbols,
        generatorSources=[dict(path=name,sha256=sha256(ROOT/name))for name in sorted({Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins})],pinnedGeneratorAndRuntimeDependencies=pins,
        matchedInitializedBytes=40,matchedCodeBytes=40,generatedLiteralBytes=0,newOrdinaryFunctionCount=1,initializedDenominatorDelta=0,originalDataHelperAssemblyOrExtentCredit=0,wholeModuleLinked=False,sourceReconstructionComplete=False)
    write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),actualOwnReturns=1680,tailReturnsSeparate=560,irqReturnsSeparate=1840,callbackReturnsSeparate=80)),flush=True)
if __name__=='__main__':main()
