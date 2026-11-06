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

ARCHIVES = ['evidence/lanes/save-core/preview-accumulator299-20261101.json',
    'evidence/lanes/save-core/preview-lifetimes300-20261101.json',
    'evidence/lanes/save-core/glyph-parser303-20261101.json']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(job):
    row, index = job
    assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
    spec = importlib.util.spec_from_file_location('preview301_' + str(index), ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    address = int(row['address'], 0)
    builder.ENTRY, builder.LENGTH, builder.NAME = address, row['bytes'], row['name']
    builder.SOURCE, builder.FLAGS = row['source'], row['flags']
    builder.COMPILER, builder.COMPILER_HASH = row['compilerPath'], row['compilerSha256']
    builder.WORK = 'work/save-core/preparation-replay301/' + str(index)
    arm = measured_module('main')[1]
    current, body = builder.build(arm[address - 0x02000000:address - 0x02000000 + row['bytes']])
    assert current['compiledBytes'] == row['compiledBytes'] and current['sameOffsetBytes'] == row['sameOffsetBytes']
    assert sha(body) == row['linkedBinarySha256'] and not current['exactByteEqual']
    return current


def main():
    jobs, receipts = [], []
    for path in ARCHIVES:
        raw = (ROOT / path).read_bytes()
        document = json.loads(raw)
        receipts.append(dict(path=path, sha256=sha(raw)))
        for row in document['rows']:
            jobs.append((row, len(jobs)))
    assert len(jobs) == 14
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(run, jobs))
    raw = (json.dumps(rows, sort_keys=True, separators=(',', ':')) + '\n').encode()
    sidecar = ROOT / 'evidence/vectors/save-core-preparation301-compiler-20261101.json.gz'
    sidecar.write_bytes(gzip.compress(raw, mtime=0))
    output = dict(schema=1, compiledSourceHypotheses=len({row['source'] for row in rows}), uniqueNativeFunctions=2,
        uniqueNativeBytes=1420, genuineLinkedProfiles=14, exactSourceUnits=0, acceptedSourceBytes=0,
        archives=receipts, compilerWorkers=2, sources=[dict(path=path, sha256=sha((ROOT / path).read_bytes())) for path in sorted({row['source'] for row in rows})],
        currentCompilerProvenance=dict(path=sidecar.relative_to(ROOT).as_posix(), sha256=sha(sidecar.read_bytes()), contentSha256=sha(raw)),
        generatorSha256=sha(Path(__file__).read_bytes()),
        limits=['Nine new source alternatives refine two larger native functions; they do not add exact or accepted executable coverage.',
            'The536-byte preview uses natural width accumulation and coordinate/lifetime hypotheses. No forced registers, padding, invented arities, assembly or byte edits are used.',
            'The884-byte parser restores native default branches previously emitted as unreachable tails, preserves measured halfword stores, forwards allocator alignment4 and uses selected pointer/copy views. Its full interface and real lower formatter behavior remain unproved.',
            'Each current compiler object and real linker output is rebuilt locally. Historical source/native/profile/linked-byte identities are checked independently of debug object paths.'])
    path = ROOT / 'evidence/lanes/save-core/preparation-replay301-20261101.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: output[key] for key in ('compiledSourceHypotheses', 'uniqueNativeFunctions', 'uniqueNativeBytes', 'genuineLinkedProfiles', 'exactSourceUnits')}))


if __name__ == '__main__':
    main()
