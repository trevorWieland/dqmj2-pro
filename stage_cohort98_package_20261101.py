import subprocess
import sys
from project import ROOT, read_json, write_json
import oracle_source_closure_20261031
import stage_verified_cohort


def main():
    manifests = [
        'evidence/lanes/save-core/lookup-node-ready-20261031.json',
        'evidence/lanes/save-core/linked-caller-ready-20261031.json',
        'provenance/arm7-child-irq-mask168-handoff-20261101.json',
        'provenance/handoffs/ghidra429-actor434-20261031.json']
    extra = ['prepare_source_cohort_20261101.py', 'publish_source_cohort_20261101.py',
        'cohort98-specification-20261101.json', 'run_cohort_20261031_98.py', 'finalize_cohort_20261031_98.py',
        'stage_cohort98_package_20261101.py', 'compile_allocation_ports_20261031.py',
        'verify_windows_allocation_ports_20261031.py', 'reject_heap_search_drafts_20261101.py',
        'qualify_heap_search_drafts_20261031.py', 'main_heap_search_fixture_20261031.py',
        'qualify_heap_commit_draft_20261101.py', 'main_heap_commit_fixture_20261101.py',
        'qualify_connected_heap_drafts_20261101.py', 'main_heap_connected_fixture_20261101.py',
        'qualify_heap_commit_measured_views_20261101.py', 'qualify_connected_heap_measured_views_20261101.py',
        'docs/2026-11-01-cohort98-allocation-and-draft-validation.md',
        'evidence/attempts/main-heap-search-behavior-qualified-drafts-20261031.json',
        'evidence/attempts/main-heap-search-negative-controls-20261101.json',
        'evidence/attempts/main-heap-commit-behavior-qualified-draft-20261101.json',
        'evidence/attempts/main-connected-heap-behavior-qualified-drafts-20261101.json',
        'evidence/attempts/main-heap-commit-measured-views-behavior-qualified-draft-20261101.json',
        'evidence/attempts/main-connected-heap-measured-views-behavior-qualified-drafts-20261101.json',
        'evidence/attempts/main-heap-commit-draft-profiles-20261101.json',
        'evidence/attempts/main-heap-commit-bitfield-views-20261101.json',
        'evidence/attempts/main-heap-commit-read-views-20261101.json',
        'evidence/attempts/main-heap-commit-group-views-20261101.json',
        'evidence/attempts/main-heap-commit-group-live-20261101.json',
        'evidence/portability/allocation-build-20261031.json',
        'evidence/portability/windows-allocation-execution-20261031.json']
    for manifest in manifests:
        extra.append(manifest)
        for item in read_json(ROOT / manifest)['files']:
            extra.append(item['path'])
    labels = ['save-lookup-node-root', 'save-linked-caller-root', 'arm7-child-irq-mask168-root',
              'overlay-ghidra-actor-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
        for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    for folder in ['src/runtime/20261031_heap_block_search', 'src/runtime/20261101_heap_block_commit',
                   'src/runtime/20261101_heap_block_commit_measured_views',
                   'generated/heap-search-negative-20261101', 'generated/heap-commit-negative-20261101',
                   'generated/heap-commit-views-20261101', 'generated/heap-commit-read-views-20261101',
                   'generated/heap-commit-group-views-20261101', 'generated/heap-commit-group-live-20261101']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*') if p.is_file())
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/verification').glob('cohort98-*20261101.json'))
    assert all((ROOT / name).is_file() for name in extra)
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    original = oracle_source_closure_20261031.collect

    def captured_collect():
        result = original()
        write_json(ROOT / 'evidence/verification/cohort98-captured-oracle-closure-20261031.json', result)
        return result

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', '98', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', 'evidence/verification/cohort98-captured-oracle-closure-20261031.json'],
                   cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
