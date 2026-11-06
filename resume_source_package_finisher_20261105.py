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
    driver = read_json(ROOT / f'evidence/verification/cohort{cohort}-continuation-driver-v18-20261101.json')
    validation = read_json(ROOT / f'evidence/verification/cohort{cohort}-validation-driver.json')
    assert driver['state'] == 'failed' and driver['currentCommand'][0] == 'finish_source_package_v14_20261102.py'
    assert len(driver['steps']) == 5 and all(row['exitCode'] == 0 for row in driver['steps'][:4])
    assert validation['state'] == 'build-and-regression-checks-passed' and len(validation['steps']) == 16
    assert all(row['exitCode'] == 0 or row.get('externalApplicationSnapshotDifferences') is True for row in validation['steps'])
    assert not plan['linksPending'] and plan['sourceMatchedFunctions'] == plan['expectedSourceMatchedFunctions']
    assert plan['sourceLinkedBytes'] == plan['expectedSourceLinkedBytes']
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    prior = f'evidence/verification/cohort{cohort - 1}-expanded-source-closure-20261101.json'
    committed = subprocess.check_output(['git', 'show', 'HEAD:' + prior], cwd=ROOT)
    assert committed == (ROOT / prior).read_bytes() and read_json(ROOT / prior)['passed']
    output = ROOT / f'evidence/verification/cohort{cohort}-staging-resume-driver-20261105.json'
    log = ROOT / f'logs/integration/cohort{cohort}-staging-resume-finisher-20261105.txt'
    command = [sys.executable, str(ROOT / 'finish_source_package_v14_20261102.py'),
               '--cohort', str(cohort), '--stage', options.stage, '--document', options.document, '--label', options.label]
    result = dict(cohort=cohort, sourceCredit=0, startedUtc=now(), state='running',
        originalSourceAndSixteenValidationStagesRetained=True, originalFinisherUnchanged=True,
        validationSha256=sha256(ROOT / f'evidence/verification/cohort{cohort}-validation-driver.json'),
        finalizedPlanSha256=sha256(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json'),
        registrySha256=plan['sourceRegistrySha256'], preferencesSha256=plan['sourcePreferenceSha256'],
        command=command, log=log.relative_to(ROOT).as_posix(), generatorSha256=sha256(__file__))
    write_json(output, result)
    with log.open('w', encoding='utf-8') as stream:
        run = subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT)
    result.update(exitCode=run.returncode, finishedUtc=now(), logSha256=sha256(log))
    if run.returncode:
        result['state'] = 'failed'
        write_json(output, result)
        raise SystemExit(run.returncode)
    closure = f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json'
    assert read_json(ROOT / closure)['passed']
    assert subprocess.check_output(['git', 'show', 'HEAD:' + closure], cwd=ROOT) == (ROOT / closure).read_bytes()
    result.update(state='packaged', closureSha256=sha256(ROOT / closure))
    write_json(output, result)
    print(dict(cohort=cohort, state='packaged', functions=plan['sourceMatchedFunctions'], bytes=plan['sourceLinkedBytes']))


if __name__ == '__main__':
    main()
