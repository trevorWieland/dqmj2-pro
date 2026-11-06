import ctypes
import struct
from project import ROOT, read_json, sha256, write_json


def argument(bits):
    return ctypes.c_double.from_buffer_copy(int(bits, 0).to_bytes(8, 'little'))


def encoding(value):
    return int.from_bytes(struct.pack('<d', value), 'little')


def main():
    build = read_json(ROOT / 'evidence/portability/float-runtime-build-20261031.json')
    for source, digest in build['sources'].items():
        assert sha256(ROOT / source) == digest
    for report, digest in build['reports'].items():
        assert sha256(ROOT / report) == digest
    path = ROOT / build['windows']['path']
    assert sha256(path) == build['windows']['sha256']
    raw = path.read_bytes()
    pe = struct.unpack_from('<I', raw, 0x3C)[0]
    assert raw[pe:pe + 4] == b'PE\0\0' and struct.unpack_from('<H', raw, pe + 4)[0] == 0x8664
    assert struct.unpack_from('<I', raw, pe + 8)[0] == 0
    library = ctypes.CDLL(str(path))
    signatures = {
        0x0202263C: ([ctypes.c_double, ctypes.c_double], ctypes.c_double),
        0x02022684: ([ctypes.c_double, ctypes.c_void_p], ctypes.c_double),
        0x02022740: ([ctypes.c_double, ctypes.c_int], ctypes.c_double),
        0x02023E48: ([ctypes.c_double], ctypes.c_int),
        0x02023E5C: ([ctypes.c_double], ctypes.c_int),
        0x02022664: ([ctypes.c_double], ctypes.c_double),
        0x02023ECC: ([ctypes.c_double, ctypes.c_int], ctypes.c_double),
    }
    records, buffers_above_4g = [], 0
    for report_name in ['main-float-primitives-20261031', 'main-float-rounding-20261031', 'main-float-scale-wrapper-20261031']:
        report = read_json(ROOT / f'evidence/matches/{report_name}.json')
        for group in report['qualifications']:
            entry = int(group['address'], 0)
            if entry not in signatures:
                continue
            function = getattr(library, f'native_main_{entry:08x}')
            function.argtypes, function.restype = signatures[entry]
            for case in group['cases']:
                golden = case['result']
                assert golden['modelPassed'] and golden['result'] == golden['expected']
                args = [argument(golden['input'])]
                buffer, expected_buffer = None, None
                if entry == 0x0202263C:
                    args.append(argument(golden['second']))
                elif entry == 0x02022684:
                    buffer = (ctypes.c_ubyte * 64)(*[i ^ 0xA5 for i in range(64)])
                    expected_buffer = bytearray(buffer)
                    expected_buffer[16:20] = golden['expectedExponent'].to_bytes(4, 'little', signed=True)
                    pointer = ctypes.addressof(buffer) + 16
                    assert pointer > 0xFFFFFFFF
                    buffers_above_4g += 1
                    args.append(pointer)
                elif entry in [0x02022740, 0x02023ECC]:
                    args.append(golden['scale'])
                result = function(*args)
                bits = result & 0xFFFFFFFF if function.restype == ctypes.c_int else encoding(result)
                assert bits == int(golden['result'], 0), (hex(entry), case['index'], hex(bits), golden['result'])
                if buffer is not None:
                    assert bytes(buffer) == bytes(expected_buffer)
                records.append(dict(address=hex(entry), case=case['index'], result=hex(bits), actualWindowsReturn=True))
    function = library.native_main_02023ef8
    function.argtypes, function.restype = [ctypes.c_void_p, ctypes.c_void_p], ctypes.c_int
    report = read_json(ROOT / 'evidence/matches/main-case-compare-20261031.json')
    for case in report['cases']:
        golden = case['result']
        left_bytes, right_bytes = bytes.fromhex(golden['left']), bytes.fromhex(golden['right'])
        left = ctypes.create_string_buffer(left_bytes + bytes([0xA5]) * 16)
        right = left if golden['aliased'] else ctypes.create_string_buffer(right_bytes + bytes([0x5A]) * 16)
        first, second = bytes(left), bytes(right)
        assert ctypes.addressof(left) > 0xFFFFFFFF and ctypes.addressof(right) > 0xFFFFFFFF
        buffers_above_4g += 2
        result = function(ctypes.addressof(left), ctypes.addressof(right)) & 0xFFFFFFFF
        assert result == golden['result'] == golden['expected'] and bytes(left) == first and bytes(right) == second
        records.append(dict(address='0x2023ef8', case=case['index'], result=hex(result), actualWindowsReturn=True))
    assert len(records) == 2912
    write_json(ROOT / 'evidence/portability/windows-float-runtime-execution-20261031.json', dict(
        buildReport='evidence/portability/float-runtime-build-20261031.json',
        buildReportSha256=sha256(ROOT / 'evidence/portability/float-runtime-build-20261031.json'),
        executableSha256=sha256(path), publicFunctions=8, actualWindowsReturns=len(records),
        callerBuffersAbove4GiB=buffers_above_4g, allPassed=True, cases=records,
        sourceChanges=0, sourceCredit=0, androidDeviceExecutions=0, fullWindowsGameProven=False,
        limitations=['Public C values/memory effects only, not ARM scratch registers or flags',
            'Ceiling excluded pending original-NaN arithmetic adaptation',
            'No dual-screen graphics, game assets, Android execution or full-game proof']))
    print(dict(functions=8, actualWindowsReturns=len(records), above4GiBBuffers=buffers_above_4g, allPassed=True))


if __name__ == '__main__':
    main()
