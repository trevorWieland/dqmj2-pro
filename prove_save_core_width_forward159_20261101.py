import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_signed_table157_20261101 as T
import save_core_float_word158_20261101 as F


def main():
    T.main()
    F.main()
    table=json.loads((ROOT/'evidence/application/save-core-signed-table157-20261101.json').read_text())
    floating=json.loads((ROOT/'evidence/application/save-core-float-word158-20261101.json').read_text())
    assert table['nativeCaseDigest']=='db14fb31019118630b8569c36d539885804bc49ee8fcfec15878400a24f23d86'
    assert floating['nativeCaseDigest']=='d6621d020cc1727a4339e0bfed58dafbd40ee509f2502278959e6a7aec4b12ef'
    assert table['sourceCreditAdded']==floating['sourceCreditAdded']==0
    assert table['counts']==dict(contexts=180,nativeCallerCheckpoints=180,actualParentReturns=0,
        actualCompiledProbeReturns=180,actualWrongProbeReturns=180,independentRejections=100,positiveControls=80)
    assert floating['counts']==dict(contexts=484,nativeCallerCheckpoints=484,actualParentReturns=0,
        actualCompiledProbeReturns=484,actualHelperReturns=4840,providedCalls=0)
    assert floating['compiledZeroInputControl']['independentRejections']==4
    assert floating['compiledZeroInputControl']['positiveControls']==4
    print(dict(tableReportSha256=T.sha((ROOT/'evidence/application/save-core-signed-table157-20261101.json').read_bytes()),
        floatingReportSha256=F.sha((ROOT/'evidence/application/save-core-float-word158-20261101.json').read_bytes())))


if __name__=='__main__':
    main()
