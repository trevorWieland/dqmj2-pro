import gzip
import hashlib
import json
import struct
from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def section_metadata(path):
    data = path.read_bytes()
    machine, count, stamp, symbols, symbol_count, optional, flags = struct.unpack_from('<HHIIIHH', data)
    assert machine == 0x14C and optional == 0
    sections = {}
    for number in range(count):
        start = 20 + number * 40
        size, pointer = struct.unpack_from('<II', data, start + 16)
        relocations = struct.unpack_from('<H', data, start + 32)[0]
        characteristics = struct.unpack_from('<I', data, start + 36)[0]
        assert not pointer or pointer + size <= len(data)
        payload = data[pointer:pointer + size] if pointer else bytes(size)
        sections[number + 1] = dict(comdat=bool(characteristics & 0x1000), selection=None,
            rawBytes=size, initializedBytesSha256=hashlib.sha256(payload).hexdigest(),
            relocationCount=relocations, characteristics=characteristics)
    index = 0
    while index < symbol_count:
        position = symbols + index * 18
        value, section, kind, storage, auxiliary = struct.unpack_from('<IhHBB', data, position + 8)
        if storage == 3 and section > 0 and kind == 0 and auxiliary == 1:
            sections[section]['selection'] = data[position + 18 + 14]
        index += 1 + auxiliary
    return sections


def main():
    base_path = ROOT / 'evidence/portability/windows-native-link-frontier111-20261101.json'
    base = read_json(base_path)
    detail_path = ROOT / base['details']['path']
    assert sha256(detail_path) == base['details']['sha256']
    raw = gzip.decompress(detail_path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == base['details']['decodedSha256']
    detail = json.loads(raw)
    by_source = {}
    for row in detail['objects']:
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert sha256(ROOT / row['object']) == row['objectSha256']
        sections = section_metadata(ROOT / row['object'])
        by_source[row['source']] = row
        for symbol in row['definitions']:
            symbol['coffSection'] = sections[symbol['section']] if symbol['section'] > 0 else None
    folds = conflicts = 0
    for module in detail['modules']:
        local_folds = local_conflicts = 0
        for duplicate in module['duplicateDefinitions']:
            definitions = []
            for provider in duplicate['providers']:
                row = by_source[provider['source']]
                matches = [symbol for symbol in row['definitions'] if symbol['name'] == duplicate['symbol']]
                assert len(matches) == 1
                definitions.append(dict(source=provider['source'], **matches[0]))
            metadata = [definition['coffSection'] for definition in definitions]
            literal = duplicate['symbol'].startswith(('__real@', '__xmm@'))
            same_bytes = len({(value['rawBytes'], value['initializedBytesSha256']) for value in metadata if value}) == 1
            pick_any = all(value and value['comdat'] and value['selection'] == 2
                and value['relocationCount'] == 0 for value in metadata)
            foldable = literal and same_bytes and pick_any and not any(definition['function'] for definition in definitions)
            duplicate.update(definitionMetadata=definitions,
                classification='identical-compiler-literal-COMDAT-pick-any' if foldable else 'needs-qualified-link-conflict-review',
                linkerResolutionActuallyTested=False)
            local_folds += foldable
            local_conflicts += not foldable
        module.update(compilerLiteralComdatDuplicateNames=local_folds,
            unresolvedNonliteralDefinitionConflicts=local_conflicts)
        folds += local_folds
        conflicts += local_conflicts
    encoded = json.dumps(detail, sort_keys=True, separators=(',', ':')).encode()
    output_detail = ROOT / 'evidence/portability/windows-native-link-frontier111-v2-details-20261101.json.gz'
    output_detail.write_bytes(gzip.compress(encoded, mtime=0))
    report = dict(base, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        originalFrontier=dict(path=base_path.relative_to(ROOT).as_posix(), sha256=sha256(base_path)),
        identicalCompilerLiteralComdatDuplicateNames=folds, unresolvedNonliteralDefinitionConflicts=conflicts,
        modules=[{key: value for key, value in module.items() if key not in ['symbols', 'duplicateDefinitions']}
            for module in detail['modules']],
        details=dict(path=output_detail.relative_to(ROOT).as_posix(), sha256=sha256(output_detail),
            decodedSha256=hashlib.sha256(encoded).hexdigest()))
    report['limitations'] = base['limitations'] + [
        'Duplicate external names are initially candidates, not necessarily conflicts: identical compiler literals can be COMDAT pick-any',
        'Only nonfunction __real/__xmm entries with identical section bytes, selection2 and no relocations are classified foldable',
        'COMDAT metadata is inspected independently; no linker acceptance, ABI or complete-game claim follows']
    write_json(ROOT / 'evidence/portability/windows-native-link-frontier111-v2-20261101.json', report)
    print(dict(verifiedObjects=base['verifiedCoffObjects'], identicalLiteralComdatNames=folds,
        nonliteralConflicts=conflicts, sourceCredit=0))


if __name__ == '__main__':
    main()
