import argparse
import ast
import copy
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from project import ROOT, now, read_json, sha256, write_json
import run_checks as original


def commands_from_frozen_main():
    tree = ast.parse(Path(original.__file__).read_text(encoding='utf-8-sig'))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'main')
    prefix = []
    for node in function.body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name)
                and target.value.id == 'report' and isinstance(target.slice, ast.Constant)
                and target.slice.value == 'entrypointPreflight' for target in node.targets):
            break
        prefix.append(node)
    else:
        raise ValueError('Frozen command construction boundary not found')
    function = copy.deepcopy(function)
    function.name = 'command_plan_only'
    function.body = prefix + [ast.Return(value=ast.Name(id='commands', ctx=ast.Load()))]
    namespace = dict(vars(original))
    exec(compile(ast.fix_missing_locations(ast.Module(body=[function], type_ignores=[])), '<frozen-command-plan>', 'exec'), namespace)
    def ignore_planning_write(path, document):
        assert Path(path) == ROOT / 'evidence/verification/recovery-order.json'
    with patch.object(sys, 'argv', [original.__file__, '--clean', '--tools']):
        namespace['write_json'] = ignore_planning_write
        return namespace['command_plan_only']()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-root', required=True)
    parser.add_argument('--failed-report-sha', required=True)
    options = parser.parse_args()
    assert Path(options.expected_root).resolve() == ROOT.resolve()
    previous_path = ROOT / 'evidence/verification/checks.json'
    assert sha256(previous_path) == options.failed_report_sha
    previous = read_json(previous_path)
    assert not previous['allChecksPassed'] and len(previous['steps']) == 909
    assert all(step['exitCode'] == 0 for step in previous['steps'][:-1])
    assert previous['steps'][-1]['exitCode'] != 0
    prerequisite = ROOT / 'evidence/verification/card-control452-current-products-20261101.json'
    repair = read_json(prerequisite)
    assert repair['fullOriginalControls'] == 44 and repair['actualWrongSourceReturns'] == repair['independentRejections'] == 4
    assert repair['originalPathGuardsUnchanged'] and repair['sourceCredit'] == 0
    commands = commands_from_frozen_main()
    assert original.replay_entrypoints(commands)['passed']
    retained = []
    for index, step in enumerate(previous['steps']):
        assert step['command'][1:] == [str(ROOT / commands[index][0]), *commands[index][1:]]
        path = ROOT / step['log']
        retained.append(dict(index=index, exitCode=step['exitCode'], log=step['log'], logSha256=sha256(path)))
    assert commands[908] == ['prove_arm7_card_control452_negative_returns_20261031.py']
    initial_hashes = {name: sha256(ROOT / name) for name in ['recovery.json', 'interpreted-recovery.json', 'source-preferences.json', 'run_checks.py']}
    report_path = ROOT / 'evidence/verification/clean106-resumed-current-products-20261101.json'
    assert not report_path.exists()
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        state='running', originalFailedReportSha256=options.failed_report_sha,
        originalRunChecksSha256=sha256(original.__file__), prerequisiteSha256=sha256(prerequisite),
        retainedOriginalSteps=retained, totalPlannedCommands=len(commands), resumedFromIndex=908,
        sourceAndRegistryHashes=initial_hashes, steps=[], sourceReconstructionComplete=False,
        limitations=['Resumes the original fresh checkout after a new explicit prerequisite; this is not an uninterrupted replay',
            'Prior successful command logs and the original failed report remain unchanged',
            'The frozen command-building prefix is evaluated with its evidence write diverted and its execution loop excluded'])
    write_json(report_path, report)
    directory = ROOT / 'logs/clean106-resumed-current-products-20261101'
    directory.mkdir(parents=True, exist_ok=True)
    for index in range(908, len(commands)):
        command = commands[index]
        argv = [sys.executable, str(ROOT / command[0]), *command[1:]]
        log = directory / f'{index:04}-{Path(command[0]).stem}.txt'
        assert not log.exists()
        timeout = original.validation_timeout(command)
        report['currentCommand'] = dict(index=index, command=argv)
        write_json(report_path, report)
        try:
            result = subprocess.run(argv, cwd=ROOT.parent, capture_output=True, text=True, errors='replace', timeout=timeout)
            output, exit_code = result.stdout + result.stderr, result.returncode
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            output, exit_code = f'{type(error).__name__}: {error}', -1
        log.write_text(output, encoding='utf-8')
        row = dict(index=index, command=argv, exitCode=exit_code, deadlineSeconds=timeout,
            log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log))
        report['steps'].append(row)
        print(dict(index=index, script=command[0], exitCode=exit_code), flush=True)
        if exit_code:
            report.update(state='failed', failureAtIndex=index, completedUtc=now())
            write_json(report_path, report)
            raise ValueError('Original remaining command failed: ' + command[0])
        write_json(report_path, report)
    from recovery_registry import verify_sources
    verify_sources()
    assert all(sha256(ROOT / name) == digest for name, digest in initial_hashes.items())
    assert sha256(previous_path) == options.failed_report_sha
    assert all(sha256(ROOT / row['log']) == row['logSha256'] for row in retained)
    rom = ROOT / 'build/exact-source.nds'
    candidates = list((ROOT / 'build').rglob('*.nds'))
    matching = [path for path in candidates if path.stat().st_size == 175959612 and sha256(path) == '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6']
    assert matching
    report.update(state='passed', completedUtc=now(), allRemainingOriginalCommandsPassed=True,
        sourceAndRegistryHashesUnchanged=True, originalLogsAndFailureReportUnchanged=True,
        exactScaffoldingRoms=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), bytes=path.stat().st_size) for path in matching],
        wholeSourceRom=False, fullWindowsGame=False)
    write_json(report_path, report)


if __name__ == '__main__':
    main()
