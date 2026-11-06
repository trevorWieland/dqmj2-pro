import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'evidence/lanes/save-core/group-validation-ready-20261031.json',
        'evidence/lanes/save-core/sequence-adapter-ready-20261031.json',
        'evidence/lanes/save-core/item-effect-chain-ready-20261031.json',
        'provenance/arm7-clean-replays-handoff-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_90.py', 'run_cohort_20261031_90.py', 'finalize_cohort_20261031_90.py',
        'stage_cohort90_package_20261031.py', 'replay_main_numeric_dispatch_profiles_20261031.py',
        'check_main_numeric_dispatch_windows32_20261031.py', 'ports/windows-native/numeric_dispatch_runner.c',
        'docs/2026-10-31-cohort90-numeric-source-and-clean-replays.md',
        'docs/2026-10-31-main-numeric-dispatch-416-profile.md',
        'docs/2026-10-31-main-numeric-dispatch-native-qualification.md',
        'docs/2026-10-31-numeric-dispatch-native-windows32.md',
        'docs/2026-10-31-arm7-clean-proposed-and-duplicate-replays.md',
        'evidence/verification/cohort90-before-adoption-20261031.json',
        'evidence/attempts/main-numeric-windows32-launch740-20261031.json',
        'evidence/verification/clean-x-proposed-cache-failure-20261031.json',
        'evidence/verification/clean-y-known-proposed-cache-stop-20261031.json',
        'evidence/verification/cohort90-frozen-eof-whitespace-20261031.json',
    ]
    for prefix in ['main-pcm-', 'main-numeric-dispatch-profile', 'main-numeric-dispatch-typed']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/attempts').glob(prefix + '*20261031.json'))
    for name in ['20261031-pcm-o3-expression', '20261031-pcm-wide-product', '20261031-pcm-wide-factor',
                 '20261031-pcm-c-division', '20261031-pcm-product-local']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'nonmatching/main-runtime' / name).rglob('*.c'))
    extra.extend(manifests)
    for path in manifests:
        document = read_json(ROOT / path)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            value = document.get(key)
            if isinstance(value, list):
                extra.extend(item['path'] for item in value if isinstance(item, dict) and 'path' in item)
    assert all((ROOT / path).is_file() for path in extra)
    labels = ['save-group-validation-root', 'save-sequence-adapter-root',
              'save-item-effect-chain-root', 'arm7-clean-replays-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '90', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
