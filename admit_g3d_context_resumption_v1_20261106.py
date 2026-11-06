import hashlib
import json
import re
import subprocess
from project import ROOT, read_json, write_json, sha256, now
from admit_g2d_canvas_scope_v1_20261106 import spans
from qualify_arm9_thumb_reference_inputs_20261105 import derive


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/g2d-canvas-next/g3d-resumption-proposal-v1.json'
    assert sha256(ROOT / proposal_name) == 'ca52f68d3dff1fa2dc9d7da89d32203271b70f30778ef5fc6bc611337432ab13'
    proposal = read_json(ROOT / proposal_name); rows = proposal['entries']
    expected = {0x02031b44: 940, 0x02032a38: 344, 0x02032cec: 488}
    assert len(rows) == 3 and {int(row['address'], 0): row['bytes'] for row in rows} == expected
    revision = '142f10ae8d094bf5ae27dc09a017b6ba3a19adeb'
    raw = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = [json.loads(line) for line in raw.splitlines()]; selected = {row['id']: row for row in ledger}
    ids = {row['id'] for row in rows}
    protected = list(spans([row for row in ledger if row['states']['functionMatched'] or row.get('sourceUnit')]))
    pins = [dict(gitObject=revision + ':ledger/functions.jsonl', sha256=hashlib.sha256(raw).hexdigest())]
    old = {
        'evidence/lanes/parallel-wave20261102/main-sdk-third/claim.json':
            ('d326107e1c58092c672cc81d8dc6a56b608ef71b8108bd73ef051992a8e55bde', 'ds_tooling_research/main-sdk-third'),
        'evidence/lanes/parallel-wave20261104/main-sdk-residual/claim.json':
            ('1b30abd58d7d0171425fb3580d1208038277e1537945fe83feb13b4b8fa7044a', 'ds_tooling_research/main-sdk-residual')}
    for name, (digest, owner) in old.items():
        assert sha256(ROOT / name) == digest
        claim = read_json(ROOT / name); assert claim['owner'] == owner
        own = {row['id']: row for row in claim['claimedFunctions'] if row['id'] in ids}
        assert set(own) == ids
        for row in rows:
            for key in ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'targetSha256']:
                assert own[row['id']][key] == row[key]
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        name = path.relative_to(ROOT).as_posix(); pins.append(dict(path=name, sha256=sha256(path)))
        document = read_json(path)
        if name in old:
            document = dict(document, claimedFunctions=[row for row in document['claimedFunctions'] if row['id'] not in ids])
        protected.extend(spans(document))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        content = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(content).hexdigest()))
        protected.extend(spans(json.loads(content)[key]))
    for pin in proposal['nativePins'] + proposal['primary']['files'] + proposal['priorAttemptInventory']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    image = derive(); base = 0x02000000
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text(encoding='utf-8').splitlines()
    relocs = (ROOT / 'config/arm9/relocs.txt').read_text(encoding='utf-8').splitlines()
    for row in rows:
        start, size = int(row['address'], 0), row['bytes']; current = selected[row['id']]
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm9', 'main', 'arm')
        assert current['bytes'] == size and current['mode'] == 'arm' and not current['states']['functionMatched'] and not current['sourceUnit']
        assert not any(max(start, a) < min(start + size, b) for a, b in protected)
        assert row['canonicalInventoryRecord'] == f'func_{start:08x} kind:function(arm,size=0x{size:x}) addr:0x{start:08x}'
        assert row['canonicalInventoryRecord'] in symbols
        for line in symbols:
            match = re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)(?:\s|$)', line)
            assert not match or not start < int(match[1], 0) < start + size
        actual = [line for line in relocs if (match := re.match(r'from:(0x[0-9a-fA-F]+)', line)) and start <= int(match[1], 0) < start + size]
        assert actual == row['originalRelocationRecords']
        assert hashlib.sha256(image[start - base:start - base + size]).hexdigest() == row['targetSha256']
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/g3d-context-next'; source_root = proposal['proposedSourceRoot']
    assert source_root == 'src/runtime/parallel_wave20261106/g3d-context-next'
    assert not folder.exists() and not (ROOT / source_root).exists() and not (ROOT / 'work/w6gn').exists()
    assert not list(ROOT.glob('wave20261106_g3d_context_next_*.py'))
    name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / name, dict(owner='ds_tooling_research', status='coordinator-admitted-source-scope-no-credit',
        sourceCredit=0, createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=source_root,
        exclusiveWorkRoot='work/w6gn', helperPrefix='wave20261106_g3d_context_next_', claimedFunctions=rows,
        historicalExactOwnIdentitiesResumedWithoutEditingClaims=True, experimentBudget=proposal['experimentBudget']))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, claim=name,
        claimSha256=sha256(ROOT / name), exclusiveSourceRoot=source_root, sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'),
        functions=3, initializedCandidateBytes=1772, sourceRevision=revision,
        proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)), protectionPins=pins,
        onlyExactThreeIdentitiesInTwoPinnedOwnHistoricalClaimsProjected=True,
        allOtherClaimsPendingSpecificationsAcceptedSourceDataAndLinkageProtected=True,
        nativeWholeExtentsAndPrimaryAndPriorAttemptsVerified=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=3, initializedCandidateBytes=1772, sourceCredit=0))


if __name__ == '__main__':
    main()
