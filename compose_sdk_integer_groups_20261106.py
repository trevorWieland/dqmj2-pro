import argparse
import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from qualify_sdk_integer_groups_20261106 import identity


READY_PATHS = {'evidence/lanes/parallel-wave20261106/sdk-constant-data/ready.json',
               'evidence/lanes/parallel-wave20261106/sdk-sound-data/ready.json'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    parser.add_argument('--ready', action='append', required=True)
    parser.add_argument('--ready-sha256', action='append', required=True)
    parser.add_argument('--trace', action='append', default=[])
    args = parser.parse_args()
    assert len(args.ready) == len(args.ready_sha256) == 2 and set(args.ready) == READY_PATHS
    config = read_json(ROOT / args.configuration)
    assert config['membershipFrozen'] is True
    spec_path = ROOT / (config['name'] + '-specification.json')
    package_path = ROOT / (config['name'] + '-package.json')
    spec, package = read_json(spec_path), read_json(package_path)
    assert not spec.get('expectedDataAdditions') and not spec['migrations']
    function_hash = hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    registry_hash = sha256(ROOT / 'recovery.json')
    occupied = []
    for row in spec['expectedAdditions']:
        key = identity(dict(row, kind='data'))
        occupied.append((key[:3], key[4], key[4] + row['bytes']))
    additions, admitted, readies, traces = [], {}, [], list(args.trace)
    for name, digest in zip(args.ready, args.ready_sha256):
        assert sha256(ROOT / name) == digest
        ready = read_json(ROOT / name)
        assert ready['functionCount'] == ready['executableBytes'] == ready['encodedAssetBytes'] == ready['measuredZeroAlignmentBytes'] == 0
        assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
        for pin in read_json(ROOT / ready['sourceManifest'])['files']:
            assert sha256(ROOT / pin['path']) == pin['sha256']
        claim_name = name.rsplit('/', 1)[0] + '/data-claim.json'
        claim = read_json(ROOT / claim_name)
        assert claim['sourceCredit'] == 0 and not claim['functionOwnershipGranted']
        for row in claim['claimedStorage']:
            key = identity(row)
            assert key not in admitted
            admitted[key] = row['bytes']
        report = read_json(ROOT / ready['report'])
        assert report['functionMatched'] == 0 and len(report['dataMatches']) == ready['dataObjects']
        assert report['dataMatchedBytes'] == ready['initializedBytes'] == ready['typedConstantDataBytes']
        for row in report['dataMatches']:
            key = identity(row)
            assert row['kind'] == row['mode'] == 'data' and row['ordinaryFunctionCredit'] == 0
            assert row['realLink']['exactDataBytes'] and row['executableSectionBytes'] == 0
            assert row['bytes'] == admitted[key]
            assert not any(old[0] == key[:3] and max(key[4], old[1]) < min(key[4] + row['bytes'], old[2]) for old in occupied)
            occupied.append((key[:3], key[4], key[4] + row['bytes']))
            additions.append({field: row[field] for field in ['program', 'processor', 'module', 'mode', 'kind', 'address', 'bytes']})
        spec['packets'].append(dict(report=ready['canonicalReport'], producer=ready['canonicalProducer'], directProducer=False))
        if ready['sourceManifest'] not in package['manifests']:
            package['manifests'].append(ready['sourceManifest'])
        for extra in [name, ready['canonicalProducer'][1]]:
            if extra not in package['extra']:
                package['extra'].append(extra)
        traces.extend([claim_name, name.rsplit('/', 1)[0] + '/coordinator-review.json'])
        readies.append(dict(path=name, sha256=digest))
    assert len(additions) == len(admitted) == 9 and sum(row['bytes'] for row in additions) == 4314
    assert {identity(row): row['bytes'] for row in additions} == admitted
    spec.update(expectedDataAdditions=additions, dataOnlyCohort=not bool(spec['expectedAdditions']),
                initializedDataAccountingVersion='strict-sdk-integer-groups-v9', ordinaryFunctionGuardsRetained=True)
    for value in [spec, config]:
        assert value['postSealCommands'][0][0] == 'qualify_mixed_arm9_reference_inputs_20261105.py'
        value['postSealCommands'][0][0] = 'qualify_mixed_source_reference_inputs_20261106.py'
    assert function_hash == hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    receipt = f'evidence/verification/cohort{config["cohort"]}-sdk-integer-groups-composition-20261106.json'
    extras = ['compose_sdk_integer_groups_20261106.py', 'qualify_sdk_integer_groups_20261106.py',
              'prepare_source_data_cohort_v9_20261106.py', 'run_next_source_package_v27_20261106.py',
              'qualify_mixed_source_reference_inputs_20261106.py', 'admit_sdk_sound_storage_20261106.py',
              'inspect_sdk_sound_constants_20261106.py', 'freeze_sdk_sound_data_packet_20261106.py',
              'probe_sdk_sound_modules_20261106.py', 'admit_sdk_constant_storage_20261106.py',
              'freeze_sdk_constant_data_packet_20261106.py', 'probe_sdk_constant_modules_20261106.py', receipt]
    for name in extras:
        if name not in package['extra']:
            package['extra'].append(name)
    for name in traces:
        assert (ROOT / name).is_file()
        if name not in package['traces']:
            package['traces'].append(name)
    document = ROOT / config['document']
    text = document.read_text(encoding='utf-8')
    text += ('\n\nSeparate initialized-data addition: nine typed SDK constant arrays / 4,314 initialized bytes. '
             'No encoded-asset or alignment bytes are added. This adds zero functions. Both unchanged leaf '
             'qualifiers preserve earlier data and require semantic sources, typed STT_OBJECT storage and genuine links. '
             'All original function guards, sixteen shared stages and committed closure remain mandatory.\n')
    write_json(ROOT / args.configuration, config)
    write_json(spec_path, spec)
    write_json(package_path, package)
    document.write_text(text, encoding='utf-8')
    assert sha256(ROOT / 'recovery.json') == registry_hash
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, functionMembershipSha256=function_hash,
        functions=len(spec['expectedAdditions']), functionBytes=sum(row['bytes'] for row in spec['expectedAdditions']),
        initializedDataObjects=9, initializedDataBytes=4314, typedConstantDataBytes=4314,
        encodedAssetBytes=0, measuredZeroAlignmentBytes=0, readyPins=readies,
        specificationSha256=sha256(spec_path), packageSha256=sha256(package_path), registryUnchanged=True,
        originalSharedStageDriverUnchanged=True, generatorSha256=sha256(__file__)))
    print(dict(functions=len(spec['expectedAdditions']), initializedDataObjects=9, initializedDataBytes=4314, sourceCredit=0))


if __name__ == '__main__':
    main()
