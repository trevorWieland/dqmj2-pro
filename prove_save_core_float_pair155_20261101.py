import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_float_pair155_20261101 as F


def main():
    F.main()
    path=ROOT/'evidence/application/save-core-float-pair155-20261101.json'
    report=json.loads(path.read_text())
    assert report['sourceCreditAdded']==0
    assert report['nativeCaseDigest']=='bc12e954d2ae364e7e3f15e63f945f1f32b005b2fc0894162b1abdd78bd08231'
    assert report['counts']==dict(contexts=443,nativeCallerCheckpoints=443,actualParentReturns=0,
        actualCompiledProbeReturns=443,actualHelperReturns=2658,providedCalls=0)
    assert report['compiledWrongConstant']['independentRejections']==4
    assert report['compiledWrongConstant']['positiveControls']==4
    print(F.sha(path.read_bytes()))


if __name__=='__main__':
    main()
