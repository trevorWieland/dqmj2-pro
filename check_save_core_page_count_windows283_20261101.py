import argparse
import ctypes
import gzip
import hashlib
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CLANG_SHA = '6b7a698ccd1d5ef7375b7733f0675a166c560112961d3e5df0f275565a9201bc'
LINKER_SHA = 'b64100b407a472f831caf2789f6c09d501e2e4c876ebc772997c294be7f9f8f3'
WRAPPER = 'src/mechanics_save/20261101_lane_page_count_word/native_main_0206e644.c'
SERVICES = 'ports/windows-native/page_count283_services.c'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def build(source, key, tools):
    clang, linker = tools / 'clang.exe', tools / 'ld.lld.exe'
    assert sha(clang.read_bytes()) == CLANG_SHA and sha(linker.read_bytes()) == LINKER_SHA
    folder = ROOT / 'work/save-core/page-count-windows283' / key
    folder.mkdir(parents=True, exist_ok=True)
    objects, provenance = [], []
    for index, path in enumerate([source, WRAPPER, SERVICES]):
        obj = folder / (str(index) + '.obj')
        command = [str(clang), '--driver-mode=cl', '--target=x86_64-pc-windows-msvc', '/TC', '/std:c11', '/O2', '/Brepro',
            '/clang:-ffreestanding', '/clang:-fno-builtin', '/clang:-fno-stack-protector', '/clang:-fno-strict-aliasing',
            '/c', str(ROOT / path), '/Fo' + str(obj)]
        if path == WRAPPER:
            command.append('/Dnative_fn_0206e634=native_main_0206e634')
        process = subprocess.run(command, cwd=ROOT, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
        assert struct.unpack_from('<I', obj.read_bytes(), 4)[0] == 0
        provenance.append(dict(source=path, sourceSha256=sha((ROOT / path).read_bytes()), object=obj.relative_to(ROOT).as_posix(),
            objectSha256=sha(obj.read_bytes()), objectTimeDateStamp=0, command=command, exitCode=0))
        objects.append(str(obj))
    dll = folder / 'page_count.dll'
    exports = ['native_main_0206e634', 'native_main_0206e644', 'page_count_reset', 'page_count_status', 'native_data_021c4f60,DATA']
    command = [str(linker), '-flavor', 'link', '/dll', '/noentry', '/nodefaultlib', '/machine:x64', '/timestamp:0',
        '/out:' + str(dll), *['/export:' + item for item in exports], *objects]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    assert process.returncode == 0, process.stdout + process.stderr
    module = ctypes.CDLL(str(dll))
    for name in ['native_main_0206e634', 'native_main_0206e644', 'page_count_reset']:
        function = getattr(module, name)
        function.argtypes, function.restype = [ctypes.c_uint32], ctypes.c_uint32
    module.page_count_status.argtypes, module.page_count_status.restype = [], ctypes.c_uint32
    return module, dict(objects=provenance, binary=dll.relative_to(ROOT).as_posix(), binarySha256=sha(dll.read_bytes()),
        linkCommand=command, linkExitCode=0)


def invoke(module, entry, profile):
    module.page_count_reset(profile['previous'])
    function = module.native_main_0206e634 if entry == 0x0206E634 else module.native_main_0206e644
    returned = function(profile['value'])
    data = bytes((ctypes.c_ubyte * 0x70).in_dll(module, 'native_data_021c4f60'))
    status = module.page_count_status()
    assert status == (0 if entry == 0x0206E634 else 3 << 16)
    return dict(rawReturn=returned, dataHex=data.hex(), serviceCalls=status >> 16)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tools-bin')
    args = parser.parse_args()
    assert sys.platform == 'win32' and ctypes.sizeof(ctypes.c_void_p) == 8
    local = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    fallback = ROOT.parents[1] / 'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    tools = Path(args.tools_bin).resolve() if args.tools_bin else local if local.is_dir() else fallback
    oracle = json.loads((ROOT / 'evidence/application/save-core-page-count282-20261101.json').read_text())
    source = oracle['matches'][0]['source']
    module, built = build(source, 'preferred', tools)
    digest, native_digest, calls = hashlib.sha256(), hashlib.sha256(), 0
    raw = (ROOT / oracle['sidecar']['path']).read_bytes()
    assert sha(raw) == oracle['sidecar']['sha256']
    for line in gzip.decompress(raw).splitlines(keepends=True):
        native_digest.update(line)
        value = json.loads(line)
        actual = invoke(module, value['entry'], value['profile'])
        expected = bytes.fromhex(value['native']['after'][str(0x021C4F50)])[16:16 + 0x70].hex()
        assert actual['rawReturn'] == value['profile']['value'] == value['native']['returnWord']
        assert actual['dataHex'] == expected
        digest.update((json.dumps(dict(entry=value['entry'], profile=value['profile'], result=actual), sort_keys=True, separators=(',', ':')) + '\n').encode())
        calls += 1
    assert native_digest.hexdigest() == oracle['nativeCaseSha256']
    controls, wrong_builds = [], []
    for row in oracle['controls']['rows']:
        wrong_module, wrong_built = build(row['source'], Path(row['source']).stem, tools)
        wrong_builds.append(wrong_built)
        for value in (0, 1, 127, 128, 255, 256, 0x12345680, 0xFFFFFFFF):
            profile = dict(value=value, previous=0xA5)
            for entry in (0x0206E634, 0x0206E644):
                good, wrong = invoke(module, entry, profile), invoke(wrong_module, entry, profile)
                assert good['rawReturn'] == value
                controls.append(dict(source=row['source'], entry=entry, profile=profile, rejected=good != wrong))
    assert sum(row['rejected'] for row in controls) == 30
    output = dict(schema=1, platform='Windows64', target='x86_64-pc-windows-msvc', signature='u32(u32)',
        compilerSha256=CLANG_SHA, linkerSha256=LINKER_SHA, explicitToolsBin=str(tools), source=built, wrongSources=wrong_builds,
        actualPublicCalls=calls, actualGoodControlCalls=48, actualWrongControlCalls=48, totalActualPublicCalls=calls + 96,
        nativeCaseSha256=native_digest.hexdigest(), windowsCaseSha256=digest.hexdigest(), controls=controls,
        sourceCoverageAdded=0, generatorSha256=sha(Path(__file__).read_bytes()),
        limits=['Two isolated C source routines execute onWindows64 withthree explicit C service providers for the wrapper.',
            'Provider arguments/order andthe full exported byte backing are checked. GameUI,emulator,Android-device andordinary menu reachability remain unproved.',
            'Fullword input/rawreturn andlow-byte stores follow the native golden;setup/status scaffolding calls areexcluded from public-function counts.',
            'Timestamp-zero COFF andPE are generated bypinned compiler /Brepro andlinker options without output editing.'])
    path = ROOT / 'evidence/ports/save-core-page-count-windows283-20261101.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: output[key] for key in ('actualPublicCalls', 'actualGoodControlCalls', 'actualWrongControlCalls', 'windowsCaseSha256')}))


if __name__ == '__main__':
    main()
