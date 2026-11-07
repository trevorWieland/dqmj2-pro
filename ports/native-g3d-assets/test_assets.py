import argparse
import ctypes as c
import hashlib
import json
from pathlib import Path
import struct
from assets_api import bind, Binding, Entry, Mapping, Scope
from synthetic_assets import half, word, image, known_pixels, model_set, texture


def output_buffer():
    raw = (c.c_ubyte * 258)(*([0xa5] * 258))
    return raw, c.addressof(raw) + 1


def pipeline(lib, path, models, banks, action):
    payload, files = image(models, banks)
    path.write_bytes(payload)
    scope, mapping, contexts, blocks, heaps = Scope(0, 9, 1, 1), Mapping(lib), [], [], []
    mount = lib.j2p_nitrofs_mount(str(path.resolve()).encode('utf-8'), len(payload), scope)
    assert mount
    try:
        mapping.add(0x020e5500, bytes([0xa5]) * 0x120)
        for i, name in enumerate((b'rom:/model.bin\0', b'rom:/bank-a.bin\0', b'rom:/bank-b.bin\0')):
            mapping.add(0x02600000 + i * 0x1000, name)
        for i, blob in enumerate(files):
            base = 0x02700800 + i * 0x100000
            capacity = (len(blob) + 3) & ~3
            heaps.append(mapping.add(base, bytes([0xa5]) * capacity))
            context = lib.j2p_nitrofs_resource_create(mount, c.byref(mapping.space), scope, 3, base, capacity)
            assert context
            contexts.append((context, base))
            assert lib.j2p_resource_load(context, 0x02600000 + i * 0x1000, 0xffffffff, 0) == base
            block, length = c.c_uint32(), c.c_uint32()
            assert lib.j2p_g3d_file_block(c.byref(mapping.space), scope, base, len(blob), 1 if not i else 0,
                c.byref(block), c.byref(length)) == 1
            assert (block.value, length.value) == (base + 20, len(blob) - 20)
            blocks.append((block.value, length.value))
        before = [bytes(item) for item in heaps]
        action(mapping, blocks, heaps)
        assert before == [bytes(item) for item in heaps]
        mapping.guards()
        for (context, base), blob, heap in zip(contexts, files, heaps):
            assert bytes(heap[1:len(blob) + 1]) == blob
            assert lib.j2p_resource_release(context, base) == 1
        assert path.read_bytes() == payload
    finally:
        for context, unused in contexts:
            lib.j2p_resource_destroy(context)
        lib.j2p_nitrofs_unmount(mount)
    return payload


def run_case(lib, path, count, fmt, alpha, digest):
    models, expected = model_set(count)
    banks = [texture(count, fmt, bank, alpha) for bank in (0, 1)]
    def action(mapping, blocks, unused):
        for bank in (0, 1):
            for mi, mat, ti, pi in expected:
                args = [c.byref(mapping.space), mapping.scope, *blocks[0], *blocks[1 + bank], mi, mat]
                binding, width, height = Binding(), c.c_uint32(), c.c_uint32()
                assert lib.j2p_g3d_model_material_binding(*args, c.byref(binding)) == 1
                assert (binding.texture_index, binding.palette_index, binding.material_count) == (ti, pi, count)
                raw, pointer = output_buffer()
                assert lib.j2p_g3d_assets_rgba(*args, pointer, 256, c.byref(width), c.byref(height)) == 1
                assert (width.value, height.value) == (8, 8)
                pixels = bytes(raw[1:-1])
                assert pixels == known_pixels(fmt, ti, pi, bank, alpha)
                assert raw[0] == 0xa5 and raw[-1] == 0xa5
                digest.update(pixels)
    pipeline(lib, path, models, banks, action)
    return len(expected) * 2


