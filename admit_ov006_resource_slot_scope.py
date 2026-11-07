import hashlib
import json
import re
import subprocess

import match_runtime
from project import ROOT, configuration, now, read_json, sha256, write_json
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_child_arm9_boundary_family_readonly_v4 import derive
from elftools.elf.elffile import ELFFile
from elftools.elf.relocation import RelocationSection


def main():
    name = 'evidence/lanes/parallel-wave20261106/ov006-resource-slot-scout/proposal.json'
    assert sha256(ROOT / name) == 'eee5e340fd03288a791bd5cc187cb27b139281e64d4c8396217d4a7da13b5f83'
    proposal = read_json(ROOT / name)
    for pin in proposal['pins']:
        assert sha256(ROOT / pin['path']) == pin['sha256'], pin['path']
    revision = '14ac8dcd6f8ab0009e5dd54d73cf31c928540776'
    baseline = [json.loads(line) for line in subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT).splitlines()]
    current = [json.loads(line) for line in (ROOT / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines()]
    protected = list(intervals([r for r in current if r['states']['functionMatched'] or r.get('sourceUnit')]))
    pins = []
    for path in sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) | set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json'))):
        protected.extend(intervals(read_json(path))); pins.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
    for path, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        protected.extend(intervals(read_json(ROOT / path)[key])); pins.append(dict(path=path, sha256=sha256(ROOT / path)))
    config = configuration(); assert sha256(config['rom']) == config['romSha256']
    from ndspy.rom import NintendoDSRom
    rom = NintendoDSRom(config['rom'].read_bytes()); overlays = rom.loadArm9Overlays([6])
    claimed = []; reviews = []
    for entry in proposal['entries']:
        identity = entry['identity']; module = identity['module']; number = int(module[2:]); start = int(identity['address'], 0); size = identity['bytes']
        assert module=='ov006'and start in {0x021e6c44,0x021e6ef4,0x021e7210,0x021e7268,0x021e73ac,0x021e749c,0x021e75ec,0x021e7608,0x021e76f0,0x021e775c,0x021e79b0,0x021e7ab0,0x021e7b00}
        assert not any((p, c, m) == ('', 'arm9', module) and max(a, start) < min(b, start + size) for p, c, m, a, b in protected)
        original = next(r for r in current if (r.get('program') or '', r['processor'], r['module'], int(r['address'], 0)) == ('', 'arm9', module, start))
        assert not original['states']['functionMatched'] and not original.get('sourceUnit') and original['bytes'] == size
        overlay = overlays[number]; image = bytes(overlay.data); base = overlay.ramAddress
        assert base == identity['base'] and image == (ROOT / identity['binary']).read_bytes()
        assert hashlib.sha256(image).hexdigest() == identity['inputModuleSha256']
        body = image[start - base:start - base + size]; assert hashlib.sha256(body).hexdigest() == identity['targetSha256']
        symbols = (ROOT / f'config/arm9/overlays/{module}/symbols.txt').read_text(encoding='utf-8').splitlines()
        assert entry['canonicalInventoryRecord'] in symbols
        starts = {int(m[1], 0) for line in symbols if (m := re.search(r'kind:function\([^)]*\) addr:(0x[0-9a-fA-F]+)', line))}
        assert not any(start < address < start + size for address in starts)
        flow = derive(image, base, start, min(a for a in starts if a > start), 'arm', {(a, 'arm') for a in starts})
        assert flow == entry['fullNativeCfgLiteralReturnProof'] and flow['complete'] and flow['bytes'] == size
        assert all(e['originalEntryLRProven'] and e['stackDelta'] == 0 for e in flow['exits'])
        outgoing = [line for line in (ROOT / f'config/arm9/overlays/{module}/relocs.txt').read_text(encoding='utf-8').splitlines() if (m := re.match(r'from:(0x[0-9a-fA-F]+)', line)) and start <= int(m[1], 0) < start + size]
        assert outgoing == entry['originalRelocationRecords']
        incoming = []
        for path in sorted((ROOT / 'config/arm9').rglob('relocs.txt')):
            for line in path.read_text(encoding='utf-8').splitlines():
                m = re.search(r' to:(0x[0-9a-fA-F]+) module:(.+)$', line)
                if m and (int(m[1], 0) & ~1) == start and f'overlay({number})' in m[2]:
                    assert m[2] == f'overlay({number})'
                    incoming.append((path.relative_to(ROOT).as_posix(), line))
        assert incoming == [(r['sourcePath'], r['record']) for r in entry['allOriginalIncomingRecords']]
        claimed.append(dict(identity, id=original['id'], originalRelocationRecords=outgoing, originalIncomingRecords=entry['allOriginalIncomingRecords']))
        reviews.append(dict(identity=identity,independentlyDerivedNativeFlow=flow,originalIncomingReferences=incoming,originalRelocationRecords=outgoing))
    assert len(claimed)==13 and sum(r['bytes']for r in claimed)==2616
    assert all(sha256(ROOT / p['path']) == p['sha256'] for p in pins)
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/ov006-resource-slot-next'
    assert not folder.exists() and not (ROOT / proposal['proposedSourceRoot']).exists() and not (ROOT / proposal['proposedWorkRoot']).exists()
    assert not list(ROOT.glob(proposal['proposedHelperPrefix'] + '*.py'))
    claim_name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / claim_name, dict(owner='workflow_research', status='coordinator-admitted-source-scope-no-credit', sourceCredit=0, createdUtc=now(),
        exclusiveSourceRoot=proposal['proposedSourceRoot'], exclusiveWorkRoot=proposal['proposedWorkRoot'], helperPrefix=proposal['proposedHelperPrefix'], claimedFunctions=claimed,
        experimentBudget='Actual measured context only. Preserve12-byte array stride vs8-byte consumedprefix and signed/unsigned3-byte tuples; odddata addresses retainbit0. No global/frozenheader migrations or register/profile grids. Proper call prototypes, genuine links, models, negatives and copied-root proof before Ready; no helper or storage credit.'))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, functions=13, initializedCandidateBytes=2616, claim=claim_name, claimSha256=sha256(ROOT / claim_name),
        exclusiveSourceRoot=proposal['proposedSourceRoot'], sharedDispatchUnchanged=True, actualDispatchSha256=sha256(ROOT / 'evidence/lanes/parallel-wave20261102/dispatch.json'),
        proposal=dict(path=name, sha256=sha256(ROOT / name)), protectionPins=pins, independentReviews=reviews, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=13, bytes=2616, sourceCredit=0))


if __name__ == '__main__': main()
