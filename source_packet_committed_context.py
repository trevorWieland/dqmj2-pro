import argparse
import copy
import hashlib
import json
import subprocess
import sys
import uuid
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, sha256, write_json
from source_selection import preferences
import qualify_arm9_overlay_reference_inputs_20261105 as overlay
import verify_committed_source_inputs_context_v9_20261106 as previous
from host_arm9_overlay_reference_policy_v1_20261106 import (
    CONTRACT, load_contract, verify_committed_promotion, ensure_scope)
from host_arm9_overlay_reference_v1_20261106 import qualify, _comparison_projection
import qualify_ten_consumers_v2 as current_references
import qualify_child_snd_reference_v1_20261107 as child_references
import registered_input_path_context_v1_20261107 as registered_paths


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def blob(name, revision='HEAD', current=False):
    raw = subprocess.check_output(['git', 'show', revision + ':' + name], cwd=ROOT)
    if current and raw != (ROOT / name).read_bytes():
        raise ValueError('Current committed context input differs: ' + name)
    return raw


def extend_contract(contract, frozen_raw, predecessor_raw, current_raw, plan):
    pins = [row for row in contract['scopePins'] if row['path'] == 'source-preferences.json']
    if len(pins) != 1 or pins[0].get('policy') or digest(frozen_raw) != pins[0]['sha256']:
        raise ValueError('Original immutable preference contract differs')
    frozen, predecessor, current = map(json.loads, (frozen_raw, predecessor_raw, current_raw))
    metadata = lambda value: {key: item for key, item in value.items() if key != 'preferences'}
    if metadata(frozen) != metadata(predecessor) or metadata(frozen) != metadata(current):
        raise ValueError('Preference namespace/schema metadata changed')
    old, prior, rows = frozen['preferences'], predecessor['preferences'], current['preferences']
    if len(prior) < len(old) or prior[:len(old)] != old:
        raise ValueError('Frozen preference prefix changed in predecessor')
    if len(rows) < len(prior) or rows[:len(prior)] != prior:
        raise ValueError('A prior preference was removed, reordered or changed')
    identities = [(row.get('program') or '', row['processor'], row['module'], row['mode'],
                   int(row['address'], 0)) for row in rows]
    if len(set(identities)) != len(rows):
        raise ValueError('Duplicate current preference identity')
    added = rows[len(prior):]
    if (len(added) != plan['duplicateMigrationFunctions']
            or len(set(plan['migrationReports'])) != len(plan['migrationReports'])
            or {row['evidence'] for row in added} != set(plan['migrationReports'])
            or digest(current_raw) != plan['sourcePreferenceSha256']):
        raise ValueError('Current preference append differs from finalized migrations')
    result = copy.deepcopy(contract)
    pin = next(row for row in result['scopePins'] if row['path'] == 'source-preferences.json')
    pin['sha256'] = digest(current_raw)
    restored = copy.deepcopy(result)
    next(row for row in restored['scopePins'] if row['path'] == 'source-preferences.json')['sha256'] = pins[0]['sha256']
    if restored != contract:
        raise ValueError('Preference extension changed another original contract field')
    return result, dict(frozenPreferences=len(old), predecessorPreferences=len(prior),
                       currentPreferences=len(rows), appendedMigrations=len(added),
                       frozenPreferenceSha256=digest(frozen_raw),
                       currentPreferenceSha256=digest(current_raw),
                       onlyOneExactPreferenceHashExtended=True, originalContractFileUnchanged=True,
                       allOriginalPreferenceRecordsPreserved=True, sourceCredit=0)


