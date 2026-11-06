from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    local = ['inspect_windows_native_link_frontier111_20261101.py',
        'reconcile_windows_link_frontier_comdat_v2_20261101.py',
        'isolate_windows_selected_functions111_20261101.py',
        'measure_windows_selected_link_frontier111_v3_20261101.py',
        'attempt_windows_selected_program_links111_20261101.py',
        'probe_main_signed_double_chain601_20261101.py',
        'verify_windows_packed_word544_20261101.py',
        'ports/windows-native/packed_word544_runner_20261101.c',
        'evidence/abi/main-signed-double-chain601-20261101.json',
        'evidence/generated/main-signed-double-chain601-native-20261101.json.gz',
        'evidence/attempts/signed-double601-probe-initial-failures-20261101.json',
        'docs/2026-11-01-signed-double601-chain.md',
        'docs/2026-11-01-windows-selected-link-frontier.md',
        'docs/2026-11-01-windows-packed-word544.md', Path(__file__).name]
    directory = ROOT / 'evidence/portability'
    patterns = ['windows-native-link-frontier111*20261101*',
        'windows-selected-functions111-20261101.json',
        'windows-selected-link-frontier111-v3*20261101*',
        'windows-selected-program-links111-20261101.json',
        'windows-program-link111*diagnostic-20261101.txt.gz',
        'packed-word544-windows32-20261101.json']
    for pattern in patterns:
        local.extend(path.relative_to(ROOT).as_posix() for path in directory.glob(pattern) if path.is_file())
    for folder in ['generated/portability/20261101-selected-windows-functions',
            'evidence/attempts/windows-program-link111-first-diagnostic-classification-20261101']:
        local.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).rglob('*') if path.is_file())
    manifest = 'provenance/windows-selected-build-and-signed-double601-ready-20261101.json'
    write_json(ROOT / manifest, dict(sourceCredit=0, nativeGameExecutionCount=0,
        isolatedSourceUnits=247, nativeWord544UniqueContexts=2560,
        fullNativeLinksSucceeded=0, fullWindowsGameProven=False,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(set(local))]))
    manifests = ['evidence/lanes/save-core/table-leaves147-ready-20261101.json',
        'evidence/lanes/save-core/table-inverse146-ready-20261101.json',
        'provenance/arm7-spi-dummy72-handoff-20261101.json',
        'provenance/arm7-main-bitfields544-handoff-20261101.json',
        'provenance/arm7-main-spi-two156-handoff-20261101.json',
        'provenance/arm7-main-spi-write536-functional-handoff-20261101.json',
        'evidence/lanes/save-core/breadth144-pointer145-ready-20261101.json', manifest]
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
    write_json(ROOT / 'evidence/verification/cohort117-worker-existing-inputs-20261101.json',
        dict(passed=True, packets=checks))
    definitions = [('mechanics-save-20261101-lane-table-leaves', 'match_mechanics_save_20261101_lane_table_leaves.py', False),
        ('mechanics-save-20261101-lane-table-inverse', 'match_mechanics_save_20261101_lane_table_inverse.py', False),
        ('arm7-spi-dummy72-20261101', 'match_arm7_spi_dummy72_20261101.py', True),
        ('arm7-main-bitfields544-20261101', 'match_arm7_main_bitfields544_20261101.py', True),
        ('arm7-main-spi-two156-20261101', 'match_arm7_main_spi_two156_20261101.py', True)]
    packets, additions = [], []
    for name, producer, direct in definitions:
        report = f'evidence/matches/{name}.json'
        assert (ROOT / producer).is_file()
        packets.append(dict(report=report, producer=[producer], directProducer=direct))
        for row in read_json(ROOT / report)['matches']:
            additions.append({key: row[key] for key in ['module', 'mode', 'address', 'bytes']})
    assert len(additions) == 8 and sum(row['bytes'] for row in additions) == 912
    specification = dict(cohort=117, previousAcceptedCohort=116, migrations=[], packets=packets,
        expectedAdditions=additions, postSealCommands=[['validate_arm7_main_spi_write536_functional_20261101.py'],
            ['probe_main_signed_double_chain601_20261101.py']], oracles=[
            dict(report=f'evidence/verification/{name}-controls-20261101.json',
                reproduce=['validate_' + name.replace('-', '_') + '_20261101.py'])
            for name in ['arm7-spi-dummy72', 'arm7-main-bitfields544', 'arm7-main-spi-two156']])
    specification['oracles'].append(dict(report='evidence/portability/packed-word544-windows32-20261101.json',
        reproduce=['verify_windows_packed_word544_20261101.py']))
    write_json(ROOT / 'cohort117-specification-20261101.json', specification)
    pending = [read_json(ROOT / f'cohort{number}-specification-20261101.json') for number in [114, 115, 116]]
    write_json(ROOT / 'cohort117-prerequisite-exclusion-20261101.json', dict(sourceCredit=0,
        purpose='Pending candidate exclusion only; no accepted coverage credit',
        packets=[packet for prior in pending for packet in prior['packets']],
        expectedAdditions=[row for prior in pending for row in prior['expectedAdditions']]))
    package = dict(cohort=117, manifests=manifests,
        archives=['table-leaves147-20261101', 'table-inverse146-20261101', 'arm7-spi-dummy72-20261101',
            'arm7-main-bitfields544-20261101', 'arm7-main-spi-two156-20261101',
            'arm7-main-spi-write536-20261101', 'save-breadth144-pointer145-20261101'],
        extra=['cohort117-specification-20261101.json', 'stage_cohort117_package_20261101.py',
            'cohort117-prerequisite-exclusion-20261101.json',
            'docs/2026-11-01-cohort117-packed-words-and-native-build-frontier.md',
            'evidence/verification/cohort117-worker-existing-inputs-20261101.json',
            'evidence/verification/cohort117-identity-preflight-20261101.json'], traces=[])
    write_json(ROOT / 'cohort117-package-20261101.json', package)
    print(dict(functionCandidates=8, initializedBytes=912, rootResearchFiles=len(set(local))))


if __name__ == '__main__':
    main()
