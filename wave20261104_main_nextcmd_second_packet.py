import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from wave20261104_main_nextcmd_second_fixture import GAME_CALLS

LANE = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-next/second'
SOURCE = 'src/runtime/parallel_wave20261104/main-command-next/second/'
PRODUCER = 'wave20261104_main_nextcmd_second_proof.py'
CANONICAL = 'evidence/matches/main-command-next-second-parallel-wave20261104.json'


def pin(name):
    return dict(path=name, sha256=sha256(ROOT / name))


def prepare():
    assert not (LANE / 'ready.json').exists(), 'READY packet is frozen'
    claim = read_json(LANE.parent / 'claim.json')
    entries = []
    for item in claim['claimedFunctions']:
        name = format(int(item['address'], 0), '08x')
        if name in GAME_CALLS:
            entries.append(dict(item, source=SOURCE + name + '.c', sourceSha256=sha256(ROOT / (SOURCE + name + '.c'))))
    assert len(entries) == len(GAME_CALLS) == 13 and sum(item['bytes'] for item in entries) == 3424
    names = set(code_closure([PRODUCER])) | {item['source'] for item in entries}
    names.update([SOURCE + 'context.h', 'src/runtime/parallel_wave20261104/main-runtime-tail/context.h'])
    mandatory = ['project.json', 'provenance/seed-manifest.json', 'config/arm9/symbols.txt', 'config/arm9/relocs.txt',
        'config/arm9/overlays/ov000/symbols.txt']
    names.update(mandatory)
    names.update(['extract/arm9/arm9.bin', 'extract/arm9_overlays/ov000.bin', 'tools/mwccarm/mwccarm/license.dat'])
    for profile, executable in [('2.0/base', 'mwldarm.exe'), ('2.0/sp1p5', 'mwccarm.exe')]:
        names.update('tools/mwccarm/mwccarm/' + profile + '/' + name for name in
            [executable, 'ELFIO.dll', 'lmgr8c.dll', 'MSL_All-DLL80_x86.dll'])
    names.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'deps/native').rglob('*')
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc')
    write_json(LANE / 'inputs.json', dict(schemaVersion=1, romSha256=claim['claimedFunctions'][0]['id'].split('/')[0],
        entries=entries, files=[pin(name) for name in sorted(names)], mandatoryExternalInputs=[pin(name) for name in mandatory],
        ownershipClaimSha256=sha256(LANE.parent / 'claim.json'), oldMeasuredContextSha256=sha256(ROOT / 'src/runtime/parallel_wave20261104/main-runtime-tail/context.h'),
        noNativeCalleeOrScaffoldingCredit=True, limits=['Only thirteen selected ordinary-C callers; other claim rows and exploration diagnostics are outside runtime dependencies.']))
    print(dict(inputs=(LANE / 'inputs.json').relative_to(ROOT).as_posix(), functions=13, bytes=3424, files=len(names)))


def identity(row, rom):
    return dict(id=rom + '/arm9/main/arm/' + format(int(row['address'], 0), '08x'), program='', processor='arm9',
        module='main', mode='arm', address=row['address'], bytes=row['bytes'], source=row['source'],
        sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])


