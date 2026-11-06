import hashlib
import json
import re
import subprocess
from project import ROOT, read_json, write_json, sha256, now
from admit_g2d_canvas_scope_v1_20261106 import spans
from qualify_arm9_thumb_reference_inputs_20261105 import derive


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/non-ready-source-scout/grid292-proposal.json'
    assert sha256(ROOT / proposal_name) == '194ba8a8e40aec0fca7f8b4350c251826e762271663960f750ad11bcb0ac461b'
    proposal = read_json(ROOT / proposal_name); row = proposal['claimedIdentity']; start, size = 0x020d0ad8, 292
    assert (row['program'], row['processor'], row['module'], row['mode'], int(row['address'], 0), row['bytes']) == ('', 'arm9', 'main', 'arm', start, size)
    old_name = proposal['previousOwnerClaim']['path']
    assert old_name == 'evidence/lanes/parallel-wave20261105/main-tail-next/claim.json'
    assert sha256(ROOT / old_name) == proposal['previousOwnerClaim']['sha256'] == '170476b838a74f5d77c6b48c8327c99f469a65c110ddcf76c9b0b49fe4f338bc'
    old = read_json(ROOT / old_name); assert old['owner'] == 'repo_audit/main-tail-next'
    own = [item for item in old['claimedFunctions'] if item['id'] == row['id']]
    assert len(own) == 1 and own[0] == row
    revision = '142f10ae8d094bf5ae27dc09a017b6ba3a19adeb'
    raw = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = [json.loads(line) for line in raw.splitlines()]; current = next(item for item in ledger if item['id'] == row['id'])
    assert current['bytes'] == size and not current['states']['functionMatched'] and not current['sourceUnit']
    protected = list(spans([item for item in ledger if item['states']['functionMatched'] or item.get('sourceUnit')]))
    pins = [dict(gitObject=revision + ':ledger/functions.jsonl', sha256=hashlib.sha256(raw).hexdigest())]
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        name = path.relative_to(ROOT).as_posix(); pins.append(dict(path=name, sha256=sha256(path))); document = read_json(path)
        if name == old_name:
            document = dict(document, claimedFunctions=[item for item in document['claimedFunctions'] if item['id'] != row['id']])
        protected.extend(spans(document))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        content = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(content).hexdigest()))
        protected.extend(spans(json.loads(content)[key]))
    assert not any(max(start, a) < min(start + size, b) for a, b in protected)
    for pin in proposal['actualInputPins']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    image = derive(); base = 0x02000000; native = image[start - base:start - base + size]
    assert hashlib.sha256(native).hexdigest() == row['targetSha256'] == proposal['targetSha256']
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text(encoding='utf-8').splitlines()
    assert f'func_{start:08x} kind:function(arm,size=0x{size:x}) addr:0x{start:08x}' in symbols
    for line in symbols:
        match = re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)(?:\s|$)', line)
        assert not match or not start < int(match[1], 0) < start + size
    relocs = (ROOT / 'config/arm9/relocs.txt').read_text(encoding='utf-8').splitlines()
    actual = [line for line in relocs if (match := re.match(r'from:(0x[0-9a-fA-F]+)', line)) and start <= int(match[1], 0) < start + size]
    assert actual == [item['originalRecord'] for item in proposal['originalOutgoingNamespaceWitnesses']]
    from link_runtime_unit import relocation_rows
    assert relocation_rows(ROOT / proposal['object']['path'], 'native_main_020d0ad8') == [item['actualObjectRelocation'] for item in proposal['originalOutgoingNamespaceWitnesses']]
    for item in proposal['originalOutgoingNamespaceWitnesses'] + proposal['originalIncomingWitnesses']:
        origin = int(re.match(r'from:(0x[0-9a-fA-F]+)', item['originalRecord'])[1], 0)
        assert item['originalRecord'] in relocs
        assert image[origin - base:origin - base + 4].hex() == item.get('originalWord', item.get('word'))
        if item.get('canonicalTargetRecord'):
            assert item['canonicalTargetRecord'] in symbols
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/main-grid-resume-next'
    source_root = 'src/runtime/parallel_wave20261106/main-grid-resume-next'
    assert not folder.exists() and not (ROOT / source_root).exists() and not (ROOT / 'work/w6gg').exists()
    assert not list(ROOT.glob('wave20261106_main_grid_resume_*.py'))
    name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / name, dict(owner='workflow_research', status='coordinator-admitted-source-scope-no-credit',
        sourceCredit=0, createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=source_root,
        exclusiveWorkRoot='work/w6gg', helperPrefix='wave20261106_main_grid_resume_', claimedFunctions=[row],
        exactHistoricalIdentityTransferredFrom='repo_audit/main-tail-next', oldClaimAndSourceAndReportsUnchanged=True))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, claim=name,
        claimSha256=sha256(ROOT / name), exclusiveSourceRoot=source_root, sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'),
        functions=1, initializedCandidateBytes=292, sourceRevision=revision,
        proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)), protectionPins=pins,
        onlyExact292OwnershipPrivatelyProjected=True, actualOriginalNineRelocationsAndTwoIncomingWordsVerified=True,
        freshC99GenuineLinkModelsCopiedRootAndCommonReadyStillRequired=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=1, initializedCandidateBytes=292, sourceCredit=0))


if __name__ == '__main__':
    main()
