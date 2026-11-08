import copy
from datetime import datetime
import importlib
import json
from pathlib import Path
from cohort176_epoch_v1 import NEW, PREFS, canonical, require, safe, sha


PENDING = dict(path='provenance/cohort176-original-pending-plan-20261108.json', bytes=2486,
    sha256='fb4454849a40683fce80cfff9a43e9d7aaafc9a2e87f2973537ec416101d26de')
PLAN = 'evidence/verification/cohort-2026-10-29-176.json'
FAILED = 'evidence/verification/cohort176-validation-driver.json'
WORKSPACE = 'evidence/verification/workspace.json'
FAILED_PIN = dict(path=FAILED, bytes=8355, sha256='ba6d931869ba8838932b6b454852adad9bb20c49a56094973e6dc78433a6d218')
WORKSPACE_PIN = dict(path=WORKSPACE, bytes=11405305, sha256='af5bb0b30e19bc8608f91cd1f7bef16dcd91a13c2fa6b1466bfd9e11487ed3a1')
SCOPED_DRIVER = 'evidence/verification/cohort176-current-scope-driver-20261108.json'
HELPER_SHA = '628d027d95d8509f0586a64da7878e3d12d4eee0998dc5330ba05cfa88587ad2'
BUILDER_SHA = '0c3fcd7eda933054b858c77fc73a8919d612be18c053bbba3c7c8b2034d3636d'
FALSE_FIELDS = ('allRecordedFilesUnchanged', 'baselineAndInputsUnchanged', 'applicationObservedUnchanged',
    'strictWholeWorkspaceIsolationPassed', 'fullToolDelivery', 'fullCleanReplayOfThisCohortProven')
JSON_ROLES = {'preservation', 'critical', 'tools', 'equivalents', 'candidate', 'supplement',
    'workspace', 'driver', 'plan', 'manifest', 'freshness', 'checksum', 'getters'}


def checked(root, pin):
    require(set(pin) <= {'path', 'sha256', 'bytes'} and {'path', 'sha256'} <= set(pin), 'Unknown or missing pin field')
    path = root / safe(pin['path'])
    require(path.resolve() == path.absolute() and path.is_file(), 'Missing or redirected scope input')
    raw = path.read_bytes()
    require(sha(raw) == pin['sha256'] and ('bytes' not in pin or len(raw) == pin['bytes']), 'Scope pin differs')
    return raw


