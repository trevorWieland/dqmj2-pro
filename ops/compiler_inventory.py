"""Inventory a compiler archive and compare it with the installed mwccarm builds.

Answers "is this compiler source actually new to us?" by identity, not by directory name:

* hash every ``mwccarm.exe`` in the archive and under ``tools/mwccarm``;
* read each banner with ``-version`` (the only execution this tool performs);
* report archive builds whose bytes are not installed, and builds whose banner collides with
  an installed build but whose bytes differ. The second case is the dangerous one: a recovered
  build can share a version banner with a different executable.

The archive is extracted under ``build/compiler-inventory/`` (gitignored). Nothing is written to
``tools/`` unless the caller copies a build there.

    python ops/compiler_inventory.py --archive work/compiler-source-test/mwccarm.zip
    python ops/compiler_inventory.py --archive mwccarm.zip --json build/compiler-inventory.json
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def banner(exe, license_path):
    env = dict(os.environ)
    if license_path.exists():
        env['LM_LICENSE_FILE'] = str(license_path)
    try:
        result = subprocess.run([str(exe), '-version'], capture_output=True, text=True,
                                timeout=30, env=env)
        text = (result.stdout or '') + (result.stderr or '')
    except Exception as error:  # noqa: BLE001
        return {'version': None, 'runtime': None, 'error': str(error)}
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    version = next((line for line in lines if line.lower().startswith('version ')), None)
    runtime = next((line for line in lines if line.lower().startswith('runtime built')), None)
    return {'version': version, 'runtime': runtime}


def label_for(path, base):
    return str(path.parent.relative_to(base)).replace('\\', '/')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--archive', required=True)
    parser.add_argument('--installed', default=str(ROOT / 'tools/mwccarm'))
    parser.add_argument('--work', default=str(ROOT / 'build/compiler-inventory'))
    parser.add_argument('--exclude', action='append', default=[],
                        help='installed label prefix to ignore (repeatable), e.g. a build this '
                             'run just installed')
    parser.add_argument('--json', dest='json_path')
    args = parser.parse_args(argv)

    installed_root = Path(args.installed).resolve()
    work = Path(args.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    license_path = installed_root / 'mwccarm' / 'license.dat'

    installed = []
    for exe in sorted(installed_root.rglob('mwccarm.exe')):
        label = label_for(exe, installed_root)
        if any(label == item or label.startswith(item.rstrip('/') + '/') for item in args.exclude):
            continue
        data = exe.read_bytes()
        installed.append({'label': label, 'path': str(exe), 'size': len(data),
                          'sha256': hashlib.sha256(data).hexdigest(),
                          **banner(exe, license_path)})
    by_hash = {}
    for row in installed:
        by_hash.setdefault(row['sha256'], []).append(row['label'])
    by_banner = {}
    for row in installed:
        by_banner.setdefault(row['version'], []).append(row['label'])

    archive = []
    with zipfile.ZipFile(args.archive) as bundle:
        bundle.extractall(work)
        members = [info for info in bundle.infolist()
                   if info.filename.lower().endswith('mwccarm.exe')]
        for info in sorted(members, key=lambda item: item.filename):
            target = work / Path(info.filename)
            data = target.read_bytes()
            archive.append({'label': label_for(target, work),
                            'path': str(target), 'size': len(data),
                            'sha256': hashlib.sha256(data).hexdigest(),
                            **banner(target, license_path)})

    new = [row for row in archive if row['sha256'] not in by_hash]
    collisions = [row for row in archive
                  if row['sha256'] not in by_hash and by_banner.get(row['version'])]
    missing = [row for row in installed if row['sha256'] not in
               {item['sha256'] for item in archive}]

    print(f'archive builds: {len(archive)}; installed builds: {len(installed)}')
    print(f'new by sha256: {len(new)}')
    for row in new:
        print(f"  NEW {row['label']:16s} {row['size']:>9d} {row['sha256']} | {row['version']}")
    if collisions:
        print('new builds whose banner already exists among installed builds:')
        for row in collisions:
            print(f"  {row['label']} shares '{row['version']}' with {by_banner[row['version']]}")
    if missing:
        print('installed builds absent from the archive:')
        for row in missing:
            print(f"  {row['label']:16s} {row['sha256']} | {row['version']}")
    print('installed (hash prefixes):')
    for row in installed:
        print(f"  {row['label']:16s} {row['sha256'][:16]} | {row['version']}")

    if args.json_path:
        Path(args.json_path).write_text(json.dumps(
            {'archive': archive, 'installed': installed,
             'new': [row['label'] for row in new],
             'bannerCollisions': [row['label'] for row in collisions],
             'missingFromArchive': [row['label'] for row in missing]}, indent=1) + '\n',
            encoding='utf-8')
        print(f'written {args.json_path}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
