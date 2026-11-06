import copy
import hashlib
import json
from pathlib import Path
import subprocess
from clean_reference_policy_parallel_wave20261102 import reference_pins, committed_reference_pins, validate_source_paths, verify_reference_copy, REFERENCE_NAMES
from project import ROOT, sha256, write_json


def main():
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    pins = committed_reference_pins(ROOT, revision)
    paths = [Path(name) for name in subprocess.run(['git', 'ls-tree', '-r', '--name-only', revision],
        cwd=ROOT, check=True, capture_output=True, text=True).stdout.splitlines()]
    validate_source_paths(paths, pins)
    controls = []

    def reject(name, operation):
        try:
            operation()
        except ValueError as error:
            controls.append(dict(name=name, rejected=True, reason=str(error)))
        else:
            raise AssertionError('Invalid snapshot was accepted: ' + name)

    for name in ['deps/undeclared-reference.c', 'deps/native/unicorn/lib/unicorn.dll', 'inputs/game.nds',
                 'extract/arm7/arm7.bin', 'work/cached.o', 'build/game.nds', '../outside.c', str(ROOT / 'outside.c')]:
        reject('unapproved-' + name, lambda name=name: validate_source_paths([Path(name)], pins))
    blobs = {}
    for name in [*pins, *['provenance/msl-' + name + '-reference-20261031.json' for name in REFERENCE_NAMES]]:
        blobs[name] = subprocess.run(['git', 'show', revision + ':' + name], cwd=ROOT, check=True, capture_output=True).stdout
    manifest = 'provenance/msl-ansi-reference-20261031.json'
    first = next(iter(pins))
    changed = dict(blobs)
    changed[first] += b'changed'
    reject('changed-committed-reference', lambda: reference_pins(changed.__getitem__))
    document = json.loads(blobs[manifest])
    for name, change in [('wrong-upstream-revision', {'revision': '0' * 40}),
                         ('nonzero-source-credit', {'sourceCredit': 1})]:
        mutated = copy.deepcopy(document)
        mutated.update(change)
        values = dict(blobs)
        values[manifest] = json.dumps(mutated).encode()
        reject(name, lambda values=values: reference_pins(values.__getitem__))
    for name, change in [('executable-reference', {'path': 'deps/msl-ansi-reference-20261031/cache.o'}),
                         ('escaping-reference', {'path': '../outside.c'}),
                         ('wrong-reference-hash', {'sha256': '0' * 64})]:
        mutated = copy.deepcopy(document)
        mutated['files'][0].update(change)
        values = dict(blobs)
        values[manifest] = json.dumps(mutated).encode()
        reject(name, lambda values=values: reference_pins(values.__getitem__))
    work = ROOT / 'work/clean-reference-policy-parallel-wave20261102'
    work.mkdir(parents=True, exist_ok=True)
    source, target = work / 'source.c', work / 'committed.c'
    source.write_bytes(blobs[first])
    target.write_bytes(blobs[first])
    assert verify_reference_copy(Path(first), source, target, pins)
    source.write_bytes(b'changed working dependency')
    reject('working-dependency-cannot-overwrite-commit', lambda: verify_reference_copy(Path(first), source, target, pins))
    source.write_bytes(blobs[first])
    target.write_bytes(b'changed committed dependency')
    reject('changed-extracted-reference', lambda: verify_reference_copy(Path(first), source, target, pins))
    receipt = dict(passed=True, controls=controls, sourceRevision=revision, committedSourcePathsChecked=len(paths),
        committedReferenceFiles=pins, committedReferenceFilesChecked=len(pins), sourceCredit=0,
        acceptedInputsChanged=False, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        policySha256=sha256(ROOT / 'clean_reference_policy_parallel_wave20261102.py'),
        cleanReplayDriverSha256=sha256(ROOT / 'validate_clean_checkout.py'))
    destination = ROOT / 'evidence/verification/parallel-wave20261102/clean-reference-policy.json'
    write_json(destination, receipt)
    print(dict(passed=True, controls=len(controls), referenceFiles=len(pins), committedPaths=len(paths)))


if __name__ == '__main__':
    main()
