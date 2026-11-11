#!/usr/bin/env python3
"""Rank permuter-ready rows: exact-size sources that do not yet reproduce the image.

`ops/permuter_queue.py` ranks *unmatched* families from the harvest filter, but a family
listing says nothing about whether a source exists that compiles to the measured size.
This tool answers the question the permuter actually needs: for every source unit in a
module, resolve its rule (compiler, flags, mode), compile it, measure the function against
the module image through ``ops/form_search`` + ``TargetModes``, and report the rows whose
compiled size is exactly the ledger size but whose bytes differ.

Those rows are the permuter's input class: same instructions and same extent, different
register allocation or operand order. Rows whose bytes already match are reported
separately -- they are ledger reconciliation work, not permuter work.

    python ops/permuter_candidates.py --module ov006
    python ops/permuter_candidates.py --module ov006 --under src/ov006/p2 --json build/candidates.json
    python ops/permuter_candidates.py --module ov006 --max-score 8

Exit status is 0 when at least one permuter-ready row was found. Nothing is written into
the tree; the JSON report is optional.
"""
import argparse
import json
import re
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import permuter    # noqa: E402
import source_units  # noqa: E402

ADDRESS = re.compile(r'([0-9a-f]{8})\.c$', re.I)


def module_image(root, module):
    config = json.loads((root / 'config/source_units.json').read_text(encoding='utf-8-sig'))
    info = config['modules'][module]
    return (root / info['originalImage']).read_bytes(), int(str(info['loadAddressBase']), 0)


