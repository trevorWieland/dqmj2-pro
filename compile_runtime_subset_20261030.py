import subprocess
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
from elftools.elf.elffile import ELFFile

CLANG_SHA = "6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc"
LINKER_SHA = "b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3"
SOURCES = ['src/runtime/20261030_string_reader/native_main_0201d618.c',
           'src/runtime/20261030_strings/native_main_0201d6b8.c',
           'src/runtime/20261030_strings/native_main_0201d800.c']


def main():
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = tools / 'bin/clang.exe', tools / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    work = ROOT / 'work/windows-pure-runtime-20261030'
    work.mkdir(parents=True, exist_ok=True)
    rows, objects = [], []

    def run(command):
        result = subprocess.run([str(item) for item in command], cwd=ROOT, capture_output=True, text=True, timeout=120)
        rows.append({'command': [str(item) for item in command], 'exitCode': result.returncode,
                     'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            raise RuntimeError(result.stdout + result.stderr)

    for source in SOURCES:
        obj = work / ((ROOT / source).stem + '.obj')
        run([clang, '--target=x86_64-pc-windows-msvc', '-O2', '-ffreestanding', '-fno-builtin',
             '-fno-stack-protector', '-c', ROOT / source, '-o', obj])
        rows[-1].update(source=source, sourceSha256=sha256(ROOT / source))
        objects.append(obj)
    windows = work / 'j2p_runtime_subset.dll'
    run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib', '/timestamp:0',
         '/out:' + str(windows), *['/export:' + obj.stem for obj in objects], *objects])
    windows_report = {'compiledWindowsSubset': True, 'compilerSha256': CLANG_SHA, 'linkerSha256': LINKER_SHA,
                      'sources': SOURCES, 'steps': list(rows), 'sourceCredit': 0, 'wholeGameCompiled': False,
                      'output': {'path': windows.relative_to(ROOT).as_posix(), 'sha256': sha256(windows), 'bytes': windows.stat().st_size},
                      'peTimestamp': 0, 'ndkArchiveSha256': 'b830098aaf18b67a42eb831c404e15e5f2990a474f054ac145b0bc957ac6d729'}
    write_json(ROOT / 'evidence/portability/windows-runtime-build-20261030.json', windows_report)
    android = work / 'libj2p_runtime_subset_arm64.so'
    run([clang, '--target=aarch64-linux-android33', '--sysroot=' + str(tools / 'sysroot'), '-O2',
         '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fPIC', '-shared', '-nostdlib',
         '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
         *[ROOT / source for source in SOURCES], '-o', android])
    with android.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf['e_machine'] == 'EM_AARCH64' and elf['e_type'] == 'ET_DYN'
        exported = {symbol.name for symbol in elf.get_section_by_name('.dynsym').iter_symbols() if symbol['st_shndx'] != 'SHN_UNDEF'}
        assert {obj.stem for obj in objects} <= exported
        assert not [tag for tag in elf.get_section_by_name('.dynamic').iter_tags() if tag.entry.d_tag == 'DT_NEEDED']
        loads = [segment for segment in elf.iter_segments() if segment['p_type'] == 'PT_LOAD']
        assert loads and all(segment['p_align'] >= 16384 and segment['p_offset'] % segment['p_align'] == segment['p_vaddr'] % segment['p_align'] for segment in loads)
    write_json(ROOT / 'evidence/portability/android-runtime-subset-compile-20261030.json',
               {'compiled': True, 'target': 'aarch64-linux-android33', 'functionsExported': sorted(exported),
                'elfLoadAlignmentMinimum': 16384, 'neededSharedLibraries': [], 'compilerSha256': CLANG_SHA,
                'linkerSha256': LINKER_SHA, 'output': {'path': android.relative_to(ROOT).as_posix(), 'sha256': sha256(android), 'bytes': android.stat().st_size},
                'steps': rows[-1:], 'sourceCredit': 0, 'androidDeviceExecutions': 0,
                'dualScreenIntegrationTested': False, 'fullGameCompiled': False})
    print({'windowsCompiled': True, 'androidArm64Compiled': True, 'androidDeviceExecutions': 0})


if __name__ == '__main__':
    main()
