#!/usr/bin/env python3
"""Rank permuter-ready rows: exact-size sources whose instruction stream is close.

`ops/permuter_queue.py` ranks *unmatched* families from the harvest filter, but a family
listing says nothing about whether a source exists that compiles to the measured size and
is close in its instruction stream. This tool answers the question the permuter needs: for
every source unit in a module (or every module), resolve the rule the repository build
would use -- primary and alternate compilers -- compile it, measure the function against the
module image through ``ops/form_search`` + ``TargetModes``, and bucket the result:

* **ready** -- exact compiled size, bytes differ, and the shim-normalized diff is at most
  ``--max-text-diff`` instruction rows (default 3). This is the permuter's market.
* **relocationOnly** -- exact size, byte diff, but the normalized diff is zero: the
  difference sits in a relocation slot, so the permuter sees score 0. Usually a patcher
  problem, not a source problem.
* **far** -- exact size, small byte score, tens of differing instruction rows. A one-byte
  encoding difference is not a near miss; the byte score alone over-reports these.
* **exact** -- the source reproduces the row under some declared rule. Ledger work.

The measurement is cached under ``work/permuter/.scan-cache.json`` keyed by source hash,
compiler and flags, so a rerun after an interruption only pays for new or changed units.

    python ops/permuter_candidates.py --module ov006
    python ops/permuter_candidates.py --modules all --json build/scan-all.json
    python ops/permuter_candidates.py --summarize build/scan-*.json \
        --out-json docs/authoring/permuter-queue-v2.json \
        --out-md docs/authoring/permuter-queue-v2.md

Nothing is written into ``src/``; the JSON/MD report is explicit.
"""
import argparse
import glob
import hashlib
import json
import re
import struct
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(ROOT / 'public_tools'))

import form_search  # noqa: E402
import permuter    # noqa: E402
import source_units  # noqa: E402

ADDRESS = re.compile(r'([0-9a-f]{8})\.c$', re.I)
CACHE = ROOT / 'work/permuter/.scan-cache.json'


def module_image(root, config, module):
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
    import subprocess
    output = subprocess.run(
        [sys.executable, str(root / 'ops/mwcc_objdump.py'), str(obj), '--mode', mode],
        capture_output=True, text=True, encoding='utf-8', errors='replace')
    if output.returncode != 0:
        return None
    return [line.rstrip() for line in output.stdout.splitlines()[4:]]


def permuter_text_diff(root, base_obj, image_slice, mode, scratch, tag):
    target = scratch / (Path(base_obj).stem + f'-{tag}-target.o')
    try:
        permuter.build_target_object(base_obj, image_slice, target)
    except SystemExit:
        return None
    before = shim_rows(root, base_obj, mode)
    after = shim_rows(root, target, mode)
    if before is None or after is None:
        return None
    return sum(1 for left, right in zip(before, after) if left != right) + abs(len(before) - len(after))


def source_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def measure_variant(root, path, unit, flags, compiler, thumb, address, image, base, size,
                    modes, scratch, variant, timeout):
    """Compile and measure one (source, compiler, flags) variant."""
    obj = scratch / f'{Path(path).stem}-{variant}.o'
    try:
        built = permuter.compile_object(root, root / path, obj, flags, thumb,
                                        compiler=root / compiler, timeout=timeout)
    except Exception as error:
        return dict(status='compile-failed', detail=str(error), variant=variant)
    if built.returncode:
        return dict(status='compile-failed', variant=variant)
    text, defined, relocations = form_search.read_object(obj)
    wanted = image[address - base:address - base + size]
    try:
        actual = form_search.relocate(text, address, relocations, defined, modes=modes)
    except (ValueError, AssertionError, struct.error) as error:
        return dict(status='relocation-failed', detail=str(error), variant=variant)
    score, length_delta = form_search.score(actual, wanted)
    record = dict(status='ok', variant=variant, compiledSize=len(actual), score=score,
                  lengthDelta=length_delta)
    if score == 0 and length_delta == 0:
        record['textDiff'] = 0
        return record
    if len(actual) == size:
        record['textDiff'] = permuter_text_diff(root, obj, wanted, unit['mode'], scratch, variant)
    return record


