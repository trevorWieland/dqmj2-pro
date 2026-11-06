import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'evidence/lanes/save-core/packed-input-ready-20261031.json',
        'provenance/handoffs/ov001-recruit373-20261031.json',
        'provenance/handoffs/ov001-membership377-20261031.json',
        'provenance/handoffs/ov001-eligibility381-20261031.json',
        'provenance/arm7-alarm-family572-handoff-20261031.json',
        'provenance/arm7-tick-callback104-boundary-handoff-20261031.json',
        'provenance/host-arm7-empty-interface-audit-handoff-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_95.py', 'run_cohort_20261031_95.py', 'finalize_cohort_20261031_95.py',
        'stage_cohort95_package_20261031.py', 'adopt_ov001_refresh_void_caller_20261031.py',
        'compile_float_runtime_ports_20261031.py', 'verify_windows_float_runtime_20261031.py',
        'prepare_float_runtime_android_20261031.py', 'ports/android-native/float_runtime_runner.c',
        'docs/2026-10-31-cohort95-float-input-and-alarm-integration.md',
        'docs/2026-10-31-float-library-and-native-portability.md',
        'evidence/abi/arm7-wram-037fe5c0-complete-alarm-type-primary-migration-20261031.json',
        'evidence/verification/arm7-callback104-inventory-review-20261031.json',
    ]
    for prefix in ['cohort95-', 'float-runtime-', 'main-float-', 'main-22480-', 'main-ascii-', 'main-case-']:
        for folder in ['evidence/verification', 'evidence/attempts', 'evidence/portability']:
            extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob(prefix + '*20261031*.json'))
    for folder in [
        'nonmatching/integration/20261031-cohort95-limits-field',
        'nonmatching/integration/20261031-cohort95-caller-proposal',
        'nonmatching/integration/20261031-cohort95-arm7-policy',
        'nonmatching/integration/20261031-cohort95-duplicate-membership',
        'nonmatching/integration/20261031-cohort95-stale-finalizer',
        'nonmatching/main-runtime/20261031-float-floor-controls/initial-nan-model',
        'nonmatching/main-runtime/20261031-case-compare-wrong-table',
    ]:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob('*') if p.is_file())
    for manifest in manifests:
        document = read_json(ROOT / manifest)
        extra.append(manifest)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            values = document.get(key)
            if isinstance(values, list):
                extra.extend(item['path'] for item in values if isinstance(item, dict) and 'path' in item)
    for folder in ['msl-math-reference-20261031', 'msl-ceil-reference-20261031', 'msl-floor-reference-20261031']:
        paths = [p.relative_to(ROOT).as_posix() for p in (ROOT / 'deps' / folder).rglob('*') if p.is_file()]
        paths.append('provenance/' + folder + '.json')
        assert all((ROOT / name).is_file() for name in paths)
        subprocess.run(['git', 'add', '-f', '--', *paths], cwd=ROOT, check=True)
    labels = ['save-packed-input-root', 'ov001-recruit373-root', 'ov001-membership377-root',
        'ov001-eligibility381-root', 'arm7-alarm-family572-root', 'arm7-tick-callback104-scope-root',
        'arm7-empty-interface-audit-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
        for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    assert all((ROOT / name).is_file() for name in extra)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '95', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
