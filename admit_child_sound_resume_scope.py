"""Independently measure one inactive child scope and transfer only its196B."""
import hashlib
import json
import subprocess

import match_runtime
from project import ROOT, configuration, native_dependencies, now, read_json, sha256, write_json
from wave20261106_nns_primary_readonly_scout import intervals
from wave20261106_child_arm9_boundary_family_readonly_v4 import derive, qualify_return_tokens


def main():
    name = 'evidence/lanes/parallel-wave20261106/child-arm9-boundary-handoff/proposal.json'
    assert sha256(ROOT / name) == 'd5fc5354ccc60c1b3bcce80b530d45ffa3b6d4369c16af9737082aae46f3d20d'
    proposal = read_json(ROOT / name)
    item = proposal['reservedSound196']
    for pin in proposal['actualInputPins']:
        assert sha256(ROOT / pin['path']) == pin['sha256'], pin['path']
    for pin in proposal['gitPins']:
        content = subprocess.check_output(['git', 'show', pin['gitObject']], cwd=ROOT)
        assert hashlib.sha256(content).hexdigest() == pin['sha256']
    old_name = item['originalClaim']['path']
    old = read_json(ROOT / old_name)
    assert old['owner'] == 'workflow_research' and item['activeSourceWorkInOldScope'] is False
    assert sha256(ROOT / old_name) == item['originalClaim']['sha256']
    native_dependencies(configuration())
    import utility_runtime
    from ndspy.rom import NintendoDSRom
    config = configuration()
    assert sha256(config['rom']) == config['romSha256']
    game = NintendoDSRom(config['rom'].read_bytes())
    assert game.files[game.filenames.idOf('dwc/utility.bin')] == (ROOT / 'extract/files/dwc/utility.bin').read_bytes()
    layout, files = utility_runtime.derive()
    module = next(m for m in layout['modules'] if m['id'] == 'utility-child-arm9-main')
    image = files[ROOT / module['binary']]
    assert image == (ROOT / module['binary']).read_bytes()
    assert hashlib.sha256(image).hexdigest() == 'af25c028552d9de7428f5393757507b3c029e80f22c9cc44e94e45103f0814d0'
    base = int(module['base'], 0)
    ghidra = [f for f in read_json(ROOT / 'evidence/utility/ghidra-arm9.json')['functions'] if f['module'] == module['id']]
    starts = {int(f['address'], 0) for f in ghidra}
    known = {(int(f['address'], 0), f['mode']) for f in ghidra}
    flows = []
    for address, size in ((0x02006eb8, 196), (0x02006f7c, 136)):
        record = next(f for f in ghidra if int(f['address'], 0) == address)
        assert record['mode'] == 'arm' and len(record['ranges']) == 1
        limit = min(a for a in starts if a > address)
        flow = derive(image, base, address, limit, 'arm', known)
        assert flow['complete'] and not flow['issues'] and not flow['gaps']
        assert flow['bytes'] == flow['codeBytes'] == size and flow['literalBytes'] == 0
        assert all(e['originalEntryLRProven'] and e['stackDelta'] == 0 for e in flow['exits'])
        flows.append(flow)
    assert flows[0]['bodySha256'] == item['identity']['targetSha256']
    call = next(c for c in flows[1]['calls'] if c['origin'] == '0x2006ff8')
    assert call['target'] == '0x2006eb8' and call['targetMode'] == 'arm' and call['nativeWord'] == 'aeffffeb'
    controls = qualify_return_tokens()
    assert controls['passed'] and controls['positiveCases'] == 7 and controls['negativeCases'] == 17
    program = 'dwc/utility.bin/move/child.srl'
    ledger = [json.loads(line) for line in (ROOT / 'ledger/functions.jsonl').read_text(encoding='utf-8').splitlines()]
    target = next(r for r in ledger if (r.get('program') or '', r['processor'], r['module'], int(r['address'], 0)) == (program, 'arm9', module['id'], 0x02006eb8))
    assert not target['states']['functionMatched'] and not target.get('sourceUnit')
    protected = list(intervals([r for r in ledger if r['states']['functionMatched'] or r.get('sourceUnit')]))
    pins = []
    paths = sorted(set((ROOT / 'evidence/lanes').rglob('claim.json')) | set((ROOT / 'evidence/lanes').rglob('data-claim.json')) | set(ROOT.glob('cohort*-*specification.json')))
    for path in paths:
        relative = path.relative_to(ROOT).as_posix()
        document = read_json(path)
        pins.append(dict(path=relative, sha256=sha256(path)))
        if relative == old_name:
            transferred = [f for f in document['functions'] if int(f['address'], 0) == 0x02006eb8]
            assert len(transferred) == 1 and transferred[0] == item['originalAllocation']
            document = dict(document, functions=[f for f in document['functions'] if int(f['address'], 0) != 0x02006eb8])
        protected.extend(intervals(document))
    for relative, key in [('ledger/data.json', 'records'), ('ledger/linkage.json', 'regions')]:
        protected.extend(intervals(read_json(ROOT / relative)[key]))
        pins.append(dict(path=relative, sha256=sha256(ROOT / relative)))
    assert not [(a, b) for p, c, m, a, b in protected if (p, c, m) == (program, 'arm9', module['id']) and max(a, 0x02006eb8) < min(b, 0x02006f7c)]
    folder = ROOT / 'evidence/lanes/parallel-wave20261106/child-snd-resume-next'
    assert not folder.exists() and not (ROOT / item['proposedSourceRoot']).exists() and not (ROOT / item['proposedWorkRoot']).exists()
    assert not list(ROOT.glob(item['proposedHelperPrefix'] + '*.py'))
    row = dict(item['identity'], id=target['id'], binary=module['binary'], base=base, boundaryMeasuredIndependently=True)
    claim_name = (folder / 'claim.json').relative_to(ROOT).as_posix()
    write_json(ROOT / claim_name, dict(owner='workflow_research', status='coordinator-admitted-source-scope-no-credit', sourceCredit=0,
        createdUtc=now(), exclusiveSourceRoot=item['proposedSourceRoot'], exclusiveWorkRoot=item['proposedWorkRoot'],
        helperPrefix=item['proposedHelperPrefix'], claimedFunctions=[row], exactIdentityTransferredFromInactiveClaim=item['originalClaim'],
        experimentBudget='One actual accepted compiler context; actual child imports/layout, genuine links, models, negative controls and copied-root proof. No profile or lifetime grids.'))
    write_json(folder / 'coordinator-admission.json', dict(passed=True, sourceCredit=0, functions=1, initializedCandidateBytes=196,
        claim=claim_name, claimSha256=sha256(ROOT / claim_name), exclusiveSourceRoot=item['proposedSourceRoot'],
        proposal=dict(path=name, sha256=sha256(ROOT / name)), protectionPins=pins, nativeFlows=flows, returnTokenControls=controls,
        oldClaimUnchanged=True, onlyExact196IdentityTransferred=True, globalBoundaryLedgerUnchanged=True,
        entryEvidence='Original Ghidra ARM entries, independently complete136B native ARM caller, actual ARM BL to196B entry, and independently complete balanced-return196B body.',
        transitiveRuntimeReachabilityFromApplicationEntryProven=False, noNativeWindowsOrGameCompletionClaim=True, generatorSha256=sha256(__file__)))
    print(dict(passed=True, functions=1, initializedCandidateBytes=196, sourceCredit=0))


if __name__ == '__main__':
    main()
