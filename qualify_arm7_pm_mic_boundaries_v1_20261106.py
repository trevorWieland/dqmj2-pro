import hashlib
import struct
from project import ROOT, configuration, read_json, write_json, sha256


PROPOSAL = 'evidence/lanes/parallel-wave20261106/arm7-sdk-next-proposal-v2/proposal.json'
EXPECTED = {0x03804d40: 532, 0x038053d0: 72, 0x03805418: 712, 0x03805784: 552}


def bounded_switch(image, base, at):
    assert base + 4 <= at < base + len(image) - 8
    compare, dispatch, default = struct.unpack_from('<III', image, at - base - 4)
    assert compare & 0xfff0f000 == 0xe3500000
    assert dispatch & 0xfffffff0 == 0x908ff100
    register = dispatch & 15
    assert register < 15 and compare >> 16 & 15 == register
    rotate = (compare >> 8 & 15) * 2; immediate = compare & 255
    maximum = ((immediate >> rotate) | (immediate << (32 - rotate))) & 0xffffffff if rotate else immediate
    assert maximum <= 255 and default & 0xff000000 == 0xea000000
    cases = [at + 8 + i * 4 for i in range(maximum + 1)]
    assert cases[-1] + 4 <= base + len(image)
    words = [struct.unpack_from('<I', image, target - base)[0] for target in cases]
    assert all(word & 0xff000000 == 0xea000000 for word in words)
    return dict(dispatch=hex(at), compareAddress=hex(at - 4), compareWord=hex(compare), dispatchWord=hex(dispatch),
        defaultWord=hex(default), upper=maximum, indexRegister=register, tableAddresses=[hex(a) for a in cases],
        tableWords=[hex(w) for w in words])


def close(row, image, base):
    start, size = int(row['address'], 0), row['bytes']
    assert sha256(ROOT / row['flow']['path']) == row['flow']['sha256']
    flow = read_json(ROOT / row['flow']['path'])
    assert not any(flow[key] for key in ['unresolved', 'unaccountedRanges', 'indirectCalls', 'tailCalls', 'addressOnlyReferences'])
    claimed = {int(item['address'], 0): int(item['word'], 0) for item in flow['instructions']}
    assert len(claimed) == len(flow['instructions'])
    todo, reached, loads, returns, edges, switches = [start], set(), [], [], set(), []
    def edge(origin, target):
        edges.add((origin, target)); todo.append(target)
    while todo:
        at = todo.pop()
        if at in reached:
            continue
        assert start <= at < start + size and at % 4 == 0 and at in claimed
        word = struct.unpack_from('<I', image, at - base)[0]
        assert word == claimed[at]; reached.add(at); condition = word >> 28
        assert condition < 15
        if word & 0xfffffff0 == 0x908ff100:
            proof = bounded_switch(image, base, at); switches.append(proof)
            for target in [at + 4] + [int(a, 0) for a in proof['tableAddresses']]:
                edge(at, target)
        elif word & 0x0fffffff == 0x012fff1e:
            returns.append(at)
            if condition != 14:
                edge(at, at + 4)
        elif word & 0x0e000000 == 0x0a000000:
            displacement = (word & 0xffffff) << 2
            if displacement & 0x02000000:
                displacement -= 0x04000000
            target = at + 8 + displacement
            if word & 0x01000000:
                edge(at, at + 4)
            else:
                edge(at, target)
                if condition != 14:
                    edge(at, at + 4)
        else:
            assert word & 0x0ffffff0 != 0x012fff10
            if word & 0x0c000000 == 0:
                assert word >> 12 & 15 != 15
            if word & 0x0c000000 == 0x04000000:
                assert not word & 0x00100000 or word >> 12 & 15 != 15
                if word >> 16 & 15 == 15:
                    assert word & 0x01100000 == 0x01100000 and word & 0x02200000 == 0
                    offset = word & 4095; target = at + 8 + (offset if word & 0x00800000 else -offset)
                    width = 1 if word & 0x00400000 else 4
                    loads.append((at, target, width, image[target - base:target - base + width].hex()))
            if word & 0x0e000000 == 0x08000000:
                assert not word & 0x00100000 or not word & 0x8000
            edge(at, at + 4)
    assert reached == set(claimed) and returns
    assert sorted(loads) == sorted((int(r['origin'], 0), int(r['address'], 0), r['bytes'], r['hex']) for r in flow['literalReads'])
    assert len({item[0] for item in loads}) == len(loads)
    for proof in switches:
        at = int(proof['dispatch'], 0)
        assert {origin for origin, target in edges if target == at} == {at - 4}
        original = [item for item in flow['boundedExecutableSwitches'] if item['dispatch'] == proof['dispatch']]
        assert len(original) == 1
        for key in ['compareAddress', 'compareWord', 'dispatchWord', 'defaultWord', 'upper', 'tableAddresses', 'tableWords']:
            assert original[0][key] == proof[key]
    assert len(switches) == len(flow['boundedExecutableSwitches'])
    coverage = bytearray(size)
    for at in reached:
        coverage[at - start:at - start + 4] = b'\x01' * 4
    for origin, target, width, value in loads:
        assert start <= target < target + width <= start + size
        for at in range(target - start, target - start + width):
            assert coverage[at] in [0, 2]; coverage[at] = 2
    assert 0 not in coverage and coverage.count(1) == row['entryReachableInstructionBytes']
    assert coverage.count(2) == row['actualLiteralReadBytes']
    assert hashlib.sha256(image[start - base:start - base + size]).hexdigest() == row['nativeSpanSha256']
    return dict(address=row['address'], bytes=size, instructionBytes=coverage.count(1), literalBytes=coverage.count(2),
        completePerOriginLiteralLoads=len(loads), originalSwitches=switches, dispatchGuardHasOnlyImmediateCmpPredecessor=True)


