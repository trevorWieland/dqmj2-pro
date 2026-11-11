"""Screen unclaimed rows for a module before authoring a packet.

Four rules have each cost a round of rework, so they live in a tool rather than in
a checklist, and each one is evaluated **independently** so no bucket can hide
another:

1. **Duplicate detection requires a definition, not a mention.** A row is a
   duplicate only when some file under ``src/`` *defines* a symbol for that address:

   * a ``.c`` function definition whose header starts at column 0 and names
     ``native_(<module>_)?<addr>`` — extern declarations, call sites and comments do
     not count;
   * in ``.s``, an exported symbol for that name (``.global``/``.type`` or a bare
     label);
   * a data symbol (``native_data_...<addr>``) is classified separately, because a
     data definition does not claim the function body.

   Duplicates are bucketed: **same-module body**, **other-module body at the same
   address** (still a real duplicate for credit purposes) and **data symbol**.
2. **BLX-immediate is authorable.** The acceptance path expands
   ``R_ARM_THM_CALL`` according to the measured callee mode: BL for a Thumb target,
   BLX-immediate for an ARM target (``public_tools/test_thumb_branches.py`` pins
   both). ``blx`` rows are therefore counted and reported but do not block.
3. **Boot floor is a documented range**, not a per-module dictionary. Any row below
   :data:`BOOT_FLOOR` is scaffolding the project does not author by hand.
4. **A disassembly failure is "unknown"**, never silently folded into ``blx``.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ('.c', '.s', '.inc', '.cpp')

# The overlay loads at 0x021d7240; everything before this address is loader
# scaffolding rather than ordinary game code, and the project does not author it by
# hand. Documented here once instead of a per-module dictionary.
BOOT_FLOOR = 0x021D8000

ADDRESS_SUFFIX = re.compile(r'([0-9a-f]{8})$')
DEFINITION = re.compile(r'^(?:[A-Za-z_][\w \t\*]*[\s\*]+)?(native_[A-Za-z0-9_]+)\s*\(')
ASM_EXPORT = re.compile(r'^\s*\.(?:global|globl|type)\s+(native_[A-Za-z0-9_]+)')
ASM_LABEL = re.compile(r'^(native_[A-Za-z0-9_]+):')
COMMENTS = re.compile(r'/\*.*?\*/|//[^\n]*', re.S)


def strip_comments(text, suffix):
    if suffix in ('.c', '.cpp', '.inc'):
        return COMMENTS.sub('', text)
    return re.sub(r'@[^\n]*|;[^\n]*', '', text)


def module_of(name):
    """Module embedded in a ``native_<module>_<addr>`` name, or None."""
    match = re.match(r'native_(?:fn_|data_)?(.+?)_[0-9a-f]{8}$', name)
    return match.group(1).replace('_', '-') if match else None


def definitions(root):
    """Map address string -> list of (kind, path, name) definition records."""
    found = {}
    for path in (root / 'src').rglob('*'):
        suffix = path.suffix.lower()
        if suffix not in SOURCES or not path.is_file():
            continue
        try:
            text = strip_comments(path.read_text(encoding='utf-8', errors='replace'), suffix)
        except OSError:
            continue
        relative = path.relative_to(root).as_posix()
        if suffix == '.s':
            for line in text.splitlines():
                match = ASM_EXPORT.match(line) or ASM_LABEL.match(line)
                if not match:
                    continue
                name = match.group(1)
                address = ADDRESS_SUFFIX.search(name)
                if address:
                    found.setdefault(address.group(1), []).append((suffix, relative, name))
            continue
        lines = text.splitlines()
        for index, line in enumerate(lines):
            if line[:1] in (' ', '\t') or not line:
                continue          # column 0 only: definitions, not locals or calls
            if line.rstrip().endswith(';') or line.startswith('extern'):
                continue          # a declaration/prototype is a mention, not a body
            match = DEFINITION.match(line)
            if not match:
                continue
            # A body opens a brace on this line or the next non-blank one.
            tail = line[match.end() - 1:]
            if '{' not in tail:
                following = next((candidate for candidate in lines[index + 1:] if candidate.strip()),
                                 '')
                if '{' not in following:
                    continue
            name = match.group(1)
            address = ADDRESS_SUFFIX.search(name)
            if address:
                found.setdefault(address.group(1), []).append((suffix, relative, name))
        # data definitions: `type native_data_<...>_<addr>[...] = ...` or a bare
        # declaration with initialiser; treated as a data record, not a body.
        for match in re.finditer(r'^(?:[A-Za-z_][\w \t\*]*[\s\*]+)?'
                                 r'(native_data_[A-Za-z0-9_]+)\s*(?:\[[^\]]*\])?\s*=',
                                 text, re.M):
            name = match.group(1)
            address = ADDRESS_SUFFIX.search(name)
            if address:
                found.setdefault(address.group(1), []).append(('data', relative, name))
    return found


def classify(records, module):
    """Bucket the definition records for one address."""
    buckets = {'same-module body': [], 'other-module body': [], 'data symbol': []}
    for suffix, path, name in records:
        if name.startswith('native_data_') or suffix == 'data':
            buckets['data symbol'].append(f'{path}:{name}')
        elif module_of(name) == module:
            buckets['same-module body'].append(f'{path}:{name}')
        else:
            buckets['other-module body'].append(f'{path}:{name}')
    return buckets


def screen(root, module, max_bytes):
    ledger = [json.loads(line) for line in
              (root / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines() if line]
    rows = [row for row in ledger
            if row.get('processor') == 'arm9' and row.get('module') == module
            and row['states'].get('functionMatched') is False and row.get('bytes')]
    defs = definitions(root)
    stats = {'boot floor': [], 'duplicate': [], 'unknown': [],
             'over max bytes': [], 'ready': [], 'blx immediate': []}
    for row in rows:
        address = int(row['address'], 16)
        key = f'{address:08x}'
        entry = {'address': address, 'bytes': row['bytes'], 'mode': row['mode']}
        # Each rule is evaluated independently; a row can trip several.
        flags = []
        if address < BOOT_FLOOR:
            flags.append('boot floor')
        buckets = classify(defs.get(key, []), module)
        if any(buckets.values()):
            entry['buckets'] = {name: items for name, items in buckets.items() if items}
            flags.append('duplicate')
        if max_bytes and row['bytes'] > max_bytes:
            flags.append('over max bytes')
        result = subprocess.run([sys.executable, str(root / 'ops/disasm.py'), '--module', module,
                                 '--address', hex(address), '--bytes', str(row['bytes']),
                                 '--mode', row['mode'], '--root', str(root)],
                                capture_output=True, text=True)
        if result.returncode != 0:
            flags.append('unknown')          # never counted as blx
        else:
            listing = result.stdout.lower()
            # BLX-immediate names a target address; `blx rN` is a register call.
            if re.search(r'\bblx\s+0x[0-9a-f]+', listing):
                stats.setdefault('blx immediate', []).append(entry)
        if not flags:
            flags.append('ready')
        for flag in flags:
            stats[flag].append(entry)
    return rows, stats


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--max-bytes', type=int, default=0)
    parser.add_argument('--json', dest='json_path')
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    rows, stats = screen(root, args.module, args.max_bytes)

    print(f'unmatched {args.module} rows: {len(rows)}')
    print('each rule is evaluated independently, so the counts overlap:')
    print(f'  boot floor (below {BOOT_FLOOR:#x}):     {len(stats["boot floor"])}')
    duplicates = stats['duplicate']
    same = sum(1 for entry in duplicates if entry['buckets'].get('same-module body'))
    other = sum(1 for entry in duplicates if entry['buckets'].get('other-module body'))
    data = sum(1 for entry in duplicates if entry['buckets'].get('data symbol'))
    print(f'  duplicate definitions:                {len(duplicates)}')
    print(f'    same-module body:                   {same}')
    print(f'    other-module body (same address):   {other}')
    print(f'    data symbol:                        {data}')
    print(f'  blx immediate (authorable):           {len(stats["blx immediate"])}')
    print(f'  unknown (disassembly failed):         {len(stats["unknown"])}')
    print(f'  over --max-bytes:                     {len(stats["over max bytes"])}')
    print(f'  READY (no rule tripped):              {len(stats["ready"])}')

    ready = sorted(stats['ready'], key=lambda entry: (entry['bytes'], entry['address']))
    for entry in ready[:30]:
        print(f'    {entry["address"]:08x} {entry["bytes"]:5d} B {entry["mode"]}')
    if args.json_path:
        Path(args.json_path).write_text(json.dumps({
            'module': args.module,
            'unmatched': len(rows),
            'bootFloor': len(stats['boot floor']),
            'duplicates': len(duplicates),
            'duplicateBuckets': {'sameModule': same, 'otherModule': other, 'data': data},
            'blxImmediateAuthorable': len(stats['blx immediate']),
            'unknown': len(stats['unknown']),
            'ready': [{'address': f'{e["address"]:#010x}', 'bytes': e['bytes'], 'mode': e['mode']}
                      for e in ready],
        }, indent=1) + '\n')
        print(f'report written: {args.json_path}')
    return 0 if stats['ready'] else 1


if __name__ == '__main__':
    sys.exit(main())
