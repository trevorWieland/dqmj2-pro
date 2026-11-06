import subprocess
from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json
from compile_runtime_subset_20261030 import CLANG_SHA, LINKER_SHA
native_dependencies(configuration())
from elftools.elf.elffile import ELFFile


REPORTS = ['main-float-primitives-20261031', 'main-float-rounding-20261031',
           'main-float-scale-wrapper-20261031', 'main-case-compare-20261031', 'main-ascii-lower-data-20261031']
EXCLUDED = {'native_main_02022480'}
ALIASES = ['0202263c', '02022684', '02022740', '02023e48', '02023e5c']
WORK = ROOT / 'work/float-runtime-ports-20261031'


def main():
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = tools / 'bin/clang.exe', tools / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    WORK.mkdir(parents=True, exist_ok=True)
    sources, exports, reports = {}, [], {}
    for name in REPORTS:
        relative = 'evidence/matches/' + name + '.json'
        report = read_json(ROOT / relative)
        assert report['romSha256'] == configuration()['romSha256']
        reports[relative] = sha256(ROOT / relative)
        for row in [*report.get('matches', []), *report.get('dataMatches', [])]:
            if row['name'] in EXCLUDED:
                continue
            assert sha256(ROOT / row['source']) == row['sourceSha256']
            sources[row['source']] = row['sourceSha256']
            if row.get('mode') != 'data':
                exports.append(row['name'])
    assert len(exports) == 8 and len(sources) == 9
    glue = WORK / 'float_runtime_glue.c'
    glue.write_text('int _fltused = 0;\n', encoding='utf-8')
    shared = ['-O2', '-ffreestanding', '-fno-builtin', '-fno-strict-aliasing', '-fno-stack-protector',
        *['-Dnative_fn_' + address + '=native_main_' + address for address in ALIASES]]
    steps = []

    def run(command):
        command = [str(item) for item in command]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        steps.append(dict(command=command, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        assert result.returncode == 0, steps[-1]

    objects = []
    for source in [*[ROOT / name for name in sources], glue]:
        obj = WORK / (source.stem + '.obj')
        run([clang, '--target=x86_64-pc-windows-msvc', *shared, '-c', source, '-o', obj])
        objects.append(obj)
    windows = WORK / 'j2p_float_runtime.dll'
    run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib', '/timestamp:0',
         '/out:' + str(windows), *['/export:' + name for name in exports], *objects])
    android = WORK / 'libj2p_float_runtime_arm64.so'
    run([clang, '--target=aarch64-linux-android33', '--sysroot=' + str(tools / 'sysroot'),
         *shared, '-fPIC', '-shared', '-nostdlib', '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
         *[ROOT / name for name in sources], '-o', android])
    with android.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf['e_machine'] == 'EM_AARCH64' and elf['e_type'] == 'ET_DYN'
        actual = {symbol.name for symbol in elf.get_section_by_name('.dynsym').iter_symbols() if symbol['st_shndx'] != 'SHN_UNDEF'}
        assert set(exports) <= actual
        assert not [tag for tag in elf.get_section_by_name('.dynamic').iter_tags() if tag.entry.d_tag == 'DT_NEEDED']
        loads = [segment for segment in elf.iter_segments() if segment['p_type'] == 'PT_LOAD']
        assert loads and all(segment['p_align'] >= 16384 for segment in loads)
    report = dict(sources=sources, exports=sorted(exports), reports=reports,
        compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA, steps=steps,
        windows=dict(path=windows.relative_to(ROOT).as_posix(), sha256=sha256(windows), bytes=windows.stat().st_size),
        android=dict(path=android.relative_to(ROOT).as_posix(), sha256=sha256(android), bytes=android.stat().st_size,
            target='aarch64-linux-android33', minimumLoadAlignment=16384, neededSharedLibraries=[]),
        strictAliasingDisabledForMeasuredWordViews=True, reconstructedSourcesChanged=False,
        excludedCeiling=dict(reason='Original ARM arithmetic canonicalizes NaNs; host operator replacement semantics remain separate'),
        sourceCredit=0, androidDeviceExecutions=0, dualScreenExecutionTested=False, fullGameCompiled=False)
    write_json(ROOT / 'evidence/portability/float-runtime-build-20261031.json', report)
    print(dict(windowsCompiled=True, androidArm64Compiled=True, functions=8, androidExecutions=0))


if __name__ == '__main__':
    main()
