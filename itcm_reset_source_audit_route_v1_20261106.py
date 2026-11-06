import copy
from contextlib import contextmanager
from unittest.mock import patch
from project import ROOT, read_json
import qualify_arm9_overlay_reference_inputs_20261105 as overlay
import verify_committed_source_inputs_v14_20261105 as audit
from qualify_itcm_reset_reference_v1_20261106 import REPORT, IMAGE, ITCM, qualify


def project(actual, proof):
    selected = [b for b in actual if b['report'] == REPORT]
    assert len(selected) == 1
    assert {p: h for p, h in selected[0]['sourceHashes'].items() if p.startswith('extract/')} == proof['originalDerivedNativeInputs']
    assert set(proof['originalDerivedNativeInputs']) == {IMAGE, ITCM}
    copies = copy.deepcopy(actual)
    row = next(b for b in copies if b['report'] == REPORT)
    for name in proof['originalDerivedNativeInputs']:
        del row['sourceHashes'][name]
    assert all(a == b for a, b in zip(actual, copies) if a['report'] != REPORT)
    return copies


@contextmanager
def route():
    original = audit.qualify_overlay

    def qualified_overlay(actual, directory):
        if not any(b['report'] == REPORT for b in actual):
            return original(actual, directory)
        proof = qualify()
        previous_projection = overlay.project_batches

        def projected(batches, report, declared):
            return previous_projection(project(batches, proof), report, declared)

        with patch.object(overlay, 'project_batches', projected):
            batches, evidence = original(actual, directory)
        evidence['independentItcmResetReferenceQualification'] = proof
        evidence['originalRegistryIdentityAndAllOtherReferenceGuardsRetained'] = True
        return batches, evidence

    with patch.object(audit, 'qualify_overlay', qualified_overlay):
        yield
