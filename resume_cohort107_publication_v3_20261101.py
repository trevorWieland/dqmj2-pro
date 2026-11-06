import subprocess
import sys
from project import ROOT, read_json, write_json, sha256, now


def main():
    old = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-106.json')
    prepared = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-107.json')
    assert not old['linksPending'] and prepared['linksPending']
    assert prepared['newSourceFunctions'] == 7 and prepared['newSourceBytes'] == 400
    assert prepared['duplicateMigrationFunctions'] == 1 and prepared['duplicateMigrationBytes'] == 100
    assert sha256(ROOT / 'recovery.json') == old['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == old['sourcePreferenceSha256']
    gate = read_json(ROOT / 'evidence/verification/cohort107-fresh-source-snapshot-gate-v2-20261101.json')
    assert gate['sourceSnapshotIndependentOfLaterRootBuilds']
    assert gate['nativePreflight']['exitCode'] == 0
    assert gate['targetRegistrySha256'] == old['sourceRegistrySha256']
    commands = [
        ['publish_prepared_source_migrations_v6_20261101.py', '--cohort', '107'],
        ['run_source_cohort_20261101.py', '--cohort', '107'],
        ['finalize_source_cohort_20261101.py', '--cohort', '107'],
        ['finish_source_package_v8_20261101.py', '--cohort', '107', '--stage',
            'stage_cohort107_package_v3_20261101.py', '--document',
            'docs/2026-11-01-cohort107-typed-boundaries-v3.md', '--label', 'typed boundaries and IRQ getters']]
    report = dict(generator=__file__.split(chr(92))[-1], generatorSha256=sha256(__file__),
        startedUtc=now(), state='running', sourceCredit=0, preparedSourceSelectionUnchanged=True, steps=[])
    output = ROOT / 'evidence/verification/cohort107-publication-resume-v3-20261101.json'
    for index, command in enumerate(commands):
        log = ROOT / f'logs/integration/cohort107-resume-v3-{index:02}-20261101.txt'
        report['currentCommand'] = command
        write_json(output, report)
        with log.open('w', encoding='utf-8') as stream:
            result = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT,
                stdout=stream, stderr=subprocess.STDOUT)
        report['steps'].append(dict(command=command, exitCode=result.returncode,
            log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log)))
        if result.returncode:
            report.update(state='failed', finishedUtc=now())
            write_json(output, report)
            raise SystemExit(result.returncode)
    report.update(state='packaged', finishedUtc=now())
    report.pop('currentCommand', None)
    write_json(output, report)


if __name__ == '__main__':
    main()
