from project import ROOT, read_json, sha256
from classify_cohort171_archived_diagnostic_v1_20261106 import classify as classify_previous

LOG = 'evidence/attempts/cohort171-archived-diagnostic-sealing-failure-20261106/original-whitespace-findings.txt'
LOG_SHA = '135904169e87ccfbd49be8aaff689c8d3a6a3bcdd612e78f028d0d7769a5e75d'
BUNDLE = 'evidence/verification/cohort171-preserved-sealing-diagnostic-bundle-v1-20261106.json'


def classify(cohort, row):
    if classify_previous(cohort, row):
        return True
    if cohort != 171 or row.get('path') != LOG or row.get('sha256') != LOG_SHA:
        return False
    if row.get('frozenRegisteredInput') is not False or row.get('frozenOracleInput') is not False:
        return False
    bundle = read_json(ROOT / BUNDLE)
    assert bundle['sourceCredit'] == 0 and bundle['verbatimFailureEvidence']
    assert sha256(ROOT / bundle['originalFailedDriver']) == bundle['originalFailedDriverSha256']
    failed = read_json(ROOT / bundle['originalFailedDriver'])
    assert failed['state'] == 'failed' and failed['steps'][-1]['exitCode'] == 1
    assert failed['steps'][-1]['command'][0] == 'finish_source_package_v24_20261106.py'
    pins = {p['path']: p['sha256'] for p in bundle['files']}
    assert pins[LOG] == LOG_SHA and sha256(ROOT / LOG) == LOG_SHA
    assert all(sha256(ROOT / path) == digest for path, digest in pins.items())
    driver_copy = LOG.rsplit('/', 1)[0] + '/failed-driver-v41.json'
    assert (ROOT / driver_copy).read_bytes() == (ROOT / bundle['originalFailedDriver']).read_bytes()
    assert not any(LOG in b['sourceHashes'] for b in read_json(ROOT / 'recovery.json')['batches'])
    closure = read_json(ROOT / 'evidence/verification/cohort171-captured-oracle-closure-20261031.json')
    assert LOG not in closure['sourceAndEvidenceHashes']
    row.update(classified=True, verbatimUncreditedFailureLog=True, preservedDiagnosticBundle=BUNDLE,
        preservedDiagnosticBundleSha256=sha256(ROOT / BUNDLE), originalDiagnosticBytesPreserved=True)
    return True
