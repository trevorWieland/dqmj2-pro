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
from source_dependencies import dependencies_current

ARCHIVE = 'evidence/vectors/save-core-larger-dereferences296-20261101.json.gz'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def run(job):
    spec = importlib.util.spec_from_file_location('larger298_' + job['address'], ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    address = int(job['address'], 0)
    builder.ENTRY, builder.LENGTH, builder.NAME = address, job['bytes'], f'native_main_{address:08x}'
    builder.SOURCE = job['source']
    assert sha((ROOT / builder.SOURCE).read_bytes()) == job['sourceSha256']
    assert sha((ROOT / job['originDraft']).read_bytes()) == job['sourceOriginSha256']
    native = measured_module('main')[1][address - 0x02000000:address - 0x02000000 + builder.LENGTH]
    assert sha(native) == job['nativeSpanSha256']
    rows = []
    for index, original in enumerate(job['compileAttempts']):
        builder.COMPILER, builder.COMPILER_HASH = original['compilerPath'], original['compilerSha256']
        builder.FLAGS = original['flags']
        builder.WORK = f'work/save-core/larger-replay298/{address:08x}/{index}'
        row, body = builder.build(native)
        assert dependencies_current(row) and row['compiledBytes'] == original['compiledBytes']
        assert row['sameOffsetBytes'] == original['sameOffsetBytes'] and not row['exactByteEqual']
        assert sha(body) == original['linkedBinarySha256']
        rows.append(row)
    return dict(address=job['address'], bytes=job['bytes'], source=job['source'], sourceSha256=job['sourceSha256'],
        nativeSpanSha256=job['nativeSpanSha256'], profiles=rows, measuredAccesses=job['measuredAccesses'],
        interfaceClosurePending=True, sourceCredit=0)


def main():
    document = json.loads((ROOT / 'evidence/lanes/save-core/larger-dereferences296-20261101.json').read_text())
    raw = (ROOT / ARCHIVE).read_bytes()
    assert sha(raw) == document['fullProvenanceSidecar']['sha256']
    assert sha(gzip.decompress(raw)) == document['fullProvenanceSidecar']['contentSha256']
    jobs = json.loads(gzip.decompress(raw))
    assert len(jobs) == 9 and sum(job['bytes'] for job in jobs) == 7780
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(run, jobs))
    result = dict(schema=1, sourceHypotheses=len(rows), draftNativeBytes=sum(row['bytes'] for row in rows),
        compilingUnits=len(rows), genuineLinkedProfiles=sum(len(row['profiles']) for row in rows),
        nearUnits=0, exactSourceUnits=0, nativeSemanticallyQualified=0, acceptedSourceBytes=0,
        compilerWorkers=2, rows=rows, archive=dict(path=ARCHIVE, sha256=sha(raw)),
        generatorSha256=sha(Path(__file__).read_bytes()),
        limits=document['limits'] + ['This replay uses the frozen nine source/profile hypotheses and reconstructs every object/link output locally. It does not rerun the mutable historical selection or require old work binaries.',
            'The current native-linked bytes are checked against historical executable-byte hashes. Current source/object/link provenance is recorded independently of historical debug object hashes.'])
    path = ROOT / 'evidence/lanes/save-core/larger-replay298-20261101.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ('sourceHypotheses', 'draftNativeBytes', 'compilingUnits', 'genuineLinkedProfiles', 'exactSourceUnits', 'acceptedSourceBytes')}))


if __name__ == '__main__':
    main()
