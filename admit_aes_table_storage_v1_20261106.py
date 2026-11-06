import hashlib
import re
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256, now
from initialized_storage_protection_v3_20261106 import protected


def multiply(a, b):
    result = 0
    for _ in range(8):
        if b & 1:
            result ^= a
        a = ((a << 1) ^ (0x11b if a & 0x80 else 0)) & 255
        b >>= 1
    return result


def power(a, n):
    result = 1
    while n:
        if n & 1:
            result = multiply(result, a)
        a = multiply(a, a)
        n >>= 1
    return result


def tables():
    forward = []
    for x in range(256):
        inv = power(x, 254) if x else 0
        y = inv ^ 0x63
        for rotation in [1, 2, 3, 4]:
            y ^= ((inv << rotation) | (inv >> (8 - rotation))) & 255
        forward.append(y)
    inverse = [0] * 256
    assert len(set(forward)) == 256 and forward[0] == 0x63 and forward[0x53] == 0xed
    for x, y in enumerate(forward):
        inverse[y] = x
    result = {}
    for prefix, substitution, coefficients in [('Te', forward, [2, 1, 1, 3]), ('Td', inverse, [14, 9, 13, 11])]:
        for index in range(5):
            words = []
            for value in substitution:
                if index == 4:
                    word = value * 0x01010101
                else:
                    word = 0
                    for coefficient in coefficients:
                        word = (word << 8) | multiply(value, coefficient)
                    shift = index * 8
                    if shift:
                        word = ((word >> shift) | (word << (32 - shift))) & 0xffffffff
                words.append(word)
            result[prefix + str(index)] = words
    return result


def primary_tables(text):
    result = {}
    for match in re.finditer(r'static\s+const\s+uint32_t\s+(T[ed][0-4])\s*\[\s*256\s*\]\s*=\s*\{(.*?)\}\s*;', text, re.S):
        body = re.sub(r'/\*.*?\*/|//[^\n]*', '', match[2], flags=re.S)
        values = [int(value, 16) for value in re.findall(r'0x[0-9a-fA-F]+', body)]
        assert len(values) == 256 and match[1] not in result
        assert not re.sub(r'0x[0-9a-fA-F]+[uUlL]*|[\s,]', '', body)
        result[match[1]] = values
    assert len(result) == 10
    return result