def ledger_rows(root, module):
    rows = {}
    for line in (root / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines():
        if not line.strip() or module not in line:
            continue
        row = json.loads(line)
        if row.get('module') == module:
            rows[int(row['address'], 16)] = row
    return rows


def shim_rows(root, obj, mode):
    """The normalized instruction rows decomp-permuter would diff for this object."""
    import subprocess
    output = subprocess.run(
        [sys.executable, str(root / 'ops/mwcc_objdump.py'), str(obj), '--mode', mode],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    if output.returncode != 0:
        return None
    return [line.rstrip() for line in output.stdout.splitlines()[4:]]


def permuter_text_diff(root, base_obj, image_slice, mode, scratch):
    """Rows that differ after the shim's normal form, i.e. what the permuter can see.

    A difference that lives only in a relocation slot is invisible here on purpose: the
    shim renders both sides as the same symbol, so the permuter would report score 0 and
    the row would never move. Such a row is a link/relocation problem, not a source one.
    """
    target = scratch / (Path(base_obj).stem + '-target.o')
    try:
        permuter.build_target_object(base_obj, image_slice, target)
    except SystemExit:
        return None
    before = shim_rows(root, base_obj, mode)
    after = shim_rows(root, target, mode)
    if before is None or after is None:
        return None
    return sum(1 for left, right in zip(before, after) if left != right) + abs(len(before) - len(after))


def scan(root, module, under, max_score, timeout=60, max_text_diff=3):
    config = source_units.load_config(root)
    enumerated = source_units.enumerate_sources(root, config)
    rows = ledger_rows(root, module)
    image, base = module_image(root, module)
    modes = form_search.TargetModes(root, module)
    scratch = root / 'work/permuter/.scan'
    scratch.mkdir(parents=True, exist_ok=True)

    ready, exact, relocation_only, far, skipped = [], [], [], [], []
    units = [unit for unit in enumerated['compiled']
             if unit['module'] == module and (not under or unit['path'].startswith(under))]
    seen = 0
    for unit in units:
        path = unit['path']
        seen += 1
        if seen % 25 == 0:
            print(f'  {seen}/{len(units)} units, {len(ready)} ready, {len(exact)} exact, '
                  f'{len(relocation_only)} relocation-only', file=sys.stderr, flush=True)
        match = ADDRESS.search(path)
        if not match:
            skipped.append((path, 'no address in the file name'))
            continue
        address = int(match.group(1), 16)
        row = rows.get(address)
        if row is None:
            skipped.append((path, 'no ledger row'))
            continue
        size = row['bytes']
        flags = [flag for flag in unit['compilerFlags'] if flag != '-thumb']
        thumb = '-thumb' in unit['compilerFlags']
        compiler = root / unit['compilerPath']
        obj = scratch / (Path(path).stem + '.o')
        try:
            built = permuter.compile_object(root, root / path, obj, flags, thumb,
                                            compiler=compiler, timeout=timeout)
        except Exception as error:  # includes subprocess.TimeoutExpired
            skipped.append((path, 'compile failed: ' + str(error)))
            continue
        if built.returncode:
            skipped.append((path, 'compile failed'))
            continue
        text, defined, relocations = form_search.read_object(obj)
        wanted = image[address - base:address - base + size]
        try:
            actual = form_search.relocate(text, address, relocations, defined, modes=modes)
        except (ValueError, AssertionError, struct.error) as error:
            skipped.append((path, 'relocation failed: ' + str(error)))
            continue
        score, length_delta = form_search.score(actual, wanted)
        record = dict(address=f'{address:#010x}', bytes=size, mode=row['mode'], path=path,
                      sourceCompiler=unit['compilerSha256'][:8], compilerPath=unit['compilerPath'],
                      compiledSize=len(actual), score=score, lengthDelta=length_delta)
        if score == 0 and length_delta == 0:
            exact.append(record)
        elif len(actual) == size and score <= max_score:
            diff = permuter_text_diff(root, obj, wanted, row['mode'], scratch)
            record['textDiff'] = diff
            if diff is None or diff == 0:
                relocation_only.append(record)
            elif diff <= max_text_diff:
                ready.append(record)
            else:
                far.append(record)
    ready.sort(key=lambda item: (item.get('textDiff') or 0, item['score'], item['bytes'], item['address']))
    return ready, exact, relocation_only, far, skipped


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--under', help='only sources under this path prefix')
    parser.add_argument('--max-score', type=int, default=16,
                        help='largest differing-byte score to report as permuter-ready')
    parser.add_argument('--json', help='write the full scan here')
    parser.add_argument('--limit', type=int, default=40)
    parser.add_argument('--max-text-diff', type=int, default=3,
                        help='largest normalized instruction-row diff that still counts as a near miss')
    parser.add_argument('--timeout', type=float, default=60.0,
                        help='per-unit compile timeout in seconds (default 60)')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    ready, exact, relocation_only, far, skipped = scan(root, args.module, args.under, args.max_score, args.timeout, args.max_text_diff)
    print(f'permuter-ready rows ({len(ready)}): exact compiled size, bytes differ')
    print(f'{"address":>10s} {"bytes":>5s} {"score":>5s} {"mode":5s} {"compiler":8s} source')
    for record in ready[:args.limit]:
        print(f'{record["address"]:>10s} {record["bytes"]:5d} {record["score"]:5d} '
              f'{record["mode"]:5s} {record["sourceCompiler"]:8s} {record["path"]}')
    print(f'\nexact-size but a large normalized diff ({len(far)}) -- byte score is small, '
          'instruction stream is not: not a near miss')
    for record in far[:args.limit]:
        print(f'{record["address"]:>10s} {record["bytes"]:5d} {record["score"]:5d} '
              f'textdiff={record.get("textDiff")}  {record["path"]}')
    print(f'\nexact-size but relocation-only ({len(relocation_only)}) -- the permuter sees '
          'these as already matching; fix the link/relocation, not the source')
    for record in relocation_only[:args.limit]:
        print(f'{record["address"]:>10s} {record["bytes"]:5d} {record["score"]:5d}                  '
              f'{record["path"]}')
    print(f'\nalready exact under their own rule ({len(exact)}) -- ledger reconciliation, '
          'not permuter work')
    for record in exact[:args.limit]:
        print(f'{record["address"]:>10s} {record["bytes"]:5d}                  {record["path"]}')
    if skipped:
        print(f'\nskipped {len(skipped)} source(s): '
              + ', '.join(f'{Path(name).name}: {reason}' for name, reason in skipped[:6]))
    if args.json:
        destination = Path(args.json)
        if not destination.is_absolute():
            destination = root / args.json
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(dict(module=args.module, ready=ready, far=far, exact=exact,
                                               relocationOnly=relocation_only, skipped=skipped), indent=1) + '\n',
                               encoding='utf-8')
        print(f'\nreport: {destination}')
    return 0 if ready else 1


if __name__ == '__main__':
    sys.exit(main())
