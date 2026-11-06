import hashlib
from project import ROOT, read_json, write_json, sha256


CORRECTION = 'evidence/lanes/parallel-wave20261105/dwc-http-next/origin-metadata-correction.json'
CORRECTION_SHA = '1ae671f9f29cce7af9f8c7dc9956a1610b7a1cd19836d90867a162b0321ae3d2'
CLAIM_SHA = 'f7dbe39300aae4f663108883a71c86149dd85668a749896e65b84205d6239cc9'


def identity(row):
    return (row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0), row['bytes'])


def main():
    assert sha256(ROOT / CORRECTION) == CORRECTION_SHA
    receipt = read_json(ROOT / CORRECTION)
    assert receipt['claim']['sha256'] == sha256(ROOT / receipt['claim']['path']) == CLAIM_SHA
    claim = read_json(ROOT / receipt['claim']['path'])
    owned = {identity(row): row for row in claim['claimedFunctions']}
    assert len(owned) == 58 and sum(k[-1] for k in owned) == 12332
    assert len(receipt['packets']) == 3
    observed, images, counts = {}, {}, []
    for packet in receipt['packets']:
        for label in ['ready', 'input', 'canonicalDescriptor']:
            assert sha256(ROOT / packet[label]['path']) == packet[label]['sha256']
        ready = read_json(ROOT / packet['ready']['path'])
        inputs = read_json(ROOT / packet['input']['path'])
        assert inputs['ownershipOriginClaimSha256'] == packet['frozenDescriptiveOrigin']
        assert packet['actualAdmittedOriginClaimSha256'] == CLAIM_SHA
        for pin in ready['files']:
            assert sha256(ROOT / pin['path']) == pin['sha256']
        physical = packet['physicalIdentities']
        assert len(physical) == packet['functions']
        assert sum(row['bytes'] for row in physical) == packet['bytes']
        for row in physical:
            key = identity(row)
            assert key in owned and key not in observed and row['id'] == owned[key]['id']
            assert sha256(ROOT / row['source']) == row['sourceSha256']
            native = owned[key]
            if native['binary'] not in images:
                assert sha256(ROOT / native['binary']) == native['inputModuleSha256']
                images[native['binary']] = (ROOT / native['binary']).read_bytes()
            offset = key[4] - native['base']
            target = images[native['binary']][offset:offset + key[5]]
            assert hashlib.sha256(target).hexdigest() == row['targetSha256'] == native['targetSha256']
            assert row['source'].startswith('src/runtime/parallel_wave20261105/dwc-http-next/')
            assert not any(key[:3] == old[:3] and max(key[4], old[4]) < min(key[4] + key[5], old[4] + old[5]) for old in observed)
            observed[key] = row['targetSha256']
        counts.append(dict(name=packet['name'], functions=len(physical), bytes=packet['bytes']))
    assert len(observed) == 16 and sum(k[-1] for k in observed) == 1974
    write_json(ROOT / 'evidence/verification/http-origin-correction-independent-20261106.json',
        dict(passed=True, sourceCredit=0, correction=CORRECTION, correctionSha256=CORRECTION_SHA,
             actualClaimSha256=CLAIM_SHA, packets=counts, physicalFunctionIdentities=16, initializedBytes=1974,
             allFrozenPinsSourcesAndNativeTargetsVerified=True, originalPhysicalAdmissionGuardsUnchanged=True,
             frozenMetadataUnchanged=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=16, bytes=1974, sourceCredit=0))


if __name__ == '__main__':
    main()
