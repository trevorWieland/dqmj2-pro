import ctypes
import os
import shutil
import subprocess
from project import ROOT, read_json, write_json, sha256
from main_async_reader_models_20261031 import recipes, construct, OPEN, SEEK, READ
from compile_memory_primitives_ports_20261030 import CLANG_SHA, LINKER_SHA
from compile_android_checks_20261029 import ENV_NAMES, inspect_elf

SOURCE = 'src/runtime/20261031_async_reader/native_main_0202a954.c'
SOURCE_SHA = '64722c4c9cb3643fd94cf88a0ca10fd311b13d864eac3da68c4d391e75e3a0c4'
INITIALIZER = 'src/runtime/runtime08/native_main_0200bd04.c'
INITIALIZER_SHA = '452b65b15f1799ac0c0924a6f0f706c04771da62e0ab64ddc69c6e6f2d0c4706'
FIXTURE = 'ports/android-native/async_acceptance_fixture.c'
RUNNER = 'ports/android-native/async_acceptance_runner.c'


def numbers(values):
    return '{' + ','.join(str(value) + 'u' for value in values) + '}'


def vectors(path):
    rows = []
    for case in recipes():
        model = construct(case)
        events = []
        for event in model['events']:
            args = event['args'] + [0] * (3 - len(event['args']))
            fields = [dict(zip([OPEN, SEEK, READ], range(3)))[event['address']], len(event['args'])]
            events.append('{' + ','.join([*(str(x) + 'u' for x in fields), numbers(args),
                str(event['result']) + 'u', str(event['errorBefore']) + 'u', str(event['errorAfter']) + 'u',
                numbers(event['fileBefore']), numbers(event['fileAfter'])]) + '}')
        while len(events) < 3:
            events.append('{0}')
        fields = [case['path'], case['buffer'], case['length'], case['offset'], model['oldError'],
            model['result'], model['error'], len(model['events']), int(case['default'])]
        rows.append('{' + ','.join([*(str(x) + 'u' for x in fields), numbers(model['initial']),
            numbers(model['output']), '{' + ','.join(events) + '}']) + '},')
    assert len(rows) == 1440
    path.write_text('#define ASYNC_CASE_COUNT 1440u\nstatic const AsyncCase async_cases[] = {\n' +
        '\n'.join(rows) + '\n};\n', encoding='utf-8', newline='\n')


