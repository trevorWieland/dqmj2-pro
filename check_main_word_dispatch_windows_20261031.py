import ctypes
import os
import subprocess
from project import ROOT, read_json, write_json, sha256
from compile_memory_primitives_ports_20261030 import CLANG_SHA, LINKER_SHA
from compile_android_checks_20261029 import ENV_NAMES

SOURCE = 'src/runtime/20261031_word_dispatch/native_main_02005bd8.c'
FIXTURE = 'ports/windows-native/word_dispatch_fixture.c'
GOLDEN = 'evidence/matches/main-word-dispatch-20261031.json'


def main():
    golden = read_json(ROOT / GOLDEN)
    assert sha256(ROOT / SOURCE) == golden['matches'][0]['sourceSha256']
    assert golden['matches'][0]['nativeOracle']['actualReturns'] == 1048
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker = tools / 'clang.exe', tools / 'ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    work = ROOT / 'work/main-word-dispatch-20261031/windows'
    work.mkdir(parents=True, exist_ok=True)
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    steps = []

    def run(command):
        command = list(map(str, command))
        result = subprocess.run(command, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=120)
        steps.append(dict(command=command, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        if result.returncode:
            raise ValueError(result.stdout + result.stderr)

    def compile_source(source, output):
        run([clang, '--target=x86_64-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding',
             '-fno-builtin', '-fno-stack-protector', '-fno-strict-aliasing', '-c', source, '-o', output])

    fixture = work / 'fixture.obj'
    compile_source(ROOT / FIXTURE, fixture)
    exports = ['j2p_word_setup', 'j2p_word_unchanged', 'native_main_02005bd8']

    def library(source, label):
        obj, dll = work / (label + '.obj'), work / (label + '.dll')
        compile_source(source, obj)
        run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib',
             '/timestamp:0', '/out:' + str(dll), *['/export:' + name for name in exports], obj, fixture])
        value = ctypes.CDLL(str(dll))
        value.j2p_word_setup.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        value.j2p_word_setup.restype = None
        value.j2p_word_unchanged.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        value.j2p_word_unchanged.restype = ctypes.c_uint32
        value.native_main_02005bd8.argtypes = [ctypes.c_uint32]
        value.native_main_02005bd8.restype = ctypes.c_uint32
        return value, dict(path=dll.relative_to(ROOT).as_posix(), sha256=sha256(dll))

    native, artifact = library(ROOT / SOURCE, 'word-dispatch')

    def execute(loaded, item):
        shared = ctypes.create_string_buffer(bytes.fromhex(item['shared']))
        table = ctypes.create_string_buffer(bytes.fromhex(item['table']))
        loaded.j2p_word_setup(shared, table)
        result = loaded.native_main_02005bd8(item['mask'])
        assert loaded.j2p_word_unchanged(shared, table) == 1
        return result

    for case in golden['results']:
        assert execute(native, case['recipe']) == case['result']['returnValue']
    negative = ROOT / golden['negativeCompiled']['source']
    assert sha256(negative) == golden['negativeCompiled']['sourceSha256']
    wrong, wrong_artifact = library(negative, 'wrong-width')
    controls = []
    for case in golden['negativeControls']:
        assert execute(native, case['recipe']) == case['original']['returnValue']
        result = execute(wrong, case['recipe'])
        assert result == case['result']['returnValue']
        controls.append(dict(actualReturn=result, modelRejected=not case['result']['modelPassed']))
    report = dict(source=SOURCE, sourceSha256=sha256(ROOT / SOURCE), fixture=FIXTURE,
                  fixtureSha256=sha256(ROOT / FIXTURE), golden=GOLDEN, goldenSha256=sha256(ROOT / GOLDEN),
                  actualWindowsReturns=len(golden['results']), negativeActualWindowsReturns=len(controls), negativeOriginalWindowsReturns=len(controls),
                  controls=controls, artifact=artifact, negativeArtifact=wrong_artifact,
                  clangSha256=sha256(clang), linkerSha256=sha256(linker), steps=steps,
                  implementationContract='Aligned byte buffers accessed with unsigned-word views and -fno-strict-aliasing',
                  fullWindowsGameFromSourceProven=False, androidDeviceExecutionCount=0)
    write_json(ROOT / 'evidence/portability/main-word-dispatch-windows-20261031.json', report)
    print(dict(actualWindowsReturns=report['actualWindowsReturns'],
               negativeActualWindowsReturns=report['negativeActualWindowsReturns']))


if __name__ == '__main__':
    main()
