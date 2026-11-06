import importlib.util
import time
import ledger_state
from project import ROOT, write_json, sha256


def main():
    path = ROOT / 'evidence/encounter/script_assets_20261029.py'
    before = sha256(path)
    import sys
    sys.path.insert(0, str(path.parent))
    import script_assets_20261029
    import interpreted_sources
    import interpreted_empty_sources
    import interpreted_capture_sources
    import sys
    modules = [module for module in list(sys.modules.values()) if getattr(module, '__file__', None)
        and str(module.__file__).replace('\\', '/').endswith('/evidence/encounter/script_assets_20261029.py')]
    assert modules
    caches, counts = {}, dict(calls=0, hits=0, decodedBytes=0)
    originals = []
    for module in modules:
        original, read_word = module.ash, module.u32
        originals.append((module, original, read_word))
        cache = caches.setdefault(before, {})

        def wrapped(data, original=original, read_word=read_word, module=module, cache=cache):
            assert module.u32 is read_word
            assert isinstance(data, (bytes, bytearray, memoryview))
            key = bytes(data)
            counts['calls'] += 1
            if key in cache:
                counts['hits'] += 1
                return cache[key]
            result = original(key)
            assert isinstance(result, bytes)
            cache[key] = result
            counts['decodedBytes'] += len(result)
            return result

        module.ash = wrapped
    phases = []
    for index in range(2):
        started = time.perf_counter()
        before_counts = dict(counts)
        error = None
        try:
            ledger_state.build_state(write=False)
        except Exception as failure:
            error = type(failure).__name__ + ': ' + str(failure)
        phases.append(dict(index=index, elapsedSeconds=time.perf_counter() - started,
            calls=counts['calls'] - before_counts['calls'], hits=counts['hits'] - before_counts['hits'], error=error))
        print(phases[-1], flush=True)
    assert sha256(path) == before
    write_json(ROOT / 'evidence/verification/ash-memoization-benchmark-20261031.json', dict(
        originalDecoder=path.relative_to(ROOT).as_posix(), originalDecoderSha256=before,
        phases=phases, counters=counts, uniqueCompressedInputs=sum(len(cache) for cache in caches.values()),
        immutableBytesOnly=True, decoderFileUnchanged=True, sourceCredit=0, adopted=False,
        limitations=['Every distinct compressed byte string runs the unchanged original decoder; only identical byte inputs reuse immutable byte outputs',
            'Failed decodes are never cached; source-word reader identity is guarded',
            'Read-only performance experiment during a pending build; state results are not acceptance evidence',
            'No current build controller or frozen source file is changed']))


if __name__ == '__main__':
    main()
