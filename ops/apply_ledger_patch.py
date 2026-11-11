"""Apply a reviewed reconciliation patch to the private ledger, with a backup first.

The private ledger is a junction into the parent checkout and is untracked by design, so
a correction written straight into it is unreviewable unless the tool forces a backup and
refuses to guess. This tool:

1. copies ``ledger/functions.jsonl`` into ``work/ledger-backup-<sha256[:16]>.jsonl`` and
   verifies the copy's hash before continuing;
2. applies only the rows present in the patch file (matched by ledger ``id``), leaving
   every other line byte-identical;
3. reports how many rows changed and the new hash, and defaults to a dry run so the
   change has to be requested twice.

The patch format is one full ledger row per line, as emitted by
``ops/reconcile_ledger.py --patch``.

    python ops/apply_ledger_patch.py --plan work/ledger-proposed.jsonl
    python ops/apply_ledger_patch.py --plan work/ledger-proposed.jsonl --apply

Record of the first use (2026-11-11), for reproducibility
--------------------------------------------------------
Applied the 364-row stale correction produced by ``ops/reconcile_ledger.py``:

  backup         work/ledger-backup-0aa0698bcba2e596.jsonl
  backup sha256  0aa0698bcba2e59681581614fad2fab3f9858ad08acb56d62a992834978f23a6
                 (32,693,922 bytes, 16,073 rows)
  patch          work/ledger-proposed.jsonl (364 rows: functionMatched=true, sourceUnit,
                 sourceLanguage) — the 504 inverse rows were deliberately excluded
  after sha256   3476263f803f0360f168ff1547bb1e44fdb022c3592fba23b042de3c5167235f
                 (16,073 rows, unchanged count)

Reconciliation went from stale 364 / inverse 504 / unmatched 3,284 to
stale 0 / inverse 504 / unmatched 3,284 / consistent 11,520. The backup hash above is
the pre-write record; with these two hashes plus the patch file, the correction can be
audited or reversed without trusting this tool.

The private ledger has been updated again since (it is shared), so re-running this tool
on the live file reports ``rows to change: 0`` — the correction is present and the tool is
idempotent. To audit against the original instead, point ``--ledger`` at the backup
above; to audit the current state, run ``ops/reconcile_ledger.py`` and expect
stale 0 / inverse 504.
"""
import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--plan', required=True)
    parser.add_argument('--ledger', default=None)
    parser.add_argument('--backup-dir', default=None)
    parser.add_argument('--dry-run', action='store_true', default=True)
    parser.add_argument('--apply', dest='dry_run', action='store_false',
                        help='actually write the ledger (default is a dry run)')
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parent.parent
    ledger = Path(args.ledger) if args.ledger else root / 'ledger/functions.jsonl'
    backup_dir = Path(args.backup_dir) if args.backup_dir else root / 'work'
    original = ledger.read_bytes()
    digest = hashlib.sha256(original).hexdigest()
    backup = backup_dir / f'ledger-backup-{digest[:16]}.jsonl'
    print(f'ledger: {ledger}')
    print(f'  sha256 {digest}')
    if not args.dry_run:
        backup.parent.mkdir(parents=True, exist_ok=True)
        if not backup.exists():
            shutil.copyfile(ledger, backup)
        if hashlib.sha256(backup.read_bytes()).hexdigest() != digest:
            raise SystemExit('backup hash mismatch; refusing to write')
        print(f'  backup {backup}')

    plan = {}
    for line in Path(args.plan).read_text(encoding='utf-8').splitlines():
        if line.strip():
            row = json.loads(line)
            plan[row['id']] = row
    print(f'plan rows: {len(plan)}')

    output = []
    applied = 0
    for line in original.decode('utf-8').splitlines():
        if not line.strip():
            output.append(line)
            continue
        row = json.loads(line)
        replacement = plan.get(row['id'])
        if replacement is None or json.dumps(row, sort_keys=True) == json.dumps(replacement, sort_keys=True):
            output.append(line)
            continue
        output.append(json.dumps(replacement))
        applied += 1
    print(f'rows to change: {applied}')
    if args.dry_run:
        print('dry run: nothing written (pass --apply to write)')
        return 0
    text = '\n'.join(output) + '\n'
    temp = ledger.with_suffix('.jsonl.new')
    temp.write_text(text, encoding='utf-8')
    shutil.move(str(temp), str(ledger))
    print(f'written: {hashlib.sha256(text.encode("utf-8")).hexdigest()}'
          f' ({len([l for l in text.splitlines() if l.strip()])} rows)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
