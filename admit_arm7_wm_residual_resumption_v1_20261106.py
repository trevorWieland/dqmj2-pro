import copy
import hashlib
import struct
from unittest.mock import patch
from project import ROOT, configuration, read_json, write_json, sha256, now
import initialized_storage_protection_v3_20261106 as protection


def independently_close(row, image, base):
    start, size = int(row['address'], 0), row['historicalClaimedBytes']
    flow = read_json(ROOT / row['flow']['path'])
    assert sha256(ROOT / row['flow']['path']) == row['flow']['sha256']
    assert not any(flow[key] for key in ['unresolved', 'unaccountedRanges', 'indirectCalls', 'tailCalls',
        'boundedExecutableSwitches', 'addressOnlyReferences'])
    claimed = {int(item['address'], 0): int(item['word'], 0) for item in flow['instructions']}
    assert len(claimed) == len(flow['instructions'])
    todo, reached, loads, returns = [start], set(), [], []
    while todo:
        at = todo.pop()
        if at in reached:
            continue
        assert start <= at < start + size and at % 4 == 0 and at in claimed
        reached.add(at)
        word = struct.unpack_from('<I', image, at - base)[0]
        assert word == claimed[at]
        condition = word >> 28
        assert condition < 15
        if word & 0x0fffffff == 0x012fff1e:
            returns.append(at)
            if condition != 14:
                todo.append(at + 4)
        elif word & 0x0e000000 == 0x0a000000:
            displacement = (word & 0xffffff) << 2
            if displacement & 0x02000000:
                displacement -= 0x04000000
            target = at + 8 + displacement
            if word & 0x01000000:
                todo.append(at + 4)
            else:
                todo.append(target)
                if condition != 14:
                    todo.append(at + 4)
        else:
            assert word & 0x0ffffff0 != 0x012fff10
            if word & 0x0c000000 == 0:
                assert (word >> 12) & 15 != 15
            if word & 0x0c000000 == 0x04000000:
                assert not word & 0x00100000 or (word >> 12) & 15 != 15
                if (word >> 16) & 15 == 15:
                    assert word & 0x01100000 == 0x01100000 and word & 0x02200000 == 0
                    displacement = word & 4095
                    target = at + 8 + (displacement if word & 0x00800000 else -displacement)
                    width = 1 if word & 0x00400000 else 4
                    loads.append((at, target, width, image[target - base:target - base + width].hex()))
            if word & 0x0e000000 == 0x08000000:
                assert not word & 0x00100000 or not word & 0x8000
            todo.append(at + 4)
    assert reached == set(claimed) and returns
    expected = [(int(item['origin'], 0), int(item['address'], 0), item['bytes'], item['hex']) for item in flow['literalReads']]
    assert sorted(loads) == sorted(expected) and len({item[0] for item in loads}) == len(loads)
    coverage = bytearray(size)
    for at in reached:
        coverage[at - start:at - start + 4] = b'\x01' * 4
    for origin, target, width, value in loads:
        assert start <= target < target + width <= start + size
        for at in range(target - start, target - start + width):
            assert coverage[at] in [0, 2]
            coverage[at] = 2
    assert 0 not in coverage and coverage.count(1) == row['entryReachableBytes']
    assert coverage.count(2) == row['literalReadBytes']
    payload = image[start - base:start - base + size]
    assert hashlib.sha256(payload).hexdigest() == row['computedEvidenceSha256'] == row['currentHistoricalNativeSpanSha256']
    return dict(address=hex(start), bytes=size, instructionBytes=coverage.count(1), literalBytes=coverage.count(2),
        completeOriginalLiteralOriginsIndependentlyChecked=len(loads), returns=len(returns), nativeSpanSha256=hashlib.sha256(payload).hexdigest())


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next/qualified-v2/proposal.json'
    assert sha256(ROOT / proposal_name) == 'b6f6f1885b3b5be057093290bb053eca538925868b49291888d6f04fe8622ab5'
    proposal = read_json(ROOT / proposal_name)
    assert len(proposal['functions']) == 16 and sum(row['historicalClaimedBytes'] for row in proposal['functions']) == 7012
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in proposal['inputPins'])
    assert all(row['committedLedgerBytes'] is None and not row['committedFunctionMatched'] for row in proposal['functions'])
    claim_name = 'evidence/lanes/parallel-wave20261102/host-arm7-sixth/claim.json'
    assert sha256(ROOT / claim_name) == '8ff9ce697c1938b1c36dbb9e3f9b29905d23587e775bfa1ee342490bae302039'
    historical = read_json(ROOT / claim_name)
    assert historical['owner'] == 'workflow_research' and len(historical['functions']) == 51
    ready = read_json(ROOT / 'evidence/lanes/parallel-wave20261102/host-arm7-sixth/ready.json')
    assert ready['functions'] == 35
    remaining = {row['address'] for row in historical['functions']} - {row['address'] for row in ready['identities']}
    assert remaining == {row['address'] for row in proposal['functions']}
    cfg = configuration(); assert sha256(cfg['rom']) == cfg['romSha256']
    rom = cfg['rom'].read_bytes()
    offset, entry, load, length = struct.unpack_from('<4I', rom, 0x30)
    assert (offset, entry, load, length) == (624640, 0x02380000, 0x02380000, 160048)
    arm7 = rom[offset:offset + length]
    assert struct.unpack_from('<3I', arm7, 160036) == (0x027e0000, 96388, 6504)
    image, base = arm7[63636:63636 + 96388], 0x027e0000
    assert image == (ROOT / 'extract/arm7/runtime/arm7-main.bin').read_bytes()
    assert hashlib.sha256(image).hexdigest() == 'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'
    original_reader = protection.read_json

    def historical_projection(path):
        document = original_reader(path)
        if path == ROOT / claim_name:
            document = copy.deepcopy(document)
            document['functions'] = [row for row in document['functions'] if row['address'] not in remaining]
        return document

    revision = 'fcd3d2bad860d0e83b6de21c8bfb24f7d02f8bb8'
    with patch.object(protection, 'read_json', historical_projection):
        intervals, pins = protection.protected(('', 'arm7', 'arm7-main'), revision)
    reviews, functions = [], []
    owned = {row['address']: row for row in historical['functions']}
    for row in proposal['functions']:
        start, size = int(row['address'], 0), row['historicalClaimedBytes']
        assert row['configuredMode'] == row['ledgerMode'] == 'arm'
        assert row['computedExtentEqualsHistoricalClaim'] and row['completePhysicalEvidence']
        assert owned[row['address']]['bytes'] == size and owned[row['address']]['targetSha256'] == row['currentHistoricalNativeSpanSha256']
        assert not any(max(start, a) < min(start + size, b) for a, b in intervals)
        reviews.append(independently_close(row, image, base))
        functions.append(dict(program='', processor='arm7', module='arm7-main', mode='arm',
            address=hex(start), bytes=size, endExclusive=hex(start + size), targetSha256=reviews[-1]['nativeSpanSha256'],
            architecture='ARMv4T', base=base, binary='extract/arm7/runtime/arm7-main.bin',
            inputModuleSha256=hashlib.sha256(image).hexdigest(), physicalFlow=row['flow']))
    assert sum(row['instructionBytes'] for row in reviews) == 6788 and sum(row['literalBytes'] for row in reviews) == 224
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/arm7-wm-residual-next'
    new_claim_name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    source_root = 'src/arm7/parallel_wave20261106/wm-residual-next'
    assert not (ROOT / new_claim_name).exists() and not (ROOT / source_root).exists()
    write_json(ROOT / new_claim_name, dict(owner='repo_audit', status='coordinator-admitted-source-scope-no-credit',
        sourceCredit=0, createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=source_root,
        exclusiveWorkRoot='work/w6wr', helperPrefix='wave20261106_arm7_wm_residual_next_', claimedFunctions=functions,
        historicalReservationExplicitlyResumedFrom='workflow_research', historicalClaimUnchanged=dict(path=claim_name, sha256=sha256(ROOT / claim_name)),
        sourceNamesForUnmappedSevenRemainHypotheses=True, importedRequestTableAndProvidersCredit=0))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, claim=new_claim_name,
        claimSha256=sha256(ROOT / new_claim_name), exclusiveSourceRoot=source_root, sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'), functions=16,
        initializedCandidateBytes=7012, originalNativeAndStorageAdmissionGuardsRetained=True,
        proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)), independentIntegerArmDecoder=True,
        exactEveryLiteralLoadOriginWidthValueVerified=True, physicalReviews=reviews, protectionPins=pins,
        onlyExactHistorical16OwnershipProjectedPrivately=True, noHistoricalFilesOrMetadataRewritten=True,
        completeNativeInstructionBytes=6788, completeNativeLiteralBytes=224, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=16, initializedCandidateBytes=7012, sourceCredit=0))


if __name__ == '__main__':
    main()