def descriptor():
    inputs = read_json(LANE / 'inputs.json')
    body = dict(schemaVersion=1, romSha256=inputs['romSha256'], producer=[PRODUCER],
        workerReport=(LANE / 'match.json').relative_to(ROOT).as_posix(), canonicalReport=CANONICAL,
        frozenInputs=[pin((LANE / 'inputs.json').relative_to(ROOT).as_posix())] + inputs['mandatoryExternalInputs'],
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']])
    output = LANE / 'canonical.json'
    if (LANE / 'ready.json').exists():
        assert read_json(output) == body
    write_json(output, body)
    print(dict(descriptor=output.relative_to(ROOT).as_posix(), sha256=sha256(output)))


def copied_root():
    clone = ROOT / 'work/w4ncsc1'
    assert not clone.exists(), 'Use a fresh short copied-root directory'
    inputs = read_json(LANE / 'inputs.json')
    descriptor_name = (LANE / 'canonical.json').relative_to(ROOT).as_posix()
    names = {item['path'] for item in inputs['files']}
    names.update(code_closure([PRODUCER, 'replay_parallel_packet.py']))
    names.update([(LANE / 'inputs.json').relative_to(ROOT).as_posix(), descriptor_name])
    for name in sorted(names):
        source, target = ROOT / name, clone / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha256(source) == sha256(target)
    assert not (clone / 'work').exists() and not (clone / CANONICAL).exists() and not (clone / LANE.relative_to(ROOT) / 'match.json').exists()
    command = [sys.executable, str(clone / 'replay_parallel_packet.py'), descriptor_name]
    result = subprocess.run(command, cwd=clone, capture_output=True, text=True, timeout=300)
    if result.returncode:
        write_json(LANE / 'copy-failure.json', dict(command=command, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        raise ValueError('Copied-root command handler proof failed')
    report = read_json(clone / CANONICAL)
    objects = []
    for row in report['matches']:
        assert sha256(clone / row['object']) == row['objectSha256']
        assert Path(row['realLink']['linkerAttempt']['cwd']).is_relative_to(clone)
        assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
        objects.append(dict(address=row['address'], object=row['object'], sha256=row['objectSha256']))
    write_json(LANE / 'copied-root.json', dict(allPassed=True, functions=len(objects), bytes=sum(row['bytes'] for row in report['matches']),
        freshCanonicalObjectsVerified=True, noInitialWorkWorkerOrCanonicalOutputs=True, allLinkerCwdsInsideCopiedRoot=True,
        originalWorkAndDiagnosticInventoriesNotCopied=True, immutableInputs=len(names), objects=objects,
        traceSha256=report['generatedTrace']['uncompressedSha256'], canonicalReportSha256=sha256(clone / CANONICAL),
        command=[sys.executable, 'replay_parallel_packet.py', descriptor_name], sourceOrCalleeCredit=0,
        actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'], stdout=result.stdout, stderr=result.stderr))
    print(dict(copiedRootPassed=True, functions=len(objects), bytes=3424))


def ready():
    report = read_json(LANE / 'match.json')
    copied = read_json(LANE / 'copied-root.json')
    inputs = read_json(LANE / 'inputs.json')
    assert report['allPassed'] and copied['allPassed'] and report['canonicalMatchedBytes'] == copied['bytes'] == 3424
    assert report['generatedTrace']['uncompressedSha256'] == copied['traceSha256']
    names = {item['path'] for item in inputs['files']}
    names.update(code_closure([PRODUCER, Path(__file__).name, 'replay_parallel_packet.py']))
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['inputs.json', 'canonical.json', 'copied-root.json', 'binding-layout-controls.json', 'traces.json.gz'])
    files = [dict(**pin(name), kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(**pin((LANE / 'match.json').relative_to(ROOT).as_posix()), kind='regenerated-worker-report'))
    body = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=150,
        romSha256=inputs['romSha256'], functions=13, bytes=3424, ordinaryCBytes=3424, justifiedAssemblyBytes=0,
        packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])],
        canonicalDescriptor=pin((LANE / 'canonical.json').relative_to(ROOT).as_posix()),
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']], files=files,
        boundedCallerCases=104, actualNativeAndSourceCallerReturns=208, suppliedNativeCalleeBodiesExecuted=0,
        suppliedCalleeOrScaffoldingSourceCredit=0, sourceClassification='ordinary C', copiedRootFreshCanonicalReplayPassed=True,
        sourceCreditPendingSharedAcceptance=True, diagnosticInventoriesAreNotRuntimeInputs=True, limits=report['limits'])
    output = LANE / 'ready.json'
    if output.exists():
        assert read_json(output) == body
    write_json(output, body)
    print(dict(ready=output.relative_to(ROOT).as_posix(), sha256=sha256(output), functions=13, bytes=3424, files=len(files)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'descriptor', 'copied_root', 'ready'])
    globals()[parser.parse_args().action]()
