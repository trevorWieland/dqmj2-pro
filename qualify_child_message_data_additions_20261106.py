import hashlib
from project import ROOT, read_json, sha256, configuration, native_dependencies
import recovery_registry
from source_dependencies import dependency_hashes, dependencies_current


FIELDS = ['source', 'sourceSha256', 'object', 'objectSha256', 'bytes', 'size', 'targetSha256',
          'relocations', 'sourceDependencies', 'section', 'compilerSha256', 'compilerFlags']


def identity(row):
    module = row['module']
    program = row.get('program') or ('dwc/utility.bin/move/child.srl' if module.startswith('utility-child-') else '')
    processor = row.get('processor') or ('arm7' if 'arm7' in module else 'arm9')
    address = int(row['address'], 0) if isinstance(row['address'], str) else row['address']
    return program, processor, module, row['kind'], address


def selected_data():
    result = {}
    for batch in recovery_registry.batches():
        if batch['kind'] not in ('data', 'mixed'):
            continue
        report = read_json(ROOT / batch['report'])
        for row in report.get('dataMatches', []):
            item = {**report, **row, 'evidence': batch['report']}
            key = identity(item)
            assert key not in result
            result[key] = item
    return result


def qualify(before, after, expected, functions, directory):
    config = configuration()
    native_dependencies(config)
    import ndspy.bmg as bmg
    from child_message_data_codec_20261106 import c_source
    from match_child_message_data_20261106 import LAYOUT, inspect_object, link_unit, LINKER, LINKER_HASH, COMPILER, COMPILER_HASH, FLAGS
    import os
    assert sha256(LINKER) == LINKER_HASH
    for key, row in before.items():
        assert key in after and all(after[key].get(field) == row.get(field) for field in FIELDS)
    added = set(after) - set(before)
    wanted = {identity(row): row['bytes'] for row in expected}
    assert len(wanted) == len(expected) == 8 and added == set(wanted)
    layout = read_json(ROOT / LAYOUT)
    assert {key[4] for key in added} == {int(row['address'], 0) for row in layout['assets']}
    native_path = ROOT / layout['binary']
    assert sha256(native_path) == layout['inputModuleSha256']
    native = native_path.read_bytes()
    asset_map = {int(row['address'], 0): row for row in layout['assets']}
    occupied = []
    for row in before.values():
        key = identity(row)
        size = row.get('bytes', row.get('size'))
        assert isinstance(size, int) and size > 0
        occupied.append((key[:3], key[4], key[4] + size))
    for row in functions.values():
        address = int(row['address'], 0) if isinstance(row['address'], str) else row['address']
        module = row['module']
        namespace = row.get('program') or ('dwc/utility.bin/move/child.srl' if module.startswith('utility-child-') else '')
        processor = row.get('processor') or ('arm7' if 'arm7' in module else 'arm9')
        occupied.append(((namespace, processor, module), address, address + row['size']))
    proofs = []
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    for key in sorted(added):
        row, asset = after[key], asset_map[key[4]]
        assert key[:3] == ('dwc/utility.bin/move/child.srl', 'arm9', 'utility-child-arm9-main')
        assert row['kind'] == 'data' and row['mode'] == 'data' and row['ordinaryFunctionCredit'] == 0
        assert row['bytes'] == row['size'] == row['compiledBytes'] == wanted[key]
        assert row['sourceLanguage'] == 'C' and row['compilerFlags'] == FLAGS
        assert row['compiler'] == COMPILER.relative_to(ROOT).as_posix()
        assert sha256(COMPILER) == row['compilerSha256'] == COMPILER_HASH
        assert row['relocations'] == [] and row['executableSectionBytes'] == 0
        assert row['allocatedZeroFillBytes'] == 0 and row['initializedBytes'] == row['bytes']
        assert dependencies_current(row)
        assert dependency_hashes(row) == {name: sha256(ROOT / name) for name in [LAYOUT, asset['semanticSource']]}
        symbol = f'native_child_message_data_{key[4]:08x}'
        code, payload, encoded, alignment = c_source(read_json(ROOT / asset['semanticSource']), symbol, bmg)
        assert row['source'] == f'generated/child-message-data/{key[4]:08x}.c'
        assert (ROOT / row['source']).read_text() == code
        for label in ['source', 'object']:
            assert sha256(ROOT / row[label]) == row[label + 'Sha256']
        assert row['targetSha256'] == row['outputSha256'] == hashlib.sha256(payload).hexdigest()
        assert native[key[4] - 0x02000000:key[4] - 0x02000000 + len(payload)] == payload
        assert row['encodedAssetBytes'] == encoded and row['measuredZeroAlignmentBytes'] == alignment
        assert not [p for p in occupied if p[0] == key[:3] and max(key[4], p[1]) < min(key[4] + len(payload), p[2])]
        occupied.append((key[:3], key[4], key[4] + len(payload)))
        section, unused_index, unused_offset, debug = inspect_object(ROOT / row['object'], symbol, payload)
        target = directory / f'{key[4]:08x}'
        target.mkdir(parents=True, exist_ok=True)
        link = link_unit(ROOT / row['object'], symbol, section, key[4], payload, target, LINKER, env)
        proofs.append(dict(address=hex(key[4]), initializedBytes=len(payload), encodedAssetBytes=encoded,
                           measuredZeroAlignmentBytes=alignment, realLink=link, nonAllocatedDebugRelocations=debug))
    assert sum(row['initializedBytes'] for row in proofs) == 3808
    assert sum(row['encodedAssetBytes'] for row in proofs) == 3799
    assert sum(row['measuredZeroAlignmentBytes'] for row in proofs) == 9
    return dict(passed=True, newInitializedDataObjects=8, newInitializedDataBytes=3808,
                newEncodedAssetBytes=3799, newDataAlignmentBytes=9, newSourceFunctions=0,
                earlierDataPreserved=len(before), proofs=proofs, sourceCreditPendingSharedAcceptance=True)
