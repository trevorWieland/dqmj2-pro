import ctypes
import hashlib
import struct
from project import ROOT, read_json, sha256, write_json
from main_string_reader_native_20261030 import DATA, model, state


class Reader(ctypes.Structure):
    _fields_ = [('cursor', ctypes.c_void_p), ('eof', ctypes.c_int)]


def main():
    build = read_json(ROOT / 'evidence/portability/windows-runtime-build-20261030.json')
    assert build['compiledWindowsSubset']
    for row in build['steps']:
        if 'source' in row:
            assert sha256(ROOT / row['source']) == row['sourceSha256']
    path = ROOT / build['output']['path']
    assert sha256(path) == build['output']['sha256']
    image = path.read_bytes()
    pe = struct.unpack_from('<I', image, 0x3C)[0]
    assert image[pe:pe + 4] == b'PE' + bytes(2)
    assert struct.unpack_from('<H', image, pe + 4)[0] == 0x8664
    optional = pe + 24
    assert struct.unpack_from('<H', image, optional)[0] == 0x20B
    assert struct.unpack_from('<I', image, optional + 16)[0] == 0
    assert struct.unpack_from('<II', image, optional + 120) == (0, 0)
    library = ctypes.CDLL(str(path))
    read = library.native_main_0201d618
    read.argtypes, read.restype = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int], ctypes.c_int
    copy = library.native_main_0201d6b8
    copy.argtypes, copy.restype = [ctypes.c_void_p, ctypes.c_void_p], ctypes.c_void_p
    compare = library.native_main_0201d800
    compare.argtypes, compare.restype = [ctypes.c_void_p, ctypes.c_void_p], ctypes.c_int
    counts = {'readerCalls': 0, 'copyCalls': 0, 'compareCalls': 0, 'opaqueDefaultCalls': 0}
    digest = hashlib.sha256()

    def reader_case(byte, eof, mode, value, alignment):
        buffer = ctypes.create_string_buffer(bytes([0xA5]) * 256)
        cursor = ctypes.addressof(buffer) + 32 + alignment
        ctypes.memmove(cursor, bytes([byte]), 1)
        original = buffer.raw
        context = Reader(cursor, ctypes.c_int(eof).value)
        synthetic_context, synthetic_cursor = DATA + 0x100, DATA + 0x400 + alignment
        memory = state(synthetic_context, synthetic_cursor, eof)
        memory[synthetic_cursor - DATA] = byte
        expected, result, reads, writes = model(memory, synthetic_context, value, mode)
        returned = read(ctypes.byref(context), value, mode) & 0xFFFFFFFF
        expected_cursor, expected_eof = struct.unpack_from('<II', expected, 0x100)
        delta = ((expected_cursor - synthetic_cursor + 0x80000000) & 0xFFFFFFFF) - 0x80000000
        assert returned == result and context.eof & 0xFFFFFFFF == expected_eof
        assert context.cursor - cursor == delta and buffer.raw == original
        counts['readerCalls'] += 1
        digest.update(repr((mode, byte, eof, value, returned, expected_eof, delta)).encode())

    for byte in range(256):
        for eof in [0, 0xFFFFFFFF]:
            for mode in range(3):
                reader_case(byte, eof, mode, 0x87654321, byte & 3)
    for eof in [0, 1, 2, 0xFFFFFFFF, 0x80000000, 0x12345678]:
        for value in [0, 1, 255, 256, 0xFFFFFFFF, 0x80000000, 0x12345678]:
            for mode in range(3):
                reader_case(128, eof, mode, value, mode & 3)
    for mode in [3, 255, 0xFFFFFFFF, 0x80000000]:
        for opaque in [0, 1, 0xFFFFFFFF]:
            assert read(opaque, 0xDEADBEEF, mode) == 0
            counts['opaqueDefaultCalls'] += 1

    def strings(a, b, left, right):
        first, second = ctypes.create_string_buffer(bytes([0xA5]) * 256), ctypes.create_string_buffer(bytes([0xA5]) * 256)
        p, q = ctypes.addressof(first) + 16 + left, ctypes.addressof(second) + 16 + right
        a, b = a.split(bytes(1), 1)[0], b.split(bytes(1), 1)[0]
        ctypes.memmove(p, a + bytes(1), len(a) + 1)
        ctypes.memmove(q, b + bytes(1), len(b) + 1)
        before_first, before_second = first.raw, second.raw
        index = 0
        aa, bb = a + bytes(1), b + bytes(1)
        while aa[index] == bb[index] and aa[index] != 0:
            index += 1
        expected = aa[index] - bb[index]
        assert compare(p, q) == expected
        assert first.raw == before_first and second.raw == before_second
        counts['compareCalls'] += 1
        predicted = bytearray(before_first)
        predicted[16 + left:16 + left + len(b) + 1] = b + bytes(1)
        assert copy(p, q) == p
        assert first.raw == bytes(predicted) and second.raw == before_second
        counts['copyCalls'] += 1
        digest.update(repr((a.hex(), b.hex(), left, right, expected)).encode())

    for byte in range(256):
        for alignment in range(4):
            strings(bytes([byte]) * 5, bytes([byte ^ 128]) * 5, alignment, (alignment + 1) % 4)
            strings(bytes([byte]) * 5, bytes([byte]) * 5, alignment, alignment)
    for length in [0, 1, 2, 3, 4, 5, 7, 8, 15, 16, 31, 64]:
        for left in range(4):
            for right in range(4):
                a = bytes((index * 73 % 255 + 1) for index in range(length))
                strings(a, a, left, right)
    report = {'host': 'Windows x86_64', 'dll': build['output'], 'sources': build['sources'],
              'hostPublicCalls': counts, 'totalHostPublicCalls': sum(counts.values()),
              'allPublicResultsAndMemoryEffectsPassed': True, 'stateDigest': digest.hexdigest(),
              'peImportDirectoryEmpty': True, 'peEntryPointZero': True,
              'hostReaderLayout': {'pointerBytes': ctypes.sizeof(ctypes.c_void_p), 'eofOffset': Reader.eof.offset,
                                   'structureBytes': ctypes.sizeof(Reader)},
              'ndsReaderLayout': {'pointerBytes': 4, 'eofOffset': 4, 'structureBytes': 8},
              'sourceCreditFromHostTests': 0, 'fullWindowsGameFromSourceProven': False,
              'androidDeviceExecutions': 0,
              'limitations': ['Three isolated pure runtime routines, not an executable game or engine port',
                  'Typed host structures have host pointer layout; only normalized public state is compared',
                  'Host CPU register/flag equality to ARM is not claimed',
                  'Partially overlapping copy ranges, unbounded strings and invalid active pointers are unsupported']}
    write_json(ROOT / 'evidence/portability/windows-runtime-execution-20261030.json', report)
    print({'windowsHostCallsPassed': sum(counts.values()), 'functions': 3, 'fullGame': False, 'androidDeviceExecutions': 0})


if __name__ == '__main__':
    main()