def main():
    golden_path = ROOT / 'evidence/matches/main-async-reader-20261031.json'
    golden = read_json(golden_path)
    assert sha256(ROOT / SOURCE) == SOURCE_SHA == golden['matches'][0]['sourceSha256']
    assert sha256(ROOT / INITIALIZER) == INITIALIZER_SHA
    assert golden['oracle']['pairs'] == 1440 and golden['oracle']['actualTopReturns'] == 2880
    for pin in golden['generatorSources']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = tools / 'bin/clang.exe', tools / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    work = ROOT / 'work/async-acceptance-ports-20261031'
    work.mkdir(parents=True, exist_ok=True)
    header = work / 'async_acceptance_vectors.h'
    vectors(header)
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    steps = []

    def run(command):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=120)
        steps.append(dict(command=command, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        assert result.returncode == 0, result.stdout + result.stderr

    sources = [SOURCE, INITIALIZER, FIXTURE]
    common = ['-std=c11', '-O2', '-ffreestanding', '-fno-builtin', '-fno-stack-protector',
        '-fno-strict-aliasing', '-Dnative_main_0200bd04=native_fn_0200bd04', '-I' + str(work)]
    objects = []
    for index, source in enumerate(sources):
        obj = work / f'{index}.obj'
        run([clang, '--target=x86_64-pc-windows-msvc', *common, '-c', ROOT / source, '-o', obj])
        objects.append(obj)
    windows = work / 'j2p_async_acceptance.dll'
    exports = ['j2p_async_run_all', 'j2p_async_cases_done', 'j2p_async_provider_calls']
    run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib', '/timestamp:0',
        '/out:' + str(windows), *['/export:' + name for name in exports], *objects])
    library = ctypes.CDLL(str(windows))
    for name in exports:
        getattr(library, name).restype = ctypes.c_uint32
        getattr(library, name).argtypes = []
    assert library.j2p_async_run_all() == 0
    assert library.j2p_async_cases_done() == 1440 and library.j2p_async_provider_calls() == 648
    negative = golden['negativeControls']
    assert sha256(ROOT / negative['source']) == negative['sourceSha256']
    wrong_object = work / 'wrong-read-status.obj'
    run([clang, '--target=x86_64-pc-windows-msvc', *common, '-c', ROOT / negative['source'], '-o', wrong_object])
    wrong_dll = work / 'j2p_async_acceptance_wrong.dll'
    run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib', '/timestamp:0',
        '/out:' + str(wrong_dll), *['/export:' + name for name in exports], wrong_object, *objects[1:]])
    wrong = ctypes.CDLL(str(wrong_dll))
    wrong.j2p_async_run_all.restype = ctypes.c_uint32
    wrong.j2p_async_run_all.argtypes = []
    failed_case = wrong.j2p_async_run_all()
    first_read_failure = next(index + 1 for index, case in enumerate(recipes()) if construct(case)['error'] == 2)
    assert failed_case == first_read_failure
    android = work / 'j2p_async_acceptance_arm64'
    run([clang, '--target=aarch64-linux-android33', '--sysroot=' + str(tools / 'sysroot'), *common,
        '-fPIE', '-pie', '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
        *[ROOT / source for source in sources], ROOT / RUNNER, '-o', android])
    elf = inspect_elf(android)
    assert all(row['alignment'] >= 16384 for row in elf['loads'])
    bundle = ROOT / 'build/android-async-acceptance-bundle-20261031'
    bundle.mkdir(parents=True, exist_ok=True)
    files = [(android, android.name), (header, 'generated/' + header.name)]
    files += [(ROOT / source, 'sources/' + (ROOT / source).name) for source in [*sources, RUNNER]]
    artifacts = []
    for source, relative in files:
        target = bundle / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        artifacts.append(dict(path=relative, sha256=sha256(target), bytes=target.stat().st_size))
    report = dict(windowsNativeCases=1440, windowsActualSourceReturns=1440, windowsProvidedCalls=648,
        windowsWholeCNegativeRejected=True, negativeFirstFailureCase=failed_case,
        negativeSource=negative['source'], negativeSourceSha256=negative['sourceSha256'],
        windowsDllSha256=sha256(windows), androidCompiled=True, androidDeviceExecutions=0,
        dualScreenIntegrationTested=False, fullGameCompiled=False, sourceCredit=0, romOrSaveIncluded=False,
        compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA, steps=steps, elf=elf, artifacts=artifacts,
        nativeGoldenReportSha256=sha256(golden_path), bundle=bundle.relative_to(ROOT).as_posix(),
        sourcePins=[dict(path=path, sha256=sha256(ROOT / path)) for path in [*sources, RUNNER, 'prepare_async_acceptance_ports_20261031.py']],
        limitations=['Logical unit fixture with supplied file services; no actual filesystem or asynchronous completion',
            'The 84-byte byte-backed context uses explicit four-byte alignment and clang no-strict-aliasing semantics',
            'Pointer-to-u32 initializer return is unused; its visible compiler warning is retained',
            'Provider file pointer is checked as context+12; source-level values/memory replace ARM-specific register comparison',
            'No Android device, dual-screen, graphics, input, audio, game ROM or save execution'])
    write_json(bundle / 'manifest.json', report)
    write_json(ROOT / 'evidence/portability/async-acceptance-windows-android-20261031.json', report)
    print(dict(windowsNativeCases=1440, androidCompiled=True, androidDeviceExecutions=0))


if __name__ == '__main__':
    main()
