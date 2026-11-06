import json
import re
import subprocess
import sys
import time
from project import ROOT, read_json, write_json, sha256


def run(command, log):
    with (ROOT / log).open('w', encoding='utf-8') as stream:
        subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)


def main():
    plan_path = ROOT / 'evidence/verification/cohort-2026-10-29-98.json'
    while read_json(plan_path)['linksPending']:
        driver = read_json(ROOT / 'evidence/verification/cohort98-validation-driver.json')
        assert driver['state'] != 'failed', driver
        time.sleep(5)
    plan = read_json(plan_path)
    assert plan['sourceMatchedFunctions'] == 9111 and plan['sourceLinkedBytes'] == 696933
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    readme = ROOT / 'README.md'
    text = readme.read_text()
    previous = next(line for line in text.splitlines() if line.startswith('Latest accepted source cohort '))
    replacement = ('Latest accepted source cohort 98: **9,111 functions / 696,933 initialized module bytes '
        f'({plan["sourceCoveragePercentage"]:.6f}%)**, with all 20 module comparisons, both checksum matches, '
        '144 isolated checksum returns and 5,117 getter comparisons passing. The original-length/SHA ROM is '
        'still scaffolding-assisted. See [allocation and connected draft validation]'
        '(docs/2026-11-01-cohort98-allocation-and-draft-validation.md). This is not an overall game percentage or source-only ROM proof.')
    readme.write_text(text.replace(previous, replacement), encoding='utf-8')
    rows = [json.loads(line) for line in (ROOT / 'ledger/functions.jsonl').read_text().splitlines()]
    selected = [dict(processor=r['processor'], program=r.get('program') or '', module=r['module'], mode=r['mode'],
        name=r['symbol'], address=int(r['address'], 16), source=r['sourceUnit'], sourceSha256=r['sourceSha256'], bytes=r['bytes'])
        for r in rows if r['states']['functionMatched']]
    assert len(selected) == plan['sourceMatchedFunctions']
    snapshot = 'evidence/verification/accepted-cohort98-identities-v2-20261101.json'
    write_json(ROOT / snapshot, dict(acceptedCohort=98, romSha256=plan['exactRom']['sha256'], functions=selected,
        ledgerSha256=sha256(ROOT / 'ledger/functions.jsonl'), acceptedEvidenceSha256=sha256(plan_path)))
    run([sys.executable, str(ROOT / 'stage_cohort98_package_20261101.py')], 'logs/integration/cohort98-stage-20261101.txt')
    output = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--cached', '--check'],
        cwd=ROOT, capture_output=True, text=True)
    assert output.returncode in [0, 2], output
    (ROOT / 'logs/integration/cohort98-whitespace-20261101.txt').write_text(output.stdout + output.stderr)
    paths = sorted(set(re.findall(r'^(.+?):\d+: (?:trailing whitespace|new blank line at EOF|space before tab)', output.stdout, re.M)))
    closure = read_json(ROOT / 'evidence/verification/cohort98-captured-oracle-closure-20261031.json')['sourceAndEvidenceHashes']
    registered = {p for batch in read_json(ROOT / 'recovery.json')['batches'] for p in batch['sourceHashes']}
    findings = []
    for path in paths:
        prior = subprocess.run(['git', 'show', 'HEAD:' + path], cwd=ROOT, capture_output=True)
        historical = prior.returncode == 0 and prior.stdout == (ROOT / path).read_bytes()
        classified = path in closure or path in registered or path.startswith('generated/') or historical
        findings.append(dict(path=path, sha256=sha256(ROOT / path), frozenRegisteredInput=path in registered,
            frozenOracleInput=path in closure, generatedHypothesis=path.startswith('generated/'),
            unchangedHistoricalInput=historical, classified=classified))
    assert all(row['classified'] for row in findings), findings
    whitespace = 'evidence/verification/cohort98-frozen-whitespace-20261101.json'
    write_json(ROOT / whitespace, dict(paths=findings, allClassified=True, frozenInputsModified=False, sourceCredit=0))
    staged = subprocess.run(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    assert not [p for p in staged if p.split('/')[0] in {'inputs', 'tools', 'work', 'extract', 'build', 'deps'}]
    subprocess.run(['git', 'add', '--', snapshot, whitespace, 'finish_cohort98_package_20261101.py'], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', 'Accept cohort 98 allocation and interrupt C with connected heap draft evidence'], cwd=ROOT, check=True)
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    for script, log in [('verify_committed_source_inputs_v3_20261031.py', 'source-input'),
                        ('verify_captured_oracle_closure_20261031.py', 'captured-closure')]:
        run([sys.executable, str(ROOT / script), '--cohort', '98'], f'logs/integration/cohort98-{log}-audit-20261101.txt')
    reports = ['evidence/verification/cohort98-committed-source-inputs-v3-20261031.json',
               'evidence/verification/cohort98-captured-oracle-closure-verification-20261031.json']
    assert read_json(ROOT / reports[0])['passed']
    assert read_json(ROOT / reports[1])['committedVerification']['passed']
    receipt = 'evidence/verification/cohort98-expanded-source-closure-20261101.json'
    write_json(ROOT / receipt, dict(cohort=98, sourceCommit=revision, passed=True, sourceCredit=0,
        fullCleanReplayProven=False, reports=[dict(path=p, sha256=sha256(ROOT / p)) for p in reports]))
    subprocess.run(['git', 'add', '--', *reports, receipt], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', 'Verify cohort 98 committed source and oracle closure'], cwd=ROOT, check=True)
    print(dict(cohort=98, sourceCommit=revision, sourceFunctions=len(selected), sourceBytes=plan['sourceLinkedBytes'], packaged=True), flush=True)


if __name__ == '__main__':
    main()
