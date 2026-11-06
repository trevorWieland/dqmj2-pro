import concurrent.futures
import re
from pathlib import Path
import match_runtime as compiler
from project import ROOT, read_json, write_json, sha256, now
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings

INPUT = ROOT / 'evidence/attempts/root-breadth-archive-recompile-v2-20261101.json'
OUTPUT = ROOT / 'evidence/attempts/root-indexed-field-widths-20261101.json'
WORK = ROOT / 'work/root-indexed-field-widths-20261101'
DRAFTS = ROOT / 'generated/recovery/20261101-indexed-field-widths'
PATTERN = re.compile(r'\*\((native_data_[0-9a-f]{8}) \+ (\([^\n;]+?\))\)')


def worker(specification):
    previous, position, kind = specification
    source = ROOT / previous['source']
    assert sha256(source) == previous['sourceSha256']
    text = source.read_text()
    spans = list(PATTERN.finditer(text))
    target = spans[position]
    replacement = f'M2C_FIELD({target.group(1)} + {target.group(2)}, {kind} *, 0)'
    modified = text[:target.start()] + replacement + text[target.end():]
    identity = previous['identity']
    label = identity['mode'] + '-' + identity['address'][2:] + f'-{position}-{kind}'
    candidate = DRAFTS / label / source.name
    candidate.parent.mkdir(parents=True, exist_ok=True)
    assert not candidate.exists()
    candidate.write_text(modified, encoding='utf-8')
    result = dict(identity=identity, source=candidate.relative_to(ROOT).as_posix(), sourceSha256=sha256(candidate),
        originalSource=previous['source'], originalSourceSha256=previous['sourceSha256'],
        replacedExpression=target.group(), replacement=replacement, compiled=False,
        genuineLinkProduced=False, exactNativeBytes=False, sourceCredit=0)
    directory = WORK / label
    compiler.WORK = directory / 'compile'
    flags = previous['compilation']['compilerFlags']
    try:
        rows, unused = compiler.compare(candidate, 'main', int(flags[0][2:]), flags[flags.index('-inline') + 1],
            speed='-opt' in flags and flags[flags.index('-opt') + 1] == 'speed',
            thumb=identity['mode'] == 'thumb', compiler=ROOT / previous['compilation']['compilerPath'])
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
        if row['exactNativeBytes'] or not row['compiled']:
            continue
        address = int(row['identity']['address'], 0)
        assert 0x02000800 <= address < 0x02040000 or address >= 0x020D0000
        text = (ROOT / row['source']).read_text()
        for position, span in enumerate(PATTERN.finditer(text)):
            for kind in ['u16', 'u32']:
                queue.append((row, position, kind))
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), startedUtc=now(),
        inputReport=INPUT.relative_to(ROOT).as_posix(), inputReportSha256=sha256(INPUT),
        sourceUnits=len({item[0]['source'] for item in queue}), variants=len(queue), compilerProcesses=3,
        selectedSourceModified=False, sourceCredit=0, state='running', results=[],
        limitations=['Indexed memory access widths are hypotheses until native instructions, storage and behavior are independently checked',
            'Address arithmetic preserves the original byte stride rather than changing array element scaling',
            'No accepted source, object, registry or coverage changes; matching hypotheses still require qualified overlap checks'])
    write_json(OUTPUT, report)
    print(dict(sourceUnits=report['sourceUnits'], variants=len(queue)), flush=True)
    with concurrent.futures.ProcessPoolExecutor(max_workers=3) as pool:
        for result in pool.map(worker, queue):
            report['results'].append(result)
            report.update(compiledVariants=sum(row['compiled'] for row in report['results']),
                genuinelyLinkedVariants=sum(row['genuineLinkProduced'] for row in report['results']),
                exactByteHypotheses=sum(row['exactNativeBytes'] for row in report['results']))
            write_json(OUTPUT, report)
    report.update(state='finished', finishedUtc=now())
    write_json(OUTPUT, report)
    print(dict(finished=True, compiled=report.get('compiledVariants', 0), linked=report.get('genuinelyLinkedVariants', 0),
        exactCandidates=report.get('exactByteHypotheses', 0), sourceCredit=0))


if __name__ == '__main__':
    main()
