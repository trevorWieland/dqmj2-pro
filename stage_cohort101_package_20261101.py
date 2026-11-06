import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import oracle_source_closure_20261031
import stage_verified_cohort

MANIFESTS = [
    'provenance/arm7-child-callback16-dispatch-abi-handoff-20261101.json',
    'provenance/arm7-child-irq-dispatch260-handoff-20261101.json',
    'provenance/arm7-child-tick-callback136-handoff-20261101.json',
    'provenance/arm7-host-timer-callback76-handoff-20261101.json',
    'provenance/arm7-host-tick-callback104-handoff-20261101.json',
    'provenance/arm7-host-timer-init124-handoff-20261101.json',
    'provenance/handoffs/ov001-reward458-20261101.json',
    'provenance/handoffs/ov001-query466-20261101.json',
    'provenance/handoffs/sdk-callers467-469-20261101.json',
    'evidence/lanes/save-core/byte-sequence105-ready-20261101.json',
    'evidence/lanes/save-core/field-sentinel111-ready-20261101.json']


def main():
    extra = [*MANIFESTS, 'cohort101-specification-20261101.json', 'stage_cohort101_package_20261101.py',
        'run_source_cohort_20261101.py', 'finalize_source_cohort_20261101.py',
        'finish_source_package_v2_20261101.py',
        'launch_versioned_clean_checkout_20261101.py',
        'prepare_legacy_replay_migrations_20261101.py', 'publish_legacy_replay_migrations_20261101.py',
        'publish_prepared_source_migrations_20261101.py', 'reproduce_legacy_arm7_closures_20261101.py',
        'reproduce_channel_parameters_closure_v2_20261101.py', 'reproduce_overlay_negative_scope_v2_20261101.py',
        'verify_object_path_metadata_20261101.py', 'evidence/verification/object-path-metadata-20261101.json',
        'match_main_callback_stream220_20261101.py', 'main_callback_stream_fixture_20261101.py',
        'src/runtime/20261101_callback_stream/native_main_020316b4.c',
        'evidence/attempts/main-callback-stream220-overstrict-lr-20261101.txt',
        'evidence/attempts/main-callback-stream220-isolated-bootstrap-20261101.txt',
        'evidence/attempts/cohort101-preparation-missing-reason-20261101.txt',
        'docs/2026-11-01-cohort101-inputs-callbacks-and-portable-replay.md',
        'docs/2026-11-01-application-reward-followup.md', 'docs/2026-11-01-main-breadth14.md',
        'draft_main_breadth14_20261101.py', 'link_main_breadth14_20261101.py',
        'draft_main_breadth_next_20261101.py', 'link_main_breadth_next_20261101.py',
        'evidence/attempts/main-breadth14-20261101.json', 'evidence/attempts/main-breadth14-genuine-links-20261101.json']
    declared, copied_dependencies = set(), []
    for name in MANIFESTS:
        for row in read_json(ROOT / name)['files']:
            path = row['path'].replace(chr(92), '/')
            file = (ROOT / path).resolve()
            assert file.is_relative_to(ROOT) and file.is_file()
            if path.split('/')[0] in ['deps', 'tools', 'inputs']:
                assert sha256(file) == row['sha256']
                copied_dependencies.append(dict(path=path, sha256=sha256(file)))
                continue
            assert path.split('/')[0] not in stage_verified_cohort.EXCLUDED
            assert file.suffix.lower() not in ['.bin', '.nds', '.sav', '.o', '.exe', '.dll']
            declared.add(path)
    for batch in [15, 16]:
        for suffix in ['', '-genuine-links']:
            name = f'evidence/attempts/main-breadth-next{batch}{suffix}-20261101.json'
            assert read_json(ROOT / name)['state'] == 'finished'
            extra.append(name)
    dependency_receipt = 'evidence/verification/cohort101-copied-dependency-inputs-20261101.json'
    write_json(ROOT / dependency_receipt, dict(copiedReadOnlyDependencies=copied_dependencies,
        copiedByCleanCheckoutInputSnapshot=True, sourceCredit=0, committedAsAuthoredSource=False))
    extra.extend([*declared, dependency_receipt])
    labels = ['arm7-child-dispatch-abi-root', 'arm7-child-dispatch260-root', 'arm7-child-tick136-root',
        'arm7-host-timer76-root', 'arm7-host-tick104-root', 'arm7-host-init124-root', 'overlay-reward458-root',
        'overlay-query466-root', 'overlay-sdk467469-root', 'save-byte-sequence105-root', 'save-field-sentinel111-root']
    for label in labels:
        folder = ROOT / 'provenance/handoffs' / label
        assert folder.is_dir()
        extra.extend(p.relative_to(ROOT).as_posix() for p in folder.glob('*.json'))
    for pattern in ['cohort101-*20261101.json', 'legacy-arm7-*-closure-compatibility-20261101.json',
                    '*-negative-scope-v2-20261101.json', 'channel67-closure-v2-compatibility-20261101.json']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/verification').glob(pattern))
    traces = ['evidence/traces/main-callback-stream220-20261101.json.gz']
    assert all((ROOT / name).is_file() for name in [*extra, *traces])
    subprocess.run(['git', 'add', '--', *sorted(declared), *traces], cwd=ROOT, check=True)
    original = oracle_source_closure_20261031.collect

    def captured_collect():
        result = original()
        write_json(ROOT / 'evidence/verification/cohort101-captured-oracle-closure-20261031.json', result)
        return result

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', '101', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', 'evidence/verification/cohort101-captured-oracle-closure-20261031.json'], cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
