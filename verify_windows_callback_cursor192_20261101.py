import gzip
import hashlib
import json
import os
import struct
import subprocess
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import measured_module
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA, DLLTOOL_SHA
import main_callback_cursor192_fixture_20261101 as fixture

WORK = ROOT / 'work/callback-cursor192-windows32-20261101'


def inputs():
    report_path = ROOT / 'evidence/matches/main-callback-cursor192-20261101.json'
    report = read_json(report_path)
    assert report['oracle']['pairs'] == 512
    trace = report['oracle']['traceArchive']
    assert sha256(ROOT / trace['path']) == trace['sha256']
    cases = json.loads(gzip.decompress((ROOT / trace['path']).read_bytes()))
    metadata, image, unused = measured_module('main')
    original_type = fixture.Uc

    class Recorder:
        latest = None

        def __init__(self, *arguments):
            self.inner = original_type(*arguments)
            self.initial = None
            self.final = None
            Recorder.latest = self

        def __getattr__(self, name):
            return getattr(self.inner, name)

        def mem_write(self, address, data):
            if address == fixture.DATA and len(data) == 4096:
                assert self.initial is None
                self.initial = bytes(data)
            return self.inner.mem_write(address, data)

        def mem_read(self, address, length):
            data = self.inner.mem_read(address, length)
            if address == fixture.DATA and length == 4096:
                self.final = bytes(data)
            return data

    payload = bytearray(struct.pack('<I', len(cases)))
    expected = bytearray()
    body = image[fixture.ENTRY - 0x02000000:fixture.ENTRY - 0x02000000 + fixture.SIZE]
    fixture.Uc = Recorder
    try:
        for case in cases:
            index = case['index']
            observed = fixture.execute(image, body, index)
            assert observed == case['original']
            captured = Recorder.latest
            before, after = captured.initial, captured.final
            assert len(before) == len(after) == 4096
            assert hashlib.sha256(after).hexdigest() == observed['pageSha256']
            events = observed['events']
            callback = next(event[1] for event in events if event[0] == 'callback')
            state, value, offset, length = callback
            callback_flags = next(event[3] for event in events if event[0] == 'service-store' and event[1] == state + 0x1C)
            waits = sum(event[0] == 'sleep' for event in events)
            irq_calls = int(any(event[0] == 'disable' for event in events))
            status = 6 if irq_calls else observed['result']
            changes = [event[3] for event in events if event[0] == 'service-store' and event[1] == fixture.DATA + 0x104]
            replacement = changes[0] if index % 3 == 0 else (changes[0] - 0x10001) & 0xFFFFFFFF if waits else 0
            final_status = struct.unpack_from('<I', before, 0x714)[0]
            irq = observed['cpsr'] & 0x80
            payload.extend(struct.pack('<10I', index, fixture.DATA + 0x100, value, length, irq,
                status, waits, callback_flags, replacement, final_status))
            payload.extend(before)
            expected.extend(struct.pack('<7I', observed['result'], irq, 1, waits, irq_calls, irq_calls, 0))
            expected.extend(after)
    finally:
        fixture.Uc = original_type
        Recorder.latest = None
    frozen = ROOT / f'evidence/portability/oracles/callback-cursor192-{sha256(report_path)}.json'
    frozen.parent.mkdir(parents=True, exist_ok=True)
    if frozen.exists():
        assert frozen.read_bytes() == report_path.read_bytes()
    else:
        frozen.write_bytes(report_path.read_bytes())
    return bytes(payload), bytes(expected), dict(path=frozen.relative_to(ROOT).as_posix(), sha256=sha256(frozen)), metadata


