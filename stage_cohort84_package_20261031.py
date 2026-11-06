import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-lane-card-frontier2240-handoff-20261031.json',
        'provenance/handoffs/ov001-phases257-20261031.json',
        'provenance/handoffs/ov001-phases259-20261031.json',
        'provenance/handoffs/ov001-query265-20261031.json',
        'provenance/handoffs/ov001-item-writes266-20261031.json',
        'evidence/lanes/save-core/creation-level-abi-ready-20261031.json',
        'evidence/lanes/save-core/skill-input-context-ready-20261031.json',
        'evidence/lanes/save-core/skill-creator-connected-ready-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_84.py', 'run_cohort_20261031_84.py', 'finalize_cohort_20261031_84.py',
        'stage_cohort84_package_20261031.py',
        'docs/2026-10-31-cohort84-card-control-and-overlay-phases.md',
        'evidence/verification/cohort84-unpublished-preparation-20261031.json',
        'evidence/verification/cohort84-registry-publication-20261031.json',
        'evidence/abi/arm7-card-storage-batch-supersession-20261031.json',
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
    sys.argv = ['stage_verified_cohort.py', '--cohort', '84', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
