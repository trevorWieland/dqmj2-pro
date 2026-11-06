import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parent
sys.path[:0]=[str(ROOT),str(ROOT/'evidence/application'),str(ROOT/'deps/native')]
import save_core_large_entry152_20261101 as F


def main():
    F.main()
    p=ROOT/'evidence/application/save-core-large-entry152-20261101.json'
    r=json.loads(p.read_text())
    assert r['sourceCreditAdded']==0
    assert r['nativeCaseDigest']=='2eb03bf35cb00c3b967e4a33268e7f0c8659ffce6b25e994472586671fd67770'
    assert r['counts']==dict(contexts=112,actualEntryReturns=224,actualHelperReturns=1008,suppliedCalls=112)
    print(hashlib.sha256(p.read_bytes()).hexdigest())


if __name__=='__main__':
    main()
