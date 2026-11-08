from contextlib import contextmanager
import json
from pathlib import Path
from unittest.mock import patch
from cohort176_epoch_v1 import installed_projection, require, sha
import cohort176_committed_context_v2 as bindings
import cohort176_native_reference_v1 as native
import cohort176_scope_acceptance_v1 as acceptance


@contextmanager
def validation_route(epoch, root, directory, references, driver_pin):
    import source_packet_committed_context as original
    import qualify_arm9_overlay_reference_inputs_20261105 as overlay
    import qualify_ten_consumers_v2 as ten
    import qualify_child_snd_reference_v1_20261107 as child
    import registered_input_path_context_v1_20261107 as registered
    root, directory = Path(root).resolve(), Path(directory).resolve()
    require(directory.is_relative_to(root / 'work') and not directory.exists(), 'Exclusive committed-context WORK output required')
    scope = acceptance.committed(epoch, root, references, driver_pin)
    plan = scope['receipt']
    require(plan['sourceRegistrySha256'] == epoch.contract['registrySha256'], 'Scoped registry differs from exact descendant epoch')
    for module, name in [(original, 'source_packet_committed_context.py'), (overlay, 'qualify_arm9_overlay_reference_inputs_20261105.py'),
            (ten, 'qualify_ten_consumers_v2.py'), (child, 'qualify_child_snd_reference_v1_20261107.py'),
            (registered, 'registered_input_path_context_v1_20261107.py')]:
        require(Path(module.__file__).resolve() == root / name and sha((root / name).read_bytes()) == epoch.current_hashes[name], 'Wrong original committed module')
        require(not hasattr(module, 'ROOT') or module.ROOT.resolve() == root, 'Wrong original module root')
    contract = original.load_contract()
    original.verify_committed_promotion(contract)
    predecessor = json.loads(epoch.read_committed('evidence/verification/cohort175-expanded-source-closure-20261101.json'))
    frozen = json.loads(epoch.read_committed('evidence/verification/cohort174-expanded-source-closure-20261101.json'))
    current_preferences = epoch.read_current('source-preferences.json')
    adjusted, append = original.extend_contract(contract,
        original.blob('source-preferences.json', frozen['sourceCommit']),
        original.blob('source-preferences.json', predecessor['sourceCommit']), current_preferences, plan)
    validated = original.preferences(plan['exactRom']['sha256'])
    require(len(validated) == append['currentPreferences'] == 187, 'Original preference validation incomplete')
    linked = original.read_json(root / 'evidence/verification/linked-source-preferences-20261030.json')
    require(linked['passed'] is True and linked['actualLinkedSourceProvenanceChecked']
        and linked['sourcePreferenceSha256'] == sha(current_preferences)
        and linked['sourceMapSha256'] == original.sha256(root / 'source-map.json')
        and linked['sourceUnitsSha256'] == original.sha256(root / 'build/link-work/source-units.json')
        and len(linked['preferredInputs']) == len(validated), 'Original actual-linked preference/source-map/unit guard failed')
    proof = original.qualify(adjusted, directory / 'old-overlay', committed=True)
    append.update(cohort=176, commit=epoch.committed_revision, originalMigrationAuditsValidated=len(validated),
        linkedPreferenceReceiptSha256=original.sha256(root / 'evidence/verification/linked-source-preferences-20261030.json'),
        predecessorSourceCommit=predecessor['sourceCommit'], frozen174SourceCommit=frozen['sourceCommit'])
    proof['preferenceAppendExtension'] = append
    prior_project = overlay.project_batches
    old_events = []
    def old_overlay(actual, report, declared):
        original.ensure_scope(proof['liveScope'])
        copies, events = original._comparison_projection(actual, adjusted)
        old_events.append(events)
        return prior_project(copies, report, declared)
    try:
        with patch.object(overlay, 'project_batches', old_overlay):
            with bindings.bindings(epoch, root, ten, child, registered):
                current_contract = ten.load_contract()
                with ten.route(current_contract, directory / 'main-ten') as current:
                    proof['currentMainReferenceQualification'] = current
                    child_contract = original.read_json(child.CONTRACT)
                    with child.route(child_contract, directory / 'child-snd') as child_proof:
                        proof['childArm9ReferenceQualification'] = child_proof
                        path_contract = original.read_json(root / registered.CONTRACT)
                        with registered.validation_route(root, path_contract) as paths:
                            proof['registeredInputPathQualification'] = paths
                            live = native.qualify(epoch, root, directory / 'new-host')
                            with installed_projection(overlay, epoch, live) as events:
                                result = dict(cohort=176, commit=epoch.committed_revision, acceptanceScope='current-main-matching-inputs',
                                    sourceCredit=0, MainMatchingWorkspaceScope=scope, namespaceQualifiedOverlayReference=proof,
                                    newHostLiveReference=dict(functions=6, bytes=1184, c99Functions=5, thumbFunctions=1,
                                        compilerLinkProofs=live.rows, inputHashes=live.inputs), comparisonProjectionEvents=events,
                                    originalMainLedgerFileConsumers=26, unchangedMainComparisonViewConsumers=36,
                                    originalFullDriverAndWorkspaceUnmodified=True)
                                yield result
                            live.ensure(epoch)
                            report = original.read_json(root / 'evidence/verification/cohort176-committed-source-inputs-v14-20261105.json')
                            paths['observedAccounting'] = registered.validate_accounting(report, path_contract)
    finally:
        original.ensure_scope(proof['liveScope'])
        acceptance.ensure_committed(epoch, scope)
        epoch.ensure()
        proof['comparisonProjectionInvocations'] = len(old_events)
        proof['projectedOriginalComparisonRoles'] = old_events
        proof['originalRegistryGateAndPriorProjectorsPreserved'] = True


