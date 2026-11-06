import hashlib
import json
import struct
import subprocess
from project import ROOT, read_json, write_json, sha256
from inspect_child_message_assets_20261105 import unpack_tokens, encode_with_recipe
from wave20261105_child_static_assets_next_formats import decode, encode


REVISION = 'fa2ba9a799e1eed41c3bca98e4ffebb290ccca29'


def main():
    raw = subprocess.check_output(['git', 'show', REVISION + ':manifest.json'], cwd=ROOT)
    manifest = json.loads(raw)
    frontier_name = 'evidence/verification/source95-frontier-closed164-20261106.json'
    frontier = read_json(ROOT / frontier_name)
    assert frontier['sourceRevision'] == REVISION
    inputs, results, rejected = [], {}, 0
    for module in manifest['modules']:
        path = ROOT / module['binary']
        assert sha256(path) == module['sha256']
        inputs.append(dict(path=module['binary'], sha256=module['sha256']))
        image = path.read_bytes()
        namespace = (module.get('program') or '', module['processor'], module['name'])
        for magic in [b'RGCN', b'RLCN', b'RCSN', b'RTFN']:
            offset = image.find(magic)
            while offset >= 0:
                views = [(offset, False)]
                if offset >= 5 and image[offset - 5] == 0x10:
                    views.append((offset - 5, True))
                offset = image.find(magic, offset + 1)
                for start, compressed in views:
                    try:
                        if compressed:
                            size = int.from_bytes(image[start + 1:start + 4], 'little')
                            assert 16 <= size <= 1048576
                            decoded, recipe, consumed = unpack_tokens(image[start:])
                            assert decoded[:4] == magic and len(decoded) == size
                            stored = encode_with_recipe(decoded, recipe)
                            assert stored == image[start:start + consumed]
                        else:
                            size = int.from_bytes(image[start + 8:start + 12], 'little')
                            assert 16 <= size <= 1048576 and start + size <= len(image)
                            stored = decoded = image[start:start + size]
                        semantic = decode(decoded)
                        assert encode(semantic) == decoded
                    except (AssertionError, ValueError, IndexError, UnicodeDecodeError, OverflowError, struct.error):
                        rejected += 1
                        continue
                    address = int(module['base'], 0) + start
                    witnesses = [r for r in frontier['investigationProposals']
                                 if (r['program'], r['processor'], r['module']) == namespace
                                 and r['knownGhidraBodyBytes'] == 0 and int(r['address'], 0) <= address
                                 and address + len(stored) <= int(r['endExclusive'], 0)]
                    key = (*namespace, address, len(stored))
                    results[key] = dict(program=namespace[0], processor=namespace[1], module=namespace[2],
                        address=hex(address), bytes=len(stored), decodedBytes=len(decoded), magic=magic.decode(),
                        compressedLz10=compressed, semanticKind=semantic['kind'],
                        storedSha256=hashlib.sha256(stored).hexdigest(), decodedSha256=hashlib.sha256(decoded).hexdigest(),
                        fitsUnprotectedZeroBodyProposal=bool(witnesses), sourceCredit=0)
    assert all(sha256(ROOT / p['path']) == p['sha256'] for p in inputs)
    candidate = [r for r in results.values() if r['fitsUnprotectedZeroBodyProposal']]
    write_json(ROOT / 'evidence/lanes/parallel-wave20261106/initialized-nitro-assets-next/inventory.json',
        dict(passed=True, sourceCredit=0, sourceOwnershipGranted=False, sourceRevision=REVISION,
             manifestSha256=hashlib.sha256(raw).hexdigest(), frontier=frontier_name,
             frontierSha256=sha256(ROOT / frontier_name), nativeInputs=inputs,
             completeSemanticallyRebuiltAssets=list(results.values()), rejectedSignatureViews=rejected,
             unprotectedProposalCandidates=candidate, candidateBytes=sum(r['bytes'] for r in candidate),
             generatorSha256=sha256(__file__), codecPins=[dict(path=p, sha256=sha256(ROOT / p)) for p in [
                 'inspect_child_message_assets_20261105.py', 'wave20261105_child_static_assets_next_formats.py',
                 'wave20261105_child_static_assets_next_font.py']], limitations=[
                 'Read-only standard Nitro2D/font signatures and visible LZ10 literal headers only.',
                 'No arbitrary compression scan, opaque data source, ownership or accepted credit.',
                 'Proposal containment is a conservative filter; large or split objects may need separate inspection.',
                 'Any admission requires current storage/function exclusion and independent ROM-derived lineage.']))
    print(dict(completeAssets=len(results), unprotectedCandidates=len(candidate),
               candidateBytes=sum(r['bytes'] for r in candidate), sourceCredit=0))


if __name__ == '__main__':
    main()
