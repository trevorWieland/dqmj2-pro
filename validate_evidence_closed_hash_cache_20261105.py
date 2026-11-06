import runpy
import time
from unittest.mock import patch
import ledger_state
from project import ROOT, read_json, write_json, sha256
from closed_snapshot_hash_cache_20261105 import scope


def main():
    baseline = read_json(ROOT / 'evidence/verification/evidence-freshness.json')
    prior_timing = read_json(ROOT / 'evidence/verification/ash-cached-acceptance-20261031.json')
    protected = ['ledger_state.py', 'validate_evidence.py',
        'validate_evidence_ash_cache_20261031.py', 'evidence/encounter/script_assets_20261029.py',
        'recovery.json', 'source-preferences.json', 'manifest.json']
    before = {name: sha256(ROOT / name) for name in protected}
    snapshots = []

    def wrap(function):
        def run(*args, **kwargs):
            if function.__name__ == 'build_state':
                assert kwargs.get('write', args[0] if args else True) is False
            with scope(snapshots):
                return function(*args, **kwargs)
        return run

    started = time.perf_counter()
    with patch.object(ledger_state, 'build_state', wrap(ledger_state.build_state)), \
            patch.object(ledger_state, 'collect_matches', wrap(ledger_state.collect_matches)):
        runpy.run_path(str(ROOT / 'validate_evidence_ash_cache_20261031.py'), run_name='__main__')
    actual = read_json(ROOT / 'evidence/verification/evidence-freshness.json')
    assert actual['passed'] and actual['negativeAcceptanceCases'] == baseline['negativeAcceptanceCases']
    assert actual['restoredSourceFunctions'] == read_json(ROOT / 'manifest.json')['functionMatched']
    assert before == {name: sha256(ROOT / name) for name in protected}
    controls = read_json(ROOT / 'evidence/verification/closed-snapshot-hash-cache-controls-20261105.json')
    assert controls['passed'] and controls['qualifierSha256'] == sha256(ROOT / 'closed_snapshot_hash_cache_20261105.py')
    output = 'evidence/verification/closed-hash-cached-acceptance-20261105.json'
    write_json(ROOT / output, dict(passed=True, sourceCredit=0,
        generatorSha256=sha256(__file__), helperSha256=controls['qualifierSha256'], elapsedSeconds=time.perf_counter() - started,
        sourceRegistrySha256=before['recovery.json'], originalFilesUnchanged=before,
        previousOriginalFreshnessSeconds=prior_timing['elapsedSeconds'],
        previousOriginalFunctions=prior_timing['restoredSourceFunctions'],
        originalNegativeAcceptanceCases=actual['negativeAcceptanceCases'],
        restoredSourceFunctions=actual['restoredSourceFunctions'], snapshotScopes=snapshots,
        exactDistinctInputHashExecutionsRetained=True, everySnapshotFullyRehashedBeforeReturn=True,
        originalParserNamespaceSourceFreshnessAndRejectionChecksUnchanged=True,
        limitations=['Only repeated hashes inside one read-only ledger snapshot reuse the original result.',
            'Every distinct file is hashed with the original function initially and again before a successful return.',
            'Each new snapshot starts empty. No file/object/report/compiler/namespace check or source-credit rule is removed.',
            'This does not establish a full clean source build or native game execution.']))
    print(dict(passed=True, elapsedSeconds=time.perf_counter() - started,
        snapshots=len(snapshots), duplicateHashesReused=sum(s['hits'] for s in snapshots)))


if __name__ == '__main__':
    main()
