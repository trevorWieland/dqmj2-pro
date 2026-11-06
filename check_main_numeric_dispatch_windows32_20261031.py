import hashlib
import os
import struct
import subprocess
from project import ROOT, read_json, write_json, sha256
from compile_memory_primitives_ports_20261030 import CLANG_SHA, LINKER_SHA
from compile_android_checks_20261029 import ENV_NAMES
from check_main_word_pattern_windows32_20261031 import DLLTOOL_SHA
from main_numeric_dispatch_fixture_20261031 import initial, DIVIDE, RESERVE, APPEND, EMPTY, DISABLE, RESTORE

SOURCE = 'src/runtime/20261031_numeric_dispatch/native_main_0203b660.c'
RUNNER = 'ports/windows-native/numeric_dispatch_runner.c'
GOLDEN = 'evidence/matches/main-numeric-dispatch-20261031.json'
OUTPUT = 'evidence/portability/main-numeric-dispatch-windows32-20261031.json'


def mix(value, data):
    for byte in data:
        value = (value ^ byte) * 16777619 & 0xFFFFFFFF
    return value


def corpus(golden):
    raw = bytearray(struct.pack('<II', 0x4A324E56, len(golden['results'])))
    digest = 2166136261
    helpers = services = 0
    for case in golden['results']:
        item, result = case['recipe'], case['result']
        model = initial(item)
        assert result['modelPassed'] and result['actualReturns'] == 1
        assert hashlib.sha256(model['expectedData']).hexdigest() == result['dataSha256']
        assert hashlib.sha256(model['expectedGlobal']).hexdigest() == result['globalSha256']
        raw.extend(struct.pack('<8I', *model['args']))
        raw.extend(struct.pack('<II', (item['index'] >> 2 & 1) * 128, result['result']))
        counts = [model['expectedHelpers'][address] for address in [DIVIDE, RESERVE, APPEND, EMPTY, DISABLE, RESTORE]]
        raw.extend(struct.pack('<6I', *counts))
        events = model['expectedServices']
        raw.extend(struct.pack('<I', len(events)))
        kinds = {0x0203B854: 0, 0x0200932C: 1, 0x02009264: 2, 0x0203B9C0: 3}
        for event in events:
            values = [kinds[event['target']], len(event['arguments']), event.get('transientWord2C', 0xFFFFFFFF),
                      *event['arguments'], *([0] * (10 - len(event['arguments'])))]
            raw.extend(struct.pack('<13I', *values))
        raw.extend(model['beforeData'])
        raw.extend(model['beforeGlobal'])
        raw.extend(model['expectedData'])
        raw.extend(model['expectedGlobal'])
        digest = mix(digest, model['expectedData'] + model['expectedGlobal'] + struct.pack('<I', result['result']))
        helpers += sum(counts)
        services += len(events)
    return bytes(raw), digest, helpers, services


def absolute_bindings(path):
    entries = [('_native_data_020f5b00', 0x020F5B00, 0),
               ('_native_data_020f5b4c', 0x020F5B4C, 0),
               ('_native_fn_0203b9b0', 0x0203B9B0, 0x20)]
    strings, symbols = bytearray(), bytearray()
    for name, value, kind in entries:
        symbols.extend(bytes(4) + struct.pack('<I', 4 + len(strings)))
        symbols.extend(struct.pack('<IhHBB', value, -1, kind, 2, 0))
        strings.extend(name.encode() + bytes(1))
    data = struct.pack('<HHIIIHH', 0x14C, 0, 0, 20, len(entries), 0, 0)
    data += symbols + struct.pack('<I', 4 + len(strings)) + strings
    assert len(symbols) == len(entries) * 18
    assert struct.unpack_from('<HH', data) == (0x14C, 0)
    for index, unused in enumerate(entries):
        assert struct.unpack_from('<h', data, 20 + index * 18 + 12)[0] == -1
    path.write_bytes(data)
    return dict(symbols=[dict(name=name, address=hex(value), type=kind) for name, value, kind in entries],
                sections=0, executableCodeBytes=0, initializedDataBytes=0,
                ordinaryFunctionCredit=0, sha256=sha256(path))