def main():
    name = 'evidence/lanes/parallel-wave20261106/structured-table-read-only/aes-proposal.json'
    assert sha256(ROOT / name) == 'a649e466e7b51b92eae374e1eb8d2eac6b62b384cf6123ee4ace4b86ed6b4c63'
    proposal = read_json(ROOT / name)
    snapshot_name = 'evidence/lanes/parallel-wave20261106/structured-table-read-only/aes-primary-snapshot.json'
    assert sha256(ROOT / snapshot_name) == '0e7ece85950fbee41d4b181f63084c4dc5b0b5e9fb273af2a94b83319480da5d'
    assert proposal['sourceRevision'] == 'fcd3d2bad860d0e83b6de21c8bfb24f7d02f8bb8'
    assert proposal['sourceCredit'] == proposal['dataCredit'] == proposal['functionCredit'] == 0
    assert len(proposal['objects']) == 10 and sum(r['bytes'] for r in proposal['objects']) == 10240
    primary = ROOT / 'work/w6ac/scout/heimdal-rijndael-alg-fst.c'
    header = primary.with_suffix('.h')
    assert sha256(primary) == 'abb323462fa6202fee8e0f1a46c8911cb75eb08422cf730fd2eba5de5f7220e4'
    assert sha256(header) == '7983930d42b99673cdf159df4ca0206fa0d487a1934dac6b6b8c98ae4dc2407a'
    generated = tables()
    declared = primary_tables(primary.read_text(encoding='utf-8-sig'))
    assert generated == declared
    cfg = configuration(); native_dependencies(cfg)
    assert sha256(cfg['rom']) == cfg['romSha256'] == '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    import ndspy.rom
    rom = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes())
    overlay = rom.loadArm9Overlays([6])[6]
    image, base = bytes(overlay.data), overlay.ramAddress
    manifest = read_json(ROOT / 'manifest.json')
    module = next(m for m in manifest['modules'] if m['name'] == 'ov006')
    assert base == int(module['base'], 0) and len(image) == module['bytes']
    assert image == (ROOT / module['binary']).read_bytes()
    assert hashlib.sha256(image).hexdigest() == module['sha256'] == 'fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341'
    symbols = set((ROOT / 'config/arm9/symbols.txt').read_text(encoding='utf-8').splitlines())
    relocs = set((ROOT / 'config/arm9/relocs.txt').read_text(encoding='utf-8').splitlines())
    intervals, pins = protected(('', 'arm9', 'ov006'), proposal['sourceRevision'])
    source_root = ROOT / 'src/runtime/parallel_wave20261106/aes-table-data'
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/aes-table-data'
    reference_root = ROOT / 'deps/reference/heimdal-a6cf94577c0d1e5bca5304342e4ddffb18255afe-rijndael'
    assert not source_root.exists() and not folder.exists() and not reference_root.exists()
    documents, claimed, reviews, end = {}, [], [], 0
    for row in proposal['objects']:
        start, length = int(row['address'], 0), row['bytes']
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm9', 'ov006', 'data')
        assert row['elements'] == 256 and row['elementBytes'] == 4 and length == 1024
        assert start >= end and int(row['endExclusive'], 0) == start + length
        end = start + length
        assert row['configuredDataRecord'] in symbols
        for line in symbols:
            m = re.search(r' addr:(0x[0-9a-fA-F]+)$', line)
            assert not m or not start < int(m[1], 0) < end
        assert not any(max(start, a) < min(end, b) for a, b in intervals)
        words = generated[row['primarySymbol']]
        payload = b''.join(word.to_bytes(4, 'little') for word in words)
        assert image[start - base:end - base] == payload
        assert hashlib.sha256(payload).hexdigest() == row['targetSha256']
        assert row['primaryDeclaration']['sha256'] == sha256(primary)
        assert row['primaryDeclaration']['declarationType'] == 'static const uint32_t ' + row['primarySymbol'] + '[256]'
        for witness in row['originalPointerWitnesses']:
            origin = int(witness['origin'], 0); caller = witness['configuredCaller']
            assert caller['canonicalRecord'] in symbols and caller['mode'] == 'thumb' and caller['module'] == 'ov006'
            assert int(caller['address'], 0) <= origin and origin + 4 <= int(caller['address'], 0) + caller['bytes']
            assert witness['originalRecord'] in relocs
            assert witness['originalRecord'] == f'from:0x{origin:08x} kind:load to:0x{start:08x} module:overlay(6)'
            assert image[origin - base:origin - base + 4] == start.to_bytes(4, 'little')
        widths = row['nativeBoundedWordIndexWitnesses']
        assert len(widths) >= 8
        for witness in widths:
            assert witness['elementBytes'] == 4 and witness['maximumElementIndex'] == 255
            assert witness['minimumUnsignedByteOffset'] == 0 and witness['maximumUnsignedByteOffset'] == 1020
            assert witness['offsetAlwaysMultipleOf4'] and int(witness['tableAddress'], 0) == start
            for instruction in [*witness['precedingInstructions'], witness['nativeWordLoad']]:
                at = int(instruction['address'], 0); encoded = bytes.fromhex(instruction['bytes'])
                assert image[at - base:at - base + len(encoded)] == encoded
            load = int.from_bytes(bytes.fromhex(witness['nativeWordLoad']['bytes']), 'little')
            assert load & 0xfe00 == 0x5800
            literal = witness['literalBaseProof']; origin = int(literal['literalOrigin'], 0)
            insn = literal['loadInstruction']; at = int(insn['address'], 0)
            halfword = int.from_bytes(bytes.fromhex(insn['bytes']), 'little')
            assert halfword & 0xf800 == 0x4800 and ((at + 4) & ~3) + ((halfword & 255) * 4) == origin
            assert image[origin - base:origin - base + 4] == start.to_bytes(4, 'little')
        leaf = f'ov006-{start:08x}.json'
        documents[leaf] = dict(version=1, kind='aes-rijndael-transform-table', symbol=row['primarySymbol'],
            elementType='u32', elementCount=256, finiteFieldPolynomial='0x11b', affineConstant='0x63',
            packing='uint32-high-coefficient-byte-first-little-endian-storage',
            baseMixCoefficients=row['baseMixCoefficientsBeforeRotationHighByteToLowByte'],
            rotationRightBits=row['rotationRightBits'], substitution='forward' if row['primarySymbol'].startswith('Te') else 'inverse',
            finalRoundReplicatedSubstitution=row['primarySymbol'].endswith('4'), primarySource=dict(
                path=(reference_root / primary.name).relative_to(ROOT).as_posix(), sha256=sha256(primary),
                commit=row['primaryDeclaration']['commit'], symbol=row['primarySymbol']))
        claimed.append(dict(program='', processor='arm9', module='ov006', kind='data', mode='data',
            formatKind='aes-rijndael-transform-table', address=hex(start), bytes=1024,
            elementType='u32', elementCount=256, targetSha256=row['targetSha256'],
            semanticSource=(source_root / leaf).relative_to(ROOT).as_posix()))
        reviews.append(dict(address=hex(start), bytes=1024, primarySymbol=row['primarySymbol'],
            all256PrimaryAndIndependentGeneratedWordsAndNativeBytesEqual=True,
            originalPointerWords=len(row['originalPointerWitnesses']), actualThumbBoundedWordLoads=len(widths)))
    assert all(not p.get('path') or sha256(ROOT / p['path']) == p['sha256'] for p in pins)
    reference_root.mkdir(parents=True)
    for path in [primary, header]:
        (reference_root / path.name).write_bytes(path.read_bytes())
    write_json(reference_root / 'reference-snapshot.json', dict(sourceCredit=0,
        repository='https://github.com/heimdal/heimdal', commit='a6cf94577c0d1e5bca5304342e4ddffb18255afe',
        originalReadOnlySnapshot=dict(path=snapshot_name, sha256=sha256(ROOT / snapshot_name)),
        files=[dict(path=p.name, sha256=sha256(p)) for p in [primary, header]]))
    source_root.mkdir(parents=True)
    for leaf, document in documents.items():
        write_json(source_root / leaf, document)
    for row in claimed:
        row['semanticSourceSha256'] = sha256(ROOT / row['semanticSource'])
    write_json(folder / 'coordinator-review.json', dict(passed=True, sourceCredit=0, objects=10,
        initializedCandidateBytes=10240, sourceRevision=proposal['sourceRevision'],
        proposal=dict(path=name, sha256=sha256(ROOT / name)), independentFiniteFieldAndPrimaryAndOriginalRomAgreement=True,
        nativeConsumersAreThumb=True, objectReviews=reviews, protectedIntervals=len(intervals), protectionPins=pins,
        allCohortSpecificationExclusionsApplied=True, publicPrimaryCopiedVerbatimTo=reference_root.relative_to(ROOT).as_posix(),
        generatorSha256=sha256(__file__), limits=['Storage admission only; full source generation, genuine typed objects/placement, copied-root negatives and shared acceptance remain required.',
        'No caller function, provider, gap, envelope, alignment or original Nintendo authorship credit.']))
    write_json(folder / 'data-claim.json', dict(status='coordinator-admitted-initialized-storage-no-credit',
        owner='workflow_research', sourceRevision=proposal['sourceRevision'], createdUtc=now(), functionCount=0,
        functionOwnershipGranted=False, sourceCredit=0, exclusiveSourceRoot=source_root.relative_to(ROOT).as_posix(),
        exclusiveWorkRoot='work/w6at', helperPrefix='wave20261106_aes_table_data_', claimedStorage=claimed))
    print(dict(passed=True, objects=10, initializedCandidateBytes=10240, sourceCredit=0))


if __name__ == '__main__':
    main()
