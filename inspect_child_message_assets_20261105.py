import copy
import hashlib
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256


def unpack_tokens(raw):
    assert raw[0] == 0x10
    size = int.from_bytes(raw[1:4], 'little')
    cursor, decoded, groups = 4, bytearray(), []
    while len(decoded) < size:
        flags = raw[cursor]
        cursor += 1
        tokens = []
        for bit in range(7, -1, -1):
            if len(decoded) == size:
                assert flags & ((1 << (bit + 1)) - 1) == 0
                break
            if flags & (1 << bit):
                word = int.from_bytes(raw[cursor:cursor + 2], 'big')
                cursor += 2
                length, distance = (word >> 12) + 3, (word & 4095) + 1
                assert distance <= len(decoded) and len(decoded) + length <= size
                for unused in range(length):
                    decoded.append(decoded[-distance])
                tokens.append([length, distance])
            else:
                decoded.append(raw[cursor])
                cursor += 1
                tokens.append(None)
        groups.append(tokens)
    return bytes(decoded), groups, cursor


def encode_with_recipe(decoded, groups):
    output = bytearray(b'\x10' + len(decoded).to_bytes(3, 'little'))
    cursor = 0
    for index, tokens in enumerate(groups):
        assert 1 <= len(tokens) <= 8 and (len(tokens) == 8 or index == len(groups) - 1)
        flags = sum((1 << (7 - bit)) for bit, token in enumerate(tokens) if token is not None)
        output.append(flags)
        for token in tokens:
            if token is None:
                assert cursor < len(decoded)
                output.append(decoded[cursor])
                cursor += 1
            else:
                length, distance = token
                assert 3 <= length <= 18 and 1 <= distance <= min(4096, cursor)
                assert cursor + length <= len(decoded)
                assert all(decoded[cursor + i] == decoded[cursor + i - distance] for i in range(length))
                output.extend((((length - 3) << 12) | (distance - 1)).to_bytes(2, 'big'))
                cursor += length
    assert cursor == len(decoded)
    return bytes(output)


def semantic_source(obj):
    assert not obj.instructions and not obj.labels and not obj.scripts
    messages = []
    for message in obj.messages:
        assert all(isinstance(part, str) for part in message.stringParts)
        messages.append(dict(info=list(message.info), stringParts=message.stringParts, isNull=message.isNull))
    return dict(id=obj.id, encoding=obj.encoding, endianness=obj.endianness,
        unk14=obj.unk14, unk18=obj.unk18, unk1C=obj.unk1C, messages=messages)


def from_source(source, bmg):
    obj = bmg.BMG(id=source['id'])
    for key in ['encoding', 'endianness', 'unk14', 'unk18', 'unk1C']:
        setattr(obj, key, source[key])
    obj.messages = [bmg.Message(bytes(row['info']), list(row['stringParts']), row['isNull'])
        for row in source['messages']]
    return obj.save()


def main():
    native_dependencies(configuration())
    import ndspy.bmg as bmg
    import ndspy.lz10 as lz10
    profile = read_json(ROOT / 'evidence/verification/source95-frontier-byte-profiles-20261105.json')['regions'][0]
    assert profile['module'] == 'utility-child-arm9-main'
    path = ROOT / profile['binary']
    assert sha256(path) == profile['binarySha256']
    data = path.read_bytes()
    start, end = int(profile['address'], 0) - 0x02000000, int(profile['endExclusive'], 0) - 0x02000000
    folder = ROOT / 'evidence/lanes/parallel-wave20261105/source95-data-inspection'
    folder.mkdir(exist_ok=True, parents=True)
    assets, controls = [], []
    for magic in range(start, end - 8):
        if data[magic:magic + 8] != b'MESGbmg1':
            continue
        offset = magic - 5
        assert offset >= start and data[offset] == 0x10
        decoded, recipe, consumed = unpack_tokens(data[offset:end])
        assert decoded == lz10.decompress(data[offset:end])
        obj = bmg.BMG(decoded)
        source = semantic_source(obj)
        rebuilt = from_source(source, bmg)
        assert rebuilt == decoded
        encoded = encode_with_recipe(rebuilt, recipe)
        assert encoded == data[offset:offset + consumed]
        ordinary = lz10.compress(rebuilt)
        wrong_source = copy.deepcopy(source)
        message = next(row for row in wrong_source['messages'] if row['stringParts'])
        message['stringParts'][0] += 'x'
        try:
            different = encode_with_recipe(from_source(wrong_source, bmg), recipe)
        except (AssertionError, IndexError):
            rejected = True
        else:
            rejected = different != encoded
        assert rejected
        wrong_recipe = copy.deepcopy(recipe)
        token = next(token for group in wrong_recipe for token in group if token is not None)
        token[1] = 4097
        try:
            encode_with_recipe(rebuilt, wrong_recipe)
        except AssertionError:
            pass
        else:
            raise AssertionError('Out-of-range LZ reference accepted')
        name = f'child-message-{offset + 0x02000000:08x}.json'
        target = folder / name
        write_json(target, dict(sourceCredit=0, inspectionOnly=True,
            source=source, compressionRecipe=recipe, originalCompression='Nintendo LZ10 token choices',
            compressionRecipeContainsOriginalLiteralBytes=False))
        reread = read_json(target)
        assert encode_with_recipe(from_source(reread['source'], bmg), reread['compressionRecipe']) == encoded
        assets.append(dict(program='dwc/utility.bin/move/child.srl', processor='arm9', module=profile['module'],
            address=hex(0x02000000 + offset), bytes=consumed, decodedBytes=len(decoded),
            sourcePath=target.relative_to(ROOT).as_posix(), sourceSha256=sha256(target),
            originalEncodedSha256=hashlib.sha256(encoded).hexdigest(), decodedSha256=hashlib.sha256(decoded).hexdigest(),
            messages=len(source['messages']), semanticBmgRebuildExact=True, originalLzChoicesRebuildExact=True,
            defaultLzCompressorExact=ordinary == encoded, boundaryPaddingClaimed=0,
            executableScriptRecords=0, sourceOwnershipGranted=False))
        controls.append(dict(address=hex(0x02000000 + offset), alteredMessageNotOriginal=True, invalidDistanceRejected=True))
    assert len(assets) == 8 and sum(row['messages'] for row in assets) == 48
    assert sha256(path) == profile['binarySha256']
    report = folder / 'semantic-roundtrip.json'
    write_json(report, dict(passed=True, sourceCredit=0, sharedSourceRegistryChanged=False,
        generatorSha256=sha256(__file__), originalModule=dict(path=profile['binary'], sha256=profile['binarySha256']),
        assets=assets, controls=controls, encodedBytes=sum(row['bytes'] for row in assets),
        decodedBytes=sum(row['decodedBytes'] for row in assets),
        limitations=['Read-only semantic asset decomposition and byte-exact data-encoding proof; not accepted source.',
            'The containing region also starts with executable Thumb code, which is excluded from these eight asset slices.',
            'No raw executable bytes or opaque binary payloads are copied into the semantic source.',
            'Storage/ownership protection audit, source-defined data compilation/linkage and full acceptance remain required.',
            'No source-only ROM or native Windows game execution is established.']))
    print(dict(passed=True, assets=len(assets), messages=48, encodedBytes=sum(row['bytes'] for row in assets),
        decodedBytes=sum(row['decodedBytes'] for row in assets), sourceCredit=0))


if __name__ == '__main__':
    main()
