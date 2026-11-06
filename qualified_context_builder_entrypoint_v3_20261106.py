from project import ROOT, read_json, sha256
from qualified_auth_context_guard_v2_20261106 import verify as verify_mapping


def verify():
    mapping = verify_mapping()
    name = 'evidence/verification/context-builder-v3-cli-entrypoint-qualification-20261106.json'
    proof = read_json(ROOT / name)
    assert proof['passed'] and proof['sourceCredit'] == 0
    assert proof['originalLockExitStatusAndExceptionPropagationRestored']
    for path, expected in proof['qualifiedHashes'].items():
        assert sha256(ROOT / path) == expected
    return dict(mapping, cliEntryPointQualification=name, cliEntryPointQualificationSha256=sha256(ROOT / name),
        originalBuildLockAndExitStatusRetained=True, originalBuilderMainAndIntegrationChecksRetained=True)
