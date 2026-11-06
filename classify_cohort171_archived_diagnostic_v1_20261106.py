from project import ROOT, read_json, sha256

TARGET = 'evidence/lanes/parallel-wave20261106/main-grid-resume-next/first/failed-unsealed-v1/wave20261106_main_grid_resume_first_build.py'
TARGET_SHA = '58665018f47cbe55a57d8f0d85cb909350bc5016767dd66ff3ef830cf7852927'
READY = 'evidence/lanes/parallel-wave20261106/main-grid-resume-next/first/ready.json'
READY_SHA = '1e8018292d6f0c958c5556cbafa864adc81fa3c8e0ba910456162512cad4e1db'


def classify(cohort, row):
    if cohort != 171 or row.get('path') != TARGET or row.get('sha256') != TARGET_SHA:
        return False
    if row.get('frozenRegisteredInput') is not False or row.get('frozenOracleInput') is not False:
        return False
    assert sha256(ROOT / TARGET) == TARGET_SHA and sha256(ROOT / READY) == READY_SHA
    ready = read_json(ROOT / READY)
    pins = {p['path']: p['sha256'] for p in ready['files']}
    assert pins[TARGET] == TARGET_SHA
    receipt = TARGET.rsplit('/', 1)[0] + '/receipt.json'
    assert sha256(ROOT / receipt) == pins[receipt] == 'a73830145466df232cb730946fc18b44dc73bbabf6585c3779a2221e4660a631'
    failure = read_json(ROOT / receipt)
    assert failure['sourceCredit'] == 0 and failure['originalAddedAssertionFailed']
    frozen = read_json(ROOT / 'evidence/verification/cohort171-frozen-ordinary-union-20261106.json')
    assert dict(path=READY, sha256=READY_SHA) in frozen['readys']
    registry = read_json(ROOT / 'recovery.json')
    assert not any(TARGET in batch['sourceHashes'] for batch in registry['batches'])
    closure = read_json(ROOT / 'evidence/verification/cohort171-captured-oracle-closure-20261031.json')
    assert TARGET not in closure['sourceAndEvidenceHashes']
    row.update(classified=True, frozenUncreditedLaneDiagnostic=True,
        immutableReadyManifest=READY, immutableReadyManifestSha256=READY_SHA,
        archivedFailedAttemptReceipt=receipt, originalDiagnosticBytesPreserved=True)
    return True
