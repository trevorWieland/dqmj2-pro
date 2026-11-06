import hashlib
import os
from project import ROOT, read_json, sha256, configuration, native_dependencies
from source_dependencies import dependencies_current, dependency_hashes
from qualify_child_message_data_additions_20261106 import selected_data, identity, FIELDS


def qualify(before, after, expected, functions, directory):
    config = configuration()
    native_dependencies(config)
    from sdk_constant_data_codec_20261106 import render, validate_layout
    from match_sdk_constant_data_20261106 import LAYOUT, link
    from match_child_message_data_20261106 import inspect_object, COMPILER, COMPILER_HASH, LINKER, LINKER_HASH
    claim_name = 'evidence/lanes/parallel-wave20261106/sdk-constant-data/data-claim.json'
    assert sha256(ROOT / claim_name) == 'eb8ac464861a504fc5d190da497bb6d8f918ce1de7ce1473db743b55796f6283'
    claim = read_json(ROOT / claim_name)
    admitted = {identity(row): row for row in claim['claimedStorage']}
    wanted = {identity(row): row['bytes'] for row in expected}
    added = set(after) - set(before)
    assert all(identity(row) == key for key, row in after.items())
    assert len(expected) == len(wanted) == 3 and added == set(wanted) == set(admitted)
    assert sum(wanted.values()) == 562 and wanted == {key: row['bytes'] for key, row in admitted.items()}
    for key, row in before.items():
        assert key in after and all(after[key].get(field) == row.get(field) for field in FIELDS)
    layout = read_json(ROOT / LAYOUT)
    validate_layout(layout)
    assets = {identity(row): row for row in layout['assets']}
    assert set(assets) == added
    occupied = []
    for row in before.values():
        key = identity(row)
        occupied.append((key[:3], key[4], key[4] + row.get('bytes', row.get('size'))))
    for row in functions.values():
        key = identity(dict(row, kind='data'))
        occupied.append((key[:3], key[4], key[4] + row['size']))
    assert sha256(COMPILER) == COMPILER_HASH and sha256(LINKER) == LINKER_HASH
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    proofs = []
    for key in sorted(added):
        row, asset = after[key], assets[key]
        assert row['kind'] == row['mode'] == 'data'
        assert row['ordinaryFunctionCredit'] == row['executableSectionBytes'] == row['allocatedZeroFillBytes'] == 0
        assert row['relocations'] == [] and row['sourceLanguage'] == 'C'
        flags = ['-O2', '-proc', asset['compilerProcessor'], '-sym', 'on', '-nolink', '-lang', 'c99']
        assert row['compilerFlags'] == flags and row['compilerSha256'] == COMPILER_HASH
        assert row['compiler'] == COMPILER.relative_to(ROOT).as_posix()
        assert dependencies_current(row)
        assert asset['semanticSource'] == admitted[key]['semanticSource']
        assert sha256(ROOT / asset['semanticSource']) == asset['semanticSourceSha256'] == admitted[key]['semanticSourceSha256']
        assert dependency_hashes(row) == {name: sha256(ROOT / name) for name in [LAYOUT, asset['semanticSource']]}
        code, payload = render(read_json(ROOT / asset['semanticSource']), asset['nativeSymbol'])
        assert row['source'] == f'generated/sdk-constant-data/{key[2]}-{key[4]:08x}.c'
        assert (ROOT / row['source']).read_text() == code
        assert row['bytes'] == row['size'] == row['initializedBytes'] == row['compiledBytes'] == len(payload) == wanted[key]
        assert row['targetSha256'] == row['outputSha256'] == admitted[key]['targetSha256'] == hashlib.sha256(payload).hexdigest()
        assert sha256(ROOT / asset['binary']) == asset['inputModuleSha256']
        image = (ROOT / asset['binary']).read_bytes()
        start = key[4] - int(asset['moduleBase'], 0)
        assert image[start:start + len(payload)] == payload
        for label in ['source', 'object']:
            assert sha256(ROOT / row[label]) == row[label + 'Sha256']
        assert row['encodedAssetBytes'] == row['measuredZeroAlignmentBytes'] == 0
        assert not any(scope == key[:3] and max(key[4], a) < min(key[4] + len(payload), b) for scope, a, b in occupied)
        occupied.append((key[:3], key[4], key[4] + len(payload)))
        section, unused_index, unused_offset, debug = inspect_object(ROOT / row['object'], asset['nativeSymbol'], payload)
        actual = link(ROOT / row['object'], section, asset['nativeSymbol'], asset, payload,
                      directory / f'{key[2]}-{key[4]:08x}', env)
        proofs.append(dict(address=hex(key[4]), module=key[2], initializedBytes=len(payload),
                           nonAllocatedDebugRelocations=debug, realLink=actual))
    return dict(passed=True, newInitializedDataObjects=3, newInitializedDataBytes=562, newTypedConstantDataBytes=562,
                newEncodedAssetBytes=0, newDataAlignmentBytes=0, newSourceFunctions=0,
                earlierDataPreserved=len(before), proofs=proofs, sourceCreditPendingSharedAcceptance=True)
