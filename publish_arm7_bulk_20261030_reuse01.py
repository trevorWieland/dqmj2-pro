import hashlib
import json
from pathlib import Path
import match_arm7_bulk_20261030_reuse01 as matcher
from project import write_json

ROOT = Path(__file__).resolve().parent


def main():
    report = matcher.run('published-reuse01')
    if len(report['matches']) != 7 or sum(row['bytes'] for row in report['matches']) != 252:
        raise ValueError('Fresh source-only unit closure changed')
    if sum(row['oracle']['actualOriginalAndRecompiledReturns'] for row in report['matches']) != 1120:
        raise ValueError('Fresh native/source actual return evidence incomplete')
    path = Path(__file__)
    report.update(oracleGenerator=report['generator'], oracleGeneratorSha256=report['generatorSha256'],
        generator=path.name, generatorSha256=hashlib.sha256(path.read_bytes()).hexdigest(), canonicalReportRegeneratedFromFreshSource=True)
    report['generatorSources'].append({'path': path.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    canonical = ROOT / 'evidence/matches/arm7-bulk-20261030-reuse01.json'
    write_json(canonical, report)
    print(json.dumps({'canonicalReport': canonical.relative_to(ROOT).as_posix(),
        'sha256': hashlib.sha256(canonical.read_bytes()).hexdigest(), 'sourceOnlyRebuild': True,
        'functions': 7, 'bytes': 252, 'actualOriginalAndRecompiledReturns': 1120}), flush=True)


if __name__ == '__main__':
    main()
