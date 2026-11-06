import hashlib
import concurrent.futures
import gzip
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'evidence/application/save-core-dialog261-20261101.json': '58797e70fb8b60a2cce34495d0dbbb2ce743a72125f64dfc61023f7f5d91f530',
    'evidence/application/save-core-constructor270-20261101.json': '976df78158cb9b7fc51561826e6bbacb7ece72c0a523a27fc565709d03c2a65e',
    'evidence/application/save-core-preview271-20261101.json': '9d8c63584f856720d193017cba7e8c16f35b8932013ecb498bdd3c4c6df1f8fe',
}
PROFILES = ['dialog-extent259', 'explicit-byte-views262', 'preview-words263',
            'preview-words263-selected', 'constructor269', 'allocation-words273', 'roster-stride274']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def compiler_replay(row):
    sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
    from link_runtime_unit import measured_module
    assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
    key = row['sourceSha256'][:16] + '-' + sha(json.dumps(row['flags']).encode())[:12]
    spec = importlib.util.spec_from_file_location('large275_build_' + key, ROOT / 'evidence/application/save_core_historical_link_20261031.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    address = int(row['address'], 0)
    builder.ENTRY, builder.LENGTH, builder.NAME = address, row['bytes'], row['name']
    builder.SOURCE, builder.FLAGS = row['source'], row['flags']
    builder.COMPILER, builder.COMPILER_HASH = row['compilerPath'], row['compilerSha256']
    builder.WORK = 'work/save-core/large275-compiler/' + key
    arm = measured_module('main')[1]
    current, body = builder.build(arm[address - 0x02000000:address - 0x02000000 + row['bytes']])
    assert current['compiledBytes'] == row['compiledBytes'] and current['sourceSha256'] == row['sourceSha256']
    assert sha(body) == row['linkedBinarySha256'] and not current['exactByteEqual']
    return current


def main():
    profiles = {}
    for name in PROFILES:
        data = json.loads((ROOT / ('evidence/lanes/save-core/' + name + '-20261101.json')).read_text())
        for row in data if isinstance(data, list) else data['rows']:
            key = row['source'], tuple(row['flags']), row['compilerPath']
            profiles[key] = row
    assert len(profiles) == 26 and len({row['source'] for row in profiles.values()}) == 14
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        compiled = list(pool.map(compiler_replay, profiles.values()))
    compiler_raw = (json.dumps(compiled, sort_keys=True, indent=2) + '\n').encode()
    compiler_sidecar = ROOT / 'evidence/vectors/save-core-large275-compiler-20261101.json.gz'
    compiler_sidecar.write_bytes(gzip.compress(compiler_raw, mtime=0))
    producers = ['compile_save_core_constructor269_20261101.py',
        'compile_save_core_allocation_words273_20261101.py',
        'compile_save_core_roster_stride274_20261101.py',
        'evidence/application/save_core_dialog261_fixtures_20261101.py',
        'evidence/application/save_core_constructor270_fixtures_20261101.py',
        'evidence/application/save_core_preview271_fixtures_20261101.py']
    steps = []
    for path in producers:
        process = subprocess.run([sys.executable, str(ROOT / path)], cwd=ROOT, capture_output=True,
            text=True, timeout=600, creationflags=subprocess.CREATE_NO_WINDOW)
        assert process.returncode == 0, (path, process.stdout[-1000:], process.stderr[-2500:])
        steps.append(dict(producer=path, sha256=sha((ROOT / path).read_bytes()), exitCode=0))
    reports = []
    sources = {}
    for path, expected in EXPECTED.items():
        data = json.loads((ROOT / path).read_text())
        assert data['caseSha256'] == expected and data['sourceCredit'] == 0
        raw = (ROOT / data['sidecar']['path']).read_bytes()
        assert sha(raw) == data['sidecar']['sha256']
        rows = data['preferredSources'] if path.endswith('dialog261-20261101.json') else [data['candidate']]
        for row in rows:
            assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
            assert sha((ROOT / row['object']).read_bytes()) == row['objectSha256']
            assert not row['exactByteEqual']
            sources[row['source']] = row['sourceSha256']
        reports.append(dict(path=path, sha256=sha((ROOT / path).read_bytes()), nativeCaseSha256=expected,
            sidecar=data['sidecar']))
    output = dict(schema=1, sourceCredit=0, acceptedFunctions=0, acceptedBytes=0,
        compilerProfiles=len(compiled), compiledSourceHypotheses=14, compilerWorkers=2,
        compilerProvenance=dict(path=compiler_sidecar.relative_to(ROOT).as_posix(),
            sha256=sha(compiler_sidecar.read_bytes()), uncompressedSha256=sha(compiler_raw)),
        functionalSources=[dict(path=path, sha256=digest) for path, digest in sorted(sources.items())],
        steps=steps, functionalReports=reports,
        limitations=['All functional reports cover explicitly qualified slices/contexts of nonmatching larger hypotheses.',
            'Draft/compiling/genuine-link/functional andexact accepted stages are independent;this script registers orselects no source.',
            'Generated fixture reports andsidecars are materialized within this invocation. Current object/link provenance may change across repository roots while source/native case identities remain pinned.'])
    target = ROOT / 'evidence/lanes/save-core/large-replay275-20261101.json'
    target.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(functionalSourceHypotheses=len(sources), acceptedBytes=0,
        reportSha256=sha(target.read_bytes()), nativeCaseDigests=list(EXPECTED.values()))))


if __name__ == '__main__':
    main()