def main():
    golden = read_json(ROOT / GOLDEN)
    assert sha256(ROOT / SOURCE) == golden['matches'][0]['sourceSha256']
    assert sha256(ROOT / golden['fixture']['path']) == golden['fixture']['sha256']
    assert golden['matches'][0]['nativeOracle']['actualReturns'] == 1280
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker, dlltool = tools / 'clang.exe', tools / 'ld.lld.exe', tools / 'llvm-dlltool.exe'
    assert [sha256(path) for path in [clang, linker, dlltool]] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    work = ROOT / 'work/main-numeric-dispatch-20261031/windows32'
    work.mkdir(parents=True, exist_ok=True)
    payload, digest, helper_count, service_count = corpus(golden)
    (work / 'vectors.bin').write_bytes(payload)
    bindings = absolute_bindings(work / 'absolute-bindings.obj')
    definition = work / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nWriteFile@20\nReadFile@20\nVirtualAlloc@16\n', encoding='utf-8')
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    steps = []

    def run(command, data=None, expected=0):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, input=data, timeout=120,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode, stdoutBytes=len(result.stdout),
                          stdoutSha256=hashlib.sha256(result.stdout).hexdigest(), stderr=result.stderr.decode(errors='replace')))
        if result.returncode != expected:
            raise ValueError(steps[-1])
        return result

    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', work / 'kernel32.lib'])

    def compile_source(source, output):
        run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding',
             '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing', '-c', source, '-o', output])

    compile_source(ROOT / RUNNER, work / 'runner.obj')

    def build(source, label):
        obj, exe = work / (label + '.obj'), work / (label + '.exe')
        compile_source(source, obj)
        run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib',
             '/entry:j2p_entry', '/safeseh:no', '/fixed', '/dynamicbase:no', '/timestamp:0',
             '/manifest:embed', "/manifestuac:level='asInvoker' uiAccess='false'", '/out:' + str(exe),
             obj, work / 'runner.obj', work / 'absolute-bindings.obj', work / 'kernel32.lib'])
        data = exe.read_bytes()
        offset = struct.unpack_from('<I', data, 0x3C)[0]
        assert data[offset:offset + 4] == b'PE\0\0'
        assert struct.unpack_from('<H', data, offset + 4)[0] == 0x14C
        assert struct.unpack_from('<H', data, offset + 24)[0] == 0x10B
        assert b'asInvoker' in data and b'requestedExecutionLevel' in data
        return exe

    native = build(ROOT / SOURCE, 'numeric-core')
    result = run([native], payload)
    assert len(result.stdout) == 32
    receipt = struct.unpack('<8I', result.stdout)
    assert receipt == (0x4A324E44, 4, 640, 640, helper_count, service_count, 0, digest), receipt
    negative = ROOT / golden['wrongC']['source']
    assert sha256(negative) == golden['wrongC']['sourceSha256']
    wrong = build(negative, 'wrong-transient-word')
    rejected = run([wrong], payload, expected=42)
    assert len(rejected.stdout) == 32
    negative_receipt = struct.unpack('<8I', rejected.stdout)
    assert negative_receipt[:3] == receipt[:3] and negative_receipt[3] >= 1 and negative_receipt[6] >= 1
    write_json(ROOT / OUTPUT, dict(source=SOURCE, sourceSha256=sha256(ROOT / SOURCE),
        runner=RUNNER, runnerSha256=sha256(ROOT / RUNNER), generator=__file__, generatorSha256=sha256(__file__),
        golden=GOLDEN, goldenSha256=sha256(ROOT / GOLDEN), vectorsSha256=sha256(work / 'vectors.bin'),
        pointerBytes=4, actualWindowsReturns=receipt[3], suppliedCHelperCalls=receipt[4], suppliedLowerCalls=receipt[5],
        receipt=list(receipt), negativeReceipt=list(negative_receipt), negativeActualWindowsReturns=negative_receipt[3],
        executable=dict(path=native.relative_to(ROOT).as_posix(), sha256=sha256(native)),
        wrongExecutable=dict(path=wrong.relative_to(ROOT).as_posix(), sha256=sha256(wrong)),
        bindings=bindings, steps=steps, tools=dict(clang=CLANG_SHA, linker=LINKER_SHA, dlltool=DLLTOOL_SHA),
        implementationContract='Native Win32 process; fixed private read/write data arenas; no original executable code mapped; supplied C helper models',
        limitations=['Zero new helper/callback/data source credit; absolute COFF object contains symbols only',
                     'No original ROM/save/assets enter the Windows process; the stdin corpus is synthetic',
                     'No actual IRQ, audio, hardware, complete Windows game or Android device execution']))
    print(dict(actualWindowsReturns=receipt[3], suppliedCHelperCalls=receipt[4], suppliedLowerCalls=receipt[5],
               negativeActualWindowsReturns=negative_receipt[3], pointerBytes=4))


if __name__ == '__main__':
    main()
