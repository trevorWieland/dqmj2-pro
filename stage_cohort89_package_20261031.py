import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-child-lock-initializer136-handoff-20261031.json',
        'evidence/lanes/save-core/reverse-copy-ready-20261031.json',
        'evidence/lanes/save-core/item-byte-ready-20261031.json',
        'evidence/lanes/save-core/cleanup-words-ready-20261031.json',
        'evidence/lanes/save-core/handle-lookup-ready-20261031.json',
        'evidence/lanes/save-core/item-caller-ready-20261031.json',
        'provenance/handoffs/ov000-allocator305-20261031.json',
        'provenance/handoffs/ov006-cleanup308-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_89.py', 'run_cohort_20261031_89.py',
        'finalize_cohort_20261031_89.py', 'stage_cohort89_package_20261031.py',
        'docs/2026-10-31-cohort89-item-and-runtime-contracts.md',
        'docs/2026-10-31-item-threshold-caller-and-signed-absent-result.md',
        'evidence/verification/cohort89-before-adoption-20261031.json',
        'evidence/verification/arm7-lock-bitmap-region-integrator-review-20261031.json',
        'evidence/verification/clean-x-proposed-cache-failure-20261031.json',
        'evidence/verification/clean-y-known-proposed-cache-stop-20261031.json',
    ]
    extra.extend(manifests)
    for path in manifests:
        document = read_json(ROOT / path)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            value = document.get(key)
            if isinstance(value, list):
                extra.extend(item['path'] for item in value if isinstance(item, dict) and 'path' in item)
    assert all((ROOT / path).is_file() for path in extra)
    labels = ['arm7-child-lock136-root', 'save-reverse-copy-root', 'save-item-byte-root',
              'save-cleanup-words-root', 'save-handle-lookup-root', 'save-item-caller-root',
              'ov000-allocator305-root', 'ov006-cleanup308-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '89', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
