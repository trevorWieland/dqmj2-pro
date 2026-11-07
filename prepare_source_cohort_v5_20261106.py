import subprocess
import sys
from pathlib import Path
from unittest.mock import patch


HERE = Path(__file__).resolve().parent
ROOT = HERE if (HERE / 'project.py').is_file() else Path(__file__).resolve().parents[3]
sys.dont_write_bytecode = True
sys.path[:0] = [str(HERE), str(ROOT)]
from project import sha256, write_json
import prepare_source_cohort_v3_20261102 as base
import prepare_source_cohort_v4_20261102 as original_v4
from host_arm9_overlay_reference_policy_v1_20261106 import load_contract, committed_file, verify_committed_promotion
import cohort174_reference_one_shot_v1_20261106 as guard


SPEC = guard.SPEC
OLD = 'qualify_mixed_arm9_reference_context_v5_20261106.py'
NEW = 'qualify_mixed_overlay_reference_v1_20261106.py'
EXPECTED_COMMAND = (sys.executable, str(ROOT / OLD), SPEC, '--register')
ORIGINALS = {'prepare_source_cohort_v3_20261102.py': '95e777b73e8bcfcc73ce6a446713934d3e370ea041df8c60b9090515cd8a1aef',
    'prepare_source_cohort_v4_20261102.py': 'c28c740f0dae8176dc85fc93422b2dda806e765380f19c43f7d72c2235630054'}


class ExactPostSealProxy:
    def __init__(self, original, before):
        self.original = original
        self.before = before
        self.invocations = 0

    def __getattr__(self, name):
        return getattr(self.original, name)

    def run(self, command, *args, **kwargs):
        words = tuple(command) if isinstance(command, (list, tuple)) else ()
        if words != EXPECTED_COMMAND:
            if len(words) > 2 and words[1] == str(ROOT / OLD) and SPEC in words:
                raise ValueError('Frozen174 mixed-v5 postSeal command shape changed')
            return self.original.run(command, *args, **kwargs)
        if self.invocations:
            raise ValueError('The exact174 registration command was already dispatched once')
        if Path(kwargs.get('cwd', '')).resolve() != ROOT or kwargs.get('check') is not True:
            raise ValueError('Original postSeal working directory/check contract changed')
        self.before()
        self.invocations += 1
        replacement = [words[0], str(ROOT / NEW), *words[2:]]
        return self.original.run(replacement, *args, **kwargs)


def main():
    guard.require(HERE == ROOT, 'This work-only proposal must be reviewed/promoted/committed before any preparation execution')
    guard.require(sys.argv[1:] == [SPEC], 'Only the exact frozen174 specification argument is accepted')
    contract = load_contract()
    verify_committed_promotion(contract)
    for name, digest in ORIGINALS.items():
        guard.require(sha256(ROOT / name) == digest, 'Original v3 preparation/v4 classification changed: ' + name)
    for name in [Path(__file__).name, 'cohort174_reference_one_shot_v1_20261106.py',
            'prepare_source_cohort_v3_20261102.py', 'prepare_source_cohort_v4_20261102.py']:
        committed_file(name)
    spec = guard.read(ROOT / SPEC)
    guard.require(spec['postSealCommands'] == [[OLD, SPEC, '--register']], 'Frozen full specification postSeal list differs')
    state = guard.inspect_state()
    claim = guard.claim_once(state)
    preserved = ROOT / claim['preservedDirectory']
    proxy = ExactPostSealProxy(base.subprocess, lambda: guard.recheck_before_post_seal(claim))
    outcome = dict(attemptId=claim['attemptId'], sourceCredit=0, originalClassificationAndPreparationDelegated=True,
        originalSpecificationSha256=sha256(ROOT / SPEC), onlySubstitution=[OLD, NEW], globalAcceptanceGatesUnchanged=True)
    try:
        with patch.object(base, 'classify_additions', original_v4.classify), patch.object(base, 'subprocess', proxy):
            base.main()
        guard.require(proxy.invocations == 1, 'Original preparation did not dispatch exactly one frozen174 postSeal command')
    except BaseException as error:
        outcome.update(passed=False, failureType=type(error).__name__, exactPostSealInvocations=proxy.invocations,
            retryRequiresExplicitPreservedEvidenceRecovery=True)
        write_json(preserved / 'outcome-failed.json', outcome)
        raise
    outcome.update(passed=True, exactPostSealInvocations=1, preparationCompletedOnly=True,
        nativeAcceptanceOrCommitPerformed=False, nextAction='Continue original cohort174 global acceptance gates; do not reprepare')
    write_json(preserved / 'outcome-prepared.json', outcome)


if __name__ == '__main__':
    main()
