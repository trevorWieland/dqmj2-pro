"""Run the pinned asm-lane verifier for the ov001 closing lane with a cached ledger.

``ops/verify_asm_chunk_scan.py`` re-reads the 32 MB ``ledger/functions.jsonl`` for
every row (once in ``check_row``, once in the summary), which is quadratic.  The
checks are the pinned ones and are reused verbatim; only the ledger lookup is
cached, so the result is identical to running the pinned tool directly.

    python ops/verify_ov001_close.py --record     # write the pinned fixture
    python ops/verify_ov001_close.py              # verify against the pinned fixture
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import verify_asm_chunk_scan  # noqa: E402
import form_search  # noqa: E402

LANE = 'src/ov001/p12_ov001_close/arm'
FIXTURE = 'ops/ov001_close_expectations.json'


def cached_rows():
    rows = {}
    for line in (ROOT / 'ledger/functions.jsonl').open(encoding='utf-8'):
        if not line.strip():
            continue
        row = json.loads(line)
        rows[(row['module'], int(row['address'], 16))] = row
    return rows


def cache_target_modes():
    """``form_search.TargetModes`` loads the 32 MB ledger per instance; build it once."""
    original = form_search.TargetModes
    cache = {}

    def cached(root, module=None):
        key = (str(root), module)
        if key not in cache:
            modes = original(root, module)
            modes._load()
            cache[key] = modes
        return cache[key]

    form_search.TargetModes = cached
    verify_asm_chunk_scan.form_search.TargetModes = cached


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--record', action='store_true')
    parser.add_argument('--lane', default=LANE)
    parser.add_argument('--fixture', default=FIXTURE)
    args = parser.parse_args(argv)
    rows = cached_rows()
    verify_asm_chunk_scan.ledger_row = lambda module, address: rows.get((module, address))
    cache_target_modes()
    sys.argv = ['verify_asm_chunk_scan.py', '--lane', args.lane, '--fixture', args.fixture]
    if args.record:
        sys.argv.append('--record')
    return verify_asm_chunk_scan.main()


if __name__ == '__main__':
    sys.exit(main())
