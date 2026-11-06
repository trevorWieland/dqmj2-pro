import argparse
import hashlib
import json
import os
import re
import struct
import subprocess
from pathlib import Path, PurePosixPath
from source_links import load_aliases, load_records, TABLE as ALIAS_TABLE


DENOMINATOR = 2512636
REPORTS = ('latest.json', 'arm7-latest.json', 'utility-latest.json')
CATEGORIES = [{'id': name, 'name': label} for name, label in (
    ('host_arm9', 'Host ARM9'), ('host_arm7', 'Host ARM7'),
    ('child_arm9', 'Embedded child ARM9'), ('child_arm7', 'Embedded child ARM7'),
    ('unclassified', 'Unclassified initialized-byte budget (no function claim)'))]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')


def namespace(row):
    return (row.get('program') or '', row.get('processor', 'arm9'), row.get('module', row.get('name')))


def contained(root, name):
    path = (root / str(name).replace('\\', '/')).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Missing or escaping input: ' + str(name))
    return path


def source_file(root, name, expected, pins=None):
    name = str(name).replace('\\', '/')
    if PurePosixPath(name).parts[0] not in ('src', 'include'):
        raise ValueError('Source must be under src/ or include/: ' + name)
    path = contained(root, name)
    actual = pins[path] if pins is not None and path in pins else digest(path)
    if pins is not None:
        pins[path] = actual
    if actual != expected:
        raise ValueError('Source hash differs: ' + name)
    return name


def nonoverlap(ranges, start, end):
    cursor = start
    for begin, stop in sorted(ranges):
        if begin < cursor or stop <= begin or stop > end:
            raise ValueError('Overlapping or escaping initialized ranges')
        cursor = stop


def elf_object(path, payload, symbols, code=True):
    names = b'\0.text\0.symtab\0.strtab\0.shstrtab\0' if code else b'\0.data\0.symtab\0.strtab\0.shstrtab\0'
    strings = bytearray(b'\0')
    entries = bytearray(16)
    markers = sorted({(offset, '$t' if mode == 'thumb' else '$a') for unused, offset, unused_size, mode in symbols}) if code else []
    for offset, marker in markers:
        at = len(strings)
        strings.extend(marker.encode() + b'\0')
        entries.extend(struct.pack('<IIIBBH', at, offset, 0, 0, 0, 1))
    for name, offset, size, unused_mode in symbols:
        if not name or offset < 0 or size <= 0 or offset + size > len(payload):
            raise ValueError('Invalid measured ELF symbol extent')
        at = len(strings)
        strings.extend(name.encode() + b'\0')
        entries.extend(struct.pack('<IIIBBH', at, offset, size, 0x12 if code else 0x11, 0, 1))
    output, headers = bytearray(52), [bytes(40)]
    parts = [(1, 1, 6 if code else 2, payload, 0, 0, 2, 0),
             (7, 2, 0, entries, 3, 1 + len(markers), 4, 16),
             (15, 3, 0, strings, 0, 0, 1, 0), (23, 3, 0, names, 0, 0, 1, 0)]
    for name, kind, flags, body, link, info, alignment, entry_size in parts:
        output.extend(bytes(-len(output) % alignment))
        at = len(output)
        output.extend(body)
        headers.append(struct.pack('<IIIIIIIIII', name, kind, flags, 0, at, len(body), link, info, alignment, entry_size))
    output.extend(bytes(-len(output) % 4))
    table = len(output)
    output.extend(b''.join(headers))
    output[:52] = struct.pack('<16sHHIIIIIHHHHHH', b'\x7fELF\x01\x01\x01' + bytes(9), 1, 40, 1, 0, 0, table,
                             0x05000000, 52, 0, 0, 40, 5, 4)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(output)


