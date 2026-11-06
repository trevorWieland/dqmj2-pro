import concurrent.futures
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, now
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA
from inspect_windows_native_link_frontier111_20261101 import coff

WORK = ROOT / 'work/windows-selected-functions111-20261101'
OUTPUT = ROOT / 'evidence/portability/windows-selected-functions111-20261101.json'
DRAFTS = ROOT / 'generated/portability/20261101-selected-windows-functions'


def wanted(row):
    names = set()
    for resolution in row.get('selectedEntryResolutions', []):
        names.update(resolution['emitted'])
    for resolution in row.get('acceptedArmSymbolResolutions', []):
        names.update(resolution['emittedSymbols'])
    assert names and names.issubset(row['emittedExternalFunctionSymbols'])
    return names


def flags(command):
    output = []
    index = 1
    while index < len(command):
        item = command[index]
        if item in ['-MF', '-o']:
            index += 2
        elif item in ['-c', '-MMD'] or item.endswith(('.c', '.cpp')):
            index += 1
        else:
            output.append(item)
            index += 1
    return output


def bodies(tree, data):
    output = {}
    pending = [tree]
    while pending:
        node = pending.pop()
        pending.extend(node.get('inner', []))
        if node.get('kind') != 'FunctionDecl':
            continue
        body = next((child for child in node.get('inner', []) if child.get('kind') == 'CompoundStmt'), None)
        if not body:
            continue
        location = node.get('loc', {})
        if 'includedFrom' in location or 'offset' not in location:
            continue
        name = node['name']
        position = location['offset']
        if data[position:position + len(name)] != name.encode('ascii'):
            continue
        begin, end = body['range']['begin'], body['range']['end']
        if 'offset' not in begin or 'offset' not in end:
            continue
        start, stop = begin['offset'], end['offset'] + end['tokLen']
        if data[start:start + 1] != b'{' or data[stop - 1:stop] != b'}':
            continue
        assert name not in output
        output[name] = dict(start=start, end=stop, static=node.get('storageClass') == 'static',
            bodySha256=hashlib.sha256(data[start:stop]).hexdigest())
    return output


def worker(specification):
    number, original = specification
    source = ROOT / original['source']
    assert sha256(source) == original['sourceSha256']
    assert sha256(ROOT / original['object']) == original['objectSha256']
    for dependency in original.get('dependencies', []):
        if 'path' in dependency and 'sha256' in dependency:
            path = Path(dependency['path'])
            path = path if path.is_absolute() else ROOT / path
            assert sha256(path) == dependency['sha256']
    desired = wanted(original)
    result = dict(source=original['source'], sourceSha256=original['sourceSha256'],
        originalObject=original['object'], originalObjectSha256=original['objectSha256'],
        selectedExternalSymbols=sorted(desired), sourceCredit=0, compiled=False, selectedBodiesPreserved=False)
    if source.suffix.lower() != '.c':
        result['diagnostic'] = 'Non-C source retained for separate review'
        return result
    directory = WORK / f'{number:05}'
    directory.mkdir(parents=True, exist_ok=True)
    clang = Path(original['command'][0])
    assert sha256(clang) == CLANG_SHA
    options = flags(original['command'])
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    steps = []

    def run(command):
        command = list(map(str, command))
        attempt = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=attempt.returncode,
            stdoutSha256=hashlib.sha256(attempt.stdout).hexdigest(), stderr=attempt.stderr.decode(errors='replace')))
        assert attempt.returncode == 0, steps[-1]
        return attempt.stdout

    try:
        data = source.read_bytes()
        tree = json.loads(run([clang, *options, '-Xclang', '-ast-dump=json', '-fsyntax-only', source]))
        original_bodies = bodies(tree, data)
        selected = {name: row for name, row in original_bodies.items() if '_' + name in desired}
        assert {'_' + name for name in selected} == desired
        removals = [(name, row) for name, row in original_bodies.items()
            if '_' + name not in desired and not row['static']]
        assert removals
        modified = data
        for name, row in sorted(removals, key=lambda item: item[1]['start'], reverse=True):
            modified = modified[:row['start']] + b';' + modified[row['end']:]
        candidate = DRAFTS / original['source']
        candidate.parent.mkdir(parents=True, exist_ok=True)
        if candidate.exists():
            assert candidate.read_bytes() == modified
        else:
            candidate.write_bytes(modified)
        local_options = [*options, '-iquote', source.parent]
        new_tree = json.loads(run([clang, *local_options, '-Xclang', '-ast-dump=json', '-fsyntax-only', candidate]))
        after = bodies(new_tree, modified)
        assert all(after[name]['bodySha256'] == row['bodySha256'] for name, row in selected.items())
        assert not any(name in after for name, row in removals)
        obj = directory / 'selected.obj'
        run([clang, *local_options, '-c', candidate, '-o', obj])
        symbols = coff(obj)
        emitted = {symbol['name'] for symbol in symbols['definitions'] if symbol['function']}
        assert desired.issubset(emitted)
        result.update(compiled=True, selectedBodiesPreserved=True,
            candidate=candidate.relative_to(ROOT).as_posix(), candidateSha256=sha256(candidate),
            object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj),
            selectedBodyHashes={name: row['bodySha256'] for name, row in selected.items()},
            removedPublicBodies=[dict(name=name, **row) for name, row in removals],
            remainingUnselectedExternalFunctions=sorted(emitted - desired),
            originalExternalFunctionDefinitions=len(original['emittedExternalFunctionSymbols']),
            newExternalFunctionDefinitions=len(emitted), undefinedSymbols=symbols['undefined'])
    except Exception as error:
        result['diagnostic'] = repr(error)
    result['steps'] = steps
    return result


