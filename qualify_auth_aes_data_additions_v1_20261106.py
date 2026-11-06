from project import ROOT, read_json, sha256
from qualify_child_message_data_additions_20261106 import identity
import wave20261106_auth_character_data_additions as auth
import wave20261106_aes_table_data_additions as aes


PINS = {
    'wave20261106_auth_character_data_additions.py': '6e97016dd0c80f3ec6970bfb77f9c6571e1b96ea2b32ad7e1b809bd5f55e9026',
    'wave20261106_aes_table_data_additions.py': 'd85abed3fac30e279ab2906c279605d66712a0b0cb53f55c1327eb94e76d0516',
    'evidence/lanes/parallel-wave20261106/auth-character-data/data-claim.json': '02be137cee4d5da3d0311cd4c62335d1192d29f1ed1fd672d481eb892b001ed4',
    'evidence/lanes/parallel-wave20261106/aes-table-data/data-claim.json': '366bfb04f9d8b3e92ae1e2d54b90c3699d13fb57d57654d4e596cb71803a2694'
}


def partition(before, after, expected):
    for name, digest in PINS.items():
        assert sha256(ROOT / name) == digest
    auth_claim = read_json(ROOT / 'evidence/lanes/parallel-wave20261106/auth-character-data/data-claim.json')['claimedStorage']
    aes_claim = read_json(ROOT / 'evidence/lanes/parallel-wave20261106/aes-table-data/data-claim.json')['claimedStorage']
    scopes = [{identity(row): row['bytes'] for row in rows} for rows in [auth_claim, aes_claim]]
    assert len(scopes[0]) == 102 and sum(scopes[0].values()) == 1431
    assert len(scopes[1]) == 10 and sum(scopes[1].values()) == 10240
    assert not set(scopes[0]) & set(scopes[1])
    wanted = {identity(row): row['bytes'] for row in expected}
    assert len(wanted) == len(expected) == 112 and wanted == {**scopes[0], **scopes[1]}
    added = set(after) - set(before)
    assert added == set(wanted) and set(before) <= set(after)
    assert all(after[key] == value for key, value in before.items())
    assert all(after[key]['bytes'] == wanted[key] for key in added)
    intermediate = {key: value for key, value in after.items() if key not in scopes[1]}
    assert set(intermediate) == set(before) | set(scopes[0])
    assert set(after) - set(intermediate) == set(scopes[1])
    return intermediate, [[row for row in expected if identity(row) in scope] for scope in scopes]


def qualify(before, after, expected, functions, directory):
    intermediate, groups = partition(before, after, expected)
    results = [auth.qualify(before, intermediate, groups[0], functions, directory / 'auth'),
               aes.qualify(intermediate, after, groups[1], functions, directory / 'aes')]
    assert all(result['passed'] for result in results)
    sums = {name: sum(result[name] for result in results) for name in
        ['newInitializedDataObjects', 'newInitializedDataBytes', 'newEncodedAssetBytes', 'newDataAlignmentBytes', 'newTypedConstantDataBytes']}
    assert sums == dict(newInitializedDataObjects=112, newInitializedDataBytes=11671,
        newEncodedAssetBytes=0, newDataAlignmentBytes=0, newTypedConstantDataBytes=11671)
    return dict(passed=True, **sums, sourceCredit=0, newSourceFunctions=0,
        earlierDataPreserved=len(before), allEarlierRowsPreservedExactly=True,
        exactLosslessActualRowPartition=True, noRegistryOrExpectedDataMutation=True,
        independentOriginalQualifiersUnchanged=True, groups=results,
        qualifierPins=PINS, generatorSha256=sha256(__file__))
