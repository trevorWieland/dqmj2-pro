import argparse
import json
import re
import subprocess
import sys
import time
from project import ROOT, read_json, write_json, sha256


def run(command, log):
    with (ROOT / log).open('w', encoding='utf-8') as stream:
        subprocess.run(command, cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)


def preserved_research_replay(pin,relative):
    if pin.get('classification')!='unchanged-archived-research-replay'or pin.get('sourceCredit')!=0:return False
    if not relative.startswith(('evidence/application/','evidence/attempts/'))or not relative.endswith('.py'):return False
    path=(ROOT/relative).resolve()
    if not path.is_relative_to(ROOT)or not path.is_file()or sha256(path)!=pin.get('sha256'):return False
    manifest=read_json(ROOT/pin['pinManifest'])
    if manifest.get('sourceCredit')!=0:return False
    blob=subprocess.run(['git','show',pin['workerCommit']+':'+relative],cwd=ROOT,capture_output=True)
    return blob.returncode==0 and blob.stdout==path.read_bytes()and b'\r\r\n'in blob.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--stage', required=True)
    parser.add_argument('--document', required=True)
    parser.add_argument('--label', required=True)
    options = parser.parse_args()
    cohort = options.cohort
    assert cohort > 1
    for relative in [options.stage, options.document]:
        target = (ROOT / relative).resolve()
        assert target.is_relative_to(ROOT) and target.is_file(), relative
    plan_path = ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json'
    while read_json(plan_path)['linksPending']:
        driver = read_json(ROOT / f'evidence/verification/cohort{cohort}-validation-driver.json')
        assert driver['state'] != 'failed', driver
        time.sleep(5)
    plan = read_json(plan_path)
    prior = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{cohort - 1}.json')
    assert plan['previousAcceptedCohort'] == cohort - 1
    assert plan['sourceMatchedFunctions'] == plan['expectedSourceMatchedFunctions'] == prior['sourceMatchedFunctions'] + plan['newSourceFunctions']
    assert plan['sourceLinkedBytes'] == plan['expectedSourceLinkedBytes'] == prior['sourceLinkedBytes'] + plan['newSourceBytes']
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert sha256(ROOT / 'source-preferences.json') == plan['sourcePreferenceSha256']
    text = (ROOT / 'README.md').read_text()
    previous = next(line for line in text.splitlines() if line.startswith('Latest accepted source cohort '))
    replacement = (f'Latest accepted source cohort {cohort}: **{plan["sourceMatchedFunctions"]:,} functions / '
        f'{plan["sourceLinkedBytes"]:,} initialized module bytes ({plan["sourceCoveragePercentage"]:.6f}%)**, '
        'with all 20 module comparisons, both checksum matches, 144 isolated checksum returns and 5,117 getter '
        'comparisons passing. The original-length/SHA ROM is still scaffolding-assisted. '
        f'See [{options.label}]({options.document}). This is not an overall game percentage or source-only ROM proof.')
    (ROOT / 'README.md').write_text(text.replace(previous, replacement), encoding='utf-8')
    rows = [json.loads(line) for line in (ROOT / 'ledger/functions.jsonl').read_text().splitlines()]
    selected = [dict(processor=r['processor'], program=r.get('program') or '', module=r['module'], mode=r['mode'],
        name=r['symbol'], address=int(r['address'], 16), source=r['sourceUnit'], sourceSha256=r['sourceSha256'], bytes=r['bytes'])
        for r in rows if r['states']['functionMatched']]
    assert len(selected) == plan['sourceMatchedFunctions']
    snapshot = f'evidence/verification/accepted-cohort{cohort}-identities-v2-20261101.json'
    write_json(ROOT / snapshot, dict(acceptedCohort=cohort, romSha256=plan['exactRom']['sha256'], functions=selected,
        ledgerSha256=sha256(ROOT / 'ledger/functions.jsonl'), acceptedEvidenceSha256=sha256(plan_path)))
    run([sys.executable, str(ROOT / options.stage)], f'logs/integration/cohort{cohort}-stage-20261101.txt')
    output = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--cached', '--check'], cwd=ROOT,
        capture_output=True, text=True)
    assert output.returncode in [0, 2], output
    (ROOT / f'logs/integration/cohort{cohort}-whitespace-20261101.txt').write_text(output.stdout + output.stderr)
    paths = sorted(set(re.findall(r'^(.+?):\d+: (?:trailing whitespace|new blank line at EOF|space before tab)', output.stdout, re.M)))
    closure = read_json(ROOT / f'evidence/verification/cohort{cohort}-captured-oracle-closure-20261031.json')['sourceAndEvidenceHashes']
    registered = {p for batch in read_json(ROOT / 'recovery.json')['batches'] for p in batch['sourceHashes']}
    findings = []
    for path in paths:
        old = subprocess.run(['git', 'show', 'HEAD:' + path], cwd=ROOT, capture_output=True)
        historical = old.returncode == 0 and old.stdout == (ROOT / path).read_bytes()
        findings.append(dict(path=path, sha256=sha256(ROOT / path), frozenRegisteredInput=path in registered,
            frozenOracleInput=path in closure, generatedHypothesis=path.startswith('generated/'),
            unchangedHistoricalInput=historical, classified=path in closure or path in registered or path.startswith('generated/') or historical))
    diagnostic_path = ROOT / f'evidence/verification/cohort{cohort}-preserved-failure-log-bytes-20261101.json'
    if diagnostic_path.is_file():
        preserved = {row['path']: row['sha256'] for row in read_json(diagnostic_path)['verbatimDiagnosticLogs']}
        for row in findings:
            if row['path'] in preserved:
                assert row['path'].startswith(f'evidence/attempts/cohort{cohort}-initial-evidence-order-failure-20261101/')
                assert (ROOT / row['path']).suffix == '.txt' and sha256(ROOT / row['path']) == preserved[row['path']]
                row.update(verbatimDiagnosticEvidence=True, diagnosticReceiptSha256=sha256(diagnostic_path), classified=True)
    diagnostic_sources = ROOT / f'evidence/verification/cohort{cohort}-frozen-diagnostic-sources-20261101.json'
    if diagnostic_sources.is_file():
        records = {row['path']: row for row in read_json(diagnostic_sources)['frozenDiagnosticSources']}
        for row in findings:
            if row['path'] in records:
                pin = records[row['path']]
                assert (preserved_research_replay(pin,row['path']) or row['path'].startswith('nonmatching/') or row['path'].startswith('evidence/generated/ghidra497/') or row['path'].startswith('evidence/generated/ghidra543/') or (re.fullmatch(r'evidence/generated/ghidra[0-9]+/[a-z0-9_-]+/[0-9a-f]{8}\.generated\.c', row['path']) is not None and read_json(ROOT / pin['pinManifest']).get('sourceCredit') == 0)) and sha256(ROOT / row['path']) == pin['sha256']
                assert sha256(ROOT / pin['pinManifest']) == pin['pinManifestSha256']
                declared = {item['path'].replace(chr(92), '/'): item['sha256'] for item in read_json(ROOT / pin['pinManifest'])['files']}
                assert declared[row['path']] == pin['sha256']
                row.update(frozenHandoffDiagnostic=True, pinManifest=pin['pinManifest'], pinManifestSha256=pin['pinManifestSha256'], classified=True)
    assert all(row['classified'] for row in findings), findings
    whitespace = f'evidence/verification/cohort{cohort}-frozen-whitespace-20261101.json'
    write_json(ROOT / whitespace, dict(paths=findings, allClassified=True, frozenInputsModified=False, sourceCredit=0))
    staged = subprocess.run(['git', 'diff', '--cached', '--name-only'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.splitlines()
    assert not [p for p in staged if p.split('/')[0] in {'inputs', 'tools', 'work', 'extract', 'build', 'deps'}]
    subprocess.run(['git', 'add', '--', snapshot, whitespace, 'finish_source_package_20261101.py'], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', f'Accept cohort {cohort}: {options.label}'], cwd=ROOT, check=True)
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    for script, name in [('verify_committed_source_inputs_context_v3_20261106.py', 'source-input'),
                         ('verify_captured_oracle_closure_20261031.py', 'captured-closure')]:
        run([sys.executable, str(ROOT / script), '--cohort', str(cohort)], f'logs/integration/cohort{cohort}-{name}-audit-20261101.txt')
    reports = [f'evidence/verification/cohort{cohort}-committed-source-inputs-v14-20261105.json',
               f'evidence/verification/cohort{cohort}-captured-oracle-closure-verification-20261031.json']
    assert read_json(ROOT / reports[0])['passed'] and read_json(ROOT / reports[1])['committedVerification']['passed']
    receipt = f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json'
    write_json(ROOT / receipt, dict(cohort=cohort, sourceCommit=revision, passed=True, sourceCredit=0,
        fullCleanReplayProven=False, reports=[dict(path=p, sha256=sha256(ROOT / p)) for p in reports]))
    subprocess.run(['git', 'add', '--', *reports, receipt], cwd=ROOT, check=True)
    subprocess.run(['git', 'commit', '-m', f'Verify cohort {cohort} committed source and oracle closure'], cwd=ROOT, check=True)
    print(dict(cohort=cohort, sourceCommit=revision, sourceFunctions=len(selected), sourceBytes=plan['sourceLinkedBytes'], packaged=True), flush=True)


if __name__ == '__main__':
    main()
