import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from project import ROOT, configuration, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure

LANE = ROOT / 'evidence/lanes/parallel-wave20261105/main-sdk-bulk/varargs/packet'
INPUT = LANE / 'inputs.json'
PRODUCER = 'wave20261105_main_sdk_bulk_varargs_match.py'
CANONICAL = 'evidence/matches/main-sdk-bulk-varargs-parallel-wave20261105.json'


def identity(row, rom):
    return dict(id=rom + '/arm9/main/arm/' + format(int(row['address'], 0), '08x'), program='', processor='arm9', module='main', mode='arm',
        address=row['address'], bytes=row['bytes'], source=row['source'], sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'])


def prepare():
    closed = read_json(LANE.parent / 'readable.json')['closed']
    from recover_linked_runtime import qualified_bindings
    entries = []
    names = set(code_closure([PRODUCER]))
    prior = read_json(LANE.parents[1] / 'first/inputs.json')
    names.update(pin['path'] for pin in prior['files'] if pin['path'].startswith(('deps/native/', 'tools/mwccarm/')))
    names.update(['project.json', 'tools.lock.json', 'provenance/seed-manifest.json', 'extract/arm9/arm9.bin', 'config/arm9/symbols.txt', 'config/arm9/relocs.txt'])
    reference = ROOT / 'work/w5sb/public-arm/SonicRushAdventure-Decomp/tools/cw/include/MSL_C'
    abi = dict(repository='RushRE/SonicRushAdventure-Decomp', commit='fb9b7e4dd9b5babbc114d6165f0279352bd11ecc')
    for key, name in [('arm', 'stdarg.ARM.h'), ('types', 'va_list.h'), ('cstdarg', 'cstdarg')]:
        target = LANE.parent / 'reference' / (name + '.txt')
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            assert target.read_bytes() == (reference / name).read_bytes()
        else:
            shutil.copyfile(reference / name, target)
        abi[key] = dict(path=target.relative_to(ROOT).as_posix(), sha256=sha256(target), url='https://raw.githubusercontent.com/' + abi['repository'] + '/' + abi['commit'] + '/tools/cw/include/MSL_C/' + name)
        names.add(abi[key]['path'])
    for result in sorted(closed, key=lambda result: int(result['entry']['address'], 0)):
        row = result['entry']
        item = {key: row[key] for key in ['address', 'bytes', 'source', 'sourceSha256', 'sourceDependencies', 'targetSha256', 'compilerPath', 'compilerSha256']}
        item.update(flags=row['compilerFlags'], priorRelocations=row['relocations'], referenceFunction=result['referenceFunction'],
            qualifiedDependencies=qualified_bindings(row), provenance=result['provenance'], extraLayoutChecks=[])
        address = int(item['address'], 0)
        if address in [0x020118a4, 0x02011a34]:
            item['extraLayoutChecks'] = [dict(type='va_list', bytes=4), dict(type='unsigned long', bytes=4), dict(type='WMArm9Buf', bytes=512),
                dict(type='WMArm9Buf', member='status', offset=4), dict(type='WMStatus', bytes=2000), dict(type='WMStatus', member='state', offset=0),
                dict(type='NativeStorage_020e5d80', bytes=2720), dict(type='NativeStorage_020e5d80', member='field_0008', offset=8)]
        else:
            item['extraLayoutChecks'] = [dict(type='size_t', bytes=4), dict(type='dst_string', bytes=12), dict(type='dst_string', member='len', offset=0),
                dict(type='dst_string', member='cur', offset=4), dict(type='dst_string', member='base', offset=8)]
            if address == 0x0201a670:
                item['extraLayoutChecks'] += [dict(type='va_list', bytes=4), dict(type='u64', bytes=8)]
        names.add(item['source'])
        names.update(pin['path'] for pin in item['sourceDependencies'])
        names.add(item['provenance']['referenceSource'])
        entries.append(item)
    assert len(entries) == 5 and sum(item['bytes'] for item in entries) == 2792
    body = dict(schemaVersion=1, romSha256=configuration()['romSha256'], moduleSha256=closed[0]['identity']['inputModuleSha256'], entries=entries, publishedArmABI=abi,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(names)],
        scope='Five ordinary C WM/format units with primary ARM MSL variadic declarations, one separately witnessed SDK weak export and no supplied-callee source credit.')
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


