import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'evidence/application'), str(ROOT / 'deps/native')]
import save_core_header_bridge143_20261101 as F


def main():
    F.main()
    path = ROOT / 'evidence/application/save-core-header-bridge143-20261101.json'
    report = json.loads(path.read_text())
    assert report['nativeCaseDigest'] == '5caac2058bab83a5e91423bc58418868ab4361065a8fa5f105e35f31516bffc7'
    assert report['counts'] == dict(contexts=82, actualEntryReturns=82, actualHelperReturns=162,
        providedCalls=82, headerStatusCounts={'2': 25, '0': 36, '3': 5, '4': 4, '7': 4, '5': 8})
    assert report['sourceCreditAdded'] == 0
    print(hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == '__main__':
    main()
