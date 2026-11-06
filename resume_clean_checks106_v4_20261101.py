import argparse
import subprocess
import sys
from pathlib import Path
from project import ROOT, now, read_json, sha256, write_json
from resume_clean_checks106_current_products_20261101 import commands_from_frozen_main
import run_checks as original


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-root', required=True)
    options = parser.parse_args()
    assert Path(options.expected_root).resolve() == ROOT.resolve()
    original_path = ROOT / 'evidence/verification/checks.json'
    previous_path = ROOT / 'evidence/verification/clean106-resumed-v3-20261101.json'
    previous = read_json(previous_path)
    assert previous['state'] == 'failed' and previous['failureAtIndex'] == 985
    assert previous['originalFailedReportSha256'] == sha256(original_path)
    assert [row['index'] for row in previous['steps']] == [983, 984, 985]
    assert all(row['exitCode'] == 0 for row in previous['steps'][:-1])
    assert previous['steps'][-1]['exitCode'] != 0
    commands = commands_from_frozen_main()
    assert commands[985] == ['verify_interpreted_byte_modes_sources.py']
    interpreted = {tuple(batch['reproduce']) for batch in read_json(ROOT / 'interpreted-recovery.json')['batches']}
    remaining = list(range(985, len(commands)))
    producers = [index for index in remaining if tuple(commands[index]) in interpreted]
    schedule = producers + [index for index in remaining if index not in producers]
    assert sorted(schedule) == remaining and len(set(schedule)) == len(schedule)
    prerequisite = ROOT / 'evidence/verification/clean106-interpreted-command-order-20261101.json'
    write_json(prerequisite, dict(sourceCredit=0, originalProducerIndices=producers,
        executionOrder=schedule, originalCommandCount=len(commands),
        commandsReproducedExactlyOnce=True, originalCommandsUnchanged=True,
        cause='Frozen oracle order places interpreted negative verifiers before their source producers',
        world17VerifierIndex=983, world17ProducerIndex=commands.index(['match_scr_world17_20261030_batch11.py']),
        scope='Dependency reordering only; no assertion, source, validator, timeout or byte comparison changed'))
    retained = previous['preservedCommandLogs'] + previous['steps']
    for row in retained:
        assert sha256(ROOT / row['log']) == row['logSha256']
        if 'command' in row:
            assert row['command'][1:] == [str(ROOT / commands[row['index']][0]), *commands[row['index']][1:]]
    original_hash = sha256(original_path)
    previous_hash = sha256(previous_path)
    initial_hashes = previous['sourceAndRegistryHashes']
    assert all(sha256(ROOT / name) == digest for name, digest in initial_hashes.items())
    report_path = ROOT / 'evidence/verification/clean106-resumed-v4-20261101.json'
    assert not report_path.exists()
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        state='running', previousResume=previous_path.relative_to(ROOT).as_posix(), previousResumeSha256=previous_hash,
        originalFailedReportSha256=original_hash, prerequisiteSha256=sha256(prerequisite),
        preservedCommandLogs=retained, resumedFromIndex=985, totalPlannedCommands=len(commands), steps=[],
        sourceAndRegistryHashes=initial_hashes, sourceCredit=0, sourceReconstructionComplete=False,
        limitations=['Continuation of the original materialized source106 checkout with explicit fresh-product prerequisites',
            'Original failed reports and all previous successful/failing logs remain unchanged',
            'Completion here is not an uninterrupted clean replay or a source-only ROM'])
    directory = ROOT / 'logs/clean106-resumed-v4-20261101'
    directory.mkdir(parents=True, exist_ok=True)
    write_json(report_path, report)
    for index in schedule:
        command = commands[index]
        argv = [sys.executable, str(ROOT / command[0]), *command[1:]]
        log = directory / f'{index:04}-{Path(command[0]).stem}.txt'
        assert not log.exists()
        timeout = original.validation_timeout(command)
        report['currentCommand'] = dict(index=index, command=argv)
        write_json(report_path, report)
        try:
            result = subprocess.run(argv, cwd=ROOT.parent, capture_output=True, text=True, errors='replace', timeout=timeout)
            output, status = result.stdout + result.stderr, result.returncode
        except (OSError, ValueError, subprocess.TimeoutExpired) as error:
            output, status = f'{type(error).__name__}: {error}', -1
        log.write_text(output, encoding='utf-8')
        report['steps'].append(dict(index=index, command=argv, exitCode=status,
            log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log), deadlineSeconds=timeout))
        print(dict(index=index, script=command[0], exitCode=status), flush=True)
        if status:
            report.update(state='failed', failureAtIndex=index, completedUtc=now())
            write_json(report_path, report)
            raise ValueError('Remaining original command failed: ' + command[0])
        write_json(report_path, report)
    assert sorted(row['index'] for row in report['steps']) == remaining
    from recovery_registry import verify_sources
    verify_sources()
    assert all(sha256(ROOT / name) == digest for name, digest in initial_hashes.items())
    assert sha256(original_path) == original_hash and sha256(previous_path) == previous_hash
    assert all(sha256(ROOT / row['log']) == row['logSha256'] for row in retained)
    matching = [path for path in (ROOT / 'build').rglob('*.nds') if path.stat().st_size == 175959612
        and sha256(path) == '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6']
    assert matching
    report.update(state='passed', completedUtc=now(), allRemainingOriginalCommandsPassed=True,
        sourceAndRegistryHashesUnchanged=True, originalLogsAndFailureReportsUnchanged=True,
        exactScaffoldingRoms=[dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path), bytes=path.stat().st_size) for path in matching],
        wholeSourceRom=False, fullWindowsGame=False)
    write_json(report_path, report)


if __name__ == '__main__':
    main()
