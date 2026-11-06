import cProfile
import pstats
import time
import ledger_state
from project import ROOT, write_json, sha256


def main():
    profiler = cProfile.Profile()
    before = sha256(ROOT / 'recovery.json')
    started = time.perf_counter()
    error = None
    try:
        profiler.runcall(ledger_state.build_state, write=False)
    except Exception as failure:
        error = type(failure).__name__ + ': ' + str(failure)
    output = ROOT / 'work/ledger-evaluation-profile-20261031.pstats'
    output.parent.mkdir(parents=True, exist_ok=True)
    profiler.dump_stats(output)
    stats = pstats.Stats(profiler)
    rows = [dict(file=key[0], line=key[1], function=key[2], primitiveCalls=value[0], calls=value[1],
        ownSeconds=value[2], cumulativeSeconds=value[3]) for key, value in stats.stats.items()]
    write_json(ROOT / 'evidence/verification/ledger-performance-profile-20261031.json', dict(
        elapsedSeconds=time.perf_counter() - started, error=error, sourceCredit=0,
        sourceRegistryBefore=before, sourceRegistryAfter=sha256(ROOT / 'recovery.json'),
        topCumulative=sorted(rows, key=lambda row: row['cumulativeSeconds'], reverse=True)[:30],
        topOwnTime=sorted(rows, key=lambda row: row['ownSeconds'], reverse=True)[:30],
        limitations=['Read-only performance research during a pending build; its state result is not acceptance evidence',
            'No frozen framework, current source selection or accepted result is replaced']))
    print(dict(elapsedSeconds=time.perf_counter() - started, error=error, sourceCredit=0))


if __name__ == '__main__':
    main()
