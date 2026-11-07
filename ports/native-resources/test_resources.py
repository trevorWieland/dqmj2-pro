import argparse
import ctypes as c
import hashlib
import json
from pathlib import Path
import struct
from resource_api import bind, Entry, Mapping, Scope
from synthetic_resources import image, material_result, texture


def run_case(lib, path, count, format_code, variant, digest):
    blob, keys, tex_values, palette_values, entry_offset, names_offset = texture(count, format_code, variant)
    payload, ranges, root_data = image(blob)
    path.write_bytes(payload)
    scope, entry = Scope(0, 9, 1, 1), Entry()
    mount = lib.j2p_nitrofs_mount(str(path.resolve()).encode('utf-8'), len(payload), scope)
    assert mount
    try:
        assert [lib.j2p_nitrofs_metric(mount, i) for i in range(3)] == [2, 5, 3]
        for index, (start, end) in enumerate(ranges):
            assert lib.j2p_nitrofs_file_id(mount, scope, index, c.byref(entry)) == 1
            assert (entry.id, entry.start, entry.bytes) == (index, start, end - start)
        for name, index in ((b'rom:/root.bin', 2), (b'rom:/empty', 3), (b'rom:/data/material.bin', 4),
                            (b'ROM:/DATA/MATERIAL.BIN', 4), (b'rom:\\data\\material.bin', 4),
                            (b'rom:/data/../root.bin', 2), (b'rom:/./data/material.bin', 4)):
            assert lib.j2p_nitrofs_lookup(mount, scope, name, c.byref(entry)) == 1 and entry.id == index
        chosen = (0, count // 2, count - 1)[variant]
        seed = count * 17 + format_code * 3 + variant
        initial = bytearray((i * 17 + seed) & 255 for i in range(56))
        struct.pack_into('<I', initial, 16, 0xc00f0000 | (seed & 0xffff))
        key_values = (0x91be0000, 0xdeadffff, 0x12341234)
        expected_texture, expected_palette = material_result(initial, tex_values[chosen], palette_values[chosen],
            (key_values[variant], key_values[(variant + 1) % 3], key_values[variant]))
        for selector in (0, 1):
            mapping = Mapping(lib)
            backend = mapping.add(0x020e5500, bytes([0xa5]) * 0x120)
            heap = mapping.add(0x02510800, bytes([0xa5]) * 16384)
            mapping.add(0x02510000, b'rom:/data/material.bin\0')
            mapping.add(0x02600000, keys[chosen])
            material = mapping.add(0x02601000, initial)
            context = lib.j2p_nitrofs_resource_create(mount, c.byref(mapping.space), scope, 3, 0x02510800, 16384)
            assert context
            try:
                loaded = lib.j2p_resource_load(context, 0x02510000, 0xffffffff, selector)
                offset = 0 if not selector else 16384 - ((len(blob) + 3) & ~3)
                assert loaded == 0x02510800 + offset
                expected_heap = bytearray([0xa5]) * 16384
                expected_heap[offset:offset + len(blob)] = blob
                assert bytes(heap[1:-1]) == expected_heap
                assert struct.unpack_from('<3I', bytes(backend), 1 + 0x1c) == (ranges[4][1], loaded + len(blob), 0)
                assert [lib.j2p_resource_metric(context, i) for i in range(6)] == [0, 0, 1, 1, 0, 1]
                query = loaded + names_offset + chosen * 16 if selector else 0x02600000
                assert lib.j2p_g3d_dict_data(c.byref(mapping.space), scope, loaded + 60, query) == loaded + entry_offset + chosen * 8
                assert lib.j2p_g3d_dict_index(c.byref(mapping.space), scope, loaded + 60, query) == chosen
                assert lib.j2p_g3d_material_texture(c.byref(mapping.space), scope, loaded, query, 0x02601000) == 1
                assert bytes(material[1:-1]) == expected_texture
                assert lib.j2p_g3d_material_palette(c.byref(mapping.space), scope, loaded, query, 0x02601000) == 1
                assert bytes(material[1:-1]) == expected_palette and bytes(heap[1:-1]) == expected_heap
                digest.update(bytes(material[1:-1]) + bytes(backend[1:-1]))
                assert lib.j2p_resource_release(context, loaded) == 1
                assert lib.j2p_resource_release(context, loaded) == 0
                assert lib.j2p_resource_metric(context, 2) == 0
            finally:
                lib.j2p_resource_destroy(context)
            mapping.guards()
        mapping = Mapping(lib)
        mapping.add(0x020e5500, bytes([0xa5]) * 0x120)
        output = mapping.add(0x02510800, bytes([0xa5]) * 1024)
        assert lib.j2p_nitrofs_read(mount, scope, 2, 0, c.byref(mapping.space), 0x02510800, 513) == 1
        assert bytes(output[1:514]) == root_data and bytes(output[514:-1]) == bytes([0xa5]) * 511
        mapping.guards()
        assert lib.j2p_nitrofs_metric(mount, 4) > 0
    finally:
        lib.j2p_nitrofs_unmount(mount)
    assert path.read_bytes() == payload
    return payload


def refusals(lib, path, payload):
    scope, entry, count = Scope(0, 9, 1, 1), Entry(17, 23, 31), 0
    mount = lib.j2p_nitrofs_mount(str(path.resolve()).encode('utf-8'), len(payload), scope)
    assert mount
    try:
        for invalid in (Scope(1, 9, 1, 1), Scope(0, 7, 1, 1), Scope(0, 9, 2, 1), Scope(0, 9, 1, 2)):
            before = bytes(entry)
            assert lib.j2p_nitrofs_lookup(mount, invalid, b'rom:/root.bin', c.byref(entry)) == -1
            assert bytes(entry) == before
            count += 1
        for name, status in ((b'', -1), (b'a' * 256, -1), (b'rom:/absent', 0),
                             (b'sav:/root.bin', 0), (b'rom://root.bin', 0), (b'rom:/data', 0)):
            before = bytes(entry)
            assert lib.j2p_nitrofs_lookup(mount, scope, name, c.byref(entry)) == status and bytes(entry) == before
            count += 1
        mapping = Mapping(lib)
        backend = mapping.add(0x020e5500, bytes([0xa5]) * 0x120)
        heap = mapping.add(0x02510800, bytes([0xa5]) * 16384)
        for file_id, offset, destination, length in ((2, 513, 0x02510800, 1), (0xffffffff, 0, 0x02510800, 1),
                                                   (2, 0, 0xfffffff0, 1)):
            before = bytes(backend), bytes(heap)
            assert lib.j2p_nitrofs_read(mount, scope, file_id, offset, c.byref(mapping.space), destination, length) == 0
            assert (bytes(backend), bytes(heap)) == before
            count += 1
        for name, error in ((b'rom:/empty\0', 3), (b'rom:/absent\0', 1)):
            child = Mapping(lib)
            child.add(0x020e5500, bytes([0xa5]) * 0x120)
            target = child.add(0x02510800, bytes([0xa5]) * 64)
            child.add(0x02510000, name)
            context = lib.j2p_nitrofs_resource_create(mount, c.byref(child.space), scope, 3, 0x02510800, 64)
            assert context
            try:
                assert lib.j2p_resource_load(context, 0x02510000, 3, 0) == 0
                assert lib.j2p_resource_metric(context, 0) == error and lib.j2p_resource_metric(context, 2) == 0
                assert bytes(target[1:-1]) == bytes([0xa5]) * 64
            finally:
                lib.j2p_resource_destroy(context)
            child.guards()
            count += 1
        mapping.guards()
    finally:
        lib.j2p_nitrofs_unmount(mount)
    for size in (len(payload) - 1, len(payload) + 1):
        assert not lib.j2p_nitrofs_mount(str(path.resolve()).encode('utf-8'), size, scope)
        count += 1
    assert not lib.j2p_nitrofs_mount(str(path.resolve()).encode('utf-8'), len(payload), Scope(0, 9, 1, 0))
    return count + 1


def malformed(lib, work, payload):
    fnt, fnt_size, fat, fat_size = struct.unpack_from('<4I', payload, 0x40)
    subtable = struct.unpack_from('<I', payload, fnt)[0]
    changes = [(0x40, struct.pack('<I', 0xfffffff0)), (0x48, struct.pack('<I', 0xfffffff0)),
               (0x4c, struct.pack('<I', fat_size - 1)), (fnt + 6, bytes(2)),
               (fnt + 6, struct.pack('<H', 4097)), (fnt, struct.pack('<I', 1)),
               (fnt, struct.pack('<I', fnt_size)), (fnt + 14, struct.pack('<H', 0xf001)),
               (fat + 20, struct.pack('<I', len(payload) + 1)), (fat + 16, struct.pack('<I', len(payload))),
               (fnt + subtable, b'\x7f'), (fnt + subtable + 1, bytes(1))]
    for i, (offset, value) in enumerate(changes):
        data = bytearray(payload)
        data[offset:offset + len(value)] = value
        path = work / f'malformed-{i}.nds'
        path.write_bytes(data)
        assert not lib.j2p_nitrofs_mount(str(path.resolve()).encode('utf-8'), len(data), Scope(0, 9, 1, 1))
    return len(changes)


def main():
    if not __debug__:
        raise SystemExit('Run synthetic contract checks without Python optimization')
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    lib, digest, cases = bind(args.library), hashlib.sha256(), 0
    path = args.work / 'synthetic-resource-龍.nds'
    for count in (1, 2, 15, 16, 31, 255):
        for format_code in range(8):
            for variant in range(3):
                payload = run_case(lib, path, count, format_code, variant, digest)
                cases += 1
    policies = refusals(lib, path, payload)
    malformed_count = malformed(lib, args.work, payload)
    result = dict(status='synthetic-resource-contract-passed', syntheticImages=cases, resourceLoads=cases * 2,
                  dictionaryQueries=cases * 4, unchangedTexturePaletteCalls=cases * 4, directPayloadReads=cases,
                  rejectedPolicyCases=policies, malformedImagesRejected=malformed_count,
                  outputSha256=digest.hexdigest(), librarySha256=hashlib.sha256(args.library.read_bytes()).hexdigest(),
                  originalGameInputsUsed=False, originalOracleExecuted=False, originalInstructionPayloads=False,
                  rendered=False, deviceExecuted=False, fullGameExecutionProven=False, matchingCredit=0, sourceCredit=0)
    (args.work / 'result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
