import subprocess
import sys
from project import ROOT, read_json, write_json
import stage_verified_cohort
import oracle_source_closure_20261031


def main():
    manifests = [
        'provenance/handoffs/ov000-birth388-20261031.json',
        'provenance/handoffs/ov000-birth395-20261031.json',
        'provenance/arm7-oneshot112-handoff-20261031.json',
        'provenance/arm7-valarm-insert164-handoff-20261031.json',
        'provenance/arm7-child-alarm544-handoff-20261031.json',
        'evidence/lanes/save-core/input-state-family-ready-20261031.json',
        'evidence/lanes/save-core/array-initial-index-ready-20261031.json',
        'evidence/lanes/save-core/historical-exact95-ready-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_96.py', 'publish_cohort96_prepared_20261031.py',
        'run_cohort_20261031_96.py', 'finalize_cohort_20261031_96.py',
        'stage_cohort96_package_20261031.py', 'verify_captured_oracle_closure_20261031.py',
        'sweep_main_void_views_20261031.py', 'sweep_main_compiler_profiles_20261031.py',
        'experiment_main_decimal_u64_restrict_20261031.py',
        'validate_evidence_phase_cache_20261031.py',
        'profile_ledger_evaluation_20261031.py',
        'benchmark_ash_memoization_20261031.py',
        'evidence/verification/ledger-performance-profile-20261031.json',
        'evidence/verification/ash-memoization-benchmark-20261031.json',
        'evidence/attempts/ash-benchmark-import-order-20261031.json',
        'provenance/evidence-phase-cache-framework-20261031.json',
        'evidence/verification/evidence-phase-cache-20261031.json',
        'docs/2026-10-31-cohort96-birth-sdk-and-breadth-validation.md',
    ]
    for prefix in ['cohort96-', 'main-void-', 'main-compiler-', 'main-decimal-u64-restrict-', 'main-state-dispatch-']:
        for folder in ['evidence/verification', 'evidence/attempts']:
            extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob(prefix + '*20261031*.json'))
    for folder in ['nonmatching/integration/20261031-cohort96-sealer-api',
                   'nonmatching/integration/20261031-void-sweep-initial-scope',
                   'nonmatching/integration/20261031-cohort96-rom-size-template',
                   'nonmatching/integration/20261031-ash-benchmark-import-order']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob('*') if p.is_file())
    for manifest in manifests:
        document = read_json(ROOT / manifest)
        extra.append(manifest)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            values = document.get(key)
            if isinstance(values, list):
                extra.extend(item['path'] for item in values if isinstance(item, dict) and 'path' in item)
    labels = ['ov000-birth388-root', 'ov000-birth395-root', 'arm7-oneshot112-root',
        'arm7-valarm-insert164-root', 'arm7-child-alarm544-root', 'save-input-state-family-root',
        'save-array-initial-index-root', 'save-historical-exact95-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
        for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    assert all((ROOT / name).is_file() for name in extra)
    original_collect = oracle_source_closure_20261031.collect

    def captured_collect():
        report = original_collect()
        write_json(ROOT / 'evidence/verification/cohort96-captured-oracle-closure-20261031.json', report)
        return report

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', '96', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', 'evidence/verification/cohort96-captured-oracle-closure-20261031.json'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
