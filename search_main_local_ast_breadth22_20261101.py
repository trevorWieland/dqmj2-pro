import concurrent.futures
import os
from pathlib import Path
import random
import re
import subprocess
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256, now
from permuter_local_ast_v2_20261101 import mutate, COMMIT
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

WORK = ROOT / 'work/main-local-ast-breadth22-20261101'
OUTPUT = ROOT / 'evidence/attempts/main-local-ast-breadth22-20261101.json'


def worker(spec):
    original, seed = spec
    record = original['identity']
    directory = WORK / (record['mode'] + '-' + record['address'][2:]) / str(seed)
    directory.mkdir(parents=True, exist_ok=True)
    result = dict(address=record['address'], bytes=record['bytes'], seed=seed,
        compiled=False, genuinelyLinked=False, exact=False, sourceCredit=0)
    try:
        source_input = ROOT / record['source']
        assert sha256(source_input) == record['sourceSha256']
        executable = ROOT / original['compiler']
        assert sha256(executable) == compiler.COMPILER_PINS[original['compiler']]
        preprocessed = directory / 'preprocessed.i'
        command = [str(executable), '-E', str(source_input), '-o', str(preprocessed)]
        env = dict(os.environ, LM_LICENSE_FILE=str(ROOT / 'tools/mwccarm/mwccarm/license.dat'))
        process = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=30)
        (directory / 'preprocess-stdout.txt').write_bytes(process.stdout)
        (directory / 'preprocess-stderr.txt').write_bytes(process.stderr)
        assert process.returncode == 0
        text = '\n'.join(line for line in preprocessed.read_text(encoding='utf-8').splitlines() if not line.lstrip().startswith('#'))
        function = 'native_main_' + f'{int(record["address"], 0):08x}'
        text = mutate(text, function, seed, steps=1 + seed % 3)
        source = ROOT / f'generated/recovery/20261101-local-ast-breadth22/{function}/{seed}.c'
        assert not source.exists()
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text, encoding='utf-8')
        result.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            preprocessingCommand=command, preprocessedSha256=sha256(preprocessed))
        compiler.WORK = directory / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off', speed=original['speed'],
            thumb=record['mode'] == 'thumb', compiler=executable)
        assert len(rows) == 1
        row = rows[0]
        result['compilation'] = row
        if row.get('compileFailed'):
            return result
        result['compiled'] = True
        try:
            proof = validate(row, qualified_bindings(row), directory / 'link')
            result['exact'] = True
        except ValueError as error:
            assert isinstance(error.args[0], dict)
            proof = error.args[0]
        result['genuineLinkComparison'] = proof
        binary = directory / 'link/caller.bin'
        result['genuinelyLinked'] = binary.is_file()
        if binary.is_file():
            image = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
            offset = int(record['address'], 0) - 0x02000000
            native, body = image[offset:offset + record['bytes']], binary.read_bytes()
            result.update(linkedSha256=sha256(binary),
                fullByteMismatch=sum(a != b for a, b in zip(native, body)) + abs(len(native) - len(body)))
    except Exception as error:
        result['error'] = repr(error)
    return result


def main():
    assert not OUTPUT.exists()
    input_path = ROOT / 'evidence/attempts/main-large-profile-breadth21-20261101.json'
    chosen = {}
    for row in read_json(input_path)['results']:
        key = row['identity']['address']
        if key in ['0x202fb98', '0x20095e8'] or 'fullByteMismatch' not in row:
            continue
        if key not in chosen or row['fullByteMismatch'] < chosen[key]['fullByteMismatch']:
            chosen[key] = row
    rows = sorted(chosen.values(), key=lambda row: row['fullByteMismatch'] / row['identity']['bytes'])[:12]
    rng = random.Random(0x2026110122)
    queue = [(row, rng.getrandbits(31)) for row in rows for unused in range(16)]
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        sourceCredit=0, toolCommit=COMMIT, localAstApiOnly=True, compilerProcesses=3,
        inputReport=input_path.relative_to(ROOT).as_posix(), inputReportSha256=sha256(input_path),
        units=len(rows), candidateBytes=sum(row['identity']['bytes'] for row in rows), jobs=len(queue),
        queue=[dict(address=row['identity']['address'], seed=seed) for row,seed in queue],
        results=[], state='running', sourceAcceptanceRequiresIndependentReviewAndNativeProof=True)
    write_json(OUTPUT, report)
    print(dict(units=report['units'], candidateBytes=report['candidateBytes'], jobs=len(queue)), flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(worker, spec) for spec in queue]
        for future in concurrent.futures.as_completed(futures):
            report['results'].append(future.result())
            write_json(OUTPUT, report)
            if len(report['results']) % 32 == 0:
                print(dict(completed=len(report['results']), exact=sum(row['exact'] for row in report['results'])), flush=True)
    report.update(state='finished', finishedUtc=now(), compiled=sum(row['compiled'] for row in report['results']),
        genuinelyLinked=sum(row['genuinelyLinked'] for row in report['results']), exact=sum(row['exact'] for row in report['results']))
    write_json(OUTPUT, report)


if __name__ == '__main__':
    main()
