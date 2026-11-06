import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


RUNTIME_INPUTS = {
    'extract/arm7/runtime/arm7-wram.bin': 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c',
    'extract/arm7/runtime/arm7-main.bin': 'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416',
    'extract/utility/runtime/utility-child-arm7-main.bin': 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a',
    'extract/utility/runtime/utility-child-arm7-wram.bin': '13c0f0469f28daf8fa0921ba61bd78bac7427fb872ef191ba234cd2a73f064d6'}
PARENTS = {
    'arm7_runtime.py': ('extract/arm7/arm7.bin', '9f40087972ccb8b89d4cc4baf8288123e26a479bb43fa68b18a30a59650633a1'),
    'utility_runtime.py': ('extract/files/dwc/utility.bin', 'db8ee36170897f60791f713b7669c50a125e62c6ad775fda98466c85fe48e81e')}


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def materialize(root):
    root = Path(root).resolve()
    registry = json.loads((root / 'recovery.json').read_text(encoding='utf-8-sig'))
    pins = {}
    for batch in registry['batches']:
        for name, expected in batch['sourceHashes'].items():
            if name in pins and pins[name] != expected:
                raise ValueError('Conflicting accepted runtime/source hash')
            pins[name] = expected
    missing = []
    for name, expected in RUNTIME_INPUTS.items():
        if name not in pins:
            continue
        if pins[name] != expected:
            raise ValueError('Unexpected measured runtime input pin: ' + name)
        path = root / name
        if not path.is_file():
            missing.append(name)
        elif digest(path) != expected:
            raise ValueError('Existing measured runtime input changed: ' + name)
    generators = [name for name in PARENTS if any(path.startswith('extract/arm7/runtime/' if name == 'arm7_runtime.py' else 'extract/utility/runtime/') for path in missing)]
    for name in generators:
        if name not in pins or digest(root / name) != pins[name]:
            raise ValueError('Accepted runtime generator identity differs: ' + name)
        parent, expected = PARENTS[name]
        if not (root / parent).is_file() or digest(root / parent) != expected:
            raise ValueError('Measured physical runtime input missing or changed: ' + parent)
    result = dict(missingBefore=missing, steps=[], originalExecutableInputDerivationOnly=True,
        acceptedSourceCompilation=False, sourceCredit=0, passed=False)
    for index, name in enumerate(generators):
        log = root / 'logs/checks' / ('bootstrap-' + str(index) + '-' + name + '.txt')
        log.parent.mkdir(parents=True, exist_ok=True)
        command = [sys.executable, str(root / name)]
        started = time.monotonic()
        with log.open('w', encoding='utf-8') as stream:
            run = subprocess.run(command, cwd=root, stdout=stream, stderr=subprocess.STDOUT, timeout=600)
        result['steps'].append(dict(command=command, exitCode=run.returncode, log=log.relative_to(root).as_posix(),
            logSha256=digest(log), seconds=round(time.monotonic() - started, 3)))
        if run.returncode:
            raise ValueError('Native runtime input derivation failed: ' + name + '; log=' + str(log))
    for name in missing:
        if not (root / name).is_file() or digest(root / name) != pins[name]:
            raise ValueError('Derived runtime input differs from frozen accepted comparison hash: ' + name)
    result['passed'] = True
    return result
