import hashlib
import os
import struct
import subprocess
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
import link_arm7_bulk_20261030 as arm7
import arm7_main_bitfields544_native_20261101 as fixture
from check_save_core_explicit_clear_windows32_20261101 import CLANG_SHA, LINKER_SHA, DLLTOOL_SHA

WORK = ROOT / 'work/windows-packed-word544-20261101'
SOURCES = ROOT / 'src/arm7/20261101_bitfields544'


def inputs():
    modules, unused = arm7.namespace('')
    module = modules['arm7-main']
    image = (ROOT / module['binary']).read_bytes()
    assert hashlib.sha256(image).hexdigest() == module['sha256']
    original_uc = fixture.Uc

    class Recorder:
        latest = None

        def __init__(self, *arguments):
            self.inner = original_uc(*arguments)
            self.initial = self.final = None
            Recorder.latest = self

        def __getattr__(self, name):
            return getattr(self.inner, name)

        def mem_read(self, address, size):
            data = self.inner.mem_read(address, size)
            if address == fixture.INPUT and size == 4096:
                if self.initial is None:
                    self.initial = bytes(data)
                self.final = bytes(data)
            return data

    cases = fixture.cases()
    assert len(cases) == 1280
    payload = bytearray(struct.pack('<I', len(cases) * 2))
    expected = bytearray()
    no_store = expected_rejections = 0
    fixture.Uc = Recorder
    try:
        for selector, entry in enumerate(fixture.ENTRIES):
            start = entry - int(module['base'], 0)
            body = image[start:start + 272]
            for index, case in enumerate(cases):
                native = fixture.execute(image, entry, body, case, index)
                assert native['actualOwnReturn'] and native['modelPassed']
                recorded = Recorder.latest
                assert len(recorded.initial) == len(recorded.final) == 4096
                assert hashlib.sha256(recorded.final).hexdigest() == native['inputSha256']
                pointer = native['rawRegisters'][0]
                readonly = int(not native['independentWordModel']['write'])
                no_store += readonly
                expected_rejections += int(selector == 0 and native['wordAfter'] & 0x4000 == 0)
                payload.extend(struct.pack('<3I', selector, pointer - fixture.INPUT, readonly))
                payload.extend(recorded.initial)
                expected.extend(struct.pack('<I', pointer))
                expected.extend(recorded.final)
    finally:
        fixture.Uc = original_uc
        Recorder.latest = None
    assert no_store == 120 and expected_rejections == 1040
    return bytes(payload), bytes(expected), module, no_store, expected_rejections


