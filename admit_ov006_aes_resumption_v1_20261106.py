import hashlib
import json
import re
import subprocess
from project import ROOT, read_json, write_json, sha256, now


def spans(node, parent=None):
    parent = parent or {}
    if isinstance(node, list):
        for item in node:
            yield from spans(item, parent)
    elif isinstance(node, dict):
        context = {key: node.get(key) or parent.get(key) for key in ['program', 'processor', 'module']}
        if (context['program'] or '', context['processor'] or 'arm9', context['module']) == ('', 'arm9', 'ov006'):
            size = node.get('storedBytes', node.get('bytes', node.get('size')))
            if node.get('address') and size:
                start = int(node['address'], 0) if isinstance(node['address'], str) else node['address']
                if isinstance(size, str):
                    size = len(bytes.fromhex(size)) if 'instruction' in node else int(size, 0)
                assert type(size) is int and size > 0
                yield start, start + size
        for item in node.values():
            yield from spans(item, context)


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/ov006-aes-next/resumption-proposal.json'
    assert sha256(ROOT / proposal_name) == '4148fdb47b735cea4f74ad6813130002256a3ef81c9d01cd9ec217f3330117e9'
    proposal = read_json(ROOT / proposal_name)
    old_claim_name = proposal['oldClaim']['path']
    assert sha256(ROOT / old_claim_name) == proposal['oldClaim']['sha256'] == 'add0919dae37dff2d19a1385d41984d504f03f3a679fc6002d23c9a5b0485fe0'
    old_claim = read_json(ROOT / old_claim_name)
    assert old_claim['owner'] == 'ds_tooling_research/ov006'
    rows = proposal['identities']; assert len(rows) == 4 and sum(row['bytes'] for row in rows) == 3008
    addresses = {0x021f0944: 696, 0x021f0bfc: 400, 0x021f0d8c: 956, 0x021f1148: 956}
    assert {int(row['address'], 0): row['bytes'] for row in rows} == addresses
    for pin in proposal['inputs']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    revision = 'fcd3d2bad860d0e83b6de21c8bfb24f7d02f8bb8'
    raw = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = [json.loads(line) for line in raw.splitlines()]
    selected = {row['id']: row for row in ledger}
    own = {row['id']: row for row in old_claim['claimedFunctions']}
    accepted = [row for row in ledger if row.get('states', {}).get('functionMatched') or row.get('sourceUnit')]
    protected = list(spans(accepted))
    pins = [dict(gitObject=revision + ':ledger/functions.jsonl', sha256=hashlib.sha256(raw).hexdigest())]
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        document = read_json(path)
        if path == ROOT / old_claim_name:
            document = dict(document, claimedFunctions=[row for row in document['claimedFunctions'] if row['id'] not in {r['id'] for r in rows}])
        protected.extend(spans(document))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        content = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(content).hexdigest()))
        protected.extend(spans(json.loads(content)[key]))
    symbols_name = 'config/arm9/overlays/ov006/symbols.txt'
    symbols = set((ROOT / symbols_name).read_text(encoding='utf-8').splitlines())
    relocs = set((ROOT / 'config/arm9/overlays/ov006/relocs.txt').read_text(encoding='utf-8').splitlines())
    from project import configuration, native_dependencies
    cfg = configuration(); native_dependencies(cfg)
    assert sha256(cfg['rom']) == cfg['romSha256'] == '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    import ndspy.rom
    overlay = ndspy.rom.NintendoDSRom(cfg['rom'].read_bytes()).loadArm9Overlays([6])[6]
    image, base = bytes(overlay.data), overlay.ramAddress
    assert hashlib.sha256(image).hexdigest() == 'fb9cb28ea400207bda442e3265da73af994866cf3a6c352b46a11db59835d341'
    root = ROOT / proposal['planned']['sourceRoot']; assert not root.exists()
    for row in rows:
        start, length = int(row['address'], 0), row['bytes']
        assert row['id'] in own and row['id'] in selected
        for key in ['processor', 'module', 'mode', 'address', 'bytes', 'targetSha256']:
            assert own[row['id']][key] == row[key]
        current = selected[row['id']]
        assert not current.get('sourceUnit') and not current.get('states', {}).get('functionMatched')
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm9', 'ov006', 'thumb')
        assert not (ROOT / row['sourceTarget']).exists()
        assert row['canonicalInventoryRecord'] in symbols
        assert hashlib.sha256(image[start - base:start - base + length]).hexdigest() == row['targetSha256']
        assert not any(max(start, a) < min(start + length, b) for a, b in protected)
        for line in symbols:
            match = re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)(?:\s|$)', line)
            assert not match or not start < int(match[1], 0) < start + length
        assert all(line in relocs for line in row['originalRelocationRecords'])
    reference = ROOT / 'deps/reference/heimdal-a6cf94577c0d1e5bca5304342e4ddffb18255afe-rijndael'
    assert sha256(reference / 'heimdal-rijndael-alg-fst.c') == 'abb323462fa6202fee8e0f1a46c8911cb75eb08422cf730fd2eba5de5f7220e4'
    assert sha256(reference / 'heimdal-rijndael-alg-fst.h') == '7983930d42b99673cdf159df4ca0206fa0d487a1934dac6b6b8c98ae4dc2407a'
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    claim_name = 'evidence/lanes/parallel-wave20261106/ov006-aes-next/claim.json'
    assert not (ROOT / claim_name).exists()
    write_json(ROOT / claim_name, dict(owner='ds_tooling_research', status='coordinator-admitted-source-scope-no-credit',
        createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=proposal['planned']['sourceRoot'],
        exclusiveWorkRoot='work/w6an', helperPrefix=proposal['planned']['helperPrefix'],
        claimedFunctions=rows, sourceCredit=0, canonicalReferenceRoot=reference.relative_to(ROOT).as_posix(),
        originalHistoricalClaimUnchanged=dict(path=old_claim_name, sha256=sha256(ROOT / old_claim_name)),
        tableStorageOwnershipGranted=False, importedTableAndRconStorageCredit=0))
    board = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    write_json(ROOT / 'evidence/lanes/parallel-wave20261106/ov006-aes-next/coordinator-admission.json',
        dict(passed=True, sourceCredit=0, claim=claim_name, claimSha256=sha256(ROOT / claim_name),
            exclusiveSourceRoot=proposal['planned']['sourceRoot'], sharedDispatchUnchanged=True,
            actualDispatchSha256=sha256(board), functions=4, initializedCandidateBytes=3008,
            proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)),
            originalNativeAndStorageAdmissionGuardsRetained=True,
            onlyFourPreviouslyOwnedUnacceptedIdentitiesResumed=True, oldClaimNotModified=True,
            allCohortSpecificationsAndOtherClaimsExcluded=True, protectionPins=pins,
            allNativeSpansFreshlyDerivedFromOriginalRom=True, functionSourceAbsentAtAdmission=True,
            canonicalReferenceRoot=reference.relative_to(ROOT).as_posix(),
            noTableStorageOwnership=True, timeboxMinutes=25, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=4, initializedCandidateBytes=3008, sourceCredit=0))


if __name__ == '__main__':
    main()
