import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import oracle_source_closure_20261031
import stage_verified_cohort

MANIFESTS = [
    'provenance/arm7-host-gettick164-handoff-20261101.json',
    'provenance/main-sdk-lock-pair-handoff-20261101.json',
    'provenance/handoffs/ov003-wrapper477-20261101.json',
    'provenance/handoffs/ov003-reset488-20261101.json',
    'provenance/handoffs/ov003-toggle490-20261101.json',
    'provenance/handoffs/main-aux480-481-20261101.json',
    'evidence/lanes/save-core/bounded-buffer112-ready-20261101.json',
    'evidence/lanes/save-core/buffer112-default-native-ready-20261101.json',
    'evidence/lanes/save-core/mode-controller113-ready-20261101.json',
    'evidence/lanes/save-core/packed-resources114-ready-20261101.json']


def main():
    extra = [*MANIFESTS, 'cohort102-specification-20261101.json', 'stage_cohort102_package_20261101.py',
        'docs/2026-11-01-cohort102-runtime-controllers-and-sdk.md',
        'reproduce_sdk_symbol_transport_20261101.py', 'amend_cohort102_sdk_transport_20261101.py',
        'evidence/verification/sdk-lock-pair-symbol-transport-20261101.json',
        'verify_committed_source_inputs_v4_20261101.py', 'finish_source_package_v3_20261101.py',
        'publish_source_cohort_v2_20261101.py',
        'match_main_handle_refresh96_20261101.py', 'main_handle_refresh_fixture_20261101.py',
        'src/runtime/20261101_handle_refresh/native_main_020296b0.c',
        'compile_handle_refresh_ports_20261101.py', 'verify_windows_handle_refresh_20261101.py',
        'ports/runtime/handle_refresh_contract_20261101.c',
        'evidence/portability/handle-refresh-build-20261101.json',
        'evidence/portability/handle-refresh-windows-20261101.json',
        'evidence/attempts/main-handle-refresh96-bound-keyword-failure-20261101.txt',
        'launch_versioned_clean_checkout_v2_20261101.py', 'materialize_readonly_references_20261101.py',
        'evidence/verification/cohort101-tracked-readonly-references-20261101.json',
        'evidence/verification/clean-cohort101-j2p-clean-20261101-aa-launcher-20261101.json',
        'evidence/verification/clean-cohort101-j2p-clean-20261101-aa-20261101.json',
        'draft_main_breadth_small_20261101.py', 'link_main_breadth_small_20261101.py',
        'evidence/attempts/main-breadth-next17-20261101.json',
        'evidence/attempts/main-breadth-next17-genuine-links-20261101.json',
        'evidence/attempts/main-breadth-small18-20261101.json',
        'evidence/attempts/main-breadth-small18-genuine-links-20261101.json',
        'evidence/attempts/main-mmio-word-view-20261101.json',
        'nonmatching/integration/20261101-mmio-word-view/native_main_020088f8.c']
    declared, dependencies = set(), []
    for name in MANIFESTS:
        for row in read_json(ROOT / name)['files']:
            path = row['path'].replace(chr(92), '/')
            file = (ROOT / path).resolve()
            assert file.is_relative_to(ROOT) and file.is_file()
            if path.split('/')[0] in ['deps', 'tools', 'inputs']:
                assert sha256(file) == row['sha256']
                dependencies.append(dict(path=path, sha256=sha256(file)))
                continue
            assert path.split('/')[0] not in stage_verified_cohort.EXCLUDED
            assert file.suffix.lower() not in ['.bin', '.nds', '.sav', '.o', '.exe', '.dll']
            declared.add(path)
    receipt = 'evidence/verification/cohort102-copied-reference-inputs-20261101.json'
    write_json(ROOT / receipt, dict(copiedDependencies=dependencies, copiedByFreshInputSnapshot=True,
        committedAsAuthoredSource=False, sourceCredit=0))
    extra.extend([*declared, receipt])
    for folder in ['evidence/attempts/sdk-symbol-transport-20261101',
                   'evidence/attempts/cohort102-initial-symbol-format-failure-20261101',
                   'evidence/attempts/cohort102-source-input-v3-failure-20261101']:
        extra.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).glob('*') if path.is_file())
    labels = ['arm7-host-gettick164-root', 'main-sdk-lock-pair-root', 'overlay-wrapper477-root',
        'overlay-reset488-root', 'overlay-toggle490-root', 'overlay-mainaux480481-root',
        'save-bounded-buffer112-root', 'save-buffer112-default-root', 'save-mode-controller113-root',
        'save-packed-resources114-root']
    for label in labels:
        folder = ROOT / 'provenance/handoffs' / label
        assert folder.is_dir()
        extra.extend(path.relative_to(ROOT).as_posix() for path in folder.glob('*.json'))
    extra.extend(path.relative_to(ROOT).as_posix() for path in (ROOT / 'evidence/verification').glob('cohort102-*20261101.json'))
    traces = ['evidence/traces/main-handle-refresh96-20261101.json.gz']
    assert all((ROOT / name).is_file() for name in [*extra, *traces])
    subprocess.run(['git', 'add', '--', *sorted(declared), *traces], cwd=ROOT, check=True)
    original = oracle_source_closure_20261031.collect

    def captured_collect():
        result = original()
        write_json(ROOT / 'evidence/verification/cohort102-captured-oracle-closure-20261031.json', result)
        return result

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', '102', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', 'evidence/verification/cohort102-captured-oracle-closure-20261031.json'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
