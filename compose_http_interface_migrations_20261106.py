import argparse
import copy
import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from replay_http_interface_migration_20261106 import projection


DESCRIPTORS = {'provenance/http-explicit-interfaces-canonical-transport-20261106.json',
               'provenance/http-explicit-strncpy-canonical-transport-20261106.json'}


def identity(row):
    return row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0)


def membership(rows):
    return hashlib.sha256(json.dumps(rows, sort_keys=True).encode()).hexdigest()


def plan(configuration, specification, package, descriptor_pins, traces):
    config, spec, package = copy.deepcopy((configuration, specification, package))
    assert config['membershipFrozen'] is True
    assert config['cohort'] == spec['cohort'] == package['cohort']
    assert config['cohort'] == 167 and config['previousAcceptedCohort'] == spec['previousAcceptedCohort'] == 166
    assert not spec['migrations'] and not spec.get('expectedDataAdditions')
    assert len(descriptor_pins) == 2 and {p['path'] for p in descriptor_pins} == DESCRIPTORS
    pending = {p['path']: p for p in config['pendingZeroByteMigrationReady']}
    assert len(pending) == 2
    predecessor = read_json(ROOT / 'cohort166-parallel-wave20261105-k-specification.json')
    prior = {identity(r): r for r in predecessor['expectedAdditions']}
    new = {identity(r): r for r in spec['expectedAdditions']}
    assert len(new) == len(spec['expectedAdditions'])
    function_hash = membership(spec['expectedAdditions'])
    migrations, keys, ready_pins = [], set(), []
    extras, metadata = [__file__.split('\\')[-1]], list(traces)
    for pin in descriptor_pins:
        assert sha256(ROOT / pin['path']) == pin['sha256']
        descriptor = read_json(ROOT / pin['path'])
        ready_name = descriptor['ready']
        assert pending[ready_name]['sha256'] == descriptor['readySha256'] == sha256(ROOT / ready_name)
        assert pending[ready_name]['requiredAcceptedPredecessor'] == 166
        ready = read_json(ROOT / ready_name)
        assert ready['requiredPredecessor'] == 166
        assert ready['sourceCredit'] == ready['newByteCredit'] == ready['newFunctionCredit'] == 0
        assert ready['freshOriginalAndExplicitViewsCompiledAndLinked']
        assert ready['originalFrozenSourcesHeadersInputsAndReadyUnchanged']
        assert ready['freshCopiedRootMigratedCallers'] == ready['migrationFunctions']
        assert ready['copiedRootTamperControls'] >= 2
        assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
        for source in read_json(ROOT / ready['sourceManifest'])['files']:
            assert sha256(ROOT / source['path']) == source['sha256']
        report = read_json(ROOT / descriptor['output'])
        assert report['allPassed'] and report['migrationOnly']
        assert projection(report) == descriptor['immutableCallerProjection']
        assert report['newSourceBytes'] == report['newByteCredit'] == report['newFunctionCredit'] == 0
        assert report['frozenMigrationReady'] == ready_name
        assert report['generator'] == 'replay_http_interface_migration_20261106.py'
        assert report['generatorSha256'] == sha256(ROOT / report['generator'])
        for source in report['replayDependencies'] + report['generatorSources']:
            assert sha256(ROOT / source['path']) == source['sha256']
        declared = {identity(row): row for row in ready['migrations']}
        assert len(declared) == ready['migrationFunctions'] == len(report['matches'])
        assert [identity(r) for r in report['matches']] == [identity(r) for r in descriptor['identities']]
        for row in report['matches']:
            key = identity(row)
            assert key[:4] == ('', 'arm9', 'main', 'thumb')
            assert key in declared and key in prior and key not in new and key not in keys
            assert row['bytes'] == declared[key]['bytes'] == prior[key]['bytes']
            assert row['ordinaryCBytes'] == row['bytes'] and row['justifiedAssemblyBytes'] == 0
            assert row['interfaceMigrationOnly'] and row['realLink']['exactCallerBytes']
            assert sha256(ROOT / row['source']) == row['sourceSha256']
            assert sha256(ROOT / row['object']) == row['objectSha256']
            keys.add(key)
            migrations.append(declared[key])
        producer = ['replay_http_interface_migration_20261106.py', pin['path']]
        spec['packets'].append(dict(report=descriptor['output'], producer=producer, directProducer=False))
        if ready['sourceManifest'] not in package['manifests']:
            package['manifests'].append(ready['sourceManifest'])
        extras.extend([pin['path'], ready_name, *[p['path'] for p in report['generatorSources']]])
        ready_pins.append(dict(path=ready_name, sha256=descriptor['readySha256']))
    assert len(migrations) == 6 and sum(r['bytes'] for r in migrations) == 956
    assert function_hash == membership(spec['expectedAdditions'])
    spec['migrations'] = migrations
    config['composedZeroByteInterfaceMigrations'] = ready_pins
    receipt = f'evidence/verification/cohort{config["cohort"]}-http-interface-migration-composition-20261106.json'
    extras.append(receipt)
    for name in extras:
        if name not in package['extra']:
            package['extra'].append(name)
    for name in metadata:
        assert (ROOT / name).is_file(), name
        if name not in package['traces']:
            package['traces'].append(name)
    result = dict(passed=True, sourceCredit=0, newFunctionCredit=0, newByteCredit=0,
                  migrationFunctions=6, preservedExistingBytes=956,
                  functionMembershipSha256=function_hash, functions=len(spec['expectedAdditions']),
                  functionBytes=sum(r['bytes'] for r in spec['expectedAdditions']),
                  readyPins=ready_pins, descriptorPins=descriptor_pins,
                  originalSharedMigrationPreparerAndPublisherRequired=True,
                  originalFormalTypesProven=False, generatorSha256=sha256(__file__))
    return config, spec, package, receipt, result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('configuration')
    parser.add_argument('--descriptor', action='append', required=True)
    parser.add_argument('--sha256', action='append', required=True)
    parser.add_argument('--trace', action='append', default=[])
    args = parser.parse_args()
    assert len(args.descriptor) == len(args.sha256) == 2
    config = read_json(ROOT / args.configuration)
    spec_name, package_name = config['name'] + '-specification.json', config['name'] + '-package.json'
    unchanged = {p: sha256(ROOT / p) for p in ['recovery.json', 'source-preferences.json']}
    pins = [dict(path=p, sha256=h) for p, h in zip(args.descriptor, args.sha256)]
    config, spec, package, receipt, result = plan(config, read_json(ROOT / spec_name),
                                               read_json(ROOT / package_name), pins, args.trace)
    for p, h in unchanged.items():
        assert sha256(ROOT / p) == h
    write_json(ROOT / args.configuration, config)
    write_json(ROOT / spec_name, spec)
    write_json(ROOT / package_name, package)
    result.update(specificationSha256=sha256(ROOT / spec_name), packageSha256=sha256(ROOT / package_name),
                  registryAndPreferencesUnchanged=True)
    write_json(ROOT / receipt, result)
    print(dict(passed=True, migrationFunctions=6, preservedExistingBytes=956, newByteCredit=0))


if __name__ == '__main__':
    main()
