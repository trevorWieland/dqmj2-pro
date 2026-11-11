#!/usr/bin/env python3
"""Classify the weak inverse rows: matched rows whose sourceUnit file exists but
carries neither the address nor the ledger symbol.

Buckets: PAIRED-CERTAIN, PAIRED-PROBABLE, NO-DEFINITION, DATA-OR-STUB.
The ledger is never edited. Output: work/inverse-weak.json and (optionally) a doc.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from elftools.elf.elffile import ELFFile

ROOT = Path(__file__).resolve().parent.parent
CALL_KEYWORDS = {'if', 'for', 'while', 'switch', 'return', 'sizeof', 'do', 'else'}
DATA_TOKENS = ('= {', '= {', '.word', '.byte', '.short', '.hword', 'const ', 'static const',
               'unsigned char ', 'unsigned int ', 'struct ', 'typedef struct')
C_DEF = re.compile(
    r'^\s*(?:static\s+|inline\s+|extern\s+)*[A-Za-z_][A-Za-z0-9_\s\*]*?\b'
    r'([A-Za-z_][A-Za-z0-9_]*)\s*\(([^;{}]*)\)\s*\{\s*$', re.M)
ASM_GLOBAL = re.compile(r'^\s*\.global\s+([A-Za-z_][A-Za-z0-9_]*)', re.M)
ASM_LABEL = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):', re.M)



COMPILER = 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
ASSEMBLER = 'tools/mwccarm/mwccarm/2.0/base/mwasmarm.exe'
BASE_FLAGS = ['-O2', '-enum', 'int', '-char', 'signed', '-str', 'noreuse', '-proc', 'arm946e',
              '-gccext,on', '-fp', 'soft', '-inline', 'off', '-Cpp_exceptions', 'off',
              '-RTTI', 'off', '-interworking', '-w', 'off', '-sym', 'on', '-gccinc', '-nolink',
              '-msgstyle', 'gcc']


def measure_sizes(root, path, mode):
    """Return {symbol: bytes} measured by compiling/assembling the unit, or {}."""
    with tempfile.TemporaryDirectory() as temp:
        obj = Path(temp) / 'unit.o'
        if path.suffix.lower() == '.s':
            command = [str(root / ASSEMBLER), '-proc', 'arm5TE', '-o', str(obj), str(path)]
        else:
            flags = list(BASE_FLAGS) + (['-thumb'] if mode == 'thumb' else [])
            command = [str(root / COMPILER)] + flags + ['-c', str(path), '-o', str(obj)]
        try:
            result = subprocess.run(command, capture_output=True, text=True, timeout=120)
        except (OSError, subprocess.SubprocessError):
            return {}
        if result.returncode != 0 or not obj.is_file():
            return {}
        try:
            with open(obj, 'rb') as handle:
                elf = ELFFile(handle)
                section = elf.get_section_by_name('.text')
                if section is None:
                    return {}
                symbols = [(s.name, s['st_value'], s['st_size'])
                           for s in elf.get_section_by_name('.symtab').iter_symbols()
                           if s.name and s['st_info']['type'] == 'STT_FUNC']
                sizes = {name: size for name, _value, size in symbols if size}
                if sizes:
                    return sizes
                ordered = sorted((value, name) for name, value, _size in symbols)
                sizes = {}
                for index, (value, name) in enumerate(ordered):
                    end = ordered[index + 1][0] if index + 1 < len(ordered) else section['sh_size']
                    sizes[name] = end - value
                return sizes
        except Exception:
            return {}


def weak_rows(root, ledger):
    rows = []
    for row in ledger:
        if not row['states']['functionMatched']:
            continue
        unit = row.get('sourceUnit')
        if not unit:
            continue
        path = root / unit
        if not path.is_file():
            continue
        body = path.read_text(encoding='utf-8', errors='replace').lower()
        key = f"{int(row['address'], 16):08x}"
        symbol = (row.get('symbol') or '').lower()
        strong = key in body or (symbol and symbol in body)
        if not strong:
            rows.append(row)
    return rows


def definitions(path, text):
    names = []
    if path.suffix.lower() == '.s':
        for name in ASM_GLOBAL.findall(text):
            names.append(name)
        if not names:
            names = [n for n in ASM_LABEL.findall(text) if not n.startswith('local_')]
    else:
        for match in C_DEF.finditer(text):
            name = match.group(1)
            if name not in CALL_KEYWORDS:
                names.append(name)
    seen = []
    for name in names:
        if name not in seen:
            seen.append(name)
    return seen


def bucket_for(path, text, names, symbols):
    matched = [(name, symbols[name]) for name in names if name in symbols]
    if matched:
        name, owners = matched[0]
        return 'PAIRED-PROBABLE', {
            'definition': name,
            'owners': [dict(address=owner['address'], module=owner['module'],
                            bytes=owner['bytes'], symbol=owner.get('symbol'))
                       for owner in owners],
            'evidence': 'definition name equals a ledger symbol; weak row shares the file '
                        'without its own name (unique match)' if len(matched) == 1 else
                        'definition name equals a ledger symbol (first of %d)' % len(matched),
        }
    if names:
        return 'NO-DEFINITION', {
            'definitions': names[:8],
            'evidence': 'function definition(s) present but none maps to a ledger symbol',
        }
    suffix = path.suffix.lower()
    if suffix in ('.h', '.inc'):
        return 'DATA-OR-STUB', {'kind': 'header'}
    if any(token in text for token in DATA_TOKENS):
        return 'DATA-OR-STUB', {'kind': 'data'}
    if len(text) < 200:
        return 'DATA-OR-STUB', {'kind': 'stub', 'bytes': len(text)}
    return 'NO-DEFINITION', {'evidence': 'no function definition, no data block'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--report', default=None)
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()
    ledger = [json.loads(line) for line in
              (root / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines()
              if line.strip()]
    symbols = {}
    for row in ledger:
        if row.get('symbol'):
            symbols.setdefault(row['symbol'], []).append(row)

    weak = weak_rows(root, ledger)
    results = []
    measured = {}
    for index, row in enumerate(weak):
        unit = row['sourceUnit']
        path = root / unit
        text = path.read_text(encoding='utf-8', errors='replace')
        names = definitions(path, text)
        bucket, evidence = bucket_for(path, text, names, symbols)
        if bucket == 'NO-DEFINITION' and names:
            if unit not in measured:
                measured[unit] = measure_sizes(root, path, row.get('mode'))
            sizes = measured[unit]
            candidates = [name for name in names if sizes.get(name) == row['bytes']]
            if len(candidates) == 1:
                bucket = 'PAIRED-PROBABLE'
                evidence = {'definition': candidates[0],
                            'evidence': 'measured definition size equals row bytes (unique)',
                            'measured': sizes.get(candidates[0])}
            elif len(candidates) > 1:
                evidence = {'definitions': candidates,
                            'evidence': 'several definitions match the row size; ambiguous'}
            else:
                evidence = {'definitions': names[:8],
                            'evidence': 'function definition(s) present, no unique size match',
                            'measured': sizes}
        results.append({'address': row['address'], 'module': row['module'],
                        'bytes': row['bytes'], 'mode': row.get('mode'),
                        'symbol': row.get('symbol'), 'sourceUnit': row['sourceUnit'],
                        'bucket': bucket, 'evidence': evidence})

    counts = {}
    byte_counts = {}
    for item in results:
        counts[item['bucket']] = counts.get(item['bucket'], 0) + 1
        byte_counts[item['bucket']] = byte_counts.get(item['bucket'], 0) + item['bytes']
    report = {'generatedFrom': {'tool': 'ops/classify_weak_inverse.py',
                                'ledger': 'ledger/functions.jsonl'},
              'weakRows': len(results),
              'counts': counts, 'bytes': byte_counts,
              'buckets': {name: sorted([item for item in results if item['bucket'] == name],
                                       key=lambda item: -item['bytes'])
                          for name in ('PAIRED-CERTAIN', 'PAIRED-PROBABLE',
                                       'NO-DEFINITION', 'DATA-OR-STUB')}}
    if args.report:
        Path(args.report).parent.mkdir(parents=True, exist_ok=True)
        Path(args.report).write_text(json.dumps(report, indent=1) + '\n', encoding='utf-8')
    print('weak rows:', len(results))
    for name in ('PAIRED-CERTAIN', 'PAIRED-PROBABLE', 'NO-DEFINITION', 'DATA-OR-STUB'):
        print('  %-16s %3d rows %6d B' % (name, counts.get(name, 0), byte_counts.get(name, 0)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
