from contextlib import ExitStack
from types import SimpleNamespace
from unittest.mock import patch
from project import ROOT, read_json, write_json
import recovery_order
import recovery_registry
import run_checks
import verify_workspace


def main():
    results = []
    original = (ROOT / 'source-preferences.json').read_bytes()
    for mutation in ('append-whitespace', 'remove-policy'):
        fixture = (ROOT / 'work/source-preference-runner' / mutation).resolve()
        if not fixture.is_relative_to((ROOT / 'work').resolve()):
            raise ValueError('Runner test escaped generated work directory')
        fixture.mkdir(parents=True, exist_ok=True)
        policy = fixture / 'source-preferences.json'
        policy.write_bytes(original)
        write_json(fixture / 'recovery.json', {'schemaVersion': 1, 'batches': [], 'oracles': []})
        calls = 0

        def mutate(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 1:
                if mutation == 'append-whitespace':
                    policy.write_bytes(original + b'\n')
                else:
                    policy.unlink()
            return SimpleNamespace(returncode=0, stdout='', stderr='')

        with ExitStack() as stack:
            stack.enter_context(patch.object(run_checks, 'ROOT', fixture))
            stack.enter_context(patch.object(run_checks.sys, 'argv', ['run_checks.py']))
            stack.enter_context(patch.object(run_checks.subprocess, 'run', side_effect=mutate))
            stack.enter_context(patch.object(recovery_registry, 'batches', return_value=[]))
            stack.enter_context(patch.object(recovery_registry, 'oracles', return_value=[]))
            stack.enter_context(patch.object(recovery_registry, 'verify_sources'))
            stack.enter_context(patch.object(recovery_order, 'order_batches', return_value={'batches': []}))
            stack.enter_context(patch.object(verify_workspace, 'index_evidence'))
            code = run_checks.main()
        report = read_json(fixture / 'evidence/verification/checks.json')
        assert code == 1 and report['sourcePreferencesUnchanged'] is False
        assert report['allChecksPassed'] is False and report['buildAndOracleChecksPassed'] is False
        assert all(step['exitCode'] == 0 for step in report['steps'])
        results.append({'mutation': mutation, 'allMockCommandsReturnedZero': True,
                        'policyMutationRejected': True, 'fakeBuildSuccessAccepted': False})
    result = {'passed': True, 'controls': results, 'evidenceClass': 'source-policy-runner-negative-controls',
              'realBuildOrExecutionCredit': 0, 'newSourceByteCredit': 0}
    write_json(ROOT / 'evidence/verification/source-preference-runner-negatives-20261030.json', result)
    print(result)


if __name__ == '__main__':
    main()