def main():
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
        steps.append(dict(command=command, exitCode=result.returncode,
            stdoutSha256=hashlib.sha256(result.stdout).hexdigest(), stderr=result.stderr.decode(errors='replace')))
        assert result.returncode == 0, steps[-1]
        return result.stdout

    definition = WORK / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\n', encoding='ascii')
    library = WORK / 'kernel32.lib'
    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', library])
    runner = ROOT / 'ports/windows-native/callback_cursor192_runner_20261101.c'
    primary = ROOT / 'src/runtime/20261101_callback_cursor192/native_main_0200a81c.c'

    def build(source, label):
        obj, executable = WORK / (label + '.obj'), WORK / (label + '.exe')
        run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding', '-fno-builtin',
            '-fno-stack-protector', '-fno-strict-aliasing', '-c', source, '-o', obj])
        run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib', '/entry:j2p_entry',
            '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0', '/manifest:embed',
            "/manifestuac:level='asInvoker' uiAccess='false'", '/out:' + str(executable), obj, library])
        binary = executable.read_bytes()
        pe = struct.unpack_from('<I', binary, 0x3C)[0]
        assert binary[pe:pe + 4] == b'PE\0\0' and struct.unpack_from('<H', binary, pe + 4)[0] == 0x14C
        assert struct.unpack_from('<H', binary, pe + 24)[0] == 0x10B and b'asInvoker' in binary
        return executable

    executable = build(runner, 'callback-cursor')
    payload, expected, oracle, metadata = inputs()
    outputs = [run([executable], payload) for unused in range(2)]
    assert all(len(output) == len(expected) for output in outputs)
    width = 28 + 4096
    mismatches = [index for index in range(512) if outputs[0][index * width:(index + 1) * width] != expected[index * width:(index + 1) * width]]
    assert not mismatches, mismatches[:16]
    assert outputs[0] == outputs[1] == expected
    negative_primary = ROOT / 'nonmatching/integration/20261101-callback-cursor-controls/0/source.c'
    negative_runner = WORK / 'negative-runner.c'
    text = runner.read_text(encoding='utf-8')
    before = '#include "../../src/runtime/20261101_callback_cursor192/native_main_0200a81c.c"'
    assert text.count(before) == 1
    negative_runner.write_text(text.replace(before, '#include "' + negative_primary.as_posix() + '"'), encoding='utf-8')
    negative_executable = build(negative_runner, 'negative-double-offset')
    bad = run([negative_executable], payload)
    assert len(bad) == len(expected)
    rejected = sum(bad[index * width:(index + 1) * width] != expected[index * width:(index + 1) * width] for index in range(512))
    assert rejected > 0
    files = [runner, primary, ROOT / __file__, ROOT / 'main_callback_cursor192_fixture_20261101.py']
    report = dict(passed=True, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        actualWindowsNativeExecution=True, originalArmCodeInNativeProcess=False,
        uniqueSyntheticContexts=512, freshProcessRuns=2, deterministicOutput=True,
        reconstructedBodyBytes=192, newSourceCoverageCredit=0, pageBytesComparedPerContext=4096,
        mismatchContexts=0, compiledWrongProcessReturns=512, independentWrongRejections=rejected,
        unchangedWrongControlPositives=512 - rejected, originalNativeOracle=oracle,
        moduleSha256=metadata['sha256'], inputSha256=hashlib.sha256(payload).hexdigest(),
        outputSha256=hashlib.sha256(expected).hexdigest(),
        tools=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in [clang, linker, dlltool]],
        sourceInputs=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in files], steps=steps,
        limitations=['Single-thread callback/sleep and IRQ models; original scheduler or callbacks are not reconstructed',
            'Logical026A0000 callback ID is mapped to a typed native function and restored before byte comparison',
            'Finite0..3 waits only; no permanent wait, malformed pointer, ARM scratch-register/flag or store-order equivalence claim',
            'This is an actual native component test, not a full Windows game or source-only ROM'])
    output = ROOT / 'evidence/portability/callback-cursor192-windows32-20261101.json'
    write_json(output, report)
    print(dict(passed=True, uniqueContexts=512, freshProcessRuns=2, reconstructedBytes=192,
        mismatchContexts=0, wrongRejections=rejected, sourceCredit=0))


if __name__ == '__main__':
    main()
