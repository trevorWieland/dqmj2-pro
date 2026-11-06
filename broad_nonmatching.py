import argparse
import concurrent.futures
import hashlib
import os
import re
import subprocess
from pathlib import Path
from project import ROOT, configuration, now, read_json, sha256, write_json
from discover_linked_candidates import entries
from ledger_state import collect_matches, union_size
from reuse_overlay_c import compile_entry
import match_runtime as compiler


def materialize(text, target):
    if re.search(r'\b(?:asm|__asm|__asm__)\b|/\*|//|^\s*#\s*include\s*"', text, re.M):
        raise ValueError('Draft needs assembly/comment/include review before authored C export')
    lines = text.splitlines(keepends=True)
    target.parent.mkdir(parents=True, exist_ok=True)
    dependencies = []
    if len(lines) <= 500:
        target.write_text(text, encoding='utf-8')
    else:
        if re.search(r'^\s*#\s*(?:if|elif|else|endif)\b', text, re.M) or any(line.rstrip().endswith('\\') for line in lines):
            raise ValueError('Large draft needs explicit preprocessing boundaries')
        folder = target.parent / (target.stem + '_parts')
        folder.mkdir(exist_ok=True)
        includes = []
        for index, start in enumerate(range(0, len(lines), 450)):
            part = folder / f'part{index:03d}.inc'
            part.write_text(''.join(lines[start:start + 450]), encoding='utf-8')
            includes.append(f'#include "{folder.name}/{part.name}"\n')
            dependencies.append({'path': part.relative_to(ROOT).as_posix(), 'sha256': sha256(part)})
        target.write_text(''.join(includes), encoding='utf-8')
    return dependencies


def draft(candidate, module, batch):
    old = candidate['entry']
    address = int(old['address'], 0)
    row = {'id': f'{configuration()["romSha256"]}/arm9/{module}/{old["mode"]}/{address:08x}',
           'processor': 'arm9', 'module': module, 'mode': old['mode'], 'address': old['address'],
           'nativeBytes': old['bytes'], 'nativeSpanSha256': old['targetSha256'],
           'originReport': candidate['report'], 'originSource': old['source'], 'originSourceSha256': old['sourceSha256'],
           'acceptedSourceCredit': 0, 'moduleLinked': False, 'semanticsVerified': False}
    try:
        original = ROOT / old['source']
        if sha256(original) != old['sourceSha256']:
            raise ValueError('Historical source changed')
        text = original.read_text(encoding='utf-8')
        source = ROOT / 'nonmatching' / module / batch / (old['name'] + '.c')
        dependencies = materialize(text, source)
        row.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
                   sourceDependencies=dependencies, compileSucceeded=False)
        executable = ROOT / old.get('compilerPath', 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
        compiler_path = executable.relative_to(ROOT).as_posix()
        if sha256(executable) != compiler.COMPILER_PINS.get(compiler_path):
            raise ValueError('Draft compiler is not pinned')
        work = ROOT / 'work/nonmatching' / module / batch / old['name']
        work.mkdir(parents=True, exist_ok=True)
        obj = work / 'draft.o'
        command = [str(executable), *old['compilerFlags'], '-c', str(source), '-o', str(obj)]
        process = subprocess.run(command, cwd=ROOT, env=dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat')),
                                 capture_output=True, text=True, errors='replace', timeout=60)
        row.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), sourceDependencies=dependencies,
                   compilerPath=compiler_path, compilerSha256=sha256(executable), compilerFlags=old['compilerFlags'],
                   compileSucceeded=process.returncode == 0, compileExitCode=process.returncode,
                   compileStdout=process.stdout, compileStderr=process.stderr)
        if process.returncode:
            return row
        row.update(object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj))
        spec = {'name': old['name'], 'module': module, 'mode': old['mode']}
        try:
            comparisons, exact = compile_entry(source, spec, old)
            best = next((item for item in comparisons if item.get('name') == old['name']), None)
            row['comparisons'] = comparisons
            if best:
                row.update(compiledBytes=best['compiledBytes'], matchingBytes=best['matchingBytes'],
                           proximity=best['matchingBytes'] / max(best['bytes'], best['compiledBytes'], 1),
                           relocations=best['relocations'], exactPrelinkCandidate=best['exactAfterDeclaredRelocation'])
        except Exception as error:
            row['comparisonUnsupported'] = f'{type(error).__name__}: {error}'
        row['limitations'] = ['Fresh compilation is not native semantic verification or acceptance',
                              'Byte proximity uses declared relocation arithmetic and may miss genuine linker interworking',
                              'ABI/field meanings, valid inputs and whole-module layout remain unresolved until separately measured']
    except Exception as error:
        row['draftFailure'] = f'{type(error).__name__}: {error}'
    return row


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--module', choices=['main', 'ov001', 'ov005', 'ov006'], required=True)
    parser.add_argument('--batch', required=True)
    parser.add_argument('--workers', type=int, choices=[1, 2, 3], default=3)
    parser.add_argument('--limit', type=int, default=512)
    parser.add_argument('--offset', type=int, default=0)
    options = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9-]+', options.batch):
        raise ValueError('Invalid private draft batch name')
    known, rejected = collect_matches(configuration()['romSha256'])
    accepted = [(address, address + row['size']) for (module, mode, address), row in known.items() if module == options.module]
    selected = {}
    for path in sorted((ROOT / 'evidence/attempts').glob(options.module + '-*.json')):
        if not any(word in path.name for word in ('draft', 'null', 'runtime')):
            continue
        for entry in entries(read_json(path)):
            if entry['module'] != options.module:
                continue
            address = int(entry['address'], 0)
            if any(address < end and begin < address + entry['bytes'] for begin, end in accepted):
                continue
            source = ROOT / entry['source']
            if not source.is_file() or sha256(source) != entry['sourceSha256']:
                continue
            key = entry['mode'], address
            ratio = entry['matchingBytes'] / max(entry['bytes'], entry['compiledBytes'], 1)
            if key not in selected or ratio > selected[key]['ratio']:
                selected[key] = {'entry': entry, 'report': path.relative_to(ROOT).as_posix(), 'ratio': ratio}
    candidates = sorted(selected.values(), key=lambda row: (-row['entry']['bytes'], -row['ratio'], row['entry']['address']))[options.offset:options.offset + options.limit]
    target = ROOT / 'evidence/nonmatching' / options.module / (options.batch + '.json')
    rows = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=options.workers) as pool:
        for row in pool.map(lambda item: draft(item, options.module, options.batch), candidates):
            rows.append(row)
            if len(rows) % 25 == 0:
                print({'drafted': len(rows), 'compiled': sum(row.get('compileSucceeded', False) for row in rows)}, flush=True)
    def coverage(items):
        return union_size([(int(row['address'], 0), int(row['address'], 0) + row['nativeBytes']) for row in items])
    authored = [row for row in rows if row.get('source')]
    compiled = [row for row in authored if row['compileSucceeded']]
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'], 'module': options.module,
              'candidateBacklog': len(selected), 'selected': len(candidates), 'draftedFunctions': len(authored),
              'draftedUniqueNativeBytes': coverage(authored), 'compiledFunctions': len(compiled),
              'compiledUniqueNativeBytes': coverage(compiled), 'acceptedSourceCredit': 0, 'functions': rows}
    write_json(target, report)
    print({key: report[key] for key in ['draftedFunctions', 'draftedUniqueNativeBytes', 'compiledFunctions', 'compiledUniqueNativeBytes', 'acceptedSourceCredit']})


if __name__ == '__main__':
    main()
