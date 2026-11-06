import copy
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import recovery_registry as registry
import integrate
import link_utility
from replay_sdk_data_namespace_v3_20261106 import project


def main():
    names = read_json(ROOT / 'work/integration/cohort166-sdk-namespace-v3-descriptors.json')
    assert len(names) == 4
    descriptors = [read_json(ROOT / name) for name in names]
    reports = [read_json(ROOT / d['output']) for d in descriptors]
    originals = {d['originalReport']: read_json(ROOT / d['originalReport']) for d in descriptors}
    key = lambda row: (row['program'], row['processor'], row['module'], row['address'])
    before = {key(r): r for report in originals.values() for r in report['dataMatches']}
    after = {key(r): r for report in reports for r in report['dataMatches']}
    assert before == after and len(after) == 9
    assert sum(r['bytes'] for r in after.values()) == 4314
    baseline = sha256(ROOT / 'recovery.json')
    private = ROOT / 'work/integration/cohort166-sdk-namespace-v3-private-registry.json'
    document = read_json(ROOT / 'recovery.json')
    old_reports = set(originals)
    assert len([b for b in document['batches'] if b['report'] in old_reports]) == 2
    document['batches'] = [b for b in document['batches'] if b['report'] not in old_reports]
    write_json(private, document)
    with patch.object(registry, 'REGISTRY', private):
        for name, descriptor in zip(names, descriptors):
            registry.register(descriptor['output'], ['replay_sdk_data_namespace_v3_20261106.py', name])
        arm9 = {p.relative_to(ROOT).as_posix() for p in integrate.match_reports()}
        embedded, metadata = link_utility.accepted_by_cpu('dwc/utility.bin/move/child.srl', ['arm9', 'arm7'])
    assert sha256(ROOT / 'recovery.json') == baseline
    own = {d['output'] for d in descriptors}
    expected_host = {d['output'] for d in descriptors if not d['namespace']['program']}
    assert arm9 & own == expected_host and len(expected_host) == 2
    selected_embedded = {key(r): r for cpu, plan in embedded.items() for r in plan[0] if key(r) in after}
    wanted_embedded = {k: r for k, r in after.items() if r['program']}
    assert selected_embedded == {k: {**next(report for report in reports if r in report['dataMatches']), **r}
                                 for k, r in wanted_embedded.items()}
    assert len(selected_embedded) == 3 and sum(r['bytes'] for r in selected_embedded.values()) == 1220
    controls = []
    base = descriptors[0]
    original = originals[base['originalReport']]
    variants = [('wrong-program', lambda d: d['namespace'].update(program='wrong')),
                ('wrong-processor', lambda d: d['namespace'].update(processor='arm7')),
                ('wrong-module', lambda d: d['namespace'].update(module='wrong')),
                ('wrong-object-count', lambda d: d.update(objects=d['objects'] + 1)),
                ('wrong-byte-count', lambda d: d.update(initializedBytes=d['initializedBytes'] + 1))]
    for label, change in variants:
        descriptor = copy.deepcopy(base)
        change(descriptor)
        try:
            project(original, descriptor)
        except AssertionError:
            controls.append(dict(case=label, rejected=True))
        else:
            raise AssertionError('Namespace control passed: ' + label)
    for label in ['function-credit', 'unqualified-data']:
        bad = copy.deepcopy(original)
        if label == 'function-credit':
            bad['functionMatched'] = 1
        else:
            bad['dataMatches'][0]['exactBytes'] = False
        try:
            project(bad, base)
        except AssertionError:
            controls.append(dict(case=label, rejected=True))
        else:
            raise AssertionError('Namespace control passed: ' + label)
    receipt = dict(passed=True, sourceCredit=0, objects=9, initializedBytes=4314,
        wholeOriginalRowsUnchanged=True, hostObjects=6, embeddedObjects=3,
        embeddedInitializedBytes=1220, originalIntegrateAndUtilityRoutingVerified=True,
        productionRegistryUnchanged=True, negativeControls=controls,
        generatorSha256=sha256(ROOT / 'qualify_sdk_data_namespace_v3_20261106.py'),
        transportSha256=sha256(ROOT / 'replay_sdk_data_namespace_v3_20261106.py'),
        descriptors=[dict(path=n, sha256=sha256(ROOT / n)) for n in names],
        limitations=['Private routing qualification; complete shared build and module checks remain mandatory'])
    write_json(ROOT / 'evidence/verification/sdk-data-namespace-v3-qualification-20261106.json', receipt)
    print(dict(passed=True, objects=9, initializedBytes=4314, namespaceNegativeControls=len(controls)))


if __name__ == '__main__':
    main()
