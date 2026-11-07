import argparse
from contextlib import contextmanager
import importlib.util
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import verify_committed_source_inputs_context_v10_20261106 as previous
import qualify_arm9_overlay_reference_inputs_20261105 as overlay


LANE = ROOT / 'evidence/lanes/parallel-wave20261107/child-arm9-source-input-qualification'
PROPOSAL_SHA = 'a89878577de26c73c956612bf8c78049da74c5662a2348f6ce24524469a9852b'
CONTRACT_SHA = '0d143a1a2ddc9bd689ef740afd44ab88380041c4f1528d64ecbcde7e941ea7c3'


def promotion():
    path = LANE / 'proposal.json'
    if sha256(path) != PROPOSAL_SHA:
        raise ValueError('Child ARM9 qualification proposal changed')
    proposal = read_json(path)
    pins = {path.relative_to(ROOT).as_posix(): PROPOSAL_SHA}

    def walk(value):
        if isinstance(value, dict):
            if 'path' in value and 'sha256' in value:
                if pins.setdefault(value['path'], value['sha256']) != value['sha256']:
                    raise ValueError('Qualification promotion contains conflicting pins')
            for item in value.values():
                walk(item)
        elif isinstance(value, list):
            for item in value:
                walk(item)

    walk(proposal)
    pins[Path(__file__).name] = sha256(__file__)
    for name, expected in pins.items():
        path = ROOT / name
        if not path.resolve().is_relative_to(ROOT) or sha256(path) != expected:
            raise ValueError('Promoted child context input changed: ' + name)
        committed = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=ROOT)
        if committed != path.read_bytes():
            raise ValueError('Child qualification support must be committed before activation: ' + name)
    return proposal


def qualification_module():
    path = LANE / 'qualify.py'
    spec = importlib.util.spec_from_file_location('qualified_child_arm9_input_context', path)
    module = importlib.util.module_from_spec(spec)
    before = sys.path[:]
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = before
    if module.ROOT != ROOT or Path(module.derive.__code__.co_filename).resolve() != LANE / 'geometry.py':
        raise ValueError('Child context imported a foreign geometry/runtime root')
    return module


@contextmanager
def validation_route():
    proposal = promotion()
    qualification = qualification_module()
    contract = qualification.load_contract(CONTRACT_SHA)
    live = qualification.qualify(CONTRACT_SHA)
    prior = overlay.project_batches
    proof = dict(liveSourceOnlyQualification=live.proof, comparisonProjectionInvocations=[])

    def projected(actual, report, declared):
        copies, removed = qualification.comparison_projection(actual, CONTRACT_SHA, live)
        result = prior(copies, report, declared)
        proof['comparisonProjectionInvocations'].append(removed)
        return result

    try:
        with patch.object(overlay, 'project_batches', projected):
            yield proof
    finally:
        qualification.verify_pins(contract)
        actual = live.proof
        if sha256(ROOT / actual['freshObject']) != actual['freshObjectSha256']:
            raise ValueError('Live child compilation changed during committed audit')
        if overlay.project_batches is not prior or promotion() != proposal:
            raise ValueError('Child context did not restore its exact inherited callback/promotion')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True, choices=[174])
    options = parser.parse_args()
    target = ROOT / f'evidence/verification/cohort{options.cohort}-child-arm9-reference-context-20261107.json'
    if target.exists():
        raise ValueError('Preserve the previous child context report before repeating this audit')
    plan_path = ROOT / f'evidence/verification/cohort-2026-10-29-{options.cohort}.json'
    plan = read_json(plan_path)
    names = ['recovery.json', 'source-preferences.json', plan['specification'], plan_path.relative_to(ROOT).as_posix()]
    before = {name: sha256(ROOT / name) for name in names}
    if plan['linksPending'] or plan['sourceMatchedFunctions'] != 11640 or plan['sourceLinkedBytes'] != 1262114:
        raise ValueError('The frozen finalized cohort174 membership changed')
    with validation_route() as proof:
        previous.main()
    if before != {name: sha256(ROOT / name) for name in names}:
        raise ValueError('Canonical registry/preferences/finalized cohort changed during audit')
    contract = read_json(LANE / 'contract.json')
    if proof['comparisonProjectionInvocations'] != [contract['derivedEvidence']]:
        raise ValueError('The exact two-file child evidence projection did not run exactly once')
    write_json(target, dict(passed=True, sourceCredit=0, allOriginalContextV10AuditsCompleted=True,
        canonicalSourceRegistryUnchanged=True, frozenCohortMembershipUnchanged=True,
        canonicalInputs=before, qualifiedChildARM9Reference=proof,
        childQualificationAdoptedByCoordinator=True, originalCanonicalSourceHashesUnmodified=True,
        originalRegistryMainNamespaceAndARM7AssertionsUnmodified=True,
        inheritedProjectorDelegatedAfterOriginalRegistryGuard=True,
        contract=dict(path=(LANE / 'contract.json').relative_to(ROOT).as_posix(), sha256=CONTRACT_SHA),
        proposal=dict(path=(LANE / 'proposal.json').relative_to(ROOT).as_posix(), sha256=PROPOSAL_SHA),
        generator=Path(__file__).name, generatorSha256=sha256(__file__)))


if __name__ == '__main__':
    main()
