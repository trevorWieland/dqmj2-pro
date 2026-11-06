import argparse
import hashlib
import json
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    args = parser.parse_args()
    config = read_json(ROOT / args.configuration)
    assert config['membershipFrozen'] is True
    spec_path = ROOT / (config['name'] + '-specification.json')
    package_path = ROOT / (config['name'] + '-package.json')
    spec, package = read_json(spec_path), read_json(package_path)
    assert not spec.get('expectedDataAdditions') and not spec['migrations']
    original_function_hash = hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    registry_hash = sha256(ROOT / 'recovery.json')
    ready_name = 'evidence/lanes/parallel-wave20261105/child-message-data/ready.json'
    assert sha256(ROOT / ready_name) == '1345c348ac4d12e9fef0ca7b8bdbfae6f63db17a346946f088ab3e85c64bf1db'
    ready = read_json(ROOT / ready_name)
    assert ready['functionCount'] == 0 and ready['initializedBytes'] == 3808
    assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
    for pin in read_json(ROOT / ready['sourceManifest'])['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    report = read_json(ROOT / ready['report'])
    assert report['functionMatched'] == 0 and len(report['dataMatches']) == 8
    additions = []
    occupied = []
    def interval(row):
        return (row.get('program') or '', row['processor'], row['module']), int(row['address'], 0), row['bytes']
    for row in spec['expectedAdditions']:
        scope, begin, size = interval(row)
        occupied.append((scope, begin, begin + size))
    for row in report['dataMatches']:
        scope, begin, size = interval(row)
        assert row['kind'] == 'data' and row['mode'] == 'data' and row['ordinaryFunctionCredit'] == 0
        assert row['realLink']['exactDataBytes'] and row['executableSectionBytes'] == 0
        assert not [old for old in occupied if old[0] == scope and max(begin, old[1]) < min(begin + size, old[2])]
        occupied.append((scope, begin, begin + size))
        additions.append({key: row[key] for key in ['program', 'processor', 'module', 'mode', 'kind', 'address', 'bytes']})
    assert sum(row['bytes'] for row in additions) == 3808
    spec.update(expectedDataAdditions=additions, dataOnlyCohort=not bool(spec['expectedAdditions']),
                initializedDataAccountingVersion='strict-child-message-data-v5', ordinaryFunctionGuardsRetained=True)
    spec['packets'].append(dict(report=ready['report'], producer=ready['producer'], directProducer=False))
    assert original_function_hash == hashlib.sha256(json.dumps(spec['expectedAdditions'], sort_keys=True).encode()).hexdigest()
    if ready['sourceManifest'] not in package['manifests']:
        package['manifests'].append(ready['sourceManifest'])
    extras = [ready_name, 'compose_child_message_mixed_cohort_20261106.py',
              'freeze_child_message_data_packet_20261106.py', 'admit_child_message_storage_20261106.py',
              'reserve_deferred_native_chunk_storage_v2_20261106.py', 'merge_closed_cohort_handoffs_v2_20261106.py',
              'export_reconstruction_atlas_data_v2_20261106.py',
              f'evidence/verification/cohort{config["cohort"]}-mixed-data-composition-20261106.json']
    for name in extras:
        if name not in package['extra']:
            package['extra'].append(name)
    for name in ['evidence/lanes/parallel-wave20261105/child-message-data/data-claim.json',
                 'evidence/lanes/parallel-wave20261105/child-message-data/admission-review.json',
                 'evidence/lanes/parallel-wave20261105/child-message-data/copied-root-controls.json',
                 'evidence/verification/child-message-data-accounting-preflight-20261106.json',
                 'evidence/verification/child-message-data-accounting-controls-20261106.json',
                 'evidence/verification/admitted-data-reservation-controls-20261106.json']:
        assert (ROOT / name).is_file()
        if name not in package['traces']:
            package['traces'].append(name)
    write_json(spec_path, spec)
    write_json(package_path, package)
    document = ROOT / config['document']
    text = document.read_text(encoding='utf-8')
    text += ('\n\nSeparate initialized-data addition: eight semantic message assets / 3,808 storage bytes, '
             'comprising 3,799 encoded asset bytes and nine measured zero-alignment bytes. This adds zero functions. '
             'Function guards remain unchanged; the versioned preparer separately validates data preservation, '
             'STT_OBJECT storage, exact bytes and genuine links. All sixteen original shared stages and committed '
             'closure remain mandatory.\n')
    document.write_text(text, encoding='utf-8')
    assert sha256(ROOT / 'recovery.json') == registry_hash
    write_json(ROOT / f'evidence/verification/cohort{config["cohort"]}-mixed-data-composition-20261106.json',
        dict(passed=True, sourceCredit=0, functionMembershipSha256=original_function_hash,
             functions=len(spec['expectedAdditions']), functionBytes=sum(row['bytes'] for row in spec['expectedAdditions']),
             initializedDataObjects=8, initializedDataBytes=3808, encodedAssetBytes=3799, measuredZeroAlignmentBytes=9,
             specificationSha256=sha256(spec_path), packageSha256=sha256(package_path), registryUnchanged=True,
             originalSharedStageDriverUnchanged=True, generatorSha256=sha256(__file__)))
    print(dict(functions=len(spec['expectedAdditions']), functionBytes=sum(row['bytes'] for row in spec['expectedAdditions']),
               initializedDataObjects=8, initializedDataBytes=3808, sourceCredit=0))


if __name__ == '__main__':
    main()
