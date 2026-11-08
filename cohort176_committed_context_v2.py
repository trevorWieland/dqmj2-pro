from contextlib import contextmanager
import importlib
import json
from pathlib import Path
from unittest.mock import patch
from cohort176_epoch_v1 import accounting, installed_projection, require, sha
import cohort176_legacy_live_v2 as legacy_live
import cohort176_native_reference_v1 as native
import cohort176_registered_paths_v1 as paths


@contextmanager
def path_route(epoch, root, legacy, contract):
    prepared = paths.prepare(epoch, legacy, contract)
    verifier = importlib.import_module(legacy.VERIFIER[:-3])
    require(Path(verifier.__file__).resolve() == root / legacy.VERIFIER and verifier.ROOT.resolve() == root, 'Wrong strict V8 module')
    with paths.installed(verifier, legacy, epoch, prepared, root) as proof:
        yield proof


@contextmanager
def bindings(epoch, root, ten, child, registered):
    saved_route, saved_accounting = registered.validation_route, registered.validate_accounting
    def route(actual_root, contract):
        require(Path(actual_root).resolve() == root, 'Wrong registered-path owner')
        return path_route(epoch, root, registered, contract)
    def checked(document, contract):
        registered.validate_contract(contract)
        require(epoch.committed_revision is not None and document.get('commit') == epoch.committed_revision
            and document.get('cohort') == 176, 'V8 report is not from this committed audit epoch')
        return accounting(document)
    with legacy_live.installed(epoch, ten, child):
        registered.validation_route, registered.validate_accounting = route, checked
        try:
            yield
        finally:
            unchanged = registered.validation_route is route and registered.validate_accounting is checked
            registered.validation_route, registered.validate_accounting = saved_route, saved_accounting
            require(unchanged, 'Registered path bindings changed unexpectedly')
            epoch.ensure()


@contextmanager
def validation_route(epoch, root, directory):
    import source_packet_committed_context as previous
    import qualify_arm9_overlay_reference_inputs_20261105 as overlay
    import qualify_ten_consumers_v2 as ten
    import qualify_child_snd_reference_v1_20261107 as child
    import registered_input_path_context_v1_20261107 as registered
    root = Path(root).resolve()
    epoch.ensure()
    committed_state(epoch, root, epoch.committed_revision)
    for module, name in [(previous, 'source_packet_committed_context.py'),
            (overlay, 'qualify_arm9_overlay_reference_inputs_20261105.py'),
            (ten, 'qualify_ten_consumers_v2.py'),
            (child, 'qualify_child_snd_reference_v1_20261107.py'),
            (registered, 'registered_input_path_context_v1_20261107.py')]:
        require(Path(module.__file__).resolve() == root / name and sha((root / name).read_bytes()) == epoch.current_hashes[name], 'Wrong historical context module')
        require(not hasattr(module, 'ROOT') or module.ROOT.resolve() == root, 'Wrong historical context root')
    with bindings(epoch, root, ten, child, registered):
        with previous.validation_route(176) as old:
            live = native.qualify(epoch, root, Path(directory) / 'new-host-reference')
            with installed_projection(overlay, epoch, live) as events:
                result = dict(cohort=176, commit=epoch.committed_revision, registrySha256=epoch.contract['registrySha256'],
                    contractCanonicalSha256=epoch.contract_hash, previousLiveContext=old, newHostLiveReference=dict(functions=6, bytes=1184,
                    c99Functions=5, thumbFunctions=1, compilerLinkProofs=live.rows,
                    inputHashes=live.inputs, sourceCredit=0), comparisonProjectionEvents=events,
                    originalMainLedgerFileConsumers=26, unchangedMainComparisonViewConsumers=36, sourceCredit=0)
                yield result
            live.ensure(epoch)
    epoch.ensure()


def committed_state(epoch, root, revision):
    root = Path(root).resolve()
    plan = json.loads(epoch.read_committed('evidence/verification/cohort-2026-10-29-176.json'))
    driver = json.loads(epoch.read_committed('evidence/verification/cohort176-validation-driver.json'))
    require(plan['sourceRegistrySha256'] == epoch.contract['registrySha256'] and plan['previousAcceptedCohort'] == 175,
        'Wrong finalized176 source transaction')
    require(not plan['linksPending'] and plan['moduleComparisonsExact'] == 20 and driver['state'] == 'build-and-regression-checks-passed' and len(driver['steps']) == 16,
        'Original16 acceptance gates incomplete')
    for name in ('evidence/verification/cohort-2026-10-29-176.json', 'evidence/verification/cohort176-validation-driver.json'):
        require(epoch.read_current(name) == epoch.read_committed(name), 'Acceptance state is not exact committed bytes')
    require(isinstance(revision, str) and len(revision) == 40 and all(c in '0123456789abcdef' for c in revision)
        and epoch.committed_revision == revision, 'Final audit commit must be the actual bound epoch')
    return dict(cohort=176, commit=revision, registrySha256=epoch.contract['registrySha256'], sourceCredit=0)
