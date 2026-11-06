import json
import subprocess
import sys
from project import ROOT,sha256

PINS={'prove_arm7_host_sleep_callback32_scope_20261101.py': '682f633cd01f13ef827a91ba6e1a13edcfadc2818c9ed22bce4ea606ba54d0a3', 'validate_arm7_host_sleep_callback32_scope_20261101.py': 'cdde8e848bdf2d71c8b0bf53dcbb0f8d98e58cb12942042a24986bd2993b2d65', 'arm7_host_sleep_callback32_native_20261101.py': 'f7bdc55395f34724c8b11a7c1dc5bdf470527f2b9be2f443845104d72f70219c', 'arm7_host_sleep_callback32_native_engine_20261101.py': 'a1bdcf9a398c3a78a0ca9e200a03b5a8cc6dc0b2773014dba200faf8cc818dd0'}
SCRIPTS=('prove_arm7_host_sleep_callback32_scope_20261101.py', 'validate_arm7_host_sleep_callback32_scope_20261101.py')

PRODUCTS={'evidence/attempts/arm7-host-sleep-callback32-scope-20261101.json': 'f3c4c503e7f228455ae3bdc5502d6d2dc9a36c36acd62ef9e1e4c68e76b1fc1e', 'evidence/verification/arm7-host-sleep-callback32-scope-controls-20261101.json': 'f6792ecc80f9791700be6555bf994bc1db126b3158f66208c1502a3faf63ff11'}


def main():
    for path,expected in PINS.items():
        if sha256(ROOT/path)!=expected:raise ValueError('Frozen callback witness source changed: '+path)
    logs=ROOT/'work/arm7-bulk-20261030/lane-host-sleep-callback32-native/replay-logs'
    logs.mkdir(parents=True,exist_ok=True)
    for script in SCRIPTS:
        result=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True,timeout=300)
        (logs/(script+'.stdout.txt')).write_text(result.stdout)
        (logs/(script+'.stderr.txt')).write_text(result.stderr)
        if result.returncode:raise ValueError('Frozen callback witness child failed: '+script+' '+result.stderr)
    for path,expected in PRODUCTS.items():
        if sha256(ROOT/path)!=expected:raise ValueError('Frozen callback witness product changed: '+path)
    print(json.dumps(dict(replayed=list(SCRIPTS),reports=PRODUCTS,sourceCredit=0,callerActualOuterReturns=0)),flush=True)


if __name__=='__main__':main()
