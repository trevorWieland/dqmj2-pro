import ctypes
import os
import random
import re
import subprocess
from project import ROOT, read_json, write_json, sha256
from compile_memory_primitives_ports_20261030 import CLANG_SHA, LINKER_SHA
from compile_android_checks_20261029 import ENV_NAMES


def main():
    profile_path = ROOT / 'evidence/attempts/forwarded-interfaces-20261031.json'
    profile = read_json(profile_path)
    tools = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    clang, linker = tools / 'clang.exe', tools / 'ld.lld.exe'
    assert sha256(clang) == CLANG_SHA and sha256(linker) == LINKER_SHA
    work = ROOT / 'work/forwarded-interfaces-20261031/windows'
    work.mkdir(parents=True, exist_ok=True)
    declarations = {}
    for row in profile['candidates']:
        path = ROOT / row['compiled']['source']
        assert sha256(path) == row['compiled']['sourceSha256']
        declaration = re.search(r'^extern (u32|s32|int) (native_fn_\w+)\(([^;]+)\);', path.read_text(), re.M)
        assert declaration
        result, name, arguments = declaration.groups()
        if name in declarations:
            assert declarations[name] == (result, arguments)
        declarations[name] = result, arguments
    lines = ['typedef unsigned int u32; typedef signed int s32; typedef unsigned long long u64;',
        'static u64 expected[4]; static u32 result_word, seen, failed;',
        'void j2p_forward_setup(u64 a,u64 b,u64 c,u64 d,u32 r) { expected[0]=a;expected[1]=b;expected[2]=c;expected[3]=d;result_word=r;seen=failed=0; }',
        'u32 j2p_forward_status(void) { return failed || seen!=1; }']
    for name, (result, arguments) in declarations.items():
        checks = []
        for index, part in enumerate(arguments.split(',')):
            argument = re.findall(r'[A-Za-z_]\w*', part)[-1]
            cast = '(u64)' if '*' in part else '(u64)(u32)'
            checks.append(f'({cast}{argument} != expected[{index}])')
        lines.append(f'{result} {name}({arguments}) {{ ++seen; if (' + ' || '.join(checks) +
            f') failed=1; return ({result})result_word; }}')
    stub = work / 'generated_stubs.c'
    stub.write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    environment = {key: value for key, value in os.environ.items() if key not in ENV_NAMES}
    steps = []

    def run(command):
        args = list(map(str, command))
        result = subprocess.run(args, cwd=ROOT, env=environment, capture_output=True, text=True, timeout=120)
        steps.append(dict(command=args, exitCode=result.returncode, stdout=result.stdout, stderr=result.stderr))
        assert result.returncode == 0, result.stdout + result.stderr

    def compile_source(source, output):
        run([clang, '--target=x86_64-pc-windows-msvc', '-std=c11', '-O2', '-ffreestanding',
            '-fno-builtin', '-fno-stack-protector', '-c', source, '-o', output])

    objects = []
    for index, row in enumerate(profile['candidates']):
        output = work / f'{index}.obj'
        compile_source(ROOT / row['compiled']['source'], output)
        objects.append(output)
    stub_object = work / 'stubs.obj'
    compile_source(stub, stub_object)
    exports = [row['previous']['name'] for row in profile['candidates']] + ['j2p_forward_setup', 'j2p_forward_status']

    def link(path, selected):
        run([linker, '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib', '/timestamp:0',
            '/out:' + str(path), *['/export:' + name for name in exports], *selected, stub_object])

    dll_path = work / 'forwarded.dll'
    link(dll_path, objects)

    def configure(library):
        library.j2p_forward_setup.argtypes = [ctypes.c_uint64] * 4 + [ctypes.c_uint32]
        library.j2p_forward_setup.restype = None
        library.j2p_forward_status.argtypes = []
        library.j2p_forward_status.restype = ctypes.c_uint32

    library = ctypes.CDLL(str(dll_path))
    configure(library)
    results = []
    for index, row in enumerate(profile['candidates']):
        parts = row['parameterView'].split(',')
        types = [ctypes.c_void_p if '*' in part else ctypes.c_int32 if re.match(r'\s*(s32|int)\b', part) else ctypes.c_uint32 for part in parts]
        function = getattr(library, row['previous']['name'])
        function.argtypes, function.restype = types, ctypes.c_uint32
        rng = random.Random(0xF047A000 + index)
        for tag in range(32):
            values = [rng.getrandbits(64 if kind == ctypes.c_void_p else 32) for kind in types]
            if tag < 5:
                values = [[0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF][tag]] * len(types)
            result = rng.getrandbits(32)
            library.j2p_forward_setup(*(values + [0] * (4 - len(values))), result)
            assert function(*values) == result and library.j2p_forward_status() == 0
        results.append(dict(caller=row['previous'], cases=32, actualWindowsReturns=32, suppliedCalleeCompletions=32))
    first = profile['candidates'][0]
    source = (ROOT / first['compiled']['source']).read_text()
    parameter = re.findall(r'[A-Za-z_]\w*', first['parameterView'].split(',')[0])[-1]
    wrong_source = source.replace('return ' + next(iter(declarations)) + '(' + parameter,
        'return ' + next(iter(declarations)) + '(0', 1)
    assert wrong_source != source
    wrong_path, wrong_object = work / 'wrong_zero.c', work / 'wrong_zero.obj'
    wrong_path.write_text(wrong_source, encoding='utf-8', newline='\n')
    compile_source(wrong_path, wrong_object)
    wrong_dll = work / 'wrong_forwarded.dll'
    link(wrong_dll, [wrong_object, *objects[1:]])
    wrong = ctypes.CDLL(str(wrong_dll))
    configure(wrong)
    function = getattr(wrong, first['previous']['name'])
    function.argtypes, function.restype = [ctypes.c_void_p], ctypes.c_uint32
    for value, rejected in [(0, False), (1, True), (0x1234567812345678, True)]:
        wrong.j2p_forward_setup(value, 0, 0, 0, 0xA55A1234)
        assert function(value) == 0xA55A1234
        assert bool(wrong.j2p_forward_status()) == rejected
    write_json(ROOT / 'evidence/verification/forwarded-interfaces-windows-20261031.json', dict(
        generator='check_forwarded_interfaces_windows_20261031.py', generatorSha256=sha256(__file__),
        profileSha256=sha256(profile_path), results=results, actualWindowsReturns=32 * len(results),
        suppliedCalleeCompletions=32 * len(results), nativeCalleeExecutionCredit=0,
        negativeWholeCCompiledAndLinked=True, negativeRejections=2, negativePositiveControls=1,
        negativeActualWindowsReturns=3,
        windowsDllSha256=sha256(dll_path), compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA, steps=steps,
        sourceCredit=0, registered=False, limitations=['Explicit source-language forwarding only with supplied callee definitions',
            'Pointer values are opaque implementation-qualified words and are never dereferenced',
            'No Android, game scene, complete target body or accepted-source migration claim']))
    print(dict(candidates=len(results), actualWindowsReturns=32 * len(results), wholeCNegativeRejected=True, sourceCredit=0))


if __name__ == '__main__':
    main()
