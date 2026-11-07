import argparse
import ctypes as c
import hashlib
import json
from pathlib import Path
import struct


class Scope(c.Structure):
    _fields_ = [(name, c.c_uint32) for name in ('program', 'processor', 'module', 'generation')]


class Region(c.Structure):
    _fields_ = [('scope', Scope), ('base', c.c_uint32), ('length', c.c_uint32), ('bytes', c.c_void_p)]


class Space(c.Structure):
    _fields_ = [('count', c.c_uint32), ('regions', Region * 16)]


READ = c.CFUNCTYPE(c.c_int, c.c_void_p, c.c_uint32, c.POINTER(c.c_ubyte), c.c_uint32)


def bind(path):
    lib = c.CDLL(str(path.resolve()))
    lib.j2p_guest_map.argtypes = [c.POINTER(Space), Scope, c.c_uint32, c.c_void_p, c.c_uint32]
    lib.j2p_guest_map.restype = c.c_int
    lib.j2p_card_read_polling.argtypes = [c.POINTER(Space), Scope, c.c_void_p, READ, c.c_void_p, c.c_uint32]
    lib.j2p_card_read_polling.restype = c.c_int
    lib.j2p_readonly_open.argtypes = [c.c_char_p]
    lib.j2p_readonly_open.restype = c.c_void_p
    lib.j2p_readonly_close.argtypes = [c.c_void_p]
    lib.j2p_readonly_close.restype = c.c_int
    return lib, READ(('j2p_readonly_read_at', lib))


def buffer(value):
    return (c.c_ubyte * len(value)).from_buffer_copy(value)


def fixture(lib, source, destination, length, mapped=True):
    backend = bytearray(b'\xa5' * 0x120)
    cache = bytearray(b'\x7a' * 0x220)
    struct.pack_into('<3I', backend, 0x1c, source, 0x02302000 + destination, length)
    struct.pack_into('<I', cache, 8, 0xffffffff)
    backend, cache, output = buffer(backend), buffer(cache), buffer(b'\xb6' * 8192)
    scope, space = Scope(0, 9, 1, 1), Space()
    assert lib.j2p_guest_map(c.byref(space), scope, 0x020e5500, backend, len(backend)) == 1
    if mapped:
        assert lib.j2p_guest_map(c.byref(space), scope, 0x02302000, output, len(output)) == 1
    return scope, space, backend, cache, output


def state(backend, cache, output):
    return bytes(backend), bytes(cache), bytes(output)


def run(lib, reader, image_path, image):
    file = lib.j2p_readonly_open(str(image_path.resolve()).encode('utf-8'))
    assert file
    positive, negative = 0, 0
    try:
        for offset in (0, 1, 255, 511):
            for length in (0, 1, 511, 512, 513, 1024, 1536):
                for destination in (0, 1, 3):
                    source = positive % 3 * 512 + offset
                    scope, space, backend, cache, output = fixture(lib, source, destination, length)
                    before_backend, before_cache, before_output = state(backend, cache, output)
                    result = lib.j2p_card_read_polling(c.byref(space), scope, cache, reader, file, 16)
                    assert result == 0
                    expected_output = bytearray(before_output)
                    expected_output[destination:destination + length] = image[source:source + length]
                    expected_backend = bytearray(before_backend)
                    struct.pack_into('<3I', expected_backend, 0x1c,
                                     source + length, 0x02302000 + destination + length, 0)
                    assert bytes(output) == bytes(expected_output)
                    assert bytes(backend) == bytes(expected_backend)
                    after_cache = bytes(cache)
                    assert after_cache[:8] == before_cache[:8]
                    assert after_cache[12:32] == before_cache[12:32]
                    base = struct.unpack_from('<I', after_cache, 8)[0]
                    if base == 0xffffffff:
                        assert after_cache == before_cache
                    else:
                        assert base % 512 == 0 and base + 512 <= len(image)
                        assert after_cache[32:] == image[base:base + 512]
                    positive += 1
        for kind in ('stale-scope', 'unmapped', 'zero-budget'):
            scope, space, backend, cache, output = fixture(lib, 1, 1, 513, mapped=kind != 'unmapped')
            before = state(backend, cache, output)
            if kind == 'stale-scope':
                scope.generation += 1
            result = lib.j2p_card_read_polling(c.byref(space), scope, cache, reader, file,
                                              0 if kind == 'zero-budget' else 16)
            assert result < 0 and state(backend, cache, output) == before
            negative += 1
    finally:
        assert lib.j2p_readonly_close(file) == 1
    short_path = image_path.with_name('synthetic-short-card.bin')
    short_path.write_bytes(image[:128])
    file = lib.j2p_readonly_open(str(short_path.resolve()).encode('utf-8'))
    assert file
    try:
        scope, space, backend, cache, output = fixture(lib, 0, 0, 1)
        before = state(backend, cache, output)
        assert lib.j2p_card_read_polling(c.byref(space), scope, cache, reader, file, 16) == -3
        assert state(backend, cache, output) == before
        negative += 1
    finally:
        assert lib.j2p_readonly_close(file) == 1
    return dict(syntheticReadCases=positive, rejectedPolicyCases=negative,
                originalGameInputsUsed=False, originalOracleExecuted=False,
                fullGameExecutionProven=False)


def main():
    if not __debug__:
        raise SystemExit('Run synthetic contract checks without Python optimization')
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    image = bytes((i * 37 + i // 16 + 17) & 255 for i in range(16384))
    image_path = args.work / 'synthetic-card-source-龍.bin'
    image_path.write_bytes(image)
    lib, reader = bind(args.library)
    result = run(lib, reader, image_path, image)
    assert image_path.read_bytes() == image
    result.update(status='synthetic-storage-contract-passed',
                  imageSha256=hashlib.sha256(image).hexdigest(),
                  librarySha256=hashlib.sha256(args.library.read_bytes()).hexdigest())
    (args.work / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
