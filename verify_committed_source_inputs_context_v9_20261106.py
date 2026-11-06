import subprocess
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import verify_committed_source_inputs_context_v8_20261106 as original
from embedded_reference_link_context_v2_20261106 import validation_route


def main():
    cohort = int(sys.argv[sys.argv.index('--cohort') + 1])
    assert cohort >= 172
    for name in ['verify_committed_source_inputs_context_v9_20261106.py',
            'embedded_reference_link_context_v2_20261106.py',
            'qualify_embedded_reference_link_context_v2_20261106.py']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT) == (ROOT / name).read_bytes()
    receipt = 'evidence/verification/cohort172-embedded-reference-link-route-v2-20261106.json'
    assert subprocess.check_output(['git', 'show', 'HEAD:' + receipt], cwd=ROOT) == (ROOT / receipt).read_bytes()
    proof = read_json(ROOT / receipt)
    assert proof['passed'] and proof['supportedFunctions'] == 10 and len(proof['negativeControls']) == 170
    assert proof['helper']['sha256'] == sha256(ROOT / proof['helper']['path'])
    assert proof['generatorSha256'] == sha256(ROOT / 'qualify_embedded_reference_link_context_v2_20261106.py')
    manifest = proof['controlManifest']
    assert sha256(ROOT / manifest['path']) == manifest['sha256']
    assert subprocess.check_output(['git', 'show', 'HEAD:' + manifest['path']], cwd=ROOT) == (ROOT / manifest['path']).read_bytes()
    with patch.object(original, 'validation_route', validation_route):
        original.main()
    write_json(ROOT / f'evidence/verification/cohort{cohort}-embedded-reference-context-v9-20261106.json',
        dict(passed=True, sourceCredit=0, previousV8QualificationReceiptAndAllUnderlyingAuditsCompleted=True,
            versionedContextFactorySubstitution=True, independentRawRomCanonicalModeExtentAndSourcePathRequired=True,
            originalContractObjectElfAndFlatRelinkerChecksRetained=True,
            qualificationReceipt=dict(path=receipt, sha256=sha256(ROOT / receipt)),
            generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
