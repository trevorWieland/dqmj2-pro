import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


TABLE = 'public_tools/source_aliases.json'
HEADER = 'include/bytematch_names.h'
DEFINITIONS = 'public_tools/source_definitions.json'
IDENTITY_FIELDS = ('program', 'processor', 'module', 'mode', 'address')
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|\x27(?:\\.|[^\x27\\])*\x27|/\*.*?\*/|//[^\n]*', re.S)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_path(root, name):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name:
        raise ValueError('Expected a canonical public source path')
    parts = PurePosixPath(name)
    if parts.is_absolute() or '..' in parts.parts or parts.parts[0] not in {'src', 'include'}:
        raise ValueError('Path leaves public source directories')
    path = (root / name).resolve()
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError('Source or quoted include is missing: ' + name)
    return path


def remove_tokens(text, literals):
    def replace(match):
        token = match[0]
        if token.startswith(('"', "'")) and not literals:
            return token
        return re.sub(r'[^\n]', ' ', token)
    return TOKENS.sub(replace, text)


def identity(row):
    if any(field not in row for field in IDENTITY_FIELDS):
        raise ValueError('Alias needs the full program/CPU/module/mode/address identity')
    program, processor, module, mode, address = (row[field] for field in IDENTITY_FIELDS)
    if program != '' or processor != 'arm9' or mode not in {'arm', 'thumb'}:
        raise ValueError('Alias is outside the declared host ARM9 source-link scope')
    if module != 'main' and not re.fullmatch(r'ov00[0-7]', str(module)):
        raise ValueError('Unknown alias module namespace')
    if not isinstance(address, str) or not re.fullmatch(r'0x[0-9a-f]{8}', address):
        raise ValueError('Alias needs a canonical initialized address')
    value = int(address, 0)
    if value % (4 if mode == 'arm' else 2):
        raise ValueError('Alias address disagrees with instruction mode')
    suffix = address[2:]
    expected_report = 'func_' + ('' if module == 'main' else module + '_') + suffix
    expected_source = 'native_' + module + '_' + suffix
    if row.get('reportSymbol') != expected_report or row.get('sourceSymbol') != expected_source:
        raise ValueError('Alias symbol crosses its physical module namespace')
    if row.get('complete') is not False:
        raise ValueError('A source-display alias cannot assert source completion')
    return program, processor, module, mode, value


def closure(root, row):
    declarations = [(row['sourcePath'], row['sourceSha256'])]
    declarations.extend((entry['path'], entry['sha256']) for entry in row.get('sourceDependencies', []))
    pins = {}
    for name, expected in declarations:
        path = source_path(root, name)
        if path in pins or not isinstance(expected, str) or not re.fullmatch(r'[0-9a-f]{64}', expected):
            raise ValueError('Duplicate or malformed source/include pin')
        if digest(path) != expected:
            raise ValueError('Source hash differs: ' + name)
        pins[path] = expected
    primary = source_path(root, row['sourcePath'])
    if primary.suffix.lower() not in {'.c', '.cpp'}:
        raise ValueError('Source aliases must identify a C/C++ definition')
    seen, pending = set(), [primary]
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        text = remove_tokens(path.read_text(encoding='utf-8-sig'), literals=False)
        for include in re.findall(r'(?m)^\s*#\s*include\s*"([^"\n]+)"', text):
            if '\\' in include or ':' in include or PurePosixPath(include).is_absolute() or '..' in PurePosixPath(include).parts:
                raise ValueError('Quoted include escapes its source directory')
            candidate = (path.parent / include).resolve()
            if not candidate.is_relative_to(root) or not candidate.is_file():
                raise ValueError('Source or quoted include is missing: ' + include)
            if candidate not in pins:
                raise ValueError('Quoted include lacks a declared hash: ' + include)
            pending.append(candidate)
    if seen != set(pins):
        raise ValueError('Source pins differ from the reachable quoted include closure')
    return primary


def definition_matches(path, name):
    text = remove_tokens(path.read_text(encoding='utf-8-sig'), literals=True)
    pattern = re.compile(r'\b' + re.escape(name) + r'\s*\([^;{}]*\)\s*\{')
    matches = []
    for match in pattern.finditer(text):
        depth = 0
        for brace in re.findall(r'[{}]', text[:match.start()]):
            depth = depth + 1 if brace == '{' else max(0, depth - 1)
        if depth == 0:
            matches.append(match)
    return matches


def definition(path, name):
    if len(definition_matches(path, name)) != 1:
        raise ValueError('Source symbol has no unique top-level C definition: ' + name)


