import concurrent.futures
import gzip
import hashlib
import json
import os
import re
import shlex
import struct
import subprocess
import sys
import threading
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256, now
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA

SNAPSHOT = 'evidence/verification/accepted-cohort111-identities-v2-20261101.json'
WORK = ROOT / 'work/windows-source-census111-targetabi-v2-20261101'
PROGRESS = ROOT / 'evidence/portability/windows-source-census111-targetabi-v2-progress-20261101.json'
HASHES = {}
LOCK = threading.Lock()


def definitions(path):
    data = path.read_bytes()
    machine, sections, stamp, offset, count, optional, characteristics = struct.unpack_from('<HHIIIHH', data)
    assert machine == 0x14C
    strings = offset + count * 18
    names = []
    index = 0
    while index < count:
        start = offset + index * 18
        raw = data[start:start + 8]
        if raw[:4] == bytes(4):
            address = strings + struct.unpack_from('<I', raw, 4)[0]
            end = data.find(b'\0', address)
            name = data[address:end].decode('utf-8', errors='replace')
        else:
            name = raw.rstrip(b'\0').decode('utf-8', errors='replace')
        section, kind, storage, auxiliary = struct.unpack_from('<hHBB', data, start + 12)
        if section > 0 and storage == 2 and kind & 0x20:
            names.append(name)
        index += 1 + auxiliary
    return sorted(set(names))


def dependency_hashes(path):
    if not path.is_file():
        return []
    raw = path.read_text(encoding='utf-8').replace('\\\n', ' ')
    if ': ' not in raw:
        return [dict(parseFailed=True, dependencyFileSha256=sha256(path))]
    names = shlex.split(raw.split(': ', 1)[1], posix=True)
    results = []
    for name in names:
        source = Path(name)
        if not source.is_absolute():
            source = ROOT / source
        source = source.resolve()
        if not source.is_file():
            results.append(dict(path=str(source), missing=True))
            continue
        with LOCK:
            digest = HASHES.get(str(source))
        if digest is None:
            digest = sha256(source)
            with LOCK:
                HASHES[str(source)] = digest
        relative = source.relative_to(ROOT).as_posix() if source.is_relative_to(ROOT) else str(source)
        results.append(dict(path=relative, sha256=digest, repositoryLocal=source.is_relative_to(ROOT)))
    return results


def classify(stderr):
    if 'file not found' in stderr:
        return 'missing-header'
    if any(word in stderr for word in ['invalid instruction mnemonic', 'invalid operand for instruction', 'unknown register name', 'unsupported inline asm']):
        return 'target-assembly-or-register'
    if 'static assertion failed' in stderr:
        return 'host-layout-assertion'
    if 'undeclared identifier' in stderr or 'unknown type name' in stderr:
        return 'missing-type-or-declaration'
    if 'too few arguments' in stderr or 'too many arguments' in stderr or 'conflicting types' in stderr:
        return 'signature-or-type-conflict'
    return 'other-compiler-diagnostic'


