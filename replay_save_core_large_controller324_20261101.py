import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from link_runtime_unit import measured_module


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    archived_path = 'evidence/lanes/save-core/large-controller324-archive-20261101.json'
    archive = json.loads((ROOT / archived_path).read_text())
    sidecar = archive['historicalArchive']
    packed = (ROOT / sidecar['path']).read_bytes()
    assert sha(packed) == sidecar['sha256'] and sha(gzip.decompress(packed)) == sidecar['contentSha256']
    historical = json.loads(gzip.decompress(packed))
    for item in archive['sources']:
        raw = (ROOT / item['path']).read_bytes()
        assert sha(raw) == item['sha256'] and len(raw.splitlines()) <= 500
        assert b'SECOND_REG' not in raw and b'M2C_ERROR' not in raw
    module, arm, _ = measured_module('main')
    native = arm[0xBB878:0xBB878 + 13664]
    assert sha(native) == archive['nativeSpanSha256']
    candidates = [row for row in historical if row.get('compilable')]
    assert len(candidates) == 1 and len(historical) == 2
    current = []
    for index, prior in enumerate(candidates[0]['compileAttempts']):
        spec = importlib.util.spec_from_file_location('controller324_' + str(index), ROOT / 'evidence/application/save_core_historical_link_20261031.py')
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        builder.ENTRY, builder.LENGTH, builder.NAME = 0x020BB878, 13664, prior['name']
        builder.SOURCE, builder.FLAGS = prior['source'], prior['flags']
        builder.COMPILER, builder.COMPILER_HASH = prior['compilerPath'], prior['compilerSha256']
        builder.WORK = 'work/save-core/large-controller324/' + str(index)
        row, body = builder.build(native)
        assert (row['compiledBytes'], row['sameOffsetBytes']) == (prior['compiledBytes'], prior['sameOffsetBytes'])
        assert sha(body) == prior['linkedBinarySha256'] and not row['exactByteEqual']
        current.append(row)
    raw = (json.dumps(current, sort_keys=True, separators=(',', ':')) + '\n').encode()
    packed = gzip.compress(raw, mtime=0)
    path = ROOT / 'evidence/vectors/save-core-large324-current-20261101.json.gz'
    path.write_bytes(packed)
    result = dict(schema=1, sourceCredit=0, newFunctions=0, newBytes=0, nativeFunctions=1, nativeBytes=13664,
        sourceHypotheses=2, compiledHypotheses=1, genuineLinkedProfiles=2, exactSourceUnits=0,
        actualNativeReturns=0, actualCompiledReturns=0, sources=archive['sources'],
        archivedReport=dict(path=archived_path, sha256=sha((ROOT / archived_path).read_bytes())),
        historicalArchive=sidecar, currentCompilerProvenance=dict(path=path.relative_to(ROOT).as_posix(), sha256=sha(packed), contentSha256=sha(raw)),
        compiledRanges=[dict(source=row['source'], compiledBytes=row['compiledBytes'], sameOffsetBytes=row['sameOffsetBytes'], linkedBinarySha256=row['linkedBinarySha256']) for row in current],
        generatorSha256=sha(Path(__file__).read_bytes()), limits=archive['limits'])
    path = ROOT / 'evidence/lanes/save-core/large-controller324-20261101.json'
    path.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(compiling=1, profiles=2, exact=0, sourceCredit=0, reportSha256=sha(path.read_bytes()))))


if __name__ == '__main__':
    main()
