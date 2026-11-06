import gzip
import hashlib
import json
import re
import struct
from collections import defaultdict
from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def coff(path):
    data = path.read_bytes()
    machine, sections, stamp, offset, count, optional, flags = struct.unpack_from('<HHIIIHH', data)
    assert machine == 0x14C and optional == 0
    assert 20 + sections * 40 <= len(data)
    strings = offset + count * 18
    assert strings + 4 <= len(data)
    string_size = struct.unpack_from('<I', data, strings)[0]
    assert strings + string_size <= len(data)
    symbols, index = {}, 0
    while index < count:
        start = offset + index * 18
        raw = data[start:start + 8]
        if raw[:4] == bytes(4):
            position = strings + struct.unpack_from('<I', raw, 4)[0]
            assert strings + 4 <= position < strings + string_size
            end = data.index(b'\0', position, strings + string_size)
            name = data[position:end].decode('utf-8')
        else:
            name = raw.rstrip(b'\0').decode('utf-8')
        value, section, kind, storage, auxiliary = struct.unpack_from('<IhHBB', data, start + 8)
        symbols[index] = dict(name=name, value=value, section=section,
            function=bool(kind & 0x20), storage=storage)
        assert index + auxiliary < count
        index += 1 + auxiliary
    definitions, undefined, weak, relocations = [], [], [], []
    for symbol in symbols.values():
        if symbol['storage'] == 2:
            if symbol['section'] > 0 or symbol['section'] == 0 and symbol['value']:
                definitions.append(symbol)
            elif symbol['section'] == 0:
                undefined.append(symbol)
        elif symbol['storage'] == 105:
            weak.append(symbol)
    for number in range(sections):
        start = 20 + number * 40
        section_name = data[start:start + 8].rstrip(b'\0').decode('ascii')
        pointer = struct.unpack_from('<I', data, start + 24)[0]
        length = struct.unpack_from('<H', data, start + 32)[0]
        assert length != 0xFFFF and pointer + length * 10 <= len(data)
        for item in range(length):
            address, symbol_index, kind = struct.unpack_from('<IIH', data, pointer + item * 10)
            assert symbol_index in symbols
            symbol = symbols[symbol_index]
            if symbol['storage'] in [2, 105]:
                relocations.append(dict(section=section_name, offset=address,
                    type=kind, symbol=symbol['name']))
    return dict(definitions=definitions, undefined=undefined, weak=weak, relocations=relocations)


def scope(entry):
    return entry['processor'], entry.get('program') or '', entry['module']


def address(name):
    found = re.search(r'(?:^|_)([0-9a-fA-F]{8})$', name)
    return int(found[1], 16) if found else None


