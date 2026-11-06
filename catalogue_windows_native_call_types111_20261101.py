import concurrent.futures
import gzip
import hashlib
import json
import os
import subprocess
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, now
from isolate_windows_selected_functions111_20261101 import flags
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA

OUTPUT = ROOT / 'evidence/portability/windows-native-call-types111-20261101.json'


def unpack(report):
    path = ROOT / report['details']['path']
    assert sha256(path) == report['details']['sha256']
    raw = gzip.decompress(path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == report['details']['decodedSha256']
    return json.loads(raw)


def function_reference(node):
    while node.get('kind') in ['ImplicitCastExpr', 'ParenExpr', 'CStyleCastExpr'] and len(node.get('inner', [])) == 1:
        node = node['inner'][0]
    reference = node.get('referencedDecl', {})
    return reference if node.get('kind') == 'DeclRefExpr' and reference.get('kind') == 'FunctionDecl' else None


def scalar_value(node):
    while node.get('kind') in ['ImplicitCastExpr', 'ParenExpr', 'CStyleCastExpr', 'ConstantExpr'] and len(node.get('inner', [])) == 1:
        node = node['inner'][0]
    return node.get('value') if node.get('kind') in ['IntegerLiteral', 'FloatingLiteral'] else None


def worker(specification):
    original, metadata = specification
    source = ROOT / metadata.get('nativeCompileSource', original['source'])
    expected = metadata.get('nativeCompileSourceSha256', original['sourceSha256'])
    assert sha256(source) == expected
    assert sha256(ROOT / metadata['object']) == metadata['objectSha256']
    clang = Path(original['command'][0])
    assert sha256(clang) == CLANG_SHA
    command = [str(clang), *flags(original['command']), '-iquote', str((ROOT / original['source']).parent),
        '-Xclang', '-ast-dump=json', '-fsyntax-only', str(source)]
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    run = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
        timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
    result = dict(source=original['source'], sourceSha256=original['sourceSha256'],
        compileSource=source.relative_to(ROOT).as_posix(), compileSourceSha256=expected,
        object=metadata['object'], objectSha256=metadata['objectSha256'], scopes=metadata['scopes'],
        selectedInstances=metadata['selectedInstances'], command=command, exitCode=run.returncode,
        astSha256=hashlib.sha256(run.stdout).hexdigest(), stderr=run.stderr.decode(errors='replace'))
    if run.returncode:
        result['parsed'] = False
        return result
    tree = json.loads(run.stdout)
    defined = {row['name'] for row in metadata['definitions'] if row['function']}
    undefined = {row['name'] for row in metadata['undefined']}
    declarations, definitions, aliases, calls, indirect, references = {}, {}, {}, [], [], []
    pending = [tree]
    while pending:
        node = pending.pop()
        pending.extend(node.get('inner', []))
        if node.get('kind') == 'TypedefDecl':
            aliases[node['name']] = node.get('type', {})
        if node.get('kind') != 'FunctionDecl':
            continue
        name = node['name']
        emitted = node.get('mangledName', '_' + name)
        if emitted not in defined | undefined:
            continue
        body = next((child for child in node.get('inner', []) if child.get('kind') == 'CompoundStmt'), None)
        record = dict(name=name, symbol=emitted, type=node.get('type', {}),
            parameters=[child.get('type', {}) for child in node.get('inner', []) if child.get('kind') == 'ParmVarDecl'],
            variadic=bool(node.get('variadic')), storageClass=node.get('storageClass'),
            defined=body is not None, location=node.get('loc'))
        declarations.setdefault(emitted, []).append(record)
        if not body or emitted not in defined:
            continue
        definitions[emitted] = record
        inside = [body]
        while inside:
            expression = inside.pop()
            inside.extend(expression.get('inner', []))
            reference = expression.get('referencedDecl', {})
            if expression.get('kind') == 'DeclRefExpr' and reference.get('kind') == 'FunctionDecl':
                references.append(dict(owner=emitted, targetName=reference['name'],
                    referencedType=reference.get('type', {}), range=expression.get('range')))
            if expression.get('kind') != 'CallExpr':
                continue
            children = expression.get('inner', [])
            target = function_reference(children[0]) if children else None
            item = dict(owner=emitted, resultType=expression.get('type', {}),
                arguments=[dict(type=argument.get('type', {}), literalValue=scalar_value(argument))
                    for argument in children[1:]], range=expression.get('range'))
            if target:
                item.update(targetName=target['name'], referencedFunctionType=target.get('type', {}))
                calls.append(item)
            else:
                indirect.append(item)
    result.update(parsed=True, functionDefinitions=definitions, externalDeclarations=declarations,
        typedefs=aliases, directCalls=calls, indirectCalls=indirect, functionReferences=references,
        allDefinedFunctionsFound=set(definitions) == defined)
    return result


def main():
    assert not OUTPUT.exists()
    census_path = ROOT / 'evidence/portability/windows-source-census111-targetabi-v4-20261101.json'
    census = read_json(census_path)
    originals = {row['source']: row for row in unpack(census)['results'] if row['compiled']}
    frontier_path = ROOT / 'evidence/portability/windows-selected-link-frontier111-v3-20261101.json'
    frontier = read_json(frontier_path)
    metadata = unpack(frontier)['objects']
    assert len(metadata) == 8375
    progress = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        sourceCredit=0, state='running', startedUtc=now(), sourceUnits=len(metadata),
        clangWorkers=6, completed=0, parsed=0, unresolvedAbiAliasesApplied=0)
    write_json(OUTPUT, progress)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = [pool.submit(worker, (originals[row['source']], row)) for row in metadata]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            if len(results) % 250 == 0 or len(results) == len(metadata):
                progress.update(completed=len(results), parsed=sum(row['parsed'] for row in results))
                write_json(OUTPUT, progress)
                print(dict(completed=len(results), parsed=progress['parsed']), flush=True)
    results.sort(key=lambda row: row['source'])
    raw = json.dumps(results, sort_keys=True, separators=(',', ':')).encode()
    detail = ROOT / 'evidence/portability/windows-native-call-types111-details-20261101.json.gz'
    detail.write_bytes(gzip.compress(raw, mtime=0))
    progress.update(state='completed', finishedUtc=now(),
        definitionsWithAllCoffFunctions=sum(row.get('allDefinedFunctionsFound', False) for row in results),
        directCallSites=sum(len(row.get('directCalls', [])) for row in results),
        indirectCallSites=sum(len(row.get('indirectCalls', [])) for row in results),
        census=dict(path=census_path.relative_to(ROOT).as_posix(), sha256=sha256(census_path)),
        frontier=dict(path=frontier_path.relative_to(ROOT).as_posix(), sha256=sha256(frontier_path)),
        details=dict(path=detail.relative_to(ROOT).as_posix(), sha256=sha256(detail), decodedSha256=hashlib.sha256(raw).hexdigest()),
        limitations=['AST declarations/call types are observations, not a native ABI compatibility or original-caller proof',
            'No symbol alias, stub, implicit prototype repair or native code substitution is applied',
            'Default promotions, opaque aggregates, function pointers and source-specific views require qualified review',
            'This uses the source111 native frontier before shared-data declaration deduplication; selected function bodies are identical',
            'No native game execution, new source coverage or full Windows game is claimed'])
    write_json(OUTPUT, progress)
    print(dict(completed=len(results), parsed=progress['parsed'], directCalls=progress['directCallSites'],
        indirectCalls=progress['indirectCallSites'], sourceCredit=0))


if __name__ == '__main__':
    main()
