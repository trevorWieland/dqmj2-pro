"""Re-screen unmatched Thumb rows with mode-aware branch relocation.

The 2026-11-11 BLX-mode fix changes how ``R_ARM_THM_CALL`` is expanded: a call to
an ARM target is a ``BLX`` immediate, not a ``BL``. This tool measures what that
changes on the real backlog. It does **not** invent sources. For every unmatched
arm9 Thumb row it:

1. scans the measured image for BLX-immediate sites (bit 12 clear in the second
   halfword, first halfword ``11110``);
2. collects every candidate source in ``--candidates`` whose file name carries
   the row address, compiles each with the pinned compiler and profile, and
   scores it twice -- once with the old placeholder rule (``modes=None``, always
   BL) and once with :class:`ops.form_search.TargetModes` (the fix);
3. keeps the best candidate per row and classifies the row:

   * ``exact-after`` -- best form now reproduces the image byte-exactly;
   * ``blx-only-to-exact`` -- was a 1-2 byte miss, now exact;
   * ``improved-still-diff`` -- fewer differing bytes, still not exact;
   * ``source-mismatch`` -- a source exists but the fix does not reduce the diff;
   * ``needs-source`` -- no best-known form exists; the row is further split into
     ``blx-reachable`` (every BLX target resolves to ARM, so the mode fix removes
     that blocker) and ``blx-unresolved`` (a BLX target has no mode evidence).

The output separates *compile-exact* from *reachable*; a row without a source is
never counted as matched.

    python ops/blx_rescreen.py --candidates "../../work/permuter-candidates/**/*.c" \
        --candidates "../../work/worktrees/*/src/**/*.c" --json build/blx-rescreen.json
"""
import argparse
import collections
import hashlib
import json
import struct
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import form_search  # noqa: E402
from thumb_branch import is_blx  # noqa: E402

MODULES = ('ov006', 'main')
SOURCE_SUFFIXES = ('.c', '.cpp')


def scan_blx(image, base, row):
    """Return ``[(offset, site, target)]`` for BLX-immediate sites in a row."""
    start = int(row['address'], 0) - base
    body = image[start:start + row['bytes']]
    sites = []
    for offset in range(0, len(body) - 3, 2):
        first, second = struct.unpack_from('<HH', body, offset)
        if (first & 0xF800) != 0xF000 or not is_blx(second):
            continue
        sign = (first >> 10) & 1
        j1, j2 = (second >> 13) & 1, (second >> 11) & 1
        i1, i2 = 1 - (j1 ^ sign), 1 - (j2 ^ sign)
        immediate = (sign << 24) | (i1 << 23) | (i2 << 22)
        immediate |= ((first & 0x3FF) << 12) | ((second & 0x7FF) << 1)
        if immediate & (1 << 24):
            immediate -= 1 << 25
        site = int(row['address'], 0) + offset
        sites.append((offset, site, ((site + 4) & ~3) + immediate))
    return sites


def unmatched_thumb_rows(root):
    ledger = root / 'ledger/functions.jsonl'
    rows = []
    with ledger.open(encoding='utf-8') as stream:
        for line in stream:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if (row.get('processor') == 'arm9' and row.get('mode') == 'thumb'
                    and row.get('module') in MODULES and row.get('bytes')
                    and (row.get('states') or {}).get('functionMatched') is False):
                rows.append(row)
    return rows


def candidate_index(patterns):
    """Index candidate sources by the 8-hex row address in their file name."""
    import re
    found = collections.defaultdict(dict)
    for pattern in patterns:
        for path in Path().glob(pattern):
            if path.suffix.lower() not in SOURCE_SUFFIXES or not path.is_file():
                continue
            match = re.search(r'([0-9a-fA-F]{8})$', path.stem)
            if not match:
                continue
            address = int(match.group(1), 16)
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            found[address].setdefault(digest, path)
    return {address: list(paths.values()) for address, paths in found.items()}


