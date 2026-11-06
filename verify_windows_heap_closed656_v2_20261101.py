import gzip
import hashlib
import json
import os
import struct
import subprocess
from project import ROOT, configuration, read_json, write_json, sha256
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA, DLLTOOL_SHA
from link_runtime_unit import measured_module
from main_heap_initializers_fixture_20261101 import HEADER, EXP, scenario

WORK = ROOT / 'work/heap-closed656-windows32-20261101'


def main():
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker, dlltool = [tools / name for name in ['clang.exe', 'ld.lld.exe', 'llvm-dlltool.exe']]
    assert [sha256(path) for path in [clang, linker, dlltool]] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    WORK.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
                   if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    steps = []

    def run(command, data=None, timeout=120):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, input=data, capture_output=True,
                                timeout=timeout, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode,
            stdoutSha256=hashlib.sha256(result.stdout).hexdigest(), stderr=result.stderr.decode(errors='replace')))
        assert result.returncode == 0, steps[-1]
        return result

    report_path = ROOT / 'evidence/matches/main-heap-initializers276-20261101.json'
    golden_bytes = report_path.read_bytes()
    archive = ROOT / 'evidence/portability/oracles' / ('heap-initializers-' + hashlib.sha256(golden_bytes).hexdigest() + '.json')
    archive.parent.mkdir(parents=True, exist_ok=True)
    if archive.exists():
        assert archive.read_bytes() == golden_bytes
    else:
        archive.write_bytes(golden_bytes)
    golden = read_json(archive)
    assert sha256(ROOT / golden['fixture']) == golden['fixtureSha256']
    trace = golden['oracle']['traceArchive']
    assert sha256(ROOT / trace['path']) == trace['sha256']
    records = json.loads(gzip.decompress((ROOT / trace['path']).read_bytes()))
    originals = {(int(row['entry'], 0), row['index']): row['original'] for row in records}
    unused, image, unused2 = measured_module('main')
    fill = struct.unpack_from('<3I', image, 0x020DD588 - 0x02000000)
    constants = WORK / 'measured-fill-words.c'
    constants.write_text('unsigned int native_data_020dd588[3] = {' + ','.join(hex(word) + 'U' for word in fill) + '};\n', encoding='utf-8')
    definition = WORK / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\n', encoding='ascii')
    library = WORK / 'kernel32.lib'
    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', library])
    sources = [ROOT / 'ports/windows-native/heap_closed656_runner_20261101.c', constants]
    sources.extend(ROOT / f'src/runtime/20261101_heap_initializers/native_main_{entry:08x}.c' for entry in [HEADER, EXP])
    sources.extend(ROOT / f'src/runtime/20261101_heap_support/native_main_{entry:08x}.c' for entry in [0x0202ADFC, 0x0202B9F4, 0x0202BA20])
    sources.extend(ROOT / f'nonmatching/integration/20261101-typed-heap-existing-helpers/native_main_{entry:08x}.c'
                   for entry in [0x0202B9CC, 0x0202B9DC, 0x0202B8EC])
    sources.append(ROOT / 'nonmatching/integration/20261101-typed-heap-existing-helpers/canonical-views/native_main_0202b884.c')
    sources.append(ROOT / 'src/runtime/runtime08/native_main_0202bb88.c')
    objects = []
    for number, source in enumerate(sources):
        obj = WORK / f'source-{number:02}.obj'
        run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding', '-fno-builtin',
             '-fno-stack-protector', '-fno-strict-aliasing', '-Wno-incompatible-pointer-types',
             '-Wno-int-conversion', '-c', source, '-o', obj])
        objects.append(obj)
    aliases = [0x0202B914, 0x0202ADFC, 0x0202B9F4, 0x0202BA20, 0x0202B9CC, 0x0202B9DC, 0x0202B8EC, 0x0202B884]
    executable = WORK / 'heap-closed.exe'
    run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib', '/entry:j2p_entry',
         '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0', '/manifest:embed',
         "/manifestuac:level='asInvoker' uiAccess='false'", '/out:' + str(executable),
         *[f'/alternatename:_native_fn_{entry:08x}=_native_main_{entry:08x}' for entry in aliases], *objects, library])
    binary = executable.read_bytes()
    pe = struct.unpack_from('<I', binary, 0x3C)[0]
    assert binary[pe:pe + 4] == b'PE\0\0' and struct.unpack_from('<H', binary, pe + 4)[0] == 0x14C
    assert struct.unpack_from('<H', binary, pe + 24)[0] == 0x10B and b'asInvoker' in binary
    payload, expected = bytearray(struct.pack('<3I', 0x4A324850, 1, 2400)), []
    for entry in [HEADER, EXP]:
        for index in range(1200):
            pages, wanted, registers, flags, heap, unused_rng = scenario(image, entry, index)
            assert hashlib.sha256(b''.join(wanted)).hexdigest() == originals[entry, index]['pagesSha256']
            payload.extend(struct.pack('<7I', entry, index, *registers[:4], flags))
            payload.extend(b''.join(pages))
            expected.append((entry, index, heap if entry == EXP else 0, b''.join(wanted)))
    output = run([executable], bytes(payload), timeout=180).stdout
    repeated = run([executable], bytes(payload), timeout=180).stdout
    assert output == repeated
    assert output[:12] == payload[:12] and len(output) == 12 + 2400 * (12 + 8192)
    failures = []
    for position, (entry, index, result, wanted) in enumerate(expected):
        offset = 12 + position * (12 + 8192)
        actual_header = struct.unpack_from('<3I', output, offset)
        if actual_header != (entry, index, result) or output[offset + 12:offset + 12 + 8192] != wanted:
            failures.append(dict(entry=hex(entry), index=index, header=list(actual_header)))
    assert not failures, failures[:8]
    report = dict(generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__),
        actualWindowsNativeCalls=2400, repeatedFreshProcessRuns=2, sourceRoutineBodies=10,
        sourceRoutineNativeInitializedBytes=656, suppliedHelperOutcomes=0, armEmulationInNativeProcess=False,
        originalArmCodeOrRomSaveInputsInNativeProcess=False, pointerBytes=4,
        memoryComparisonBytesPerCall=8192, fullPageFailures=failures,
        goldenReport=archive.relative_to(ROOT).as_posix(), goldenReportSha256=sha256(archive),
        currentNativeReportPath=report_path.relative_to(ROOT).as_posix(), goldenSnapshotContentAddressed=True,
        sources=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in sources],
        tools=dict(clangSha256=CLANG_SHA, linkerSha256=LINKER_SHA, dlltoolSha256=DLLTOOL_SHA),
        measuredFillData=dict(address='0x20dd588', bytes=12, sha256=hashlib.sha256(struct.pack('<3I', *fill)).hexdigest(), sourceCredit=0),
        executable=dict(path=executable.relative_to(ROOT).as_posix(), sha256=sha256(executable)), steps=steps,
        sourceCredit=0, fullWindowsGameBuilt=False, androidDeviceExecutions=0,
        limitations=['Actual PE32 C execution on Windows; fixed low32-bit VM preserves the tested word-pointer model',
            'Global storage is bridged to native typed variables; internal root-list addresses are not public results',
            'One explicit typed adapter calls the unchanged integer-pointer next-list routine',
            'The fill primitive is a deterministic platform C loop, not a provided outcome or native ARM blob',
            'Header initializer is void; host raw return registers are not compared as API results',
            'No arbitrary high64-bit pointers, Android device, physical MMIO, graphics or full-game claim'])
    write_json(ROOT / 'evidence/portability/heap-closed656-windows32-v2-20261101.json', report)
    print(dict(windowsNativeCalls=2400, sourceRoutines=10, suppliedOutcomes=0, fullPageFailures=0, sourceCredit=0))


if __name__ == '__main__':
    main()