def weak_witness():
    report = read_json(LANE / 'match.json')
    proof = report['weakSourceExportEvidence'][0]
    assert proof['compiler']['binding'] == proof['split']['binding'] == proof['finalElf']['binding'] == 14
    body = dict(schemaVersion=1, scope='generated-canonical-source-export-records-only', exports=[proof['export']], requiredCompilerBinding=14,
        definedFunctionOnly=True, originalAliasesAndStrongScopesUnchanged=True, sourceByteCredit=0)
    path = LANE / 'std-proven-weak-exports-v1.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path, body)
    fields = ['sha256', 'rawStInfo', 'binding', 'type', 'bytes', 'bodySha256', 'relocations']
    evidence = dict(schemaVersion=1, allPassed=True, manifest=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)),
        exactCompilerSplitFinalScope=[{key: proof[stage][key] for key in fields} for stage in ['compiler', 'split', 'finalElf']],
        sourceAndPublishedDeclarationPinned=True, fullNativeInitializedBytesExact=True, originalObjectRelocationsPreserved=True,
        strongInterfaceNegative=next(control for control in report['negativeEvidence'] if control.get('requiredCompilerBinding') == 14),
        unchangedGlobalDsdScopeCheckRequired=True, isolatedWholeConfigDsdFeasibility='ARM9 symbols not found in the isolated caller ELF; no module markers or ELF artifacts were fabricated.',
        sourceOrByteCredit=0)
    output = LANE / 'weak-export-qualification.json'
    if output.exists():
        assert read_json(output) == evidence
    write_json(output, evidence)
    print(dict(weakManifest=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))


def copied_root():
    clone = ROOT / 'work/w5sbvc1'
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
    write_json(LANE / 'copied-root.json', dict(allPassed=True, functions=len(objects), bytes=2792, freshCanonicalObjectsVerified=True,
        noInitialWorkWorkerOrCanonicalOutputs=True, allLinkerCwdsInsideCopiedRoot=True, immutableInputs=len(names), objects=objects,
        canonicalReportSha256=sha256(clone / CANONICAL), actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        suppliedCalleeSourceOrExecutionCredit=0, stdout=result.stdout, stderr=result.stderr))
    print(dict(copiedRootPassed=True, functions=len(objects), bytes=2792))


def ready():
    report, copied, inputs = read_json(LANE / 'match.json'), read_json(LANE / 'copied-root.json'), read_json(INPUT)
    assert report['allPassed'] and copied['allPassed'] and report['matchedBytes'] == copied['bytes'] == 2792
    assert sum(row['ordinaryCBytes'] for row in report['matches']) == 2792 and sum(row['justifiedAssemblyBytes'] for row in report['matches']) == 0
    names = {pin['path'] for pin in inputs['files']}
    names.update(code_closure([PRODUCER, Path(__file__).name, 'replay_parallel_packet.py']))
    names.update((LANE / name).relative_to(ROOT).as_posix() for name in ['inputs.json', 'canonical.json', 'copied-root.json', 'std-proven-weak-exports-v1.json', 'weak-export-qualification.json'])
    files = [dict(path=name, sha256=sha256(ROOT / name), kind='frozen-runtime-input-or-proof') for name in sorted(names)]
    files.append(dict(path=(LANE / 'match.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'match.json'), kind='regenerated-worker-report'))
    body = dict(schemaVersion=1, status='ready-for-coordinator-acceptance', acceptedBaselineCohort=154, romSha256=inputs['romSha256'], functions=5, bytes=2792,
        ordinaryCBytes=2792, justifiedAssemblyBytes=0, packets=[dict(report=(LANE / 'match.json').relative_to(ROOT).as_posix(), producer=[PRODUCER])],
        canonicalDescriptor=dict(path=(LANE / 'canonical.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'canonical.json')),
        identities=[identity(row, inputs['romSha256']) for row in inputs['entries']], files=files, actualNativeAndSourceCallerReturns=report['actualNativeAndSourceCallerReturns'],
        primitiveProbeSourceCredit=0, suppliedCalleeSourceOrExecutionCredit=0, copiedRootFreshCanonicalReplayPassed=True, diagnosticInventoriesAreNotRuntimeInputs=True,
        sourceClassification='Ordinary C with published ARM MSL varargs ABI, original imports and separately qualified SDK weak export', sourceCreditPendingSharedAcceptance=True, limits=report['limits'])
    body['weakSourceExportWitness'] = dict(path=(LANE / 'std-proven-weak-exports-v1.json').relative_to(ROOT).as_posix(), sha256=sha256(LANE / 'std-proven-weak-exports-v1.json'))
    path = LANE / 'ready.json'
    if path.exists():
        assert read_json(path) == body
    write_json(path, body)
    print(dict(ready=path.relative_to(ROOT).as_posix(), sha256=sha256(path), functions=5, bytes=2792, files=len(files)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'descriptor', 'weak_witness', 'copied_root', 'ready'])
    globals()[parser.parse_args().action]()
