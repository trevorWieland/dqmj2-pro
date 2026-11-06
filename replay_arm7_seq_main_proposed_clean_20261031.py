import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import uuid

ROOT = Path(__file__).resolve().parent
FROZEN = {
    'match_arm7_seq_main_proposed_20261030.py': '0adc8fc70533f545e5ff6a2fb752afeb0db7948532e230305ffac02fd3b435bd',
    'validate_arm7_seq_main_proposed_20261030.py': 'f02631beca16e0970b6879e3300a1192152bc549e744830f2474a5ec07863fa2',
    'nonmatching/arm7-bulk/20261030/seq-main-final01/closure.json': '647fed0c1bf6ed7c93d7c2df1c2919285cdcb9775340bbaf97717b33502b5b16',
    'nonmatching/arm7-bulk/20261030/seq-main-final01/generator-pins.json': 'e1d036c7e8170fd3b1166f179d0f8627e4d22a3599bbd7aa88ad4becd27a3fc5',
    'evidence/attempts/arm7-seq-main-proposed-20261030.json': '91a25bd6ffa57feef5c043f97d8bd4c4f306642f43d54929fc947dfcb10b2069',
    'evidence/verification/arm7-seq-main-proposed-controls-20261030.json': '2f2d94ca51d18f5c6af8e19859f4bc017fe48e5761f438e10eea3c2eb4682884',
}
LEGACY_REPORT = ROOT / 'evidence/attempts/arm7-seq-main-proposed-20261030.json'
LEGACY_CONTROLS = ROOT / 'evidence/verification/arm7-seq-main-proposed-controls-20261030.json'
OUTPUT = ROOT / 'evidence/verification/arm7-seq-main-proposed-clean-replay-20261031.json'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_inputs():
    for name, expected in FROZEN.items():
        if sha(ROOT / name) != expected:
            raise ValueError('Frozen proposed input differs: ' + name)


def relative(path):
    return path.resolve().relative_to(ROOT).as_posix()


def new_work(name=None):
    scope = ROOT / 'work/arm7-bulk-20261030/seq-main-clean-replay-20261031'
    result = (ROOT / name).resolve() if name else scope / ('run-' + uuid.uuid4().hex)
    if result == scope or not result.is_relative_to(scope):
        raise ValueError('Replay directory must be a child of the dedicated work scope')
    if result.exists() and any(result.iterdir()):
        raise ValueError('Replay directory must start empty; cached products are forbidden')
    result.mkdir(parents=True, exist_ok=True)
    return result


def receipt(path):
    return {'path': relative(path), 'sha256': sha(path), 'bytes': path.stat().st_size}


def missing_object_control(validator, report, label):
    obj = ROOT / report['matches'][0]['object']
    saved = obj.read_bytes()
    obj.unlink()
    try:
        try:
            validator.validate(report)
        except ValueError as error:
            expected = 'Current track input/product changed or missing: ' + relative(obj)
            if str(error) != expected:
                raise ValueError('Missing-object control failed for a different reason') from error
            return {'name': label, 'rejected': True, 'exception': type(error).__name__, 'reason': str(error)}
        raise ValueError('Validator accepted a missing freshly generated object')
    finally:
        obj.write_bytes(saved)


