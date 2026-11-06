import argparse
import hashlib
import json
import re
from pathlib import Path, PurePosixPath


TABLE = 'public_tools/source_aliases.json'
HEADER = 'include/bytematch_names.h'
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


def definition(path, name):
    text = remove_tokens(path.read_text(encoding='utf-8-sig'), literals=True)
    pattern = re.compile(r'\b' + re.escape(name) + r'\s*\([^;{}]*\)\s*\{')
    matches = [match for match in pattern.finditer(text)
               if text[:match.start()].count('{') == text[:match.start()].count('}')]
    if len(matches) != 1:
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


def main():
    parser = argparse.ArgumentParser(description='Generate or check ByteMatch source-display aliases without editing compiler inputs.')
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--write-header', action='store_true')
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        if args.write_header:
            generate_header(root)
        aliases = load_aliases(root)
        print(json.dumps(dict(schemaVersion=1, status='source-links-passed', header=HEADER,
                              aliases=load_records(root), sourcePaths=aliases, sourceCreditAdded=0), indent=2))
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, str(error) + '\n')


if __name__ == '__main__':
    main()
