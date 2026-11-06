import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'evidence/lanes/save-core/thread-commands-ready-20261031.json',
        'evidence/lanes/save-core/roster-actions-ready-20261031.json',
        'provenance/handoffs/ov001-recruit353-20261031.json',
        'provenance/handoffs/ov001-recruit360-20261031.json',
        'provenance/handoffs/ov001-template350-functional-20261031.json',
        'provenance/arm7-crc-table32-handoff-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_93.py', 'run_cohort_20261031_93.py', 'finalize_cohort_20261031_93.py',
        'stage_cohort93_package_20261031.py', 'adapt_arm7_crc_table32_report_20261031.py',
        'docs/2026-10-31-main-decimal-reference-and-native-models.md',
        'docs/2026-10-31-cohort93-decimal-recruitment-and-data.md',
        'provenance/msl-ansi-reference-20261031.json',
        'evidence/verification/cohort93-before-adoption-20261031.json',
        'evidence/verification/cohort93-first-data-path-failure-20261031.json',
    ]
    for prefix in ['main-decimal-family-', 'main-decimal-standard-rounding-', 'main-decimal-round-helpers-']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/attempts').glob(prefix + '*20261031.json'))
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'nonmatching/integration/20261031-cohort93-data-path').glob('*.py'))
    for manifest in manifests:
        document = read_json(ROOT / manifest)
        extra.append(manifest)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            values = document.get(key)
            if isinstance(values, list):
                extra.extend(item['path'] for item in values if isinstance(item, dict) and 'path' in item)
    assert all((ROOT / name).is_file() for name in extra)
    labels = ['save-thread-commands-root', 'save-roster-actions-root', 'ov001-recruit353-root',
              'ov001-recruit360-root', 'ov001-template350-root', 'arm7-crc-table32-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    reference = read_json(ROOT / 'provenance/msl-ansi-reference-20261031.json')
    subprocess.run(['git', 'add', '-f', '--', *[row['path'] for row in reference['files']]], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '93', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
