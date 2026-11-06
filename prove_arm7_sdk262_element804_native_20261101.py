import gzip
import hashlib
import json
from pathlib import Path
import arm7_sdk262_element804_native_20261101 as native
from project import ROOT,sha256,write_json

def main():
    main=(ROOT/'extract/arm7/runtime/arm7-main.bin').read_bytes();wram=(ROOT/'extract/arm7/runtime/arm7-wram.bin').read_bytes();rows=[];visited=set();helpers=0
    for index,case in enumerate(native.cases()):
        result=native.run(main,wram,case,index)
        if not result['actualOwnReturn']or not result['modelPassed']:raise ValueError('Native full parser disagrees with independent full-state/store model')
        rows.append(result);visited.update(a for a in result['visited']if native.TOP<=a<native.TOP+800);helpers+=len(result['actualNativeHelperReturns'])
    if visited!=set(range(native.TOP,native.TOP+800,4)):raise ValueError('Complete200 parser instructions not visited')
    raw=(json.dumps(rows,sort_keys=True,separators=(',',':'))+'\n').encode();directory=ROOT/'work/arm7-bulk-20261030/sdk262-element804-native';directory.mkdir(parents=True,exist_ok=True);path=directory/'native-records.json.gz';path.write_bytes(gzip.compress(raw,mtime=0));compatible=sum(native.source_compatible(r['case'])for r in rows)
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),model='arm7_sdk262_element804_native_20261101.py',modelSha256=sha256(ROOT/'arm7_sdk262_element804_native_20261101.py'),nativeModuleSha256=hashlib.sha256(main).hexdigest(),processor='arm7',program='',module='arm7-main',mode='arm',address=hex(native.TOP),bytes=804,codeBytes=800,literalBytes=4,actualOwnReturns=len(rows),actualHelperReturns=helpers,actualPrefixFillReturns=len(rows),all200OwnInstructionsVisited=True,allIndependentWholeMemoryAndOrderedWriteModelsPass=True,sourceCompatibleFixtureCount=compatible,oddCfpTypedPointerContextsExcludedFromSourceCompatibility=len(rows)-compatible,compiledSourceComparison=False,sourceCredit=0,constructorCredit=0,trace=dict(path=path.relative_to(ROOT).as_posix(),compressedSha256=sha256(path),rawSha256=hashlib.sha256(raw).hexdigest(),gzipMtime=0));output=ROOT/'evidence/attempts/arm7-sdk262-element804-native-20261101.json';write_json(output,report);print(json.dumps(dict(report=output.relative_to(ROOT).as_posix(),sha256=sha256(output),returns=len(rows),helpers=helpers,sourceCompatible=compatible)),flush=True)

if __name__=='__main__':main()