def scan(root, modules, max_score, timeout, max_text_diff, under=None, cache_path=None):
    config = source_units.load_config(root)
    enumerated = source_units.enumerate_sources(root, config)
    rows_by_module = {module: ledger_rows(root, module) for module in modules}
    images = {module: module_image(root, config, module) for module in modules}
    modes = {}
    scratch = root / 'work/permuter/.scan'
    scratch.mkdir(parents=True, exist_ok=True)
    cache_file = Path(cache_path) if cache_path else CACHE
    if not cache_file.is_absolute():
        cache_file = root / cache_file
    cache = json.loads(cache_file.read_text(encoding='utf-8')) if cache_file.is_file() else {}
    buckets = dict(ready=[], relocationOnly=[], far=[], exact=[], skipped=[])

    units = [unit for unit in enumerated['compiled']
             if unit['module'] in modules and (not under or unit['path'].startswith(under))]
    print(f'{len(units)} compiled unit(s) in {len(modules)} module(s)', file=sys.stderr)
    for index, unit in enumerate(units, 1):
        if index % 200 == 0:
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            cache_file.write_text(json.dumps(cache), encoding='utf-8')
        path = unit['path']
        if index % 25 == 0:
            print(f'  {index}/{len(units)}  ready={len(buckets["ready"])} '
                  f'reloc={len(buckets["relocationOnly"])} far={len(buckets["far"])} '
                  f'exact={len(buckets["exact"])}', file=sys.stderr, flush=True)
        match = ADDRESS.search(path)
        if not match:
            buckets['skipped'].append(dict(path=path, reason='no address in the file name'))
            continue
        address = int(match.group(1), 16)
        module = unit['module']
        row = rows_by_module[module].get(address)
        if row is None:
            buckets['skipped'].append(dict(path=path, reason='no ledger row'))
            continue
        size = row['bytes']
        image, base = images[module]
        if module not in modes:
            modes[module] = form_search.TargetModes(root, module)
        variants = [(unit['compilerFlags'], unit['compilerPath'])]
        for alternate in unit.get('alternates') or []:
            variants.append((alternate['compilerFlags'], alternate['compilerPath']))
        key_base = f'{path}|{source_sha(root / path)}|{address:#x}'
        best = None
        for variant_index, (flags, compiler) in enumerate(variants):
            if not (root / compiler).is_file():
                continue
            key = f'{key_base}|{compiler}|{" ".join(flags)}'
            cached = cache.get(key)
            if cached is None:
                clean = [flag for flag in flags if flag != '-thumb']
                thumb = '-thumb' in flags
                cached = measure_variant(root, path, unit, clean, compiler, thumb, address,
                                         image, base, size, modes[unit['module']], scratch,
                                         f'v{variant_index}', timeout)
                cache[key] = cached
            if cached['status'] != 'ok':
                continue
            candidate = dict(cached, compiler=compiler, flags=list(flags))
            if best is None or candidate['score'] < best['score']:
                best = candidate
            if candidate['score'] == 0:
                break
        if best is None:
            buckets['skipped'].append(dict(path=path, reason='no variant compiled'))
            continue
        record = dict(address=f'{address:#010x}', bytes=size, mode=row['mode'], path=path,
                      module=unit['module'], compiler=best['compiler'],
                      flags=best['flags'], score=best['score'],
                      compiledSize=best['compiledSize'], textDiff=best.get('textDiff'),
                      ledgerMatched=row['states']['functionMatched'])
        if best['score'] == 0:
            buckets['exact'].append(record)
        elif best['compiledSize'] == size and best['score'] <= max_score:
            diff = best.get('textDiff')
            if diff is None:
                buckets['skipped'].append(dict(path=path, reason='target build failed'))
            elif diff == 0:
                buckets['relocationOnly'].append(record)
            elif diff <= max_text_diff:
                buckets['ready'].append(record)
            else:
                buckets['far'].append(record)
    for bucket in buckets.values():
        bucket.sort(key=lambda item: (item.get('textDiff') or 0, item.get('score') or 0,
                                      item.get('bytes') or 0, item.get('address') or ''))
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps(cache), encoding='utf-8')
    return dict(modules=modules, buckets=buckets, units=len(units))


