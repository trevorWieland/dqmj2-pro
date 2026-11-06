import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import time
from unittest.mock import patch
import bootstrap_runtime_inputs_parallel_wave20261102 as bootstrap
from project import ROOT, sha256, write_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cold-root', type=Path)
    args = parser.parse_args()
    work = ROOT / 'work/runtime-bootstrap-parallel-wave20261102' / str(time.time_ns())
    work.mkdir(parents=True, exist_ok=True)
    names = [*bootstrap.RUNTIME_INPUTS, *bootstrap.PARENTS]
    names.extend(row[0] for row in bootstrap.PARENTS.values())
    pins = {name: sha256(ROOT / name) for name in names}
    registry = dict(batches=[dict(sourceHashes=pins)])
    controls = []

    def fixture(name, omit_runtime=False):
        folder = work / name
        folder.mkdir(parents=True, exist_ok=False)
        for relative in names:
            if omit_runtime and relative in bootstrap.RUNTIME_INPUTS:
                continue
            destination = folder / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, destination)
        write_json(folder / 'recovery.json', registry)
        return folder

    def reject(name, folder):
        with patch.object(bootstrap.subprocess, 'run', side_effect=AssertionError('Invalid native input invoked a generator')):
            try:
                bootstrap.materialize(folder)
            except ValueError as error:
                controls.append(dict(name=name, rejected=True, reason=str(error), generatorInvoked=False))
            else:
                raise AssertionError('Invalid runtime bootstrap accepted: ' + name)

    warm = fixture('warm')
    with patch.object(bootstrap.subprocess, 'run', side_effect=AssertionError('Warm bootstrap invoked a generator')):
        result = bootstrap.materialize(warm)
    assert result['passed'] and not result['steps'] and not result['missingBefore']
    controls.append(dict(name='verified-warm-inputs-no-generation', passed=True))
    for name, target in [('tampered-runtime', next(iter(bootstrap.RUNTIME_INPUTS))),
                         ('tampered-generator', 'arm7_runtime.py'),
                         ('tampered-physical-input', bootstrap.PARENTS['arm7_runtime.py'][0])]:
        folder = fixture(name, omit_runtime=name != 'tampered-runtime')
        (folder / target).write_bytes(b'tampered')
        reject(name, folder)
    folder = fixture('missing-physical-input', omit_runtime=True)
    (folder / bootstrap.PARENTS['arm7_runtime.py'][0]).unlink()
    reject('missing-physical-input', folder)
    folder = fixture('wrong-accepted-runtime-pin', omit_runtime=True)
    wrong = copy.deepcopy(registry)
    wrong['batches'][0]['sourceHashes'][next(iter(bootstrap.RUNTIME_INPUTS))] = '0' * 64
    write_json(folder / 'recovery.json', wrong)
    reject('wrong-accepted-runtime-pin', folder)
    import run_checks
    import recovery_registry
    published = []
    with patch.object(sys, 'argv', ['run_checks.py']), patch.object(bootstrap, 'materialize', return_value=dict(passed=True)), \
            patch.object(recovery_registry, 'verify_sources', side_effect=ValueError('fixture accepted source changed')), \
            patch.object(run_checks, 'write_json', side_effect=lambda path, value: published.append((path, copy.deepcopy(value)))):
        try:
            run_checks.main()
        except ValueError as error:
            assert str(error) == 'fixture accepted source changed'
        else:
            raise AssertionError('Changed accepted source passed replay preflight')
    assert len(published) == 1 and published[0][0] == ROOT / 'evidence/verification/checks.json'
    early = published[0][1]
    assert not early['allChecksPassed'] and not early['buildAndOracleChecksPassed'] and not early['steps']
    assert early['state'] == 'failed-source-input-preflight' and 'fixture accepted source changed' in early['failure']
    controls.append(dict(name='early-source-failure-publishes-current-failed-checks', passed=True,
        noAcceptedSourceCompilation=True, publishedState=early['state']))
    cold = None
    if args.cold_root:
        target = args.cold_root.resolve()
        if target == ROOT or not target.is_relative_to(ROOT.parent) or target.is_relative_to(ROOT):
            raise ValueError('Cold diagnostic requires a separate disposable sibling checkout')
        prior_logs = {str(path.relative_to(target)): sha256(path) for path in (target / 'logs/clean-checkout').glob('*.txt')}
        missing = [name for name in bootstrap.RUNTIME_INPUTS if not (target / name).exists()]
        if set(missing) != set(bootstrap.RUNTIME_INPUTS):
            raise ValueError('Cold diagnostic requires every measured runtime input to be absent')
        helper = target / Path(bootstrap.__file__).name
        if helper.exists():
            raise ValueError('Refusing to replace an existing cold diagnostic helper')
        shutil.copyfile(bootstrap.__file__, helper)
        log = ROOT / 'logs/parallel-wave20261102/bootstrap-cold-diagnostic.txt'
        log.parent.mkdir(parents=True, exist_ok=True)
        code = "import json; from pathlib import Path; import bootstrap_runtime_inputs_parallel_wave20261102 as b; r=b.materialize(Path.cwd()); from recovery_registry import verify_sources; verify_sources(); print(json.dumps(dict(bootstrap=r, completeAcceptedSourceHashGatePassed=True, sourceCompilation=False)))"
        with log.open('w', encoding='utf-8') as stream:
            run = subprocess.run([sys.executable, '-c', code], cwd=target,
                stdout=stream, stderr=subprocess.STDOUT, timeout=900)
        cold = dict(root=str(target), helper=helper.name, helperSha256=sha256(helper), missingBefore=missing,
            exitCode=run.returncode, log=log.relative_to(ROOT).as_posix(), logSha256=sha256(log),
            originalLogsPreserved=all(sha256(target / name) == digest for name, digest in prior_logs.items()),
            diagnosticOnly=True, originalImmutableFullReplayStillFailed=True, fullCleanReplayProven=False)
        if run.returncode == 0:
            cold['proof'] = json.loads(log.read_text(encoding='utf-8'))
    report = dict(passed=all(c.get('rejected') or c.get('passed') for c in controls) and (cold is None or cold['exitCode'] == 0),
        controls=controls, coldDiagnostic=cold, sourceCredit=0, generatorSha256=sha256(__file__),
        helperSha256=sha256(bootstrap.__file__), runChecksSha256=sha256(ROOT / 'run_checks.py'))
    destination = ROOT / 'evidence/verification/parallel-wave20261102' / ('runtime-bootstrap-controls.json' if cold else 'runtime-bootstrap-controls-only.json')
    write_json(destination, report)
    print(dict(passed=report['passed'], controls=len(controls), coldDiagnosticExitCode=cold['exitCode'] if cold else None))
    if not report['passed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