def replay(name=None):
    frozen_inputs()
    import match_arm7_seq_main_proposed_20261030 as matcher
    import validate_arm7_seq_main_proposed_20261030 as validator
    from project import write_json
    directory = new_work(name)
    if matcher.ROOT != ROOT or validator.ROOT != ROOT or validator._FRESH:
        raise ValueError('Replay requires the local frozen modules and an initially empty validator cache')
    fresh_report = directory / 'proposed-report.json'
    fresh_controls = directory / 'proposed-controls.json'
    previous = matcher.WORK, validator.REPORT, matcher.write_json, validator.write_json
    writes = []
    controls = []
    stdout = io.StringIO()

    def route(expected, destination):
        def writer(requested, value):
            if Path(requested).resolve() != expected.resolve():
                raise ValueError('Unexpected frozen-generator output path')
            write_json(destination, value)
            writes.append({'requested': relative(expected), 'actual': relative(destination)})
        return writer

    try:
        matcher.WORK = directory / 'generated'
        validator.REPORT = fresh_report
        matcher.write_json = route(LEGACY_REPORT, fresh_report)
        validator.write_json = route(LEGACY_CONTROLS, fresh_controls)
        with contextlib.redirect_stdout(stdout):
            matcher.main()
        report = json.loads(fresh_report.read_text())
        for row in report['matches']:
            if not (ROOT / row['object']).resolve().is_relative_to(matcher.WORK):
                raise ValueError('Fresh object escaped the dedicated work directory')
            if not (ROOT / row['realArm7Link']['cwd']).resolve().is_relative_to(matcher.WORK):
                raise ValueError('Fresh link escaped the dedicated work directory')
        controls.append(missing_object_control(validator, report, 'missing-object-before-validator-cache'))
        with contextlib.redirect_stdout(stdout):
            validator.main()
        result = json.loads(fresh_controls.read_text())
        original_controls = json.loads(LEGACY_CONTROLS.read_text())['controls']
        if [row['name'] for row in result['controls']] != [row['name'] for row in original_controls]:
            raise ValueError('Frozen validator control identities changed')
        if not result['allPassed'] or not all(row['rejected'] for row in result['controls']):
            raise ValueError('A frozen negative control failed')
        controls.append(missing_object_control(validator, report, 'missing-object-after-validator-cache'))
        if len(validator.validate(report)) != 1:
            raise ValueError('Restored proposed validation did not return exactly one zero-credit unit')
        controls.append({'name': 'restored-fresh-positive', 'passed': True})
        try:
            new_work(relative(directory))
        except ValueError as error:
            if 'must start empty' not in str(error):
                raise
            controls.append({'name': 'populated-work-directory-rejected', 'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Replay accepted a populated work directory')
        if len(writes) != 2:
            raise ValueError('Expected exactly one producer report and one full-validator control report')
    finally:
        matcher.WORK, validator.REPORT, matcher.write_json, validator.write_json = previous
        frozen_inputs()
    log = directory / 'frozen-entrypoint-stdout.txt'
    log.write_text(stdout.getvalue(), encoding='utf-8')
    output = {
        'schemaVersion': 1,
        'generator': Path(__file__).name,
        'generatorSha256': sha(Path(__file__)),
        'actualInvocationCwd': str(Path.cwd().resolve()),
        'repository': str(ROOT),
        'dedicatedWorkDirectory': relative(directory),
        'initialWorkDirectoryEmpty': True,
        'copiedCachedProducts': False,
        'frozenInputFiles': [{'path': key, 'sha256': value} for key, value in FROZEN.items()],
        'entrypointOrder': [Path(matcher.__file__).name + ':main', Path(validator.__file__).name + ':main'],
        'runtimeOutputRouting': writes,
        'runtimeGlobalsChanged': ['matcher.WORK', 'validator.REPORT', 'matcher.write_json', 'validator.write_json'],
        'runtimeGlobalsRestored': True,
        'validationOrCompilerFunctionsReplaced': False,
        'legacyReportsAndSourcesUnchanged': True,
        'producerReport': receipt(fresh_report),
        'fullFrozenValidatorReport': receipt(fresh_controls),
        'legacyStdout': dict(receipt(log), authoritativeReceipt=False,
            reason='Frozen entrypoint print statements reference their historical output filenames; new routed report receipts are authoritative'),
        'actualOriginalAndCompiledReturnsPerFullProof': report['actualNativeAndCompiledReturns'],
        'actualSeparateNestedReturnsPerFullProof': report['actualSeparatelyObservedNestedReturns'],
        'frozenValidatorControls': len(result['controls']),
        'wrapperControls': controls,
        'sourceAcceptanceCredit': 0,
        'additionalFunctionOrByteCredit': 0,
        'boundaryMigrationApproved': False,
        'allPassed': True,
    }
    write_json(OUTPUT, output)
    print(json.dumps({'report': relative(OUTPUT), 'sha256': sha(OUTPUT), 'frozenControls': len(result['controls']),
        'wrapperControls': len(controls), 'allPassed': True}), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-directory')
    args = parser.parse_args()
    replay(args.work_directory)


if __name__ == '__main__':
    main()
