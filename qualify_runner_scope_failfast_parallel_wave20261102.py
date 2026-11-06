import ast
import contextlib
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from unittest.mock import patch
import verify_workspace
from project import ROOT, read_json, write_json, sha256
from runner_scope_fixture_parallel_wave20261102 import BASE_COMMIT, BASE_SHA256, build


def main():
    work = ROOT / 'work/runner-scope-failfast-parallel-wave20261102' / str(time.time_ns())
    work.mkdir(parents=True)
    source = ROOT / 'run_checks.py'
    before = sha256(source)
    candidate = build(work, observed_scope_guard=True)
    spec = importlib.util.spec_from_file_location('scope_prototype_' + work.name, candidate)
    prototype = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = prototype
    spec.loader.exec_module(prototype)
    original = ROOT / 'validate_evidence.py'
    original_hash = '2c5687696d22c5693da783423a4d5d366ad309edf5100ff10c106e7da6c37d59'
    if sha256(original) != original_hash:
        raise ValueError('Frozen original validator differs')
    body = next(node.body for node in ast.parse(original.read_text(encoding='utf-8-sig')).body if isinstance(node, ast.If))
    start = next(i for i, node in enumerate(body) if isinstance(node, ast.For) and isinstance(node.target, ast.Tuple))
    end = next(i for i, node in enumerate(body) if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple)
        and isinstance(node.targets[0].elts[0], ast.Name) and node.targets[0].elts[0].id == 'accepted_matches')
    code = compile(ast.fix_missing_locations(ast.Module(body=body[start:end], type_ignores=[])), str(original), 'exec')
    fixtures = work / 'fixtures'
    fixtures.mkdir()
    shutil.copyfile(ROOT / 'recovery.json', fixtures / 'recovery.json')
    tests = []
    environment = dict(ROOT=fixtures, Path=Path, copy=copy, subprocess=subprocess, patch=patch,
        run_checks=prototype, verify_workspace=verify_workspace, read_json=read_json, write_json=write_json, tests=tests)
    log = work / 'original-contracts.txt'
    started = time.perf_counter()
    with log.open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
        exec(code, environment)
    negative_seconds = time.perf_counter() - started
    if len(tests) != 3:
        raise ValueError('Original runner contract count differs')
    mutation = read_json(fixtures / 'work/runner-registry-mutation/evidence/verification/checks.json')
    if len(mutation['steps']) != 1 or mutation.get('scopeChangedDuringReplay') != ['recovery.json']:
        raise ValueError('Changed scope did not terminate after its first successful command')
    extras = []
    for label, changed in [('preference-mutation', 'source-preferences.json'),
                           ('interpreted-mutation', 'interpreted-recovery.json'),
                           ('removed-registry', 'recovery.json'), ('unchanged-scope', None)]:
        fixture = work / label
        fixture.mkdir()
        shutil.copyfile(ROOT / 'recovery.json', fixture / 'recovery.json')
        calls = []

        def command(argv, **options):
            calls.append(argv)
            if changed == 'recovery.json':
                (fixture / changed).unlink(missing_ok=True)
            elif changed:
                write_json(fixture / changed, dict(batches=[], preferences=[], injectedScopeChange=True))
            return subprocess.CompletedProcess(argv, 0, stdout='', stderr='')

        started = time.perf_counter()
        with log.open('a', encoding='utf-8') as stream, contextlib.redirect_stdout(stream), \
                patch.object(prototype, 'ROOT', fixture), patch.object(sys, 'argv', ['run_checks.py']), \
                patch.object(prototype.subprocess, 'run', side_effect=command), patch.object(verify_workspace, 'index_evidence'):
            status = prototype.main()
        result = read_json(fixture / 'evidence/verification/checks.json')
        seconds = time.perf_counter() - started
        if changed:
            assert status == 1 and len(calls) == 1 and not result['allChecksPassed'] and not result['buildAndOracleChecksPassed']
            assert result['scopeChangedDuringReplay'] == [changed]
        else:
            assert status == 0 and len(calls) > 1000 and result['allChecksPassed'] and result['buildAndOracleChecksPassed']
        extras.append(dict(name=label, passed=True, status=status, commands=len(calls), seconds=seconds,
            allChecksPassed=result['allChecksPassed'], sourceHashesCurrent=result['sourceHashesCurrent']))
    assert sha256(source) == before and sha256(original) == original_hash
    report = dict(passed=True, scope='Deterministically regenerated adopted runner; no live runner or frozen validator changed',
        baseRunnerCommit=BASE_COMMIT, baseRunnerSha256=BASE_SHA256, liveRunnerSha256=before,
        generatorSha256=sha256(Path(__file__)), fixtureBuilderSha256=sha256(ROOT / 'runner_scope_fixture_parallel_wave20261102.py'),
        prototype=str(candidate.relative_to(ROOT)), prototypeSha256=sha256(candidate),
        originalValidatorSha256=original_hash, exactOriginalNegativeCases=tests, originalContractsSeconds=negative_seconds,
        mutationCommandsWithoutEarlyTermination=extras[-1]['commands'], mutationCommandsAfter=1, additionalContracts=extras,
        log=str(log.relative_to(ROOT)), logSha256=sha256(log), sourceCredit=0, realSourceCompilation=False,
        completeOriginalFourteenCaseValidatorRun=False, liveRunnerUnchanged=True)
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/runner-scope-failfast-reproducible.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