def refusals(lib, path):
    models, unused = model_set(3)
    banks, records = [texture(3, 5, bank, 1) for bank in (0, 1)], []
    def action(mapping, blocks, heaps):
        model_raw, texture_raw = heaps[0], heaps[1]
        originals = [bytes(item) for item in heaps]
        def reject(label, expected=-1, scope=None, model_bytes=None, material=0, model=0, capacity=256, pointer=None):
            raw, default_pointer = output_buffer()
            width, height = c.c_uint32(17), c.c_uint32(29)
            before = [bytes(item) for item in heaps]
            args = [c.byref(mapping.space), scope or mapping.scope, blocks[0][0],
                blocks[0][1] if model_bytes is None else model_bytes, *blocks[1], model, material]
            status = lib.j2p_g3d_assets_rgba(*args, default_pointer if pointer is None else pointer,
                capacity, c.byref(width), c.byref(height))
            assert status == expected, (label, status, expected)
            assert not width.value and not height.value and bytes(raw) == bytes([0xa5]) * len(raw)
            assert before == [bytes(item) for item in heaps]
            records.append(label)
        for field, value in (('program', 1), ('processor', 7), ('module', 2), ('generation', 0), ('generation', 2)):
            scope = Scope(0, 9, 1, 1)
            setattr(scope, field, value)
            reject('namespace-' + field + '-' + str(value), scope=scope)
        reject('short-model-span', model_bytes=19)
        reject('unmapped-model-tail', model_bytes=blocks[0][1] + 100)
        reject('model-index-absent', model=2, expected=0)
        reject('material-index-absent', material=3, expected=0)
        reject('output-capacity-short', capacity=255)
        reject('output-overlaps-model', pointer=c.addressof(model_raw) + 1)
        reject('output-overlaps-texture', pointer=c.addressof(texture_raw) + 1)
        dict_entry = 8 + half(models, 14)
        mdl = word(models, dict_entry + 4)
        mat = mdl + word(models, mdl + 8)
        tex_dict, pal_dict = mat + half(models, mat), mat + half(models, mat + 2)
        te, pe = tex_dict + half(models, tex_dict + 6), pal_dict + half(models, pal_dict + 6)
        first_tex, first_pal = te + 4, pe + 4
        model_changes = [('model-signature', 0, '<I', 0), ('model-total-overflow', 4, '<I', 0xffffffff),
            ('model-size-overflow', mdl, '<I', 0xffffffff), ('material-offset-overflow', mdl + 8, '<I', 0xffffffff),
            ('texture-list-offset', mat, '<H', 65535), ('palette-list-offset', mat + 2, '<H', 65535),
            ('texture-index-overflow', mat + half(models, first_tex), '<B', 255),
            ('palette-index-overflow', mat + half(models, first_pal), '<B', 255)]
        for label, offset, kind, value in model_changes:
            struct.pack_into(kind, model_raw, 21 + offset, value)
            reject(label)
            c.memmove(c.addressof(model_raw), originals[0], len(model_raw))
        for label, offset in (('duplicate-texture-binding', mat + half(models, first_tex)),
                ('duplicate-palette-binding', mat + half(models, first_pal))):
            model_raw[21 + offset] = 0
            reject(label, expected=-3)
            c.memmove(c.addressof(model_raw), originals[0], len(model_raw))
        for label, offset, kind, value, status in (
            ('texture-total-overflow', 4, '<I', 0xffffffff, -1),
            ('texture-primary-overflow', 36, '<I', 0xfffffff0, -1),
            ('texture-secondary-overflow', 40, '<I', 0xfffffff0, -1),
            ('palette-region-overflow', 56, '<I', 0xfffffff0, -1),
            ('missing-palette-dictionary', 52, '<H', 0, 0)):
            struct.pack_into(kind, texture_raw, 21 + offset, value)
            reject(label, expected=status)
            c.memmove(c.addressof(texture_raw), originals[1], len(texture_raw))
        entry = half(banks[0], 14) + half(banks[0], half(banks[0], 14) + 6) + 4
        struct.pack_into('<I', texture_raw, 21 + entry + 8, 2 << 26)
        reject('unsupported-format', expected=-2)
        c.memmove(c.addressof(texture_raw), originals[1], len(texture_raw))
    payload = pipeline(lib, path, models, banks, action)
    for offset, value in ((0x40, 0xfffffff0), (0x48, 0xfffffff0)):
        broken = bytearray(payload)
        struct.pack_into('<I', broken, offset, value)
        altered = path.with_name('malformed-' + str(offset) + '.nds')
        altered.write_bytes(broken)
        assert not lib.j2p_nitrofs_mount(str(altered.resolve()).encode('utf-8'), len(broken), Scope(0, 9, 1, 1))
        records.append('filesystem-table-overflow-' + str(offset))
    return records


def main():
    if not __debug__:
        raise SystemExit('Run contract tests without Python optimization')
    parser = argparse.ArgumentParser()
    parser.add_argument('--library', type=Path, required=True)
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    args.work.mkdir(parents=True, exist_ok=True)
    lib, digest, materials, images = bind(args.library), hashlib.sha256(), 0, 0
    path = args.work / 'synthetic-assets-龍.nds'
    for count in (1, 3, 16, 31):
        for fmt in (3, 4, 5):
            for alpha in (0, 1):
                materials += run_case(lib, path, count, fmt, alpha, digest)
                images += 1
    rejected = refusals(lib, path)
    report = dict(status='synthetic-filesystem-to-canonical-rgba-chain-passed', syntheticImages=images,
        resourceLoads=images * 3 + 3, canonicalMaterialDecodes=materials, explicitDistinctBanks=2,
        decodedPixels=materials * 64, formats=[3, 4, 5], compressedModes=[0, 1, 2, 3], rejectedInputs=rejected,
        outputSha256=digest.hexdigest(), librarySha256=hashlib.sha256(args.library.read_bytes()).hexdigest(),
        originalGameInputsUsed=False, originalOracleExecuted=False, downloadedAssetsUsed=False,
        noPartialWritesVerified=True, rendererExecuted=False, deviceExecuted=False, wholeGameExecuted=False,
        matchingCredit=0, sourceCredit=0)
    (args.work / 'result.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
