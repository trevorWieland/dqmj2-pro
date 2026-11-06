import concurrent.futures
from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256, now, configuration
from ledger_state import collect_matches
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

REPORT = ROOT / 'evidence/attempts/main-large-profile-breadth21-20261101.json'
WORK = ROOT / 'work/main-large-profile-breadth21-20261101'


def worker(spec):
    record, compiler_path, speed = spec
    source = ROOT / record['source']
    assert sha256(source) == record['sourceSha256']
    tag = compiler.COMPILER_PINS[compiler_path][:12] + ('-speed' if speed else '-size')
    directory = WORK / (record['mode'] + '-' + record['address'][2:]) / tag
    result = dict(identity=record, compiler=compiler_path, speed=speed, compiled=False,
        genuinelyLinked=False, exact=False, sourceCredit=0)
    try:
        compiler.WORK = directory / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off', speed=speed,
            thumb=record['mode'] == 'thumb', compiler=ROOT / compiler_path)
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
            native = (ROOT / 'extract/arm9/arm9.bin').read_bytes()
            offset = int(record['address'], 0) - 0x02000000
            target = native[offset:offset + record['bytes']]
            body = binary.read_bytes()
            result.update(linkedSha256=sha256(binary), linkedBytes=len(body),
                fullByteMismatch=sum(a != b for a, b in zip(body, target)) + abs(len(body) - len(target)))
    except Exception as error:
        result['error'] = repr(error)
    return result


def main():
    assert not REPORT.exists()
    selected, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    used, inputs = {}, []
    for path in sorted((ROOT / 'evidence/attempts').glob('main-*breadth*.json')):
        document = read_json(path)
        rows = [row for row in document.get('results', []) if row.get('compilable') and
            row.get('bytes', 0) >= 256 and row.get('draftSource')]
        if rows:
            inputs.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))
        for row in rows:
            key = row.get('mode', 'arm'), row['address']
            if ('main', key[0], int(key[1], 0)) in selected:
                continue
            used.setdefault(key, row)
    records, deferred = [], []
    for (mode, address), row in sorted(used.items(), key=lambda item: -item[1]['bytes']):
        source_input = ROOT / row['draftSource']
        text = source_input.read_text(encoding='utf-8')
        if len(text.splitlines()) > 500 or '/*' in text or '//' in text:
            deferred.append(dict(address=address, reason='source formatting review required'))
            continue
        source = ROOT / f'generated/recovery/20261101-large-profile-breadth21/{mode}-{int(address, 0):08x}.c'
        assert not source.exists()
        source.parent.mkdir(parents=True, exist_ok=True)
        source.write_text(text, encoding='utf-8')
        records.append(dict(processor='arm9', module='main', mode=mode, address=address,
            bytes=row['bytes'], source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source),
            originalSource=row['draftSource'], originalSourceSha256=sha256(source_input)))
    queue = [(record, compiler_path, speed) for record in records
        for compiler_path in compiler.COMPILER_PINS for speed in [False, True]]
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        sourceCredit=0, acceptedSourceChanged=False, state='running', compilerProcesses=3,
        compilerPins=compiler.COMPILER_PINS, inputs=inputs, queue=records, deferred=deferred,
        sourceUnits=len(records), initializedCandidateBytes=sum(row['bytes'] for row in records),
        compilerJobs=len(queue), results=[],
        limitations=['Generated C is an unqualified hypothesis',
            'Full linked bytes are compared including pools; no relocation or stack masks',
            'Even exact hypotheses require source/interface/boundary review and native controls',
            'No registry, accepted sources, module or ROM credit changes'])
    write_json(REPORT, report)
    print({key: report[key] for key in ['sourceUnits', 'initializedCandidateBytes', 'compilerJobs']}, flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(worker, spec) for spec in queue]
        for future in concurrent.futures.as_completed(futures):
            report['results'].append(future.result())
            report.update(completedJobs=len(report['results']),
                compiledJobs=sum(row['compiled'] for row in report['results']),
                genuineLinkedJobs=sum(row['genuinelyLinked'] for row in report['results']),
                exactHypotheses=sum(row['exact'] for row in report['results']))
            write_json(REPORT, report)
            if len(report['results']) % 32 == 0:
                print({key: report[key] for key in ['completedJobs', 'compiledJobs', 'genuineLinkedJobs', 'exactHypotheses']}, flush=True)
    report.update(state='finished', finishedUtc=now())
    write_json(REPORT, report)


if __name__ == '__main__':
    main()
