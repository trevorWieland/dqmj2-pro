import concurrent.futures
import hashlib
from pathlib import Path
import random
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256, now
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings
from permuter_local_ast_20261101 import mutate, COMMIT, ALLOWED

OUTPUT = ROOT / 'evidence/attempts/local-permuter-bump60-20261101.json'
WORK = ROOT / 'work/local-permuter-bump60-20261101'


def worker(job):
    seed, text, parent_hash, steps = job
    directory = WORK / str(seed)
    result = dict(seed=seed, parentSha256=parent_hash, mutationSteps=steps,
        compiled=False, genuinelyLinked=False, exact=False, score=None, sourceCredit=0)
    try:
        modified = mutate(text, 'native_main_0203c8a4', seed, steps)
        source = ROOT / f'generated/recovery/20261101-local-permuter-bump60/{seed}/native_main_0203c8a4.c'
        source.parent.mkdir(parents=True, exist_ok=True)
        assert not source.exists()
        source.write_text(modified, encoding='utf-8')
        result.update(source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source))
        compiler.WORK = directory / 'compile'
        rows, unused = compiler.compare(source, 'main', 2, 'off', compiler=ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe')
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
            body = binary.read_bytes()
            native = (ROOT / 'extract/arm9/arm9.bin').read_bytes()[0x3C8A4:0x3C8A4 + 60]
            result['score'] = sum(a != b for a, b in zip(body, native)) + abs(len(body) - len(native))
            result['linkedSha256'] = sha256(binary)
    except Exception as error:
        result['error'] = repr(error)
    return result


def main():
    assert not OUTPUT.exists()
    source = ROOT / 'generated/recovery/20261101-bump60/typed-0/native_main_0203c8a4.c'
    text = source.read_text()
    rng = random.Random(0x3C8A460)
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), toolCommit=COMMIT,
        adapterSha256=sha256(ROOT / 'permuter_local_ast_20261101.py'), source=source.relative_to(ROOT).as_posix(),
        sourceSha256=sha256(source), allowedPasses=sorted(ALLOWED), compilerProcesses=3, sourceCredit=0,
        state='running', startedUtc=now(), results=[],
        upstreamNetworkCompilerAndScorerNotImported=True, realMwldFullByteComparisonRequired=True,
        limitations=['Deterministic local AST hypotheses only; no semantic or original-source credit',
            'No distributed features, uploads, system package changes or OS scratch compiler directories',
            'A zero search score still requires manual source review and independent native/control/whole-module validation'])
    write_json(OUTPUT, report)
    parents = [(text, hashlib.sha256(text.encode()).hexdigest(), 7)]
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for epoch in range(8):
            jobs = []
            for offset in range(24):
                parent = rng.choice(parents[:8])
                seed = 0x60000000 + epoch * 24 + offset
                jobs.append((seed, parent[0], parent[1], rng.randint(1, 4)))
            for result in pool.map(worker, jobs):
                report['results'].append(result)
                if result['score'] is not None:
                    candidate = ROOT / result['source']
                    parents.append((candidate.read_text(), result['sourceSha256'], result['score']))
            parents.sort(key=lambda row: (row[2], row[1]))
            seen, unique = set(), []
            for row in parents:
                if row[1] not in seen:
                    seen.add(row[1])
                    unique.append(row)
            parents = unique[:16]
            report.update(processed=len(report['results']), bestByteScore=parents[0][2],
                compiled=sum(row['compiled'] for row in report['results']),
                genuinelyLinked=sum(row['genuinelyLinked'] for row in report['results']),
                exactHypotheses=sum(row['exact'] for row in report['results']))
            write_json(OUTPUT, report)
            print(dict(epoch=epoch, processed=report['processed'], bestByteScore=report['bestByteScore'], exact=report['exactHypotheses']), flush=True)
            if report['exactHypotheses']:
                break
    report.update(state='finished', finishedUtc=now())
    write_json(OUTPUT, report)


if __name__ == '__main__':
    main()
