import subprocess
import sys
import time
from pathlib import Path
from project import ROOT, read_json, write_json, sha256, now


def main():
    frozen_plan = ROOT / 'provenance/cohort107-frozen-input-plan-v2-20261101.json'
    frozen_hash = sha256(frozen_plan)
    declared = read_json(frozen_plan)['files']
    assert all(sha256(ROOT / row['path']) == row['sha256'] for row in declared)
    target = ROOT.parent / 'j2p-clean-20261101-ac'
    launcher = ROOT / 'evidence/verification/clean-cohort106-j2p-clean-20261101-ac-launcher-20261101.json'
    receipt = ROOT / 'evidence/verification/cohort107-fresh-source-snapshot-gate-v2-20261101.json'
    result = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        startedUtc=now(), state='waiting-for-source106-fresh-snapshot', sourceCredit=0)
    write_json(receipt, result)
    while True:
        if launcher.exists():
            report = read_json(launcher)
            if report['state'] == 'failed':
                result.update(state='failed', reason='Fresh launcher failed before dependency release',
                    launcherSha256=sha256(launcher), finishedUtc=now())
                write_json(receipt, result)
                raise SystemExit(1)
            preflight = report.get('pathPortabilityPreflight', [])
            if preflight:
                first = preflight[0]
                assert first['exitCode'] == 0
                assert Path(first['command'][1]).name == 'reproduce_effect_queue_short_paths_v3_20261101.py'
                assert Path(first['command'][1]).parent.resolve() == target.resolve()
                assert (target / '.git').is_dir()
                accepted = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-106.json')
                assert not accepted['linksPending']
                assert sha256(target / 'recovery.json') == accepted['sourceRegistrySha256']
                assert sha256(ROOT / 'recovery.json') == accepted['sourceRegistrySha256']
                result.update(state='fresh-snapshot-and-first-native-preflight-passed',
                    launcherSha256=sha256(launcher), sourceRevision=report['sourceRevision'],
                    targetRegistrySha256=sha256(target / 'recovery.json'),
                    nativePreflight=first, sourceSnapshotIndependentOfLaterRootBuilds=True)
                write_json(receipt, result)
                break
        time.sleep(5)
    assert sha256(frozen_plan) == frozen_hash
    assert all(sha256(ROOT / row['path']) == row['sha256'] for row in declared)
    command = [sys.executable, str(ROOT / 'run_next_source_package_v8_20261101.py'),
        '--specification', 'cohort107-specification-20261101.json',
        '--stage', 'stage_cohort107_package_v2_20261101.py',
        '--document', 'docs/2026-11-01-cohort107-typed-boundaries-v2.md',
        '--label', 'typed boundaries and IRQ getters']
    completed = subprocess.run(command, cwd=ROOT)
    result.update(state='packaged' if completed.returncode == 0 else 'failed',
        continuationExitCode=completed.returncode, finishedUtc=now())
    write_json(receipt, result)
    raise SystemExit(completed.returncode)


if __name__ == '__main__':
    main()
