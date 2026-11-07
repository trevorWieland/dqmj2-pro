import argparse
import ast
import copy
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--letter', required=True)
    parser.add_argument('--previous-letter', required=True)
    parser.add_argument('--ready', required=True)
    parser.add_argument('--sha256', required=True)
    parser.add_argument('--packet-id', required=True)
    parser.add_argument('--owner', required=True)
    parser.add_argument('--admission', required=True)
    parser.add_argument('--classification')
    parser.add_argument('--classification-sha256')
    options = parser.parse_args(); cohort = options.cohort
    unchanged = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json',
        'evidence/lanes/parallel-wave20261102/dispatch.json']}
    assert cohort >= 171 and len(options.letter) == len(options.previous_letter) == 1
    assert options.letter.isascii() and options.letter.islower() and ord(options.letter) == ord(options.previous_letter) + 1
    cfg_name = f'provenance/parallel-wave20261105-{options.letter}-packets.json'
    prior_cfg_name = f'provenance/parallel-wave20261105-{options.previous_letter}-packets.json'
    prior = read_json(ROOT / prior_cfg_name)
    assert prior['cohort'] == cohort - 1 and prior['membershipFrozen'] and not (ROOT / cfg_name).exists()
    ready_path = (ROOT / options.ready).resolve()
    assert ready_path.is_relative_to(ROOT) and ready_path.name == 'ready.json' and sha256(ready_path) == options.sha256
    ready = read_json(ready_path); admission = read_json(ROOT / options.admission)
    assert admission['passed'] and admission['sourceCredit'] == 0
    assert sha256(ROOT / admission['claim']) == admission['claimSha256']
    claim = read_json(ROOT / admission['claim'])
    assert claim['status'] == 'coordinator-admitted-source-scope-no-credit'
    def identity(row):
        return row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0), row['bytes']
    owned = {identity(row) for row in claim['claimedFunctions']}
    assert ready['functions'] == len(ready['identities']) > 0 and sum(row['bytes'] for row in ready['identities']) == ready['bytes']
    assert all(identity(row) in owned and row['source'].startswith(claim['exclusiveSourceRoot'] + '/') for row in ready['identities'])
    mandatory = {}
    descriptor = ready['canonicalDescriptor']; assert sha256(ROOT / descriptor['path']) == descriptor['sha256']
    for pin in read_json(ROOT / descriptor['path'])['frozenInputs']:
        assert sha256(ROOT / pin['path']) == pin['sha256']; mandatory[pin['path']] = pin['sha256']
        value = read_json(ROOT / pin['path']) if pin['path'].endswith('.json') else None
        for item in value.get('files', []) if isinstance(value, dict) else []:
            assert item['path'] not in mandatory or mandatory[item['path']] == item['sha256']
            assert sha256(ROOT / item['path']) == item['sha256']; mandatory[item['path']] = item['sha256']
    mandatory.update({options.ready: options.sha256, descriptor['path']: descriptor['sha256'],
        options.admission: sha256(ROOT / options.admission), admission['claim']: admission['claimSha256']})
    opaque = {}
    if options.classification:
        assert options.classification_sha256 and sha256(ROOT / options.classification) == options.classification_sha256
        classification = read_json(ROOT / options.classification); assert classification['sourceCredit'] == 0
        keys = [key for key in ['sourceExpansionOpaque', 'opaqueTraceFiles'] if key in classification]
        assert len(keys) == 1
        opaque = {pin['path']: pin['sha256'] for pin in classification[keys[0]]}
        assert all(path.endswith(('.json', '.txt', '.md', '.csv')) for path in opaque)
        assert not opaque.keys() & mandatory.keys()
        assert all(sha256(ROOT / name) == digest for name, digest in opaque.items())
    stage_name = f'stage_parallel_packet_wave{cohort}_v2_20261106.py'
    package_name = f'cohort{cohort}-parallel-wave20261105-{options.letter}-package.json'
    old_stage = (ROOT / prior['stage']).read_text(encoding='utf-8')
    stage = old_stage.replace(prior['name'] + '-package.json', package_name).replace(
        f"['cohort'] == {cohort - 1}", f"['cohort'] == {cohort}")
    assert ast.dump(ast.parse(stage.replace(package_name, prior['name'] + '-package.json').replace(
        f"['cohort'] == {cohort}", f"['cohort'] == {cohort - 1}"))) == ast.dump(ast.parse(old_stage))
    assert not (ROOT / stage_name).exists(); (ROOT / stage_name).write_text(stage, encoding='utf-8')
    cfg = copy.deepcopy(prior)
    for key in ['frozenOrdinaryMembership', 'pendingInitializedDataReady', 'composedInitializedDataReady',
                'composedInitializedDataReadys', 'qualifiedDataPreparer']:
        cfg.pop(key, None)
    name = f'cohort{cohort}-parallel-wave20261105-{options.letter}'
    spec_name = name + '-specification.json'
    cfg.update(cohort=cohort, previousAcceptedCohort=cohort - 1, name=name,
        readyPackets=[options.ready], packetIds={options.ready: options.packet_id}, membershipFrozen=False,
        stage=stage_name, document=f'docs/2026-11-06-parallel-wave-{options.letter}-acceptance.md',
        reservedSpecifications=list(dict.fromkeys([*prior['reservedSpecifications'], prior['name'] + '-specification.json'])),
        postSealCommands=[['qualify_mixed_arm9_reference_context_v5_20261106.py', spec_name, '--register']],
        packetBridges={}, additionalFrozenInputs={})
    cfg['opaqueMetadata'] = sorted((set(cfg['opaqueMetadata']) | opaque.keys()) - mandatory.keys())
    receipt = f'evidence/verification/cohort{cohort}-initial-admitted-function-queue-v1-20261106.json'
    extras = [stage_name, receipt, 'bootstrap_next_admitted_function_queue_v3_20261106.py', options.admission, admission['claim']]
    if options.classification:
        extras.append(options.classification)
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], *extras]))
    write_json(ROOT / cfg_name, cfg)
    result = dict(passed=False, state='awaiting-original-intake', sourceCredit=0, previousFrozenCohort=cohort - 1,
        functions=ready['functions'], bytes=ready['bytes'], firstReady=dict(path=options.ready, sha256=options.sha256),
        actualImmutableInputMembersVerified=len(mandatory), onlyUnselectedMetadataOpaque=opaque,
        thinStageOnlyPackageAndCohortLiteralsChanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / receipt, result)
    command = [sys.executable, str(ROOT / 'intake_deferred_admitted_packet_v2_20261106.py'), cfg_name,
        '--admission', options.admission, '--ready', options.ready, '--sha256', options.sha256,
        '--packet-id', options.packet_id, '--owner', options.owner]
    subprocess.run(command, cwd=ROOT, check=True)
    assert unchanged == {name: sha256(ROOT / name) for name in unchanged}
    result.update(passed=True, state='admitted-and-prepared-disjoint-queue',
        sharedSourceRegistryPreferencesAndCapturedDispatchUnchanged=unchanged, originalIntakeAndAllNativeGuardsCompleted=True)
    write_json(ROOT / receipt, result)


if __name__ == '__main__':
    main()
