import hashlib
import json
import struct
import subprocess
from project import ROOT, configuration, read_json, write_json, sha256, now
from wave20261105_arm7_boundary_next_protections_v2 import protections


def main():
    name = 'evidence/lanes/parallel-wave20261105/arm7-boundary-next/port-proposal/proposal.json'
    assert sha256(ROOT / name) == '2f8ef0926c78d344889f2cb51d3526422366b2a5729fdf695df2cd7fc37a3dd5'
    proposal = read_json(ROOT / name)
    revision = '9d4c697530ff885ba928e1a4395ab1422f113e3b'
    raw_ledger = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    protected, pins, epoch = protections(revision, dict(committedLedgerSha256=hashlib.sha256(raw_ledger).hexdigest()))
    assert not epoch['unparsedArm7Claims']
    for cohort, letter in [(161, 'f'), (162, 'g')]:
        path = ROOT / f'cohort{cohort}-parallel-wave20261105-{letter}-specification.json'
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        for row in read_json(path)['expectedAdditions']:
            if (row.get('program') or '', row['processor'], row['module']) == ('', 'arm7', 'arm7-main'):
                begin = int(row['address'], 0)
                protected.append(dict(start=begin, end=begin + row['bytes'], kind='actual-root-pending'))
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    rom = config['rom'].read_bytes()
    offset, entry, load, size = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, size) == (624640, 0x02380000, 0x02380000, 160048)
    arm7 = rom[offset:offset + size]
    assert struct.unpack_from('<3I', arm7, 160036) == (0x027e0000, 96388, 6504)
    image, base = arm7[63636:63636 + 96388], 0x027e0000
    inventory = read_json(ROOT / 'evidence/arm7/ghidra-runtime-inventory.json')['functions']
    functions, reviews, total_code, total_literals = [], [], 0, 0
    cursor = 0x027e637c
    own_entries = {int(row['address'], 0) for row in proposal['functions']}
    for row in proposal['functions']:
        begin, size = int(row['address'], 0), row['bytes']
        end = begin + size
        assert begin == cursor
        cursor = end
        body = image[begin - base:end - base]
        assert len(body) == size and hashlib.sha256(body).hexdigest() == row['nativeSpanSha256']
        assert sha256(ROOT / row['flow']['path']) == row['flow']['sha256']
        flow = read_json(ROOT / row['flow']['path'])
        assert all(not flow[key] for key in ['unresolved', 'unaccountedRanges', 'indirectCalls', 'tailCalls',
                                             'boundedExecutableSwitches', 'addressOnlyReferences'])
        instructions = {int(item['address'], 0) for item in flow['instructions']}
        todo, reached, literals, returns = [begin], set(), [], []
        while todo:
            address = todo.pop()
            if address in reached:
                continue
            assert address in instructions and address % 4 == 0
            reached.add(address)
            word = struct.unpack_from('<I', image, address - base)[0]
            condition = word >> 28
            assert condition < 15
            successors = []
            if word & 0x0fffffff == 0x012fff1e:
                returns.append(address)
                if condition != 14:
                    successors.append(address + 4)
            elif word & 0x0e000000 == 0x0a000000:
                displacement = (word & 0xffffff) << 2
                if displacement & 0x02000000:
                    displacement -= 0x04000000
                target = address + 8 + displacement
                if word & 0x01000000:
                    successors.append(address + 4)
                else:
                    successors.append(target)
                    if condition != 14:
                        successors.append(address + 4)
            else:
                assert word & 0x0ffffff0 != 0x012fff10
                if word & 0x0c000000 == 0:
                    assert (word >> 12) & 15 != 15
                if word & 0x0c000000 == 0x04000000:
                    assert not word & 0x00100000 or (word >> 12) & 15 != 15
                    if (word >> 16) & 15 == 15:
                        assert word & 0x01100000 == 0x01100000 and word & 0x02200000 == 0
                        displacement = word & 4095
                        target = address + 8 + (displacement if word & 0x00800000 else -displacement)
                        literals.append((address, target, 1 if word & 0x00400000 else 4))
                if word & 0x0e000000 == 0x08000000:
                    assert not word & 0x00100000 or not word & 0x8000
                successors.append(address + 4)
            todo.extend(successors)
        assert reached == instructions and len(returns) == 1
        expected_literals = [(int(item['origin'], 0), int(item['address'], 0), item['bytes']) for item in flow['literalReads']]
        assert sorted(literals) == sorted(expected_literals)
        mask = bytearray(size)
        for address in reached:
            mask[address - begin:address - begin + 4] = b'\x01' * 4
        for origin, address, width in literals:
            assert begin <= address < address + width <= end
            for at in range(address - begin, address - begin + width):
                assert mask[at] in (0, 2)
                mask[at] = 2
        assert 0 not in mask and mask.count(1) == row['certificate']['instructionBytes']
        assert mask.count(2) == row['certificate']['literalBytes']
        assert not [p for p in protected if max(begin, p['start']) < min(end, p['end'])]
        assert not [r for r in inventory if r['module'] == 'arm7-main' and begin < int(r['address'], 0) < end
                    and int(r['address'], 0) not in own_entries]
        assert not row['outsideReferences']['interiorOrPoolEntries']
        functions.append(dict(program='', processor='arm7', module='arm7-main', mode='arm', address=hex(begin),
            bytes=size, endExclusive=hex(end), targetSha256=row['nativeSpanSha256'], architecture='ARMv4T',
            base=base, binary='extract/arm7/runtime/arm7-main.bin', inputModuleSha256=hashlib.sha256(image).hexdigest()))
        reviews.append(dict(address=hex(begin), independentlyReachedInstructions=len(reached),
                            independentLiteralLoads=len(literals), instructionBytes=mask.count(1), literalBytes=mask.count(2)))
        total_code += mask.count(1)
        total_literals += mask.count(2)
    assert cursor == 0x027e7cc8 and len(functions) == 9 and (total_code, total_literals) == (6388, 88)
    directory = ROOT / 'evidence/lanes/parallel-wave20261105/arm7-wm-port-next'
    assert not (directory / 'claim.json').exists()
    write_json(directory / 'coordinator-review.json', dict(passed=True, sourceCredit=0, sourceRevision=revision,
        independentIntegerDecoder=True, reviews=reviews, physicalProtectionEpoch=epoch, physicalProtectionPins=pins,
        originalRomSha256=config['romSha256'], originalRuntimeModuleSha256=hashlib.sha256(image).hexdigest(),
        proposal=name, proposalSha256=sha256(ROOT / name), generatorSha256=sha256(__file__)))
    write_json(directory / 'claim.json', dict(owner='repo_audit', status='coordinator-admitted-source-scope-no-credit',
        createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot='src/arm7/parallel_wave20261105/arm7-wm-port-next',
        exclusiveWorkRoot='work/w5wp', claimedFunctions=functions, sourceCredit=0))
    print(dict(passed=True, admittedFunctions=9, admittedBytes=6476, sourceCredit=0,
               claimSha256=sha256(directory / 'claim.json')))


if __name__ == '__main__':
    main()