def function_contract(path, name):
    raw = Path(path).read_bytes()
    if raw[:7] != b'\x7fELF\x01\x01\x01':
        raise ValueError('Expected an ARM ELF32 source object')
    header = struct.unpack_from('<16sHHIIIIIHHHHHH', raw)
    if header[1:4] != (1, 40, 1) or header[11] != 40:
        raise ValueError('Expected a relocatable ARM ELF32 source object')
    sections = [struct.unpack_from('<IIIIIIIIII', raw, header[6] + 40 * i) for i in range(header[12])]
    def body(section):
        if section[4] + section[5] > len(raw):
            raise ValueError('ELF section escapes object')
        return raw[section[4]:section[4] + section[5]]
    def symbols(section):
        strings = body(sections[section[6]])
        result = []
        for offset in range(0, section[5], 16):
            record = struct.unpack_from('<IIIBBH', body(section), offset)
            end = strings.find(b'\0', record[0])
            if end < 0:
                raise ValueError('Invalid ELF symbol name')
            result.append((strings[record[0]:end].decode(), *record[1:]))
        return result
    tables = {i: symbols(s) for i, s in enumerate(sections) if s[1] == 2}
    choices = [s for table in tables.values() for s in table if s[0] == name and s[3] & 15 == 2 and 0 < s[5] < len(sections)]
    if len(choices) != 1:
        raise ValueError('Source function missing or ambiguous: ' + name)
    symbol = choices[0]
    start, size, index = symbol[1] & ~1, symbol[2], symbol[5]
    payload = body(sections[index])[start:start + size]
    if len(payload) != size:
        raise ValueError('Source function escapes ELF section')
    relocs = []
    referenced_data = set()
    for section in sections:
        if section[1] not in (4, 9) or section[7] != index:
            continue
        table = tables[section[6]]
        step = 12 if section[1] == 4 else 8
        for offset in range(0, section[5], step):
            address, info = struct.unpack_from('<II', body(section), offset)
            if start <= address < start + size:
                target = table[info >> 8]
                target_section = target[5]
                defined = target_section not in (0, 0xfff1, 0xfff2)
                target_value = target[1] - start if target_section == index else target[1]
                if defined and target_section < len(sections) and sections[target_section][2] & 2 and not sections[target_section][2] & 4:
                    referenced_data.add(target_section)
                relocs.append((address - start, info & 255, target[0], target[3] & 15,
                               defined, target_value if defined else 0,
                               struct.unpack_from('<i', body(section), offset + 8)[0] if step == 12 else None))
    data_contracts = []
    for data_index in referenced_data:
        data_section = sections[data_index]
        data_relocs = []
        for section in sections:
            if section[1] not in (4, 9) or section[7] != data_index:
                continue
            table = tables[section[6]]
            step = 12 if section[1] == 4 else 8
            for offset in range(0, section[5], step):
                address, info = struct.unpack_from('<II', body(section), offset)
                target = table[info >> 8]
                data_relocs.append((address, info & 255, target[0], target[3] & 15, target[1],
                                    struct.unpack_from('<i', body(section), offset + 8)[0] if step == 12 else None))
        payload_hash = hashlib.sha256(body(data_section)).hexdigest() if data_section[1] != 8 else 'zero-fill'
        data_contracts.append((data_section[1:4], data_section[5], payload_hash, tuple(sorted(data_relocs))))
    mappings = [(s[1] & ~1, s[0][1]) for table in tables.values() for s in table
                if s[5] == index and re.fullmatch(r'\$[atd](?:\..*)?', s[0]) and s[1] & ~1 <= start]
    mode = 't' if symbol[1] & 1 else max(mappings)[1] if mappings else 'unknown'
    return (hashlib.sha256(payload).hexdigest(), size, mode, tuple(sorted(relocs)), tuple(sorted(data_contracts)))


def compile_index(root, path, manifest_hash):
    report = read(path)
    if report.get('status') != 'source-compilation-passed' or report.get('fullManifestCompiled') is not True or report.get('manifestSha256') != manifest_hash:
        raise ValueError('A complete fresh source-compilation report bound to this manifest is required')
    result = {}
    for row in report['results']:
        obj = contained(root, row['object'])
        if row.get('status') != 'compiled' or digest(obj) != row['objectSha256']:
            raise ValueError('Fresh compiler object missing or changed')
        key = (row['source'], row['compilerSha256'], tuple(row['compilerFlags']))
        if key in result:
            raise ValueError('Ambiguous fresh compiler profile')
        result[key] = obj
    return result


