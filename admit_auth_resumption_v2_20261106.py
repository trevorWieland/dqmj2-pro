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
        if (context['program'] or '', context['processor'] or 'arm9', context['module']) == ('', 'arm9', 'main'):
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
    proposal_name = 'evidence/lanes/parallel-wave20261106/auth-resume-read-only/proposal.json'
    assert sha256(ROOT / proposal_name) == '10d5feb17361838021d13889ca4a21ba727fe4e004d20b07f532a89c66363301'
    proposal = read_json(ROOT / proposal_name)
    old_claim_name = 'evidence/lanes/parallel-wave20261105/dwc-auth-next/claim.json'
    assert sha256(ROOT / old_claim_name) == '3d47be47b90274d6f37d8c4626a3a47dac9560e92af9baebb1ccc0572ffb6863'
    old_claim = read_json(ROOT / old_claim_name)
    assert old_claim['owner'] == 'workflow_research/dwc-auth-next'
    rows = proposal['proposedIdentities']; assert len(rows) == 16 and sum(row['bytes'] for row in rows) == 2064
    addresses = {0x02095a10:220,0x02095aec:228,0x02095bd0:132,0x02095d50:88,0x02095da8:180,0x02095e9c:120,0x02095f34:88,0x02096050:66,0x02096094:60,0x020960d0:100,0x02096174:44,0x020961c8:144,0x02096258:48,0x02096288:228,0x0209636c:70,0x020963b4:248}
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
    copies = {
        'first': 'c5e589f10b24c0c65b958fb3bfba72f13082fad40bbf746e7b4bca0eca2f5014',
        'second': '56952e6af4d5359a64639857a5161226ef8b0dfbe03dc42845f95b87ec32b749',
        'third': '30f826545ad63496a80699a3ecb171ea811ed6704977ef298f69fe9b1eca0184',
        'fourth': '1f23794104c7e63183e62a3750fd4cf2f665797216ae90bef0f693b04b5f1f86',
        'fifth': 'b37ee51cd0ac9877e043f67e2ea7e8861b8d997a01d2eb0500bad4808e6fdd99',
        'sixth': '798cdf5c7ab3f9390eef05e8976812ad3ff23516ca203d22623ab155d4348a86'}
    same_owner_copies = {ROOT / f'evidence/lanes/parallel-wave20261105/dwc-auth-next/{name}/claim.json': digest for name, digest in copies.items()}
    for path, digest in same_owner_copies.items():
        assert sha256(path) == digest
        document = read_json(path)
        assert document['owner'] == old_claim['owner'] and document['coordinatorOwnershipAuthorized']
        assert all(row['id'] in own for row in document['claimedFunctions'])
        for row in document['claimedFunctions']:
            assert all(row[key] == own[row['id']][key] for key in ['processor', 'module', 'mode', 'address', 'bytes', 'targetSha256', 'sourceTarget'])
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        document = read_json(path)
        if path == ROOT / old_claim_name or path in same_owner_copies:
            document = dict(document, claimedFunctions=[row for row in document['claimedFunctions'] if row['id'] not in {r['id'] for r in rows}])
        protected.extend(spans(document))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        content = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(content).hexdigest()))
        protected.extend(spans(json.loads(content)[key]))
    symbols_name = 'config/arm9/symbols.txt'
    symbols = set((ROOT / symbols_name).read_text(encoding='utf-8').splitlines())
    relocs = set((ROOT / 'config/arm9/relocs.txt').read_text(encoding='utf-8').splitlines())
    from project import configuration, native_dependencies
    cfg = configuration(); native_dependencies(cfg)
    assert sha256(cfg['rom']) == cfg['romSha256'] == '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
    from qualify_arm9_thumb_reference_inputs_20261105 import derive
    image, base = derive(), 0x02000000
    assert hashlib.sha256(image).hexdigest() == 'ea530f917c534c3fa2b036288dd9e4551e3cbf68b5fc36713e1217704148534f'
    root = ROOT / proposal['newExclusivePaths']['sourceRoot']; assert not root.exists()
    for row in rows:
        start, length = int(row['address'], 0), row['bytes']
        assert row['id'] in own and row['id'] in selected
        for key in ['processor', 'module', 'mode', 'address', 'bytes', 'targetSha256']:
            assert own[row['id']][key] == row[key]
        current = selected[row['id']]
        assert not current.get('sourceUnit') and not current.get('states', {}).get('functionMatched')
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm9', 'main', 'thumb')
        assert not (ROOT / row['sourceTarget']).exists()
        canonical = [line for line in symbols if re.search(r'kind:function\(thumb,size=0x' + format(length, 'x') + r'\) addr:0x0*' + format(start, 'x') + r'(?:\s|$)', line)]
        assert len(canonical) == 1
        assert hashlib.sha256(image[start - base:start - base + length]).hexdigest() == row['targetSha256']
        assert not any(max(start, a) < min(start + length, b) for a, b in protected)
        for line in symbols:
            match = re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)(?:\s|$)', line)
            assert not match or not start < int(match[1], 0) < start + length
        assert all(item['record'] in relocs for item in row['originalRecords'])
    reference = ROOT / 'deps/reference/libntrdwc-ac-c6622266a9388d854443c659daf316fd9d1f540d'
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    claim_name = 'evidence/lanes/parallel-wave20261106/auth-resume-next/claim.json'
    assert not (ROOT / claim_name).exists()
    write_json(ROOT / claim_name, dict(owner='workflow_research', status='coordinator-admitted-source-scope-no-credit',
        createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=proposal['newExclusivePaths']['sourceRoot'],
        exclusiveWorkRoot='work/w6ar', helperPrefix=proposal['newExclusivePaths']['helperPrefix'],
        claimedFunctions=rows, sourceCredit=0, canonicalReferenceRoot=reference.relative_to(ROOT).as_posix(),
        originalHistoricalClaimUnchanged=dict(path=old_claim_name, sha256=sha256(ROOT / old_claim_name)),
        tableStorageOwnershipGranted=False, importedHelpersAndStorageCredit=0))
    board = ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'
    write_json(ROOT / 'evidence/lanes/parallel-wave20261106/auth-resume-next/coordinator-admission.json',
        dict(passed=True, sourceCredit=0, claim=claim_name, claimSha256=sha256(ROOT / claim_name),
            exclusiveSourceRoot=proposal['newExclusivePaths']['sourceRoot'], sharedDispatchUnchanged=True,
            actualDispatchSha256=sha256(board), functions=16, initializedCandidateBytes=2064,
            proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)),
            originalNativeAndStorageAdmissionGuardsRetained=True,
            onlySixteenPreviouslyOwnedUnacceptedIdentitiesResumed=True, oldClaimNotModified=True,
            exactSixHistoricalSameOwnerSubsetClaimsPreserved={path.relative_to(ROOT).as_posix(): digest for path, digest in same_owner_copies.items()},
            allCohortSpecificationsAndOtherClaimsExcluded=True, protectionPins=pins,
            allNativeSpansFreshlyDerivedFromOriginalRom=True, functionSourceAbsentAtAdmission=True,
            canonicalReferenceRoot=reference.relative_to(ROOT).as_posix(),
            noTableStorageOwnership=True, timeboxMinutes=25, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=16, initializedCandidateBytes=2064, sourceCredit=0))


if __name__ == '__main__':
    main()
