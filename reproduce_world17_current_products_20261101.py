import argparse
import gzip
import runpy
import sys
from pathlib import Path
import match_runtime
from project import ROOT, read_json, write_json, sha256


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--expected-root', required=True)
    options = parser.parse_args()
    assert Path(options.expected_root).resolve() == ROOT.resolve()
    matcher = 'match_scr_world17_20261030_batch11.py'
    assert sha256(ROOT / matcher) == 'b405d19b31a6a5d85f1c66ba2ec3fee66410482a7c34d6bed352bd65b3d0d1ff'
    names = [matcher, 'validate_scr_world17_20261030_batch11.py',
        'verify_interpreted_bounded_selection_sources.py', 'interpreted_bounded_selection_sources.py',
        'recovery.json', 'source-preferences.json', 'interpreted-recovery.json', 'run_checks.py']
    frozen = {name: sha256(ROOT / name) for name in names}
    positive = ROOT / 'evidence/matches/scripts-20261030-world17.json'
    archive = ROOT / 'evidence/attempts/world17-current-products-20261101'
    archive.mkdir(parents=True, exist_ok=True)
    old = archive / 'original-report.json.gz'
    assert not old.exists()
    old.write_bytes(gzip.compress(positive.read_bytes(), mtime=0))
    old_sha = sha256(positive)
    runpy.run_path(str(ROOT / matcher), run_name='__main__')
    runpy.run_path(str(ROOT / 'verify_interpreted_bounded_selection_sources.py'), run_name='__main__')
    assert all(sha256(ROOT / name) == digest for name, digest in frozen.items())
    current = read_json(positive)
    negatives = read_json(ROOT / 'evidence/verification/interpreted-bounded-selection-source-negatives-20261030.json')
    write_json(ROOT / 'evidence/verification/world17-current-products-20261101.json',
        dict(generator=Path(__file__).name, generatorSha256=sha256(__file__), expectedRoot=str(ROOT),
            originalFrozenImplementations=frozen, originalReportSha256=old_sha,
            oldReportArchive=old.relative_to(ROOT).as_posix(), oldReportArchiveSha256=sha256(old),
            freshCanonicalReportSha256=sha256(positive),
            fullOriginalProducerAndNegativeVerifierPassed=True,
            completeOwnEntryExecutions=current['pairedCompleteOwnEntryExecutions'],
            actualNativeReturningCalls=current['pairedNativeReturningCalls'],
            negativeResultSha256=sha256(ROOT / 'evidence/verification/interpreted-bounded-selection-source-negatives-20261030.json'),
            sourceCredit=0, sourceAndValidatorsAndRegistriesUnchanged=True,
            limitations=['Fresh world17 compiler/native products repair a stale source-only build cwd receipt',
                'Original path guards and exact-reason negative controls are unchanged',
                'No report field is rewritten manually and no source or acceptance condition is weakened',
                'This targeted replay does not prove a full uninterrupted clean build or source-only ROM']))
    print(dict(world17OriginalProducerAndAllOriginalNegativesPassed=True, sourceCredit=0))


if __name__ == '__main__':
    main()