def receipt_check(root, private, receipt, manifest_hash):
    data = read(receipt)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    if data.get('buildPassed') is not True or data.get('publicGitRevision') != revision or data.get('acceptedManifestSha256') != manifest_hash:
        raise ValueError('Build receipt must bind a successful build to this public revision and manifest')
    if os.environ.get('GITHUB_SHA') and os.environ['GITHUB_SHA'] != revision:
        raise ValueError('Public build revision differs from CI revision')
    started = data.get('replayStartedTimeNs', data.get('startedTimeNs', data.get('startTimeNs')))
    if not isinstance(started, int):
        raise ValueError('Build receipt lacks its start time')
    for name in REPORTS:
        relative = 'evidence/linking/' + name
        path = contained(private, relative)
        pin = data['reports'][relative]
        if digest(path) != pin['sha256'] or path.stat().st_mtime_ns < started:
            raise ValueError('Link report is stale or differs from fresh build receipt: ' + relative)
    return revision


def original_sections(private, module):
    if module.get('program') or module.get('processor') != 'arm9':
        return []
    name = module['name']
    folder = Path('config/arm9') / ('overlays/' + name if name.startswith('ov') else name if name != 'main' else '')
    path = private / folder / 'delinks.txt'
    if not path.is_file():
        return []
    result = []
    for line in path.read_text().splitlines():
        match = re.match(r'\s+\.\S+\s+start:(0x[0-9a-f]+) end:(0x[0-9a-f]+) kind:(code|data|rodata)\b', line)
        if match and int(match[2], 0) > int(match[1], 0):
            result.append((int(match[1], 0), int(match[2], 0), match[3] == 'code'))
    return result


def selected_rows(unit, module, accepted):
    name = unit['source'].replace('\\', '/')
    begin, end = int(unit['start'], 0), int(unit['end'], 0)
    key = (*namespace(module), name, unit['sourceSha256'])
    rows = [r for r in accepted.get(key, []) if begin <= int(r['address'], 0) < end]
    cursor = begin
    for row in sorted(rows, key=lambda r: int(r['address'], 0)):
        if int(row['address'], 0) != cursor:
            return []
        cursor += row['bytes']
    return rows if cursor == end else []


def verify_compilation_equivalence(root, private, compilation):
    root, private = root.resolve(), private.resolve()
    manifest_path = contained(root, 'public/accepted-functions.json')
    manifest = read(manifest_path)
    fresh = compile_index(root, compilation, digest(manifest_path))
    accepted, pins, contracts, verified = {}, {}, {}, set()
    modules = {m['name']: m for m in read(contained(private, 'ledger/modules.json'))['modules']}
    for row in manifest['functions']:
        accepted.setdefault((*namespace(row), row['sourceUnit'], row['sourceSha256']), []).append(row)
    for filename in REPORTS:
        for unit in read(contained(private, 'evidence/linking/' + filename))['sourceUnits']:
            if unit.get('kind', 'function') != 'function':
                continue
            rows = selected_rows(unit, modules[unit['module']], accepted)
            if not rows:
                continue
            obj = contained(private, unit['object'])
            if digest(obj) != unit['sha256']:
                raise ValueError('Linker source object changed: ' + str(obj))
            for row in rows:
                source = source_file(root, row['sourceUnit'], row['sourceSha256'], pins)
                for dependency in row.get('sourceDependencies', []):
                    source_file(root, dependency['path'], dependency['sha256'], pins)
                symbol = unit.get('symbols', {}).get(row['symbol']) or unit.get('function') or unit.get('symbol') or row['symbol']
                fresh_obj = fresh[(source, row['compilerSha256'], tuple(row['compilerFlags']))]
                key = (obj, fresh_obj, symbol)
                if key not in contracts:
                    contracts[key] = function_contract(obj, symbol) == function_contract(fresh_obj, symbol)
                if not contracts[key]:
                    raise ValueError('Fresh compiler bytes, relocations, or referenced data differ: ' + source + ':' + symbol)
                verified.add(row['id'])
    if len(verified) != len(manifest['functions']) or any(digest(p) != h for p, h in pins.items()):
        raise ValueError('Fresh equivalence omitted accepted functions or sources changed')
    return dict(verifiedFreshSourceFunctions=len(verified), verifiedFunctionContracts=len(contracts),
                acceptedManifestSha256=digest(manifest_path), publicSourceObjectsEquivalentToLinkedInputs=True,
                historicalLinkReportsDoNotEstablishFreshLinking=True)


