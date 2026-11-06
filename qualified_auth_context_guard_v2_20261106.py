from project import ROOT, read_json, sha256
from auth_context_route_v2_20261106 import contract


def verify():
    name = 'evidence/verification/auth-context-production-routing-v2-qualification-20261106.json'
    proof = read_json(ROOT / name)
    assert proof['passed'] and proof['sourceCredit'] == proof['contextDataCredit'] == 0
    assert proof['scopeNegativeControlsPassed'] and proof['originalAllSharedChecksRetained']
    for path, expected in proof['qualifiedCodeAndDescriptorHashes'].items():
        assert sha256(ROOT / path) == expected
    declared = contract()
    assert proof['originalCompilerObjectSha256'] == declared['objectSha256']
    return dict(qualification=name, qualificationSha256=sha256(ROOT / name),
        onlyScopedAuthCallerFunctionExtractionChanged=True, originalIntegrationMainAndModuleChecksRetained=True,
        originalWholeCompilerObjectUnchanged=True, originalCompilerContextStorageCredit=0)
