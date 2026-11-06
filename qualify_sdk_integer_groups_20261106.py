from project import ROOT, read_json
from qualify_sdk_constant_data_additions_20261106 import selected_data, identity, qualify as constants
from qualify_sdk_sound_data_additions_20261106 import qualify as sound


def qualify(before, after, expected, functions, directory):
    groups = [
        ('constants', 'evidence/lanes/parallel-wave20261106/sdk-constant-data/data-claim.json', constants, 3, 562),
        ('sound', 'evidence/lanes/parallel-wave20261106/sdk-sound-data/data-claim.json', sound, 6, 3752)]
    assert len(expected) == 9 and len({identity(row) for row in expected}) == 9
    wanted = {identity(row): row for row in expected}
    assert set(after) - set(before) == set(wanted) and sum(row['bytes'] for row in expected) == 4314
    results, observed = [], set()
    occupied = []
    for row in expected:
        key = identity(row)
        span = key[:3], key[4], key[4] + row['bytes']
        assert not any(span[0] == old[0] and max(span[1], old[1]) < min(span[2], old[2]) for old in occupied)
        occupied.append(span)
    for label, claim_name, checker, objects, initialized in groups:
        claim = read_json(ROOT / claim_name)
        keys = {identity(row) for row in claim['claimedStorage']}
        assert len(keys) == objects and not keys & observed and keys <= set(wanted)
        subset = {key: row for key, row in after.items() if key in before or key in keys}
        rows = [row for row in expected if identity(row) in keys]
        proof = checker(before, subset, rows, functions, directory / label)
        assert proof['passed'] and proof['newInitializedDataObjects'] == objects
        assert proof['newInitializedDataBytes'] == proof['newTypedConstantDataBytes'] == initialized
        results.append(dict(group=label, qualification=proof))
        observed.update(keys)
    assert observed == set(wanted)
    return dict(passed=True, newInitializedDataObjects=9, newInitializedDataBytes=4314, newTypedConstantDataBytes=4314,
                newEncodedAssetBytes=0, newDataAlignmentBytes=0, newSourceFunctions=0,
                earlierDataPreserved=len(before), groups=results, sourceCreditPendingSharedAcceptance=True)
