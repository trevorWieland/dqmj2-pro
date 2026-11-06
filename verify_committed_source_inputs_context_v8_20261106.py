import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import verify_committed_source_inputs_context_v7_20261106 as original
from embedded_reference_link_context_v1_20261106 import validation_route


def main():
    cohort = int(sys.argv[sys.argv.index('--cohort') + 1])
    assert cohort >= 171
    for name in ['verify_committed_source_inputs_context_v8_20261106.py',
            'embedded_reference_link_context_v1_20261106.py',
            'qualify_embedded_reference_link_context_v1_20261106.py']:
        assert subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT) == (ROOT / name).read_bytes()
    receipt = 'evidence/verification/cohort171-embedded-reference-link-route-v1-20261106.json'
    assert subprocess.check_output(['git', 'show', 'HEAD:' + receipt], cwd=ROOT) == (ROOT / receipt).read_bytes()
    proof = read_json(ROOT / receipt)
    assert proof['passed'] and proof['supportedFunctions'] == 7 and len(proof['negativeControls']) == 119
    assert proof['helper']['sha256'] == sha256(ROOT / proof['helper']['path'])
    with validation_route():
        original.main()
    write_json(ROOT / f'evidence/verification/cohort{cohort}-embedded-reference-context-v8-20261106.json',
        dict(passed=True, sourceCredit=0, allOriginalV7AndUnderlyingAuditsCompleted=True,
            embeddedAndLegacyFlatContractsChecked=True, missingOutputNeverSynthesizedFromNative=True,
            qualificationReceipt=dict(path=receipt, sha256=sha256(ROOT / receipt)),
            generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
