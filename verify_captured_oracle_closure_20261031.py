import argparse
from project import ROOT, read_json, write_json, sha256
from oracle_source_closure_20261031 import verify_commit


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    options = parser.parse_args()
    captured = ROOT / f'evidence/verification/cohort{options.cohort}-captured-oracle-closure-20261031.json'
    report = read_json(captured)
    assert report['registrySha256'] == sha256(ROOT / 'recovery.json')
    assert not report['missingRequiredPaths']
    changed = [path for path, digest in report['sourceAndEvidenceHashes'].items()
        if not (ROOT / path).is_file() or sha256(ROOT / path) != digest]
    assert not changed, changed
    result = verify_commit(report)
    output = dict(capturedClosure=captured.relative_to(ROOT).as_posix(), capturedClosureSha256=sha256(captured),
        sourceRegistrySha256=report['registrySha256'], currentContentHashesRechecked=True,
        currentPathsChecked=len(report['sourceAndEvidenceHashes']), committedVerification=result,
        sourceCredit=0, fullCleanReplayProven=False, limitations=[
            'Uses the complete unchanged collector result captured during source staging, followed by current content and committed-blob checks',
            'Static discovery retains the original limitations for dynamically constructed inputs; fresh clean execution remains required'])
    write_json(ROOT / f'evidence/verification/cohort{options.cohort}-captured-oracle-closure-verification-20261031.json', output)
    assert result['passed'], result
    print(dict(cohort=options.cohort, currentPathsChecked=output['currentPathsChecked'], committed=True))


if __name__ == '__main__':
    main()