EPOCH_CONTRACT = 'cohort176-epoch-contract-v3.json'
SCOPE_CONTRACT = 'provenance/cohort176-main-matching-workspace-contract-v1-20261108.json'
SCOPE_PROOF = 'evidence/verification/cohort176-main-workspace-scope-20261108.json'
REPORT = 'evidence/verification/cohort176-current-scope-context-v1-20261108.json'


def run_inherited(epoch, root, directory, references, driver_pin):
    import sys
    import verify_committed_source_inputs_context_v9_20261106 as previous
    root = Path(root).resolve()
    name = 'verify_committed_source_inputs_context_v9_20261106.py'
    require(Path(previous.__file__).resolve() == root / name and previous.ROOT.resolve() == root
        and sha((root / name).read_bytes()) == epoch.current_hashes[name], 'Wrong inherited V9 entrypoint')
    with validation_route(epoch, root, directory, references, driver_pin) as proof:
        argv = sys.argv
        try:
            sys.argv = [str(root / name), '--cohort', '176']
            previous.main()
        finally:
            sys.argv = argv
    epoch.ensure()
    return dict(passed=True, cohort=176, commit=epoch.committed_revision, sourceCredit=0,
        acceptanceScope='current-main-matching-inputs', allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted=True,
        canonicalRegistryEpochAuthenticated=True, historical1375BatchRecordsPreserved=True,
        originalFullDriverPassed=False, originalHistoricalWorkspacePassed=False,
        MainMatchingWorkspaceScope=proof['MainMatchingWorkspaceScope'], contextQualification=proof,
        generator=Path(__file__).name, generatorSha256=sha(Path(__file__).read_bytes()))


def ensure_epoch_contract(epoch, pin):
    raw = epoch.read_current(pin['path'])
    require(sha(raw) == pin['sha256'] and len(raw) == pin['bytes']
        and raw == epoch.read_committed(pin['path']), 'Epoch contract is not exact committed bytes')


def main():
    import argparse
    from datetime import datetime, timezone
    import subprocess
    import uuid
    from cohort176_epoch_v1 import Epoch, canonical
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, choices=[176], required=True)
    for role in ('epoch-contract', 'scope-contract', 'scope-proof', 'scope-driver'):
        parser.add_argument('--' + role + '-sha256', required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    target = root / REPORT
    require(not target.exists() and target.parent.resolve() == target.parent.absolute(), 'Exclusive canonical context report required')
    def pinned(name, expected):
        raw = acceptance.checked(root, dict(path=name, sha256=expected))
        return dict(path=name, sha256=expected, bytes=len(raw))
    epoch_pin = pinned(EPOCH_CONTRACT, args.epoch_contract_sha256)
    contract = json.loads(acceptance.checked(root, epoch_pin))
    references = dict(contract=pinned(SCOPE_CONTRACT, args.scope_contract_sha256),
        preproof=pinned(SCOPE_PROOF, args.scope_proof_sha256))
    driver_pin = pinned(acceptance.SCOPED_DRIVER, args.scope_driver_sha256)
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    epoch = Epoch.committed(root, contract, canonical(contract), revision)
    ensure_epoch_contract(epoch, epoch_pin)
    output = root / 'work/integration/cohort176-current-scope-context' / uuid.uuid4().hex
    report = run_inherited(epoch, root, output, references, driver_pin)
    ensure_epoch_contract(epoch, epoch_pin)
    report.update(createdUtc=datetime.now(timezone.utc).isoformat(), epochContract=epoch_pin,
        scopeContract=references['contract'], workspaceScopeProof=references['preproof'], scopedDriver=driver_pin)
    epoch.ensure()
    with target.open('x', encoding='utf-8', newline='\n') as stream:
        json.dump(report, stream, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
