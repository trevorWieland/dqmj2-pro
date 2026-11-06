import argparse
import ctypes
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import struct
import sys

ROOT = Path(__file__).resolve().parent
CLANG_SHA = '6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA = 'b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
ORACLE = 'evidence/application/save-core-skill-byteview266-20261101.json'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class Record(ctypes.Structure):
    _fields_ = [('threshold', ctypes.c_ubyte * 10), ('actions', ctypes.c_ubyte * 40), ('features', ctypes.c_ubyte * 10)]


def compile_source(source, label, tools):
    clang, linker = tools / 'clang.exe', tools / 'ld.lld.exe'
    assert sha(clang.read_bytes()) == CLANG_SHA and sha(linker.read_bytes()) == LINKER_SHA
    folder = ROOT / 'work/save-core/skill-record-windows267' / label
    folder.mkdir(parents=True, exist_ok=True)
    obj, dll = folder / 'source.obj', folder / 'skill_record_bytes.dll'
    commands = [[str(clang), '--driver-mode=cl', '--target=x86_64-pc-windows-msvc', '/TC', '/std:c11', '/O2', '/Brepro',
        '/clang:-ffreestanding', '/clang:-fno-builtin', '/clang:-fno-stack-protector', '/clang:-fno-strict-aliasing',
        '/c', str(ROOT / source), '/Fo' + str(obj)],
        [str(linker), '-flavor', 'link', '/dll', '/noentry', '/machine:x64', '/nodefaultlib',
         '/timestamp:0', '/export:native_main_0207ad98', '/out:' + str(dll), str(obj)]]
    results = []
    for command in commands:
        process = subprocess.run(command, cwd=ROOT, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
        results.append(dict(command=command, exitCode=process.returncode, stdout=process.stdout.decode(errors='replace'), stderr=process.stderr.decode(errors='replace')))
    assert struct.unpack_from('<I', obj.read_bytes(), 4)[0] == 0
    module = ctypes.CDLL(str(dll))
    function = module.native_main_0207ad98
    function.argtypes, function.restype = [ctypes.POINTER(Record), ctypes.c_int8], ctypes.c_int
    return module, function, dict(source=source, sourceSha256=sha((ROOT / source).read_bytes()),
        object=obj.relative_to(ROOT).as_posix(), objectSha256=sha(obj.read_bytes()), objectTimeDateStamp=0,
        binary=dll.relative_to(ROOT).as_posix(), binarySha256=sha(dll.read_bytes()), results=results)


def call(function, data, index):
    record = Record()
    assert ctypes.sizeof(record) == 60
    ctypes.memmove(ctypes.addressof(record), data, 60)
    returned = function(ctypes.byref(record), index)
    assert ctypes.string_at(ctypes.addressof(record), 60) == data
    return returned


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tools-bin')
    args = parser.parse_args()
    assert sys.platform == 'win32' and ctypes.sizeof(ctypes.c_void_p) == 8
    local = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    fallback = ROOT.parents[1] / 'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    tools = Path(args.tools_bin).resolve() if args.tools_bin else local if local.is_dir() else fallback
    oracle = json.loads((ROOT / ORACLE).read_text())
    source = oracle['candidate']['source']
    assert sha((ROOT / source).read_bytes()) == oracle['candidate']['sourceSha256']
    module, function, built = compile_source(source, 'preferred', tools)
    case_digest, native_digest, count = hashlib.sha256(), hashlib.sha256(), 0
    sidecar = ROOT / oracle['sidecar']['path']
    assert sha(sidecar.read_bytes()) == oracle['sidecar']['sha256']
    for line in gzip.open(sidecar, 'rb'):
        native_digest.update(line)
        value = json.loads(line)
        data = bytes.fromhex(value['recordHex'])
        returned = call(function, data, value['profile']['index'])
        assert returned == value['expected'] == value['native']['rawReturn']
        case_digest.update((json.dumps(dict(profile=value['profile'], recordSha256=sha(data), expected=value['expected'], actual=returned), sort_keys=True, separators=(',', ':')) + '\n').encode())
        count += 1
    assert native_digest.hexdigest() == oracle['caseSha256'] and count == 16125
    wrong_source = oracle['controls']['candidate']['source']
    wrong_module, wrong_function, wrong_built = compile_source(wrong_source, 'wrong', tools)
    raw = gzip.decompress((ROOT / oracle['controls']['sidecar']['path']).read_bytes())
    assert sha(raw) == oracle['controls']['caseSha256']
    controls = []
    for value in json.loads(raw):
        data = bytes.fromhex(value['recordHex'])
        good, wrong = call(function, data, 0), call(wrong_function, data, 0)
        assert good == value['native']['rawReturn'] and wrong == value['wrong']['rawReturn']
        controls.append(dict(expected=good, actualWrong=wrong, rejected=wrong != good))
    assert sum(v['rejected'] for v in controls) == 2
    report = dict(schema=1, host='Windows', architecture='x86_64', target='x86_64-pc-windows-msvc',
        compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA, explicitToolsBin=str(tools),
        source=built, wrongSource=wrong_built, actualPublicCalls=count, actualControlPublicCalls=6,
        totalActualPublicCalls=count + 6, nativeCaseSha256=native_digest.hexdigest(), windowsCaseSha256=case_digest.hexdigest(),
        controls=controls, recordBytes=60, recordInvariant=True, sourceCoverageAdded=0,
        generatorSha256=sha(Path(__file__).read_bytes()),
        limits=['Only one pure C helper iscompiled forWindows64;no game runtime,UI,emulator orAndroid device executes.',
            'Exactly the native-qualified signed-char/60-byte domains are called. No out-of-object failing control isexecuted onhost.',
            'Toolpath isexplicit,pinned and can be supplied via--tools-bin. Private DLL/COFF outputs remain underwork.'])
    path = ROOT / 'evidence/ports/save-core-skill-bytes-windows267-20261101.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('actualPublicCalls', 'totalActualPublicCalls', 'windowsCaseSha256')}))


if __name__ == '__main__':
    main()
