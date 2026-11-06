import json
from pathlib import Path
from project import ROOT, read_json, write_json, sha256


NAME = 'cohort148-parallel-wave20261102'
ORIGINALS = [
    'cohort148-nitrosdk-breadth-and-coherent-scene-20261102',
    'cohort149-storage-closure-and-battle-context-20261102',
    'cohort150-arm7-receive-and-source-breadth-20261102'
]
CHILD = 'evidence/lanes/parallel-wave20261102/utility-child/'
NEXT_CHILD = 'evidence/lanes/parallel-wave20261102/utility-child-next/'
OVERLAY = 'evidence/lanes/parallel-wave20261102/overlay000/'
NEW_PACKETS = [
    dict(report=CHILD + 'packet-ready.json', producer=['wave20261102_child_next_replay_first.py'], directProducer=False),
    dict(report=NEXT_CHILD + 'packet-ready.json', producer=['wave20261102_child_next_replay_first.py', '--report', NEXT_CHILD + 'packet-ready.json', '--producer', 'wave20261102_child_next_packet.py', '--inputs-sha256', '1e50eb44910669c48ad78f81bb88f76180da9a3367978783db390d264d858d0e'], directProducer=False),
    dict(report=OVERLAY + 'wrapper-match.json', producer=['wave20261102_ov000_proof.py'], directProducer=False),
    dict(report=OVERLAY + 'breadth-match.json', producer=['wave20261102_ov000_breadth_proof.py', 'execute'], directProducer=False),
    dict(report=OVERLAY + 'component-forwarders-match.json', producer=['wave20261102_ov000_forwarders_proof.py', 'execute'], directProducer=False),
    dict(report=OVERLAY + 'tag-scans-match.json', producer=['wave20261102_ov000_scans.py', 'execute'], directProducer=False)
]
EXCLUDED = {'deps', 'tools', 'inputs', 'build', 'work', 'extract', 'asm', 'logs', '.git', '__pycache__'}