def prepare(root, private, output, diagnostic=False, receipt=None, compilation=None):
    root, private, output = root.resolve(), private.resolve(), output.resolve()
    if not output.is_relative_to(root / 'build') and not output.is_relative_to(root / 'work'):
        raise ValueError('Generated project must remain beneath the public root build/ or work/')
    manifest_path = contained(root, 'public/accepted-functions.json')
    manifest = read(manifest_path)
    if manifest['initializedDenominatorBytes'] != DENOMINATOR:
        raise ValueError('Full initialized denominator is required')
    manifest_hash = digest(manifest_path)
    revision = None if diagnostic else receipt_check(root, private, receipt or output / 'build-receipt.json', manifest_hash)
    fresh = compile_index(root, compilation or root / 'build/public-source-compile/report.json', manifest_hash) if not diagnostic or compilation else {}
    inventory = read(contained(private, 'ledger/modules.json'))
    modules = inventory['modules']
    if len(modules) != 20 or sum(m['bytes'] for m in modules) != DENOMINATOR or inventory['buildSha256'] != manifest['romSha256']:
        raise ValueError('All twenty original modules and the full denominator are required')
    module_map = {m['name']: m for m in modules}
    if len(module_map) != 20:
        raise ValueError('Module names must have unique physical namespaces')
    accepted = {}
    for row in manifest['functions']:
        if row.get('states', {}).get('functionMatched') is not True or row.get('states', {}).get('moduleLinked') is not True:
            raise ValueError('Public manifest contains unaccepted source')
        key = (*namespace(row), row['sourceUnit'], row['sourceSha256'])
        accepted.setdefault(key, []).append(row)
    links, selections = {}, {}
    for filename in REPORTS:
        report = read(contained(private, 'evidence/linking/' + filename))
        if not report.get('allModuleBytesExact') or not report.get('symbolCheckPassed') or report['buildNamespace'] != manifest['romSha256']:
            raise ValueError('Real exact module linking and symbol checks are required')
        for module in report['modules']:
            name = module['module']
            if name in links:
                raise ValueError('Duplicate module link output')
            links[name] = module
        for unit in report['sourceUnits']:
            if unit.get('kind') != 'bss' and unit.get('section') != '.bss' and unit.get('compiledBytes', 0) > 0:
                selections.setdefault(unit['module'], []).append(unit)
    if set(links) != set(module_map):
        raise ValueError('Partial module link reports cannot be published')
    candidates = {}
    aliases = load_aliases(root) if (root / ALIAS_TABLE).is_file() else {}
    alias_records = {r['reportSymbol']: r for r in load_records(root)} if aliases else {}
    ledger_path = contained(private, 'ledger/functions.jsonl')
    for line in ledger_path.read_text().splitlines():
        row = json.loads(line)
        candidates.setdefault(namespace(row), []).append(row)
    units, credited, original_bytes, unknown_bytes = [], set(), 0, 0
    elf_object(output / 'base/empty.o', b'', [], True)
    hashes, equivalent = {}, {}
    def check(path, expected):
        path = path.resolve()
        if path not in hashes:
            hashes[path] = digest(path)
        if hashes[path] != expected:
            raise ValueError('Pinned build input or output differs: ' + str(path))
    for module in modules:
        name, base = module['name'], int(module['base'], 0)
        original_path = contained(private, module['binary'])
        linked = links[name]
        linked_path = contained(private, linked['output'])
        check(original_path, module['sha256'])
        check(linked_path, linked['outputSha256'])
        original, rebuilt = original_path.read_bytes(), linked_path.read_bytes()
        if len(original) != module['bytes'] or original != rebuilt or linked['inputSha256'] != module['sha256'] or not linked['exactBytes']:
            raise ValueError('Original and genuinely linked module images differ: ' + name)
        original_bytes += len(original)
        all_units = selections.get(name, [])
        nonoverlap([(int(u['start'], 0), int(u['end'], 0)) for u in all_units], base, base + len(original))
        category = ('child_' if module.get('program') else 'host_') + module['processor']
        physical = ('child' if module.get('program') else 'host') + '/' + module['processor'] + '/' + name
        selected = []
        for unit in all_units:
            obj = contained(private, unit['object'])
            check(obj, unit['sha256'])
            check(contained(private, unit['source']), unit['sourceSha256'])
            rows = selected_rows(unit, module, accepted) if unit.get('kind', 'function') == 'function' else []
            if not rows:
                continue
            symbols = []
            for row in rows:
                source = source_file(root, row['sourceUnit'], row['sourceSha256'], hashes)
                for dependency in row.get('sourceDependencies', []):
                    source_file(root, dependency['path'], dependency['sha256'], hashes)
                symbol = unit.get('symbols', {}).get(row['symbol']) or unit.get('function') or unit.get('symbol') or row['symbol']
                if fresh:
                    fresh_obj = fresh[(source, row['compilerSha256'], tuple(row['compilerFlags']))]
                    key = (obj, fresh_obj, symbol)
                    if key not in equivalent:
                        equivalent[key] = function_contract(obj, symbol) == function_contract(fresh_obj, symbol)
                    if not equivalent[key]:
                        raise ValueError('Fresh compiler bytes or relocations differ: ' + symbol)
                symbols.append((symbol, int(row['address'], 0) - int(unit['start'], 0), row['bytes'], row['mode']))
                credited.add(row['id'])
            selected.append((int(unit['start'], 0), int(unit['end'], 0), source, symbols))
        sections = original_sections(private, module)
        real_candidates = []
        cursor = base
        for row in sorted(candidates.get(namespace(module), []), key=lambda r: int(r['address'], 0)):
            begin, size = int(row['address'], 0), row.get('bytes')
            if type(size) is not int or size <= 0 or begin < cursor or begin + size > base + len(original):
                continue
            end = begin + size
            if any(begin < stop and start < end for start, stop, unused_source, unused_symbols in selected):
                continue
            if any(begin < stop and start < end and (not code or start > begin or stop < end) for start, stop, code in sections):
                continue
            real_candidates.append(row)
            cursor = end
        points = {base, base + len(original)}
        for begin, end, unused_source, unused_symbols in selected:
            points.update((begin, end))
        for begin, end, unused_code in sections:
            points.update(x for x in (begin, end) if base < x < base + len(original))
        for row in real_candidates:
            points.update((int(row['address'], 0), int(row['address'], 0) + row['bytes']))
        ordered = sorted(points)
        spans = [(begin, end, next((s for s in selected if s[0] <= begin and end <= s[1]), None)) for begin, end in zip(ordered, ordered[1:])]
        for begin, end, selection in spans:
            source = selection[2] if selection else 'src'
            key = hashlib.sha256((physical + '/' + str(begin)).encode()).hexdigest()[:20]
            target = output / 'target' / (key + '.o')
            base_path = output / 'base' / (key + '.o')
            known = next((code for start, stop, code in sections if start <= begin and end <= stop), None)
            candidate = next((r for r in real_candidates if int(r['address'], 0) == begin and int(r['address'], 0) + r['bytes'] == end), None)
            if candidate and candidate['symbol'] in aliases:
                alias = alias_records[candidate['symbol']]
                if namespace(candidate) != namespace(alias) or candidate['mode'] != alias['mode'] or begin != int(alias['address'], 0):
                    raise ValueError('Source alias crosses a physical function identity')
                source = aliases[candidate['symbol']]
            code = bool(selection or candidate)
            symbols = [(n, o + selection[0] - begin, z, m) for n, o, z, m in selection[3]] if selection else [
                (candidate['symbol'], 0, candidate['bytes'], candidate['mode'])] if candidate else []
            unclassified = not code and known is not False
            if unclassified:
                unknown_bytes += end - begin
                symbols = [(f'__initialized_span_{begin:08x}', 0, end - begin, 'data')]
            elf_object(target, original[begin - base:end - base], symbols, code)
            metadata = dict(source_path=source, complete=bool(selection), progress_categories=[category])
            if unclassified:
                metadata['progress_categories'].append('unclassified')
            group = str(PurePosixPath(source).with_suffix('')) if selection or source != 'src' else 'unreconstructed'
            item = dict(name=group + '/' + physical + f'/{begin:08x}', target_path=target.relative_to(output).as_posix(),
                        base_path='base/empty.o', metadata=metadata)
            if selection:
                elf_object(base_path, rebuilt[begin - base:end - base], symbols, code)
                item['base_path'] = base_path.relative_to(output).as_posix()
            units.append(item)
    if original_bytes != DENOMINATOR or len(credited) != len(manifest['functions']):
        raise ValueError('Export omitted initialized bytes or closed accepted functions: ' + str(len(credited)))
    for path, expected in hashes.items():
        if digest(path) != expected:
            raise ValueError('Build input changed during export: ' + str(path))
    project = dict(min_version='3.8.3', build_base=False, build_target=False, units=units, progress_categories=CATEGORIES)
    write(output / 'objdiff.json', project)
    accepted_ids = {(namespace(r), int(r['address'], 0), r['mode']) for r in manifest['functions']}
    functional = []
    draft_path = private / 'ledger/behavior-drafts-20261101.json'
    if draft_path.is_file():
        for row in read(draft_path)['functions']:
            state = row.get('states', {})
            identity = (namespace(row), int(row['address'], 0), row['mode'])
            if state.get('boundedBehaviorQualified') is True and not state.get('functionMatched') and identity not in accepted_ids:
                names = [r['symbol'] for r in candidates.get(namespace(row), []) if r['address'] == row['address'] and r['mode'] == row['mode']]
                if len(names) == 1:
                    functional.append(dict(name=names[0], confidence='medium'))
    write(output / 'functional.json', dict(functions=sorted(functional, key=lambda r: r['name'])))
    summary = dict(schemaVersion=1, publicGitRevision=revision, diagnostic=diagnostic, publishable=not diagnostic,
                   acceptedManifestSha256=manifest_hash, originalInitializedBytes=original_bytes, moduleCount=len(modules),
                   acceptedFunctions=len(credited), units=len(units), unclassifiedInitializedBytes=unknown_bytes,
                   freshCompilationVerified=bool(fresh),
                   accounting='Final linked initialized image comparison. Only accepted and measured candidate function extents count as code. Unidentified initialized residuals enter a separate data budget, without invented functions; code percentage is not overall game completion.',
                   targetOnlyUnits=sum(u['base_path'] == 'base/empty.o' for u in units), functionalFunctions=len(functional),
                   absentSourceBaseline='base/empty.o contains no code, data, or functions; it is an explicit absence representation, not a compiled implementation.')
    write(output / 'export-receipt.json', summary)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--private-root', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, default=Path('build/B2JJ-modified'))
    parser.add_argument('--receipt', type=Path)
    parser.add_argument('--compile-report', type=Path)
    parser.add_argument('--diagnostic', action='store_true')
    args = parser.parse_args()
    output = args.out_dir if args.out_dir.is_absolute() else args.root / args.out_dir
    try:
        print(json.dumps(prepare(args.root, args.private_root, output, args.diagnostic, args.receipt, args.compile_report), indent=2))
    except (OSError, ValueError, KeyError, TypeError, struct.error) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
