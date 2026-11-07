import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261106_dwc_main_friend_next_first_v2_compiler import LANE


PRODUCER = 'wave20261106_dwc_main_friend_next_first_v2_match.py'
CANONICAL = 'evidence/matches/dwc-main-friend-next-first-v2-parallel-wave20261106.json'
INPUT = LANE / 'inputs.json'


def identity(row, rom):
    return dict(id=rom + '/arm9/main/thumb/' + format(int(row['address'], 0), '08x'),
        program='', processor='arm9', module='main', mode='thumb', address=row['address'], bytes=row['bytes'],
        source=row['source'], sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])


def prepare():
    preliminary = read_json(LANE / 'initial.json')['matches']
    derivation = read_json(LANE / 'derivation.json')
    if len(preliminary) != 8 or sum(row['bytes'] for row in preliminary) != 1484:
        raise ValueError('Initial friend membership differs')
    entries = []
    for row in preliminary:
        item = {key: row[key] for key in ['address', 'bytes', 'source', 'sourceSha256', 'sourceDependencies', 'targetSha256',
            'compilerPath', 'compilerSha256', 'compilerFlags', 'relocations', 'nativeSymbolEntries']}
        origin = next(value for value in derivation['entries'] if value['address'] == row['address'])
        item.update(sourceProvenance=origin, boundaryReturnContract='signed32-return' if int(row['address'], 0) in [0x209d168, 0x209d704] else 'void')
        entries.append(item)
    names = set(code_closure([PRODUCER]))
    previous = read_json(ROOT / 'evidence/lanes/parallel-wave20261105/main-record-next/third/inputs.json')
    names.update(pin['path'] for pin in previous['files'] if pin['path'].startswith(('deps/native/', 'tools/mwccarm/')))
    names.update(['project.json', 'tools.lock.json', 'provenance/seed-manifest.json', 'extract/arm9/arm9.bin', 'config/arm9/symbols.txt', 'config/arm9/relocs.txt'])
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['native-inputs.json', 'derivation.json', 'interface-limits.json', 'literal-spelling-equivalence.json'])
    for item in read_json(LANE / 'native-inputs.json')['files']:
        names.add(item['path'])
    names.add(read_json(LANE / 'native-inputs.json')['claim']['path'])
    names.add('evidence/lanes/parallel-wave20261106/dwc-main-friend-next/coordinator-admission.json')
    for item in entries:
        names.add(item['source'])
        names.update(pin['path'] for pin in item['sourceDependencies'])
        origin = item['sourceProvenance']['derivation']
        names.add(origin['primary'])
        names.update(pin['path'] for pin in origin['referencePins'])
    body = dict(schemaVersion=1, romSha256=configuration()['romSha256'], moduleSha256=sha256(ROOT / 'extract/arm9/arm9.bin'),
        ownershipOriginClaimSha256=read_json(LANE / 'native-inputs.json')['claim']['sha256'], entries=entries,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(names)],
        scope='Only eight selected complete ordinary-C friend callers; actual source/ABI inputs remain parsed. Experimental and historical inventories are separate zero-credit evidence.')
    if INPUT.exists() and read_json(INPUT) != body:
        raise ValueError('Already-frozen friend inputs changed')
    write_json(INPUT, body)
    print(dict(inputs=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT), files=len(names)))


def descriptor():
    inputs = read_json(INPUT)
    body = dict(schemaVersion=1, romSha256=inputs['romSha256'], producer=[PRODUCER],
        workerReport=(LANE / 'match.json').relative_to(ROOT).as_posix(), canonicalReport=CANONICAL,
        frozenInputs=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))],
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']])
    path = LANE / 'canonical.json'
    if path.exists() and read_json(path) != body:
        raise ValueError('Frozen friend descriptor changed')
    write_json(path, body)
    print(dict(descriptor=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))


