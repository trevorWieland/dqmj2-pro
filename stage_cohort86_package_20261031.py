import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-lane-halfword188-handoff-20261031.json',
        'provenance/handoffs/ov001-family293-20261031.json',
        'evidence/lanes/save-core/table-kind-ready-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_85.py', 'run_cohort_20261031_85.py', 'finalize_cohort_20261031_85.py',
        'stage_cohort86_package_20261031.py',
        'docs/2026-10-31-cohort86-halfword-fields-and-state-machines.md',
        'docs/2026-10-31-main-near-stride-and-mask-frontier.md',
        'evidence/verification/cohort86-before-adoption-20261031.json',
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
    labels = ['arm7-halfword188-root', 'ov001-family293-root', 'save-table-kind-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    if archives:
        subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '86', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
