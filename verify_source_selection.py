import copy
from unittest.mock import patch
from project import ROOT, configuration, read_json, sha256, write_json
import source_selection as selection
from ledger_state import collect_matches
from recovery_registry import batches


def main():
    namespace = configuration()['romSha256']
    document = read_json(selection.POLICY)
    policies = selection.preferences(namespace)
    key = ('main', 'arm', 0x02065DEC)
    policy = policies[key]
    audit = read_json(ROOT / policy['evidence'])
    controls = []
    selected_sources = []
    for identity, preference in policies.items():
        current_audit = read_json(ROOT / preference['evidence'])
        wanted = {current_audit['previous']['report'], current_audit['preferred']['report']}
        selected_batches = [row for row in batches() if row['report'] in wanted]
        if len(selected_batches) != 2:
            raise ValueError('Migration requires both retained registered implementations')
        for order in (selected_batches, list(reversed(selected_batches))):
            with patch('recovery_registry.batches', return_value=order):
                matches, rejected = collect_matches(namespace)
            current = matches[identity]
            assert selection.preferred(current, preference) and current['size'] == preference['bytes']
            assert any(row['source'] == current_audit['previous']['source'] for row in current['alternativeImplementations'])
            controls.append({'name': 'report-order-' + str(len(controls)), 'source': current['source'], 'passed': True})
        selected_sources.append(current['source'])
        if identity == key:
            unit = current
    work = ROOT / 'work/source-selection-negatives'
    work.mkdir(parents=True, exist_ok=True)

    def reject(name, mutate, reason):
        changed = copy.deepcopy(document)
        mutate(changed)
        path = work / 'policy.json'
        write_json(path, changed)
        try:
            selection.preferences(namespace, path)
        except ValueError as error:
            if reason not in str(error):
                raise AssertionError((name, str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            return
        raise AssertionError('Invalid source preference accepted: ' + name)

    reject('wrong-build', lambda r: r.update(romSha256='0' * 64), 'namespace differs')
    reject('duplicate-identity', lambda r: r['preferences'].append(copy.deepcopy(r['preferences'][0])), 'Duplicate')
    reject('changed-evidence', lambda r: r['preferences'][0].update(evidenceSha256='0' * 64), 'evidence changed')
    reject('wrong-source-hash', lambda r: r['preferences'][0].update(sourceSha256='0' * 64), 'identity differs')
    reject('wrong-target-hash', lambda r: r['preferences'][0].update(targetSha256='0' * 64), 'identity differs')
    reject('wrong-processor', lambda r: r['preferences'][0].update(processor='arm7'), 'processor/mode/alignment')
    reject('misaligned-arm', lambda r: r['preferences'][0].update(address='0x02065dee'), 'processor/mode/alignment')
    reject('escaping-evidence', lambda r: r['preferences'][0].update(evidence='../outside.json'), 'escapes')
    changed_audit = copy.deepcopy(audit)
    changed_audit['newByteCredit'] = 40
    evidence_path = work / 'inflated-audit.json'
    write_json(evidence_path, changed_audit)
    reject('inflated-migration-credit', lambda r: r['preferences'][0].update(
        evidence=evidence_path.relative_to(ROOT).as_posix(), evidenceSha256=sha256(evidence_path)), 'scope differs')
    stale = {**unit, **audit['previous']}
    available, rejected = {key: stale}, []
    selection.enforce(available, rejected, {key: policy})
    assert key not in available and rejected[0]['historicalVariantFallbackAllowed'] is False
    controls.append({'name': 'missing-fresh-preferred-has-no-historical-fallback', 'passed': True})
    try:
        selection.enforce({key: {**unit, 'size': 44}}, [], policies)
    except ValueError as error:
        assert 'native span differs' in str(error)
        controls.append({'name': 'wrong-native-extent', 'rejected': True})
    else:
        raise AssertionError('Wrong preferred native extent accepted')
    assert sha256(ROOT / audit['previous']['source']) == audit['previous']['sourceSha256']
    result = {'passed': True, 'controls': controls, 'selectedSource': unit['source'],
              'historicalSourceRetained': audit['previous']['source'], 'sourceBytesReplaced': sum(row['bytes'] for row in policies.values()),
              'selectedSources': selected_sources,
              'newSourceFunctions': 0, 'newSourceBytes': 0, 'reportOrderIndependent': True}
    write_json(ROOT / 'evidence/verification/source-selection-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, 'controls', len(controls))


if __name__ == '__main__':
    main()
