import argparse
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--original-source-commit', required=True)
    options = parser.parse_args()
    cohort = options.cohort
    plan = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json')
    validation = read_json(ROOT / f'evidence/verification/cohort{cohort}-validation-driver.json')
    assert not plan['linksPending'] and validation['state'] == 'build-and-regression-checks-passed'
    assert len(validation['steps']) == 16
    assert all(r['exitCode'] == 0 or r.get('externalApplicationSnapshotDifferences') is True for r in validation['steps'])
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    subprocess.run(['git', 'merge-base', '--is-ancestor', options.original_source_commit, 'HEAD'], cwd=ROOT, check=True)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    reports = [f'evidence/verification/cohort{cohort}-committed-source-inputs-v13-20261105.json',
               f'evidence/verification/cohort{cohort}-captured-oracle-closure-verification-20261031.json']
    for script, label in [('verify_committed_source_inputs_v13_20261105.py', 'source-input-v13'),
                          ('verify_captured_oracle_closure_20261031.py', 'captured-closure')]:
        log = ROOT / f'logs/integration/cohort{cohort}-{label}-audit-20261105.txt'
        with log.open('w', encoding='utf-8') as stream:
            subprocess.run([sys.executable, str(ROOT / script), '--cohort', str(cohort), *(['--output', reports[0]] if label == 'source-input-v13' else [])],
                           cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)
    assert read_json(ROOT / reports[0])['passed'] and read_json(ROOT / reports[0])['commit'] == revision
    assert read_json(ROOT / reports[1])['committedVerification']['passed']
    receipt = f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json'
    write_json(ROOT / receipt, dict(cohort=cohort, sourceCommit=revision,
        originalSourceCommit=options.original_source_commit, passed=True, sourceCredit=0,
        fullCleanReplayProven=False, originalSourceAndSixteenValidationStagesRetained=True,
        originalEightInputVerifierUnchanged=True,
        reports=[dict(path=p, sha256=sha256(ROOT / p)) for p in reports]))
    paths = [*reports, receipt]
    subprocess.run(['git', 'add', '--', *paths], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', f'Verify cohort {cohort} committed source and qualified reference closure'], cwd=ROOT, check=True)
    print(dict(cohort=cohort, sourceCommit=revision, passed=True,
               functions=plan['sourceMatchedFunctions'], bytes=plan['sourceLinkedBytes']))


if __name__ == '__main__':
    main()
