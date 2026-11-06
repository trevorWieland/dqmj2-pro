import argparse
import json
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, configuration
from parallel_status import interval, collisions, number


EXCLUDED = {'deps', 'tools', 'inputs', 'build', 'work', 'extract', 'asm', 'logs', '.git', '__pycache__'}


def reserved_storage(root, rom):
    result = []
    for name, key in [('ledger/linkage.json', 'regions'), ('ledger/data.json', 'records')]:
        document = read_json(root / name)
        if document['buildSha256'] != rom:
            raise ValueError('Bookkeeping ledger belongs to another ROM')
        for row in document[key]:
            if key == 'records' and (row.get('kind') == 'bss' or not row.get('states', {}).get('dataMatched')):
                continue
            size = number(row['bytes'])
            if size <= 0:
                continue
            module = row['module']
            processor = row.get('processor') or ('arm7' if 'arm7' in module else 'arm9')
            program = row.get('program') or ('dwc/utility.bin/move/child.srl' if module.startswith('utility-child-') else '')
            begin = number(row['address'])
            result.append((name, ((program, processor, module), begin, begin + size, 'data')))
    return result


def metadata_names(config):
    names = set(config['readyPackets']) | set(config.get('opaqueMetadata', []))
    if any(Path(name).suffix.lower() not in {'.json', '.txt', '.csv', '.md'} for name in names):
        raise ValueError('Opaque metadata cannot contain compiler source or executable payloads')
    return names


def classify_metadata(relative, runtime, opaque):
    if relative not in opaque:
        return False
    if runtime:
        raise ValueError('Actual compiler/replay input cannot be opaque metadata: ' + relative)
    return True


def packet_identifier(name, index, config, used):
    value = config.get('packetIds', {}).get(name, Path(name).parent.name) + '-' + str(index)
    if value in used or '/' in value or '\\' in value or ':' in value:
        raise ValueError('Packet replay identifier is not unique and confined: ' + value)
    used.add(value)
    return value


