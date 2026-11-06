import concurrent.futures
import itertools
import re
from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256, now
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

INPUT = ROOT / 'evidence/attempts/root-breadth-archive-recompile-v2-20261101.json'
OUTPUT = ROOT / 'evidence/attempts/root-global-width-survey-20261101.json'
WORK = ROOT / 'work/root-global-widths-20261101'
DRAFTS = ROOT / 'generated/recovery/20261101-global-widths'


def worker(specification):
    previous, declarations, types = specification
    source = ROOT / previous['source']
    assert sha256(source) == previous['sourceSha256']
    text = source.read_text()
    substitutions = []
    for name, kind in zip(declarations, types):
        before = f'extern u8 {name}[];'
        after = f'extern {kind} {name}[];'
        assert text.count(before) == 1
        text = text.replace(before, after)
        if kind != 'u8':
            substitutions.append(dict(symbol=name, previousType='u8', hypothesisType=kind))
    identity = previous['identity']
    label = identity['mode'] + '-' + identity['address'][2:] + '-' + '-'.join(types)
    candidate = DRAFTS / label / source.name
    candidate.parent.mkdir(parents=True, exist_ok=True)
    if candidate.exists():
        assert candidate.read_text() == text
    else:
        candidate.write_text(text, encoding='utf-8')
    result = dict(identity=identity, source=candidate.relative_to(ROOT).as_posix(), sourceSha256=sha256(candidate),
        originalSource=previous['source'], originalSourceSha256=previous['sourceSha256'],
        measuredNativeAccessRequired=True, substitutions=substitutions, compiled=False,
        genuineLinkProduced=False, exactNativeBytes=False, sourceCredit=0)
    directory = WORK / label
    compiler.WORK = directory / 'compile'
    flags = previous['compilation']['compilerFlags']
    executable = ROOT / previous['compilation']['compilerPath']
    try:
        rows, unused = compiler.compare(candidate, 'main', int(flags[0][2:]), flags[flags.index('-inline') + 1],
            speed='-opt' in flags and flags[flags.index('-opt') + 1] == 'speed',
            thumb=identity['mode'] == 'thumb', compiler=executable)
        assert len(rows) == 1 and not rows[0].get('compileFailed')
        row = rows[0]
        result.update(compiled=True, compilation=row)
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
    previous = read_json(INPUT)
    queue = []
    for row in previous['results']:
        if row['exactNativeBytes']:
            continue
        text = (ROOT / row['source']).read_text()
        variables = re.findall(r'extern u8 (native_data_[0-9a-f]{8})\[\];', text)
        used = [name for name in variables if re.search(r'(?<![\w*])\*' + name + r'\b', text)]
        assert len(used) <= 3
        for types in itertools.product(['u8', 'u16', 'u32'], repeat=len(used)):
            if used and any(kind != 'u8' for kind in types):
                queue.append((row, used, types))
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        inputReport=INPUT.relative_to(ROOT).as_posix(), inputReportSha256=sha256(INPUT),
        sourceUnits=len({item[0]['source'] for item in queue}), variants=len(queue), compilerProcesses=3,
        selectedSourceModified=False, sourceCredit=0, state='running', results=[],
        limitations=['Generated array-width hypotheses only; historical global type and complete storage extent unproved',
            'Compiler/link equality does not prove defined behavior, native access width, caller contracts or reachable states',
            'No original source, registry, accepted object or byte coverage changes'])
    write_json(OUTPUT, report)
    print(dict(sourceUnits=report['sourceUnits'], variants=len(queue)), flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(worker, specification) for specification in queue]
        for future in concurrent.futures.as_completed(futures):
            report['results'].append(future.result())
            report.update(compiledVariants=sum(row['compiled'] for row in report['results']),
                genuinelyLinkedVariants=sum(row['genuineLinkProduced'] for row in report['results']),
                exactByteHypotheses=sum(row['exactNativeBytes'] for row in report['results']))
            write_json(OUTPUT, report)
            if len(report['results']) % 25 == 0:
                print(dict(processed=len(report['results']), exactCandidates=report['exactByteHypotheses']), flush=True)
    report.update(state='finished', finishedUtc=now())
    write_json(OUTPUT, report)
    print(dict(finished=True, compiled=report['compiledVariants'], linked=report['genuinelyLinkedVariants'],
        exactCandidates=report['exactByteHypotheses'], sourceCredit=0))


if __name__ == '__main__':
    main()
