from pathlib import Path
from project import ROOT, read_json, write_json, sha256


def main():
    local = ['match_main_pointer_chain9a5c_20261101.py',
        'src/runtime/20261101_list_count60/native_main_02009a5c.c',
        'evidence/matches/main-pointer-chain9a5c-20261101.json',
        'evidence/traces/main-pointer-chain9a5c-20261101.json.gz',
        'evidence/attempts/list-count-validation-name-collision-20261101.json',
        'docs/2026-11-01-word-pointer-list-count.md',
        'ports/windows-native/pointer_halfword_runner_20261101.c',
        'verify_windows_pointer_halfwords_20261101.py',
        'evidence/portability/pointer-halfwords-windows32-20261101.json',
        'docs/2026-11-01-windows-pointer-halfword-behavior.md',
        'measure_active_recovery_progress_v2_20261101.py',
        'evidence/verification/active-recovery-progress-v2-20261101.json',
        'survey_root_breadth_sp1p6_20261101.py',
        'evidence/attempts/root-breadth-sp1p6-survey-20261101.json',
        'survey_root_global_widths_20261101.py',
        'evidence/attempts/root-global-width-survey-20261101.json',
        'evidence/attempts/main-breadth-next20-20261101.json',
        'docs/2026-11-01-root-bulk-width-and-compiler-surveys.md',
        Path(__file__).name]
    for row in read_json(ROOT / 'evidence/attempts/root-global-width-survey-20261101.json')['results']:
        local.append(row['source'])
    manifest = 'provenance/main-list-count60-and-width-research-ready-20261101.json'
    write_json(ROOT / manifest, dict(newFunctionCandidates=1, newByteCandidates=60,
        exactWidthHypothesisFunctionsSeparateZeroCredit=11, nativeWindowsHalfwordContextsSeparateZeroCredit=1024,
        selectedSourcesModified=False, wholeModuleAcceptancePending=True,
        files=[dict(path=name, sha256=sha256(ROOT / name)) for name in sorted(set(local))]))
    manifests = ['provenance/arm7-main-pxi-retry64-handoff-20261101.json',
        'provenance/arm7-main-spi-fast288-handoff-20261101.json',
        'provenance/arm7-main-spi-fields272-handoff-20261101.json',
        'evidence/lanes/save-core/save-widget-exit142-ready-20261101.json', manifest]
    audit = {}
    for name in manifests:
        fields = {}
        for field, rows in read_json(ROOT / name).items():
            if 'requiredExisting' in field and isinstance(rows, list):
                for row in rows:
                    assert sha256(ROOT / row['path']) == row['sha256'], row['path']
                fields[field] = len(rows)
        audit[name] = fields
    write_json(ROOT / 'evidence/verification/cohort115-worker-existing-inputs-20261101.json',
        dict(passed=True, packets=audit))
    definitions = [('arm7-main-pxi-retry64', True, 'arm7-main', '0x27f6074', 64),
        ('arm7-main-spi-fast288', True, 'arm7-main', '0x27f56ec', 288),
        ('arm7-main-spi-fields272', True, 'arm7-main', '0x27f5a24', 136),
        ('mechanics-save-20261101-lane-save-widget-exit', False, 'main', '0x2079f9c', 36),
        ('main-pointer-chain9a5c', False, 'main', '0x2009a5c', 60)]
    packets = []
    additions = []
    for name, direct, module, address, size in definitions:
        producer = 'match_' + name.replace('-', '_') + '_20261101.py'
        if name.startswith('mechanics-save'):
            producer = 'match_mechanics_save_20261101_lane_save_widget_exit.py'
        report = 'evidence/matches/' + name + ('-20261101' if not name.startswith('mechanics-save') else '') + '.json'
        assert (ROOT / producer).is_file() and (ROOT / report).is_file()
        packets.append(dict(report=report, producer=[producer], directProducer=direct))
        additions.append(dict(module=module, mode='arm', address=address, bytes=size))
    additions.append(dict(module='arm7-main', mode='arm', address='0x27f5aac', bytes=136))
    specification = dict(cohort=115, previousAcceptedCohort=114, migrations=[], packets=packets,
        expectedAdditions=additions, postSealCommands=[], oracles=[dict(
            report=f'evidence/verification/{name}-controls-20261101.json',
            reproduce=['validate_' + name.replace('-', '_') + '_20261101.py'])
            for name in ['arm7-main-pxi-retry64', 'arm7-main-spi-fast288', 'arm7-main-spi-fields272']])
    specification['oracles'].append(dict(report='evidence/portability/pointer-halfwords-windows32-20261101.json',
        reproduce=['verify_windows_pointer_halfwords_20261101.py']))
    write_json(ROOT / 'cohort115-specification-20261101.json', specification)
    package = dict(cohort=115, manifests=manifests,
        archives=['arm7-main-pxi-retry64-20261101', 'arm7-main-spi-fast288-20261101',
            'arm7-main-spi-fields272-20261101', 'save-widget-exit142-20261101'],
        extra=['cohort115-specification-20261101.json', 'stage_cohort115_package_20261101.py',
            'docs/2026-11-01-cohort115-native-effects-and-width-frontier.md',
            'evidence/verification/cohort115-worker-existing-inputs-20261101.json',
            'evidence/verification/cohort115-identity-preflight-20261101.json'], traces=[])
    write_json(ROOT / 'cohort115-package-20261101.json', package)
    print(dict(candidates=6, initializedBytes=sum(row['bytes'] for row in additions), localFiles=len(set(local))))


if __name__ == '__main__':
    main()
