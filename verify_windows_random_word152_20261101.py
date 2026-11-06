import gzip
import hashlib
import json
import os
import random
import struct
import subprocess
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA, DLLTOOL_SHA
import prepare_random_word152_native_views_20261101 as views

WORK = ROOT / 'work/windows-random-word152-20261101'


def main():
    views.main()
    proof_path = ROOT / 'evidence/matches/main-random-word152-20261101.json'
    proof = read_json(proof_path)
    assert proof['oracle']['pairs'] == 512 and proof['oracle']['providers'] == 0
    trace_path = ROOT / 'evidence/traces/main-random-word152-20261101.json.gz'
    assert any(row['path'] == trace_path.relative_to(ROOT).as_posix() and row['sha256'] == sha256(trace_path)
        for row in proof['replayDependencies'])
    cases = json.loads(gzip.decompress(trace_path.read_bytes()))
    payload = bytearray(struct.pack('<I', len(cases)))
    expected = bytearray()
    rng = random.Random(0x152003D1)
    for pair in cases:
        native = pair['original']
        assert native == pair['candidate'] and native['actualReturn'] and native['modelPassed']
        prefix = bytearray(rng.randbytes(16))
        payload.extend(struct.pack('<II', native['case']['seed'], native['case']['argument']))
        payload.extend(prefix)
        result = native['result']
        final_seed = next(row[2] for row in reversed(native['writes']) if row[0] == 0x020F6044)
        predicate = int(result >> 16 == (((result & 255) * ~(result >> 8 & 255) + 123) & 65535))
        struct.pack_into('<I', prefix, 12, result)
        expected.extend(struct.pack('<III', result, final_seed, predicate))
        expected.extend(prefix)
    directory = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker, dlltool = [directory / name for name in ['clang.exe', 'ld.lld.exe', 'llvm-dlltool.exe']]
    assert [sha256(path) for path in [clang, linker, dlltool]] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    WORK.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    steps = []
    def run(command, data=None):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, input=data, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode, stdoutSha256=hashlib.sha256(result.stdout).hexdigest(),
            stderr=result.stderr.decode(errors='replace')))
        assert result.returncode == 0, steps[-1]
        return result.stdout
    definition = WORK / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\n', encoding='ascii')
    library = WORK / 'kernel32.lib'
    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', library])
    runner = ROOT / 'ports/windows-native/random_word152_runner_20261101.c'
    original_source = ROOT / proof['matches'][0]['source']
    assert sha256(original_source) == proof['matches'][0]['sourceSha256']
    variants = ROOT / 'generated/portability/20261101-random-word152-shared-views'
    source = variants / 'word.c'
    dependencies = [ROOT / 'src/mechanics_save/runtime_rng.c', variants / 'predicate.c']
    sources = [runner, source, *dependencies]
    def build(paths, label):
        objects = []
        for index, path in enumerate(paths):
            obj = WORK / f'{label}-{index}.obj'
            run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-fpack-struct=4',
                '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing',
                '-I', ROOT / 'ports/common', '-c', path, '-o', obj])
            objects.append(obj)
        executable = WORK / (label + '.exe')
        run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib',
            '/entry:j2p_entry', '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0',
            '/manifest:embed', "/manifestuac:level='asInvoker' uiAccess='false'",
            '/alternatename:_native_fn_0203d294=_saved_runtime_random',
            '/alternatename:_native_fn_0203d1f0=_native_main_0203d1f0',
            '/out:' + str(executable), *objects, library])
        binary = executable.read_bytes()
        offset = struct.unpack_from('<I', binary, 0x3C)[0]
        assert binary[offset:offset + 4] == b'PE\0\0' and struct.unpack_from('<H', binary, offset + 4)[0] == 0x14C
        assert struct.unpack_from('<H', binary, offset + 24)[0] == 0x10B and b'asInvoker' in binary
        return executable
    executable = build(sources, 'random-word')
    outputs = [run([executable], payload) for unused in range(2)]
    assert outputs[0] == outputs[1] == bytes(expected)
    wrong_source = variants / 'wrong-word.c'
    wrong_executable = build([runner, wrong_source, *dependencies], 'wrong-encoding')
    wrong_output = run([wrong_executable], payload)
    assert len(wrong_output) == len(expected)
    rejected = sum(wrong_output[index:index + 28] != expected[index:index + 28] for index in range(0, len(expected), 28))
    anticipated = sum(bool(pair['original']['case']['argument']) for pair in cases)
    assert rejected == anticipated and 0 < rejected < len(cases)
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), sourceCredit=0,
        componentFunctions=3, uniqueContexts=len(cases), repeatedProcesses=2, actualWindowsTopReturns=len(cases) * 2,
        actualWrongWindowsTopReturns=len(cases), independentRejections=rejected, unchangedPositives=len(cases) - rejected,
        originalArmEvidence=dict(path=proof_path.relative_to(ROOT).as_posix(), sha256=sha256(proof_path)),
        originalArmTrace=dict(path=trace_path.relative_to(ROOT).as_posix(), sha256=sha256(trace_path)),
        sharedNativeViews=dict(path='evidence/portability/random-word152-shared-views-20261101.json',
            sha256=sha256(ROOT / 'evidence/portability/random-word152-shared-views-20261101.json')),
        inputSources=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in [*sources, wrong_source]],
        tools=dict(clang=CLANG_SHA, linker=LINKER_SHA, dlltool=DLLTOOL_SHA),
        executable=dict(path=executable.relative_to(ROOT).as_posix(), sha256=sha256(executable)),
        expectedOutputSha256=hashlib.sha256(expected).hexdigest(), inputSha256=hashlib.sha256(payload).hexdigest(), steps=steps,
        allPassed=True, fullWindowsGame=False, androidDeviceExecutions=0,
        limitations=['Actual hidden PE32 execution of three C functions using deterministic synthetic word/byte storage',
            'No ROM, save or ARM executable data is supplied to the Windows process',
            'Two disjoint logical global regions use separate C storage; full record extent, unrelated aliases and global RAM layout are not proved',
            'Caller RNG limits256/65535 fit both unsigned caller words and the existing signed positive-limit callee API',
            'Return words, RNG state, encoded-word predicate and complete16-byte backing are compared; CPU flags/stack/ARM registers are not Windows API assertions',
            'No full scene, future observed RNG state, player control, threading, complete native game or Android ABI claim'])
    write_json(ROOT / 'evidence/portability/random-word152-windows32-20261101.json', report)
    print(dict(uniqueContexts=len(cases), actualWindowsTopReturns=len(cases) * 2,
        wrongReturns=len(cases), wrongRejections=rejected, allPassed=True, sourceCredit=0))


if __name__ == '__main__':
    main()
