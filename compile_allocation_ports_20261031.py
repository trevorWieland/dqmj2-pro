import subprocess
from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json
from compile_runtime_subset_20261030 import CLANG_SHA, LINKER_SHA
native_dependencies(configuration())
from elftools.elf.elffile import ELFFile


EXPORTS = ['native_main_0202a37c', 'native_main_0202b334', 'native_data_020dd580',
    'native_data_020edd64', 'native_data_020edd54', 'allocation_contract_result',
    'allocation_contract_calls', 'allocation_contract_address', 'allocation_contract_words']
WORK = ROOT / 'work/allocation-ports-20261031'


def main():
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = tools / 'bin/clang.exe', tools / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    report_path = ROOT / 'evidence/matches/main-allocation-dispatch-20261031.json'
    report = read_json(report_path)
    assert report['romSha256'] == configuration()['romSha256']
    sources = {row['source']: row['sourceSha256'] for row in report['matches']}
    assert len(sources) == 2 and all(sha256(ROOT / path) == digest for path, digest in sources.items())
    glue = ROOT / 'ports/runtime/allocation_contracts_20261031.c'
    sources[glue.relative_to(ROOT).as_posix()] = sha256(glue)
    WORK.mkdir(parents=True, exist_ok=True)
    flags = ['-O2', '-ffreestanding', '-fno-builtin', '-fno-stack-protector',
        '-Dnative_fn_0202b334=native_main_0202b334']
    steps = []

    def run(command):
        command = [str(item) for item in command]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        steps.append(dict(command=command, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        assert result.returncode == 0, steps[-1]

    objects = []
    for source in sources:
        path = ROOT / source
        obj = WORK / (path.stem + '.obj')
        run([clang, '--target=x86_64-pc-windows-msvc', *flags, '-c', path, '-o', obj])
        objects.append(obj)
    windows = WORK / 'j2p_allocation_views.dll'
    run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib', '/timestamp:0',
        '/out:' + str(windows), *['/export:' + name for name in EXPORTS], *objects])
    android = WORK / 'libj2p_allocation_views_arm64.so'
    run([clang, '--target=aarch64-linux-android33', '--sysroot=' + str(tools / 'sysroot'), *flags,
        '-fPIC', '-shared', '-nostdlib', '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
        *[ROOT / source for source in sources], '-o', android])
    with android.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf['e_machine'] == 'EM_AARCH64' and elf['e_type'] == 'ET_DYN'
        actual = {symbol.name for symbol in elf.get_section_by_name('.dynsym').iter_symbols() if symbol['st_shndx'] != 'SHN_UNDEF'}
        assert set(EXPORTS) <= actual
        assert not [tag for tag in elf.get_section_by_name('.dynamic').iter_tags() if tag.entry.d_tag == 'DT_NEEDED']
        assert all(segment['p_align'] >= 16384 for segment in elf.iter_segments() if segment['p_type'] == 'PT_LOAD')
    write_json(ROOT / 'evidence/portability/allocation-build-20261031.json', dict(sources=sources,
        nativeGoldenReport=report_path.relative_to(ROOT).as_posix(), nativeGoldenReportSha256=sha256(report_path),
        compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA, steps=steps, exports=EXPORTS,
        windows=dict(path=windows.relative_to(ROOT).as_posix(), sha256=sha256(windows)),
        android=dict(path=android.relative_to(ROOT).as_posix(), sha256=sha256(android), target='aarch64-linux-android33', minimumLoadAlignment=16384),
        sourceCredit=0, reconstructedSourcesChanged=False, suppliedLowerAllocatorBodies=True,
        fullWindowsGameCompiled=False, androidDeviceExecutions=0, limitations=[
            'Two unchanged reconstructed functions plus explicit test-only lower allocator outcomes and minimal runtime globals',
            'No actual heap, game scene, graphics, dual-screen or device execution proof']))
    print(dict(functions=2, windowsBuilt=True, androidBuilt=True, androidExecutions=0))


if __name__ == '__main__':
    main()
