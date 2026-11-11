"""Reconcile the private ledger against the public src/ tree.

The ledger's ``states.functionMatched`` flag is the input to the duplicate check, the
harvest filter and the permuter queue, so a stale flag silently misleads all three.
This tool answers one question per ledger row: does the public tree actually *define* a
symbol for that row's address?

It reports three buckets:

* **stale** — a definition exists in ``src/`` but the ledger says ``functionMatched`` is
  false (merged work the ledger has not absorbed);
* **inverse** — the ledger says matched but no definition exists (a lost or renamed
  source);
* **genuinely unmatched** — neither.

Nothing tracked is modified. The proposed ledger patch is a copy written under ``work/``
so a coordinator can review it before touching the private tree.

    python ops/reconcile_ledger.py
    python ops/reconcile_ledger.py --json work/ledger-reconciliation.json \\
        --patch work/ledger-proposed.jsonl
"""
import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ('.c', '.s', '.inc', '.cpp')
ADDRESS_SUFFIX = re.compile(r'([0-9a-f]{8})$')
# Any identifier may carry the address: the tree uses ``native_<module>_<addr>`` for
# recovered units but the ledger still names some rows ``func_<addr>``, and a symbol
# that does not match would be reported as an inverse error instead of a definition.
DEFINITION = re.compile(r'^(?:[A-Za-z_][\w \t\*]*[\s\*]+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(')
ASM_EXPORT = re.compile(r'^\s*\.(?:global|globl|type)\s+([A-Za-z_][A-Za-z0-9_]*)')
ASM_LABEL = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):')
COMMENTS = re.compile(r'/\*.*?\*/|//[^\n]*', re.S)


def definitions(root):
    """Map address string -> list of (path, symbol) definitions found in src/."""
    found = {}
    for path in (root / 'src').rglob('*'):
        suffix = path.suffix.lower()
        if suffix not in SOURCES or not path.is_file():
            continue
        try:
            text = path.read_text(encoding='utf-8', errors='replace')
        except OSError:
            continue
        relative = path.relative_to(root).as_posix()
        text = COMMENTS.sub('', text) if suffix != '.s' else text
        candidates = []
        if suffix == '.s':
            for line in text.splitlines():
                match = ASM_EXPORT.match(line) or ASM_LABEL.match(line)
                if match:
                    candidates.append(match.group(1))
        else:
            lines = text.splitlines()
            for index, line in enumerate(lines):
                if line[:1] in (' ', '\t') or not line:
                    continue
                if line.rstrip().endswith(';') or line.startswith('extern'):
                    continue
                match = DEFINITION.match(line)
                if not match:
                    continue
                if '{' not in line[match.end() - 1:]:
                    following = next((item for item in lines[index + 1:] if item.strip()), '')
                    if '{' not in following:
                        continue
                candidates.append(match.group(1))
        for symbol in candidates:
            match = ADDRESS_SUFFIX.search(symbol)
            if match:
                found.setdefault(match.group(1), []).append((relative, symbol))
    return found


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--json', dest='json_path', default=None)
    parser.add_argument('--patch', dest='patch_path', default=None)
    args = parser.parse_args(argv)

    started = time.perf_counter()
    root = Path(args.root).resolve()
    defs = definitions(root)
    ledger_path = root / 'ledger/functions.jsonl'
    rows = [json.loads(line) for line in ledger_path.read_text(encoding='utf-8').splitlines()
            if line.strip()]

    stale, inverse, unmatched = [], [], []
    proposals = []
    for row in rows:
        if not row.get('bytes'):
            continue
        key = f"{int(row['address'], 16):08x}"
        defined = defs.get(key)
        matched = bool(row['states'].get('functionMatched'))
        record = {'address': row['address'], 'module': row['module'], 'bytes': row['bytes'],
                  'mode': row['mode'], 'symbol': row.get('symbol'),
                  'source': defined[0][0] if defined else None}
        if defined and not matched:
            stale.append(record)
            proposals.append(dict(row, **{
                'states': dict(row['states'], functionMatched=True),
                'sourceUnit': defined[0][0],
                'sourceLanguage': row.get('sourceLanguage') or
                                  ('assembly' if defined[0][0].endswith('.s') else 'c'),
            }))
        elif matched and not defined:
            inverse.append(record)
        elif not matched:
            unmatched.append(record)

    elapsed = time.perf_counter() - started
    print(f'ledger rows with bytes: {sum(1 for row in rows if row.get("bytes"))}')
    print(f'  stale (source exists, ledger says unmatched):  {len(stale)}')
    print(f'  inverse (ledger says matched, source absent):  {len(inverse)}')
    print(f'  genuinely unmatched:                          {len(unmatched)}')
    print('\nfirst 10 stale rows:')
    for record in stale[:10]:
        print(f"  {record['address']:>10s} {record['module']:18s} {record['bytes']:5d} B "
              f"{record['source']}")
    print(f'\nruntime: {elapsed:.2f} s')

    if args.json_path:
        Path(args.json_path).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_path).write_text(json.dumps({
            'counts': {'stale': len(stale), 'inverse': len(inverse),
                       'unmatched': len(unmatched)},
            'stale': stale, 'inverse': inverse,
            'runtimeSeconds': round(elapsed, 2),
        }, indent=1) + '\n', encoding='utf-8')
        print(f'report written: {args.json_path}')
    if args.patch_path:
        Path(args.patch_path).parent.mkdir(parents=True, exist_ok=True)
        with Path(args.patch_path).open('w', encoding='utf-8') as stream:
            for row in proposals:
                stream.write(json.dumps(row) + '\n')
        print(f'proposed patch written: {args.patch_path} ({len(proposals)} rows)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
