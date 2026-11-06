from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    local = ['match_main_global_width780_20261101.py', 'main_global_width_fixture_20261101.py',
        'evidence/matches/main-global-width780-20261101.json',
        'evidence/traces/main-global-width780-20261101.json.gz',
        'docs/2026-11-01-qualified-global-width780.md', Path(__file__).name]
    for folder in ['src/runtime/20261101_global_width780',
            'nonmatching/integration/20261101-global-width-controls',
            'evidence/attempts/global-width780-initial-vector-correlation-20261101']:
        local.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).rglob('*') if path.is_file())
    manifest = 'provenance/main-global-width780-ready-20261101.json'
    write_json(ROOT / manifest, dict(newFunctionCandidates=10, newByteCandidates=780,
        actualPairedTopReturns=3840, suppliedCalleesExplicit=True, originalIrqHelpersExecuted=True,
        nativeList60Excluded=True, wholeModuleAcceptancePending=True,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(set(local))]))
    manifests = [manifest, 'provenance/handoffs/ov001-rows598-ordinary-caller-20261101.json',
        'provenance/handoffs/ov001-rows595-functional-frontier-20261101.json',
        'evidence/lanes/save-core/header-bridge143-ready-20261101.json']
    checks = {}
    for name in manifests:
        counts = {}
        for field, rows in read_json(ROOT / name).items():
            if ('required' in field.lower() or 'existing' in field.lower()) and isinstance(rows, list):
                if not all(isinstance(row, dict) and 'path' in row and 'sha256' in row for row in rows):
                    continue
                for row in rows:
                    assert sha256(ROOT / row['path']) == row['sha256'], row['path']
                counts[field] = len(rows)
        checks[name] = counts
    write_json(ROOT / 'evidence/verification/cohort116-worker-existing-inputs-20261101.json',
        dict(passed=True, packets=checks))
    packets = [dict(report='evidence/matches/main-global-width780-20261101.json',
        producer=['match_main_global_width780_20261101.py'], directProducer=False),
        dict(report='evidence/matches/ov001-20261101-rows598.json',
        producer=['match_ov001_rows598_20261101.py'], directProducer=False)]
    additions = []
    for packet in packets:
        for row in read_json(ROOT / packet['report'])['matches']:
            additions.append({key: row[key] for key in ['module', 'mode', 'address', 'bytes']})
    assert len(additions) == 11 and sum(row['bytes'] for row in additions) == 912
    specification = dict(cohort=116, previousAcceptedCohort=115, migrations=[], packets=packets,
        expectedAdditions=additions, oracles=[], postSealCommands=[
            ['prove_ov001_rows595_20261101.py'], ['prove_save_core_header_bridge143_20261101.py']])
    write_json(ROOT / 'cohort116-specification-20261101.json', specification)
    prior = [read_json(ROOT / f'cohort{number}-specification-20261101.json') for number in [114, 115]]
    write_json(ROOT / 'cohort116-prerequisite-exclusion-20261101.json', dict(sourceCredit=0,
        purpose='Pending candidate interval exclusion only; these rows do not establish acceptance',
        packets=[packet for item in prior for packet in item['packets']],
        expectedAdditions=[row for item in prior for row in item['expectedAdditions']]))
    package = dict(cohort=116, manifests=manifests,
        archives=['ov001-rows598-20261101', 'ov001-rows595-20261101', 'header-bridge143-20261101'],
        extra=['cohort116-specification-20261101.json', 'stage_cohort116_package_20261101.py',
            'cohort116-prerequisite-exclusion-20261101.json',
            'docs/2026-11-01-cohort116-width-callers-and-header-evidence.md',
            'evidence/verification/cohort116-worker-existing-inputs-20261101.json',
            'evidence/verification/cohort116-identity-preflight-20261101.json'], traces=[])
    write_json(ROOT / 'cohort116-package-20261101.json', package)
    print(dict(functionCandidates=11, initializedBytes=912, rootFiles=len(set(local))))


if __name__ == '__main__':
    main()