def main():
    specifications = [read_json(ROOT / (name + '-specification.json')) for name in ORIGINALS]
    packages = [read_json(ROOT / (name + '-package.json')) for name in ORIGINALS]
    packets = [row for spec in specifications for row in spec['packets']]
    additions = [row for spec in specifications for row in spec['expectedAdditions']]
    migrations = [row for spec in specifications for row in spec['migrations']]
    declared, comparison_inputs = {}, {}

    def include(name, expected=None):
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError('Wave input is unavailable or escaped: ' + name)
        digest = sha256(path)
        if expected and digest != expected:
            raise ValueError('Frozen packet input changed: ' + name)
        if path.relative_to(ROOT).parts[0] in EXCLUDED:
            comparison_inputs[name] = digest
            return
        if path.suffix.lower() in {'.bin', '.nds', '.sav', '.o', '.elf', '.exe', '.dll'}:
            raise ValueError('Executable payload cannot enter source package: ' + name)
        if name in declared and declared[name] != digest:
            raise ValueError('Packet source pin conflict: ' + name)
        declared[name] = digest

    for folder in [CHILD, NEXT_CHILD]:
        child = read_json(ROOT / (folder + 'packet-ready.json'))
        for row in child['generatorSources']:
            include(row['path'], row['sha256'])
        include(folder + 'packet-ready-inputs.json', child['inputManifestSha256'])
        include(folder + 'packet-ready-verification.json')
        for name in ['packet-ready-original.json', 'copied-root-replay-proof.json']:
            if (ROOT / (folder + name)).is_file():
                include(folder + name)
    immutable_json = [CHILD + 'packet-ready-inputs.json', NEXT_CHILD + 'packet-ready-inputs.json',
        OVERLAY + 'proof-inputs.json', OVERLAY + 'breadth-inputs.json',
        OVERLAY + 'component-forwarders-inputs.json', OVERLAY + 'tag-scans-inputs.json']
    include('replay_parallel_packet.py')
    for index, packet in enumerate(NEW_PACKETS):
        report = read_json(ROOT / packet['report'])
        if report.get('failed') or report.get('allPassed') is False:
            raise ValueError('Packet still has failed checks: ' + packet['report'])
        include(packet['report'])
        identifier = ['child2604', 'child-next804', 'ov000-wrapper96', 'ov000-breadth412', 'ov000-forwarders360', 'ov000-scans256'][index]
        canonical = 'evidence/matches/parallel-wave20261102-' + identifier + '.json'
        descriptor = 'provenance/parallel-wave20261102-' + identifier + '-replay.json'
        write_json(ROOT / descriptor, dict(workerReport=packet['report'], canonicalReport=canonical, romSha256=report['romSha256'],
            producer=packet['producer'], frozenInputs=[dict(path=immutable_json[index], sha256=sha256(ROOT / immutable_json[index]))],
            identities=[dict(program=row.get('program') or '', **{key: row[key] for key in ('processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256')}) for row in report['matches']]))
        include(descriptor)
        if (ROOT / canonical).is_file():
            include(canonical)
        packets.append(dict(report=canonical, producer=['replay_parallel_packet.py', descriptor], directProducer=False))
        for row in report['matches']:
            if not row.get('exactAfterDeclaredRelocation') or not row.get('realLink', {}).get('exactCallerBytes'):
                raise ValueError('Packet lacks complete real-link match: ' + row['name'])
            include(row['source'], row['sourceSha256'])
            for dependency in row.get('sourceDependencies', []):
                include(dependency['path'], dependency['sha256'])
            additions.append({key: row[key] for key in ('module', 'mode', 'address', 'bytes')})
    for name in ['ready.json', 'component-forwarders-ready.json', 'tag-scans-ready.json']:
        ready = read_json(ROOT / (OVERLAY + name))
        include(OVERLAY + name)
        for row in ready['files']:
            include(row['path'], row['sha256'])
    identities = {(r['module'], r['mode'], int(r['address'], 0)) for r in additions}
    if len(identities) != len(additions):
        raise ValueError('Aggregate wave duplicates a proposed function')
    for index, row in enumerate(additions):
        start, end = int(row['address'], 0), int(row['address'], 0) + row['bytes']
        for other in additions[:index]:
            if row['module'] == other['module'] and start < int(other['address'], 0) + other['bytes'] and int(other['address'], 0) < end:
                raise ValueError('Aggregate wave contains overlapping extents')
    input_pins = [dict(path=name + suffix, sha256=sha256(ROOT / (name + suffix)))
        for name in ORIGINALS for suffix in ('-specification.json', '-package.json')]
    specification = dict(cohort=148, previousAcceptedCohort=147, migrations=migrations, packets=packets,
        expectedAdditions=additions, originalChecksRetained=True,
        postSealCommands=[command for spec in specifications for command in spec.get('postSealCommands', [])],
        oracles=[oracle for spec in specifications for oracle in spec.get('oracles', [])],
        aggregateInputProposals=input_pins, originalProposalCohorts=[148, 149, 150],
        standaloneProposalPublicationSuperseded=True)
    manifest = 'provenance/parallel-wave20261102-source-files.json'
    write_json(ROOT / manifest, dict(sourceCredit=0, producedReportPinsDescribePreSealHandoff=True,
        files=[dict(path=path, sha256=digest) for path, digest in sorted(declared.items())],
        privateComparisonInputs=[dict(path=path, sha256=digest) for path, digest in sorted(comparison_inputs.items())],
        executableInputsCommitted=False))
    write_json(ROOT / (NAME + '-specification.json'), specification)
    extra = {value for package in packages for value in package['extra']}
    extra.update(name + suffix for name in ORIGINALS for suffix in ('-specification.json', '-package.json'))
    extra.update([__file__.split('\\')[-1], NAME + '-specification.json', 'stage_parallel_wave.py',
        'docs/2026-11-02-parallel-wave-acceptance.md', 'evidence/lanes/parallel-wave20261102/dispatch.json'])
    write_json(ROOT / (NAME + '-package.json'), dict(cohort=148,
        manifests=list(dict.fromkeys([name for package in packages for name in package['manifests']] + [manifest])),
        archives=list(dict.fromkeys(name for package in packages for name in package['archives'])),
        traces=list(dict.fromkeys(name for package in packages for name in package.get('traces', []))), extra=sorted(extra)))
    board = read_json(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json')
    board.update(pendingAcceptedCohorts=[147, 148],
        pendingSpecifications={'147': 'cohort147-arm7-cam-bootstrap-and-native-constructor-20261102-specification.json',
            '148': NAME + '-specification.json'},
        standaloneProposalsSuperseded=input_pins,
        aggregatePendingFunctions=len(additions), aggregatePendingBytes=sum(r['bytes'] for r in additions))
    for lane in board['active']:
        if lane['id'] == 'utility-child':
            lane['handedOffReports'] = [CHILD + 'packet-ready.json']
        if lane['id'] == 'utility-child-next':
            lane['handedOffReports'] = [NEXT_CHILD + 'packet-ready.json']
        if lane['id'] == 'overlay000':
            lane['handedOffReports'] = [OVERLAY + 'wrapper-match.json', OVERLAY + 'breadth-match.json', OVERLAY + 'component-forwarders-match.json', OVERLAY + 'tag-scans-match.json']
    write_json(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json', board)
    print(dict(cohort=148, functions=len(additions), initializedBytes=sum(r['bytes'] for r in additions),
        migrations=len(migrations), sourceRegistryChanged=False, originalProposalsPreserved=True))


if __name__ == '__main__':
    main()
