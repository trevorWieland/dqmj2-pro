import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time


ROOT = Path(__file__).resolve().parent
SUFFIX = 'channel67-parallel-wave20261102'
MATCH = 'evidence/matches/arm7-channel-parameters-20261030-67.json'
CONTROL = 'evidence/verification/arm7-channel-parameters-controls-20261030-67.json'
WRAPPER = 'reproduce_channel_parameters_closure_v2_20261101.py'
VALIDATOR = 'validate_arm7_channel_parameters_20261030_67.py'
PROFILE = 'nonmatching/arm7-bulk/20261030/channel-parameters-final67/'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--instance', default='cold')
    options = parser.parse_args()
    if not options.instance.isalnum():
        raise ValueError('Instance must contain only letters and digits')
    sandbox = ROOT / 'work' / SUFFIX / options.instance
    sandbox.mkdir(parents=True, exist_ok=False)
    logs = ROOT / 'logs' / SUFFIX / options.instance
    logs.mkdir(parents=True, exist_ok=False)
    receipt_path = ROOT / 'evidence/verification' / SUFFIX / (options.instance + '.json')
    before = {name: digest(ROOT / name) for name in [MATCH, CONTROL, 'recovery.json', 'manifest.json', 'source-map.json', VALIDATOR]}
    pins = read(ROOT / (PROFILE + 'generator-pins.json'))['files']
    names = {row['path'] for row in pins}
    names.update([PROFILE + 'generator-pins.json', WRAPPER, VALIDATOR,
        'match_arm7_channel_parameters_20261030_67.py', 'seal_recovery_evidence_20261031.py',
        'project.json', MATCH, CONTROL, 'inputs/game.nds', 'inputs/save.sav',
        'extract/arm7/arm7.bin', 'evidence/arm7/ghidra-runtime-inventory.json',
        'deps/references/pokediamond-b623abef/arm7/lib/src/SND_exChannel.c',
        'deps/references/pokediamond-b623abef/arm7/lib/include/SND_util.h',
        'tools/mwccarm/mwccarm/license.dat'])
    names.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'extract/arm7/runtime').glob('*.bin'))
    names.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'deps/native/ndspy').rglob('*') if path.is_file() and '__pycache__' not in path.parts)
    tools = ROOT / 'tools/mwccarm/mwccarm/2.0/base'
    names.update(path.relative_to(ROOT).as_posix() for path in tools.iterdir() if path.suffix.lower() in ['.exe', '.dll'])
    copied = []
    for name in sorted(names):
        source = (ROOT / name).resolve()
        if not source.is_relative_to(ROOT):
            raise ValueError('Copy escaped the project')
        target = sandbox / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        copied.append(dict(path=name, sha256=digest(target), bytes=target.stat().st_size))
    for row in pins:
        if digest(sandbox / row['path']) != row['sha256']:
            raise ValueError('Frozen input changed: ' + row['path'])
    historical = ROOT.parent / 'j2p-clean-20261031-z' / MATCH
    old = read(historical)
    required = {row['path'] for row in read(sandbox / MATCH)['generatorSources']}
    extra = sorted({row['path'] for row in old['generatorSources']} - required)
    if extra != ['seal_recovery_evidence_20261031.py']:
        raise ValueError('Historical first-failure diagnosis changed')
    historical_copy = sandbox / 'historical-z-report.json'
    shutil.copyfile(historical, historical_copy)
    diagnosis = "import json; import validate_arm7_channel_parameters_20261030_67 as v; r=json.load(open('historical-z-report.json'));\ntry: v.validate(r)\nexcept ValueError as e:\n assert str(e)=='Complete channel-parameter generator closure differs'; print(str(e))\nelse: raise AssertionError('Historical incompatible seal accepted')"
    commands = [[sys.executable, '-c', diagnosis], [sys.executable, str(sandbox / WRAPPER)],
        [sys.executable, str(sandbox / VALIDATOR)]]
    receipt = dict(generator=Path(__file__).name, generatorSha256=digest(Path(__file__)),
        sandbox=sandbox.relative_to(ROOT).as_posix(), copiedInputs=copied, sourceCredit=0,
        historicalReportSha256=digest(historical_copy), historicalUnexpectedClosureEntries=extra,
        copiedObjectsOrWorkProducts=False, copiedExtractedOriginalModuleInputs=True,
        fullCleanCheckoutProven=False, sharedCanonicalFilesBefore=before, steps=[])
    write(receipt_path, receipt)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    for index, command in enumerate(commands):
        started = time.monotonic()
        log = logs / (str(index) + '.txt')
        with log.open('w', encoding='utf-8') as stream:
            result = subprocess.run(command, cwd=sandbox, stdout=stream, stderr=subprocess.STDOUT,
                env=env, timeout=600)
        receipt['steps'].append(dict(command=command, exitCode=result.returncode,
            seconds=round(time.monotonic() - started, 3), log=log.relative_to(ROOT).as_posix(), logSha256=digest(log)))
        write(receipt_path, receipt)
        print(dict(step=index, exitCode=result.returncode, seconds=receipt['steps'][-1]['seconds']), flush=True)
        if result.returncode:
            raise SystemExit(result.returncode)
    controls = read(sandbox / CONTROL)
    normalized = read(sandbox / MATCH)
    receipt.update(passed=controls['allPassed'], positiveUnits=controls['positiveUnits'],
        matchedInitializedBytes=controls['matchedInitializedBytes'],
        actualOriginalAndCompiledReturns=controls['actualOriginalAndCompiledReturns'],
        negativeControls=len(controls['controls']),
        originalGeneratorClosureEntries=len(normalized['generatorSources']),
        supplementalReplaySources=normalized['supplementalReplaySources'],
        reportSha256=digest(sandbox / MATCH), controlsSha256=digest(sandbox / CONTROL),
        sharedCanonicalFilesAfter={name: digest(ROOT / name) for name in before})
    receipt['sharedCanonicalFilesUnchanged'] = receipt['sharedCanonicalFilesAfter'] == before
    receipt['sourceAndChannelReportsUnchanged'] = all(receipt['sharedCanonicalFilesAfter'][name] == before[name] for name in [MATCH, CONTROL, VALIDATOR])
    if not receipt['sourceAndChannelReportsUnchanged']:
        raise ValueError('Channel source or shared reports changed during isolated proof')
    write(receipt_path, receipt)
    print(dict(passed=receipt['passed'], controls=receipt['negativeControls'], receipt=str(receipt_path)), flush=True)


if __name__ == '__main__':
    main()
