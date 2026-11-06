import copy
from project import ROOT, read_json, write_json, sha256


def main():
    name = 'provenance/parallel-wave20261105-o-packets.json'
    assert not (ROOT / name).exists()
    cfg = copy.deepcopy(read_json(ROOT / 'provenance/parallel-wave20261105-n-packets.json'))
    ready_name = 'evidence/lanes/parallel-wave20261106/ov006-md5-next/ready.json'
    assert sha256(ROOT / ready_name) == 'c10264ece8c35ccd42a94bbe2f67d73c554ce736e4f3eaddd1de62abad65f541'
    classification_name = 'evidence/lanes/parallel-wave20261106/ov006-md5-next/diagnostic-classification-v1.json'
    assert sha256(ROOT / classification_name) == '52f1d202e3489e7be4b2b41a968a66e40013a2acbaf611419d38dcca67e649c7'
    classification = read_json(ROOT / classification_name)
    opaque = {pin['path']: pin['sha256'] for pin in classification['sourceExpansionOpaque']}
    mandatory = {pin['path']: pin['sha256'] for pin in classification['mandatoryParsed']}
    ready = read_json(ROOT / ready_name)
    for manifest in read_json(ROOT / ready['canonicalDescriptor']['path'])['frozenInputs']:
        mandatory[manifest['path']] = manifest['sha256']
        for pin in read_json(ROOT / manifest['path'])['files']:
            if pin['path'].endswith('.json'):
                assert pin['path'] not in opaque
                mandatory[pin['path']] = pin['sha256']
    assert len(opaque) == 4 and not opaque.keys() & mandatory.keys()
    assert all(sha256(ROOT / path) == digest for path, digest in {**opaque, **mandatory}.items())
    stage_name = 'stage_parallel_packet_wave170_v2_20261106.py'
    stage = (ROOT / 'stage_parallel_packet_wave169_v2_20261106.py').read_text(encoding='utf-8')
    stage = stage.replace('cohort169-parallel-wave20261105-n-package.json', 'cohort170-parallel-wave20261105-o-package.json').replace("['cohort'] == 169", "['cohort'] == 170")
    assert not (ROOT / stage_name).exists()
    (ROOT / stage_name).write_text(stage, encoding='utf-8')
    for key in ['frozenOrdinaryMembership', 'pendingInitializedDataReady', 'composedInitializedDataReady',
                'composedInitializedDataReadys', 'qualifiedDataPreparer']:
        cfg.pop(key, None)
    cfg.update(cohort=170, previousAcceptedCohort=169, name='cohort170-parallel-wave20261105-o',
        readyPackets=[ready_name], packetIds={ready_name: 'ov006-md5-first'}, membershipFrozen=False,
        stage=stage_name, document='docs/2026-11-06-parallel-wave-o-acceptance.md',
        reservedSpecifications=[*cfg['reservedSpecifications'], 'cohort169-parallel-wave20261105-n-specification.json'],
        postSealCommands=[['qualify_mixed_arm9_reference_context_v3_20261106.py',
            'cohort170-parallel-wave20261105-o-specification.json', '--register']],
        packetBridges={}, additionalFrozenInputs={})
    cfg['opaqueMetadata'] = sorted((set(cfg['opaqueMetadata']) | opaque.keys()) - mandatory.keys())
    receipt = 'evidence/verification/cohort170-initial-disjoint-queue-20261106.json'
    cfg['extra'] = list(dict.fromkeys([*cfg['extra'], stage_name, classification_name,
        'bootstrap_cohort170_disjoint_queue_20261106.py', 'admit_ov006_md5_resumption_v1_20261106.py',
        'evidence/lanes/parallel-wave20261106/ov006-md5-next/coordinator-admission.json',
        'evidence/lanes/parallel-wave20261106/ov006-md5-next/claim.json', receipt]))
    write_json(ROOT / name, cfg)
    write_json(ROOT / receipt, dict(passed=True, sourceCredit=0, ordinaryMembershipFrozen=False,
        firstReady=dict(path=ready_name, sha256=sha256(ROOT / ready_name)), functions=3, bytes=2322,
        opaqueOnlyFourUnselectedPresealDiagnostics=opaque, allActualRuntimeInputsFullyParsed=mandatory,
        priorCohort169Reserved=True, noSharedPreparationStarted=True, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
