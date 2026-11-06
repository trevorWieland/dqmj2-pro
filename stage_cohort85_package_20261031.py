import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-lane-card-control452-handoff-20261031.json',
        'provenance/arm7-lane-card-priority64-handoff-20261031.json',
        'provenance/handoffs/ov001-random272-20261031.json',
        'provenance/handoffs/ov001-mapper280-20261031.json',
        'provenance/handoffs/ov001-copy283-20261031.json',
        'provenance/handoffs/battle-contracts275-native-20261031.json',
        'evidence/lanes/save-core/menu-setup-ready-20261031.json',
        'evidence/lanes/save-core/group-criterion-ready-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_85.py', 'run_cohort_20261031_85.py', 'finalize_cohort_20261031_85.py',
        'stage_cohort85_package_20261031.py',
        'docs/2026-10-31-cohort85-card-controls-and-group-criteria.md',
        'docs/2026-10-31-main-word-dispatch-native-and-windows.md',
        'evidence/verification/cohort85-before-adoption-20261031.json',
    ]
    extra.extend(manifests)
    for path in manifests:
        document = read_json(ROOT / path)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            value = document.get(key)
            if isinstance(value, list):
                extra.extend(item['path'] for item in value if isinstance(item, dict) and 'path' in item)
    missing = [path for path in extra if not (ROOT / path).is_file()]
    assert not missing, missing
    labels = ['arm7-card-control452-root', 'arm7-card-priority64-root', 'ov001-random272-root',
              'ov001-mapper280-root', 'ov001-copy283-root', 'battle-contracts275-root',
              'save-menu-setup-root', 'save-group-criterion-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    if archives:
        subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '85', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