def load_records(root):
    root = Path(root).resolve()
    table = json.loads((root / TABLE).read_text(encoding='utf-8-sig'))
    if table.get('schemaVersion') != 1 or not isinstance(table.get('aliases'), list):
        raise ValueError('Expected source-alias schemaVersion 1')
    records, symbols, identities = [], set(), set()
    for row in table['aliases']:
        key = identity(row)
        if key in identities or row['reportSymbol'] in symbols:
            raise ValueError('Duplicate alias identity or report symbol')
        identities.add(key)
        symbols.add(row['reportSymbol'])
        primary = closure(root, row)
        definition(primary, row['sourceSymbol'])
        records.append(dict(row))
    return sorted(records, key=lambda row: row['reportSymbol'])


def header_bytes(records):
    return ''.join('#define ' + row['reportSymbol'] + ' ' + row['sourceSymbol'] + '\n'
                   for row in records).encode('utf-8')


def generate_header(root):
    root = Path(root).resolve()
    records = load_records(root)
    header = root / HEADER
    header.parent.mkdir(parents=True, exist_ok=True)
    header.write_bytes(header_bytes(records))
    return records


def load_aliases(root):
    root = Path(root).resolve()
    records = load_records(root)
    header = root / HEADER
    if not header.is_file() or header.read_bytes() != header_bytes(records):
        raise ValueError('Generated ByteMatch names header is missing or stale')
    return {row['reportSymbol']: row['sourcePath'] for row in records}


def accepted_manifest(root):
    path = root / 'public/accepted-functions.json'
    manifest = json.loads(path.read_text(encoding='utf-8-sig'))
    if manifest.get('schemaVersion') != 1 or not isinstance(manifest.get('functions'), list):
        raise ValueError('Expected a frozen accepted-source manifest')
    rows = {row['id']: row for row in manifest['functions']}
    if len(rows) != len(manifest['functions']):
        raise ValueError('Duplicate frozen accepted function identity')
    return rows, digest(path)


def full_identity(row):
    if any(field not in row for field in IDENTITY_FIELDS):
        raise ValueError('Definition needs the complete physical function identity')
    return row['program'] or '', row['processor'], row['module'], row['mode'], int(row['address'], 0)


def compiler_closure(root, row):
    from public_manifest import compiler_flags, include_names
    pins = {source_path(root, row['sourceUnit']): row['sourceSha256']}
    for entry in row.get('sourceDependencies', []):
        path = source_path(root, entry['path'])
        if path in pins and pins[path] != entry['sha256']:
            raise ValueError('Conflicting frozen include pins')
        pins[path] = entry['sha256']
    for path, expected in pins.items():
        if digest(path) != expected:
            raise ValueError('Frozen translation unit or include hash differs: ' + str(path))
    unused, directories = compiler_flags(root, row['compilerFlags'])
    pending, seen = [source_path(root, row['sourceUnit'])], set()
    while pending:
        path = pending.pop()
        if path in seen:
            continue
        seen.add(path)
        for delimiter, name in include_names(path):
            locations = ([path.parent] if delimiter == '"' else []) + directories
            found = None
            for directory in locations:
                candidate = (directory / name).resolve()
                if not candidate.is_relative_to(root):
                    raise ValueError('Compiler include escapes the public root')
                if candidate.is_file():
                    found = candidate
                    break
            if found is None or found not in pins:
                raise ValueError('Compiler include is missing or unpinned: ' + name)
            pending.append(found)
    return pins, seen


def precise_definition(root, row, symbol):
    pins, reachable = compiler_closure(root, row)
    choices = [(path, definition_matches(path, symbol)) for path in reachable]
    choices = [(path, matches) for path, matches in choices if matches]
    if len(choices) != 1 or len(choices[0][1]) != 1:
        raise ValueError('Definition is missing or ambiguous within its actual compiler include closure: ' + symbol)
    path = choices[0][0]
    return path, pins[path]


