import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'evidence/lanes/save-core/state-gates-ready-20261031.json',
        'evidence/lanes/save-core/live-count-loops-ready-20261031.json',
        'evidence/lanes/save-core/pop-index-abi-ready-20261031.json',
        'provenance/handoffs/ov001-recruit364-20261031.json',
        'provenance/arm7-valarm-init68-handoff-20261031.json',
        'provenance/main-u64-unsigned-abi-arm7-handoff-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_94.py', 'run_cohort_20261031_94.py', 'finalize_cohort_20261031_94.py',
        'stage_cohort94_package_20261031.py', 'adapt_main_decimal_host_entries_20261031.py',
        'repair_cohort94_decimal_entry_maps_20261031.py',
        'evidence/matches/main-decimal-pow2-20261031.json',
        'evidence/matches/main-decimal-from-double-20261031.json',
        'docs/2026-10-31-cohort94-numeric-models-and-input-repairs.md',
        'evidence/verification/cohort94-before-adoption-20261031.json',
    ]
    for prefix in ['main-decimal-pow2-', 'main-decimal-from-double-', 'main-decimal-to-double-',
                   'main-decimal-u64-', 'main-popcount64-']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/attempts').glob(prefix + '*20261031.json'))
    for folder in ['20261031-decimal-from-double-wrong-registers', '20261031-decimal-double-first-helper-map']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'nonmatching/main-runtime' / folder).glob('*.py'))
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/verification/cohort94-first-entry-maps').glob('*.json'))
    for manifest in manifests:
        document = read_json(ROOT / manifest)
        extra.append(manifest)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            values = document.get(key)
            if isinstance(values, list):
                extra.extend(item['path'] for item in values if isinstance(item, dict) and 'path' in item)
    assert all((ROOT / name).is_file() for name in extra)
    labels = ['save-state-gates-root', 'save-live-count-loops-root', 'save-pop-index-abi-root',
              'ov001-recruit364-root', 'arm7-valarm-init68-root', 'main-u64-unsigned-abi-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '94', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
