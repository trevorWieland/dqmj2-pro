"""Dump a documented data table to CSV from a private module image.

The data dictionary (``docs/data/index.json``) records each table's module, address,
stride and field layout.  This tool turns that into something a modder can open: it
reads the module image out of a private checkout, slices the table and writes CSV.

    python public_tools/data_dump.py --root <private-checkout> --list
    python public_tools/data_dump.py --root <private-checkout> --table species_roster --count 16
    python public_tools/data_dump.py --root <private-checkout> --table species_roster --count 16 \
        --out build/species.csv

Only tables with a proven address are dumpable; a table whose base is ``unknown`` is
reported as such instead of being guessed.  WRAM structures (the ARM7 sound views) are
also refused: they do not exist in a ROM image.  Generated CSV is never committed.
"""

import argparse
import csv
import io
import json
import sys
from pathlib import Path

# The dictionary is a repository artifact, while --root points at the private checkout
# that carries manifest.json and the module images.
INDEX = Path(__file__).absolute().parents[1] / 'docs/data/index.json'
WRAM_BASE = 0x03000000
MODES = ('dumpable', 'no-address', 'wram-structure', 'unknown-stride', 'no-image')
WIDTHS = {'u8': 1, 's8': 1, 'u16': 2, 's16': 2, 'u32': 4, 's32': 4, 'int': 4, 'uint': 4}
SIGNED = {'s8', 's16', 's32', 'int'}


def load_index(root):
    path = INDEX if INDEX.is_absolute() else root / INDEX
    if not path.is_file():
        raise SystemExit('data dictionary index not found: ' + str(path))
    document = json.loads(path.read_text(encoding='utf-8'))
    tables = document.get('tables')
    if not isinstance(tables, list):
        raise SystemExit('data dictionary index has no tables')
    return {table['id']: table for table in tables}


def manifest_module(root, name):
    path = root / 'manifest.json'
    if not path.is_file():
        raise SystemExit('manifest.json is required to locate the module image: ' + str(path))
    manifest = json.loads(path.read_text(encoding='utf-8-sig'))
    for module in manifest.get('modules', []):
        if module['name'] == name:
            return module
    raise SystemExit('unknown module in the data dictionary: ' + name)


def dumpability(table, root=None):
    address = table.get('address')
    if address in (None, 'unknown'):
        return 'no-address'
    base = int(address, 0)
    if base >= WRAM_BASE:
        return 'wram-structure'
    if not isinstance(table.get('stride'), int) or table['stride'] <= 0:
        return 'unknown-stride'
    if root is not None:
        # The address must actually live in a captured module image; a symbol name can
        # name a range the current image set does not cover.
        try:
            module = manifest_module(root, table['module'])
            image = (root / (module.get('binary') or '')).read_bytes()
            module_base = int(module.get('loadAddressBase') or module['base'], 0)
        except (SystemExit, OSError, KeyError):
            return 'no-image'
        if not (module_base <= base and base + int(table['stride']) <= module_base + len(image)):
            return 'no-image'
    return 'dumpable'


def element_type(field, stride):
    """Return (width, signed) for a field, or (stride, False) for a blob field."""
    text = str(field.get('type') or '')
    name = text.split('[')[0].strip()
    if name in WIDTHS:
        return WIDTHS[name], name in SIGNED
    count = 0
    if '[' in text and text.endswith(']'):
        try:
            count = int(text[text.index('[') + 1:-1], 0)
        except ValueError:
            count = 0
    if count and WIDTHS.get(name):
        return WIDTHS[name] * count, name in SIGNED
    return stride, False


def read_table(root, table, count, start=0):
    module = manifest_module(root, table['module'])
    image_path = root / (module.get('binary') or module.get('originalImage') or '')
    if not image_path.is_file():
        raise SystemExit('module image is unavailable: ' + str(image_path))
    image = image_path.read_bytes()
    base = int(module.get('loadAddressBase') or module['base'], 0)
    address = int(table['address'], 0)
    stride = int(table['stride'])
    offset = address - base + start * stride
    if offset < 0 or offset + count * stride > len(image):
        raise SystemExit('table range lies outside the module image')
    rows = []
    for index in range(count):
        record = image[offset + index * stride:offset + (index + 1) * stride]
        row = {'index': index, 'address': '0x%08x' % (address + (start + index) * stride)}
        for field in table.get('fields') or []:
            position = int(field['offset'])
            width, signed = element_type(field, stride - position)
            raw = record[position:position + width]
            if not raw:
                row[field['name']] = ''
                continue
            if len(raw) in (1, 2, 4):
                row[field['name']] = int.from_bytes(raw, 'little', signed=signed)
            else:
                row[field['name']] = raw.hex()
        if not (table.get('fields') or []):
            row['raw'] = record.hex()
        rows.append(row)
    return rows, base, module


def main():
    parser = argparse.ArgumentParser(description='Dump a documented data table to CSV.')
    parser.add_argument('--root', type=Path, default=Path('.'), help='checkout with docs/data/index.json')
    parser.add_argument('--table', help='table id from docs/data/index.json')
    parser.add_argument('--list', action='store_true', help='list tables and whether they are dumpable')
    parser.add_argument('--count', type=int, default=16, help='records to dump (default 16)')
    parser.add_argument('--start', type=int, default=0, help='first record index (default 0)')
    parser.add_argument('--out', type=Path, help='CSV path (default stdout)')
    args = parser.parse_args()
    root = args.root.resolve()
    tables = load_index(root)
    if args.list or not args.table:
        for name, table in tables.items():
            state = dumpability(table, root)
            print('%-24s %-14s %-12s %s' % (name, table.get('module'), state, table.get('title', '')))
        return 0
    table = tables.get(args.table)
    if table is None:
        print('unknown table: ' + args.table, file=sys.stderr)
        return 2
    state = dumpability(table, root)
    if state != 'dumpable':
        print('%s is not dumpable: %s' % (args.table, state), file=sys.stderr)
        return 1
    try:
        rows, base, module = read_table(root, table, args.count, args.start)
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 1
    fieldnames = ['index', 'address'] + [field['name'] for field in table.get('fields') or []]
    if not (table.get('fields') or []):
        fieldnames.append('raw')
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    text = buffer.getvalue()
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding='utf-8', newline='\n')
        print('wrote %d row(s) to %s' % (len(rows), args.out))
    else:
        print(text, end='')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
