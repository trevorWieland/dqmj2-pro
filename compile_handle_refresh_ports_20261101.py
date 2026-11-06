import subprocess
from project import ROOT, configuration, native_dependencies, read_json, sha256, write_json
from compile_runtime_subset_20261030 import CLANG_SHA, LINKER_SHA
native_dependencies(configuration())
from elftools.elf.elffile import ELFFile

WORK = ROOT / 'work/handle-refresh-ports-20261101'


def main():
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64'
    clang, linker = tools / 'bin/clang.exe', tools / 'bin/ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    source = ROOT / 'src/runtime/20261101_handle_refresh/native_main_020296b0.c'
    native_report = ROOT / 'evidence/matches/main-handle-refresh96-20261101.json'
    row = read_json(native_report)['matches'][0]
    assert row['sourceSha256'] == sha256(source) and row['bytes'] == 96
    text = source.read_text()
    replacements = [('extern u32 native_fn_02029688(u32);', 'extern u32 native_fn_02029688(void *);'),
        ('u32 native_main_020296b0(u32 arg0)', 'u32 native_main_020296b0(void *arg0)')]
    for before, after in replacements:
        assert text.count(before) == 1
        text = text.replace(before, after)
    WORK.mkdir(parents=True, exist_ok=True)
    port = WORK / source.name
    port.write_text(text)
    for before, after in reversed(replacements):
        text = text.replace(after, before)
    assert text == source.read_text()
    glue = ROOT / 'ports/runtime/handle_refresh_contract_20261101.c'
    flags = ['-O2', '-ffreestanding', '-fno-builtin', '-fno-stack-protector']
    steps = []

    def run(command):
        command = [str(value) for value in command]
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=120)
        steps.append(dict(command=command, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        assert result.returncode == 0, steps[-1]

    objects = []
    for path in [port, glue]:
        obj = WORK / (path.stem + '.obj')
        run([clang, '--target=x86_64-pc-windows-msvc', *flags, '-c', path, '-o', obj])
        objects.append(obj)
    exports = ['native_main_020296b0', 'set_handle_contract']
    windows = WORK / 'j2p_handle_refresh.dll'
    run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib', '/timestamp:0',
        '/out:' + str(windows), *['/export:' + name for name in exports], *objects])
    android = WORK / 'libj2p_handle_refresh_arm64.so'
    run([clang, '--target=aarch64-linux-android33', '--sysroot=' + str(tools / 'sysroot'), *flags,
        '-fPIC', '-shared', '-nostdlib', '-Wl,-z,max-page-size=16384', '-Wl,-z,common-page-size=16384',
        port, glue, '-o', android])
    with android.open('rb') as stream:
        elf = ELFFile(stream)
        assert elf['e_machine'] == 'EM_AARCH64' and elf['e_type'] == 'ET_DYN'
        symbols = {symbol.name for symbol in elf.get_section_by_name('.dynsym').iter_symbols() if symbol['st_shndx'] != 'SHN_UNDEF'}
        assert set(exports) <= symbols
        assert not [tag for tag in elf.get_section_by_name('.dynamic').iter_tags() if tag.entry.d_tag == 'DT_NEEDED']
        assert all(segment['p_align'] >= 16384 for segment in elf.iter_segments() if segment['p_type'] == 'PT_LOAD')
    write_json(ROOT / 'evidence/portability/handle-refresh-build-20261101.json', dict(
        generator='compile_handle_refresh_ports_20261101.py', generatorSha256=sha256(__file__),
        source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
        nativeGoldenReport=native_report.relative_to(ROOT).as_posix(), nativeGoldenReportSha256=sha256(native_report),
        generatedPort=port.relative_to(ROOT).as_posix(), generatedPortSha256=sha256(port),
        onlyApiPointerTypesWidened=True, replacements=replacements,
        glue=glue.relative_to(ROOT).as_posix(), glueSha256=sha256(glue),
        compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA, steps=steps,
        windows=dict(path=windows.relative_to(ROOT).as_posix(), sha256=sha256(windows)),
        android=dict(path=android.relative_to(ROOT).as_posix(), sha256=sha256(android), target='aarch64-linux-android33', minimumLoadAlignment=16384),
        originalSourcesChanged=False, sourceCredit=0, suppliedLowerHelper=True,
        fullWindowsGameCompiled=False, androidDeviceExecutions=0,
        limitations=['Only own recovered C body; lower list helper supplied through explicit callback',
                    'Two API pointer declarations are widened for native64-bit host pointers; stored32-bit words remain unchanged',
                    'Android is compiled/inspected only; no device, graphics, dual-screen or game execution claim']))
    print(dict(windowsBuilt=True, androidBuilt=True, sourceCredit=0, androidExecutions=0))


if __name__ == '__main__':
    main()