def main():
    assert not OUTPUT.exists()
    census_path = ROOT / 'evidence/portability/windows-source-census111-targetabi-v4-20261101.json'
    census = read_json(census_path)
    detail_path = ROOT / census['details']['path']
    assert sha256(detail_path) == census['details']['sha256']
    raw = gzip.decompress(detail_path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == census['details']['decodedSha256']
    details = json.loads(raw)
    queue = [row for row in details['results'] if row['compiled']
        and set(row['emittedExternalFunctionSymbols']) - wanted(row)]
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        census=dict(path=census_path.relative_to(ROOT).as_posix(), sha256=sha256(census_path)),
        sourceUnits=len(queue), compilerWorkers=6, state='running', sourceCredit=0,
        acceptedArmSourceModified=False, nativeExecutionCount=0, fullWindowsGameProven=False, results=[],
        limitations=['Separate native source variants remove only unselected public function bodies, retaining their declarations',
            'Static helpers and selected body text are preserved; exact AST byte hashes are checked before and after',
            'Selected functions may generate different Windows code when neighboring definitions no longer permit inlining',
            'Undefined callees remain unresolved; no aliases, stubs, blank implementations or linker-forced acceptance are supplied',
            'Function and data namespace ownership, full native ABI and actual execution remain separate gates'])
    write_json(OUTPUT, report)
    print(dict(sourceUnits=len(queue), compilerWorkers=6), flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(worker, item) for item in enumerate(queue)]
        for future in concurrent.futures.as_completed(futures):
            report['results'].append(future.result())
            if len(report['results']) % 25 == 0 or len(report['results']) == len(queue):
                report.update(completed=len(report['results']), compiled=sum(row['compiled'] for row in report['results']))
                write_json(OUTPUT, report)
                print(dict(completed=report['completed'], compiled=report['compiled']), flush=True)
    report.update(state='completed', finishedUtc=now(), compiled=sum(row['compiled'] for row in report['results']),
        failed=sum(not row['compiled'] for row in report['results']),
        removedPublicDefinitions=sum(len(row.get('removedPublicBodies', [])) for row in report['results']))
    write_json(OUTPUT, report)
    print(dict(completed=True, variants=report['compiled'], failed=report['failed'],
        removedPublicDefinitions=report['removedPublicDefinitions'], sourceCredit=0))


if __name__ == '__main__':
    main()
