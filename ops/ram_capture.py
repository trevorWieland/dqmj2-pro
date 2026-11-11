"""Slice a runtime RAM dump into module images the data pipeline can consume.

Some data only exists after the program has run: `docs/data/unbacked-data.md`
proves the 24-byte `species_roster` records at `0x021c4bf8` are in main BSS, and
the script VM command block at `0x020fb264` is likewise runtime state. No static
image can ever back them, so the only way to get the bytes is to capture RAM from
a running instance and document exactly which state was captured.

This tool does the mechanical half of that:

1. validates the capture spec and its provenance (build hash, tool, capture point,
   timestamp) against the private `manifest.json`;
2. checks that every requested range really lies inside a module the manifest
   claims, and inside the dump, and refuses a dump whose size or base is
   inconsistent with that module (a wrong-sized dump silently shifts every byte);
3. slices each range out of the dump, writes it under `extract/ram/`, hashes it,
   and emits a manifest module entry per capture so `public_tools/data_dump.py`
   and the measurement build can treat the slice as an ordinary module;
4. can merge those entries into a manifest copy for that pipeline.

It does **not** capture anything itself. Running an emulator may be a permitted,
isolated, muted reference action, but it is a human decision recorded in the spec —
this tool only accepts the resulting dump.

Spec format
-----------
    {
      "dump": "work/ram/roster.bin",
      "dumpBase": "0x02000000",
      "module": "main",
      "provenance": {
        "buildSha256": "674c5cbf...",
        "tool": "DeSmuME 0.9.11 (Debugger > Tools > Dump memory)",
        "capturePoint": "monster farm open, roster populated, 15 slots filled",
        "timestampUtc": "2026-11-10T21:00:00Z"
      },
      "captures": [
        {"name": "ram-roster", "address": "0x021c4bf8", "bytes": 360},
        {"name": "ram-scriptvm", "address": "0x020fb264", "bytes": 4096}
      ]
    }

Usage
-----
    python ops/ram_capture.py --spec ram-roster.json --check
    python ops/ram_capture.py --spec ram-roster.json
    python ops/ram_capture.py --spec ram-roster.json --apply-manifest build/manifest-with-ram.json

Exit codes: 0 success, 1 refused (bad spec, provenance, size or range),
2 I/O problem.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIRED_PROVENANCE = ('buildSha256', 'tool', 'capturePoint', 'timestampUtc')
DEFAULT_RAM_DIR = 'extract/ram'


def parse_int(value):
    return value if isinstance(value, int) else int(str(value), 0)


def sha256(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def load_manifest(root):
    path = root / 'manifest.json'
    if not path.is_file():
        raise SystemExit(f'manifest.json is required to resolve modules: {path}')
    return json.loads(path.read_text(encoding='utf-8-sig'))


def module_for(manifest, name):
    for module in manifest.get('modules', []):
        if module.get('name') == name:
            return module
    raise SystemExit(f'unknown module in manifest.json: {name}')


def module_span(root, module):
    """(base, end) of a module, counting the image bytes and the recorded BSS.

    The end is taken from `expectedBssBytes` when present, because a runtime
    capture targets BSS as often as the image; the delinks `.bss` line is only
    consulted when the manifest has no count.
    """
    base = parse_int(module.get('loadAddressBase') or module['base'])
    image_bytes = int(module.get('bytes') or 0)
    bss_bytes = int(module.get('expectedBssBytes') or 0)
    if not image_bytes:
        image = module.get('binary')
        if image and (root / image).is_file():
            image_bytes = (root / image).stat().st_size
    if not bss_bytes:
        delinks = module.get('delinks') or ''
        candidate = root / delinks if delinks else None
        if candidate and candidate.is_file():
            for line in candidate.read_text(errors='replace').splitlines():
                if '.bss' in line and 'start:' in line and 'end:' in line:
                    start = int(line.split('start:')[1].split()[0], 0)
                    end = int(line.split('end:')[1].split()[0], 0)
                    return base, max(end, base + image_bytes)
    return base, base + image_bytes + bss_bytes


def validate_spec(root, spec, manifest):
    problems = []
    for field in ('dump', 'dumpBase', 'module', 'provenance', 'captures'):
        if field not in spec:
            problems.append(f'spec is missing "{field}"')
    if problems:
        return problems

    provenance = spec['provenance']
    for field in REQUIRED_PROVENANCE:
        if not provenance.get(field):
            problems.append(f'provenance is missing "{field}"')

    rom_hash = (manifest.get('rom') or {}).get('sha256')
    if rom_hash and provenance.get('buildSha256') != rom_hash:
        problems.append(f'provenance buildSha256 {provenance.get("buildSha256")} does not match '
                        f'the manifest rom sha256 {rom_hash}')

    dump = root / spec['dump']
    if not dump.is_file():
        problems.append(f'dump not found: {dump}')
        return problems
    size = dump.stat().st_size
    dump_base = parse_int(spec['dumpBase'])

    module = module_for(manifest, spec['module'])
    base, end = module_span(root, module)
    if not (base <= dump_base and dump_base + size <= end):
        problems.append(f'dump range {dump_base:#x}-{dump_base + size:#x} is not inside '
                        f'module {spec["module"]} ({base:#x}-{end:#x}); a dump of the wrong '
                        f'size or base shifts every captured byte')

    for capture in spec['captures']:
        name = capture.get('name')
        address = parse_int(capture['address'])
        length = parse_int(capture['bytes'])
        if not name:
            problems.append(f'capture at {address:#x} has no name')
            continue
        if length <= 0:
            problems.append(f'capture {name} has a non-positive size')
        if not (base <= address and address + length <= end):
            problems.append(f'capture {name} range {address:#x}-{address + length:#x} is outside '
                            f'module {spec["module"]} ({base:#x}-{end:#x})')
        if not (dump_base <= address and address + length <= dump_base + size):
            problems.append(f'capture {name} range {address:#x}-{address + length:#x} is outside '
                            f'the dump {dump_base:#x}-{dump_base + size:#x}')
    return problems


def apply_to_manifest(root, manifest, entries):
    merged = dict(manifest)
    modules = list(manifest.get('modules', []))
    existing = {module.get('name') for module in modules}
    for entry in entries:
        if entry['name'] in existing:
            raise SystemExit(f'refusing to duplicate module name in manifest: {entry["name"]}')
        modules.append(entry)
    merged['modules'] = modules
    return merged


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--spec', required=True, help='capture spec JSON')
    parser.add_argument('--root', default=str(ROOT), help='private checkout root')
    parser.add_argument('--out-dir', default=DEFAULT_RAM_DIR,
                        help=f'where slices are written (default {DEFAULT_RAM_DIR})')
    parser.add_argument('--check', action='store_true', help='validate only, write nothing')
    parser.add_argument('--dry-run', action='store_true', help='validate and report, write nothing')
    parser.add_argument('--apply-manifest', metavar='PATH',
                        help='write a manifest copy with the new module entries merged in')
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    spec = json.loads(Path(args.spec).read_text())
    manifest = load_manifest(root)

    problems = validate_spec(root, spec, manifest)
    if problems:
        print('refusing capture:', file=sys.stderr)
        for problem in problems:
            print(f'  {problem}', file=sys.stderr)
        return 1

    dump = root / spec['dump']
    dump_base = parse_int(spec['dumpBase'])
    data = dump.read_bytes()
    print(f'dump       {dump} ({len(data)} bytes) base {dump_base:#010x}')
    provenance = spec['provenance']
    print(f'provenance build {provenance["buildSha256"][:12]}… tool "{provenance["tool"]}"')
    print(f'           captured {provenance["timestampUtc"]}: {provenance["capturePoint"]}')

    out_dir = root / args.out_dir
    entries = []
    for capture in spec['captures']:
        name = capture['name']
        address = parse_int(capture['address'])
        length = parse_int(capture['bytes'])
        offset = address - dump_base
        blob = data[offset:offset + length]
        if len(blob) != length:
            print(f'refusing: slice {name} is {len(blob)} bytes, expected {length}', file=sys.stderr)
            return 1
        target = out_dir / f'{name}_{address:08x}.bin'
        digest = hashlib.sha256(blob).hexdigest()
        print(f'capture    {name}: {address:#010x} + {length:#x} = {digest[:16]}…')
        if not (args.check or args.dry_run):
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(blob)
            print(f'           wrote {target.relative_to(root)}')
        entries.append({
            'name': name,
            'base': f'{address:#010x}',
            'loadAddressBase': f'{address:#010x}',
            'binary': str(target.relative_to(root)).replace('\\', '/'),
            'bytes': length,
            'sha256': digest,
            'kind': 'runtime-capture',
            'provenance': {
                'buildSha256': provenance['buildSha256'],
                'tool': provenance['tool'],
                'capturePoint': provenance['capturePoint'],
                'timestampUtc': provenance['timestampUtc'],
                'dump': spec['dump'],
                'dumpBase': f'{dump_base:#010x}',
                'dumpSha256': hashlib.sha256(data).hexdigest(),
            },
        })

    fragment = {'schemaVersion': 1, 'modules': entries}
    fragment_path = root / 'build' / 'ram-capture' / 'manifest-modules.json'
    if not (args.check or args.dry_run):
        fragment_path.parent.mkdir(parents=True, exist_ok=True)
        fragment_path.write_text(json.dumps(fragment, indent=1) + '\n')
        print(f'fragment   {fragment_path.relative_to(root)} ({len(entries)} module entries)')
        if args.apply_manifest:
            merged = apply_to_manifest(root, manifest, entries)
            target = Path(args.apply_manifest)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps(merged, indent=1) + '\n')
            print(f'manifest   {target} ({len(merged["modules"])} modules)')

    if args.check:
        print('\n--check: validation passed, nothing written')
    elif args.dry_run:
        print('\n--dry-run: validation passed, nothing written')
    return 0


if __name__ == '__main__':
    sys.exit(main())
