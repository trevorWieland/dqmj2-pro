from project import ROOT, read_json, sha256


def select(cohort, closure):
    names = [f'evidence/verification/cohort{cohort}-committed-source-inputs-v{version}-{date}.json'
             for version, date in [(14, '20261105'), (8, '20261101'), (7, '20261101'), (6, '20261101')]]
    audit = next((ROOT / name for name in names if (ROOT / name).is_file()), None)
    assert audit is not None
    matches = [item for item in closure['reports'] if item['path'] == audit.relative_to(ROOT).as_posix()]
    assert len(matches) == 1 and matches[0]['sha256'] == sha256(audit)
    assert read_json(audit)['passed'] is True
    return audit
