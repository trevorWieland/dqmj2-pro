import gzip
import hashlib
import json
import os
import random
import struct
import subprocess
import zipfile
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA
import match_runtime
from elftools.elf.elffile import ELFFile

WORK = ROOT / 'work/android-random-word152-20261101'
BUNDLE = ROOT / 'build/ports/android-random-word152-20261101'


def main():
    windows_path = ROOT / 'evidence/portability/random-word152-windows32-20261101.json'
    windows = read_json(windows_path)
    assert windows['allPassed'] and windows['actualWindowsTopReturns'] == 1024
    original_path = ROOT / 'evidence/matches/main-random-word152-20261101.json'
    original = read_json(original_path)
    assert windows['originalArmEvidence']['sha256'] == sha256(original_path)
    trace_path = ROOT / 'evidence/traces/main-random-word152-20261101.json.gz'
    assert windows['originalArmTrace']['sha256'] == sha256(trace_path)
    cases = json.loads(gzip.decompress(trace_path.read_bytes()))
    rng = random.Random(0x152003D1)
    payload = bytearray(struct.pack('<I', len(cases)))
    expected = bytearray()
    for pair in cases:
        native = pair['original']
        assert native == pair['candidate'] and native['actualReturn'] and native['modelPassed']
        array = bytearray(rng.randbytes(16))
        payload.extend(struct.pack('<II', native['case']['seed'], native['case']['argument']))
        payload.extend(array)
        value = native['result']
        seed = next(row[2] for row in reversed(native['writes']) if row[0] == 0x020F6044)
        predicate = int(value >> 16 == (((value & 255) * ~(value >> 8 & 255) + 123) & 65535))
        struct.pack_into('<I', array, 12, value)
        expected.extend(struct.pack('<III', value, seed, predicate))
        expected.extend(array)
    assert hashlib.sha256(payload).hexdigest() == windows['inputSha256']
    assert hashlib.sha256(expected).hexdigest() == windows['expectedOutputSha256']
    ndk = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = ndk / 'bin/clang.exe', ndk / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    BUNDLE.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    variants = ROOT / 'generated/portability/20261101-random-word152-shared-views'
    sources = [ROOT / 'ports/android-native/random_word152_runner_20261101.c',
        variants / 'word.c', ROOT / 'src/mechanics_save/runtime_rng.c', variants / 'predicate.c']
    assert sha256(ROOT / original['matches'][0]['source']) == original['matches'][0]['sourceSha256']
    steps, objects, dependencies = [], [], set()
    def run(command):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT.parent, env=environment, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode, stdout=result.stdout.decode(errors='replace'),
            stderr=result.stderr.decode(errors='replace')))
        assert result.returncode == 0, steps[-1]
        return result
    for index, source in enumerate(sources):
        obj, dep = WORK / f'{index}.o', WORK / f'{index}.d'
        run([clang, '--target=aarch64-linux-android26', '--sysroot=' + str(ndk / 'sysroot'),
            '-std=c11', '-O2', '-fPIE', '-fno-strict-aliasing', '-I', ROOT / 'ports/common',
            '-MD', '-MF', dep, '-c', source, '-o', obj])
        body = dep.read_text().split(': ', 1)[1].replace('\\\n', ' ')
        for token in body.split():
            path = Path(token).resolve()
            assert path.is_file() and path.is_relative_to(ROOT), token
            dependencies.add(path)
        objects.append(obj)
    executable = BUNDLE / 'random-word152'
    linked = run([clang, '--target=aarch64-linux-android26', '--sysroot=' + str(ndk / 'sysroot'),
        '-fuse-ld=lld', '-fPIE', '-pie', '-Wl,--build-id=sha1', '-Wl,--trace', *objects, '-o', executable])
    for line in linked.stdout.decode(errors='replace').splitlines():
        value = line.strip().split('(', 1)[0]
        path = Path(value)
        if path.is_file():
            path = path.resolve()
            assert path.is_relative_to(ROOT), value
            dependencies.add(path)
    with executable.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf.elfclass == 64 and elf.little_endian and elf['e_machine'] == 'EM_AARCH64' and elf['e_type'] == 'ET_DYN'
        interpreter = next(segment.get_interp_name() for segment in elf.iter_segments() if segment['p_type'] == 'PT_INTERP')
        assert interpreter == '/system/bin/linker64'
        names = {symbol.name for symbol in elf.get_section_by_name('.symtab').iter_symbols()}
        assert {'native_main_0203d158', 'native_main_0203d1f0', 'saved_runtime_random'} <= names
    (BUNDLE / 'vectors.bin').write_bytes(payload)
    (BUNDLE / 'expected.bin').write_bytes(expected)
    hashes = '\n'.join(sha256(BUNDLE / name) + '  ' + name for name in ['random-word152', 'vectors.bin', 'expected.bin']) + '\n'
    (BUNDLE / 'SHA256SUMS').write_text(hashes, encoding='ascii')
    readme = ('# Private Android ARM64 RNG-word component test\n\n'
        'This is a native command-line component, not the game or a dual-screen interface. It targets Android API26 and later; device compatibility is unverified. No device execution has occurred.\n\n'
        'Keep the bundle private. After copying it to a disposable executable test directory on an authorized Android ARM64 device, run:\n\n'
        '```sh\nchmod 700 random-word152\n./random-word152 < vectors.bin > actual.bin\ncmp actual.bin expected.bin\n```\n\n'
        'Successful execution requires exit0 and exact binary equality for512 synthetic contexts. SHA256SUMS identifies the bundle. It reads no ROM/save files and uses no display, audio or network APIs. The identical input/expected bytes have passed two actual Windows PE32 processes; Android floating, pointer-heavy or full-game behavior is not established.\n')
    (BUNDLE / 'README.md').write_text(readme, encoding='utf-8')
    bundle_zip = BUNDLE.with_suffix('.zip')
    with zipfile.ZipFile(bundle_zip, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(BUNDLE.iterdir()):
            if path.is_file():
                entry = zipfile.ZipInfo(path.name, date_time=(2000, 1, 1, 0, 0, 0))
                entry.compress_type = zipfile.ZIP_DEFLATED
                entry.external_attr = (0o100755 if path.name == 'random-word152' else 0o100644) << 16
                archive.writestr(entry, path.read_bytes(), compresslevel=9)
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
        target='aarch64-linux-android26', executableFormat='ELF64/AArch64/PIE', interpreter=interpreter,
        compiledComponentFunctions=3, syntheticContexts=len(cases), androidDeviceExecutions=0,
        actualWindowsTopReturnsReferenced=1024, wholeGame=False, dualScreenInterface=False,
        nativeElfCompiledAndLinked=True, elfMetadataVerified=True, allPassed=True,
        privateBundleZip=dict(path=bundle_zip.relative_to(ROOT).as_posix(), sha256=sha256(bundle_zip), bytes=bundle_zip.stat().st_size),
        inputs=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in sources],
        compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA,
        dependencies=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in sorted(dependencies)],
        bundle=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), bytes=path.stat().st_size)
            for path in sorted(BUNDLE.iterdir()) if path.is_file()],
        windowsEvidence=dict(path=windows_path.relative_to(ROOT).as_posix(), sha256=sha256(windows_path)), steps=steps,
        limitations=['Cross-compilation and ELF inspection only; no actual Android/Thor execution or system inspection',
            'Only a primitive word/global-data component with explicit positive RNG-limit wrappers; no ARM64 pointer model or full engine',
            'Synthetic payload/expected output are identical to the actual Windows test; no original ROM/save content enters this component',
            'Full native game, module completeness, scene reachability, dual-screen UI and a source-only ROM remain unproved'])
    write_json(ROOT / 'evidence/portability/android-random-word152-build-20261101.json', report)
    print(dict(nativeAndroidElfBuilt=True, syntheticContexts=len(cases), androidExecutions=0,
        pinnedDependencies=len(dependencies), executableSha256=sha256(executable), sourceCredit=0))


if __name__ == '__main__':
    main()