def mandatory_inputs(initial, root=ROOT):
    pending, found = list(initial), {}
    while pending:
        pin = pending.pop(0)
        path = (root / pin['path']).resolve()
        if not path.is_relative_to(root) or not path.is_file():
            raise ValueError('Mandatory replay input is unavailable or escaped')
        relative = path.relative_to(root).as_posix()
        if relative in found:
            if found[relative] != pin['sha256']:
                raise ValueError('Conflicting mandatory replay input identities')
            continue
        if sha256(path) != pin['sha256']:
            raise ValueError('Mandatory replay input changed: ' + relative)
        found[relative] = pin['sha256']
        if path.suffix == '.json':
            value = read_json(path)
            external = value.get('mandatoryExternalInputs', []) if isinstance(value, dict) else []
            if not isinstance(external, list):
                raise ValueError('Mandatory external inputs must be a pin list')
            pending.extend(external)
    return [dict(path=path, sha256=digest) for path, digest in found.items()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    options = parser.parse_args()
    config = read_json(ROOT / options.configuration)
    cohort = config['cohort']
    if cohort != config['previousAcceptedCohort'] + 1:
        raise ValueError('Wave must follow its accepted predecessor')
    name = config['name']
    declared, comparison, packets, additions, owned = {}, {}, [], [], []
    opaque_names, opaque, identifiers = metadata_names(config), {}, set()
    rom = configuration()['romSha256']

    def include(name, expected=None, runtime=False):
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or not path.is_file():
            raise ValueError('Unavailable or escaped packet input: ' + name)
        relative = path.relative_to(ROOT).as_posix()
        digest = sha256(path)
        if expected and digest != expected:
            raise ValueError('Frozen packet input changed: ' + relative)
        if classify_metadata(relative, runtime, opaque_names):
            opaque[relative] = digest
            return
        if path.relative_to(ROOT).parts[0] in EXCLUDED:
            comparison[relative] = digest
            return
        if path.suffix.lower() in {'.bin', '.nds', '.sav', '.o', '.elf', '.exe', '.dll'}:
            raise ValueError('Executable payload cannot enter authored source: ' + relative)
        if relative in declared and declared[relative] != digest:
            raise ValueError('Conflicting packet input pins: ' + relative)
        declared[relative] = digest

    reserved = reserved_storage(ROOT, rom)
    for metadata in config.get('opaqueMetadata', []):
        include(metadata)
    for line in (ROOT / 'ledger/functions.jsonl').read_text().splitlines():
        row = json.loads(line)
        if row['states']['functionMatched']:
            reserved.append(('current-selected-source', interval(row)))
    for path in config.get('reservedSpecifications', []):
        spec = read_json(ROOT / path)
        for row in spec['expectedAdditions'] + spec.get('migrations', []):
            reserved.append((path, interval(row)))
    for ready_name in config['readyPackets']:
        ready = read_json(ROOT / ready_name)
        if ready.get('status') != 'ready-for-coordinator-acceptance' or ready['romSha256'] != rom:
            raise ValueError('Worker packet is not ready for this ROM: ' + ready_name)
        produced = {packet['report'] for packet in ready['packets']}
        include(ready_name)
        for row in ready['files']:
            include(row['path'], None if row['path'] in produced else row['sha256'])
        for packet_index, packet in enumerate(ready['packets']):
            report = read_json(ROOT / packet['report'])
            if report.get('failed') or report.get('allPassed') is False or report['romSha256'] != rom:
                raise ValueError('Worker match report failed: ' + packet['report'])
            if not report.get('matches'):
                raise ValueError('Empty packet is not an acceptance chunk')
            for pin in report.get('generatorSources', []):
                include(pin['path'], pin['sha256'], runtime=True)
            include(packet['report'])
            if ready.get('canonicalDescriptor'):
                existing = ready['canonicalDescriptor']
                include(existing['path'], existing['sha256'], runtime=True)
                frozen = read_json(ROOT / existing['path'])['frozenInputs']
            else:
                if not isinstance(report.get('inputs'), dict):
                    raise ValueError('Packet requires a pinned canonicalDescriptor or report.inputs: ' + ready_name)
                frozen = [report['inputs']]
            frozen = mandatory_inputs(frozen + config.get('additionalFrozenInputs', {}).get(ready_name, []))
            if not frozen:
                raise ValueError('Packet lacks mandatory frozen replay inputs')
            for pin in frozen:
                include(pin['path'], pin['sha256'], runtime=True)
            identifier = packet_identifier(ready_name, packet_index, config, identifiers)
            descriptor = 'provenance/' + name + '-' + identifier + '-replay.json'
            canonical = 'evidence/matches/' + name + '-' + identifier + '.json'
            identities = []
            for row in report['matches']:
                if not row.get('exactAfterDeclaredRelocation') or not row.get('realLink', {}).get('exactCallerBytes'):
                    raise ValueError('Packet lacks a complete genuine linked match: ' + row['name'])
                include(row['source'], row['sourceSha256'], runtime=True)
                for dependency in row.get('sourceDependencies', []):
                    include(dependency['path'], dependency['sha256'], runtime=True)
                identities.append(dict(program=row.get('program') or '', **{
                    key: row[key] for key in ('processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256', 'targetSha256')}))
                additions.append(dict(program=row.get('program') or '', **{
                    key: row[key] for key in ('processor', 'module', 'mode', 'address', 'bytes')}))
                owned.append((identifier, interval(row)))
            write_json(ROOT / descriptor, dict(romSha256=rom, producer=packet['producer'],
                workerReport=packet['report'], canonicalReport=canonical,
                frozenInputs=frozen, identities=identities))
            include(descriptor)
            if (ROOT / canonical).is_file():
                include(canonical)
            bridge = config.get('packetBridges', {}).get(ready_name, 'replay_parallel_packet.py')
            include(bridge)
            packets.append(dict(report=canonical, producer=[bridge, descriptor], directProducer=False))
    overlaps = collisions(owned, reserved)
    if overlaps:
        raise ValueError('Wave overlaps accepted/reserved/other packet extents: ' + str(overlaps))
    include('replay_parallel_packet.py')
    manifest = 'provenance/' + name + '-source-files.json'
    write_json(ROOT / manifest, dict(sourceCredit=0, producedReportPinsDescribePreSealHandoff=True,
        files=[dict(path=path, sha256=digest) for path, digest in sorted(declared.items())],
        opaqueIntakeMetadata=[dict(artifact=path, sha256=digest) for path, digest in sorted(opaque.items())],
        privateComparisonInputs=[dict(path=path, sha256=digest) for path, digest in sorted(comparison.items())],
        executableInputsCommitted=False))
    write_json(ROOT / (name + '-specification.json'), dict(cohort=cohort,
        previousAcceptedCohort=config['previousAcceptedCohort'], migrations=[], packets=packets,
        expectedAdditions=additions, originalChecksRetained=True,
        postSealCommands=config.get('postSealCommands', []), oracles=[],
        readyPacketInputs=[dict(path=path, sha256=sha256(ROOT / path)) for path in config['readyPackets']]))
    write_json(ROOT / (name + '-package.json'), dict(cohort=cohort, manifests=[manifest], archives=[], traces=sorted(opaque),
        extra=[options.configuration, Path(__file__).name, config['stage'], config['document'],
            name + '-specification.json', 'evidence/lanes/parallel-wave20261102/dispatch.json', *config.get('extra', [])]))
    print(dict(cohort=cohort, functions=len(additions), bytes=sum(row['bytes'] for row in additions),
        sourceRegistryChanged=False, originalChecksRetained=True))


if __name__ == '__main__':
    main()
