from project import ROOT, read_json, sha256


BUNDLE = 'evidence/lanes/parallel-wave20261106/selection-snapshot-next/production-wrapper-handoff.json'
BUNDLE_SHA = '80a5e1d1684967295d9c230a3cd6e18d7eb5dc5eb79530681bd837d866f2c566'


def verify():
    assert sha256(ROOT / 'run_source_cohort_20261101.py') == '9a33d505f728eb77f6846bbff7b2094208bad42ae8a4960bf6dd9d7bb5f61fa1'
    assert sha256(ROOT / BUNDLE) == BUNDLE_SHA
    proof = read_json(ROOT / BUNDLE)
    assert proof['passed'] and proof['sourceCredit'] == 0 and proof['allOriginal269ControlsPassed']
    for pin in proof['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    return dict(originalStage='verify_source_selection.py',
                actualStage='verify_source_selection_v2_20261106.py', qualification=BUNDLE,
                qualificationSha256=BUNDLE_SHA, originalFullMainAndAllControlsRetained=True,
                originalFreshSourceObjectAndDependencyChecksRetained=True)