def main():
    layout_path = ROOT / 'evidence/portability/windows-target-layout-20261101.json'
    layout = read_json(layout_path)
    assert layout['targetProfilesAgree'] and layout['windowsMatchesMeasuredTarget']['pack4']
    assert not layout['windowsMatchesMeasuredTarget']['default']
    snapshot = read_json(ROOT / SNAPSHOT)
    groups = {}
    for row in snapshot['functions']:
        groups.setdefault(row['source'], []).append(row)
    selected = [(name, rows) for name, rows in sorted(groups.items()) if Path(name).suffix.lower() in ['.c', '.cpp']]
    excluded = [dict(source=name, sourceSha256=rows[0]['sourceSha256'], selectedInstances=len(rows),
        reason='Assembly source requires a separately justified native platform implementation')
        for name, rows in sorted(groups.items()) if Path(name).suffix.lower() not in ['.c', '.cpp']]
    clang = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin/clang.exe'
    assert sha256(clang) == CLANG_SHA
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    WORK.mkdir(parents=True, exist_ok=True)
    started = now()
    begun = time.monotonic()
    progress = dict(state='running', startedUtc=started, generator=Path(__file__).name,
        generatorSha256=sha256(__file__), snapshot=SNAPSHOT, snapshotSha256=sha256(ROOT / SNAPSHOT),
        sourceUnits=len(selected), excludedAssemblyUnits=len(excluded), workers=6, completed=0,
        compiled=0, failed=0, selectedSymbolOmissions=0, sourceCredit=0, nativeExecutionCount=0, targetLayoutProbe=dict(path=layout_path.relative_to(ROOT).as_posix(), sha256=sha256(layout_path)), targetPackingBytes=4)
    write_json(PROGRESS, progress)

    def compile_one(item):
        number, (name, rows) = item
        source = ROOT / name
        expected_hashes = {row['sourceSha256'] for row in rows}
        assert len(expected_hashes) == 1 and sha256(source) in expected_hashes
        directory = WORK / f'{number:05}'
        directory.mkdir(parents=True, exist_ok=True)
        obj, dep = directory / 'source.obj', directory / 'source.d'
        standard = '-std=c++17' if source.suffix.lower() == '.cpp' else '-std=c11'
        command = [str(clang), '--target=i686-pc-windows-msvc', standard, '-O2', '-ffreestanding',
            '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing', '-fpack-struct=4', '-MMD', '-MF', str(dep),
            '-I', str(ROOT), '-c', str(source), '-o', str(obj)]
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True,
            timeout=60, creationflags=subprocess.CREATE_NO_WINDOW)
        assert sha256(source) in expected_hashes
        diagnostics = result.stderr.decode('utf-8', errors='replace')
        (directory / 'diagnostics.txt').write_text(diagnostics, encoding='utf-8')
        row = dict(source=name, sourceSha256=next(iter(expected_hashes)),
            selectedInstances=len(rows), selectedInitializedBytes=sum(entry['bytes'] for entry in rows),
            command=command, exitCode=result.returncode, compiled=result.returncode == 0,
            diagnosticClass=None if result.returncode == 0 else classify(diagnostics),
            stderr=diagnostics, stdoutSha256=hashlib.sha256(result.stdout).hexdigest(),
            dependencies=dependency_hashes(dep), nativeExecutionCount=0, sourceCredit=0)
        if result.returncode == 0:
            symbols = definitions(obj)
            missing = []
            resolutions = []
            for entry in rows:
                names = {entry['name']}
                if entry['name'].startswith('func_'):
                    names.add('native_' + entry['name'][5:])
                names.update({'_' + name for name in list(names)})
                exact_names = set(symbols).intersection(names)
                address = int(entry['address'], 0) if isinstance(entry['address'], str) else entry['address']
                suffix = f'{address:08x}'
                suffix_matches = [name for name in symbols if re.search(r'(?:^|_)' + suffix + r'$', name, re.I)]
                resolved = sorted(exact_names) if exact_names else suffix_matches if len(suffix_matches) == 1 else []
                if not resolved:
                    missing.append(entry['name'])
                resolutions.append(dict(processor=entry['processor'], program=entry['program'], module=entry['module'],
                    mode=entry['mode'], address=entry['address'], ledgerName=entry['name'], emitted=resolved,
                    rule='qualified-source-address-suffix' if not exact_names and resolved else 'canonical-alias'))
            row['selectedEntryResolutions'] = resolutions
            missing = sorted(set(missing))
            row.update(object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj),
                emittedExternalFunctionSymbols=symbols, selectedSymbolsMissing=missing,
                selectedSymbolsPresent=len({entry['name'] for entry in rows}) - len(missing))
        return row

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        futures = {pool.submit(compile_one, item): item[1][0] for item in enumerate(selected)}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                row = future.result()
            except Exception as error:
                row = dict(source=name, compiled=False, diagnosticClass='census-execution-failure',
                    error=repr(error), sourceCredit=0, nativeExecutionCount=0)
            results.append(row)
            progress['completed'] += 1
            progress['compiled' if row['compiled'] else 'failed'] += 1
            progress['selectedSymbolOmissions'] += int(bool(row.get('selectedSymbolsMissing')))
            if len(results) % 100 == 0 or len(results) == len(selected):
                progress['elapsedSeconds'] = round(time.monotonic() - begun, 3)
                write_json(PROGRESS, progress)
                print({key: progress[key] for key in ['completed', 'sourceUnits', 'compiled', 'failed', 'selectedSymbolOmissions']}, flush=True)
    results.sort(key=lambda row: row['source'])
    raw = json.dumps(dict(results=results, excluded=excluded), sort_keys=True, separators=(',', ':')).encode()
    detail = ROOT / 'evidence/portability/windows-source-census111-targetabi-v2-details-20261101.json.gz'
    detail.write_bytes(gzip.compress(raw, mtime=0))
    classes = {}
    for row in results:
        if not row['compiled']:
            kind = row['diagnosticClass']
            classes[kind] = classes.get(kind, 0) + 1
    progress.update(state='completed', finishedUtc=now(), elapsedSeconds=round(time.monotonic() - begun, 3),
        diagnosticClasses=classes, clang=dict(path=clang.relative_to(ROOT).as_posix(), sha256=sha256(clang)),
        details=dict(path=detail.relative_to(ROOT).as_posix(), sha256=sha256(detail), decodedSha256=hashlib.sha256(raw).hexdigest()),
        allSelectedFunctionsProvenEmitted=False, fullNativeLinkProven=False, fullWindowsGameProven=False,
        limitations=['Unmodified accepted111 C/C++ compile only with measured four-byte target packing; objects are neither linked nor executed',
            'Assembly sources are enumerated separately and do not count as native compiler successes',
            'COFF source-qualified names and unique exact address suffixes are checked; no broader cross-module or ABI equivalence follows',
            'Current repository-local headers are hashed; missing or external dependencies remain diagnostics',
            'No compatibility stubs, fake source definitions or generated disassembly are used as native implementation'])
    write_json(PROGRESS, progress)
    write_json(ROOT / 'evidence/portability/windows-source-census111-targetabi-v2-20261101.json', progress)
    print(dict(state='completed', compiled=progress['compiled'], failed=progress['failed'], sourceCredit=0), flush=True)


if __name__ == '__main__':
    main()
