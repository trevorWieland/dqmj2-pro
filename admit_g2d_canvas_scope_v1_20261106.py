import hashlib
import json
import re
import subprocess
from project import ROOT, read_json, write_json, sha256, now
from qualify_arm9_thumb_reference_inputs_20261105 import derive


def spans(node, parent=None):
    parent = parent or {}
    if isinstance(node, list):
        for item in node:
            yield from spans(item, parent)
    elif isinstance(node, dict):
        context = {key: node.get(key, parent.get(key)) for key in ['program', 'processor', 'module']}
        namespace = (context['program'] or '', context['processor'] or 'arm9', context['module'])
        size = node.get('storedBytes', node.get('bytes', node.get('size')))
        if namespace == ('', 'arm9', 'main') and node.get('address') and size:
            start = int(node['address'], 0) if isinstance(node['address'], str) else node['address']
            if isinstance(size, str):
                size = len(bytes.fromhex(size)) if 'instruction' in node else int(size, 0)
            assert type(size) is int and size > 0
            yield start, start + size
        for item in node.values():
            yield from spans(item, context)


def main():
    proposal_name = 'evidence/lanes/parallel-wave20261106/ov006-crypto-utility-next/g2d-canvas-resumption-proposal-v1.json'
    assert sha256(ROOT / proposal_name) == 'd53e2e8278425056492ef7ca86a16c04fd45dca90c23367d2fc72262ac6079f9'
    proposal = read_json(ROOT / proposal_name); rows = proposal['entries']
    expected = {0x02086ba8: 320, 0x02086d18: 256, 0x02087334: 160, 0x02087674: 172,
        0x02087720: 156, 0x020877bc: 352, 0x02087a48: 452, 0x02087c0c: 256,
        0x02087d0c: 200, 0x02087dd4: 112, 0x02087e84: 180, 0x02087fa8: 576,
        0x020881e8: 408, 0x020885d0: 316, 0x02089524: 108, 0x02089a14: 144}
    assert len(rows) == 16 and {int(row['address'], 0): row['bytes'] for row in rows} == expected
    assert sum(expected.values()) == 4168
    revision = '9e6aea5ee032dd24a884041a098b669534d88629'
    raw = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    ledger = [json.loads(line) for line in raw.splitlines()]; selected = {row['id']: row for row in ledger}
    protected = list(spans([row for row in ledger if row['states']['functionMatched'] or row.get('sourceUnit')]))
    pins = [dict(gitObject=revision + ':ledger/functions.jsonl', sha256=hashlib.sha256(raw).hexdigest())]
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) |
        set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        protected.extend(spans(read_json(path)))
    for name, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        content = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
        pins.append(dict(gitObject=revision + ':' + name, sha256=hashlib.sha256(content).hexdigest()))
        protected.extend(spans(json.loads(content)[key]))
    for pin in proposal['nativePins'] + proposal['primary']['files'] + proposal['existingFrozenSourceContextPins'] + [proposal['fingerprintAudit']]:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    image = derive(); base = 0x02000000
    symbols = (ROOT / 'config/arm9/symbols.txt').read_text(encoding='utf-8').splitlines()
    relocs = (ROOT / 'config/arm9/relocs.txt').read_text(encoding='utf-8').splitlines()
    functions = []
    for row in rows:
        start, size = int(row['address'], 0), row['bytes']
        assert (row['program'], row['processor'], row['module'], row['mode']) == ('', 'arm9', 'main', 'arm')
        current = selected[row['id']]
        assert current['bytes'] == size and current['mode'] == 'arm'
        assert not current['states']['functionMatched'] and not current['sourceUnit']
        assert not any(max(start, a) < min(start + size, b) for a, b in protected)
        assert row['canonicalInventoryRecord'] == f'func_{start:08x} kind:function(arm,size=0x{size:x}) addr:0x{start:08x}'
        assert row['canonicalInventoryRecord'] in symbols
        for line in symbols:
            match = re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)(?:\s|$)', line)
            assert not match or not start < int(match[1], 0) < start + size
        actual_relocs = [line for line in relocs if (match := re.match(r'from:(0x[0-9a-fA-F]+)', line)) and start <= int(match[1], 0) < start + size]
        assert actual_relocs == row['originalRelocationRecords']
        assert hashlib.sha256(image[start - base:start - base + size]).hexdigest() == row['targetSha256']
        functions.append(row)
    equivalents = []
    for target, accepted, size in [(0x02087fa8, 0x02035788, 576), (0x020881e8, 0x020359c8, 408)]:
        bodies, signatures = [], []
        assert any(row['address'] == hex(accepted) and row['bytes'] == size and row['states']['functionMatched']
            and row['processor'] == 'arm9' and row['module'] == 'main' and row['mode'] == 'arm' for row in ledger)
        for address in [target, accepted]:
            body = bytearray(image[address - base:address - base + size]); signature = []
            for line in relocs:
                match = re.match(r'from:(0x[0-9a-fA-F]+) kind:(\S+)', line)
                if match and address <= int(match[1], 0) < address + size:
                    offset = int(match[1], 0) - address
                    assert offset % 4 == 0 and offset + 4 <= size
                    signature.append((offset, match[2])); body[offset:offset + 4] = bytes(4)
            bodies.append(body); signatures.append(signature)
        assert bodies[0] == bodies[1] and signatures[0] == signatures[1]
        equivalents.append(dict(target=hex(target), accepted=hex(accepted), bytes=size,
            normalizedWholeBodySha256=hashlib.sha256(bodies[0]).hexdigest(), originalRelocationOffsetsAndKinds=signatures[0]))
    assert all(not pin.get('path') or sha256(ROOT / pin['path']) == pin['sha256'] for pin in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/g2d-canvas-next'
    source_root = 'src/runtime/parallel_wave20261106/g2d-canvas-next'
    assert not folder.exists() and not (ROOT / source_root).exists() and not (ROOT / 'work/w6gc').exists()
    assert not list(ROOT.glob('wave20261106_g2d_canvas_next_*.py'))
    claim_name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / claim_name, dict(owner='ds_tooling_research', status='coordinator-admitted-source-scope-no-credit',
        sourceCredit=0, createdUtc=now(), sourceRevision=revision, exclusiveSourceRoot=source_root,
        exclusiveWorkRoot='work/w6gc', helperPrefix='wave20261106_g2d_canvas_next_', claimedFunctions=functions,
        noHistoricalClaimOwnershipInvented=True, historicalAttemptsRemainImmutable=True))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, claim=claim_name,
        claimSha256=sha256(ROOT / claim_name), exclusiveSourceRoot=source_root, sharedDispatchUnchanged=True,
        actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'), functions=16,
        initializedCandidateBytes=4168, sourceRevision=revision,
        proposal=dict(path=proposal_name, sha256=sha256(ROOT / proposal_name)), protectionPins=pins,
        allHistoricalClaimsCohortSpecificationsAndAcceptedStorageExcluded=True,
        independentOriginalNativeWholeBodyEquivalences=equivalents, equivalentBodiesHaveNoAdditionalCreditYet=True,
        primarySourceAndExistingAcceptedContextPinsVerified=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=16, initializedCandidateBytes=4168, sourceCredit=0))


if __name__ == '__main__':
    main()
