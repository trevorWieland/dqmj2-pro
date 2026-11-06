import subprocess
import sys
from project import ROOT, read_json, write_json
import oracle_source_closure_20261031
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-child-alarm-programmer156-handoff-20261101.json',
        'provenance/arm7-child-timer-callback76-handoff-20261101.json',
        'evidence/lanes/save-core/memory-init-ready-20261101.json',
        'evidence/lanes/save-core/status-inputs-ready-20261101.json',
        'provenance/handoffs/ov001-action436-functional-20261101.json']
    extra = ['prepare_source_cohort_migrations_20261101.py', 'publish_cohort99_prepared_20261101.py',
        'cohort99-specification-20261101.json', 'run_cohort_20261101_99.py', 'finalize_cohort_20261101_99.py',
        'stage_cohort99_package_20261101.py', 'finish_cohort99_package_20261101.py',
        'preflight_child_programmer156_module_20261101.py',
        'evidence/verification/child-programmer156-module-preflight-20261101.json',
        'docs/2026-11-01-cohort99-explicit-inputs-and-callback-scope.md',
        'docs/2026-11-01-application-integration-findings.md',
        'audit_small_wrapper_inputs_20261101.py',
        'make_behavior_draft_ledger_20261101.py', 'ledger/behavior-drafts-20261101.json',
        'generated/audits/wrapper-input-ledger98-20261101.json',
        'evidence/attempts/small-wrapper-input-audit-20261101.json',
        'qualify_heap_region_return_draft_20261101.py', 'main_heap_region_fixture_20261101.py',
        'reject_heap_region_return_draft_20261101.py',
        'src/runtime/20261101_heap_region_return/native_main_0202b1a8.c',
        'evidence/attempts/main-heap-region-return-draft-profiles-20261101.json',
        'evidence/attempts/main-heap-region-return-behavior-qualified-draft-20261101.json',
        'evidence/attempts/main-heap-region-return-negative-controls-20261101.json']
    for manifest in manifests:
        extra.append(manifest)
        extra.extend(item['path'] for item in read_json(ROOT / manifest)['files'])
    labels = ['arm7-child-alarm-programmer156-root', 'arm7-child-timer-callback76-root',
              'save-memory-init-root', 'save-status-inputs-root', 'overlay-action436-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
        for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/verification').glob('cohort99-*20261101.json'))
    assert all((ROOT / name).is_file() for name in extra)
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    original = oracle_source_closure_20261031.collect

    def captured_collect():
        result = original()
        write_json(ROOT / 'evidence/verification/cohort99-captured-oracle-closure-20261031.json', result)
        return result

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', '99', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', 'evidence/verification/cohort99-captured-oracle-closure-20261031.json'],
                   cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
