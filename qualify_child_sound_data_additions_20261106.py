import hashlib
import os
import re
from project import ROOT, read_json, sha256, configuration, native_dependencies
from source_dependencies import dependency_hashes, dependencies_current
from qualify_child_message_data_additions_20261106 import selected_data, identity, FIELDS


LAYOUT = 'src/utility/parallel_wave20261105/child-sdat-next/layout.json'
CLAIM = 'evidence/lanes/parallel-wave20261105/child-sdat-next/data-claim.json'
CODECS = {
    'wave20261105_child_sdat_next_codec.py': '7b820010dd3315db95a8427573083b0b0b824b6dd6889c0d47563553957c08c8',
    'wave20261105_child_sdat_next_events.py': 'ef15d7ac50c69015e21291f947eeb59bf217a67d634c7cbebe46dcf5ff031e20',
    'wave20261105_child_sdat_next_waves.py': '820f2cf8b3732931aa3a980fa67dede30531b2c54d2a101d012b53b0ff8ce462',
    'child_message_data_codec_20261106.py': 'ed3351715d2024c6d65f2a9330b050f4db6280af8b88c147d13b51cd13ec1e07',
}


def literal_payload(code, symbol, size):
    declaration = re.fullmatch(r'\s*const unsigned char ' + re.escape(symbol) + r'\[' + str(size) +
                               r'\]\s*=\s*\{([\s\S]*)\};\s*', code)
    assert declaration
    fields = declaration[1].strip().rstrip(',').split(',')
    assert all(re.fullmatch(r'\s*0x[0-9a-fA-F]{2}\s*', field) for field in fields)
    result = bytes(int(field, 16) for field in fields)
    assert len(result) == size
    return result


def qualify(before, after, expected, functions, directory):
    config = configuration()
    native_dependencies(config)
    from child_message_data_codec_20261106 import encode as lz_encode
    from wave20261105_child_sdat_next_codec import encode
    from match_child_message_data_20261106 import inspect_object, link_unit, LINKER, LINKER_HASH, COMPILER, COMPILER_HASH, FLAGS
    assert {name: sha256(ROOT / name) for name in CODECS} == CODECS
    assert sha256(ROOT / CLAIM) == '1b7056ebf3afb429d0b7b74923f5312393aab0d6aff4c4359a2e48a18d63db25'
    assert sha256(LINKER) == LINKER_HASH
    for key, row in before.items():
        assert key in after and all(after[key].get(field) == row.get(field) for field in FIELDS)
    added = set(after) - set(before)
    wanted = {identity(row): row['bytes'] for row in expected}
    assert len(wanted) == len(expected) == 1 and added == set(wanted)
    claim = {identity(row): row for row in read_json(ROOT / CLAIM)['claimedStorage']}
    assert wanted == {key: row['bytes'] for key, row in claim.items()}
    layout = read_json(ROOT / LAYOUT)
    assets = {int(row['address'], 0): row for row in layout['assets']}
    assert len(assets) == 1 and set(assets) == {key[4] for key in added}
    assert sha256(ROOT / layout['binary']) == layout['inputModuleSha256'] == 'af25c028552d9de7428f5393757507b3c029e80f22c9cc44e94e45103f0814d0'
    native = (ROOT / layout['binary']).read_bytes()
    occupied = []
    for row in before.values():
        key = identity(row)
        size = row.get('bytes', row.get('size'))
        assert isinstance(size, int) and size > 0
        occupied.append((key[:3], key[4], key[4] + size))
    for row in functions.values():
        namespace = identity(dict(row, kind='data'))
        occupied.append((namespace[:3], namespace[4], namespace[4] + row['size']))
    proofs = []
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    for key in sorted(added):
        row, asset, admitted = after[key], assets[key[4]], claim[key]
        assert key[:3] == ('dwc/utility.bin/move/child.srl', 'arm9', 'utility-child-arm9-main')
        assert row['kind'] == 'data' and row['mode'] == 'data' and row['ordinaryFunctionCredit'] == 0
        assert row['bytes'] == row['size'] == row['compiledBytes'] == wanted[key]
        assert row['sourceLanguage'] == 'C' and row['compilerFlags'] == FLAGS
        assert row['compiler'] == COMPILER.relative_to(ROOT).as_posix()
        assert sha256(COMPILER) == row['compilerSha256'] == COMPILER_HASH
        assert row['relocations'] == [] and row['executableSectionBytes'] == 0
        assert row['allocatedZeroFillBytes'] == 0 and row['initializedBytes'] == row['bytes']
        assert dependencies_current(row)
        assert asset['semanticSource'] == admitted['semanticSource']
        assert sha256(ROOT / asset['semanticSource']) == asset['semanticSourceSha256'] == admitted['semanticSourceSha256']
        assert dependency_hashes(row) == {name: sha256(ROOT / name) for name in [LAYOUT, asset['semanticSource']]}
        document = read_json(ROOT / asset['semanticSource'])
        decoded = encode(document['semantic'])
        encoded = lz_encode(decoded, document['compressionRecipe'])
        alignment = (-len(encoded)) % 4
        assert document['storageAlignment'] == 4 and document['measuredZeroAlignmentBytes'] == alignment
        payload = encoded + bytes(alignment)
        symbol = f'native_child_sound_asset_{key[4]:08x}'
        assert row['source'] == f'generated/child-sdat-next/{key[4]:08x}.c'
        assert literal_payload((ROOT / row['source']).read_text(), symbol, len(payload)) == payload
        for label in ['source', 'object']:
            assert sha256(ROOT / row[label]) == row[label + 'Sha256']
        assert row['targetSha256'] == row['outputSha256'] == admitted['targetSha256'] == hashlib.sha256(payload).hexdigest()
        assert native[key[4] - 0x02000000:key[4] - 0x02000000 + len(payload)] == payload
        assert row['encodedAssetBytes'] == admitted['encodedAssetBytes'] == len(encoded)
        assert row['measuredZeroAlignmentBytes'] == admitted['measuredZeroAlignmentBytes'] == alignment
        assert not [p for p in occupied if p[0] == key[:3] and max(key[4], p[1]) < min(key[4] + len(payload), p[2])]
        occupied.append((key[:3], key[4], key[4] + len(payload)))
        section, unused_index, unused_offset, debug = inspect_object(ROOT / row['object'], symbol, payload)
        target = directory / f'{key[4]:08x}'
        target.mkdir(parents=True, exist_ok=True)
        link = link_unit(ROOT / row['object'], symbol, section, key[4], payload, target, LINKER, env)
        proofs.append(dict(address=hex(key[4]), initializedBytes=len(payload), encodedAssetBytes=len(encoded),
                           measuredZeroAlignmentBytes=alignment, realLink=link, nonAllocatedDebugRelocations=debug))
    assert sum(row['initializedBytes'] for row in proofs) == 13936
    assert sum(row['encodedAssetBytes'] for row in proofs) == 13935
    assert sum(row['measuredZeroAlignmentBytes'] for row in proofs) == 1
    return dict(passed=True, newInitializedDataObjects=1, newInitializedDataBytes=13936,
                newEncodedAssetBytes=13935, newDataAlignmentBytes=1, newSourceFunctions=0,
                earlierDataPreserved=len(before), proofs=proofs, sourceCreditPendingSharedAcceptance=True)
