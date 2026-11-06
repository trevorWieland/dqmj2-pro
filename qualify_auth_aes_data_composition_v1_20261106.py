import copy
from project import ROOT, read_json, write_json, sha256, configuration
from ledger_state import collect_matches
from qualify_sdk_constant_data_additions_20261106 import selected_data
from qualify_auth_aes_data_additions_v1_20261106 import identity, partition, qualify


def main():
    pins = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json']}
    before = selected_data()
    functions, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected and len(before) == 346 and len(functions) == 11339
    after = dict(before)
    expected = []
    for name in ['evidence/matches/auth-character-data-20261106.json', 'evidence/matches/aes-table-data-20261106.json']:
        report = read_json(ROOT / name)
        for row in report['dataMatches']:
            item = {**report, **row, 'evidence': name}
            key = identity(item)
            assert key not in after
            after[key] = item
            expected.append({key: row[key] for key in ['program', 'processor', 'module', 'mode', 'kind', 'address', 'bytes']})
    assert len(after) == 458
    proof = qualify(before, after, expected, functions, ROOT / 'work/integration/cohort169-auth-aes-combined-qualification-v1')
    cases = []
    for field, value in [('program', 'other/child.srl'), ('processor', 'arm7'), ('module', 'ov000'),
                         ('kind', 'function'), ('address', '0x022088bc'), ('bytes', 1020)]:
        candidate = copy.deepcopy(expected); candidate[-1][field] = value
        cases.append(('wrong-' + field, before, after, candidate))
    cases.append(('duplicate-expected', before, after, [*expected, expected[-1]]))
    cases.append(('missing-expected', before, after, expected[:-1]))
    added = set(after) - set(before)
    missing = dict(after); missing.pop(next(iter(added)))
    cases.append(('missing-new-row', before, missing, expected))
    extra = dict(after); key = next(iter(added)); extra[(*key[:4], 0x02ffff00)] = extra[key]
    cases.append(('extra-new-row', before, extra, expected))
    dropped = dict(after); dropped.pop(next(iter(before)))
    cases.append(('dropped-prior-data', before, dropped, expected))
    changed = copy.deepcopy(after); changed[next(iter(before))]['targetSha256'] = '0' * 64
    cases.append(('changed-prior-data', before, changed, expected))
    changed = copy.deepcopy(after); changed[next(iter(added))]['bytes'] -= 4
    cases.append(('changed-new-extent', before, changed, expected))
    rejected_cases = []
    for label, earlier, later, wanted in cases:
        try:
            partition(earlier, later, wanted)
        except (AssertionError, KeyError):
            rejected_cases.append(label)
        else:
            raise AssertionError(label)
    assert all(sha256(ROOT / name) == digest for name, digest in pins.items())
    write_json(ROOT / 'evidence/verification/cohort169-auth-aes-data-composition-qualification-v1-20261106.json',
        dict(passed=True, sourceCredit=0, actualPriorData=346, projectedData=458,
            originalEarlierFunctionsUnchanged=11339, actualOriginalAuthAndAesQualifiers=proof,
            rejectedGroupingControls=rejected_cases, noRegistryOrPreferencesMutation=True,
            actualRegistryAndPreferencePins=pins, generatorSha256=sha256(__file__)))
    print(dict(passed=True, freshObjects=112, initializedCandidateBytes=11671, groupingNegatives=len(rejected_cases), sourceCredit=0))


if __name__ == '__main__':
    main()