def summarize(paths):
    merged = dict(modules=[], buckets=dict(ready=[], relocationOnly=[], far=[], exact=[], skipped=[]),
                  units=0)
    for name in paths:
        data = json.loads(Path(name).read_text(encoding='utf-8'))
        merged['units'] += data.get('units', 0)
        for module in data.get('modules') or []:
            if module not in merged['modules']:
                merged['modules'].append(module)
        for bucket, entries in data['buckets'].items():
            merged['buckets'].setdefault(bucket, []).extend(entries)
    return merged


def report(merged, json_path, md_path):
    buckets = merged['buckets']
    totals = {name: dict(rows=len(entries), bytes=sum(entry.get('bytes') or 0 for entry in entries))
              for name, entries in buckets.items()}
    by_module = {}
    for name, entries in buckets.items():
        if name == 'skipped':
            continue
        for entry in entries:
            module = entry.get('module') or '?'
            cell = by_module.setdefault(module, {}).setdefault(name, [0, 0])
            cell[0] += 1
            cell[1] += entry.get('bytes') or 0
    if json_path:
        destination = Path(json_path)
        if not destination.is_absolute():
            destination = ROOT / json_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(dict(generatedAt=time.strftime('%Y-%m-%dT%H:%M:%S%z'),
                                               units=merged['units'], modules=merged['modules'],
                                               totals=totals, byModule=by_module,
                                               **buckets), indent=1) + '\n', encoding='utf-8')
        print(f'json: {destination}')
    if md_path:
        lines = [
            '# Permuter queue v2',
            '',
            'Generated by `ops/permuter_candidates.py` from `config/source_units.json`, the',
            'ledger and the module images. Buckets:',
            '',
            '* **ready** -- exact size, bytes differ, normalized instruction-row diff <= 3.',
            '  This is the permuter market.',
            '* **relocationOnly** -- exact size, byte diff, normalized diff 0: the difference',
            '  is inside a relocation slot. A patcher/link problem, not a source problem.',
            '* **far** -- exact size, small byte score, tens of differing rows. Not a near miss.',
            '* **exact** -- the source already reproduces the row under some declared rule.',
            '',
            f"units scanned: {merged['units']}; modules: {', '.join(sorted(merged['modules']))}",
            '',
            '| bucket | rows | bytes |',
            '| --- | --- | --- |',
        ]
        for name in ('ready', 'relocationOnly', 'far', 'exact', 'skipped'):
            if name in totals:
                lines.append(f"| {name} | {totals[name]['rows']} | {totals[name]['bytes']} |")
        lines += ['', '## Per module', '',
                  '| module | ready (rows/B) | relocation-only | far | exact |',
                  '| --- | --- | --- | --- | --- |']
        for module in sorted(by_module):
            cells = by_module[module]
            fmt = lambda name: (f"{cells[name][0]} / {cells[name][1]}" if name in cells else '-')
            lines.append(f'| {module} | {fmt("ready")} | {fmt("relocationOnly")} | '
                         f'{fmt("far")} | {fmt("exact")} |')
        if buckets['ready']:
            lines += ['', '## True near misses', '',
                      '| address | bytes | score | textDiff | module | source |',
                      '| --- | --- | --- | --- | --- | --- |']
            for entry in buckets['ready']:
                lines.append(f"| `{entry['address']}` | {entry['bytes']} | {entry['score']} | "
                             f"{entry.get('textDiff')} | {entry['module']} | `{entry['path']}` |")
        if buckets['relocationOnly']:
            lines += ['', '## Relocation-only (patcher/link, not source)', '',
                      '| address | bytes | module | source |',
                      '| --- | --- | --- | --- |']
            for entry in buckets['relocationOnly']:
                lines.append(f"| `{entry['address']}` | {entry['bytes']} | {entry['module']} | "
                             f"`{entry['path']}` |")
        lines += ['',
                  '## Snapshot note',
                  '',
                  'This report is a scan snapshot. Two relocation-only causes were found and',
                  'fixed the same day, so a fresh scan is cleaner than this table:',
                  '',
                  '* ten accepted ov006 rows had a Thumb function pointer literal whose bit 0',
                  '  the patcher dropped (`ops/form_search.py` now sets it, tests in',
                  '  `ops/test_form_search.py`);',
                  '* `0x020337c4` (main, 364 B) named its pivot table `native_data_020d9aac`',
                  '  while the image holds `0x020d90ac`; the corrected source is',
                  '  `src/main/permuter_20261111/native_main_020337c4.c`.',
                  '',
                  'See `docs/authoring/permuter.md` for both, and rerun this tool to refresh.',
                  '']
        destination = Path(md_path)
        if not destination.is_absolute():
            destination = ROOT / md_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        print(f'md: {destination}')
    print(f"ready {totals['ready']['rows']} rows / {totals['ready']['bytes']} B; "
          f"relocation-only {totals['relocationOnly']['rows']}; far {totals['far']['rows']}; "
          f"exact {totals['exact']['rows']}; skipped {totals['skipped']['rows']}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', action='append', default=[])
    parser.add_argument('--modules', help='comma-separated modules, or "all"')
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--under', help='only sources under this path prefix')
    parser.add_argument('--max-score', type=int, default=24)
    parser.add_argument('--max-text-diff', type=int, default=3)
    parser.add_argument('--timeout', type=float, default=60.0)
    parser.add_argument('--json', help='write the scan here')
    parser.add_argument('--limit', type=int, default=40)
    parser.add_argument('--summarize', nargs='+', help='merge scan JSONs into the v2 report')
    parser.add_argument('--cache', help='per-process measurement cache path')
    parser.add_argument('--out-json')
    parser.add_argument('--out-md')
    args = parser.parse_args(argv)
    root = Path(args.root).resolve()

    if args.summarize:
        report(summarize(args.summarize), args.out_json or 'docs/authoring/permuter-queue-v2.json',
               args.out_md or 'docs/authoring/permuter-queue-v2.md')
        return 0

    config = source_units.load_config(root)
    known = sorted(config['modules'])
    if args.modules == 'all':
        modules = known
    elif args.modules:
        modules = [name.strip() for name in args.modules.split(',') if name.strip()]
    else:
        modules = args.module
    if not modules:
        parser.error('give --module, --modules or --summarize')
    unknown = [name for name in modules if name not in known]
    if unknown:
        parser.error('unknown module(s): ' + ', '.join(unknown))

    result = scan(root, modules, args.max_score, args.timeout, args.max_text_diff,
                  under=args.under, cache_path=args.cache)
    payload = dict(modules=modules, units=result['units'], buckets=result['buckets'])
    if args.json:
        destination = Path(args.json)
        if not destination.is_absolute():
            destination = root / args.json
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=1) + '\n', encoding='utf-8')
        print(f'report: {destination}')
    for name in ('ready', 'relocationOnly', 'far', 'exact'):
        entries = result['buckets'][name]
        print(f'{name:15s} {len(entries):5d} row(s) '
              f'{sum(entry.get("bytes") or 0 for entry in entries):6d} B')
    for entry in result['buckets']['ready'][:args.limit]:
        print(f'  READY {entry["address"]} {entry["bytes"]:4d} B score={entry["score"]} '
              f'textdiff={entry.get("textDiff")} {entry["path"]}')
    return 0 if result['buckets']['ready'] else 1


if __name__ == '__main__':
    sys.exit(main())
