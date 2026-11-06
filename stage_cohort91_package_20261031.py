import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'evidence/lanes/save-core/packed-classify-ready-20261031.json',
        'evidence/lanes/save-core/packed-pointer-abi-ready-20261031.json',
        'evidence/lanes/save-core/compare-mutex-ready-20261031.json',
        'evidence/lanes/save-core/void-tail-audit-ready-20261031.json',
        'evidence/lanes/save-core/packed-thumb-scope91-model-ready-20261031.json',
        'provenance/arm7-mmio-poll44-handoff-20261031.json',
        'provenance/arm7-spi-functional1204-handoff-20261031.json',
        'provenance/handoffs/ov000-birth330-functional-20261031.json',
        'provenance/handoffs/ov000-selection333-native-20261031.json',
        'provenance/handoffs/ov000-commit336-native-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_91.py', 'run_cohort_20261031_91.py', 'finalize_cohort_20261031_91.py',
        'stage_cohort91_package_20261031.py', 'adapt_packed_pointer_host_bindings_20261031.py',
        'repair_cohort91_host_bindings_20261031.py', 'probe_main_field_widths_20261031.py',
        'qualify_root_main_frontier_20261031.py', 'replay_root_main_profiles_20261031.py',
        'docs/2026-10-31-main-widths-and-forwarded-pointer.md',
        'docs/2026-10-31-packed-thumb-scope-integration-repair.md',
        'docs/2026-10-31-cohort91-pointer-contracts-and-widths.md',
        'evidence/verification/cohort91-before-adoption-20261031.json',
        'evidence/verification/cohort91-first-binding-failure-20261031.json',
        'evidence/verification/cohort91-first-binding-integration-20261031.json',
        'evidence/verification/cohort91-frozen-whitespace-20261031.json',
        'evidence/verification/root-main-qualified-frontier-20261031.json',
        'evidence/attempts/main-reservation-pointer-probe-20261031.json',
        'evidence/attempts/main-field-width-probe-20261031.json',
    ]
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/verification/cohort91-first-bindings').glob('*.json'))
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/attempts').glob('root-main-current-profile-replay*20261031.json'))
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'nonmatching/main-runtime/20261031-qualified-main-frontier').rglob('*.c'))
    for manifest in manifests:
        document = read_json(ROOT / manifest)
        extra.append(manifest)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            values = document.get(key)
            if isinstance(values, list):
                extra.extend(item['path'] for item in values if isinstance(item, dict) and 'path' in item)
    assert all((ROOT / name).is_file() for name in extra)
    labels = ['save-packed-classify-root', 'save-packed-pointer-abi-root', 'save-compare-mutex-root',
              'save-void-tail-audit-root', 'save-packed-thumb-scope91-root', 'arm7-mmio-poll44-root',
              'arm7-spi-functional1204-root', 'ov000-birth330-root', 'ov000-selection333-root', 'ov000-commit336-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '91', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
