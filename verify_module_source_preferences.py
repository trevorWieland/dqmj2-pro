import copy
from project import ROOT, configuration, read_json, write_json
from recovery_registry import entries
from source_selection import preferences
from source_variants import consolidate


def unit(version, identity):
    report = read_json(ROOT / version['report'])
    row = next(row for row in entries(report) if row.get('source', report.get('source')) == version['source']
               and int(row['address'], 0) == int(identity['address'], 0))
    start = int(identity['address'], 0)
    return {'module': identity['module'], 'processor': identity['processor'], 'mode': identity['mode'],
            'section': '.text', 'kind': 'function', 'start': hex(start), 'end': hex(start + identity['bytes']),
            'source': version['source'], 'sourceSha256': version['sourceSha256'], 'sourceReport': version['report'],
            'targetSha256': row['targetSha256'], 'object': row.get('object', report.get('object')),
            'sha256': row.get('objectSha256', report.get('objectSha256'))}


def main():
    policies = preferences(configuration()['romSha256'])
    controls = []
    for key, policy in policies.items():
        audit = read_json(ROOT / policy['evidence'])
        old, new = unit(audit['previous'], policy), unit(audit['preferred'], policy)
        for order in [[old, new], [new, old]]:
            result = consolidate(copy.deepcopy(order), {key: policy})
            assert len(result) == 1 and result[0]['source'] == policy['source']
            assert any(row['source'] == old['source'] for row in result[0]['equivalentUnlinkedImplementations'])
            controls.append({'module': key[0], 'address': hex(key[2]), 'preferredSelected': True})
    key = ('ov005', 'arm', 0x021E08B8)
    policy = policies[key]
    audit = read_json(ROOT / policy['evidence'])
    old, new = unit(audit['previous'], policy), unit(audit['preferred'], policy)

    def reject(name, candidates):
        try:
            consolidate(candidates, {key: policy})
        except ValueError as error:
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            return
        raise AssertionError('Bad module source selection accepted: ' + name)

    reject('preferred-absent-no-old-fallback', [copy.deepcopy(old)])
    for name, field, value in [('wrong-report', 'sourceReport', 'wrong.json'),
                               ('wrong-body', 'targetSha256', '0' * 64),
                               ('stale-source', 'sourceSha256', '0' * 64),
                               ('stale-object', 'sha256', '0' * 64),
                               ('wrong-mode', 'mode', 'thumb'),
                               ('wrong-processor', 'processor', 'arm7'),
                               ('wrong-extent', 'end', hex(int(new['end'], 0) + 4))]:
        changed = copy.deepcopy(new)
        changed[field] = value
        reject(name, [copy.deepcopy(old), changed])
    result = {'passed': True, 'controls': controls, 'preferredSources': len(policies),
              'sourceSelectionOrderIndependent': True, 'newSourceCredit': 0}
    write_json(ROOT / 'evidence/verification/module-source-preference-controls-20261030.json', result)
    print({'passed': True, 'preferredSources': len(policies), 'controls': len(controls)}, flush=True)


if __name__ == '__main__':
    main()
