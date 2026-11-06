import gzip
import hashlib
import json
from pathlib import Path
import compile_arm7_core127_helper128_virtual_20261101 as compiler
import arm7_core127_helper128_source_native_20261101 as native
import compile_arm7_core126_state76_20261101 as getter_compiler
import prove_arm7_lane_setting_producer_20261031 as producer
import link_arm7_bulk_20261030 as linker
from project import ROOT,sha256,write_json
WORK=ROOT/'work/arm7-bulk-20261030/core127-helper128-functional'
REPORT=ROOT/'evidence/attempts/arm7-core127-helper128-functional-20261101.json'
PINS=ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core127-helper128-functional/generator-pins.json'


def normalized(value):
    writes=[list(x)for x in value['orderedWrites']];slot=0x03033800-8-16+12
    for row in writes:
        if row[0]==slot and row[1]==4:row[2]=native.TOP+0x1c
    return dict(result=value['rawResult'],privateWord=value['privateWord'],registers=[value['rawRegisters'][j]for j in[0,3,*range(4,12),13,14]],cpsr=value['cpsr'],normalizedRegionHashes=value['normalizedOriginalRegionHashes'],orderedWritesWithOnlyActualCallLrSlotNormalized=writes,modelChecks=value['modelChecks'])


def main():
    producer.main();pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Helper128 typed functional input/source/runtime closure differs')
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();seed=json.loads((ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core124-pointer128/profile.json').read_text())['units'][0];modules,functions=linker.namespace('');bindings={'native_host_arm7_arm_027f4e1c':functions[0x27f4e1c],'native_host_arm7_arm_027ea584':functions[0x27ea584],'native_host_arm7_io_048080bc':linker.data_binding(seed,0x048080bc,modules),'native_host_arm7_io_04808140':linker.data_binding(seed,0x04808140,modules)};body,build=compiler.build(dict(seed,address='0x26d0000'),(ROOT/seed['source']).read_text(),WORK/'virtual',bindings)
    if len(body)!=136:raise ValueError('Complete functional C code/pool extent changed')
    getter_seed=json.loads((ROOT/'nonmatching/arm7-bulk/20261101/lane-main-core126-state76-final/profile.json').read_text())['units'][0];getter_row,getter_link,getter_body=getter_compiler.compile_unit(getter_seed,ROOT/getter_seed['source'],WORK/'source-getter76',strict=True);source_main=bytearray(main);source_main[0xa584:0xa584+76]=getter_body;records=[];scratch=0;helper_events=0;visited=set()
    for index,case in enumerate(native.cases()):
        first=native.run(main,wram,case,index);second=native.run(bytes(source_main),wram,case,index,body=body,entry=0x026d0000)
        if not first['modelPassed']or not second['modelPassed']or normalized(first)!=normalized(second):raise ValueError('Original/relocated C private word/ABI/flag/full normalized memory and write model differs')
        differences=[j for j in(1,2,12)if first['rawRegisters'][j]!=second['rawRegisters'][j]];scratch+=bool(differences);helper_events+=first['scopedHelperReturns']+second['scopedHelperReturns'];visited.update(first['visited']);records.append(dict(case=case,original=first,compiled=second,scratchRegisterDifferences=differences))
    if not set(range(native.TOP,native.TOP+116,4)).issubset(visited):raise ValueError('Complete original owned code not visited')
    raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));names={Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins};report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-main',originalAddress=hex(native.TOP),nativeBytes=128,compiledBytes=136,compiledCodeBytes=116,compiledLiteralBytes=20,virtualExecutionAddress='0x26d0000',source=seed,virtualBuild=build,freshSourceGetter76=dict(source=getter_row,realLink=getter_link,additionalSourceCredit=0),vectors=len(records),actualOriginalAndCompiledOwnReturns=2*len(records),actualFillReturnsSeparate=2*len(records),constructorActualReturnCredit=0,actualNestedHelperEventsSeparate=helper_events,sourceGetter76ReturnsWithOriginalCounterpartsScopedWithinOwnRuns=2*len(records),scratchDifferenceCases=scratch,fullRawRegisterOrReadInterleavingEquivalenceClaimed=False,R0R3CalleeSavedSpLrFlagsAndAllNormalizedRamMatch=True,onlyActualTransferReturnLrStackSlotNormalized=True,orderedWritesEquivalentAfterOnlyDeclaredLrNormalization=True,ownCodeAndPoolReadAddressesDifferByDeclaredVirtualLayout=True,portReadOccursBeforePrivateSubtractionStoreInC=True,noAsynchronousPortOrConcurrencyEquivalenceClaimed=True,allSupportedOwnedBranchAndInstructionCoverage=True,actualTransferByteGetterByteWriterAndStateGetterNoProviders=True,generatorSources=[dict(path=n,sha256=sha256(ROOT/n))for n in sorted(names)],pinnedGeneratorAndRuntimeDependencies=pins,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0),sourceAdmissionAccepted=False,matchedSourceDataAndDenominatorCredit=0,physicalHardwareOrGameReachabilityProven=False);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=report['actualOriginalAndCompiledOwnReturns'],helperEvents=helper_events,scratchDifferenceCases=scratch,sourceCredit=0)),flush=True)
if __name__=='__main__':main()