class Acceptance:
    def __init__(self, references, contract, bundle, proof, builder):
        require(set(references) == {'contract', 'preproof'}, 'Unknown acceptance input reference')
        require(set(contract['jsonPins']) == JSON_ROLES and contract['schemaVersion'] == 1 and contract['cohort'] == 176, 'Wrong scope contract schema')
        require(contract['jsonPins']['plan'] == PENDING, 'Immutable original pending plan required')
        require(contract['jsonPins']['driver'] == FAILED_PIN and contract['jsonPins']['workspace'] == WORKSPACE_PIN, 'Original failed records changed')
        membership = [r for r in contract['membershipPins'] if r['path'] == PENDING['path']]
        require(membership == [PENDING] and not any(r['path'] == PLAN for r in contract['membershipPins']), 'Live plan still pinned as pending membership')
        require(contract['registrySha256'] == NEW and contract['preferenceSha256'] == PREFS, 'Wrong matching-input epoch')
        pending, driver, manifest = bundle['plan'], bundle['driver'], bundle['manifest']
        require(pending['linksPending'] is True and pending['previousAcceptedCohort'] == 175
            and pending['sourceRegistrySha256'] == NEW and pending['sourcePreferenceSha256'] == PREFS, 'Wrong original pending state')
        require(pending['expectedSourceMatchedFunctions'] == 11660 and pending['expectedSourceLinkedBytes'] == 1267058
            and pending['newSourceFunctions'] == 8 and pending['newSourceBytes'] == 1412, 'Wrong source transaction delta')
        require(pending['duplicateMigrationFunctions'] == 0 and pending['preferredSourceInputsRequired'] == 187, 'Preference scope changed')
        require(driver['state'] == 'failed' and len(driver['steps']) == 16 and driver['sourceRegistrySha256'] == NEW, 'Original failed driver changed')
        require(all(type(s['exitCode']) is int and s['exitCode'] == 0 for s in driver['steps'][:15])
            and driver['steps'][15]['command'] == ['verify_workspace.py'] and driver['steps'][15]['exitCode'] == 1, 'Original actual gate outcomes changed')
        require(proof['MainMatchingWorkspaceScopePassed'] is True and proof['contractSha256'] == references['contract']['sha256']
            and proof['historicalOriginalGateExitCode'] == 1 and proof['preservedSuccessfulGates'] == 15, 'No exact scoped qualification')
        require(all(proof[name] is False for name in FALSE_FIELDS), 'Historical or delivery failure hidden')
        require(proof['sourceCreditAddedByScopeRepair'] == 0 and proof['sourceRegistrySha256'] == NEW
            and proof['sourcePreferenceSha256'] == PREFS, 'Scope repair changed credit or epoch')
        require(proof['sourceMatchedFunctions'] == manifest['functionMatched'] == 11660
            and proof['sourceLinkedBytes'] == manifest['sourceLinkedBytes'] == 1267058
            and proof['moduleComparisonsExact'] == 20, 'Current source or link counts differ')
        require(proof['currentAuthoredFiles'] == 43638 + len(contract['extraSupportPins'])
            and proof['unacceptedCandidateFiles'] == 2 and proof['extraSupportFiles'] == len(contract['extraSupportPins']), 'Authored support count differs')
        require(proof['checksumVectors'] == 36 and proof['checksumActualReturns'] == 144 and proof['getterComparisons'] == 5117, 'Native oracle scope differs')
        require(bundle['workspace']['isolation']['allRecordedFilesUnchanged'] is False
            and bundle['workspace']['isolation']['baselineAndInputsUnchanged'] is False
            and bundle['workspace']['isolation']['applicationObservedUnchanged'] is False, 'Original workspace failure hidden')
        self.references, self.contract, self.bundle, self.proof = map(copy.deepcopy, (references, contract, bundle, proof))
        self.builder = builder

    def record_references(self):
        manifest = self.bundle['manifest']
        result = dict(originalPendingPlan=copy.deepcopy(PENDING), originalFailedDriver=copy.deepcopy(FAILED_PIN),
            originalWorkspace=copy.deepcopy(WORKSPACE_PIN), contract=copy.deepcopy(self.references['contract']),
            proof=copy.deepcopy(self.references['preproof']), manifest=copy.deepcopy(self.contract['jsonPins']['manifest']),
            getters=copy.deepcopy(self.contract['jsonPins']['getters']), exactRom=copy.deepcopy(self.bundle['supplement']['exactLayoutROM']),
            scopedDriver=dict(path=SCOPED_DRIVER), manifestFacts=dict(initializedModuleByteDenominator=sum(m['bytes'] for m in manifest['modules']),
                sourceMatchedFunctionBytes=manifest['sourceMatchedFunctionBytes'], sourceMatchedDataBytes=manifest['sourceMatchedDataBytes']))
        require(set(result) == {'originalPendingPlan', 'originalFailedDriver', 'originalWorkspace', 'contract', 'proof', 'manifest',
            'getters', 'exactRom', 'scopedDriver', 'manifestFacts'}, 'Unknown builder reference')
        require(set(result['manifestFacts']) == {'initializedModuleByteDenominator', 'sourceMatchedFunctionBytes', 'sourceMatchedDataBytes'}, 'Unknown manifest fact')
        return result

    def records(self, created):
        return self.builder.build_records(self.bundle['plan'], self.proof, self.bundle['driver'], self.record_references(), created)

    def driver(self):
        return self.records(self.proof['qualificationCompletedUtc'])[0]

    def receipt(self, driver_pin, created):
        driver, receipt = self.records(created)
        require(canonical(driver_pin) == canonical(receipt['scopedDriver']), 'Scoped driver pin differs from shared serialization')
        return receipt


