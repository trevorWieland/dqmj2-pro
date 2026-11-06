import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-lane-halfword-control80-handoff-20261031.json',
        'evidence/lanes/save-core/state-loop-ready-20261031.json',
        'evidence/lanes/save-core/width-leaves-ready-20261031.json',
        'evidence/lanes/save-core/packed-sweep-ready-20261031.json',
        'provenance/handoffs/ov005-controller295-20261031.json',
        'provenance/handoffs/ov005-callbacks296-data-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_87.py', 'run_cohort_20261031_87.py',
        'finalize_cohort_20261031_87.py', 'stage_cohort87_package_20261031.py',
        'docs/2026-10-31-cohort87-source-and-symbolic-callbacks.md',
        'docs/2026-10-31-word-pattern-native-and-win32.md',
        'docs/2026-10-31-header-append-and-symbolic-callback-data.md',
        'evidence/verification/cohort87-before-adoption-20261031.json',
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
    labels = ['arm7-halfword-control80-root', 'save-state-loop-root', 'save-width-leaves-root',
              'save-packed-sweep-root', 'ov005-controller295-root', 'ov005-callbacks296-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    if archives:
        subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '87', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
