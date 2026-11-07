import hashlib
import json
import os
import subprocess
import sys
import uuid
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE if (HERE / 'project.py').is_file() else Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT))
from host_arm9_overlay_reference_policy_v1_20261106 import load_contract


SPEC = 'cohort174-parallel-wave20261105-s-specification.json'
MAIN = 'provenance/arm9-reference-only-consumers-20261101.json'
THUMB = 'provenance/arm9-thumb-reference-only-consumers-20261105.json'
ARM_RECEIPT = 'evidence/verification/cohort174-arm9-reference-packets-v2-20261105.json'
OUTPUTS = [ARM_RECEIPT, 'evidence/verification/cohort174-thumb-reference-inputs-20261105.json',
    'evidence/verification/cohort174-mixed-reference-inputs-20261105.json',
    'evidence/verification/cohort174-namespaced-overlay-reference-v1-20261106.json']
PLAN = 'evidence/verification/cohort-2026-10-29-174.json'
TRANSACTION = 'work/integration/cohort174-recovery-transaction.json'
CLAIM = 'work/integration/cohort174-reference-admission-v1-attempt.json'
ACCEPTED = 'evidence/verification/cohort-2026-10-29-173.json'
STABLE = [SPEC, MAIN, THUMB, 'recovery.json', 'source-preferences.json', ACCEPTED, *OUTPUTS]


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(path.read_bytes())


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def classify(main, outputs, candidate_plan, candidate_registered, marker, expected_new_main):
    reasons = []
    protected = [consumer for consumer in main['consumers'] if consumer.get('sourceOnlyCompilerInputQualification') == ARM_RECEIPT]
    arm = outputs.get(ARM_RECEIPT)
    if protected:
        actual = {proof['report'] for proof in arm.get('qualification', [])} if arm else set()
        missing = [consumer['report'] for consumer in protected if consumer['report'] not in actual]
        reasons.append('The fixed ARM receipt is referenced by registered main consumers; any legacy rerun can destroy their first-registration proof')
        if missing:
            reasons.append('The protected first-registration receipt is already incomplete: ' + ','.join(missing))
    if arm and arm.get('registered') is True and arm.get('qualification'):
        reasons.append('A successful nonempty ARM registration receipt exists, including a possible interruption before its ledger write')
    namespaced = outputs.get(OUTPUTS[-1])
    if namespaced and namespaced.get('passed') is True and namespaced.get('registered') is True:
        reasons.append('Namespaced admission already completed; resume subsequent acceptance rather than repeat preparation')
    if candidate_plan is not None:
        reasons.append('A cohort174 preparation/acceptance plan already exists and requires explicit continuation review')
    if candidate_registered:
        reasons.append('The live native registry already contains frozen174 packet reports')
    if marker:
        reasons.append('An immutable one-shot launch claim already exists; process death alone does not authorize retry')
    if expected_new_main != 0:
        reasons.append('The reviewed exact frozen174 residual set unexpectedly contains ARM main reference consumers')
    return dict(safeToStart=not reasons, blockedReasons=reasons, protectedMainConsumers=[item['report'] for item in protected],
        recoveryRequired=bool(reasons), expectedNewMainConsumers=expected_new_main,
        existingEmptyRegisteredReceiptIsNotRegistrationEvidence=bool(arm and arm.get('registered') and not arm.get('qualification')))


