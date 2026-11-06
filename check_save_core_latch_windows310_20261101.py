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
STORAGE = 'ports/windows-native/latch310_storage.c'
SOURCE = 'src/mechanics_save/20261101_lane_latch_word/native_main_02062358.c'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def build(source, key, tools):
    clang, linker = tools / 'clang.exe', tools / 'ld.lld.exe'
    assert sha(clang.read_bytes()) == CLANG_SHA and sha(linker.read_bytes()) == LINKER_SHA
    folder = ROOT / 'work/save-core/latch-windows310' / key
    folder.mkdir(parents=True, exist_ok=True)
    objects, provenance = [], []
    for index, path in enumerate((source, STORAGE)):
        obj = folder / (str(index) + '.obj')
        command = [str(clang), '--driver-mode=cl', '--target=x86_64-pc-windows-msvc', '/TC', '/std:c11', '/O2', '/Brepro',
            '/clang:-ffreestanding', '/clang:-fno-builtin', '/clang:-fno-stack-protector', '/clang:-fno-strict-aliasing',
            '/c', str(ROOT / path), '/Fo' + str(obj)]
        process = subprocess.run(command, cwd=ROOT, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, process.stdout + process.stderr
        assert struct.unpack_from('<I', obj.read_bytes(), 4)[0] == 0
        objects.append(str(obj))
        provenance.append(dict(source=path, sourceSha256=sha((ROOT / path).read_bytes()), object=obj.relative_to(ROOT).as_posix(),
            objectSha256=sha(obj.read_bytes()), objectTimeDateStamp=0, command=command, exitCode=0))
    dll = folder / 'latch.dll'
    command = [str(linker), '-flavor', 'link', '/dll', '/noentry', '/nodefaultlib', '/machine:x64', '/timestamp:0',
        '/out:' + str(dll), '/export:native_main_02062358', '/export:latch_reset', '/export:native_data_021b9bd4,DATA', *objects]
    process = subprocess.run(command, cwd=ROOT, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    assert process.returncode == 0, process.stdout + process.stderr
    module = ctypes.CDLL(str(dll))
    module.latch_reset.argtypes, module.latch_reset.restype = [ctypes.c_uint32], None
    module.native_main_02062358.argtypes, module.native_main_02062358.restype = [ctypes.c_uint32], ctypes.c_uint32
    return module, dict(objects=provenance, binary=dll.relative_to(ROOT).as_posix(), binarySha256=sha(dll.read_bytes()),
        linkCommand=command, linkExitCode=0)


def invoke(module, profile):
    module.latch_reset(profile['previous'])
    result = module.native_main_02062358(profile['value'])
    return dict(rawReturn=result, data=bytes((ctypes.c_ubyte * 0x280).in_dll(module, 'native_data_021b9bd4')).hex())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--tools-bin')
    args = parser.parse_args()
    assert sys.platform == 'win32' and ctypes.sizeof(ctypes.c_void_p) == 8
    local = ROOT / 'tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    fallback = ROOT.parents[1] / 'dqmj2pro-decomp/tools/android-ndk/r30/toolchains/llvm/prebuilt/windows-x86_64/bin'
    tools = Path(args.tools_bin).resolve() if args.tools_bin else local if local.is_dir() else fallback
    native = json.loads((ROOT / 'evidence/application/save-core-latch309-20261101.json').read_text())
    wrong_native = json.loads((ROOT / 'evidence/application/save-core-latch311-controls-20261101.json').read_text())
    module, preferred = build(SOURCE, 'preferred', tools)
    packed = (ROOT / native['leafSidecar']['path']).read_bytes()
    raw = gzip.decompress(packed)
    assert sha(packed) == native['leafSidecar']['sha256'] and sha(raw) == native['leafCaseSha256']
    digest, calls = hashlib.sha256(), 0
    for line in raw.splitlines():
        row = json.loads(line)
        actual = invoke(module, row['profile'])
        expected = bytes.fromhex(row['native']['after'][str(0x021B9BC4)])[16:16 + 0x280].hex()
        assert actual['rawReturn'] == row['native']['returnWord'] == row['profile']['value']
        assert actual['data'] == expected
        digest.update((json.dumps(dict(profile=row['profile'], actual=actual), sort_keys=True, separators=(',', ':')) + '\n').encode())
        calls += 1
    controls, builds = [], []
    for candidate in wrong_native['rows']:
        wrong, built = build(candidate['source'], Path(candidate['source']).stem, tools)
        builds.append(built)
        for value in (0, 1, 127, 128, 165, 255, 256, 0x12345680, 0xFFFFFFFF):
            profile = dict(value=value, previous=165)
            good, bad = invoke(module, profile), invoke(wrong, profile)
            assert good['rawReturn'] == value
            controls.append(dict(source=candidate['source'], profile=profile, rejected=good != bad))
    assert calls == 1536 and sum(row['rejected'] for row in controls) == 16
    report = dict(schema=1, actualPublicCalls=calls, actualGoodControlCalls=len(controls), actualWrongControlCalls=len(controls),
        totalActualPublicCalls=calls + len(controls) * 2, nativeCaseSha256=native['leafCaseSha256'],
        windowsCaseSha256=digest.hexdigest(), source=preferred, wrongSources=builds, controls=controls,
        generatorSha256=sha(Path(__file__).read_bytes()), sourceCredit=0,
        limits=['The same unchanged reconstructed setter C is compiled to a Windows64 DLL and actually called. Storage adapts the physical global to a local byte array; no native function body is replaced by a model.',
            'Only the pure byte writer is executed on Windows; the396-byte controller and overlay birth caller are not executed here.',
            'All three complete wrong C controls have the same rejection/positive domains as native ARM. No Windows game, Android device or ordinary scene execution is claimed.'])
    path = ROOT / 'evidence/ports/save-core-latch-windows310-20261101.json'
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('actualPublicCalls', 'actualGoodControlCalls', 'actualWrongControlCalls', 'totalActualPublicCalls', 'windowsCaseSha256')}))


if __name__ == '__main__':
    main()
