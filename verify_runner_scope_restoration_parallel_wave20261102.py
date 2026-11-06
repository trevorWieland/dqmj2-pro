import contextlib
import difflib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from unittest.mock import patch
import recovery_registry
import verify_workspace
from project import ROOT, read_json, sha256, write_json
from runner_scope_fixture_parallel_wave20261102 import BASE_COMMIT, BASE_SHA256, build


def main():
    work = ROOT / 'work/runner-scope-restoration-parallel-wave20261102' / str(time.time_ns())
    work.mkdir(parents=True)
    previous = build(work)
    candidate = build(work, observed_scope_guard=True)
    tests = []
    before = sha256(ROOT / 'run_checks.py')
    original_verify = recovery_registry.verify_sources
    for label, path in [('without-observed-scope-guard', previous), ('with-observed-scope-guard', candidate)]:
        spec = importlib.util.spec_from_file_location('scope_restoration_' + label.replace('-', '_') + work.name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        fixture = work / label
        fixture.mkdir()
        registry = fixture / 'recovery.json'
        shutil.copyfile(ROOT / 'recovery.json', registry)
        original_bytes = registry.read_bytes()
        original_hash = sha256(registry)
        calls = []
        verification_calls = []
        changed_hash = []
        observed_mutation_hashes = []

        def command(argv, **options):
            calls.append(argv)
            if Path(argv[1]).name == 'verify_workspace.py':
                data = read_json(registry)
                data['injectedScopeChange'] = True
                write_json(registry, data)
                changed_hash.append(sha256(registry))
                assert changed_hash[-1] != original_hash
            return subprocess.CompletedProcess(argv, 0, stdout='', stderr='')

        def verify():
            verification_calls.append(True)
            original_verify()

        def observed_hash(path):
            if Path(path) == registry and changed_hash:
                if observed_mutation_hashes:
                    assert sha256(registry) == changed_hash[-1]
                    registry.write_bytes(original_bytes)
                    assert sha256(registry) == original_hash
                observed_mutation_hashes.append(sha256(registry))
            return sha256(path)

        log = fixture / 'runner.txt'
        started = time.perf_counter()
        with log.open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream), \
                patch.object(module, 'ROOT', fixture), patch.object(sys, 'argv', ['run_checks.py']), \
                patch.object(module.subprocess, 'run', side_effect=command), \
                patch.object(module, 'sha256', side_effect=observed_hash), \
                patch.object(recovery_registry, 'verify_sources', side_effect=verify), \
                patch.object(verify_workspace, 'index_evidence'):
            status = module.main()
        result = read_json(fixture / 'evidence/verification/checks.json')
        assert len(verification_calls) == 2 and len(calls) > 1000 and len(changed_hash) == 1
        assert observed_mutation_hashes == [changed_hash[0], original_hash]
        assert result['scopeChangedDuringReplay'] == ['recovery.json']
        assert status == 1 and not result['allChecksPassed'] and result['sourceHashesCurrent']
        assert result['recoveryRegistryUnchanged'] and sha256(registry) == original_hash
        assert result['buildAndOracleChecksPassed'] == (label == 'without-observed-scope-guard')
        tests.append(dict(name=label, passed=True, commands=len(calls), seconds=time.perf_counter()-started,
            registryBeforeSha256=original_hash, mutatedSha256=changed_hash[0], restoredSha256=sha256(registry),
            actualSourcePreAndPostChecks=len(verification_calls), checks=str((fixture / 'evidence/verification/checks.json').relative_to(ROOT)),
            checksSha256=sha256(fixture / 'evidence/verification/checks.json'),
            allChecksPassed=result['allChecksPassed'], buildAndOracleChecksPassed=result['buildAndOracleChecksPassed']))
    assert sha256(ROOT / 'run_checks.py') == before
    patch_text = ''.join(difflib.unified_diff((ROOT / 'run_checks.py').read_text(encoding='utf-8-sig').splitlines(keepends=True),
        candidate.read_text(encoding='utf-8').splitlines(keepends=True), fromfile='a/run_checks.py', tofile='b/run_checks.py'))
    patch_path = work / 'proposed-run_checks.patch'
    patch_path.write_text(patch_text, encoding='utf-8')
    report = dict(passed=True, baseRunnerCommit=BASE_COMMIT, baseRunnerSha256=BASE_SHA256,
        liveRunnerSha256=before, liveRunnerUnchanged=True, sourceCredit=0,
        generatorSha256=sha256(Path(__file__)), fixtureBuilderSha256=sha256(ROOT / 'runner_scope_fixture_parallel_wave20261102.py'),
        prototype=str(candidate.relative_to(ROOT)), prototypeSha256=sha256(candidate),
        proposedPatch=str(patch_path.relative_to(ROOT)), proposedPatchSha256=sha256(patch_path),
        tests=tests, hashBypass=False, sourceChecksBypassed=False, realSourceCompilation=False,
        completeOriginalFourteenCaseValidatorRun=False)
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/runner-scope-restoration-reproducible.json', report)
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
