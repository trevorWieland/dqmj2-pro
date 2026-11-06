from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    previous_packages = [read_json(ROOT / name) for name in ['cohort119-package-v2-20261101.json',
        'cohort120-package-20261101.json', 'cohort121-package-20261101.json']]
    prior_specs = [read_json(ROOT / f'cohort{number}-specification-20261101.json') for number in [119, 120, 121]]
    manifests = sorted({name for package in previous_packages for name in package['manifests']} | {
        'evidence/lanes/save-core/menu-resource-flows185-ready-20261101.json',
        'provenance/arm7-core119-pair188-functional-handoff-20261101.json',
        'provenance/handoffs/ov005-helpers664-curve-and-point-table-20261101.json',
        'provenance/native-random-word152-and-bitcast-v2-ready-20261101.json'})
    counts = {}
    for name in manifests:
        fields = {}
        for field, rows in read_json(ROOT / name).items():
            if ('required' in field.lower() or 'existing' in field.lower()) and isinstance(rows, list):
                if not all(isinstance(row, dict) and 'path' in row and 'sha256' in row for row in rows):
                    continue
                for row in rows:
                    assert sha256(ROOT / row['path']) == row['sha256'], row['path']
                fields[field] = len(rows)
        counts[name] = fields
    write_json(ROOT / 'evidence/verification/cohort119-expanded-existing-inputs-20261101.json', dict(passed=True, packets=counts))
    packets = [packet for spec in prior_specs for packet in spec['packets']]
    packets.extend([dict(report='evidence/matches/mechanics-save-20261101-lane-menu-resource-flows.json',
        producer=['match_mechanics_save_20261101_lane_menu_resource_flows.py'], directProducer=False),
        dict(report='evidence/matches/ov005-20261101-helpers664.json',
        producer=['match_ov005_helpers664_20261101.py'], directProducer=False)])
    additions = [{key: row[key] for key in ['module', 'mode', 'address', 'bytes']}
        for packet in packets for row in read_json(ROOT / packet['report'])['matches']]
    assert len(additions) == 11 and sum(row['bytes'] for row in additions) == 1556
    commands = [command for spec in prior_specs for command in spec.get('postSealCommands', [])]
    commands.extend([['validate_arm7_core119_pair188_functional_20261101.py'],
        ['probe_same_width_bitcasts_v2_20261101.py'], ['verify_windows_random_word152_20261101.py'],
        ['build_android_random_word152_20261101.py']])
    oracles = [oracle for spec in prior_specs for oracle in spec.get('oracles', [])]
    oracles.extend([dict(report='evidence/portability/random-word152-windows32-20261101.json',
        reproduce=['verify_windows_random_word152_20261101.py']),
        dict(report='evidence/portability/android-random-word152-build-20261101.json',
        reproduce=['build_android_random_word152_20261101.py'])])
    specification = dict(cohort=119, previousAcceptedCohort=118, migrations=[], packets=packets,
        expectedAdditions=additions, postSealCommands=commands, oracles=oracles,
        consolidatesPreviouslyWaitingPlans=[119, 120, 121, 122], originalChecksRetained=True)
    write_json(ROOT / 'cohort119-expanded-specification-20261101.json', specification)
    pending = read_json(ROOT / 'cohort118-specification-20261101.json')
    write_json(ROOT / 'cohort119-expanded-prerequisite-exclusion-20261101.json', dict(sourceCredit=0,
        purpose='Pending118 identity exclusion only; no accepted coverage', packets=pending['packets'],
        expectedAdditions=pending['expectedAdditions']))
    archives = sorted({name for package in previous_packages for name in package['archives']} | {
        'save-menu-resource185-20261101', 'arm7-core119-pair188-20261101', 'ov005-helpers664-20261101',
        'root-native-research-20261101'})
    extra = sorted({name for package in previous_packages for name in package['extra']} | {
        'prepare_cohort119_expanded_20261101.py', 'stage_cohort119_expanded_20261101.py',
        'run_next_source_package_v12_20261101.py', 'cohort119-expanded-specification-20261101.json',
        'cohort119-expanded-prerequisite-exclusion-20261101.json',
        'docs/2026-11-01-cohort119-expanded-source-and-native-components.md',
        'evidence/verification/cohort119-expanded-existing-inputs-20261101.json',
        'evidence/verification/cohort119-expanded-identity-preflight-20261101.json',
        'evidence/verification/cohort119-pending-consolidation-20261101.json',
        'evidence/verification/cohort119-pending-consolidation-processes-20261101.json',
        'evidence/verification/cohort119-helpers664-existing-inputs-20261101.json',
        'evidence/verification/cohort122-save-existing-inputs-20261101.json',
        'evidence/verification/cohort122-arm7-functional-existing-inputs-20261101.json'})
    extra += [path.relative_to(ROOT).as_posix() for path in
        (ROOT / 'evidence/attempts/cohort119-pending-plan-consolidation-20261101').glob('*') if path.is_file()]
    write_json(ROOT / 'cohort119-expanded-package-20261101.json', dict(cohort=119, manifests=manifests,
        archives=archives, extra=sorted(set(extra)), traces=[]))
    print(dict(functionCandidates=11, initializedBytes=1556, originalRegressionGatesRetained=True))


if __name__ == '__main__':
    main()