def live_state(root, references):
    root = Path(root).resolve()
    require(set(references) == {'contract', 'preproof'}, 'Unknown scope input')
    contract = json.loads(checked(root, references['contract']))
    preproof = json.loads(checked(root, references['preproof']))
    require(contract['jsonPins']['plan'] == PENDING, 'Pending plan pin must be immutable')
    bundle = {name: json.loads(checked(root, pin)) for name, pin in contract['jsonPins'].items()}
    require(sha(checked(root, PENDING)) == PENDING['sha256'], 'Pending snapshot changed')
    module = importlib.import_module('cohort176_main_matching_workspace_scope')
    require(Path(module.__file__).resolve() == root / 'cohort176_main_matching_workspace_scope.py'
        and sha(Path(module.__file__).read_bytes()) == HELPER_SHA, 'Wrong live scope qualifier')
    actual = module.qualify(root, references['contract']['path'], references['contract']['sha256'])
    captured = copy.deepcopy(preproof)
    completed = captured.pop('qualificationCompletedUtc')
    require(isinstance(completed, str) and datetime.fromisoformat(completed).utcoffset() is not None, 'Explicit finalizer timestamp metadata required')
    require(canonical(actual) == canonical(captured), 'Matching-input scope changed since captured preproof')
    builder = importlib.import_module('cohort176_scope_state')
    require(Path(builder.__file__).resolve() == root / 'cohort176_scope_state.py'
        and sha(Path(builder.__file__).read_bytes()) == BUILDER_SHA, 'Wrong shared record builder')
    return Acceptance(references, contract, bundle, preproof, builder)


def precommit(root, references, driver_pin, created):
    state = live_state(root, references)
    require(canonical(json.loads(checked(Path(root).resolve(), driver_pin))) == canonical(state.driver()), 'Scoped driver differs')
    receipt = state.receipt(driver_pin, created)
    expected = state.builder.encode(receipt)
    require(checked(Path(root).resolve(), state.builder.pin(PLAN, expected)) == expected, 'Canonical current-scope receipt differs before finisher')
    return receipt


def committed(epoch, root, references, driver_pin):
    require(epoch.committed_revision is not None, 'Committed matching-scope epoch required')
    epoch.ensure()
    state = live_state(root, references)
    root = Path(root).resolve()
    names = list(dict.fromkeys([PLAN, FAILED, WORKSPACE, PENDING['path'], driver_pin['path'],
        *[p['path'] for p in references.values()], *[p['path'] for p in state.contract['extraSupportPins']]]))
    for name in names:
        require(epoch.read_current(name) == epoch.read_committed(name), 'Scope acceptance input is not exact committed bytes')
    driver = json.loads(checked(root, driver_pin))
    require(canonical(driver) == canonical(state.driver()), 'Committed scoped driver differs')
    receipt = json.loads(epoch.read_current(PLAN))
    require(canonical(receipt) == canonical(state.receipt(driver_pin, receipt['acceptedBuildCreatedUtc'])), 'Canonical receipt is not the truthful finalized scope')
    epoch.ensure()
    pins = [dict(path=name, sha256=sha(epoch.read_current(name))) for name in names]
    return dict(cohort=176, commit=epoch.committed_revision, receipt=receipt, scopeDriver=driver,
        liveScopeProof={k: v for k, v in state.proof.items() if k != 'qualificationCompletedUtc'},
        acceptanceQualificationCompletedUtc=state.proof['qualificationCompletedUtc'], definingRecordPins=pins, acceptanceScope='current-main-matching-inputs', sourceCreditAddedByScopeRepair=0)


def ensure_committed(epoch, snapshot):
    epoch.ensure()
    require(snapshot['commit'] == epoch.committed_revision, 'Scope acceptance commit changed')
    for pin in snapshot['definingRecordPins']:
        raw = epoch.read_current(pin['path'])
        require(sha(raw) == pin['sha256'] and raw == epoch.read_committed(pin['path']), 'Defining acceptance record changed')
