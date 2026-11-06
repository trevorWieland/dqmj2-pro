import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-sdk-prefix/first'
INPUT = LANE / 'inputs.json'
PRODUCER = 'wave20261104_main_sdk_prefix_match.py'
CANONICAL = 'evidence/matches/main-sdk-prefix-first-parallel-wave20261104.json'


def identity(row, rom):
    return dict(id=rom + '/arm9/main/arm/' + format(int(row['address'], 0), '08x'), program='', processor='arm9',
        module='main', mode='arm', address=row['address'], bytes=row['bytes'], source=row['source'],
        sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])


def descriptor():
    inputs = read_json(INPUT)
    body = dict(schemaVersion=1, romSha256=inputs['romSha256'], producer=[PRODUCER],
        workerReport=(LANE / 'match.json').relative_to(ROOT).as_posix(), canonicalReport=CANONICAL,
        frozenInputs=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))],
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']])
    path = LANE / 'canonical.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path, body)
    print(dict(descriptor=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))


def copied_root():
    clone = ROOT / 'work/w4spc2'
    assert not clone.exists(), 'Use a new copied-root directory'
    inputs = read_json(INPUT)
    descriptor_name = (LANE / 'canonical.json').relative_to(ROOT).as_posix()
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER, 'replay_parallel_packet.py']))
    names.update([INPUT.relative_to(ROOT).as_posix(), descriptor_name])
    for name in sorted(names):
        source, target = ROOT / name, clone / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha256(source) == sha256(target)
    shutil.copytree(ROOT / 'deps/native', clone / 'deps/native', dirs_exist_ok=True,
        ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    assert not (clone / 'work').exists() and not (clone / CANONICAL).exists()
    assert not (clone / LANE.relative_to(ROOT) / 'match.json').exists()
    command = [sys.executable, str(clone / 'replay_parallel_packet.py'), descriptor_name]
    result = subprocess.run(command, cwd=clone, capture_output=True, text=True, timeout=300)
    if result.returncode:
        write_json(LANE / 'copy-failure.json', dict(command=command, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        raise ValueError('Copied-root SDK prefix proof failed')
    report = read_json(clone / CANONICAL)
    objects = []
    for row in report['matches']:
        assert sha256(clone / row['object']) == row['objectSha256']
        assert Path(row['realLink']['linkerAttempt']['cwd']).is_relative_to(clone)
        assert row['ordinaryCBytes'] + row['justifiedAssemblyBytes'] == row['bytes']
        objects.append(dict(address=row['address'], object=row['object'], sha256=row['objectSha256']))
    write_json(LANE / 'copied-root.json', dict(allPassed=True, functions=len(objects), bytes=sum(row['bytes'] for row in report['matches']),
        freshCanonicalObjectsVerified=True, noInitialWorkWorkerOrCanonicalOutputs=True, allLinkerCwdsInsideCopiedRoot=True,
        originalWorkReferenceSdkAndExplorationInventoriesNotCopied=True, immutableInputs=len(names), objects=objects,
        canonicalReportSha256=sha256(clone / CANONICAL), command=[sys.executable, 'replay_parallel_packet.py', descriptor_name],
        callerExecutionCredit=0, primitiveSourceCredit=0, stdout=result.stdout, stderr=result.stderr))
    print(dict(copiedRootPassed=True, functions=len(objects), bytes=2252))


def ready():
    report = read_json(LANE / 'match.json')
    copied = read_json(LANE / 'copied-root.json')
    inputs = read_json(INPUT)
    assert report['allPassed'] and copied['allPassed'] and report['matchedBytes'] == copied['bytes'] == 2252
    assert sum(row['ordinaryCBytes'] for row in report['matches']) == 2252
    assert sum(row['justifiedAssemblyBytes'] for row in report['matches']) == 0
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER, Path(__file__).name, 'replay_parallel_packet.py']))
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['inputs.json', 'canonical.json', 'copied-root.json'])
    files = [dict(path=name, sha256=sha256(ROOT / name), kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(path=(LANE / 'match.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'match.json'), kind='regenerated-worker-report'))
    body = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=152,
        romSha256=inputs['romSha256'], functions=29, bytes=2252, ordinaryCBytes=2252, justifiedAssemblyBytes=0,
        packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])],
        canonicalDescriptor=dict(path=(LANE / 'canonical.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'canonical.json')),
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']], files=files,
        actualNativeCallerReturns=0, primitiveProbeSourceCredit=0, suppliedCalleeSourceCredit=0,
        sourceClassification='ordinary C with separately qualified aligned extern storage',
        copiedRootFreshCanonicalReplayPassed=True, diagnosticInventoriesAreNotRuntimeInputs=True,
        sourceCreditPendingSharedAcceptance=True, limits=report['limits'])
    output = LANE / 'ready.json'
    if output.exists():
        assert read_json(output) == body
    write_json(output, body)
    print(dict(ready=output.relative_to(ROOT).as_posix(), sha256=sha256(output), functions=29, bytes=2252, files=len(files)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['descriptor', 'copied_root', 'ready'])
    globals()[parser.parse_args().action]()