def main():
    original_path = ROOT / 'evidence/matches/arm7-main-bitfields544-20261101.json'
    original = read_json(original_path)
    assert len(original['matches']) == 2
    for row in original['matches']:
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert row['bytes'] == 272
    directory = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker, dlltool = [directory / name for name in ['clang.exe', 'ld.lld.exe', 'llvm-dlltool.exe']]
    assert [sha256(path) for path in [clang, linker, dlltool]] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    WORK.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items()
        if key not in {'CL', '_CL_', 'CFLAGS', 'CPPFLAGS', 'LDFLAGS', 'LIB', 'LIBPATH', 'INCLUDE'}}
    steps = []

    def run(command, data=None):
        command = list(map(str, command))
        attempt = subprocess.run(command, cwd=ROOT, env=environment, input=data, capture_output=True,
            timeout=120, creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=attempt.returncode,
            stdoutSha256=hashlib.sha256(attempt.stdout).hexdigest(), stderr=attempt.stderr.decode(errors='replace')))
        assert attempt.returncode == 0, steps[-1]
        return attempt.stdout

    definition = WORK / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nReadFile@20\nWriteFile@20\nVirtualAlloc@16\nVirtualProtect@16\n', encoding='ascii')
    library = WORK / 'kernel32.lib'
    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', library])
    runner = ROOT / 'ports/windows-native/packed_word544_runner_20261101.c'
    sources = [SOURCES / f'native_arm7_main_{entry:08x}.c' for entry in fixture.ENTRIES]

    def build(paths, label):
        objects = []
        for index, path in enumerate([runner] + paths):
            obj = WORK / f'{label}-{index}.obj'
            run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-fpack-struct=4',
                '-ffreestanding', '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing',
                '-iquote', SOURCES, '-c', path, '-o', obj])
            objects.append(obj)
        executable = WORK / (label + '.exe')
        run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib',
            '/entry:j2p_entry', '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0',
            '/manifest:embed', "/manifestuac:level='asInvoker' uiAccess='false'",
            '/out:' + str(executable), *objects, library])
        binary = executable.read_bytes()
        position = struct.unpack_from('<I', binary, 0x3C)[0]
        assert binary[position:position + 4] == b'PE\0\0'
        assert struct.unpack_from('<H', binary, position + 4)[0] == 0x14C
        assert struct.unpack_from('<H', binary, position + 24)[0] == 0x10B and b'asInvoker' in binary
        return executable

    executable = build(sources, 'packed-word')
    payload, expected, module, readonly, predicted_rejections = inputs()
    outputs = [run([executable], payload) for unused in range(2)]
    assert outputs[0] == outputs[1] == expected
    text = sources[0].read_text()
    assert text.count('p->flag=0;') == 2
    wrong = WORK / 'wrong-set-flag.c'
    wrong.write_text(text.replace('p->flag=0;', 'p->flag=1;'), encoding='utf-8')
    bad = run([build([wrong, sources[1]], 'wrong-packed-word')], payload)
    assert len(bad) == len(expected)
    width = 4100
    rejected = sum(bad[index * width:(index + 1) * width] != expected[index * width:(index + 1) * width] for index in range(2560))
    assert rejected == predicted_rejections
    files = [runner, ROOT / __file__, ROOT / 'arm7_main_bitfields544_native_20261101.py',
        SOURCES / 'native_fields.h', *sources]
    report = dict(passed=True, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        actualWindowsNativeExecution=True, originalArmCodeInNativeProcess=False,
        uniqueSyntheticContexts=2560, freshNativeProcessRuns=2, nativeCallsPerProcess=2560,
        originalArmActualReturns=2560, providedCalls=0, pageBytesComparedPerContext=4096,
        returnAndFullPageMismatches=0, deterministicOutput=True,
        readOnlyInputPageCallsPerProcess=readonly, bitfieldStorageBytes=4,
        compiledWrongSourceActualReturns=2560, independentWrongRejections=rejected,
        unchangedWrongControlPositives=2560 - rejected, newSourceCoverageCredit=0,
        wholeGame=False, androidLayoutProven=False,
        inputSha256=hashlib.sha256(payload).hexdigest(), outputSha256=hashlib.sha256(expected).hexdigest(),
        originalSourceProof=dict(path=original_path.relative_to(ROOT).as_posix(), sha256=sha256(original_path)),
        module=module, sourceInputs=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in files],
        tools=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in [clang, linker, dlltool]],
        steps=steps, limitations=['Two packed-word functions only; ordinary scene reachability and field names remain unproved',
            'Windows return/full-page effects and no-store protection checked; Windows flags, registers and exact memory order are not compared',
            'Bitfield layout is proven for the measured ARM profile and this pinned Windows profile only; Android remains separate',
            'Aligned synthetic pointers span the mapped page including the last word; malformed pointers and concurrency are unsupported',
            'These are native component tests, not a complete Windows game or source-only ROM'])
    write_json(ROOT / 'evidence/portability/packed-word544-windows32-20261101.json', report)
    print(dict(passed=True, uniqueContexts=2560, nativeRuns=2, readonlyCallsPerRun=readonly,
        wrongRejections=rejected, sourceCredit=0))


if __name__ == '__main__':
    main()
