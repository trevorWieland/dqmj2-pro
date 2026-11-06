import os
import shutil
import subprocess
from project import ROOT, read_json, sha256, write_json
from compile_runtime_subset_20261030 import CLANG_SHA, LINKER_SHA
from compile_float_runtime_ports_20261031 import ALIASES
from compile_android_checks_20261029 import inspect_elf, ENV_NAMES


ADDRESSES = [0x0202263C, 0x02022684, 0x02022740, 0x02023E48, 0x02023E5C, 0x02022664, 0x02023ECC]


def main():
    build = read_json(ROOT / 'evidence/portability/float-runtime-build-20261031.json')
    execution = read_json(ROOT / 'evidence/portability/windows-float-runtime-execution-20261031.json')
    assert execution['allPassed'] and execution['actualWindowsReturns'] == 2912
    assert execution['executableSha256'] == build['windows']['sha256']
    for name, digest in build['sources'].items():
        assert sha256(ROOT / name) == digest
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = tools / 'bin/clang.exe', tools / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    work = ROOT / 'work/float-runtime-ports-20261031/android-runner'
    work.mkdir(parents=True, exist_ok=True)
    lines = ['typedef struct { unsigned kind; unsigned long long x, y, result; int scale, exponent; } FloatVector;',
             '#define FLOAT_VECTOR_COUNT 1120u', 'static const FloatVector float_vectors[] = {']
    scalar_count = 0
    for name in ['main-float-primitives-20261031', 'main-float-rounding-20261031', 'main-float-scale-wrapper-20261031']:
        relative = f'evidence/matches/{name}.json'
        assert sha256(ROOT / relative) == build['reports'][relative]
        for group in read_json(ROOT / relative)['qualifications']:
            entry = int(group['address'], 0)
            if entry not in ADDRESSES:
                continue
            for case in group['cases']:
                row = case['result']
                assert row['modelPassed'] and row['result'] == row['expected']
                values = [str(ADDRESSES.index(entry)), row['input'] + 'ULL', row['second'] + 'ULL',
                          row['result'] + 'ULL', str(row['scale']), str(row['expectedExponent'] or 0)]
                lines.append('    {' + ', '.join(values) + '},')
                scalar_count += 1
    assert scalar_count == 1120
    lines += ['};', 'typedef struct { unsigned aliased, result; unsigned char left[160], right[160]; } ByteVector;',
              '#define BYTE_VECTOR_COUNT 1792u', 'static const ByteVector byte_vectors[] = {']
    relative = 'evidence/matches/main-case-compare-20261031.json'
    assert sha256(ROOT / relative) == build['reports'][relative]
    cases = read_json(ROOT / relative)['cases']
    for case in cases:
        row = case['result']
        assert row['modelPassed'] and row['result'] == row['expected']
        left, right = bytes.fromhex(row['left']), bytes.fromhex(row['right'])
        assert len(left) <= 160 and len(right) <= 160 and bytes([0]) in left and bytes([0]) in right
        fields = [str(int(row['aliased'])), str(row['result']) + 'u',
                  '{' + ','.join(str(value) for value in left) + '}',
                  '{' + ','.join(str(value) for value in right) + '}']
        lines.append('    {' + ', '.join(fields) + '},')
    assert len(cases) == 1792
    lines.append('};')
    header = work / 'float_runtime_vectors.h'
    header.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    runner = ROOT / 'ports/android-native/float_runtime_runner.c'
    output = work / 'j2p_float_runtime_check_arm64'
    command = [str(clang), '--target=aarch64-linux-android33', '--sysroot=' + str(tools / 'sysroot'),
        '-std=c11', '-O2', '-fno-builtin', '-fno-strict-aliasing', '-fno-stack-protector', '-fPIE', '-pie',
        '-I' + str(work), '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
        *['-Dnative_fn_' + address + '=native_main_' + address for address in ALIASES],
        str(runner), *[str(ROOT / source) for source in build['sources']], '-o', str(output)]
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    elf = inspect_elf(output)
    assert all(row['alignment'] >= 16384 for row in elf['loads'])
    bundle = ROOT / 'build/android-float-runtime-bundle-20261031'
    files = [(output, output.name), (runner, 'sources/float_runtime_runner.c'), (header, 'generated/float_runtime_vectors.h')]
    files += [(ROOT / name, 'sources/' + (ROOT / name).name) for name in build['sources']]
    artifacts = []
    for source, relative in files:
        destination = bundle / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        artifacts.append(dict(path=relative, sha256=sha256(destination), bytes=destination.stat().st_size))
    report = dict(androidRunnerCompiled=True, androidDeviceExecutions=0, dualScreenIntegrationTested=False,
        fullGameCompiled=False, sourceCredit=0, romOrSaveIncluded=False, publicFunctions=8, syntheticVectors=2912,
        expectedSuccessStdout='J2P float runtime: 2912 cases passed', compilerSha256=CLANG_SHA,
        linkerSha256=LINKER_SHA, command=command, cwd=str(ROOT), exitCode=result.returncode,
        stdout=result.stdout, stderr=result.stderr, elf=elf, artifacts=artifacts,
        bundle=bundle.relative_to(ROOT).as_posix(),
        limitations=['AndroidAPI33 AArch64 PIE compiled/inspected only; no device execution',
            'Platform libc supplies stdout and buffer comparison/copy; no application or DS service substitutions',
            'Ceiling is excluded until target canonical-NaN arithmetic is adapted',
            'No graphics/input/audio/dual-screen/game/save integration'])
    write_json(bundle / 'manifest.json', report)
    write_json(ROOT / 'evidence/portability/android-float-runtime-runner-20261031.json', report)
    print(dict(androidRunnerCompiled=True, syntheticVectors=2912, androidExecutions=0))


if __name__ == '__main__':
    main()