def load_definition_records(root):
    root = Path(root).resolve()
    rows, manifest_hash = accepted_manifest(root)
    table = json.loads((root / DEFINITIONS).read_text(encoding='utf-8-sig'))
    if table.get('schemaVersion') != 1 or table.get('acceptedManifestSha256') != manifest_hash:
        raise ValueError('Definition table is stale for this frozen accepted manifest')
    result, seen = [], set()
    for entry in table['definitions']:
        row = rows.get(entry['id'])
        if row is None or row.get('states', {}).get('functionMatched') is not True or row.get('states', {}).get('moduleLinked') is not True:
            raise ValueError('Definition entry is not a closed accepted function')
        frozen_identity = {**row, 'program': row.get('program') or ''}
        if full_identity(entry) != full_identity(frozen_identity):
            raise ValueError('Definition crosses its frozen physical function identity')
        if entry['translationUnit'] != row['sourceUnit'] or entry['translationUnitSha256'] != row['sourceSha256']:
            raise ValueError('Definition translation unit differs from its accepted source pin')
        symbol = entry['reportSymbol']
        if not isinstance(symbol, str) or not re.fullmatch(r'[A-Za-z_]\w*', symbol):
            raise ValueError('Definition table needs an explicit C report symbol')
        key = entry['id'], symbol
        if key in seen:
            raise ValueError('Duplicate accepted function definition mapping')
        seen.add(key)
        path, expected = precise_definition(root, row, symbol)
        if entry['definitionPath'] != path.relative_to(root).as_posix() or entry['definitionSha256'] != expected:
            raise ValueError('Definition path/hash differs from the unique frozen include definition')
        result.append(dict(entry))
    return result


def load_definition_paths(root):
    return {(entry['id'], entry['reportSymbol']): entry['definitionPath'] for entry in load_definition_records(root)}


def generate_definitions(root, report_path):
    root = Path(root).resolve()
    report_path = (root / report_path).resolve()
    if not report_path.is_relative_to(root):
        raise ValueError('Definition input report must remain beneath the public root')
    report = json.loads(report_path.read_text(encoding='utf-8-sig'))
    rows, manifest_hash = accepted_manifest(root)
    locations = {}
    for row in rows.values():
        key = row.get('program') or '', row['processor'], row['module'], int(row['address'], 0)
        locations.setdefault(key, []).append(row)
    entries = []
    for unit in report['units']:
        if unit.get('metadata', {}).get('complete') is not True:
            continue
        physical = re.search(r'/(host|child)/(arm7|arm9)/([^/]+)/([0-9a-f]{8})$', unit['name'])
        if not physical:
            raise ValueError('Matched report unit lacks its physical namespace')
        program = '' if physical[1] == 'host' else 'dwc/utility.bin/move/child.srl'
        for function in unit.get('functions', []):
            offset = str(function.get('address', '0'))
            address = int(physical[4], 16) + int(offset, 16 if offset.startswith('0x') else 10)
            candidates = locations.get((program, physical[2], physical[3], address), [])
            if len(candidates) != 1:
                raise ValueError('Report function is absent or ambiguous in the accepted manifest')
            row = candidates[0]
            primary = source_path(root, row['sourceUnit'])
            if primary.suffix.lower() != '.c':
                continue
            if len(definition_matches(primary, function['name'])) == 1:
                continue
            if int(function['size']) != row['bytes']:
                raise ValueError('Report function extent differs from its accepted identity')
            definition_path, expected = precise_definition(root, row, function['name'])
            entries.append(dict(id=row['id'], program=program, processor=row['processor'], module=row['module'],
                                mode=row['mode'], address=f"0x{int(row['address'], 0):08x}", reportSymbol=function['name'],
                                translationUnit=row['sourceUnit'], translationUnitSha256=row['sourceSha256'],
                                definitionPath=definition_path.relative_to(root).as_posix(), definitionSha256=expected))
    table = dict(schemaVersion=1, generatedBy='public_tools/source_links.py', acceptedManifestSha256=manifest_hash,
                 sourceCreditAdded=0, definitions=sorted(entries, key=lambda entry: (entry['id'], entry['reportSymbol'])))
    (root / DEFINITIONS).write_text(json.dumps(table, indent=2) + '\n', encoding='utf-8')
    return load_definition_records(root)


def main():
    parser = argparse.ArgumentParser(description='Generate or check ByteMatch source-display aliases without editing compiler inputs.')
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--write-header', action='store_true')
    parser.add_argument('--write-definitions', action='store_true')
    parser.add_argument('--report', type=Path, default=Path('build/B2JJ-diagnostic/report.json'))
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.write_header:
            generate_header(root)
        if args.write_definitions:
            generate_definitions(root, args.report)
        aliases = load_aliases(root)
        definitions = load_definition_records(root) if (root / DEFINITIONS).is_file() else []
        print(json.dumps(dict(schemaVersion=1, status='source-links-passed', header=HEADER,
                              aliases=load_records(root), sourcePaths=aliases,
                              preciseAcceptedDefinitions=len(definitions), sourceCreditAdded=0), indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
