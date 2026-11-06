import os
import shutil
import subprocess
from project import ROOT, read_json, sha256, write_json
from compile_memory_primitives_ports_20261030 import SOURCES, CLANG_SHA, LINKER_SHA
from compile_android_checks_20261029 import inspect_elf, ENV_NAMES


def main():
    native_path = ROOT / 'evidence/matches/main-memory-primitives-20261030.json'
    native = read_json(native_path)
    assert len(native['oracle']['rows']) == 2464
    assert all(sha256(ROOT / row['source']) == row['sourceSha256'] for row in native['matches'])
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = tools / 'bin/clang.exe', tools / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    work = ROOT / 'work/memory-primitives-ports-20261030/android-runner'
    work.mkdir(parents=True, exist_ok=True)
    lines = ['typedef struct { unsigned int mode, value, count, alignment, relation; int expected; } MemoryVector;',
             '#define MEMORY_VECTOR_COUNT 2464u', 'static const MemoryVector memory_vectors[] = {']
    for row in native['oracle']['rows']:
        mode, value, count, alignment, relation = row['case']
        result = row['result']['registers'][0]
        if mode == 'search':
            expected = result - 0x02500000 if result else -1
        elif mode == 'compare':
            expected = result if result < 0x80000000 else result - 0x100000000
        else:
            expected = 0
        fields = [str({'search': 0, 'compare': 1, 'fill': 2}[mode]) + 'u', hex(value) + 'u',
                  str(count) + 'u', str(alignment) + 'u', str(relation) + 'u', str(expected)]
        lines.append('    {' + ', '.join(fields) + '},')
    lines.append('};')
    header = work / 'memory_primitive_vectors.h'
    header.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    output = work / 'j2p_memory_check_arm64'
    runner = ROOT / 'ports/android-native/memory_primitives_runner.c'
    arguments = [str(clang), '--target=aarch64-linux-android33', '--sysroot=' + str(tools / 'sysroot'),
                 '-std=c11', '-O2', '-fno-builtin', '-fno-stack-protector', '-fPIE', '-pie', '-I' + str(work),
                 '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
                 str(runner), *[str(ROOT / path) for path in SOURCES], '-o', str(output)]
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    process = subprocess.run(arguments, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=120)
    assert process.returncode == 0, process.stdout + process.stderr
    elf = inspect_elf(output)
    assert all(row['alignment'] >= 16384 for row in elf['loads'])
    bundle = ROOT / 'build/android-memory-primitives-bundle-20261030'
    bundle.mkdir(parents=True, exist_ok=True)
    files = [(output, output.name), (runner, 'sources/memory_primitives_runner.c'),
             (header, 'generated/memory_primitive_vectors.h')]
    files += [(ROOT / path, 'sources/' + (ROOT / path).name) for path in SOURCES]
    artifacts = []
    for path, relative in files:
        destination = bundle / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        artifacts.append({'path': relative, 'sha256': sha256(destination), 'bytes': destination.stat().st_size})
    report = {'androidRunnerCompiled': True, 'androidDeviceExecutions': 0, 'dualScreenIntegrationTested': False,
              'fullGameCompiled': False, 'sourceCredit': 0, 'romOrSaveIncluded': False, 'syntheticVectors': 2464,
              'compilerSha256': CLANG_SHA, 'linkerSha256': LINKER_SHA,
              'nativeGoldenReportSha256': sha256(native_path), 'elf': elf,
              'command': arguments, 'cwd': str(ROOT), 'exitCode': process.returncode,
              'stdout': process.stdout, 'stderr': process.stderr, 'artifacts': artifacts,
              'bundle': bundle.relative_to(ROOT).as_posix(),
              'generatorSources': [{'path': 'prepare_memory_primitives_android_20261030.py',
                                    'sha256': sha256(ROOT / 'prepare_memory_primitives_android_20261030.py')}],
              'limitations': ['Android API33 AArch64 PIE compiled and inspected only; it has not executed',
                              'The runner uses platform libc for allocation, buffer comparison and stdout',
                              'All vectors are synthetic; the leaf C sources are unchanged from the ARM matching packet',
                              'Pointer-to-u32 alignment casts remain visible compiler diagnostics; no source patch or warning suppression is used',
                              'No graphics, input, audio, dual-screen, save loading or whole-game behavior is exercised']}
    write_json(bundle / 'manifest.json', report)
    path = ROOT / 'evidence/portability/android-memory-primitives-runner-20261030.json'
    write_json(path, report)
    print({'androidRunnerCompiled': True, 'syntheticVectors': 2464, 'androidDeviceExecutions': 0, 'reportSha256': sha256(path)})


if __name__ == '__main__':
    main()