def inspect_state(owned_claim=None):
    contract = load_contract()
    spec = read(ROOT / SPEC)
    require(digest(ROOT / SPEC) == contract['specification']['sha256'], 'Frozen174 specification changed')
    require(spec['cohort'] == 174 and spec['previousAcceptedCohort'] == 173, 'Wrong cohort predecessor')
    current = read(ROOT / 'recovery.json')
    accepted = read(ROOT / ACCEPTED)
    require(accepted['linksPending'] is False and digest(ROOT / 'recovery.json') == accepted['sourceRegistrySha256'], 'Current native registry is not the accepted173 predecessor')
    require(digest(ROOT / 'source-preferences.json') == accepted['sourcePreferenceSha256'], 'Accepted173 source preferences changed')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    for name in ['recovery.json', MAIN, THUMB]:
        require(subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT) == (ROOT / name).read_bytes(), 'Live registry/ledger is not exact current HEAD: ' + name)
    main = read(ROOT / MAIN)
    require(main == contract['historicalMainLedger']['document'], 'The exact174 one-shot baseline is no longer the original26 main consumers; review recovery first')
    excluded = {consumer['report'] for consumer in contract['consumers']}
    known = {consumer['report'] for consumer in main['consumers']}
    expected = []
    for packet in spec['packets']:
        if packet['report'] in excluded:
            continue
        report = read(ROOT / packet['report'])
        if not report.get('matches'):
            continue
        pins = {pin['path'] for key in ['generatorSources', 'replayDependencies'] for pin in report.get(key, [])}
        if {'extract/arm9/arm9.bin', 'extract/arm9/itcm.bin', 'extract/arm9/dtcm.bin'} & pins and {row['mode'] for row in report['matches']} == {'arm'} and packet['report'] not in known:
            expected.append(packet['report'])
    outputs = {name: read(ROOT / name) for name in OUTPUTS if (ROOT / name).is_file()}
    marker = read(ROOT / CLAIM) if (ROOT / CLAIM).exists() else None
    if owned_claim:
        require(marker == owned_claim, 'The active one-shot claim changed')
        marker = None
    selected = {packet['report'] for packet in spec['packets']}
    registered = [batch['report'] for batch in current['batches'] if batch['report'] in selected]
    result = classify(main, outputs, read(ROOT / PLAN) if (ROOT / PLAN).exists() else None, registered, marker, len(expected))
    stable = {name: digest(ROOT / name) for name in STABLE}
    preserve = [*STABLE, PLAN, TRANSACTION, 'manifest.json', 'evidence/verification/cohort174-before-adoption-20261101.json']
    preserve += [path.relative_to(ROOT).as_posix() for path in (ROOT / 'logs/integration').glob('cohort174*') if path.is_file()]
    result.update(commit=revision, fullSpecificationPackets=len(spec['packets']), overlayPackets=14, residualPackets=len(spec['packets']) - 14,
        expectedMainReports=expected, mainConsumers=len(main['consumers']), stableFingerprints=stable,
        preserveBeforeAnyPreparation=[dict(path=name, sha256=digest(ROOT / name)) for name in sorted(set(preserve)) if (ROOT / name).is_file()],
        requiresCoordinatorExclusiveLaunch=True, noRegistrationOrPreparationPerformed=True)
    return result


def claim_once(state):
    require(state['safeToStart'], '; '.join(state['blockedReasons']))
    require(state['stableFingerprints'] == {name: digest(ROOT / name) for name in STABLE}, 'Existing registration evidence changed before launch')
    token = uuid.uuid4().hex
    directory = ROOT / 'work/integration/cohort174-one-shot-preservation' / token
    directory.mkdir(parents=True, exist_ok=False)
    for pin in state['preserveBeforeAnyPreparation']:
        raw = (ROOT / pin['path']).read_bytes()
        require(hashlib.sha256(raw).hexdigest() == pin['sha256'], 'Evidence changed before its immutable preservation')
        target = directory / 'prior' / pin['path']
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(raw)
    claim = dict(schemaVersion=1, attemptId=token, processId=os.getpid(), immutableOneShotClaim=True,
        state=state, preservedDirectory=directory.relative_to(ROOT).as_posix())
    path = ROOT / CLAIM
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(claim, stream, indent=2)
    require(state['stableFingerprints'] == {name: digest(ROOT / name) for name in STABLE}, 'Protected state changed after atomic claim')
    return claim


def recheck_before_post_seal(claim):
    state = inspect_state(owned_claim=claim)
    require(state['safeToStart'], '; '.join(state['blockedReasons']))
    require(claim['state']['stableFingerprints'] == state['stableFingerprints'], 'Protected ledger/receipt/predecessor state changed before postSeal')
    return state


if __name__ == '__main__':
    print(json.dumps(inspect_state(), indent=2))
