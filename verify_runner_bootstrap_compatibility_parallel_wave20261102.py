import ast
import copy
from pathlib import Path
import shutil
import subprocess
import time
from unittest.mock import patch
import run_checks
import verify_workspace
from project import ROOT, read_json, write_json, sha256


def main():
    validator = ROOT / 'validate_evidence.py'
    expected = '2c5687696d22c5693da783423a4d5d366ad309edf5100ff10c106e7da6c37d59'
    if sha256(validator) != expected:
        raise ValueError('Original negative validator identity differs')
    tree = ast.parse(validator.read_text(encoding='utf-8-sig'))
    body = next(node.body for node in tree.body if isinstance(node, ast.If))
    start = next(i for i, node in enumerate(body) if isinstance(node, ast.For) and isinstance(node.target, ast.Tuple))
    end = next(i for i, node in enumerate(body) if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Tuple)
        and isinstance(node.targets[0].elts[0], ast.Name) and node.targets[0].elts[0].id == 'accepted_matches')
    selected = ast.fix_missing_locations(ast.Module(body=body[start:end], type_ignores=[]))
    work = ROOT / 'work/runner-bootstrap-compatibility-parallel-wave20261102' / str(time.time_ns())
    work.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(ROOT / 'recovery.json', work / 'recovery.json')
    before = sha256(ROOT / 'recovery.json')
    tests = []
    environment = dict(ROOT=work, Path=Path, copy=copy, subprocess=subprocess, patch=patch,
        run_checks=run_checks, verify_workspace=verify_workspace, read_json=read_json, write_json=write_json, tests=tests)
    exec(compile(selected, str(validator), 'exec'), environment)
    required = ['Runner persists injected launch failure', 'Runner persists injected timeout failure',
        'Changed source registry rejects otherwise successful runner steps']
    if tests != required:
        raise ValueError('Original runner negative cases changed or were skipped')
    reports = {}
    for name in ['runner-failure-launch', 'runner-failure-timeout', 'runner-registry-mutation']:
        path = work / 'work' / name / 'evidence/verification/checks.json'
        report = read_json(path)
        if report['allChecksPassed'] or report['buildAndOracleChecksPassed']:
            raise ValueError('Injected failure retained accepted status')
        reports[name] = dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path),
            steps=len(report['steps']), runtimeInputBootstrap=report['runtimeInputBootstrap'],
            sourceHashesCurrent=report['sourceHashesCurrent'])
    result = dict(passed=True, originalValidatorSha256=expected, originalValidatorUnchanged=sha256(validator) == expected,
        exactOriginalNegativeCaseStatementsExecuted=True, originalNegativeCases=tests, reports=reports,
        authoritativeSourceRoot=str(ROOT), fixtureOutputRoot=str(work), runChecksSha256=sha256(ROOT / 'run_checks.py'),
        sourceRegistryBefore=before, sourceRegistryAfter=sha256(ROOT / 'recovery.json'), sourceCredit=0,
        acceptedSourceCompilation=False, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/runner-bootstrap-compatibility.json', result)
    print(dict(passed=True, originalNegativeCases=len(tests), unchangedValidator=True))


if __name__ == '__main__':
    main()
