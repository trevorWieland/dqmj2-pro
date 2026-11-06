import copy
import runpy
import sys
import uuid
from unittest.mock import patch
import project
from project import ROOT, read_json, write_json, sha256


def main():
    ready = 'evidence/lanes/parallel-wave20261106/sdk-constant-data/ready.json'
    ready_hash = 'b6ded369a480b97038023e5fd921a2980de0840486ee29767f767255f63b9e8c'
    assert sha256(ROOT / ready) == ready_hash
    sound_ready = 'evidence/lanes/parallel-wave20261106/sdk-sound-data/ready.json'
    sound_hash = '2645e60f6dc586c8aed21095006151cf9427f458716d5c5f3d804de90ebe8111'
    assert sha256(ROOT / sound_ready) == sound_hash
    original_config = 'provenance/parallel-wave20261105-k-packets.json'
    config = read_json(ROOT / original_config)
    original_spec = config['name'] + '-specification.json'
    spec = read_json(ROOT / original_spec)
    package = read_json(ROOT / (config['name'] + '-package.json'))
    protected = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', original_config, original_spec]}
    work = ROOT / 'work/sdk-integer-groups-composer' / uuid.uuid4().hex[:10]
    work.mkdir(parents=True)
    config.update(name=(work / 'cohort166').relative_to(ROOT).as_posix(), membershipFrozen=True,
                  document=(work / 'acceptance.md').relative_to(ROOT).as_posix())
    config_name = (work / 'configuration.json').relative_to(ROOT).as_posix()
    private_spec = ROOT / (config['name'] + '-specification.json')
    private_package = ROOT / (config['name'] + '-package.json')
    (ROOT / config['document']).write_text('Private composition fixture\n', encoding='utf-8')
    before_membership = copy.deepcopy(spec['expectedAdditions'])
    receipts = []
    original_write = project.write_json

    def private_write(path, value):
        if path == ROOT / 'evidence/verification/cohort166-sdk-integer-groups-composition-20261106.json':
            receipts.append(value)
            return original_write(work / 'composition-receipt.json', value)
        return original_write(path, value)

    def prepare(value):
        write_json(ROOT / config_name, config)
        write_json(private_spec, value)
        write_json(private_package, package)

    def execute(extra):
        command = ['compose_sdk_integer_groups_20261106.py', config_name, '--ready', ready,
                   '--ready-sha256', ready_hash, '--ready', sound_ready, '--ready-sha256', sound_hash, *extra]
        with patch.object(project, 'write_json', side_effect=private_write), patch.object(sys, 'argv', command):
            runpy.run_path(str(ROOT / command[0]), run_name='__main__')

    controls = []
    for label in ['missing-trace', 'function-overlap']:
        changed = copy.deepcopy(spec)
        if label == 'function-overlap':
            changed['expectedAdditions'].append(dict(program='', processor='arm9', module='main', mode='arm',
                                                     address='0x20d7fe0', bytes=4))
        prepare(changed)
        before = {str(path): sha256(path) for path in [ROOT / config_name, private_spec, private_package]}
        try:
            execute(['--trace', 'evidence/nonexistent-sdk-fixture-trace.json'] if label == 'missing-trace' else [])
        except AssertionError:
            assert before == {name: sha256(name) for name in before}
            controls.append(dict(control=label, rejectedWithoutCoreMetadataMutation=True))
        else:
            raise AssertionError('Invalid mixed composition accepted')
    prepare(spec)
    execute([])
    result = read_json(private_spec)
    assert result['expectedAdditions'] == before_membership and len(result['expectedDataAdditions']) == 9
    assert sum(row['bytes'] for row in result['expectedDataAdditions']) == 4314
    assert result['packets'][-1]['report'] == read_json(ROOT / sound_ready)['canonicalReport']
    assert len(receipts) == 1 and receipts[0]['registryUnchanged']
    assert protected == {name: sha256(ROOT / name) for name in protected}
    write_json(ROOT / 'evidence/verification/sdk-integer-groups-composition-preflight-20261106.json',
        dict(passed=True, sourceCredit=0, privateFixture=work.relative_to(ROOT).as_posix(), controls=controls,
             originalFunctionMembershipUnchanged=True, originalMetadataRegistryAndPolicyUnchanged=True,
             newTypedDataObjects=9, newTypedDataBytes=4314, generatorSha256=sha256(__file__),
             composerSha256=sha256(ROOT / 'compose_sdk_integer_groups_20261106.py')))
    print(dict(passed=True, controls=len(controls), initializedDataBytes=4314, sourceCredit=0))


if __name__ == '__main__':
    main()
