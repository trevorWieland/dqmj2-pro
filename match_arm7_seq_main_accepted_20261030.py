import copy
from project import ROOT, configuration, read_json, sha256, write_json
from arm7_state import runtime_state
from discontiguous_boundaries_20261030 import reconcile
import match_arm7_seq_main_proposed_20261030 as proposal

POLICY = 'evidence/regions/discontiguous-boundaries/arm7-037fff54-20261030.json'
SOURCE = 'src/arm7/20261030_seq_main/native_arm7_wram_037fff54.c'


def main():
    path = ROOT / POLICY
    if not path.is_file():
        raise ValueError('Reviewed boundary sidecar is not activated; source acceptance remains withheld')
    policy = read_json(path)
    if not policy.get('activationPerformed'):
        raise ValueError('Boundary policy activation is not recorded')
    modules, candidates, layout = runtime_state()
    revised = reconcile(candidates, modules, [(POLICY, policy)])
    row = next(x for x in revised if x['module'] == 'arm7-wram' and int(x['address'], 0) == 0x037FFF54)
    if row['size'] != 352 or not row['boundaryVerified']:
        raise ValueError('Reviewed canonical span is not352')
    original = read_json(ROOT / 'evidence/attempts/arm7-seq-main-proposed-20261030.json')
    controls = read_json(ROOT / 'evidence/verification/arm7-discontiguous-amendment-controls-20261030.json')
    if controls['controls'] != 15 or controls['status'] != 'passed':
        raise ValueError('Independent coordinator boundary controls are incomplete')
    pin = read_json(proposal.PROFILE)['matches'][0]
    if sha256(ROOT / SOURCE) != pin['sourceSha256']:
        raise ValueError('Promoted ordinary C differs from independently tested proposal')
    pin = dict(pin, source=SOURCE)
    proposal.WORK = ROOT / 'work/arm7-bulk-20261030/seq-main-accepted-61'
    entry = proposal.build(pin)
    if not entry['exactAfterRealMwLink'] or entry['oracle']['actualOriginalAndCompiledReturns'] != 790:
        raise ValueError('Promoted caller compilation/native proof failed')
    entry.update(ordinaryFunctionCredit=1, sourceCreditWithheldPendingSeparateBoundaryReview=False,
                 originalObjectScaffolding=False, implementationFamily='typed-reviewed-complete-sequence-main-caller')
    entry['boundaries'] = dict(entry['boundaries'], migrationApproved=True,
        sourceCreditWithheldPendingSeparateCoordinatorBoundaryReview=False,
        coordinatorPolicy={'path': POLICY, 'sha256': sha256(path)},
        coordinatorControls={'path': 'evidence/verification/arm7-discontiguous-amendment-controls-20261030.json',
                             'sha256': sha256(ROOT / 'evidence/verification/arm7-discontiguous-amendment-controls-20261030.json')})
    report = copy.deepcopy(original)
    report.update(matches=[entry], sourceAcceptanceCredit=352, matchedFunctions=1, matchedBytes=352,
                  boundaryMigrationApproved=True, coordinatorSidecar={'path': POLICY, 'sha256': sha256(path)},
                  originalProposalPreserved=True, wholeModuleLinked=False, sourceReconstructionComplete=False)
    paths = [x['path'] for x in original['generatorSources']]
    paths += ['match_arm7_seq_main_accepted_20261030.py', 'discontiguous_boundaries_20261030.py',
              'verify_discontiguous_boundaries_20261030.py', POLICY,
              'evidence/verification/arm7-discontiguous-amendment-controls-20261030.json',
              'evidence/attempts/arm7-seq-main-proposed-20261030.json']
    report['generatorSources'] = [{'path': p, 'sha256': sha256(ROOT / p)} for p in dict.fromkeys(paths)]
    report['generator'] = 'match_arm7_seq_main_accepted_20261030.py'
    report['generatorSha256'] = sha256(ROOT / report['generator'])
    destination = ROOT / 'evidence/matches/arm7-seq-main-accepted-20261030.json'
    write_json(destination, report)
    print({'functions': 1, 'bytes': 352, 'actualTopReturns': 790, 'reportSha256': sha256(destination)})


if __name__ == '__main__':
    main()
