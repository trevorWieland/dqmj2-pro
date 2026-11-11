"""Compile one row with every installed mwccarm build and score it against the image.

The compiler audit so far only sampled **accepted** functions, which reproduce by
construction. This tool answers the other question: for a row that does *not*
reproduce under the pinned build, does any other installed build produce the image?

    python ops/compiler_matrix.py --module ov006 --rows ops/compiler_specs/rows.json
    python ops/compiler_matrix.py --module ov006 --rows ops/compiler_specs/rows.json \\
        --json build/compiler-matrix.json

For each row it prints a matrix line per build: score, size and first difference, then
a summary of which builds reproduced which rows. Status is 0 when at least one build
reproduces at least one row (i.e. the row is a build-selection problem, not
unreachable), 1 otherwise.
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import form_search  # noqa: E402


def installed_builds(root):
    """Every compiler under tools/mwccarm, however the install nests it.

    The pinned tree nests as ``mwccarm/<version>/<variant>/``, while a recovered
    build can sit directly as ``tools/mwccarm/<year>/<tag>/``.
    """
    builds = []
    seen = set()
    for compiler in sorted((root / 'tools/mwccarm').rglob('mwccarm.exe')):
        label = f'{compiler.parent.parent.name}/{compiler.parent.name}'
        if label in seen:
            continue
        seen.add(label)
        builds.append((label, compiler))
    return builds


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--module', required=True)
    parser.add_argument('--rows', required=True)
    parser.add_argument('--root', default=str(ROOT))
    parser.add_argument('--json', dest='json_path')
    parser.add_argument('--work', default=None)
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    spec = json.loads(Path(args.rows).read_text(encoding='utf-8'))
    rows = spec['rows']
    builds = installed_builds(root)
    work = Path(args.work or root / 'build/compiler_matrix')
    work.mkdir(parents=True, exist_ok=True)
    image, _, base = form_search.module_image(root, args.module)

    print(f'builds: {len(builds)}; rows: {len(rows)}')
    results = {}
    exact_count = 0
    for row in rows:
        address = int(row['address'], 0)
        want = image[address - base: address - base + row['bytes']]
        source = Path(row['source'])
        if not source.is_absolute():
            source = root / source
        text = source.read_text(encoding='utf-8')
        source_path = work / f"{row['name']}.c"
        source_path.write_text(text, encoding='utf-8')
        print(f"\n=== {row['address']} ({row['bytes']} B) {row['label']}")
        per_build = {}
        for label, compiler in builds:
            obj = work / f"{row['name']}-{label.replace('/', '-')}.o"
            compiled = form_search.compile_source(compiler, source_path, obj, root)
            if compiled.returncode != 0:
                per_build[label] = None
                continue
            text_bytes, defined, relocations = form_search.read_object(obj)
            try:
                actual = form_search.relocate(text_bytes, address, relocations, defined)
            except ValueError:
                per_build[label] = None
                continue
            current = form_search.score(actual, want)
            first = next((i for i, (a, b) in enumerate(zip(actual, want)) if a != b), None)
            per_build[label] = {'score': current, 'size': len(actual), 'first_diff': first}
            marker = 'EXACT' if current == (0, 0) else f'{current}'
            print(f'  {label:14s} {marker:12s} size={len(actual):3d} '
                  f'first_diff={first if first is not None else "-"}')
            if current == (0, 0):
                exact_count += 1
        results[row['name']] = per_build

    print('\n=== summary')
    flips = {}
    for row in rows:
        hits = [label for label, value in results[row['name']].items()
                if value and value['score'] == (0, 0)]
        flips[row['name']] = hits
        print(f"  {row['address']:>10s} {row['label'][:52]:54s} "
              f"{'EXACT by ' + ', '.join(hits) if hits else 'no build reproduces'}")
    if args.json_path:
        Path(args.json_path).write_text(json.dumps({'rows': results, 'flips': flips},
                                                   indent=1) + '\n', encoding='utf-8')
        print(f'matrix written: {args.json_path}')
    print(f'\n{exact_count} row/build reproductions out of {len(rows) * len(builds)}')
    return 0 if exact_count else 1


if __name__ == '__main__':
    sys.exit(main())
