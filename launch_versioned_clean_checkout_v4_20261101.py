import argparse
import subprocess
import sys
import time
from pathlib import Path
from unittest.mock import patch
import validate_clean_checkout as clean
import materialize_readonly_references_20261101 as readonly
from project import ROOT, read_json, write_json, sha256, now


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--target', type=Path, required=True)
    parser.add_argument('--timeout', type=int, default=43200)
    options = parser.parse_args()
    name = f'evidence/verification/cohort{options.cohort}-expanded-source-closure-20261101.json'
    while True:
        path = ROOT / name
        committed = subprocess.run(['git', 'show', 'HEAD:' + name], cwd=ROOT, capture_output=True)
        if path.is_file() and committed.returncode == 0 and committed.stdout == path.read_bytes():
            break
        time.sleep(5)
    plan = read_json(ROOT / f'evidence/verification/cohort-2026-10-29-{options.cohort}.json')
    assert not plan['linksPending'] and read_json(path)['passed']
    assert sha256(ROOT / 'recovery.json') == plan['sourceRegistrySha256']
    assert not options.target.exists()
    revision = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    canonical = ROOT / 'evidence/verification/clean-checkout.json'
    canonical_hash = sha256(canonical)
    output = ROOT / f'evidence/verification/clean-cohort{options.cohort}-{options.target.name}-20261101.json'
    materialize = readonly.materialize
    original_run = clean.run
    preflight_steps = []

    def pinned_materialize(target):
        current = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
        assert current == revision
        result = materialize(target)
        assert result['sourceRevision'] == revision
        return result

    def publish(path, report):
        path = Path(path).resolve()
        if path == canonical.resolve():
            write_json(output, report)
        elif path.parent == canonical.parent.resolve() and path.name.startswith('clean-checkout-'):
            write_json(output.with_name(output.stem + '-historical.json'), report)
        else:
            raise ValueError('Unexpected clean-checkout publication namespace')

    def preflight_run(command, cwd, log, timeout):
        if len(command) > 1 and Path(command[1]).name == 'run_checks.py':
            commands = [['reproduce_effect_queue_short_paths_v3_20261101.py', '--canonical'], ['utility_runtime.py'], ['arm7_runtime.py'],
                ['reproduce_channel_parameters_closure_v2_20261101.py']]
            commands += [['reproduce_legacy_arm7_closures_20261101.py', '--family', family]
                for family in ['driver-leaves', 'timing', 'setting', 'initializer', 'alarm-selector']]
            for index, arguments in enumerate(commands):
                preflight_log = Path(log).with_name(f'path-portability-preflight-{index:02}.txt')
                step = original_run([sys.executable, str(options.target / arguments[0]), *arguments[1:]],
                    cwd, preflight_log, 1800)
                preflight_steps.append(step)
                result['pathPortabilityPreflight'] = preflight_steps
                write_json(receipt, result)
                if step['exitCode']:
                    raise ValueError('Fresh source/path portability preflight failed: ' + arguments[0])
        return original_run(command, cwd, log, timeout)

    receipt = ROOT / f'evidence/verification/clean-cohort{options.cohort}-{options.target.name}-launcher-20261101.json'
    result = dict(startedUtc=now(), cohort=options.cohort, sourceRevision=revision, target=str(options.target.resolve()),
        originalDriver='validate_clean_checkout.py', originalDriverSha256=sha256(clean.__file__),
        redirectedReport=output.relative_to(ROOT).as_posix(), canonicalReportSha256=canonical_hash,
        originalMaterializationAndChecksUnchanged=False, originalCheckCommandsUnchanged=True,
        materializer=readonly.__name__, materializerSha256=sha256(readonly.__file__),
        referenceManifest=readonly.REFERENCES.relative_to(ROOT).as_posix(), referenceManifestSha256=sha256(readonly.REFERENCES), supplementalFreshPathPreflight=True,
        launcher=Path(__file__).name, launcherSha256=sha256(__file__), sourceCredit=0, state='running')
    write_json(receipt, result)
    try:
        with patch.object(clean, 'materialize', pinned_materialize), patch.object(clean, 'write_json', publish), patch.object(clean, 'run', preflight_run):
            clean.main(options.target, options.timeout)
        report = read_json(output)
        assert report['snapshot']['sourceRevision'] == revision
        result.update(state='passed', freshBuildAndOracleChecksPassed=report['freshBuildAndOracleChecksPassed'],
                      allChecksPassed=report['allChecksPassed'])
    except Exception as error:
        result.update(state='failed', failure=f'{type(error).__name__}: {error}')
        raise
    finally:
        assert sha256(canonical) == canonical_hash
        result.update(finishedUtc=now(), canonicalReportUnchanged=True)
        write_json(receipt, result)


if __name__ == '__main__':
    main()
