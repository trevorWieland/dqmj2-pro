import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-sdk-bulk/first'
INPUT = LANE / 'inputs.json'
PRODUCER = 'wave20261105_main_sdk_bulk_match.py'
CANONICAL = 'evidence/matches/main-sdk-bulk-first-parallel-wave20261105.json'


def identity(row, rom):
    return dict(id=rom + '/arm9/main/arm/' + format(int(row['address'], 0), '08x'), program='', processor='arm9', module='main', mode='arm',
        address=row['address'], bytes=row['bytes'], source=row['source'], sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])


def prepare():
    discovery = read_json(LANE.parent / 'discovery.json')
    entries = []
    names = set(code_closure([PRODUCER]))
    names.update(['project.json', 'tools.lock.json', 'provenance/seed-manifest.json', 'extract/arm9/arm9.bin', 'config/arm9/symbols.txt', 'config/arm9/relocs.txt', 'tools/mwccarm/mwccarm/license.dat'])
    for path in (ROOT / 'deps/native').rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            names.add(path.relative_to(ROOT).as_posix())
    for version in ['base', 'sp1p5']:
        folder = ROOT / 'tools/mwccarm/mwccarm/2.0' / version
        names.update(path.relative_to(ROOT).as_posix() for path in folder.iterdir() if path.suffix.lower() in ['.exe', '.dll'])
    for closed in sorted(discovery['closed'], key=lambda result: int(result['entry']['address'], 0)):
        row = closed['entry']
        item = {key: row[key] for key in ['address', 'bytes', 'source', 'sourceSha256', 'sourceDependencies', 'targetSha256', 'compilerPath', 'compilerSha256']}
        item.update(flags=row['compilerFlags'], priorRelocations=row['relocations'], referenceFunction=closed['row']['referenceFunction'],
            qualifiedDependencies=closed['realLink']['bindings'] if 'bindings' in closed['realLink'] else {}, provenance=closed['provenance'], extraLayoutChecks=[])
        from recover_linked_runtime import qualified_bindings
        item['qualifiedDependencies'] = qualified_bindings(row)
        address = int(row['address'], 0)
        if address == 0x02012464:
            item['extraLayoutChecks'] = [dict(type='WMBssDesc', bytes=192), dict(type='WMBssDesc', member='gameInfoLength', offset=60),
                dict(type='WMBssDesc', member='otherElementCount', offset=62), dict(type='WMBssDesc', member='gameInfo', offset=64),
                dict(type='WMOtherElements', bytes=132), dict(type='WMOtherElements', member='element[0].body', offset=8), dict(type='WMOtherElements', member='element[15].body', offset=128)]
        elif address == 0x020121AC:
            item['extraLayoutChecks'] = [dict(type='WMMpRecvData', bytes=12), dict(type='WMMpRecvData', member='aid', offset=4),
                dict(type='WMMpRecvHeader', bytes=22), dict(type='WMMpRecvHeader', member='count', offset=4), dict(type='WMMpRecvHeader', member='length', offset=6), dict(type='WMMpRecvHeader', member='data', offset=10)]
        elif address == 0x020125BC:
            item['extraLayoutChecks'] = [dict(type='RTCTime', bytes=12), dict(type='RTCTime', member='minute', offset=4), dict(type='RTCTime', member='second', offset=8)]
        names.add(item['source'])
        names.update(pin['path'] for pin in item['sourceDependencies'])
        names.add(item['provenance']['referenceSource'])
        entries.append(item)
    assert len(entries) == 11 and sum(item['bytes'] for item in entries) == 2344
    body = dict(schemaVersion=1, romSha256=configuration()['romSha256'], moduleSha256=discovery['closed'][0]['identity']['inputModuleSha256'],
        reservationClaimSha256='3f01f7750e336d6b8c83553c67d675d279cf1c6f6fc368d55b355d685c852472', entries=entries,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(names)],
        scope='Eleven independently linked ordinary C WM/MB caller units; comparative inventories and unselected source drafts are not runtime inputs.')
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
    clone = ROOT / 'work/w5sbc1'
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
    write_json(LANE / 'copied-root.json', dict(allPassed=True, functions=len(objects), bytes=2344, freshCanonicalObjectsVerified=True,
        noInitialWorkWorkerOrCanonicalOutputs=True, allLinkerCwdsInsideCopiedRoot=True, immutableInputs=len(names), objects=objects,
        canonicalReportSha256=sha256(clone / CANONICAL), actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        suppliedCalleeSourceOrExecutionCredit=0, stdout=result.stdout, stderr=result.stderr))
    print(dict(copiedRootPassed=True, functions=len(objects), bytes=2344))


def ready():
    report, copied, inputs = read_json(LANE / 'match.json'), read_json(LANE / 'copied-root.json'), read_json(INPUT)
    assert report['allPassed'] and copied['allPassed'] and report['matchedBytes'] == copied['bytes'] == 2344
    assert sum(row['ordinaryCBytes'] for row in report['matches']) == 2344 and sum(row['justifiedAssemblyBytes'] for row in report['matches']) == 0
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER, Path(__file__).name, 'replay_parallel_packet.py']))
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['inputs.json', 'canonical.json', 'copied-root.json'])
    files = [dict(path=name, sha256=sha256(ROOT / name), kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(path=(LANE / 'match.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'match.json'), kind='regenerated-worker-report'))
    body = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=154, romSha256=inputs['romSha256'], functions=11, bytes=2344,
        ordinaryCBytes=2344, justifiedAssemblyBytes=0, packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])],
        canonicalDescriptor=dict(path=(LANE / 'canonical.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'canonical.json')),
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']], files=files, actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        primitiveProbeSourceCredit=0, suppliedCalleeSourceOrExecutionCredit=0, copiedRootFreshCanonicalReplayPassed=True, diagnosticInventoriesAreNotRuntimeInputs=True,
        sourceClassification='Ordinary C with original typed data/function imports and zero-credit compiler helper binding', sourceCreditPendingSharedAcceptance=True, limits=report['limits'])
    path = LANE / 'ready.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path, body)
    print(dict(ready=path.relative_to(ROOT).as_posix(), sha256=sha256(path), functions=11, bytes=2344, files=len(files)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'descriptor', 'copied_root', 'ready'])
    globals()[parser.parse_args().action]()
