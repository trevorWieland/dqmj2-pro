import concurrent.futures
import gzip
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA

WORK = ROOT / 'work/windows-pointer-casts-20261101'
OUTPUT = ROOT / 'generated/portability/20261101-pointer-casts'


def position(location):
    return location.get('expansionLoc', location.get('spellingLoc', location))


def macro_end(data, node):
    location = node['range']['end']
    point = position(location)
    end = point['offset'] + point['tokLen']
    if 'expansionLoc' not in location:
        return end
    cursor = end
    while cursor < len(data) and data[cursor:cursor + 1].isspace():
        cursor += 1
    if data[cursor:cursor + 1] != b'(':
        return end
    depth = 0
    quoted = None
    escaped = False
    for index in range(cursor, len(data)):
        byte = data[index]
        if quoted is not None:
            if escaped:
                escaped = False
            elif byte == 92:
                escaped = True
            elif byte == quoted:
                quoted = None
            continue
        if byte in (34, 39):
            quoted = byte
        elif byte == 40:
            depth += 1
        elif byte == 41:
            depth -= 1
            if depth == 0:
                return index + 1
    raise ValueError('Unclosed macro expression')


def edits(ast, data, source):
    selected = set()

    def walk(node):
        if node.get('kind') == 'ImplicitCastExpr' and node.get('castKind') in ['IntegralToPointer', 'PointerToIntegral']:
            begin = position(node['range']['begin'])
            if begin.get('file') and Path(begin['file']).resolve() != source.resolve():
                raise ValueError('Conversion belongs to another file')
            start, end = begin['offset'], macro_end(data, node)
            assert 0 <= start < end <= len(data)
            selected.add((start, end, node['type']['qualType'], node['castKind']))
        for child in node.get('inner', []):
            walk(child)

    walk(ast)
    spans = sorted(selected)
    for first in spans:
        for second in spans:
            if first[0] < second[0] < first[1] < second[1]:
                raise ValueError('Crossing macro ranges require manual review')
    return spans


def apply(data, changes):
    events = {}
    for start, end, target, kind in sorted(changes, key=lambda row: (row[0], -row[1])):
        events.setdefault(start, []).append((0, -end, ('((' + target + ')(').encode()))
        events.setdefault(end, []).append((1, -start, b'))'))
    result = bytearray()
    previous = 0
    for offset, inserts in sorted(events.items()):
        result.extend(data[previous:offset])
        for order, endpoint, text in sorted(inserts, key=lambda item: (-item[0], item[1])):
            result.extend(text)
        previous = offset
    result.extend(data[previous:])
    return bytes(result)


def main():
    census_path = ROOT / 'evidence/portability/windows-source-census111-targetabi-v4-20261101.json'
    census = read_json(census_path)
    details = ROOT / census['details']['path']
    assert sha256(details) == census['details']['sha256']
    data = json.loads(gzip.decompress(details.read_bytes()))
    candidates = [row for row in data['results'] if row.get('diagnosticClass') == 'explicit-pointer-word-conversion-required']
    clang = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe'
    assert sha256(clang) == CLANG_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}

    def process(item):
        number, row = item
        source = ROOT / row['source']
        assert sha256(source) == row['sourceSha256']
        original = source.read_bytes()
        record = dict(source=row['source'], originalSourceSha256=row['sourceSha256'], sourceCredit=0)
        if re.search(rb'^\s*#\s*include\b', original, re.M):
            return dict(record, state='manual-header-scope-required')
        command = [str(clang), '--target=i686-pc-windows-msvc', '-std=c11', '-fpack-struct=4',
            '-Xclang', '-ast-dump=json', '-fsyntax-only', str(source)]
        parsed = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
            timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
        ast = json.loads(parsed.stdout)
        changes = edits(ast, original, source)
        assert changes
        changed = apply(original, changes)
        path = OUTPUT / row['source']
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            assert path.read_bytes() == changed
        path.write_bytes(changed)
        assert sha256(source) == row['sourceSha256']
        obj = WORK / f'{number:03}.obj'
        command = [str(clang), '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding',
            '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing', '-fpack-struct=4',
            '-c', str(path), '-o', str(obj)]
        built = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
            timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
        record.update(state='windows-compiled-unqualified' if built.returncode == 0 else 'windows-refused-unqualified',
            candidate=path.relative_to(ROOT).as_posix(), candidateSha256=sha256(path),
            casts=[dict(start=start, end=end, targetType=target, kind=kind) for start, end, target, kind in changes],
            command=command, compilerExit=built.returncode, diagnostics=built.stderr.decode(errors='replace'),
            objectSha256=sha256(obj) if built.returncode == 0 else None)
        return record

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        pending = {pool.submit(process, item): item[1]['source'] for item in enumerate(candidates)}
        for future in concurrent.futures.as_completed(pending):
            try:
                results.append(future.result())
            except Exception as error:
                results.append(dict(source=pending[future], state='review-required', error=repr(error), sourceCredit=0))
    results.sort(key=lambda row: row['source'])
    counts = {}
    for row in results:
        counts[row['state']] = counts.get(row['state'], 0) + 1
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        census=dict(path=census_path.relative_to(ROOT).as_posix(), sha256=sha256(census_path)),
        sourceCredit=0, selectedSourceModified=False, originalArmByteEquivalenceProven=False,
        nativeBehaviorProven=False, counts=counts, candidates=results,
        limitations=['Generated candidates only; no registry/preferences or accepted source changes',
            'Every explicit cast still requires original per-unit compiler/genuine-link and relevant native behavior validation',
            'Header conversions and ambiguous macro spans remain manual review; no warning or acceptance guard is disabled'])
    write_json(ROOT / 'evidence/portability/windows-pointer-cast-drafts-20261101.json', report)
    print(dict(counts=counts, acceptedSourceChanges=0, sourceCredit=0))


if __name__ == '__main__':
    main()
