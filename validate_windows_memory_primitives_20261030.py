import ctypes
import hashlib
from project import ROOT, read_json, sha256, write_json


def main():
    build_path = ROOT / 'evidence/portability/windows-memory-primitives-build-20261030.json'
    build = read_json(build_path)
    golden_path = ROOT / 'evidence/matches/main-memory-primitives-20261030.json'
    golden = read_json(golden_path)
    assert sha256(golden_path) == build['nativeGoldenReportSha256']
    assert sha256(ROOT / 'compile_memory_primitives_ports_20261030.py') == build['generatorSha256']
    dll_path = ROOT / build['output']['path']
    assert sha256(dll_path) == build['output']['sha256']
    for step in build['steps']:
        if 'source' in step:
            assert sha256(ROOT / step['source']) == step['sourceSha256']
    library = ctypes.CDLL(str(dll_path))
    search = library.native_main_0201b21c
    search.argtypes = [ctypes.c_void_p, ctypes.c_int32, ctypes.c_uint32]
    search.restype = ctypes.c_void_p
    compare = library.native_main_0201b248
    compare.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32]
    compare.restype = ctypes.c_int32
    fill = library.native_main_0201b288
    fill.argtypes = [ctypes.c_void_p, ctypes.c_int32, ctypes.c_uint32]
    fill.restype = None
    results = []
    for tag, row in enumerate(golden['oracle']['rows']):
        mode, value, count, alignment, relation = row['case']
        memory = bytearray((i * 73 + tag * 11) & 255 for i in range(0x1000))
        offset, other = 0x100 + alignment, 0x600 + alignment
        if mode == 'search':
            memory[offset:offset + count] = bytes([(value + 1) & 255]) * count
            if count and relation != 2:
                memory[offset + (0 if relation == 0 else count - 1)] = value
        elif mode == 'compare':
            memory[offset:offset + count] = bytes([value]) * count
            memory[other:other + count] = memory[offset:offset + count]
            if relation:
                memory[other + (0 if relation == 1 else count - 1)] = (value + relation) & 255
        buffer = ctypes.create_string_buffer(bytes(memory), len(memory))
        base = ctypes.addressof(buffer)
        assert base >= 0x100000000
        expected_r0 = row['result']['registers'][0]
        if mode == 'search':
            actual = search(base + offset, value | ((tag & 0xFFFFFF) << 8), count)
            normalized = 0 if actual is None else 0x02500000 + actual - base
            assert normalized == expected_r0
        elif mode == 'compare':
            actual = compare(base + offset, base + other, count)
            assert actual == ctypes.c_int32(expected_r0).value
            normalized = actual
        else:
            assert fill(base + offset, value, count) is None
            normalized = None
        digest = hashlib.sha256(buffer.raw).hexdigest()
        assert digest == row['result']['dataSha256']
        results.append({'case': row['case'], 'actualReturn': True, 'normalizedResult': normalized,
                        'completeBufferSha256': digest, 'hostBufferAbove4GiB': True})
    assert len(results) == 2464
    report = {'windowsNativeCalls': len(results), 'allPassed': True, 'sourceCredit': 0,
              'fullWindowsGameFromSourceProven': False, 'androidDeviceExecutions': 0,
              'buildReport': build_path.relative_to(ROOT).as_posix(), 'buildReportSha256': sha256(build_path),
              'nativeGoldenReport': golden_path.relative_to(ROOT).as_posix(), 'nativeGoldenReportSha256': sha256(golden_path),
              'generatorSources': [{'path': 'validate_windows_memory_primitives_20261030.py', 'sha256': sha256(ROOT / 'validate_windows_memory_primitives_20261030.py')}],
              'results': results,
              'limitations': ['Windows x64 execution of unchanged leaf C only; no full game or device run',
                              'C return values and all buffer bytes checked; host scratch registers/flags are not observed',
                              'The fill pointer-to-u32 cast uses only the low two alignment bits; all tested host buffers exceed 4GiB',
                              'Android AArch64 linking is separate compile evidence; Android execution and dual-screen behavior remain untested']}
    path = ROOT / 'evidence/portability/windows-memory-primitives-execution-20261030.json'
    write_json(path, report)
    print({'windowsNativeCalls': len(results), 'allPassed': True, 'reportSha256': sha256(path), 'sourceCredit': 0})


if __name__ == '__main__':
    main()
