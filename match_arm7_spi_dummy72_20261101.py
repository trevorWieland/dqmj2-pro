import gzip
import hashlib
import json
from pathlib import Path
import match_arm7_main_spi276_20261101 as compiler
import arm7_spi_dummy72_native_20261101 as native
import audit_arm7_lane_scope107_20261101 as exclusion
from project import ROOT,sha256,write_json
SOURCE=ROOT/'nonmatching/arm7-bulk/20261101/lane-spi-dummy72-final'
WORK=ROOT/'work/arm7-bulk-20261030/spi-dummy72-final'
REPORT=ROOT/'evidence/matches/arm7-spi-dummy72-20261101.json'
PINS=SOURCE/'generator-pins.json'
EXCLUSION='evidence/verification/lane-root108-connected-exclusion-observed-20261101.json'


def main():
    pins=json.loads(PINS.read_text())['files']
    for item in pins:
        path=(ROOT/item['path']).resolve()
        if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=item['sha256']:raise ValueError('Complete current dummy-pair input/source closure differs')
    ownership=compiler.ownership();profile=json.loads((SOURCE/'profile.json').read_text())['units'];selected=json.loads((ROOT/EXCLUSION).read_text())['functions'];original=(ROOT/profile[0]['binary']).read_bytes();matches=[]
    for seed in profile:
        address=int(seed['address'],0)
        if any(exclusion.overlaps(selected,('arm7','','arm7-wram',mode,address,36))for mode in('arm','thumb')):raise ValueError('Dummy-pair source overlaps historical normalized selected extent')
        row,link,body=compiler.compile_unit(seed,ROOT/seed['source'],WORK/seed['address'][2:]);own=original[address-native.BASE:address-native.BASE+36];records=[];visited=set()
        if body!=own:raise ValueError('Complete current dummy unit source link differs')
        for index,case in enumerate(native.cases()):
            first=native.execute(original,address,own,case,index);second=native.execute(original,address,body,case,index)
            if first!=second or not first['modelPassed']:raise ValueError('Dummy-pair original/source CPU/halfword/frame model differs')
            records.append(dict(case=case,execution=first));visited.update(first['visited'])
        if visited!=set(range(address,address+32,4)):raise ValueError('Dummy complete eight-instruction domain differs')
        unsupported=[]
        for index,case in enumerate([dict(native.cases()[0],stuck=True)]):
            first=native.execute(original,address,own,case,index,budget=300,allow_no_return=True);second=native.execute(original,address,body,case,index,budget=300,allow_no_return=True)
            if first!=second or first['actualOwnReturn']or not first['busyPortReached']:raise ValueError('Permanent busy did not reach its measured bounded loop')
            unsupported.append(dict(execution=first,supportedErrorPathCredit=0))
        raw=(json.dumps(records,sort_keys=True,separators=(',',':'))+'\n').encode();trace=WORK/seed['address'][2:]/'native-records.json.gz';trace.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0));wram=next(x for x in ownership['modules']if x['module']=='arm7-wram');image_offset=wram['sourceImageOffset']+address-native.BASE
        row.update(realLink=link,exactBytes=True,exactAfterDeclaredRelocation=True,nativeSymbols={},nativeSymbolEntries=link['bindings'],sourceOnlyCompilerInput=True,originalObjectScaffolding=False,sourceAbiContract=dict(physicalArgumentWords=0,rawReturnBits=32,zeroExtendedControlHalfword=True,volatileHalfwordPorts=['0x40001c0','0x40001c2'],busyBit=128,historicalPublicDevicePolicyMeaningProven=False),physicalSource=dict(inputImageOffset=image_offset,romOffset=ownership['romArm7Offset']+image_offset,bytes=36,runtimeBase=hex(native.BASE),module='arm7-wram',noInitializedDenominatorIncrease=True),oracle=dict(vectors=len(records),actualOriginalAndCompiledReturns=2*len(records),actualNestedReturns=0,allOwnInstructionsVisited=True,independentFullHalfwordPollModel=True,rawRegistersFlagsStackAndMappedMemoryCompared=True,providerReplacements=[],physicalPeripheralExecution=False,wholeHardwareContextProven=False,unsupported=unsupported,maxInstructionsPerRun=1000,trace=dict(path=trace.relative_to(ROOT).as_posix(),rawSha256=hashlib.sha256(raw).hexdigest(),compressedSha256=sha256(trace),gzipMtime=0)));matches.append(row)
    names={Path(__file__).name,PINS.relative_to(ROOT).as_posix()}|{x['path']for x in pins};report=dict(schemaVersion=1,generator=Path(__file__).name,generatorSha256=sha256(__file__),processor='arm7',program='',module='arm7-wram',romSha256='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6',matches=matches,nativeSymbols={},runtimeOwnership=ownership,generatorSources=[dict(path=x,sha256=sha256(ROOT/x))for x in sorted(names)],pinnedGeneratorAndRuntimeDependencies=pins,newOrdinaryFunctionCount=2,matchedInitializedBytes=72,matchedCodeBytes=64,generatedLiteralBytes=8,initializedDenominatorDelta=0,totalActualOwnReturns=sum(x['oracle']['actualOriginalAndCompiledReturns']for x in matches),existingImplementationFamily='spi_dummy_halfword_poll',newImplementationFamilyCount=0,wholeModuleLinked=False,sourceReconstructionComplete=False,originalDataAssemblyOrExtentCredit=0);write_json(REPORT,report);print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(),sha256=sha256(REPORT),ownReturns=report['totalActualOwnReturns'])),flush=True)
if __name__=='__main__':main()
