import concurrent.futures
from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256, now
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

INPUT = ROOT / 'evidence/attempts/root-breadth-source-archive-v2-20261101.json'
OUTPUT = ROOT / 'evidence/attempts/root-breadth-sp1p6-survey-20261101.json'
WORK = ROOT / 'work/root-breadth-sp1p6-20261101'
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe'


def worker(record):
    source = ROOT / record['source']
    assert sha256(source) == record['sourceSha256']
    flags = record['compilerFlags']
    directory = WORK / (record['mode'] + '-' + record['address'][2:])
    compiler.WORK = directory / 'compile'
    result = dict(identity={key: record[key] for key in ['processor', 'program', 'module', 'mode', 'address', 'initializedBytes']},
        source=record['source'], sourceSha256=sha256(source), compiled=False, genuineLinkProduced=False,
        exactNativeBytes=False, sourceCredit=0)
    try:
        rows, unused = compiler.compare(source, 'main', int(flags[0][2:]), flags[flags.index('-inline') + 1],
            speed='-opt' in flags and flags[flags.index('-opt') + 1] == 'speed',
            thumb=record['mode'] == 'thumb', compiler=COMPILER)
        assert len(rows) == 1 and not rows[0].get('compileFailed')
        row = rows[0]
        result.update(compiled=True, freshObjectSha256=row['objectSha256'], compilation=row)
        try:
            proof = validate(row, qualified_bindings(row), directory / 'link')
            result['exactNativeBytes'] = True
        except ValueError as error:
            assert isinstance(error.args[0], dict)
            proof = error.args[0]
        result['genuineLinkComparison'] = proof
        binary = directory / 'link/caller.bin'
        result.update(genuineLinkProduced=binary.is_file(), freshLinkedSha256=sha256(binary) if binary.is_file() else None)
    except Exception as error:
        result['error'] = repr(error)
    return result


def main():
    assert not OUTPUT.exists()
    archive = read_json(INPUT)
    records = [record for record in archive['records'] if record['compiledInHistoricalProof']]
    assert len(records) == 385
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        sourceArchive=INPUT.relative_to(ROOT).as_posix(), sourceArchiveSha256=sha256(INPUT),
        compilerSha256=sha256(COMPILER), sourceCredit=0, selectedSourceModified=False,
        originalObjectOrCacheInputs=0, compilerProcesses=3, state='running', results=[],
        limitations=['Per-unit historical optimization and inline settings are retained with a separately pinned compiler',
            'Compiler/link byte equality is a candidate only; argument contracts and behavior need independent validation',
            'No accepted source, object, registry, module or coverage change'])
    write_json(OUTPUT, report)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for result in pool.map(worker, records, chunksize=1):
            report['results'].append(result)
            report.update(compiledUnits=sum(row['compiled'] for row in report['results']),
                genuinelyLinkedUnits=sum(row['genuineLinkProduced'] for row in report['results']),
                exactByteHypotheses=sum(row['exactNativeBytes'] for row in report['results']))
            write_json(OUTPUT, report)
            if len(report['results']) % 25 == 0:
                print(dict(processed=len(report['results']), exactCandidates=report['exactByteHypotheses']), flush=True)
    report.update(state='finished', finishedUtc=now())
    write_json(OUTPUT, report)
    print(dict(finished=True, compiled=report['compiledUnits'], linked=report['genuinelyLinkedUnits'],
        exactCandidates=report['exactByteHypotheses'], sourceCredit=0))


if __name__ == '__main__':
    main()