def copied_root():
    clone = ROOT / 'work/w6mfrv2c1'
    if clone.exists():
        raise ValueError('Copied friend root must be initially empty')
    names = {pin['path'] for pin in read_json(INPUT)['files']}
    names.update(code_closure([PRODUCER, 'replay_parallel_packet.py']))
    names.update([INPUT.relative_to(ROOT).as_posix(), (LANE / 'canonical.json').relative_to(ROOT).as_posix()])
    for name in sorted(names):
        source, target = ROOT / name, clone / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        if sha256(source) != sha256(target):
            raise ValueError('Copied input differs')
    if (clone / 'work').exists() or (clone / CANONICAL).exists() or (clone / LANE.relative_to(ROOT) / 'match.json').exists():
        raise ValueError('Copied root contains cached game products')
    result = subprocess.run([sys.executable, str(clone / 'replay_parallel_packet.py'), (LANE / 'canonical.json').relative_to(ROOT).as_posix()],
        cwd=clone, capture_output=True, text=True, timeout=300)
    if result.returncode:
        write_json(LANE / 'copy-failure.json', dict(exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        raise ValueError('Fresh copied-root friend replay failed')
    report = read_json(clone / CANONICAL)
    objects = []
    for row in report['matches']:
        if sha256(clone / row['object']) != row['objectSha256'] or not Path(row['realLink']['linkerAttempt']['cwd']).is_relative_to(clone):
            raise ValueError('Canonical report did not publish fresh copied-root compiler/linker products')
        if row['ordinaryCBytes'] != row['bytes'] or row['justifiedAssemblyBytes']:
            raise ValueError('Copied ordinary-C partition differs')
        objects.append(dict(address=row['address'], object=row['object'], sha256=row['objectSha256']))
    if len(objects) != 8 or report['matchedBytes'] != 1484:
        raise ValueError('Copied canonical membership differs')
    write_json(LANE / 'copied-root.json', dict(allPassed=True, functions=8, bytes=1484,
        freshCanonicalObjectsVerified=True, noInitialWorkWorkerOrCanonicalProducts=True,
        allLinkerCwdsInsideCopiedRoot=True, immutableInputs=len(names), objects=objects,
        canonicalReportSha256=sha256(clone / CANONICAL), actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        suppliedCalleeSourceOrExecutionCredit=0, stdout=result.stdout, stderr=result.stderr))
    print(dict(copiedRootPassed=True, functions=8, bytes=1484))


def ready():
    inputs, report, copied = read_json(INPUT), read_json(LANE / 'match.json'), read_json(LANE / 'copied-root.json')
    if not report['allPassed'] or not copied['allPassed'] or report['matchedFunctions'] != 8 or report['matchedBytes'] != 1484 or copied['bytes'] != 1484:
        raise ValueError('Friend packet proof not complete')
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER, Path(__file__).name, 'replay_parallel_packet.py']))
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['inputs.json', 'canonical.json', 'copied-root.json'])
    files = [dict(path=name, sha256=sha256(ROOT / name), kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(path=(LANE / 'match.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'match.json'), kind='regenerated-worker-report'))
    body = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=170,
        romSha256=inputs['romSha256'], functions=8, bytes=1484, ordinaryCBytes=1484, justifiedAssemblyBytes=0,
        packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])],
        canonicalDescriptor=dict(path=(LANE / 'canonical.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'canonical.json')),
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']], files=files,
        actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        copiedRootFreshCanonicalReplayPassed=True, suppliedCalleeSourceOrExecutionCredit=0,
        sourceCreditPendingSharedAcceptance=True, diagnosticInventoriesAreNotRuntimeInputs=True, limits=report['limits'])
    path = LANE / 'ready.json'
    if path.exists() and read_json(path) != body:
        raise ValueError('Frozen friend Ready changed')
    write_json(path, body)
    print(dict(ready=path.relative_to(ROOT).as_posix(), sha256=sha256(path), functions=8, bytes=1484, files=len(files)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'descriptor', 'copied_root', 'ready'])
    globals()[parser.parse_args().action]()
