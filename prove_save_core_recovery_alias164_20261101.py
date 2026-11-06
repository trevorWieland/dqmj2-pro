import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_recovery_alias164_20261101 as F


def main():
    F.main()
    path=ROOT/'evidence/application/save-core-recovery-alias164-20261101.json'
    report=json.loads(path.read_text())
    assert report['sourceCreditAdded']==0
    assert report['nativeCaseDigest']=='6ac397559bb4175bab710e7a9eaef787de9aef86cd8c10cc021bc0c326cab54f'
    assert report['counts']==dict(contexts=1326,nativeCallerCheckpoints=1326,actualParentReturns=0,
        actualControllerReturns=1326,actualHelperReturns=618,providerCompletedWrapperContinuations=198,providedCalls=1713)
    assert len(report['unsupported'])==2
    assert all(not row['actualControllerReturn'] and not row['postFaultCredit'] for row in report['unsupported'])
    print(F.sha(path.read_bytes()))


if __name__=='__main__':
    main()
