import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from project import ROOT, read_json, sha256, write_json
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261102/main-sdk-next'
PRODUCER = 'wave20261102_main_sdk_next_match.py'
CANONICAL = 'evidence/matches/main-sdk-next-parallel-wave20261102.json'


def identity(row, rom):
    return dict(id=rom + '/arm9/main/arm/' + format(int(row['address'], 0), '08x'), processor='arm9', program='', module='main', mode='arm', address=row['address'], bytes=row['bytes'], source=row['source'], sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])


def descriptor():
    inputs = read_json(LANE / 'inputs.json')
    body = dict(schemaVersion=1, romSha256=inputs['romSha256'], producer=[PRODUCER], workerReport=(LANE / 'match.json').relative_to(ROOT).as_posix(), canonicalReport=CANONICAL, frozenInputs=[dict(path=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'inputs.json'))], identities=[identity(row, inputs['romSha256']) for row in inputs['entries']])
    path = LANE / 'canonical-packet.json'
    if path.exists() and read_json(path) != body:
        raise ValueError('Immutable canonical SDK descriptor already differs')
    write_json(path, body)
    print(dict(descriptor=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))


def copy_file(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
    if sha256(source) != sha256(destination):
        raise ValueError('Copied-root input changed: ' + str(source))


def copied_root():
    clone = ROOT / 'work/parallel-wave20261102/main-sdk-next/copied-root'
    if clone.exists():
        raise ValueError('Copied-root replay target must start absent')
    clone.mkdir(parents=True)
    inputs = read_json(LANE / 'inputs.json')
    relative_descriptor = (LANE / 'canonical-packet.json').relative_to(ROOT).as_posix()
    names = set(code_closure([PRODUCER, 'replay_parallel_packet.py']))
    names.update([relative_descriptor, (LANE / 'inputs.json').relative_to(ROOT).as_posix(), 'extract/arm9/arm9.bin'])
    names.update(pin['path'] for pin in inputs['immutableNativeConfiguration'])
    for item in inputs['entries']:
        names.add(item['source'])
        names.update(pin['path'] for pin in item['sourceDependencies'])
    for name in sorted(names):
        copy_file(ROOT / name, clone / name)
    for path in sorted((ROOT / 'tools/mwccarm/mwccarm/2.0/base').glob('*')):
        if path.suffix.lower() in ['.exe', '.dll']:
            copy_file(path, clone / path.relative_to(ROOT))
    copy_file(ROOT / 'tools/mwccarm/mwccarm/license.dat', clone / 'tools/mwccarm/mwccarm/license.dat')
    shutil.copytree(ROOT / 'deps/native', clone / 'deps/native', ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
    if (clone / 'work').exists() or (clone / CANONICAL).exists() or (clone / 'evidence/lanes/parallel-wave20261102/main-sdk-next/match.json').exists():
        raise ValueError('Copied-root replay was contaminated by preexisting outputs')
    command = [sys.executable, str(clone / 'replay_parallel_packet.py'), relative_descriptor]
    process = subprocess.run(command, cwd=clone, capture_output=True, text=True, timeout=120)
    if process.returncode:
        write_json(LANE / 'copied-root-failure.json', dict(command=command, exitCode=process.returncode, stdout=process.stdout, stderr=process.stderr))
        raise ValueError('Copied-root SDK packet replay failed')
    report = read_json(clone / CANONICAL)
    objects = []
    for row in report['matches']:
        artifact = clone / row['object']
        link_cwd = Path(row['realLink']['linkerAttempt']['cwd'])
        if sha256(artifact) != row['objectSha256'] or not link_cwd.is_relative_to(clone):
            raise ValueError('Copied-root canonical objects/linker did not originate in copied root')
        objects.append(dict(address=row['address'], object=row['object'], objectSha256=row['objectSha256'], targetSha256=row['targetSha256']))
    proof = dict(schemaVersion=1, allPassed=True, clone=clone.relative_to(ROOT).as_posix(), command=[sys.executable, 'replay_parallel_packet.py', relative_descriptor], startedWithNoWorkProductsOrWorkerOrCanonicalReport=True, originalWorkAndReferenceSdkNotCopied=True, copiedAuthoredInputs=len(names), functions=len(objects), bytes=sum(row['bytes'] for row in report['matches']), canonicalReportFreshObjectsVerified=True, everyLinkerWorkingDirectoryInsideCopiedRoot=True, negativeControlsRejected=len(report['negativeEvidence']), nativeTypedLayoutChecks=sum(row['compilerChecks'] for row in report['typedLayoutChecks']), actualNativeFunctionReturns=0, objects=objects, stdout=process.stdout, stderr=process.stderr, copiedCanonicalReportSha256=sha256(clone / CANONICAL), sourceCreditPendingCoordinator=True)
    write_json(LANE / 'copied-root-replay.json', proof)
    print(dict(copiedRootPassed=True, functions=len(objects), bytes=proof['bytes'], canonicalObjectsFresh=True))


def ready():
    report = read_json(LANE / 'match.json')
    inputs = read_json(LANE / 'inputs.json')
    clone = read_json(LANE / 'copied-root-replay.json')
    if not report['allPassed'] or not clone['allPassed'] or clone['bytes'] != report['matchedBytes']:
        raise ValueError('SDK packet or copied-root proof incomplete')
    names = set(code_closure([PRODUCER, Path(__file__).name, 'replay_parallel_packet.py', 'wave20261102_main_sdk_next_discover.py']))
    names.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'src/runtime/parallel_wave20261102/main-sdk-next').rglob('*') if path.is_file())
    names.update(path.relative_to(ROOT).as_posix() for path in LANE.glob('*') if path.is_file() and path.name not in ['claim.json', 'ready.json', 'match.json'])
    body = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=146, functions=report['matchedFunctions'], bytes=report['matchedBytes'], sourceCreditPendingIntegrator=report['matchedBytes'], romSha256=report['romSha256'], packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])], canonicalDescriptor=dict(path=(LANE / 'canonical-packet.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'canonical-packet.json')), canonicalReplayCommand=['replay_parallel_packet.py', (LANE / 'canonical-packet.json').relative_to(ROOT).as_posix()], identities=[identity(row, report['romSha256']) for row in inputs['entries']], files=[dict(path=name, sha256=sha256(ROOT / name), kind='frozen-source-or-evidence') for name in sorted(names)], actualNativeFunctionReturns=0, typedNativeCompilerLayoutChecks=sum(row['compilerChecks'] for row in report['typedLayoutChecks']), wholeCNegativeControlsRejected=len(report['negativeEvidence']), copiedRootCanonicalReplayPassed=True, limits=report['limits'] + ['Five remaining claimed units (4,056 bytes) remain uncredited; final negative C/header contexts and diagnostic histories are retained. Earlier invalid closure reports are diagnostic records, not frozen-source replay claims.', 'The mutable lane claim is not a replay dependency. Existing accepted source, global registries, source-map, ROM inputs and compiler tools remain unchanged.'])
    path = LANE / 'ready.json'
    if path.exists() and read_json(path) != body:
        raise ValueError('Immutable ready SDK packet already differs')
    write_json(path, body)
    print(dict(ready=path.relative_to(ROOT).as_posix(), sha256=sha256(path), files=len(names), functions=body['functions'], bytes=body['bytes']))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['descriptor', 'copied_root', 'ready'])
    globals()[parser.parse_args().action]()
