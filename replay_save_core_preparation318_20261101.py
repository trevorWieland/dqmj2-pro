import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
EXPECTED = {
    'evidence/application/save-core-glyph305-20261101.json': ('caseSha256', 'dfc0247040fe6b95ceff2a1da68564c532cb06fab796f3394d4b1351aa894c99'),
    'evidence/application/save-core-preview317-20261101.json': ('caseSha256', 'c6b4832623a94f808a09320f34840f6a74a8613442dbf1155e2e3dbef81f5057')}
PRODUCERS = ['replay_save_core_preparation301_20261101.py',
    'evidence/application/save_core_glyph305_fixtures_20261101.py',
    'evidence/application/save_core_preview317_fixtures_20261101.py']


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    for producer in PRODUCERS:
        process = subprocess.run([sys.executable, str(ROOT / producer)], cwd=ROOT, capture_output=True, text=True, timeout=900)
        assert process.returncode == 0, (producer, process.stdout[-1000:], process.stderr[-2000:])
    compiler_path = 'evidence/lanes/save-core/preparation-replay301-20261101.json'
    compiler = json.loads((ROOT / compiler_path).read_text())
    assert (compiler['compiledSourceHypotheses'], compiler['genuineLinkedProfiles'], compiler['acceptedSourceBytes']) == (9, 14, 0)
    reports, sources = [], {row['path']: row['sha256'] for row in compiler['sources']}
    for path, (key, expected) in EXPECTED.items():
        report = json.loads((ROOT / path).read_text())
        assert report[key] == expected and report['sourceCredit'] == 0
        raw = (ROOT / report['sidecar']['path']).read_bytes()
        assert sha(raw) == report['sidecar']['sha256'] and sha(gzip.decompress(raw)) == expected
        rows = report.get('candidates', [report.get('candidate')])
        for row in rows:
            assert sha((ROOT / row['source']).read_bytes()) == row['sourceSha256']
            assert sha((ROOT / row['object']).read_bytes()) == row['objectSha256'] and not row['exactByteEqual']
            sources[row['source']] = row['sourceSha256']
        reports.append(dict(path=path, sha256=sha((ROOT / path).read_bytes()), nativeCaseSha256=expected, sidecar=report['sidecar']))
    glyph = json.loads((ROOT / next(iter(EXPECTED))).read_text())
    preview = json.loads((ROOT / list(EXPECTED)[1]).read_text())
    assert (glyph['cases'], glyph['actualTopReturns'], glyph['actualNativeHelperReturns'], glyph['suppliedBoundaryCalls']) == (1562, 4686, 32586, 5331)
    assert glyph['nativeCodeOffsets'] == list(range(0, 868, 4))
    assert (preview['cases'], preview['totalActualPreviewReturns'], preview['actualMapperReturns'], preview['actualRankHelperReturns']) == (1344, 2688, 2692, 4800)
    assert len(preview['unsupported']) == 4 and all(not row['actualReturn'] and not row['postFaultStateClaimed'] for row in preview['unsupported'])
    output = dict(schema=1, sourceCredit=0, newFunctions=0, newBytes=0, compiledSourceHypotheses=9,
        uniqueNativeFunctions=2, uniqueNativeBytes=1420, genuineCompilerLinkProfiles=14,
        functionalSourceHypotheses=3, actualParserTopReturns=4686, actualPreviewTopReturns=2688,
        actualMapperReturns=2692, actualParserHelperReturns=32586, actualRankHelperReturns=4800,
        suppliedParserBoundaryCalls=5331, reports=reports,
        compilerReport=dict(path=compiler_path, sha256=sha((ROOT / compiler_path).read_bytes())),
        sources=[dict(path=path, sha256=digest) for path, digest in sorted(sources.items())],
        producers=[dict(path=path, sha256=sha((ROOT / path).read_bytes())) for path in PRODUCERS],
        generatorSha256=sha(Path(__file__).read_bytes()),
        limits=compiler['limits'] + glyph['limits'] + preview['limitations'])
    path = ROOT / 'evidence/lanes/save-core/preparation318-20261101.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps(dict(compilingSourceHypotheses=9, profiles=14, parserReturns=4686, previewReturns=2688,
        mapperReturns=2692, sourceCredit=0, reportSha256=sha(path.read_bytes()))))


if __name__ == '__main__':
    main()
