import ctypes
import gzip
import hashlib
import json
from project import ROOT, read_json, write_json, sha256
from main_handle_refresh_fixture_20261101 import DATA, scenario, word, put


def cleanup(page):
    current = word(page, 0x64)
    assert current and not page[0xA] & 4
    found = False
    for header in [0x14, 0x1C, 0x24]:
        address = word(page, header)
        previous = None
        visited = set()
        while address:
            assert DATA <= address <= DATA + 4096 - 20 and address not in visited
            visited.add(address)
            following = word(page, address - DATA + 0x10)
            if address == current:
                put(page, header if previous is None else previous - DATA + 0x10, following)
                put(page, address - DATA + 0x10, 0)
                found = True
                break
            previous, address = address, following
        if found:
            break
    if found:
        put(page, 0xC, word(page, 0xC) | 0x10)
    put(page, 0x64, 0)
    put(page, 0xF8, 0)
    return 1


def main():
    build_path = ROOT / 'evidence/portability/handle-refresh-build-20261101.json'
    build = read_json(build_path)
    assert sha256(ROOT / build['source']) == build['sourceSha256']
    assert sha256(ROOT / build['glue']) == build['glueSha256']
    assert sha256(ROOT / build['generatedPort']) == build['generatedPortSha256']
    assert sha256(ROOT / build['nativeGoldenReport']) == build['nativeGoldenReportSha256']
    library = ROOT / build['windows']['path']
    assert sha256(library) == build['windows']['sha256']
    dll = ctypes.CDLL(str(library))
    callback_type = ctypes.CFUNCTYPE(ctypes.c_uint32, ctypes.c_void_p)
    setter = dll.set_handle_contract
    setter.argtypes, setter.restype = [callback_type], None
    function = dll.native_main_020296b0
    function.argtypes, function.restype = [ctypes.c_void_p], ctypes.c_uint32
    report = read_json(ROOT / build['nativeGoldenReport'])
    trace = report['oracle']['traceArchive']
    assert sha256(ROOT / trace['path']) == trace['sha256']
    raw = gzip.decompress((ROOT / trace['path']).read_bytes())
    assert hashlib.sha256(raw).hexdigest() == trace['decodedSha256']
    vectors = json.loads(raw)
    backing = ctypes.create_string_buffer(6144)
    base, page_address = ctypes.addressof(backing), ctypes.addressof(backing) + 1024
    assert ctypes.sizeof(ctypes.c_void_p) == 8 and page_address > 0xFFFFFFFF
    calls, failures = [], []

    def lower(address):
        try:
            assert address == page_address
            page = bytearray(ctypes.string_at(address, 4096))
            result = cleanup(page)
            ctypes.memmove(address, bytes(page), 4096)
            calls.append(dict(result=result, stateSha256=hashlib.sha256(page).hexdigest()))
            return result
        except BaseException as error:
            failures.append(type(error).__name__ + ': ' + str(error))
            return 0

    callback = callback_type(lower)
    setter(callback)
    cases = []
    for vector in vectors:
        index, golden = vector['index'], vector['original']
        initial, expected, expected_result = scenario(index)
        assert hashlib.sha256(expected).hexdigest() == golden['stateSha256']
        assert expected_result == golden['result']
        prefix, suffix = bytes([0xA7]) * 1024, bytes([0x5C]) * 1024
        ctypes.memmove(base, prefix + bytes(initial) + suffix, 6144)
        calls.clear()
        result = function(page_address)
        assert not failures, failures
        after = ctypes.string_at(page_address, 4096)
        assert result == expected_result and after == expected
        assert ctypes.string_at(base, 1024) == prefix
        assert ctypes.string_at(page_address + 4096, 1024) == suffix
        assert len(calls) == int(bool(word(initial, 0x60) and word(initial, 0x64)))
        cases.append(dict(index=index, result=result, actualWindowsCalls=1,
            suppliedLowerCalls=len(calls), stateSha256=hashlib.sha256(after).hexdigest()))
    write_json(ROOT / 'evidence/portability/handle-refresh-windows-20261101.json', dict(
        generator='verify_windows_handle_refresh_20261101.py', generatorSha256=sha256(__file__),
        buildReport=build_path.relative_to(ROOT).as_posix(), buildReportSha256=sha256(build_path),
        windowsLibrarySha256=sha256(library), actualWindowsFunctionCalls=len(cases),
        suppliedLowerCalls=sum(row['suppliedLowerCalls'] for row in cases),
        cases=cases, allPassed=True, dataPointerAbove4GiB=True, prefixAndSuffixGuardsPreserved=True,
        storedWordsRemain32Bit=True, independentNativeGoldenEffects=True,
        fullWindowsGameCompiled=False, androidDeviceExecutions=0, sourceCredit=0,
        limitations=['Recovered own C body executes as Windows x64 code; source API pointer types widened only',
            'Lower helper behavior is supplied through a Python callback and receives no native-Windows helper credit',
            'Bounded three-list contexts with input flag0x4 clear; no concurrency/free-callback/scene/graphics proof']))
    print(dict(actualWindowsCalls=len(cases), allPassed=True, dataPointerAbove4GiB=True,
        suppliedLowerCalls=sum(row['suppliedLowerCalls'] for row in cases), sourceCredit=0))


if __name__ == '__main__':
    main()
