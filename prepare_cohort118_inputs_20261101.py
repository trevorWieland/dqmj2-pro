from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    local = ['qualify_windows_itcm_shared_data72_20261101.py',
        'catalogue_windows_native_call_types111_20261101.py',
        'measure_windows_qualified_alias_candidates111_20261101.py',
        'link_windows_qualified_aliases111_20261101.py',
        'docs/2026-11-01-windows-shared-data72.md',
        'docs/2026-11-01-windows-native-call-types.md',
        'docs/2026-11-01-windows-qualified-function-aliases.md',
        'evidence/attempts/windows-shared-data72-first-namespace-failure-20261101.json', Path(__file__).name]
    patterns = ['windows-itcm-shared-data72-20261101.json',
        'windows-host-arm9-shared-data72-link-diagnostic-20261101.txt.gz',
        'windows-native-call-types111*20261101*',
        'windows-qualified-alias111*20261101*']
    for pattern in patterns:
        local.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / 'evidence/portability').glob(pattern) if path.is_file())
    for folder in ['generated/portability/20261101-shared-data72',
            'evidence/attempts/windows-qualified-alias111-first-scalar-normalization-20261101']:
        local.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).rglob('*') if path.is_file())
    manifest = 'provenance/windows-native-typed-alias-frontier-ready-20261101.json'
    write_json(ROOT / manifest, dict(sourceCredit=0, fullWindowsGameProven=False, nativeExecutionCount=0,
        qualifiedAliasesApplied=1760, remainingHostUndefinedNames=7116,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(set(local))]))
    manifests = ['provenance/handoffs/ov001-prepare622-row-preparation-20261101.json',
        'provenance/handoffs/ov001-scalar626-double-word-producer-20261101.json',
        'provenance/handoffs/ov006-record610-functional-source-20261101.json',
        'evidence/lanes/save-core/larger-frontier148-152-ready-20261101.json',
        'evidence/lanes/save-core/binary64-frontier153-155-ready-20261101.json',
        'evidence/lanes/save-core/width-forward156-159-ready-20261101.json', manifest]
    counts = {}
    for name in manifests:
        fields = {}
        for field, rows in read_json(ROOT / name).items():
            if ('required' in field.lower() or 'existing' in field.lower()) and isinstance(rows, list):
                if not all(isinstance(row, dict) and 'path' in row and 'sha256' in row for row in rows):
                    continue
                for row in rows:
                    assert sha256(ROOT / row['path']) == row['sha256'], row['path']
                fields[field] = len(rows)
        counts[name] = fields
    write_json(ROOT / 'evidence/verification/cohort118-worker-existing-inputs-20261101.json',
        dict(passed=True, packets=counts))
    packets = [dict(report='evidence/matches/ov001-20261101-prepare622.json',
        producer=['match_ov001_prepare622_20261101.py'], directProducer=False),
        dict(report='evidence/matches/ov001-20261101-scalar626.json',
        producer=['match_ov001_scalar626_20261101.py'], directProducer=False)]
    additions = []
    for packet in packets:
        for row in read_json(ROOT / packet['report'])['matches']:
            additions.append({key: row[key] for key in ['module', 'mode', 'address', 'bytes']})
    assert len(additions) == 2 and sum(row['bytes'] for row in additions) == 432
    specification = dict(cohort=118, previousAcceptedCohort=117, migrations=[], packets=packets,
        expectedAdditions=additions, oracles=[], postSealCommands=[['prove_ov006_record610_20261101.py'],
            ['prove_save_core_large_entry152_20261101.py'], ['prove_save_core_float_pair155_20261101.py'],
            ['prove_save_core_width_forward159_20261101.py']])
    write_json(ROOT / 'cohort118-specification-20261101.json', specification)
    prior = [read_json(ROOT / f'cohort{number}-specification-20261101.json') for number in range(114, 118)]
    write_json(ROOT / 'cohort118-prerequisite-exclusion-20261101.json', dict(sourceCredit=0,
        purpose='Pending identity exclusion only; no accepted coverage',
        packets=[packet for item in prior for packet in item['packets']],
        expectedAdditions=[row for item in prior for row in item['expectedAdditions']]))
    package = dict(cohort=118, manifests=manifests,
        archives=['ov001-prepare622-20261101', 'ov001-scalar626-20261101', 'ov006-record610-20261101',
            'save-larger-frontier148-152-20261101', 'save-binary64-153-155-20261101', 'save-width-forward156-159-20261101'],
        extra=['cohort118-specification-20261101.json', 'stage_cohort118_package_20261101.py',
            'cohort118-prerequisite-exclusion-20261101.json',
            'docs/2026-11-01-cohort118-row-preparation-and-native-link-types.md',
            'evidence/verification/cohort118-worker-existing-inputs-20261101.json',
            'evidence/verification/cohort118-identity-preflight-20261101.json'], traces=[])
    write_json(ROOT / 'cohort118-package-20261101.json', package)
    print(dict(functionCandidates=2, initializedBytes=432, rootResearchFiles=len(set(local))))


if __name__ == '__main__':
    main()
