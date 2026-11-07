from project import ROOT, read_json, sha256
from qualified_context_builder_entrypoint_v3_20261106 import verify as verify_previous


def verify():
    previous = verify_previous()
    name = 'evidence/verification/context-builder-v4-cli-entrypoint-qualification-20261106.json'
    proof = read_json(ROOT / name)
    assert proof['passed'] and proof['sourceCredit'] == 0
    assert proof['actualOsLockExitAndExceptionCleanupPassed']
    for path, expected in proof['qualifiedHashes'].items():
        assert sha256(ROOT / path) == expected
    module_name = 'evidence/verification/mb-register-module-route-v2-qualification-20261106.json'
    module = read_json(ROOT / module_name)
    assert module['passed'] and module['allModuleBytesExact'] and module['strictSymbolsPassed']
    assert module['previousAcceptedCorpusIncluded'] and module['hostArm9ModuleComparisons'] == 11
    assert module['allBaselineSourceUnitIdentitiesPreserved'] and module['preparedSourceAndAllObjectInputsUnchanged']
    assert len(module['controls']['rejectedActualElfMutations']) == 10
    assert sha256(ROOT / module['route']['path']) == module['route']['sha256']
    assert module['generatorSha256'] == sha256(ROOT / 'retry_mb_register_prepared_link_v1_20261106.py')
    return dict(previous, scopedRegisterModuleQualification=module_name,
        scopedRegisterModuleQualificationSha256=sha256(ROOT / module_name),
        newCliEntryPointQualification=name, newCliEntryPointQualificationSha256=sha256(ROOT / name),
        unmodifiedWholeCompilerObjectAndActualLocalBssRequired=True, initializedStorageCredit=0)
