import re
from project import ROOT, read_json, sha256


def select(expanded, cohort):
    assert expanded['passed']
    pattern = rf'evidence/verification/cohort{cohort}-committed-source-inputs-v(6|7|8|9|10|11|12)-(20261101|20261105)\.json'
    candidates = [r for r in expanded['reports'] if re.fullmatch(pattern, r['path'])]
    assert len(candidates) == 1
    entry = candidates[0]
    assert sha256(ROOT / entry['path']) == entry['sha256']
    proof = read_json(ROOT / entry['path'])
    assert proof['passed'] and proof['cohort'] == cohort and proof['commit'] == expanded['sourceCommit']
    version = int(re.fullmatch(pattern, entry['path'])[1])
    if version >= 9:
        assert proof['previousEightInputVerifierUnchanged'] is True
        assert proof['sourceCredit'] == 0
    if version >= 12:
        assert proof['exactFrozenRegistryUnmodified'] is True
        assert len(proof['qualifiedCopiedReferenceInputs']) == 4
    return entry['path']
