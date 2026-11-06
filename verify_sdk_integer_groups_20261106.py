from project import ROOT, read_json, write_json, configuration, sha256
from ledger_state import collect_matches
from qualify_sdk_integer_groups_20261106 import qualify, selected_data, identity


def main():
    reports = ['evidence/matches/sdk-constant-data-canonical-20261106.json',
               'evidence/matches/sdk-sound-data-canonical-20261106.json']
    protected = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json']}
    before = selected_data()
    after, expected = dict(before), []
    for name in reports:
        report = read_json(ROOT / name)
        assert report['functionMatched'] == 0
        for row in report['dataMatches']:
            key = identity(row)
            assert key not in after
            after[key] = dict(report, **row)
            expected.append(row)
    controls = []
    for label, changed in [('missing-group', expected[:3]),
                            ('duplicate-identity', expected[:-1] + [expected[0]]),
                            ('changed-group-extent', [dict(expected[0], bytes=expected[0]['bytes'] + 1)] + expected[1:])]:
        try:
            qualify(before, after, changed, {}, ROOT / 'work/integration/sdk-integer-groups-controls' / label)
        except AssertionError:
            controls.append(dict(control=label, rejected=True))
        else:
            raise AssertionError('Invalid data group union admitted')
    functions, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    proof = qualify(before, after, expected, functions, ROOT / 'work/integration/sdk-integer-groups-positive')
    assert protected == {name: sha256(ROOT / name) for name in protected}
    write_json(ROOT / 'evidence/verification/sdk-integer-groups-accounting-preflight-20261106.json',
        dict(passed=True, sourceCredit=0, controls=controls, positiveQualification=proof,
             reports=[dict(path=name, sha256=sha256(ROOT / name)) for name in reports],
             registryAndPolicyUnchanged=True, actualEarlierDataRows=len(before), actualFunctionRows=len(functions),
             generatorSha256=sha256(__file__), qualifierSha256=sha256(ROOT / 'qualify_sdk_integer_groups_20261106.py')))
    print(dict(passed=True, controls=len(controls), initializedDataObjects=9, initializedDataBytes=4314, sourceCredit=0))


if __name__ == '__main__':
    main()
