"""Generate the canonical symbol map from the private address ledger.

The private tree keeps one row per measured function in
``ledger/functions.jsonl`` and the module inventory in ``manifest.json``.  Both are
private inputs, so this tool lives under ``ops/`` rather than ``public_tools/`` and
is expected to run in a private checkout (or against one via ``--root``).

It writes two deterministic files:

* ``symbols.txt``  — one line per symbol: ``<address> <size> <module> <mode> <name>``
* ``symbols.json`` — the same rows plus processor, source and name provenance

The map is generated, never committed: a symbol map is a build product, so it is
emitted beneath ``build/`` and reproduced by running this tool.  Rows are sorted by
module, then by numeric address, so the output depends only on the inputs.

Names are resolved in this order, and every row records which step supplied it:

1. ``ledger``      — the ledger already carries a real (non-placeholder) symbol.
2. ``source``      — a ``.c``/``.s`` definition in the row's ``sourceUnit`` whose
                     identifier contains the row's address, or the only definition.
3. ``dependency``  — another ledger row's relocation targets this address with a
                     real symbol name (call sites name their callee).
4. ``definition-order`` — the row's source file defines exactly as many functions
                     as the ledger has rows for that file: pair them in address
                     order with definition order.
5. ``unresolved``  — none of the above; the placeholder is kept and ``--check``
                     fails for accepted rows in this state.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# A row is a placeholder when the ledger only has the address-derived form the
# spec names, ``func_XXXXXXXX``.  Module-qualified ledger symbols such as
# ``func_arm7_main_027e7e54`` are the canonical identity for that row.
PLACEHOLDER = re.compile(r'func_[0-9a-fA-F]{8}$')
# Names that are themselves address-derived (``func_…``/``native_fn_…``) are never
# used as a resolved name, whether they come from a dependency or a definition.
ADDRESS_NAME = re.compile(r'(?:func|native_fn)_(?:[A-Za-z0-9]+_)?[0-9a-fA-F]{8}$')
C_DEFINITION = re.compile(r'\b([A-Za-z_]\w*)\s*\([^;{}\n]*\)\s*\{')
C_SIGNATURE = re.compile(r'^\s*[A-Za-z_][\w \t\*]*?\b([A-Za-z_]\w*)\s*\([^;{}]*\)\s*$')
ASM_GLOBAL = re.compile(r'(?m)^\s*\.(?:global|globl)\s+([A-Za-z_]\w*)')
ASM_TYPE = re.compile(r'(?m)^\s*\.type\s+([A-Za-z_]\w*)\s*,\s*%?function')
STEM_ADDRESS = re.compile(r'[0-9a-f]{8}$', re.IGNORECASE)
TRAILING_ADDRESS = re.compile(r'([0-9a-fA-F]{8})$')
CONTROL = {'if', 'for', 'while', 'switch', 'do', 'else', 'return', 'sizeof', 'case', 'default', 'goto'}

# Accepted rows that stay at their address-derived ledger symbol because the only
# evidence that could name them (the original object symbol tables and the match
# reports) was pruned from the private tree.  Recorded so CI can gate on "no new
# unresolved" instead of absolute zero.
UNRESOLVED_BASELINE = 151

_DEFINITION_CACHE = {}


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ledger_rows(root):
    path = root / 'ledger/functions.jsonl'
    rows = [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]
    if not rows:
        raise ValueError('The address ledger is empty: ' + str(path))
    return rows


def module_inventory(root):
    manifest = read_json(root / 'manifest.json')
    modules = manifest.get('modules')
    if not isinstance(modules, list) or not modules:
        raise ValueError('manifest.json has no module inventory')
    return {module['name']: module for module in modules}


def address_of(value):
    """Return an address from a relocation target or an address-bearing name."""
    if isinstance(value, int):
        return value
    if not isinstance(value, str):
        return None
    if value.lower().startswith('0x'):
        try:
            return int(value, 16)
        except ValueError:
            return None
    found = TRAILING_ADDRESS.search(value)
    return int(found.group(1), 16) if found else None


def source_definitions(path):
    """Return the function identifiers declared by one source file.

    Parsed once per file: the ledger has one row per function, so multi-function
    files would otherwise be re-read for every row.  Only lines that can start a
    definition are examined, so large sources stay linear.
    """
    cached = _DEFINITION_CACHE.get(path)
    if cached is not None:
        return cached
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    if path.suffix == '.c':
        names = []
        lines = [line.rstrip() for line in text.splitlines()]
        for index, line in enumerate(lines):
            if not line or line.lstrip().startswith(('#', '//', '/*', '*')):
                continue
            if '{' in line:
                found = C_DEFINITION.search(line)
                if found and found.group(1) not in CONTROL:
                    names.append(found.group(1))
                    continue
            signature = C_SIGNATURE.match(line)
            if signature and signature.group(1) not in CONTROL:
                following = next((item for item in lines[index + 1:] if item.strip()), '')
                if following.lstrip().startswith('{'):
                    names.append(signature.group(1))
    elif path.suffix == '.s':
        names = ASM_GLOBAL.findall(text) + ASM_TYPE.findall(text)
    else:
        names = []
    seen, ordered = set(), []
    for name in names:
        if name not in seen:
            seen.add(name)
            ordered.append(name)
    _DEFINITION_CACHE[path] = ordered
    return ordered


def dependency_names(rows):
    """Map (module, address) to the real symbol names call sites use for it."""
    names = {}
    for row in rows:
        for dependency in row.get('dependencies') or []:
            symbol = dependency.get('symbol') or ''
            address = address_of(dependency.get('target'))
            module = dependency.get('targetModule') or row.get('module')
            if address is None or not symbol or ADDRESS_NAME.match(symbol):
                continue
            names.setdefault((module, address), {}).setdefault(symbol, 0)
            names[(module, address)][symbol] += 1
    return names


def pick_dependency_name(candidates, definitions):
    """Choose one name deterministically: a source definition, then the most used."""
    for name in definitions:
        if name in candidates:
            return name
    ranked = sorted(candidates.items(), key=lambda item: (-item[1], item[0]))
    return ranked[0][0] if ranked else None


def resolve_names(rows, root):
    """Return (names, provenance) for every ledger row, keyed by row index."""
    definitions_by_source = {}
    rows_by_source = {}
    for row in rows:
        source = (row.get('sourceUnit') or '').replace('\\', '/')
        if source:
            rows_by_source.setdefault(source, []).append(row)
    dependencies = dependency_names(rows)
    names, provenance = {}, {}

    def definitions(source):
        if source not in definitions_by_source:
            path = root / source
            definitions_by_source[source] = source_definitions(path) if path.is_file() else []
        return definitions_by_source[source]

    for index, row in enumerate(rows):
        symbol = row.get('symbol') or ''
        if symbol and not PLACEHOLDER.match(symbol):
            names[index], provenance[index] = symbol, 'ledger'
            continue
        source = (row.get('sourceUnit') or '').replace('\\', '/')
        address = int(row['address'], 0)
        short = '%08x' % (address & 0xFFFFFFFF)
        if source:
            declared = definitions(source)
            for name in declared:
                if short in name.lower():
                    names[index], provenance[index] = name, 'source'
                    break
            if index in names:
                continue
            if len(declared) == 1:
                names[index], provenance[index] = declared[0], 'source'
                continue
            stem = Path(source).stem
            if STEM_ADDRESS.search(stem) and short in stem.lower():
                names[index], provenance[index] = stem, 'source'
                continue
            candidates = dependencies.get((row.get('module'), address))
            if candidates:
                chosen = pick_dependency_name(candidates, declared)
                if chosen:
                    names[index], provenance[index] = chosen, 'dependency'
                    continue
        else:
            candidates = dependencies.get((row.get('module'), address))
            if candidates:
                chosen = pick_dependency_name(candidates, [])
                if chosen:
                    names[index], provenance[index] = chosen, 'dependency'
                    continue
        names[index], provenance[index] = symbol or ('unresolved_' + short), 'unresolved'

    # Pair the remaining rows with the remaining definitions when a file's ledger
    # row count matches its definition count exactly, in address/definition order.
    index_of = {id(row): index for index, row in enumerate(rows)}
    for source, source_rows in sorted(rows_by_source.items()):
        pending = sorted((int(row['address'], 0), index_of[id(row)]) for row in source_rows
                         if provenance[index_of[id(row)]] == 'unresolved')
        if not pending:
            continue
        declared = definitions(source)
        claimed = {names[index_of[id(row)]] for row in source_rows
                   if provenance[index_of[id(row)]] != 'unresolved'}
        spare = [name for name in declared if name not in claimed]
        if len(spare) == len(pending):
            for (address, index), name in zip(pending, spare):
                names[index], provenance[index] = name, 'definition-order'
    return names, provenance


def build_map(root):
    """Return the sorted symbol rows and the unresolved rows for one checkout."""
    rows = ledger_rows(root)
    modules = module_inventory(root)
    names, provenance = resolve_names(rows, root)
    symbols, unresolved = [], []
    for index, row in enumerate(rows):
        module = row.get('module')
        if module not in modules:
            raise ValueError('Ledger row names an unknown module: ' + str(module))
        accepted = bool(row.get('states', {}).get('functionMatched'))
        name, source_of_name = names[index], provenance[index]
        if source_of_name == 'unresolved':
            unresolved.append(dict(address=row['address'], module=module, symbol=row.get('symbol'),
                                   source=row.get('sourceUnit'), accepted=accepted))
        size = row.get('bytes')
        symbols.append(dict(address=row['address'], size=size if isinstance(size, int) else 0,
                            module=module, mode=row.get('mode') or 'unknown', name=name,
                            processor=row.get('processor'), source=row.get('sourceUnit') or None,
                            nameSource='address-fallback' if source_of_name == 'unresolved' else source_of_name,
                            accepted=accepted))
    symbols.sort(key=lambda item: (item['module'], int(item['address'], 0), item['name']))
    unresolved.sort(key=lambda item: (item['module'], int(item['address'], 0)))
    return symbols, unresolved


def render_text(symbols):
    return ''.join('%s %d %s %s %s\n' % (row['address'], row['size'], row['module'],
                                         row['mode'], row['name']) for row in symbols)


def render_json(symbols):
    return json.dumps(dict(schemaVersion=1, symbols=symbols), indent=1, sort_keys=True) + '\n'


def summary(symbols, unresolved):
    by_module, by_source = {}, {}
    for row in symbols:
        by_module[row['module']] = by_module.get(row['module'], 0) + 1
        by_source[row['nameSource']] = by_source.get(row['nameSource'], 0) + 1
    return dict(schemaVersion=1, rows=len(symbols), modules=len(by_module),
                byModule=dict(sorted(by_module.items())),
                accepted=sum(1 for row in symbols if row['accepted']),
                byNameSource=dict(sorted(by_source.items())),
                unresolved=len(unresolved),
                unresolvedAccepted=sum(1 for row in unresolved if row['accepted']),
                unresolvedRows=[{key: row[key] for key in ('address', 'module', 'symbol', 'source')}
                                for row in unresolved[:20]])


def write_outputs(output, symbols):
    output.mkdir(parents=True, exist_ok=True)
    (output / 'symbols.txt').write_text(render_text(symbols), encoding='utf-8', newline='\n')
    (output / 'symbols.json').write_text(render_json(symbols), encoding='utf-8', newline='\n')
    return dict(text=str(output / 'symbols.txt'), json=str(output / 'symbols.json'))


def main():
    parser = argparse.ArgumentParser(description='Generate the canonical symbol map from the address ledger.')
    parser.add_argument('--root', type=Path, default=Path('.'),
                        help='checkout that contains ledger/functions.jsonl and manifest.json')
    parser.add_argument('--out-dir', type=Path, default=Path('build/symbol-map'),
                        help='generated output directory (relative to --root)')
    parser.add_argument('--check', action='store_true',
                        help='verify naming only: fail when an accepted row has no resolvable name')
    parser.add_argument('--allow-unresolved', nargs='?', type=int, const=UNRESOLVED_BASELINE,
                        metavar='N', default=None,
                        help='with --check: allow up to N accepted rows to stay at their address-derived '
                             'symbol (default N=%d, the documented baseline), so the gate catches new '
                             'unresolved rows without demanding absolute zero' % UNRESOLVED_BASELINE)
    args = parser.parse_args()
    root = args.root.resolve()
    try:
        symbols, unresolved = build_map(root)
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2
    report = summary(symbols, unresolved)
    if not args.check:
        output = args.out_dir if args.out_dir.is_absolute() else root / args.out_dir
        report['output'] = write_outputs(output, symbols)
    print(json.dumps(report, indent=1))
    if args.check and args.allow_unresolved is None and report['unresolvedAccepted']:
        print('%d accepted row(s) have no resolvable name' % report['unresolvedAccepted'], file=sys.stderr)
        return 1
    if args.check and args.allow_unresolved is not None and report['unresolvedAccepted'] > args.allow_unresolved:
        print('%d accepted row(s) have no resolvable name, above the allowed %d'
              % (report['unresolvedAccepted'], args.allow_unresolved), file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
