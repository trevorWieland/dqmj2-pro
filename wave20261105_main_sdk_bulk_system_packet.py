import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-sdk-bulk/system/packet'
INPUT = LANE / 'inputs.json'
PRODUCER = 'wave20261105_main_sdk_bulk_system_match.py'
CANONICAL = 'evidence/matches/main-sdk-bulk-system-parallel-wave20261105.json'


def identity(row, rom):
    return dict(id=rom + '/arm9/main/arm/' + format(int(row['address'], 0), '08x'), program='', processor='arm9', module='main', mode='arm',
        address=row['address'], bytes=row['bytes'], source=row['source'], sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])


def prepare():
    closed = read_json(LANE.parent / 'materialized-v2.json')['closed'][0]
    row = closed['entry']
    from recover_linked_runtime import qualified_bindings
    item = {key: row[key] for key in ['address', 'bytes', 'source', 'sourceSha256', 'sourceDependencies', 'targetSha256', 'compilerPath', 'compilerSha256']}
    item.update(flags=row['compilerFlags'], priorRelocations=row['relocations'], referenceFunction='WmReceiveFifo', qualifiedDependencies=qualified_bindings(row),
        provenance=closed['provenance'], extraLayoutChecks=read_json(LANE.parent / 'layout.json')['checks'])
    names = set(code_closure([PRODUCER]))
    prior = read_json(LANE.parents[1] / 'first/inputs.json')
    names.update(pin['path'] for pin in prior['files'] if pin['path'].startswith(('deps/native/', 'tools/mwccarm/')))
    names.update(['project.json', 'tools.lock.json', 'provenance/seed-manifest.json', 'extract/arm9/arm9.bin', 'config/arm9/symbols.txt', 'config/arm9/relocs.txt'])
    names.add(item['source'])
    names.update(pin['path'] for pin in item['sourceDependencies'])
    names.add(item['provenance']['referenceSource'])
    body = dict(schemaVersion=1, romSha256=configuration()['romSha256'], moduleSha256=closed['identity']['inputModuleSha256'], entries=[item],
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(names)],
        scope='One complete ordinary C SDK FIFO dispatcher; all exploratory whole-TU snapshots and other SDK functions receive zero source credit and are not runtime inputs.')
    if INPUT.exists():
        assert read_json(INPUT) == body
    write_json(INPUT, body)
    print(dict(inputs=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT), files=len(names)))


def descriptor():
    inputs = read_json(INPUT)
    body = dict(schemaVersion=1, romSha256=inputs['romSha256'], producer=[PRODUCER], workerReport=(LANE / 'match.json').relative_to(ROOT).as_posix(),
        canonicalReport=CANONICAL, frozenInputs=[dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=sha256(INPUT))], identities=[identity(row, inputs['romSha256']) for row in inputs['entries']])
    path = LANE / 'canonical.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path, body)
    print(dict(descriptor=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))


def copied_root():
    clone = ROOT / 'work/w5sbsc1'
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
    assert not (clone / 'work').exists() and not (clone / CANONICAL).exists() and not (clone / LANE.relative_to(ROOT) / 'match.json').exists()
    result = subprocess.run([sys.executable, str(clone / 'replay_parallel_packet.py'), descriptor_name], cwd=clone, capture_output=True, text=True, timeout=300)
    if result.returncode:
        write_json(LANE / 'copy-failure.json', dict(exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        raise ValueError('Copied-root SDK bulk proof failed')
    report = read_json(clone / CANONICAL)
    objects = []
    for row in report['matches']:
        assert sha256(clone / row['object']) == row['objectSha256']
        assert Path(row['realLink']['linkerAttempt']['cwd']).is_relative_to(clone)
        assert row['ordinaryCBytes'] + row['justifiedAssemblyBytes'] == row['bytes']
        objects.append(dict(address=row['address'], object=row['object'], sha256=row['objectSha256']))
    write_json(LANE / 'copied-root.json', dict(allPassed=True, functions=len(objects), bytes=940, freshCanonicalObjectsVerified=True,
        noInitialWorkWorkerOrCanonicalOutputs=True, allLinkerCwdsInsideCopiedRoot=True, immutableInputs=len(names), objects=objects,
        canonicalReportSha256=sha256(clone / CANONICAL), actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        suppliedCalleeSourceOrExecutionCredit=0, stdout=result.stdout, stderr=result.stderr))
    print(dict(copiedRootPassed=True, functions=len(objects), bytes=940))


def ready():
    report, copied, inputs = read_json(LANE / 'match.json'), read_json(LANE / 'copied-root.json'), read_json(INPUT)
    assert report['allPassed'] and copied['allPassed'] and report['matchedBytes'] == copied['bytes'] == 940
    assert sum(row['ordinaryCBytes'] for row in report['matches']) == 940 and sum(row['justifiedAssemblyBytes'] for row in report['matches']) == 0
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER, Path(__file__).name, 'replay_parallel_packet.py']))
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['inputs.json', 'canonical.json', 'copied-root.json'])
    files = [dict(path=name, sha256=sha256(ROOT / name), kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(path=(LANE / 'match.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'match.json'), kind='regenerated-worker-report'))
    body = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=154, romSha256=inputs['romSha256'], functions=1, bytes=940,
        ordinaryCBytes=940, justifiedAssemblyBytes=0, packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])],
        canonicalDescriptor=dict(path=(LANE / 'canonical.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'canonical.json')),
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']], files=files, actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        primitiveProbeSourceCredit=0, suppliedCalleeSourceOrExecutionCredit=0, copiedRootFreshCanonicalReplayPassed=True, diagnosticInventoriesAreNotRuntimeInputs=True,
        sourceClassification='Ordinary C SDK FIFO dispatcher with original typed common-static storage and callee imports', sourceCreditPendingSharedAcceptance=True, limits=report['limits'])
    path = LANE / 'ready.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path, body)
    print(dict(ready=path.relative_to(ROOT).as_posix(), sha256=sha256(path), functions=1, bytes=940, files=len(files)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'descriptor', 'copied_root', 'ready'])
    globals()[parser.parse_args().action]()
