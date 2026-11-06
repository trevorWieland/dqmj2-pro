import hashlib
import json
import shutil
import struct
import subprocess
from project import ROOT, read_json, write_json, sha256, configuration, native_dependencies, now
from child_message_data_codec_20261106 import encode as lz_encode
from admit_child_message_storage_20261106 import namespace, NAMESPACE


def main():
    config = configuration()
    native_dependencies(config)
    import ndspy.rom
    import ndspy.lz10
    import utility_runtime
    from wave20261105_child_static_assets_next_formats import encode
    proposal_name = 'evidence/lanes/parallel-wave20261105/child-static-assets-next/proposal.json'
    assert sha256(ROOT / proposal_name) == '56439e6a3a4e2c270342d6a2d5d8e50d3fd04d5b9c5d1e0574c40417586dc7d5'
    proposal = read_json(ROOT / proposal_name)
    assert proposal['proposedAssets'] == 37 and proposal['proposedStoredBytes'] == 50456
    assert sha256(config['rom']) == config['romSha256']
    rom = ndspy.rom.NintendoDSRom(config['rom'].read_bytes())
    archive = rom.getFileByName('dwc/utility.bin')
    assert archive == utility_runtime.INPUT.read_bytes()
    layout, files = utility_runtime.derive()
    module = next(row for row in layout['modules'] if row['id'] == NAMESPACE[2])
    image = files[ROOT / module['binary']]
    assert hashlib.sha256(image).hexdigest() == module['sha256'] == 'af25c028552d9de7428f5393757507b3c029e80f22c9cc44e94e45103f0814d0'
    revision = 'e62f4358584bdfdad40f992d05c9eed7deec395b'
    protected, pins = [], []
    def add(row, parent=None):
        if (row.get('module') or (parent or {}).get('module')) != NAMESPACE[2]:
            return
        if namespace(row, parent) != NAMESPACE or not row.get('address'):
            return
        size = row.get('storedBytes', row.get('bytes', row.get('size')))
        if size:
            begin = int(row['address'], 0) if isinstance(row['address'], str) else row['address']
            protected.append((begin, begin + size))
    for name, key in [('ledger/functions.jsonl', None), ('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        raw = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(raw).hexdigest()))
        rows = [json.loads(line) for line in raw.splitlines()] if key is None else json.loads(raw)[key]
        for row in rows:
            add(row)
    def walk(node, parent):
        if isinstance(node, dict):
            context = {key: node.get(key, parent.get(key)) for key in ['program', 'processor', 'module']}
            add(node, context)
            for value in node.values():
                walk(value, context)
        elif isinstance(node, list):
            for value in node:
                walk(value, parent)
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
                   set((ROOT / 'evidence/lanes').rglob('data-claim.json')) |
                   set(ROOT.glob('cohort16*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        walk(read_json(path), {})
    for row in read_json(ROOT / 'evidence/utility/ghidra-arm9.json')['functions']:
        if row['module'] == NAMESPACE[2]:
            protected.extend((int(a, 0), int(b, 0)) for a, b in row['ranges'])
    protected.append((0x020111e8, 0x02011200))
    source_root = ROOT / 'src/utility/parallel_wave20261105/child-static-assets-next'
    assert not source_root.exists()
    rows, independent = [], []
    for asset in proposal['assets']:
        address, size = int(asset['address'], 0), asset['bytes']
        assert not any(max(address, a) < min(address + size, b) for a, b in protected)
        assert 0x02011200 <= address < address + size <= 0x02022620 and address % 4 == 0
        path = (ROOT / asset['semanticSource']['path']).resolve()
        assert path.is_relative_to(ROOT / 'work/w5sa') and sha256(path) == asset['semanticSource']['sha256']
        document = read_json(path)
        native = image[address - 0x02000000:address - 0x02000000 + size]
        decoded = ndspy.lz10.decompress(native)
        magic, bom, version, extent, header, count = struct.unpack_from('<4sHHIHH', decoded)
        assert bom == 0xfeff and version in (0x100, 0x101) and extent == len(decoded) and header == 16
        blocks, cursor = [], 16
        for unused in range(count):
            kind, length = struct.unpack_from('<4sI', decoded, cursor)
            assert length >= 8 and cursor + length <= len(decoded)
            blocks.append((kind, decoded[cursor + 8:cursor + length]))
            cursor += length
        assert cursor == len(decoded)
        semantic = document['semantic']
        assert encode(semantic) == decoded
        payload = lz_encode(decoded, document['compressionRecipe'])
        padding = (-len(payload)) % 4
        assert len(payload) == asset['encodedBytes'] and padding == asset['measuredZeroAlignmentBytes']
        assert payload + bytes(padding) == native and hashlib.sha256(native).hexdigest() == asset['targetSha256']
        units = 0
        if magic == b'RGCN':
            assert blocks[0][0] == b'RAHC'
            pixels = bytes(blocks[0][1][24:])
            values = [value for byte in pixels for value in (byte & 15, byte >> 4)]
            actual = [int(pixel, 16) for tile in semantic['tiles'] for row in tile for pixel in row]
            assert values == actual
            units = len(values)
        elif magic == b'RLCN':
            assert blocks[0][0] == b'TTLP'
            values = list(struct.iter_unpack('<H', blocks[0][1][16:]))
            actual = [c['r5'] | c['g5'] << 5 | c['b5'] << 10 | c['unusedBit15'] << 15 for c in semantic['colors']]
            assert [v[0] for v in values] == actual
            units = len(actual)
        elif magic == b'RCSN':
            assert blocks[0][0] == b'NRCS'
            values = [v[0] for v in struct.iter_unpack('<H', blocks[0][1][12:])]
            actual = [c['tile'] | int(c['horizontalFlip']) << 10 | int(c['verticalFlip']) << 11 | c['palette'] << 12
                      for row in semantic['rows'] for c in row]
            assert values == actual
            units = len(actual)
        else:
            assert magic == b'RTFN'
            raw = next(data for kind, data in blocks if kind == b'PLGC')
            width, height, cell, baseline, maximum, bpp, flags = struct.unpack_from('<BBHbBBB', raw)
            glyph = next(s for s in semantic['sections'] if s['kind'] == 'glyph-bitmap')
            assert len(raw) == 8 + cell * len(glyph['glyphs'])
            for index, bitmap in enumerate(glyph['glyphs']):
                word = int.from_bytes(raw[8 + index * cell:8 + (index + 1) * cell], 'big')
                expected = [word >> (cell * 8 - (at + 1) * bpp) & ((1 << bpp) - 1) for at in range(width * height)]
                assert expected == [int(value, 16) for line in bitmap['rows'] for value in line]
                units += len(expected)
        protected.append((address, address + size))
        independent.append(dict(address=hex(address), magic=magic.decode(), independentSemanticUnits=units,
                                decodedBytes=len(decoded), storedBytes=size, measuredZeroAlignmentBytes=padding))
        rows.append(dict(program=NAMESPACE[0], processor=NAMESPACE[1], module=NAMESPACE[2], mode='data', kind='data',
            formatKind=semantic['kind'], address=hex(address), bytes=size, encodedAssetBytes=len(payload),
            measuredZeroAlignmentBytes=padding, targetSha256=asset['targetSha256'],
            semanticSource=(source_root / f'{address:08x}.json').relative_to(ROOT).as_posix(),
            semanticSourceSha256=sha256(path), privateProposalSource=path.relative_to(ROOT).as_posix()))
    assert len(rows) == 37 and sum(row['bytes'] for row in rows) == 50456
    assert sum(row['encodedAssetBytes'] for row in rows) == 50402
    assert sum(row['measuredZeroAlignmentBytes'] for row in rows) == 54
    partition = proposal['fullFrontierPartition']
    cursor = 0x020111e8
    for interval in partition:
        assert int(interval['address'], 0) == cursor
        cursor = int(interval['endExclusive'], 0)
        assert cursor - int(interval['address'], 0) == interval['bytes']
    assert cursor == 0x02022620 and sum(row['bytes'] for row in partition) == 70712
    source_root.mkdir(parents=True)
    for row in rows:
        shutil.copyfile(ROOT / row['privateProposalSource'], ROOT / row['semanticSource'])
        assert sha256(ROOT / row['semanticSource']) == row['semanticSourceSha256']
    directory = ROOT / 'evidence/lanes/parallel-wave20261105/child-static-assets-next'
    write_json(directory / 'coordinator-review.json', dict(passed=True, sourceCredit=0, sourceRevision=revision,
        sourceRomSha256=config['romSha256'], originalContainerSha256=hashlib.sha256(archive).hexdigest(),
        originalModuleSha256=module['sha256'], originalRomToChildAutoloadVerified=True,
        independentlyCheckedAssets=independent, protectionPins=pins, protectedRangesChecked=len(protected),
        proposedInitializedBytes=50456, encodedAssetBytes=50402, measuredZeroAlignmentBytes=54,
        decodedSemanticBytes=sum(row['decodedBytes'] for row in independent),
        frontierBytes=70712, proposalSha256=sha256(ROOT / proposal_name), generatorSha256=sha256(__file__)))
    write_json(directory / 'data-claim.json', dict(status='coordinator-admitted-initialized-storage-no-credit',
        owner='repo_audit', sourceRevision=revision, createdUtc=now(), claimedStorage=rows, functionCount=0,
        functionOwnershipGranted=False, sourceCredit=0, exclusiveSourceRoot=source_root.relative_to(ROOT).as_posix()))
    print(dict(passed=True, storageObjects=37, initializedBytes=50456, sourceCredit=0,
               claimSha256=sha256(directory / 'data-claim.json')))


if __name__ == '__main__':
    main()
