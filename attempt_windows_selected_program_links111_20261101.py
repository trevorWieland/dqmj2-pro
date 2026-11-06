import gzip
import hashlib
import json
import os
import subprocess
from collections import defaultdict
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from check_save_core_explicit_clear_windows32_20261101 import LINKER_SHA


def main():
    frontier_path = ROOT / 'evidence/portability/windows-selected-link-frontier111-v3-20261101.json'
    frontier = read_json(frontier_path)
    details_path = ROOT / frontier['details']['path']
    assert sha256(details_path) == frontier['details']['sha256']
    raw = gzip.decompress(details_path.read_bytes())
    assert hashlib.sha256(raw).hexdigest() == frontier['details']['decodedSha256']
    detail = json.loads(raw)
    groups = defaultdict(dict)
    for row in detail['objects']:
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert sha256(ROOT / row['object']) == row['objectSha256']
        if 'nativeCompileSource' in row:
            assert sha256(ROOT / row['nativeCompileSource']) == row['nativeCompileSourceSha256']
        for processor, program, module in row['scopes']:
            groups[processor, program][row['objectSha256']] = row
    linker = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/ld.lld.exe'
    assert sha256(linker) == LINKER_SHA
    work = ROOT / 'work/windows-selected-program-links111-20261101'
    work.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    attempts = []
    for index, ((processor, program), members) in enumerate(sorted(groups.items())):
        label = f'{index:02}-{processor}'
        dll = work / (label + '.dll')
        assert not dll.exists()
        objects = [ROOT / row['object'] for row in sorted(members.values(), key=lambda row: row['source'])]
        arguments = ['/dll', '/noentry', '/machine:x86', '/nodefaultlib', '/safeseh:no',
            '/timestamp:0', '/errorlimit:0', '/opt:noref', '/out:' + str(dll), *map(str, objects)]
        response = work / (label + '.rsp')
        response.write_text('\n'.join(subprocess.list2cmdline([value]) for value in arguments) + '\n', encoding='utf-8')
        command = [str(linker), '-flavor', 'link', '@' + str(response)]
        run = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        diagnostic = run.stdout + run.stderr
        log = ROOT / f'evidence/portability/windows-program-link111-{label}-diagnostic-20261101.txt.gz'
        log.write_bytes(gzip.compress(diagnostic, mtime=0))
        text = diagnostic.decode(errors='replace')
        row = dict(processor=processor, program=program, objectUnits=len(objects),
            command=command, responseFile=response.relative_to(ROOT).as_posix(), responseSha256=sha256(response),
            exitCode=run.returncode, outputProduced=dll.is_file(),
            outputSha256=sha256(dll) if dll.is_file() else None,
            undefinedSymbolDiagnosticCount=text.count('undefined symbol:'),
            duplicateSymbolDiagnosticCount=text.count('duplicate symbol:'),
            diagnostic=dict(path=log.relative_to(ROOT).as_posix(), sha256=sha256(log),
                decodedSha256=hashlib.sha256(diagnostic).hexdigest()),
            nativeExecutionCount=0, fullGame=False)
        assert run.returncode != 0 and not row['outputProduced'], row
        assert row['undefinedSymbolDiagnosticCount'] + row['duplicateSymbolDiagnosticCount'] > 0, row
        row['undefinedScanMayStopAtDuplicate'] = bool(row['duplicateSymbolDiagnosticCount'] and not row['undefinedSymbolDiagnosticCount'])
        attempts.append(row)
        print(dict(processor=processor, program=program, objects=len(objects),
            exitCode=run.returncode, undefined=row['undefinedSymbolDiagnosticCount'],
            duplicates=row['duplicateSymbolDiagnosticCount']), flush=True)
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        frontier=dict(path=frontier_path.relative_to(ROOT).as_posix(), sha256=sha256(frontier_path)),
        linker=dict(path=linker.relative_to(ROOT).as_posix(), sha256=sha256(linker)), attempts=attempts,
        diagnosticsMeasured=True, nativeLinksSucceeded=0, nativeExecutionCount=0, sourceCredit=0,
        generatedStubs=0, aliasesApplied=0, unresolvedAcceptanceForced=False,
        acceptedArmSourcesModified=False, fullWindowsGameProven=False,
        limitations=['Diagnostic DLL links have no entry point and are never loaded; this is not a playable or complete game',
            'All selected C source objects are retained with opt:noref; no missing logic is hidden by dead-code collection',
            'Host/utility processor programs remain separate; physically overlapping overlays still require qualified runtime ownership',
            'Compiler-blocked source units, ARM assembly and later cohorts remain outside this source111 corpus',
            'Undefined and duplicate symbols are retained as hard failures; no force flags or compatibility stubs are used'])
    write_json(ROOT / 'evidence/portability/windows-selected-program-links111-20261101.json', report)


if __name__ == '__main__':
    main()
