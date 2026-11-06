import subprocess
import sys
from contextlib import ExitStack
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from project import ROOT, now, read_json, sha256, write_json
import recovery_order
import recovery_registry
import run_checks
import verify_workspace


def runner_probe(inject_timeout):
    fixture = (ROOT / 'work/runner-deadline-controls' / str(inject_timeout)).resolve()
    assert fixture.is_relative_to((ROOT / 'work').resolve())
    fixture.mkdir(parents=True, exist_ok=True)
    write_json(fixture / 'recovery.json', {'schemaVersion': 1, 'batches': [], 'oracles': []})
    commands = ['match_scr_context_words_20261030_batch13.py',
                'match_scr_byte_modes_20261030_batch14.py',
                'match_scr_world32_20261030_batch09.py', 'reproduce.py']
    batches = [{'reproduce': [name]} for name in commands]
    captured = []

    def invoke(argv, **options):
        name = Path(argv[1]).name
        captured.append({'command': name, 'seconds': options['timeout']})
        if inject_timeout and name == commands[0]:
            raise subprocess.TimeoutExpired(argv, options['timeout'])
        return SimpleNamespace(returncode=0, stdout='', stderr='')

    with ExitStack() as stack:
        stack.enter_context(patch.object(run_checks, 'ROOT', fixture))
        stack.enter_context(patch.object(run_checks.sys, 'argv', ['run_checks.py', '--clean']))
        stack.enter_context(patch.object(run_checks.subprocess, 'run', side_effect=invoke))
        stack.enter_context(patch.object(recovery_registry, 'batches', return_value=batches))
        stack.enter_context(patch.object(recovery_registry, 'oracles', return_value=[]))
        stack.enter_context(patch.object(recovery_registry, 'verify_sources'))
        stack.enter_context(patch.object(recovery_order, 'order_batches', return_value={'batches': batches}))
        stack.enter_context(patch.object(verify_workspace, 'index_evidence'))
        status = run_checks.main()
    report = read_json(fixture / 'evidence/verification/checks.json')
    assert len(captured) == len(report['steps'])
    assert all(row['seconds'] == step['deadlineSeconds'] for row, step in zip(captured, report['steps']))
    if inject_timeout:
        assert status == 1 and not report['allChecksPassed'] and not report['buildAndOracleChecksPassed']
        assert captured[-1]['command'] == commands[0] and report['steps'][-1]['exitCode'] == -1
        assert 'TimeoutExpired' in report['steps'][-1]['failure']
    else:
        assert status == 0
        limits = {row['command']: row['seconds'] for row in captured}
        assert all(600 < limits[name] <= 1800 for name in [*commands[:-1], 'validate_evidence.py'])
        assert limits['reproduce.py'] == 600 and limits['integrate.py'] == 960
    return {'injectedTimeout': inject_timeout, 'subprocessDeadlinesRecorded': True,
            'timeoutStopsLaterCommands': inject_timeout, 'calls': captured,
            'realBuildCredit': 0, 'passed': True}


def main():
    controls = [runner_probe(False), runner_probe(True)]
    normal = subprocess.run([sys.executable, '-c', 'print("complete")'],
                            capture_output=True, text=True, timeout=5, check=True)
    assert normal.stdout.strip() == 'complete'
    controls.append({'normalChildActuallyReturned': True})
    try:
        subprocess.run([sys.executable, '-u', '-c',
                        'import time; print("deadline-control-ready", flush=True); time.sleep(5)'],
                       capture_output=True, timeout=0.5, check=True)
    except subprocess.TimeoutExpired as error:
        assert b'deadline-control-ready' in error.stdout
        controls.append({'startedHangingChildTerminatedByDeadline': True})
    else:
        raise AssertionError('Deadline failed to reject a nonreturning child')
    logs = ['cohort48-context-words-root.txt', 'cohort49-byte-modes-root.txt',
            'cohort50-world32-source-closure-root.txt', 'cohort49-validation-13.txt',
            'cold-o-world32-isolated-deadline-diagnostic-20261030.txt']
    observations = []
    for name in logs:
        path = ROOT / 'logs/integration' / name
        if path.is_file():
            stat = path.stat()
            born = getattr(stat, 'st_birthtime', None)
            observations.append({'path': path.relative_to(ROOT).as_posix(), 'sha256': sha256(path),
                                 'shellLogElapsedSeconds': stat.st_mtime - born if born else None,
                                 'scope': 'Local shell log creation to final write; not a calibrated benchmark'})
    report = {'createdUtc': now(), 'passed': True, 'controls': controls,
              'generator': 'verify_runner_deadlines.py', 'generatorSha256': sha256(ROOT / 'verify_runner_deadlines.py'),
              'runnerSha256': sha256(ROOT / 'run_checks.py'), 'localObservations': observations,
              'nativeInstructionAndTimeoutChecksChanged': False, 'newSourceCredit': 0,
              'futureFullCleanRunStillRequired': True}
    write_json(ROOT / 'evidence/verification/runner-deadlines-20261030.json', report)
    print({'passed': True, 'controls': len(controls), 'newSourceCredit': 0})


if __name__ == '__main__':
    main()
