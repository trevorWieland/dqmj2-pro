import hashlib
import os
import random
import struct
import subprocess
from project import ROOT, read_json, write_json, sha256
from compile_memory_primitives_ports_20261030 import CLANG_SHA, LINKER_SHA
from compile_android_checks_20261029 import ENV_NAMES

SOURCE = 'src/runtime/20261031_word_pattern/native_main_0203c5b8.c'
RUNNER = 'ports/windows-native/word_pattern_runner.c'
GOLDEN = 'evidence/matches/main-word-pattern-20261031.json'
DLLTOOL_SHA = 'd2f0d02b4ae109d2801f83506c329c1ca0e36d52919b273eaffb915c8cd095d1'


def bytes_c(data):
    return '{' + ','.join(str(value) for value in data) + '}'


def vectors(golden, target):
    rows = []
    for case in golden['results']:
        item = case['recipe']
        rng = random.Random(0xC5B80000 + item['index'])
        rng.randbytes(3)
        rng.randbytes(12)
        before, flags = rng.randbytes(512), rng.randbytes(16)
        after = bytearray(before)
        if item['count'] > 0:
            for index in range(item['count']):
                value = 1 if item['mode'] == 0 else 2
                if index == (item['count'] - 1 if item['mode'] == 0 else 0):
                    value = 0
                struct.pack_into('<I', after, index * 4, value)
        assert hashlib.sha256(after).hexdigest() == case['result']['bufferSha256']
        flag_after = bytes.fromhex(case['result']['flag'])
        values = [str(item['count']), str(item['mode']), str(int(item['default'])), str(case['result']['result'])]
        values.extend(bytes_c(data) for data in [before, after, flags, flag_after])
        rows.append('{' + ','.join(values) + '},')
    target.write_text('#define PATTERN_CASE_COUNT ' + str(len(rows)) + 'u\n' +
                      'static const PatternCase pattern_cases[] = {\n' + '\n'.join(rows) + '\n};\n',
                      encoding='utf-8', newline='\n')


def main():
    golden = read_json(ROOT / GOLDEN)
    assert sha256(ROOT / SOURCE) == golden['matches'][0]['sourceSha256']
    assert golden['matches'][0]['nativeOracle']['actualReturns'] == 1204
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker, dlltool = tools / 'clang.exe', tools / 'ld.lld.exe', tools / 'llvm-dlltool.exe'
    assert [sha256(path) for path in [clang, linker, dlltool]] == [CLANG_SHA, LINKER_SHA, DLLTOOL_SHA]
    work = ROOT / 'work/main-word-pattern-20261031/windows32'
    work.mkdir(parents=True, exist_ok=True)
    vectors(golden, work / 'word_pattern_vectors.h')
    definition = work / 'kernel32.def'
    definition.write_text('LIBRARY KERNEL32.dll\nEXPORTS\nExitProcess@4\nGetStdHandle@4\nWriteFile@20\n', encoding='utf-8')
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    steps = []

    def run(command, expected=0):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, timeout=120,
                                creationflags=subprocess.CREATE_NO_WINDOW)
        steps.append(dict(command=command, exitCode=result.returncode,
                          stdout=result.stdout.decode(errors='replace'), stderr=result.stderr.decode(errors='replace')))
        if result.returncode != expected:
            raise ValueError(steps[-1])
        return result

    run([dlltool, '-m', 'i386', '-k', '-d', definition, '-l', work / 'kernel32.lib'])

    def compile_source(source, output):
        run([clang, '--target=i686-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding',
             '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing', '-I' + str(work),
             '-c', source, '-o', output])

    compile_source(ROOT / RUNNER, work / 'runner.obj')

    def build(source, label):
        obj, exe = work / (label + '.obj'), work / (label + '.exe')
        compile_source(source, obj)
        run([linker, '-flavor', 'link', '/machine:x86', '/subsystem:console', '/nodefaultlib',
             '/entry:j2p_entry', '/safeseh:no', '/timestamp:0', '/out:' + str(exe),
             obj, work / 'runner.obj', work / 'kernel32.lib'])
        data = exe.read_bytes()
        offset = struct.unpack_from('<I', data, 0x3C)[0]
        assert data[offset:offset + 4] == b'PE\0\0'
        assert struct.unpack_from('<H', data, offset + 4)[0] == 0x14C
        assert struct.unpack_from('<H', data, offset + 24)[0] == 0x10B
        return exe

    native = build(ROOT / SOURCE, 'word-pattern')
    result = run([native])
    assert len(result.stdout) == 32
    receipt = struct.unpack('<8I', result.stdout)
    assert receipt[:4] == (0x4A325057, 4, 602, 602) and receipt[4:6] == (584, 0)
    assert receipt[7] == 0x16403210
    negative = ROOT / golden['negativeCompiled']['source']
    assert sha256(negative) == golden['negativeCompiled']['sourceSha256']
    wrong = build(negative, 'wrong-stride')
    wrong_result = run([wrong], expected=41)
    assert len(wrong_result.stdout) == 32
    wrong_receipt = struct.unpack('<8I', wrong_result.stdout)
    assert wrong_receipt[:3] == receipt[:3] and wrong_receipt[3] > 0 and wrong_receipt[5] > 0
    assert wrong_receipt[7] == receipt[7]
    write_json(ROOT / 'evidence/portability/main-word-pattern-windows32-20261031.json', dict(
        source=SOURCE, sourceSha256=sha256(ROOT / SOURCE), runner=RUNNER, runnerSha256=sha256(ROOT / RUNNER),
        golden=GOLDEN, goldenSha256=sha256(ROOT / GOLDEN), pointerBytes=4,
        actualWindowsReturns=receipt[3], suppliedFillCalls=receipt[4], receipt=list(receipt),
        negativeReceipt=list(wrong_receipt), negativeActualWindowsReturns=wrong_receipt[3],
        executable=dict(path=native.relative_to(ROOT).as_posix(), sha256=sha256(native)),
        wrongExecutable=dict(path=wrong.relative_to(ROOT).as_posix(), sha256=sha256(wrong)), steps=steps,
        tools=dict(clang=CLANG_SHA, linker=LINKER_SHA, dlltool=DLLTOOL_SHA),
        implementationContract='Win32 pointer layout; aligned buffers; -fno-strict-aliasing; supplied C word-fill boundary',
        limitations=['No original ARM fill-helper source is reconstructed by the supplied Windows boundary',
                    'No original ROM/save/assets are required by the synthetic executable',
                    'No complete Windows game or Android device execution is proven']))
    print(dict(actualWindowsReturns=receipt[3], suppliedFillCalls=receipt[4],
               negativeActualWindowsReturns=wrong_receipt[3], pointerBytes=4))


if __name__ == '__main__':
    main()
