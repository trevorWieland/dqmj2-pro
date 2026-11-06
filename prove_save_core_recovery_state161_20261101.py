import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_recovery_state161_fixtures_20261101 as F


def main():
    F.main()
    path=ROOT/'evidence/application/save-core-recovery-state161-20261101.json'
    r=json.loads(path.read_text())
    assert r['sourceCreditAdded']==0
    assert r['nativeCaseDigest']=='75908dc239ad8c7fd686fae8a1f093efe7d30c19abd44753c34855a69995bedc'
    assert r['sequences']['nativeCaseDigest']=='b2ab4efce236894a5a4a49377385519924586e4a3a4c700cb430fb2216d786f0'
    assert r['counts']==dict(contexts=1326,actualEntryReturns=1326,actualHelperReturns=618,
        providerCompletedWrapperContinuations=198,providedCalls=1713)
    assert r['sequences']['actualEntryReturns']==698 and r['sequences']['actualHelperReturns']==12
    assert r['sequences']['providerCompletedWrapperContinuations']==6
    assert r['sequences']['providedCalls']==274
    print(F.sha(path.read_bytes()))


if __name__=='__main__':
    main()