@contextmanager
def validation_route(cohort):
    if cohort < 175:
        raise ValueError('Historical cohorts retain their original context')
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    contract = load_contract()
    verify_committed_promotion(contract)
    plan = json.loads(blob(f'evidence/verification/cohort-2026-10-29-{cohort}.json', current=True))
    driver = json.loads(blob(f'evidence/verification/cohort{cohort}-validation-driver.json', current=True))
    if (plan['linksPending'] or plan['moduleComparisonsExact'] != 20
            or driver['state'] != 'build-and-regression-checks-passed' or len(driver['steps']) != 16
            or digest(blob('recovery.json', current=True)) != plan['sourceRegistrySha256']):
        raise ValueError('Current committed cohort lacks its original acceptance gates')
    predecessor = plan['previousAcceptedCohort']
    prior_closure = json.loads(blob(f'evidence/verification/cohort{predecessor}-expanded-source-closure-20261101.json'))
    frozen_closure = json.loads(blob('evidence/verification/cohort174-expanded-source-closure-20261101.json'))
    current_raw = blob('source-preferences.json', current=True)
    adjusted, append = extend_contract(contract,
        blob('source-preferences.json', frozen_closure['sourceCommit']),
        blob('source-preferences.json', prior_closure['sourceCommit']), current_raw, plan)
    validated = preferences(plan['exactRom']['sha256'])
    if len(validated) != append['currentPreferences']:
        raise ValueError('Original migration audit did not validate every current preference')
    linked = read_json(ROOT / 'evidence/verification/linked-source-preferences-20261030.json')
    if (linked['passed'] is not True or not linked['actualLinkedSourceProvenanceChecked']
            or linked['sourcePreferenceSha256'] != digest(current_raw)
            or linked['sourceMapSha256'] != sha256(ROOT / 'source-map.json')
            or linked['sourceUnitsSha256'] != sha256(ROOT / 'build/link-work/source-units.json')
            or len(linked['preferredInputs']) != len(validated)):
        raise ValueError('Current preferences lack complete unchanged actual-link provenance')
    directory = ROOT / 'work/integration/source-packet-overlay-context' / uuid.uuid4().hex[:12]
    proof = qualify(adjusted, directory, committed=True)
    append.update(cohort=cohort, commit=revision, originalMigrationAuditsValidated=len(validated),
                  linkedPreferenceReceiptSha256=sha256(ROOT / 'evidence/verification/linked-source-preferences-20261030.json'),
                  predecessorSourceCommit=prior_closure['sourceCommit'],
                  frozen174SourceCommit=frozen_closure['sourceCommit'])
    proof['preferenceAppendExtension'] = append
    original = overlay.project_batches
    projections = []
    def projected(actual, report, declared):
        ensure_scope(proof['liveScope'])
        copies, removed = _comparison_projection(actual, adjusted)
        projections.append(copy.deepcopy(removed))
        return original(copies, report, declared)
    try:
        with patch.object(overlay, 'project_batches', projected):
            for name in ['qualify_ten_consumers_v2.py', 'ten-consumer-contract-v2.json',
                         'evidence/verification/cohort175-main-consumer-inventory-v2-20261107.json']:
                blob(name, current=True)
            current_contract = current_references.load_contract()
            with current_references.route(current_contract, directory / 'current-main') as current:
                proof['currentMainReferenceQualification'] = current
                for name in ['qualify_child_snd_reference_v1_20261107.py',
                             'child-snd-reference-contract-v1.json', 'test_child_reference.py']:
                    blob(name, current=True)
                child_contract = read_json(child_references.CONTRACT)
                with child_references.route(child_contract, directory / 'child-snd') as child:
                    proof['childArm9ReferenceQualification'] = child
                    for name in ['registered_input_path_context_v1_20261107.py',
                                 registered_paths.CONTRACT, 'test_registered_input_path_context.py']:
                        blob(name, current=True)
                    registered_contract = read_json(ROOT / registered_paths.CONTRACT)
                    with registered_paths.validation_route(ROOT, registered_contract) as registered:
                        proof['registeredInputPathQualification'] = registered
                        yield proof
                        registered['observedAccounting'] = registered_paths.validate_accounting(
                            read_json(ROOT / f'evidence/verification/cohort{cohort}-committed-source-inputs-v14-20261105.json'),
                            registered_contract)
    finally:
        ensure_scope(proof['liveScope'])
        proof['comparisonProjectionInvocations'] = len(projections)
        proof['projectedOriginalComparisonRoles'] = projections
        proof['originalRegistryGateAndPriorProjectorsPreserved'] = True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    args = parser.parse_args()
    with validation_route(args.cohort) as proof:
        previous.main()
    revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
    write_json(ROOT / f'evidence/verification/cohort{args.cohort}-overlay-reference-context-v11-20261107.json',
        dict(passed=True, commit=revision, sourceCredit=0,
             allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted=True,
             namespaceQualifiedOverlayReference=proof, originalOverlayMembershipUnchanged=True,
             originalMainNamespaceAssertionsAndOriginal26ConsumersPreserved=True,
             contract=dict(path=CONTRACT, sha256=sha256(ROOT / CONTRACT)),
             generator=Path(__file__).name, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
