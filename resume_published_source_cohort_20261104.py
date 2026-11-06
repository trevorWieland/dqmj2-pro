import argparse
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256, now


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--document', required=True)
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    cohort = options.cohort
    plan = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json')
    assert plan['linksPending'] and plan['previousAcceptedCohort'] == cohort - 1
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    prerequisite = f'evidence/verification/cohort{cohort - 1}-expanded-source-closure-20261101.json'
    committed = subprocess.run(['git', 'show', 'HEAD:' + prerequisite], cwd=ROOT, capture_output=True, check=True)
    assert committed.stdout == (ROOT / prerequisite).read_bytes() and read_json(ROOT / prerequisite)['passed']
    output = ROOT / f'evidence/verification/cohort{cohort}-published-resume-driver-20261104.json'
    result = dict(cohort=cohort, startedUtc=now(), state='running', steps=[], allOriginalValidationStagesRequired=True,
                  sourceRegistrySha256=plan['sourceRegistrySha256'], generatorSha256=sha256(__file__))
    commands = [['run_source_cohort_20261101.py', '--cohort', str(cohort)],
                ['finalize_source_cohort_20261101.py', '--cohort', str(cohort)],
                ['finish_source_package_v14_20261102.py', '--cohort', str(cohort), '--stage', options.stage,
                 '--document', options.document, '--label', options.label]]
    for index, command in enumerate(commands):
        result['currentCommand'] = command
        write_json(output, result)
        log = ROOT / f'logs/integration/cohort{cohort}-published-resume-{index:02}-20261104.txt'
        with log.open('w', encoding='utf-8') as stream:
            run = subprocess.run([sys.executable, str(ROOT / command[0]), *command[1:]], cwd=ROOT,
                                 stdout=stream, stderr=subprocess.STDOUT)
        result['steps'].append(dict(command=command, exitCode=run.returncode,
                                   log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log)))
        if run.returncode:
            result.update(state='failed', finishedUtc=now())
            write_json(output, result)
            raise SystemExit(run.returncode)
    result.update(state='packaged', finishedUtc=now())
    result.pop('currentCommand')
    write_json(output, result)


if __name__ == '__main__':
    main()
