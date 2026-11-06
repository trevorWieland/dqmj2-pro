import concurrent.futures
import os
import re
import subprocess
from pathlib import Path
import match_runtime as compiler
from slice_reference_sdk_entities_v3_20261102 import functions, slice_closed
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


WORK = ROOT / 'work/main-nitrosdk-visibility-closed-20261102'
OUTPUT = ROOT / 'evidence/attempts/main-nitrosdk-visibility-closed-20261102.json'


def worker(row):
    entry = row['entry']
    address = int(entry['address'], 0)
    folder = WORK / f'{address:08x}'
    folder.mkdir(parents=True, exist_ok=True)
    result = dict(identity=row['identity'], referenceFunction=row['referenceFunction'], profile=row['profile'], sourceCredit=0)
    try:
        original = ROOT / row['referenceSource']
        assert sha256(original) == entry['sourceSha256']
        executable = ROOT / entry['compiler']
        assert sha256(executable) == entry['compilerSha256']
        expanded = folder / 'expanded.i'
        flags = list(entry['compilerFlags'])
        command = [str(executable), *flags, '-E', str(original), '-o', str(expanded)]
        process = subprocess.run(command, cwd=ROOT, capture_output=True, timeout=60,
            env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')))
        result.update(preprocessingExitCode=process.returncode, preprocessingCommand=command,
            stdout=process.stdout.decode(errors='replace'), stderr=process.stderr.decode(errors='replace'))
        assert process.returncode == 0
        text = expanded.read_text(encoding='utf-8')
        seed = row['referenceFunction']
        for function in sorted(functions(text), key=lambda f: f['start'], reverse=True):
            header = text[function['start']:function['opening']]
            if function['name'] == seed or re.search(r'\binline\b', header): continue
            text = text[:function['start']] + re.sub(r'\bstatic\s+', '', header).rstrip() + ';\n' + text[function['end']:]
        text, selection = slice_closed(text, [seed])
        result['selection'] = selection
        forbidden = re.findall(r'\b(?:asm|__asm|__asm__|va_list|size_t|J2pUnknownVaList)\b', text)
        assert not forbidden, ('Nonordinary or provisional source tokens', sorted(set(forbidden)))
        aliases = {seed: f'native_main_{address:08x}'}
        for name, binding in row['bindings'].items():
            if name == seed: continue
            assert re.fullmatch(r'[A-Za-z_]\w*', name), ('Nonlexical ELF symbol needs storage review', name)
            target = int(binding['address'], 0)
            alias = f'native_fn_{target:08x}' if binding['kind'] == 'function' else f'native_data_main_{target:08x}'
            assert name not in aliases or aliases[name] == alias
            aliases[name] = alias
        for name in sorted(aliases, key=len, reverse=True):
            text = re.sub(r'\b' + re.escape(name) + r'\b', aliases[name], text)
        assert len(text.splitlines()) <= 500, ('Source exceeds500lines', len(text.splitlines()))
        source = ROOT / f'nonmatching/main/20261102-nitrosdk-visibility-closed/native_main_{address:08x}.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists()
        source.write_text(text, encoding='utf-8')
        result.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), aliases=aliases,
            expandedSha256=sha256(expanded), physicalLines=len(text.splitlines()))
        compiler.FLAGS = flags
        compiler.WORK = folder / 'compile'
        rows, _ = compiler.compare(source, 'main', '2', 'off', compiler=executable)
        result['compilationRows'] = rows
        assert len(rows) == 1 and not rows[0].get('compileFailed')
        compiled = rows[0]
        proof = validate(compiled, qualified_bindings(compiled), folder / 'link')
        result.update(genuineExact=True, compiledEntry=compiled, genuineLinkProof=proof, genuineLinkedBytes=compiled['bytes'])
    except Exception as error:
        result.update(genuineExact=False, refusalType=type(error).__name__, refusal=repr(error))
    write_json(folder / 'result.json', result)
    return result


def main():
    assert not OUTPUT.exists()
    input_report = ROOT / 'evidence/attempts/main-nitrosdk-visibility-v1-linked-archive-20261102.json'
    chosen = {}
    for row in read_json(input_report)['results']:
        if not row.get('genuineLinkedExact'): continue
        key = row['identity']['address']
        priority = {'base4p': 0, 'base2space': 1, 'sp2space': 2, 'base2speed': 3}[row['profile']]
        if key not in chosen or priority < chosen[key][0]: chosen[key] = priority, row
    queue = [item[1] for item in sorted(chosen.values(), key=lambda item: -item[1]['identity']['bytes'])]
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
        inputReportSha256=sha256(input_report), compilerProcesses=3, queuedFunctions=len(queue), results=[])
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for result in pool.map(worker, queue):
            report['results'].append(result)
            if len(report['results']) % 16 == 0:
                write_json(OUTPUT, report)
                print(dict(completed=len(report['results']), total=len(queue),
                    exact=sum(r['genuineExact'] for r in report['results'])), flush=True)
    report.update(genuineExactFunctions=sum(r['genuineExact'] for r in report['results']),
        genuineExactBytes=sum(r.get('genuineLinkedBytes', 0) for r in report['results']),
        interfaceBoundaryNativeAndSharedAcceptanceStillPending=True)
    write_json(OUTPUT, report)
    print(dict(functions=report['genuineExactFunctions'], bytes=report['genuineExactBytes'], sourceCredit=0))


if __name__ == '__main__':
    main()
