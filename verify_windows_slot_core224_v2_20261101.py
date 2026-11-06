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
import main_slot_initializer96_fixture_v2_20261101 as initializer
import main_slot_reference56_fixture_20261101 as caller

WORK = ROOT / 'work/slot-core224-windows32-v2-20261101'


def inputs():
    report_path = ROOT / 'evidence/matches/main-slot-core152-v2-20261101.json'
    report = read_json(report_path)
    for row in report['matches']:
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        for item in row['sourceDependencies']:
            assert sha256(ROOT / item['path']) == item['sha256']
    trace = report['oracle']['traceArchive']
    assert sha256(ROOT / trace['path']) == trace['sha256']
    cases = json.loads(gzip.decompress((ROOT / trace['path']).read_bytes()))
    cases = [case for case in cases if case['cDefinedDomain']]
    assert len(cases) == 961
    metadata, image, unused = measured_module('main')
    payload = bytearray(struct.pack('<I', len(cases)))
    expected = bytearray()
    for case in cases:
        module = initializer if case['kind'] == 'initializer' else caller
        original_type = module.Uc

        class Recorder:
            latest = None

            def __init__(self, *arguments):
                self.inner = original_type(*arguments)
                self.before = {}
                self.after = {}
                self.arguments = {}
                Recorder.latest = self

            def __getattr__(self, name):
                return getattr(self.inner, name)

            def mem_write(self, address, data):
                if address in [module.DATA, module.GLOBAL] and len(data) == 4096:
                    assert address not in self.before
                    self.before[address] = bytes(data)
                return self.inner.mem_write(address, data)

            def mem_read(self, address, length):
                data = self.inner.mem_read(address, length)
                if address in [module.DATA, module.GLOBAL] and length == 4096:
                    self.after[address] = bytes(data)
                return data

            def reg_write(self, register, value):
                if register in module.REGS[:3]:
                    self.arguments[register] = value
                return self.inner.reg_write(register, value)

        module.Uc = Recorder
        try:
            native = image[module.ENTRY - 0x02000000:module.ENTRY - 0x02000000 + module.SIZE]
            observed = module.execute(image, native, case['index'])
            assert observed == case['original']
            captured = Recorder.latest
            before = b''.join(captured.before[address] for address in [module.DATA, module.GLOBAL])
            after = b''.join(captured.after[address] for address in [module.DATA, module.GLOBAL])
            assert len(before) == len(after) == 8192
            assert hashlib.sha256(after).hexdigest() == observed['pagesSha256']
            arguments = [captured.arguments[register] for register in module.REGS[:3]]
            service = [entry[1] for entry in observed['calls'] if entry[0] == 0x020092A4]
            assert len(service) <= 1
            command = service[0] if service else [0, 0]
            payload.extend(struct.pack('<5I', int(module is caller), case['index'], *arguments))
            payload.extend(before)
            expected.extend(struct.pack('<4I', observed['result'], len(service), *command))
            expected.extend(after)
        finally:
            module.Uc = original_type
            Recorder.latest = None
    frozen = ROOT / f'evidence/portability/oracles/slot-core152-{sha256(report_path)}.json'
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
    runner = ROOT / 'ports/windows-native/slot_core224_runner_v2_20261101.c'
    folder = ROOT / 'src/runtime/20261101_slot_core152'
    primary96, primary56 = [folder / f'native_main_{address:08x}.c' for address in [0x0203B5D8, 0x0203A650]]

    def build(selected96, label):
        objects = []
        for number, source in enumerate([runner, selected96, primary56]):
            obj = WORK / f'{label}-{number}.obj'
            run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding', '-fno-builtin',
                '-fno-stack-protector', '-fno-strict-aliasing', '-Wno-deprecated-non-prototype', '-c', source, '-o', obj])
            objects.append(obj)
        executable = WORK / (label + '.exe')
        run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib', '/entry:j2p_entry',
            '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0', '/manifest:embed',
            "/manifestuac:level='asInvoker' uiAccess='false'", '/out:' + str(executable),
            '/alternatename:_native_fn_0203b5d8=_native_main_0203b5d8', *objects, library])
        binary = executable.read_bytes()
        pe = struct.unpack_from('<I', binary, 0x3C)[0]
        assert binary[pe:pe + 4] == b'PE\0\0' and struct.unpack_from('<H', binary, pe + 4)[0] == 0x14C
        assert struct.unpack_from('<H', binary, pe + 24)[0] == 0x10B and b'asInvoker' in binary
        return executable

    executable = build(primary96, 'slot-core')
    payload, expected, oracle, metadata = inputs()
    outputs = [run([executable], payload) for unused in range(2)]
    width = 16 + 8192
    assert all(len(output) == len(expected) for output in outputs)
    mismatches = [index for index in range(961) if outputs[0][index * width:(index + 1) * width] != expected[index * width:(index + 1) * width]]
    assert not mismatches, mismatches[:16]
    assert outputs[0] == outputs[1] == expected
    negative = ROOT / 'nonmatching/integration/20261101-slot-core152-controls/0/source.c'
    bad = run([build(negative, 'negative-count')], payload)
    assert len(bad) == len(expected)
    rejected = sum(bad[index * width:(index + 1) * width] != expected[index * width:(index + 1) * width] for index in range(961))
    assert rejected > 0
    files = [runner, primary96, primary56, folder / 'state.h', ROOT / 'src/runtime/runtime03/native_main_020388dc.c',
        ROOT / __file__, ROOT / 'main_slot_initializer96_fixture_v2_20261101.py', ROOT / 'main_slot_reference56_fixture_20261101.py']
    report = dict(passed=True, generator=Path(__file__).name, generatorSha256=sha256(__file__),
        actualWindowsNativeExecution=True, originalArmCodeInNativeProcess=False,
        uniqueSyntheticContexts=961, excludedBinaryOnlyContexts=63, freshProcessRuns=2, deterministicOutput=True,
        reconstructedInitializedRoutineBytes=224, reconstructedInstructionBytes=220, newSourceCoverageCredit=0,
        dataAndGlobalBytesComparedPerContext=8192, mismatchContexts=0,
        compiledWrongProcessReturns=961, independentWrongRejections=rejected, unchangedWrongControlPositives=961 - rejected,
        originalNativeOracle=oracle, moduleSha256=metadata['sha256'],
        inputSha256=hashlib.sha256(payload).hexdigest(), outputSha256=hashlib.sha256(expected).hexdigest(),
        sourceInputs=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in files],
        tools=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)) for path in [clang, linker, dlltool]], steps=steps,
        limitations=['Only the C-defined slot range0..31;63 positive-count wide-slot cases are excluded',
            'The original command queue is a typed two-word host provider; reservation helper72 and new96/caller56 C execute natively',
            'Logical global prefix020F4C38 is bridged through12 aligned host bytes; signed/unsigned word ABI adapter is explicit',
            'No ARM scratch/flags/store-order equivalence, physical command transmission, concurrency or full native game claim'])
    output = ROOT / 'evidence/portability/slot-core224-windows32-v2-20261101.json'
    write_json(output, report)
    print(dict(passed=True, uniqueContexts=961, freshProcessRuns=2, initializedRoutineBytes=224,
        mismatchContexts=0, wrongRejections=rejected, excludedBinaryOnlyContexts=63, sourceCredit=0))


if __name__ == '__main__':
    main()
