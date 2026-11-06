import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from link_runtime_unit import measured_module

TAGS = ('314', '315', '316')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compile_current(job):
    row, index = job
    assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
    spec = importlib.util.spec_from_file_location('breadth319_' + str(index), ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    address = int(row['address'], 0)
    builder.ENTRY, builder.LENGTH, builder.NAME = address, row['bytes'], row['name']
    builder.SOURCE, builder.FLAGS = row['source'], row['flags']
    builder.COMPILER, builder.COMPILER_HASH = row['compilerPath'], row['compilerSha256']
    builder.WORK = 'work/save-core/breadth319/' + str(index)
    arm = measured_module('main')[1]
    result, body = builder.build(arm[address - 0x02000000:address - 0x02000000 + row['bytes']])
    assert result['compiledBytes'] == row['compiledBytes'] and result['sameOffsetBytes'] == row['sameOffsetBytes']
    assert sha(body) == row['linkedBinarySha256'] and not result['exactByteEqual']
    return result


def main():
    attempted, drafts, compiled, rows, receipts = {}, {}, {}, [], []
    for tag in TAGS:
        path = ROOT / ('evidence/lanes/save-core/app-large' + tag + '-20261101.json')
        report = json.loads(path.read_text())
        archive = report['fullProvenanceSidecar']
        packed = (ROOT / archive['path']).read_bytes()
        assert sha(packed) == archive['sha256'] and sha(gzip.decompress(packed)) == archive['uncompressedSha256']
        receipts.append(dict(path=path.relative_to(ROOT).as_posix(), sha256=sha(path.read_bytes()), archive=archive))
        for row in json.loads(gzip.decompress(packed)):
            identity = row['module'], row['processor'], row['mode'], int(row['address'], 0)
            assert identity not in attempted
            attempted[identity] = row
            if row.get('source'):
                assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
                drafts[identity] = row
            if row.get('compilable'):
                compiled[identity] = row
                for candidate in row.get('compileAttempts', []):
                    if candidate.get('realLinkSucceeded'):
                        rows.append((candidate, len(rows)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        current = list(pool.map(compile_current, rows))
    raw = (json.dumps(current, sort_keys=True, separators=(',', ':')) + '\n').encode()
    sidecar = ROOT / 'evidence/vectors/save-core-breadth319-current-20261101.json.gz'
    sidecar.write_bytes(gzip.compress(raw, mtime=0))
    result = dict(schema=1, selectedFunctions=len(attempted), selectedNativeBytes=sum(row['bytes'] for row in attempted.values()),
        sourceHypotheses=len(drafts), draftNativeBytes=sum(row['bytes'] for row in drafts.values()),
        compiledSourceHypotheses=len(compiled), compiledNativeBytes=sum(row['bytes'] for row in compiled.values()),
        genuineLinkedProfiles=len(current), exactSourceUnits=0, nativeSemanticallyQualified=0, acceptedSourceBytes=0,
        sources=[dict(path=row['source'], sha256=row['sourceSha256']) for row in drafts.values()],
        archivedSelectionReports=receipts, compilerWorkers=2,
        currentCompilerProvenance=dict(path=sidecar.relative_to(ROOT).as_posix(), sha256=sha(sidecar.read_bytes()), contentSha256=sha(raw)),
        generatorSha256=sha(Path(__file__).read_bytes()),
        limits=['Thirty-eight distinct previously unselected identities were attempted across the three bounded queues; existing draft sources remain refinements, not net-new recovered coverage.',
            'The13664-byte new-name candidate stops at UnsupportedPhysicalWordPair. Its generated SECOND_REG and unsetR2/R3 are not translated into invented C arguments or a fake wider return.',
            'These are compile-first source hypotheses. Inferred fields, pointer widths/strides, output extents, selected-C interfaces, return contracts and ordinary paths need independent native validation.',
            'Each compiling source/profile is genuinely rebuilt and linked from current files; old debug objects/work outputs are unnecessary. Compiler/object/link metadata remains separate from executable-byte identities.',
            'Failed conversion and compilation evidence remains in the compressed provenance archives, with zero exact or accepted source credit.'])
    path = ROOT / 'evidence/lanes/save-core/breadth319-20261101.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ('selectedFunctions', 'selectedNativeBytes', 'sourceHypotheses', 'draftNativeBytes', 'compiledSourceHypotheses', 'compiledNativeBytes', 'genuineLinkedProfiles', 'exactSourceUnits')}))


if __name__ == '__main__':
    main()
