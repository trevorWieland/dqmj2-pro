"""Screen unclaimed rows for a module before authoring a packet.

Three rules have each cost a round of rework, so they live in a tool rather than in
a checklist:

1. **Whole-tree duplicate grep.** A row is skipped when its address string appears
   anywhere under ``src/`` (``.c``, ``.h``, ``.s``, ``.inc``, ``.cpp``), including
   ``src/transplants/`` and every batch directory. On ov006 this excludes 345 of
   671 unmatched rows — the ledger lags the source tree and the tree is
   authoritative.
2. **BL vs BLX.** Rows containing ``blx`` are toolchain-blocked (the immediate
   encoder is incomplete) and are excluded; rows with ``bl`` are authorable now that
   the Thumb BL encoder landed. Screening uses ``ops/disasm.py`` in the row's own
   mode, so ARM and Thumb rows are judged by their real instruction stream.
3. **Boot floor.** Rows below the module's first real function are codegen-hostile
   and are excluded by a per-module floor.

Usage
-----
    python ops/screen_candidates.py --module ov006
    python ops/screen_candidates.py --module ov006 --max-bytes 120 --json out.json

Output is a human table plus, with --json, a machine-readable list of ready rows.
Exit status is 0 when at least one row is ready.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ('.c', '.h', '.s', '.inc', '.cpp')
# First authorable address per module; anything below is boot-floor scaffolding.
BOOT_FLOOR = {'ov006': 0x021D8000, 'ov000': 0x021D8000, 'ov001': 0x021D8000}


def source_corpus(root):
    corpus = {}
    for path in (root / 'src').rglob('*'):
        if path.suffix.lower() in SOURCES and path.is_file():
            try:
                corpus[path.relative_to(root).as_posix()] = path.read_text(
                    encoding='utf-8', errors='replace')
            except OSError:
                continue
    return corpus


def screen(root, module, max_bytes, corpus):
    ledger = [json.loads(line) for line in
              (root / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines() if line]
    rows = [row for row in ledger
            if row.get('processor') == 'arm9' and row.get('module') == module
            and row['states'].get('functionMatched') is False and row.get('bytes')]
    floor = BOOT_FLOOR.get(module, 0)
    ready, duplicates, blx_blocked, boot = [], [], [], []
    for row in rows:
        address = int(row['address'], 16)
        key = f'{address:08x}'
        if any(key in text for text in corpus.values()):
            duplicates.append((address, row['bytes'], row['mode']))
            continue
        if address < floor:
            boot.append((address, row['bytes'], row['mode']))
            continue
        if max_bytes and row['bytes'] > max_bytes:
            continue
        result = subprocess.run([sys.executable, str(root / 'ops/disasm.py'), '--module', module,
                                 '--address', hex(address), '--bytes', str(row['bytes']),
                                 '--mode', row['mode'], '--root', str(root)],
                                capture_output=True, text=True)
        listing = result.stdout.lower()
        if result.returncode != 0:
            blx_blocked.append((address, row['bytes'], row['mode']))
            continue
        if 'blx' in listing:
            blx_blocked.append((address, row['bytes'], row['mode']))
            continue
        ready.append((address, row['bytes'], row['mode'],
                      'bl' in listing.replace('.', ' ').split()))
    return rows, ready, duplicates, blx_blocked, boot


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--max-bytes', type=int, default=0)
    parser.add_argument('--json', dest='json_path')
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    corpus = source_corpus(root)
    rows, ready, duplicates, blx_blocked, boot = screen(root, args.module, args.max_bytes, corpus)

    print(f'src files scanned: {len(corpus)}')
    print(f'unmatched {args.module} rows: {len(rows)}')
    print(f'  already defined under src/ (whole-tree grep): {len(duplicates)}')
    print(f'  boot floor (below {BOOT_FLOOR.get(args.module, 0):#x}):        {len(boot)}')
    print(f'  blx-bearing (toolchain-blocked):              {len(blx_blocked)}')
    print(f'  ready to author:                              {len(ready)}')
    ready.sort(key=lambda item: (item[1], item[0]))
    for address, size, mode, has_bl in ready[:30]:
        print(f'    {address:08x} {size:5d} B {mode:5s} {"bl" if has_bl else "  "}')
    if args.json_path:
        Path(args.json_path).write_text(json.dumps({
            'module': args.module,
            'unmatched': len(rows),
            'duplicates': len(duplicates),
            'boot_floor': len(boot),
            'blx_blocked': len(blx_blocked),
            'ready': [{'address': f'{a:#010x}', 'bytes': s, 'mode': m} for a, s, m, _ in ready],
        }, indent=1) + '\n')
        print(f'report written: {args.json_path}')
    return 0 if ready else 1


if __name__ == '__main__':
    sys.exit(main())
