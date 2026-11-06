from project import ROOT, configuration, read_json, sha256, write_json
from source_selection import POLICY, preferences


def main():
    namespace = configuration()['romSha256']
    policies = preferences(namespace)
    ledger = read_json(ROOT / 'source-map.json')
    if ledger['buildSha256'] != namespace:
        raise ValueError('Preferred-source linked ledger build differs')
    records = {(row['module'], row['mode'], int(row['address'], 0)): row for row in ledger['matchedFunctions']}
    units = read_json(ROOT / 'build/link-work/source-units.json')['units']
    results = []
    for key, policy in policies.items():
        row = records.get(key)
        if row is None or row['sourceUnit'] != policy['source'] or row['sourceSha256'] != policy['sourceSha256']:
            raise ValueError('Linked ledger does not select the preferred source')
        if not row['states']['moduleLinked'] or (row.get('sourceSelection') or {}).get('evidenceSha256') != policy['evidenceSha256']:
            raise ValueError('Preferred source has no current linked provenance')
        selected = [unit for unit in units if unit['module'] == key[0] and int(unit['start'], 0) == key[2]
                    and int(unit['end'], 0) == key[2] + policy['bytes']]
        if len(selected) != 1:
            raise ValueError('Preferred source has no unique actual module input')
        unit = selected[0]
        if unit['source'] != policy['source'] or unit['sourceSha256'] != policy['sourceSha256'] or unit['sha256'] != row['objectSha256'] or unit.get('sourceReport') != policy['report']:
            raise ValueError('Actual module input differs from preferred source')
        if sha256(ROOT / unit['object']) != unit['sha256'] or unit['targetSha256'] != policy['targetSha256']:
            raise ValueError('Preferred module object/native hash differs')
        results.append({'module': key[0], 'mode': key[1], 'address': hex(key[2]),
                        'source': policy['source'], 'objectSha256': unit['sha256'], 'newByteCredit': 0})
    report = {'passed': True, 'romSha256': namespace, 'preferredInputs': results,
              'sourcePreferenceSha256': sha256(POLICY), 'sourceMapSha256': sha256(ROOT / 'source-map.json'),
              'sourceUnitsSha256': sha256(ROOT / 'build/link-work/source-units.json'),
              'actualLinkedSourceProvenanceChecked': True, 'newSourceBytes': 0}
    write_json(ROOT / 'evidence/verification/linked-source-preferences-20261030.json', report)
    print(report)


if __name__ == '__main__':
    main()
