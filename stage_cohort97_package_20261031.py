import subprocess
import sys
from project import ROOT, read_json, write_json
import stage_verified_cohort
import oracle_source_closure_20261031


def main():
    manifests = [
        'provenance/arm7-child-alarm-control224-handoff-20261031.json',
        'provenance/arm7-child-tick324-handoff-20261031.json',
        'evidence/lanes/save-core/forward-animation-abi-ready-20261031.json',
        'evidence/lanes/save-core/bit-accumulator-ready-20261031.json',
        'evidence/lanes/save-core/status-cluster-ready-20261031.json',
        'provenance/handoffs/main-transitive422-static-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_97.py', 'publish_cohort97_prepared_20261031.py',
        'run_cohort_20261031_97.py', 'finalize_cohort_20261031_97.py',
        'stage_cohort97_package_20261031.py', 'verify_captured_oracle_closure_20261031.py',
        'validate_evidence_ash_cache_20261031.py',
        'docs/2026-10-31-cohort97-measured-input-contracts.md',
        'evidence/verification/main-transitive-inputs422-20261031.json',
    ]
    for prefix in ['cohort97-', 'main-measured-', 'main-38148-']:
        for folder in ['evidence/verification', 'evidence/attempts']:
            extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob(prefix + '*20261031*.json'))
    for manifest in manifests:
        document = read_json(ROOT / manifest)
        extra.append(manifest)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            values = document.get(key)
            if isinstance(values, list):
                extra.extend(item['path'] for item in values if isinstance(item, dict) and 'path' in item)
    labels = ['arm7-child-alarm-control224-root', 'arm7-child-tick324-root',
        'save-forward-animation-abi-root', 'save-bit-accumulator-root', 'save-status-cluster-root',
        'main-transitive422-static-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
        for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    assert all((ROOT / name).is_file() for name in extra)
    original_collect = oracle_source_closure_20261031.collect

    def captured_collect():
        report = original_collect()
        write_json(ROOT / 'evidence/verification/cohort97-captured-oracle-closure-20261031.json', report)
        return report

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', '97', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', 'evidence/verification/cohort97-captured-oracle-closure-20261031.json'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