def main():
    census_path = ROOT / 'evidence/portability/windows-source-census111-targetabi-v4-20261101.json'
    census = read_json(census_path)
    snapshot = read_json(ROOT / census['snapshot'])
    assert sha256(ROOT / census['snapshot']) == census['snapshotSha256']
    details_path = ROOT / census['details']['path']
    assert sha256(details_path) == census['details']['sha256']
    raw = gzip.decompress(details_path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == census['details']['decodedSha256']
    details = json.loads(raw)
    sources = defaultdict(list)
    for entry in snapshot['functions']:
        sources[entry['source']].append(entry)
    rows, groups = [], defaultdict(list)
    selected_addresses = defaultdict(list)
    for entry in snapshot['functions']:
        location = int(entry['address'], 0) if isinstance(entry['address'], str) else entry['address']
        selected_addresses[(entry['processor'], entry.get('program') or '', location)].append(entry)
    for original in details['results']:
        if not original['compiled']:
            continue
        assert sha256(ROOT / original['source']) == original['sourceSha256']
        assert sha256(ROOT / original['object']) == original['objectSha256']
        symbols = coff(ROOT / original['object'])
        row = dict(source=original['source'], sourceSha256=original['sourceSha256'],
            object=original['object'], objectSha256=original['objectSha256'],
            scopes=[list(value) for value in sorted({scope(entry) for entry in sources[original['source']]})],
            selectedInstances=sources[original['source']], **symbols)
        rows.append(row)
        for value in row['scopes']:
            groups[tuple(value)].append(row)
    assert len(rows) == census['compiled'] == 8375
    frontier = []
    for namespace, members in sorted(groups.items()):
        local_definitions = defaultdict(list)
        available = defaultdict(list)
        processor, program, module = namespace
        for value, providers in groups.items():
            if value[:2] != namespace[:2]:
                continue
            for row in providers:
                for symbol in row['definitions']:
                    record = dict(source=row['source'], module=value[2], function=symbol['function'])
                    available[symbol['name']].append(record)
                    if value == namespace:
                        local_definitions[symbol['name']].append(record)
        needs = defaultdict(list)
        for row in members:
            for symbol in row['undefined']:
                used = [entry for entry in row['relocations'] if entry['symbol'] == symbol['name']]
                needs[symbol['name']].append(dict(source=row['source'], relocationCount=len(used),
                    relocationTypes=sorted({entry['type'] for entry in used})))
        resolutions, counts = [], defaultdict(int)
        for name, consumers in sorted(needs.items()):
            if name in local_definitions:
                classification = 'exact-name-defined-in-same-module'
            elif name in available:
                classification = 'exact-name-defined-in-same-program-other-module'
            elif name in ['_memcpy', '_memset', '_memmove', '__fltused'] or name.startswith('___'):
                classification = 'native-runtime-symbol-needs-implementation-or-link-contract'
            else:
                classification = 'unresolved-symbol'
            location = address(name)
            candidates = selected_addresses.get((processor, program, location), []) if location is not None else []
            if classification == 'unresolved-symbol' and candidates:
                classification = 'address-labelled-selected-source-needs-qualified-alias-or-platform-work'
            counts[classification] += 1
            resolutions.append(dict(symbol=name, classification=classification,
                consumers=consumers, exactNameProviders=available.get(name, []),
                addressLabelCandidates=[{key: candidate[key] for key in
                    ['processor', 'program', 'module', 'mode', 'address', 'name', 'source']} for candidate in candidates],
                aliasAutomaticallyApplied=False))
        duplicate = [dict(symbol=name, providers=providers) for name, providers in local_definitions.items()
            if len({provider['source'] for provider in providers}) > 1]
        frontier.append(dict(processor=processor, program=program, module=module,
            objectUnits=len(members), undefinedNames=len(needs), resolutionCounts=dict(counts),
            duplicateExternalDefinitionNames=len(duplicate), duplicateDefinitions=duplicate,
            symbols=resolutions))
    output = dict(objects=rows, modules=frontier)
    encoded = json.dumps(output, sort_keys=True, separators=(',', ':')).encode()
    detail_path = ROOT / 'evidence/portability/windows-native-link-frontier111-details-20261101.json.gz'
    detail_path.write_bytes(gzip.compress(encoded, mtime=0))
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        census=dict(path=census_path.relative_to(ROOT).as_posix(), sha256=sha256(census_path)),
        sourceSnapshot=dict(path=census['snapshot'], sha256=census['snapshotSha256']),
        verifiedCoffObjects=len(rows), moduleScopes=len(frontier), sourceCredit=0,
        originalSourceModified=False, symbolAliasesApplied=0, generatedStubs=0,
        nativeGameExecutionCount=0, fullNativeLinkProven=False, fullWindowsGameProven=False,
        modules=[{key: value for key, value in module.items() if key not in ['symbols', 'duplicateDefinitions']}
            for module in frontier],
        details=dict(path=detail_path.relative_to(ROOT).as_posix(), sha256=sha256(detail_path),
            decodedSha256=hashlib.sha256(encoded).hexdigest()),
        limitations=['Source111 accepted C/C++ corpus only; later cohorts and failed compiler units are separate',
            'COFF symbols and relocations are measured; no executable link or ABI compatibility is established',
            'Same-program other-module names may need overlay lifetime/context qualification before linking',
            'Address suffixes only nominate qualified candidates and never generate aliases or infer data/function types',
            'All external definitions in a compiled source are retained, including surplus entries outside selected ARM ranges',
            'Native runtime/platform dependencies and duplicate definitions remain failures for a full-game build'])
    write_json(ROOT / 'evidence/portability/windows-native-link-frontier111-20261101.json', report)
    print(dict(objects=len(rows), moduleScopes=len(frontier),
        undefinedNames=sum(row['undefinedNames'] for row in frontier),
        duplicateNames=sum(row['duplicateExternalDefinitionNames'] for row in frontier), sourceCredit=0))


if __name__ == '__main__':
    main()
