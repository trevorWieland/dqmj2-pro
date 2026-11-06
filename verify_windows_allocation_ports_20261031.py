import ctypes
import hashlib
import random
import struct
from project import ROOT, read_json, sha256, write_json


def main():
    build = read_json(ROOT / 'evidence/portability/allocation-build-20261031.json')
    assert all(sha256(ROOT / path) == digest for path, digest in build['sources'].items())
    assert sha256(ROOT / build['nativeGoldenReport']) == build['nativeGoldenReportSha256']
    library_path = ROOT / build['windows']['path']
    assert sha256(library_path) == build['windows']['sha256']
    dll = ctypes.CDLL(str(library_path))
    slots = (ctypes.c_ubyte * 320).in_dll(dll, 'native_data_020edd64')
    flags = (ctypes.c_ubyte * 3).in_dll(dll, 'native_data_020edd54')
    default = (ctypes.c_ubyte * 1).in_dll(dll, 'native_data_020dd580')
    supplied = ctypes.c_uint32.in_dll(dll, 'allocation_contract_result')
    called = ctypes.c_uint32.in_dll(dll, 'allocation_contract_calls')
    address = ctypes.c_uint32.in_dll(dll, 'allocation_contract_address')
    words = (ctypes.c_uint32 * 3).in_dll(dll, 'allocation_contract_words')
    assert ctypes.sizeof(ctypes.c_uint32) == 4 and ctypes.addressof(slots) > 0xFFFFFFFF
    native = read_json(ROOT / build['nativeGoldenReport'])
    cases = []
    for qualification in native['qualifications']:
        entry = int(qualification['address'], 0)
        function = getattr(dll, f'native_main_{entry:08x}')
        function.argtypes = [ctypes.c_uint32, ctypes.c_uint32, ctypes.c_int32]
        function.restype = ctypes.c_uint32
        for case in qualification['cases']:
            index, golden = case['index'], case['result']
            rng = random.Random(entry * 10000 + index)
            default_page, slot_page = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
            heap_word = rng.getrandbits(32)
            allocation = 0 if index % 5 == 0 else rng.getrandbits(32) | 1
            assert heap_word == golden['slotHeap'] and allocation == golden['suppliedAllocationResult']
            raw_default = golden['defaultByte']
            default_page[0x580] = raw_default
            selected = raw_default if raw_default < 128 else raw_default - 256
            if entry == 0x0202A37C and golden['arguments'][0] != 0xFFFFFFFF:
                selected = golden['arguments'][0]
            if entry == 0x0202B334:
                source_index = [0xFFFFFFFF, 0, 1, 7, 15, 16, 31, 127, 128, 255][index % 10]
                if source_index != 0xFFFFFFFF:
                    selected = source_index
            valid = selected & 255 < 16
            if valid:
                at = 0xD64 + selected * 20
                enabled_word = rng.getrandbits(32) | 1 if golden['slotEnabled'] else 0
                struct.pack_into('<I', slot_page, at, enabled_word)
                struct.pack_into('<I', slot_page, at + 12, golden['slotCounter'])
                struct.pack_into('<I', slot_page, at + 16, heap_word)
            expected = slot_page[:]
            lower_expected = entry == 0x0202B334 or valid and golden['slotEnabled']
            if entry == 0x0202A37C:
                expected[0xD56] = 1 if not lower_expected else 0 if allocation else 5
                if lower_expected and allocation:
                    struct.pack_into('<I', expected, at + 12, (golden['slotCounter'] + 1) & 0xFFFFFFFF)
            assert hashlib.sha256(expected).hexdigest() == golden['slotsSha256']
            assert hashlib.sha256(default_page).hexdigest() == golden['defaultSha256']
            slots[:] = slot_page[0xD64:0xD64 + 320]
            flags[:] = slot_page[0xD54:0xD57]
            default[0] = raw_default
            supplied.value, called.value, address.value = allocation, 0, 0
            words[:] = [0, 0, 0]
            arguments = golden['arguments']
            result = function(arguments[0], arguments[1], ctypes.c_int32(arguments[2]).value)
            assert result == golden['result']
            assert bytes(slots) == expected[0xD64:0xD64 + 320]
            assert bytes(flags) == expected[0xD54:0xD57] and default[0] == raw_default
            assert called.value == len(golden['calls'])
            if golden['calls']:
                assert address.value == int(golden['calls'][0]['address'], 0)
                assert list(words) == golden['calls'][0]['arguments']
            cases.append(dict(address=hex(entry), index=index, result=result, contractCalls=called.value))
    assert len(cases) == 1764
    write_json(ROOT / 'evidence/portability/windows-allocation-execution-20261031.json', dict(
        passed=True, actualWindowsReturns=len(cases), library=build['windows'],
        sourceHashes=build['sources'], nativeGoldenReport=build['nativeGoldenReport'],
        nativeGoldenReportSha256=build['nativeGoldenReportSha256'], dataAddress=hex(ctypes.addressof(slots)),
        dataPointersAbove4GiB=True, slotBytesComparedPerCase=320, statusBytesComparedPerCase=3,
        defaultBytesComparedPerCase=1, cases=cases, sourceCredit=0, androidDeviceExecutions=0,
        limitations=['Actual Windows execution of two unchanged recovered functions; all16 declared slot records and supplied lower-call effects checked against native golden backing',
            'Lower allocator bodies are test contracts; no real heap, arbitrary high-word aliased index, full game or device proof',
            'ARM scratch-register/CPSR state is not a Windows API contract']))
    print(dict(passed=True, windowsActualReturns=len(cases), dataPointersAbove4GiB=True))


if __name__ == '__main__':
    main()
