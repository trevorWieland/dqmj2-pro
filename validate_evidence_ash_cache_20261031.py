import runpy
import struct
import sys
import time
from project import ROOT, read_json, write_json, sha256


def main():
    decoder_path = ROOT / 'evidence/encounter/script_assets_20261029.py'
    benchmark = read_json(ROOT / 'evidence/verification/ash-memoization-benchmark-20261031.json')
    expected_hash = benchmark['originalDecoderSha256']
    assert sha256(decoder_path) == expected_hash and benchmark['decoderFileUnchanged']
    registry_hash = sha256(ROOT / 'recovery.json')
    validator_hash = sha256(ROOT / 'validate_evidence.py')
    baseline = read_json(ROOT / 'evidence/verification/evidence-freshness.json')
    sys.path.insert(0, str(decoder_path.parent))
    import script_assets_20261029 as assets
    original, read_word = assets.ash, assets.u32
    cache = {}
    counters = dict(calls=0, hits=0, successfulOriginalDecodes=0, failedOriginalDecodes=0)

    def memoized(data):
        assert assets.u32 is read_word
        assert isinstance(data, (bytes, bytearray, memoryview))
        key = bytes(data)
        counters['calls'] += 1
        if key in cache:
            counters['hits'] += 1
            return cache[key]
        try:
            result = original(key)
        except Exception:
            counters['failedOriginalDecodes'] += 1
            raise
        assert isinstance(result, bytes)
        counters['successfulOriginalDecodes'] += 1
        cache[key] = result
        return result

    header = b'ASH\0' + struct.pack('<I', 3) + bytes(8)
    value = bytearray(header + bytes([6, 1, 2, 3]))
    assert memoized(value) == bytes([1, 2, 3])
    assert memoized(bytes(value)) == bytes([1, 2, 3])
    value[-1] = 4
    assert memoized(value) == bytes([1, 2, 4])
    assert memoized(header + bytes([6, 1, 2, 3])) == bytes([1, 2, 3])
    failures_before = counters['failedOriginalDecodes']
    for unused in range(2):
        try:
            memoized(b'invalid')
        except AssertionError:
            pass
        else:
            raise ValueError('Invalid compressed bytes accepted')
    assert counters['failedOriginalDecodes'] - failures_before == 2
    controls = dict(equalImmutableKeysReuseOutput=True, mutatedInputReevaluated=True, failuresNeverCached=True)
    cache.clear()
    before = dict(counters)
    assets.ash = memoized
    started = time.perf_counter()
    try:
        runpy.run_path(str(ROOT / 'validate_evidence.py'), run_name='__main__')
    finally:
        assets.ash = original
    actual = read_json(ROOT / 'evidence/verification/evidence-freshness.json')
    manifest = read_json(ROOT / 'manifest.json')
    assert actual['passed'] and actual['negativeAcceptanceCases'] == baseline['negativeAcceptanceCases']
    assert actual['restoredSourceFunctions'] == manifest['functionMatched']
    assert sha256(ROOT / 'recovery.json') == registry_hash
    assert sha256(decoder_path) == expected_hash and sha256(ROOT / 'validate_evidence.py') == validator_hash
    write_json(ROOT / 'evidence/verification/ash-cached-acceptance-20261031.json', dict(
        passed=True, sourceCredit=0, sourceRegistrySha256=registry_hash, originalDecoderSha256=expected_hash,
        originalValidatorSha256=validator_hash, generatorSha256=sha256(__file__), elapsedSeconds=time.perf_counter() - started,
        counters={key: counters[key] - before[key] for key in counters}, uniqueCompressedInputs=len(cache),
        cacheControls=controls, restoredSourceFunctions=actual['restoredSourceFunctions'],
        allOriginalNegativeAcceptanceCases=actual['negativeAcceptanceCases'], frozenFilesUnchanged=True,
        limitations=['Every distinct exact compressed byte string runs the unchanged original decoder; only equal byte inputs reuse immutable decoded bytes',
            'Source, input, product freshness and rejection tests are the unchanged original program; no acceptance check is removed',
            'This does not replace current source/build checks or fresh clean source execution']))
    print(dict(passed=True, elapsedSeconds=time.perf_counter() - started, cacheHits=counters['hits'] - before['hits']))


if __name__ == '__main__':
    main()
