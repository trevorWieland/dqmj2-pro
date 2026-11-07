import copy
import uuid
from contextlib import contextmanager
from unittest.mock import patch
from project import ROOT
import qualify_arm9_overlay_reference_inputs_20261105 as overlay
from host_arm9_overlay_reference_policy_v1_20261106 import load_contract, verify_committed_promotion, ensure_scope
from host_arm9_overlay_reference_v1_20261106 import qualify, _comparison_projection


@contextmanager
def validation_route():
    contract = load_contract()
    verify_committed_promotion(contract)
    directory = ROOT / 'work/integration/host-arm9-overlay-reference-v1' / ('committed-' + uuid.uuid4().hex[:12])
    proof = qualify(contract, directory, committed=True)
    previous = overlay.project_batches
    projections = []

    def projected(actual, report, declared):
        ensure_scope(proof['liveScope'])
        copies, removed = _comparison_projection(actual, contract)
        projections.append(copy.deepcopy(removed))
        return previous(copies, report, declared)

    try:
        with patch.object(overlay, 'project_batches', projected):
            yield proof
    finally:
        ensure_scope(proof['liveScope'])
        proof['comparisonProjectionInvocations'] = len(projections)
        proof['projectedOriginalComparisonRoles'] = projections
        proof['originalRegistryGateAndPriorProjectorsPreserved'] = True
