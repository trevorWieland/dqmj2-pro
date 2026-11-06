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
    proposal_name = 'evidence/lanes/parallel-wave20261106/ov006-md5-next/crypto-utility-resumption-proposal.json'
    assert sha256(ROOT / proposal_name) == 'ba4bd1095436fbe214c691f01ea18fcb5f167566969a3d819967af75c960887e'
    proposal = read_json(ROOT / proposal_name)
    old_claim_name = proposal['historicalClaim']['path']
    assert sha256(ROOT / old_claim_name) == proposal['historicalClaim']['sha256'] == 'add0919dae37dff2d19a1385d41984d504f03f3a679fc6002d23c9a5b0485fe0'
    old_claim = read_json(ROOT / old_claim_name)
    assert old_claim['owner'] == 'ds_tooling_research/ov006'
    rows = proposal['entries']; assert len(rows) == 8 and sum(row['bytes'] for row in rows) == 1264
    addresses = {0x021ed86c:98,0x021ed8d0:44,0x021ed8fc:62,0x021ed964:54,0x021ed99c:56,0x021f058c:440,0x021f0744:440,0x021f08fc:70}
    assert {int(row['address'], 0): row['bytes'] for row in rows} == addresses
    for pin in [*proposal['nativePins'], *proposal['primaryPins'], proposal['attemptInventory'], proposal['keyWrapPrimarySnapshot']]:
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
    root = ROOT / proposal['proposedSourceRoot']; assert not root.exists()
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
    snapshot = read_json(ROOT / proposal['keyWrapPrimarySnapshot']['path'])
    assert all(sha256(ROOT / pin['path']) == pin['sha256'] for pin in snapshot['files'])
    reference = ROOT / 'deps/reference/hostap-ab49c33aef291e4d9cabe9a16f535bca40569a10-keywrap'
    assert not reference.exists()
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    claim_name = 'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/claim.json'
    assert not (ROOT / claim_name).exists()
    reference.mkdir(parents=True)
    for pin in snapshot['files']:
        (reference / __import__('pathlib').Path(pin['path']).name).write_bytes((ROOT / pin['path']).read_bytes())
    write_json(reference / 'reference-snapshot.json', dict(sourceCredit=0, repository=snapshot['repository'], commit=snapshot['commit'], originalReadOnlySnapshot=proposal['keyWrapPrimarySnapshot'], files=[dict(path=__import__('pathlib').Path(pin['path']).name, sha256=pin['sha256'], sourceUrl=pin['sourceUrl']) for pin in snapshot['files']], comparativeSourceOnlyOriginalNintendoRevisionUnproved=True))
    write_json(ROOT / claim_name, dict(owner='ds_tooling_research', status='coordinator-admitted-source-scope-no-credit',
        createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=proposal['proposedSourceRoot'],
        exclusiveWorkRoot='work/w6cu', helperPrefix=proposal['proposedHelperPrefix'],
        claimedFunctions=rows, sourceCredit=0, canonicalReferenceRoot=reference.relative_to(ROOT).as_posix(),
        originalHistoricalClaimUnchanged=dict(path=old_claim_name, sha256=sha256(ROOT / old_claim_name)),
        tableStorageOwnershipGranted=False, importedHelpersAndStorageCredit=0))
    board = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    write_json(ROOT / 'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/coordinator-admission.json',
        dict(passed=True, sourceCredit=0, claim=claim_name, claimSha256=sha256(ROOT / claim_name),
            exclusiveSourceRoot=proposal['proposedSourceRoot'], sharedDispatchUnchanged=True,
            actualDispatchSha256=sha256(board), functions=8, initializedCandidateBytes=1264,
            proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)),
            originalNativeAndStorageAdmissionGuardsRetained=True,
            onlyEightPreviouslyOwnedUnacceptedIdentitiesResumed=True, oldClaimNotModified=True,
            allCohortSpecificationsAndOtherClaimsExcluded=True, protectionPins=pins,
            allNativeSpansFreshlyDerivedFromOriginalRom=True, functionSourceAbsentAtAdmission=True,
            canonicalReferenceRoot=reference.relative_to(ROOT).as_posix(),
            noTableStorageOwnership=True, timeboxMinutes=25, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=8, initializedCandidateBytes=1264, sourceCredit=0))


if __name__ == '__main__':
    main()
