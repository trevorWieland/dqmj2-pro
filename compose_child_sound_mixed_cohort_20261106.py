import argparse
import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from qualify_child_sound_data_additions_20261106 import CLAIM, identity


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    parser.add_argument('--ready', required=True)
    parser.add_argument('--ready-sha256', required=True)
    parser.add_argument('--trace', action='append', default=[])
    args = parser.parse_args()
    config = read_json(ROOT / args.configuration)
    assert config['membershipFrozen'] is True
    spec_path = ROOT / (config['name'] + '-specification.json')
    package_path = ROOT / (config['name'] + '-package.json')
    spec, package = read_json(spec_path), read_json(package_path)
    assert not spec.get('expectedDataAdditions') and not spec['migrations']
    function_hash = hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    registry_hash = sha256(ROOT / 'recovery.json')
    assert sha256(ROOT / args.ready) == args.ready_sha256
    ready = read_json(ROOT / args.ready)
    assert ready['functionCount'] == 0 and ready['initializedBytes'] == 13936 and ready['dataObjects'] == 1
    assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
    manifest = read_json(ROOT / ready['sourceManifest'])
    for pin in manifest['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    report = read_json(ROOT / ready['report'])
    assert report['functionMatched'] == 0 and len(report['dataMatches']) == 1
    claim = {identity(row): row['bytes'] for row in read_json(ROOT / CLAIM)['claimedStorage']}
    additions, occupied = [], []
    for row in spec['expectedAdditions']:
        key = identity(dict(row, kind='data'))
        occupied.append((key[:3], key[4], key[4] + row['bytes']))
    for row in report['dataMatches']:
        key = identity(row)
        assert row['kind'] == 'data' and row['mode'] == 'data' and row['ordinaryFunctionCredit'] == 0
        assert row['realLink']['exactDataBytes'] and row['executableSectionBytes'] == 0
        assert row['bytes'] == claim[key]
        assert not [old for old in occupied if old[0] == key[:3] and max(key[4], old[1]) < min(key[4] + row['bytes'], old[2])]
        occupied.append((key[:3], key[4], key[4] + row['bytes']))
        additions.append({key: row[key] for key in ['program', 'processor', 'module', 'mode', 'kind', 'address', 'bytes']})
    assert {identity(row): row['bytes'] for row in additions} == claim
    assert sum(row['bytes'] for row in additions) == 13936
    spec.update(expectedDataAdditions=additions, dataOnlyCohort=not bool(spec['expectedAdditions']),
                initializedDataAccountingVersion='strict-child-sound-data-v7', ordinaryFunctionGuardsRetained=True)
    spec['packets'].append(dict(report=ready['report'], producer=ready['producer'], directProducer=False))
    for value in [spec, config]:
        assert value['postSealCommands'][0][0] == 'qualify_mixed_arm9_reference_inputs_20261105.py'
        value['postSealCommands'][0][0] = 'qualify_mixed_source_reference_inputs_20261106.py'
    write_json(ROOT / args.configuration, config)
    assert function_hash == hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    if ready['sourceManifest'] not in package['manifests']:
        package['manifests'].append(ready['sourceManifest'])
    receipt = f'evidence/verification/cohort{config["cohort"]}-sound-data-composition-20261106.json'
    extras = [args.ready, 'qualify_mixed_source_reference_inputs_20261106.py', 'initialized_storage_protection_20261106.py', 'compose_child_sound_mixed_cohort_20261106.py',
              'admit_child_sound_storage_20261106.py', 'qualify_child_sound_data_additions_20261106.py',
              'prepare_source_data_cohort_v7_20261106.py', 'run_next_source_package_v25_20261106.py', receipt]
    for name in extras:
        if name not in package['extra']:
            package['extra'].append(name)
    for name in [CLAIM, 'evidence/lanes/parallel-wave20261105/child-sdat-next/coordinator-review.json', *args.trace]:
        assert (ROOT / name).is_file()
        if name not in package['traces']:
            package['traces'].append(name)
    write_json(spec_path, spec)
    write_json(package_path, package)
    document = ROOT / config['document']
    text = document.read_text(encoding='utf-8')
    text += ('\n\nSeparate initialized-data addition: one semantic sound archive / '
             '13,936 storage bytes, comprising 13,935 encoded asset bytes and one measured zero-alignment byte. '
             'This adds zero functions. Original function guards remain unchanged; the versioned preparer '
             'separately checks data preservation, typed semantic generation, STT_OBJECT storage and genuine links. '
             'All sixteen original shared stages and committed closure remain mandatory.\n')
    document.write_text(text, encoding='utf-8')
    assert sha256(ROOT / 'recovery.json') == registry_hash
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, functionMembershipSha256=function_hash,
        functions=len(spec['expectedAdditions']), functionBytes=sum(row['bytes'] for row in spec['expectedAdditions']),
        initializedDataObjects=1, initializedDataBytes=13936, encodedAssetBytes=13935, measuredZeroAlignmentBytes=1,
        specificationSha256=sha256(spec_path), packageSha256=sha256(package_path), registryUnchanged=True,
        originalSharedStageDriverUnchanged=True, generatorSha256=sha256(__file__)))
    print(dict(functions=len(spec['expectedAdditions']), functionBytes=sum(row['bytes'] for row in spec['expectedAdditions']),
               initializedDataObjects=1, initializedDataBytes=13936, sourceCredit=0))


if __name__ == '__main__':
    main()