def compile_and_score(root, row, source, modes, work, want):
    work.mkdir(parents=True, exist_ok=True)
    obj = work / f'{row["address"].lower().replace("0x", "")}-{source.stem}.o'
    compiled = form_search.compile_source(form_search.default_compiler(root), source, obj, root)
    if compiled.returncode != 0:
        return None
    text, defined, relocations = form_search.read_object(obj)
    address = int(row['address'], 0)
    old = form_search.relocate(text, address, relocations, defined, modes=None)
    new = form_search.relocate(text, address, relocations, defined, modes=modes)
    return {
        'source': str(source),
        'old': form_search.score(old, want),
        'new': form_search.score(new, want),
        'old_size': len(old), 'new_size': len(new),
        'old_offsets': [i for i, (a, b) in enumerate(zip(old, want)) if a != b],
        'new_offsets': [i for i, (a, b) in enumerate(zip(new, want)) if a != b],
        'relocations': len(relocations),
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--candidates', action='append', default=[],
                        help='glob for candidate sources; repeatable')
    parser.add_argument('--json', dest='json_path')
    parser.add_argument('--work', default=None)
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    work = Path(args.work or root / 'build/blx_rescreen')
    modes_by_module = {module: form_search.TargetModes(root, module) for module in MODULES}
    rows = unmatched_thumb_rows(root)
    sources_by_address = candidate_index(args.candidates)
    images = {}
    report = {}
    counts = collections.Counter()
    for row in rows:
        module = row['module']
        if module not in images:
            images[module] = form_search.module_image(root, module)
        image, _, base = images[module]
        sites = scan_blx(image, base, row)
        modes = modes_by_module[module]
        address = int(row['address'], 0)
        entry = {'address': row['address'], 'module': module, 'bytes': row['bytes'],
                 'blx_sites': len(sites),
                 'blx_targets': sorted({target for _, _, target in sites}),
                 'blx_all_arm': all(modes.resolve(target)[0] == 'arm'
                                    for _, _, target in sites) if sites else None}
        candidates = sources_by_address.get(address, []) if sites else []
        want = image[address - base:address - base + row['bytes']]
        best = None
        for source in candidates:
            result = compile_and_score(root, row, source, modes, work / f'{address:08x}', want)
            if result is None:
                continue
            if best is None or result['new'] < best['new']:
                best = result
        if best is not None:
            entry['best'] = best
            old, new = best['old'], best['new']
            if new == (0, 0):
                entry['status'] = 'exact-after'
                counts['exact-after'] += 1
                if old != (0, 0) and old[0] <= 2:
                    counts['blx-only-to-exact'] += 1
            elif new < old:
                entry['status'] = 'improved-still-diff'
                counts['improved-still-diff'] += 1
            else:
                entry['status'] = 'source-mismatch'
                counts['source-mismatch'] += 1
        elif sites:
            if entry['blx_all_arm']:
                entry['status'] = 'needs-source-blx-reachable'
                counts['needs-source-blx-reachable'] += 1
            else:
                entry['status'] = 'needs-source-blx-unresolved'
                counts['needs-source-blx-unresolved'] += 1
        else:
            entry['status'] = 'no-blx'
            counts['no-blx'] += 1
        report[row['address']] = entry

    print(f'rows screened: {len(rows)}')
    print(f'rows with a BLX site: {sum(1 for e in report.values() if e["blx_sites"])}')
    print(f'rows with a candidate source: {sum(1 for e in report.values() if "best" in e)}')
    print('\nstatus distribution:')
    for status, count in counts.most_common():
        print(f'  {status:32s} {count}')
    exact = [e for e in report.values() if e['status'] == 'exact-after']
    if exact:
        print('\nexact after the fix:')
        for entry in sorted(exact, key=lambda item: item['address']):
            best = entry['best']
            print(f'  {entry["address"]} {entry["module"]:5s} {entry["bytes"]:3d} B '
                  f'old={best["old"]} new={best["new"]} {best["source"]}')
    if args.json_path:
        Path(args.json_path).write_text(json.dumps({
            'rows': report,
            'counts': dict(counts),
        }, indent=1) + '\n', encoding='utf-8')
        print(f'\nwritten {args.json_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