def qualify():
    assert sha256(ROOT / PROPOSAL) == '52522b9aba85f704742a6773e8ca46144fa58b9bea60446002dab817dc5cda1e'
    proposal = read_json(ROOT / PROPOSAL)
    cfg = configuration(); assert sha256(cfg['rom']) == cfg['romSha256']; rom = cfg['rom'].read_bytes()
    offset, entry, load, length = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, length) == (624640, 0x02380000, 0x02380000, 160048)
    raw = rom[offset:offset + length]
    assert struct.unpack_from('<3I', raw, 160024) == (0x037f8000, 63096, 15980)
    image, base = raw[540:63636], 0x037f8000
    assert image == (ROOT / 'extract/arm7/runtime/arm7-wram.bin').read_bytes()
    rows = [row for row in proposal['candidates'] if int(row['address'], 0) in EXPECTED]
    assert len(rows) == 4 and {int(r['address'], 0): r['bytes'] for r in rows} == EXPECTED
    proofs = [close(row, image, base) for row in rows]
    rejected = []
    for proof in proofs:
        for switch in proof['originalSwitches']:
            at = int(switch['dispatch'], 0) - base
            for label, position, mask in [('conditional-cmp', at - 4, 0x10000000), ('missing-cmp-flags', at - 4, 1 << 20),
                    ('other-register', at, 1), ('wrong-shift', at, 1 << 7), ('wrong-condition', at, 0x10000000),
                    ('default-call', at + 4, 1 << 24), ('case-call', at + 8, 1 << 24)]:
                changed = bytearray(image); word = struct.unpack_from('<I', changed, position)[0]
                struct.pack_into('<I', changed, position, word ^ mask)
                try:
                    bounded_switch(changed, base, base + at)
                except AssertionError:
                    rejected.append(dict(dispatch=switch['dispatch'], case=label))
                else:
                    raise AssertionError(label)
    assert sum(len(p['originalSwitches']) for p in proofs) == 3 and len(rejected) == 21
    result = dict(passed=True, sourceCredit=0, functions=4, bytes=1868, independentIntegerDecoder=True,
        originalRawRomAndWholeWramVerified=True, proofs=proofs, rejectedSwitchControls=rejected,
        noOwnershipOrSourceOrProductionRoutingChanged=True, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/arm7-pm-mic-independent-boundaries-v1-20261106.json', result)
    return result


if __name__ == '__main__':
    qualify(); print(dict(passed=True, functions=4, bytes=1868, boundedSwitches=3, sourceCredit=0))
