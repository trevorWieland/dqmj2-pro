import os
import runpy
import sys
import time
from pathlib import Path
import project
import ledger_state
import install_tools
import run_checks
import verify_workspace
from project import ROOT, read_json, write_json, sha256


ACTIVE = None
PHASES = []
HITS = 0
WORK = ROOT / 'work/evidence-phase-cache-20261031'
PIN = ROOT / 'provenance/evidence-phase-cache-framework-20261031.json'


def cached_hash(path):
    global HITS
    if ACTIVE is None:
        return sha256(path)
    key = Path(path).resolve()
    if key not in ACTIVE:
        ACTIVE[key] = sha256(key)
    else:
        HITS += 1
    return ACTIVE[key]


def finish_phase(snapshot):
    for path, expected in snapshot.items():
        if sha256(path) != expected:
            raise ValueError('File changed during snapshot: ' + str(path))


def self_test():
    global ACTIVE
    fixture = WORK / 'self-test.bin'
    fixture.parent.mkdir(parents=True, exist_ok=True)
    rejected = []
    for label in ['content-change', 'same-size-restored-timestamp', 'removed-file']:
        fixture.write_bytes(bytes([1]) * 64)
        previous = fixture.stat()
        ACTIVE = {}
        assert cached_hash(fixture) == sha256(fixture)
        assert cached_hash(fixture) == sha256(fixture)
        if label == 'removed-file':
            fixture.unlink()
        else:
            fixture.write_bytes(bytes([2]) * 64)
            if label == 'same-size-restored-timestamp':
                os.utime(fixture, ns=(previous.st_atime_ns, previous.st_mtime_ns))
        try:
            finish_phase(ACTIVE)
        except (ValueError, FileNotFoundError):
            rejected.append(label)
        else:
            raise ValueError('Cache accepted a changed snapshot')
        ACTIVE = None
    assert len(rejected) == 3
    return rejected


def main():
    global ACTIVE
    pins = read_json(PIN)
    assert all(sha256(ROOT / name) == digest for name, digest in pins['frameworkHashes'].items())
    registry_hash = sha256(ROOT / 'recovery.json')
    baseline = read_json(ROOT / 'evidence/verification/evidence-freshness.json')
    assert baseline['passed']
    rejected = self_test()
    original_build = ledger_state.build_state

    def bounded_build(*arguments, **options):
        global ACTIVE
        assert ACTIVE is None
        ACTIVE = {}
        started, hits_before = time.perf_counter(), HITS
        try:
            result = original_build(*arguments, **options)
            finish_phase(ACTIVE)
            PHASES.append(dict(uniqueFilesHashedTwice=len(ACTIVE), repeatedHashReadsAvoided=HITS - hits_before,
                elapsedSeconds=time.perf_counter() - started, startAndEndContentDigestsAgree=True))
            return result
        finally:
            ACTIVE = None

    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename and Path(filename).resolve().is_relative_to(ROOT) and module is not sys.modules[__name__]:
            for name, value in list(vars(module).items()):
                if value is sha256:
                    setattr(module, name, cached_hash)
    ledger_state.build_state = bounded_build
    original_write = project.write_json
    target = ROOT / 'evidence/verification/evidence-freshness.json'
    redirected = WORK / 'evidence-freshness.json'

    def redirected_write(path, value):
        return original_write(redirected if Path(path).resolve() == target else path, value)

    project.write_json = redirected_write
    started = time.perf_counter()
    runpy.run_path(str(ROOT / 'validate_evidence.py'), run_name='__main__')
    actual = read_json(redirected)
    assert actual['passed'] and actual['negativeAcceptanceCases'] == baseline['negativeAcceptanceCases']
    assert actual['restoredSourceFunctions'] == baseline['restoredSourceFunctions']
    assert sha256(ROOT / 'recovery.json') == registry_hash
    assert all(sha256(ROOT / name) == digest for name, digest in pins['frameworkHashes'].items())
    assert PHASES and all(phase['uniqueFilesHashedTwice'] > 0 for phase in PHASES)
    write_json(ROOT / 'evidence/verification/evidence-phase-cache-20261031.json', dict(
        frameworkPins=pins, frameworkPinSha256=sha256(PIN), sourceRegistrySha256=registry_hash,
        sourceCredit=0, passed=True, elapsedSeconds=time.perf_counter() - started, phases=PHASES,
        cacheControlsRejected=rejected, negativeAcceptanceCases=actual['negativeAcceptanceCases'],
        restoredSourceFunctions=actual['restoredSourceFunctions'], frozenFrameworkFilesUnchanged=True,
        originalFreshnessReportUnchanged=read_json(target) == baseline,
        limitations=['Cache is scoped to each synchronous ledger-state evaluation; every distinct input is hashed on first use and again before returning',
            'This benchmarks the unchanged acceptance program; no test is skipped and no current controller is replaced',
            'This is neither source coverage nor a fresh full source build']))
    print(dict(cachedPhases=len(PHASES), elapsedSeconds=time.perf_counter() - started, passed=True))


if __name__ == '__main__':
    main()
