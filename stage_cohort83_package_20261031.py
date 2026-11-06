import subprocess
from project import ROOT, read_json


def main():
    extra = [
        'prepare_cohort_20261031_83.py', 'run_cohort_20261031_83.py', 'finalize_cohort_20261031_83.py',
        'stage_cohort83_package_20261031.py',
        'docs/2026-10-31-cohort83-card-interfaces-and-async-reader.md',
        'docs/2026-10-31-asynchronous-file-acceptance-source.md',
        'docs/2026-10-31-asynchronous-status-failures.md',
        'docs/2026-10-31-async-acceptance-native-portability.md',
        'docs/2026-10-31-cohort83-historical-header-transport-repair.md',
        'prepare_async_acceptance_ports_20261031.py',
        'ports/android-native/async_acceptance_fixture.c', 'ports/android-native/async_acceptance_runner.c',
        'evidence/portability/async-acceptance-windows-android-20261031.json',
        'reproduce_main_async_status_attempts_20261031.py',
        'evidence/verification/main-async-status-inputs-20261031.json',
        'evidence/attempts/main-async-status-reproduced-20261031.json',
        'evidence/verification/arm7-card-abi16-initial-import-failure-20261031.json',
        'evidence/verification/arm7-card-abi16-transport-audit-20261031.json',
        'audit_arm7_card_abi16_transport_20261031.py',
        'provenance/arm7-lane-card-abi16-1252-handoff-20261031.json',
        'provenance/arm7-card-abi16-missing-runtime-supplement-20261031.json',
        'provenance/arm7-lane-card-init188-handoff-20261031.json',
        'provenance/handoffs/ov006-cache255-20261031.json',
        'evidence/verification/cohort83-initial-packaging-preflight-20261031.json',
        'evidence/verification/cohort83-historical-header-transport-repair-20261031.json',
    ]
    repair = read_json(ROOT / extra[-1])
    extra.extend(row['path'] for row in repair['headers'])
    extra.extend(path.relative_to(ROOT).as_posix() for path in
        (ROOT / 'nonmatching/main-runtime/20261031/async-status').rglob('*.c'))
    assert all((ROOT / path).is_file() for path in extra)
    subprocess.run(['python', 'stage_verified_cohort.py', '--cohort', '83', '--extra', *extra], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
