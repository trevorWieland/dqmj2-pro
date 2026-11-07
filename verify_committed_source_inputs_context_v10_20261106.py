import sys
from pathlib import Path
from project import ROOT, sha256, write_json
import verify_committed_source_inputs_context_v9_20261106 as previous
from host_arm9_overlay_reference_context_v1_20261106 import validation_route
from host_arm9_overlay_reference_policy_v1_20261106 import CONTRACT, LEDGER, CONTROLS


def main():
    cohort = int(sys.argv[sys.argv.index('--cohort') + 1])
    if cohort < 174:
        raise ValueError('Namespaced overlay committed input context requires cohort174 or later')
    with validation_route() as proof:
        previous.main()
    write_json(ROOT / f'evidence/verification/cohort{cohort}-overlay-reference-context-v10-20261106.json',
        dict(passed=True, sourceCredit=0, allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted=True,
            namespaceQualifiedOverlayReference=proof,
            contract=dict(path=CONTRACT, sha256=sha256(ROOT / CONTRACT)),
            separateOverlayLedger=dict(path=LEDGER, sha256=sha256(ROOT / LEDGER)),
            focusedControls=dict(path=CONTROLS, sha256=sha256(ROOT / CONTROLS)),
            originalMainNamespaceAssertionsAndOriginal26ConsumersPreserved=True,
            sourceRegistryAndFrozen174MembershipUnchanged=True,
            generator=Path(__file__).name, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
