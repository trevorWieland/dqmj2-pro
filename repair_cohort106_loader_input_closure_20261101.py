import subprocess
import sys
from project import ROOT, read_json, write_json, sha256


def git(*arguments):
    return subprocess.run(['git', *arguments], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()


def main():
    original = 'e1d26443d1e5a93b2b2747c6cb47ce7000e9030a'
    assert git('rev-parse', 'HEAD') == original
    assert not git('diff', '--cached', '--name-only')
    plan = read_json(ROOT / 'evidence/verification/cohort-2026-10-29-106.json')
    assert not plan['linksPending'] and plan['sourceMatchedFunctions'] == 9203 and plan['sourceLinkedBytes'] == 709031
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    assert read_json(ROOT / 'evidence/verification/cohort106-validation-driver.json')['state'] == 'build-and-regression-checks-passed'
    paths = ['repair_cohort106_loader_input_closure_20261101.py',
        'verify_committed_source_inputs_v8_20261101.py', 'finish_source_package_v8_20261101.py',
        'run_next_source_package_v8_20261101.py', 'docs/2026-11-01-host-arm7-derived-input-audit.md',
        'evidence/verification/cohort106-committed-source-inputs-v7-20261101.json']
    folder = ROOT / 'evidence/attempts/cohort106-arm7-loader-input-failure-20261101'
    paths += [path.relative_to(ROOT).as_posix() for path in folder.iterdir() if path.is_file()]
    assert all((ROOT / path).is_file() for path in paths)
    git('add', '--', *paths)
    git('-c', 'core.whitespace=cr-at-eol', 'diff', '--cached', '--check')
    git('commit', '-m', 'Independently derive host ARM7 loader sections in source audit')
    revision = git('rev-parse', 'HEAD')
    commands = [('verify_committed_source_inputs_v8_20261101.py', 'source-input-v8-repaired'),
        ('verify_captured_oracle_closure_20261031.py', 'captured-closure-repaired')]
    for script, label in commands:
        with (ROOT / f'logs/integration/cohort106-{label}-20261101.txt').open('w', encoding='utf-8') as stream:
            subprocess.run([sys.executable, str(ROOT / script), '--cohort', '106'], cwd=ROOT,
                stdout=stream, stderr=subprocess.STDOUT, check=True)
    reports = ['evidence/verification/cohort106-committed-source-inputs-v8-20261101.json',
        'evidence/verification/cohort106-captured-oracle-closure-verification-20261031.json']
    assert read_json(ROOT / reports[0])['passed']
    assert read_json(ROOT / reports[1])['committedVerification']['passed']
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    receipt = 'evidence/verification/cohort106-expanded-source-closure-20261101.json'
    write_json(ROOT / receipt, dict(cohort=106, sourceCommit=revision, originalSourceCommit=original,
        passed=True, sourceCredit=0, nativeSourceAndObjectSelectionsChanged=False,
        fullCleanReplayProven=False, derivedOriginalInputs=10,
        failedSevenInputAuditPreserved='evidence/verification/cohort106-committed-source-inputs-v7-20261101.json',
        reports=[dict(path=path, sha256=sha256(ROOT / path)) for path in reports]))
    git('add', '--', *reports, receipt)
    git('commit', '-m', 'Verify cohort106 committed closure with independent ARM7 loader derivation')
    print(dict(cohort=106, sourceFunctions=9203, sourceBytes=709031, sourceCommit=revision, packaged=True,
        newSourceCreditFromAuditRepair=0))


if __name__ == '__main__':
    main()
