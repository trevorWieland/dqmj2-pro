import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-lane-node-initialization216-handoff-20261031.json',
        'evidence/lanes/save-core/initializer-query-ready-20261031.json',
        'evidence/lanes/save-core/mask-merge-ready-20261031.json',
        'provenance/handoffs/ov005-callbacks300-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_88.py', 'run_cohort_20261031_88.py', 'finalize_cohort_20261031_88.py',
        'stage_cohort88_package_20261031.py', 'adapt_ov005_callbacks300_linked_20261031.py',
        'docs/2026-10-31-cohort88-ordinary-c-and-native-dependencies.md',
        'docs/2026-10-31-main-list-loop-qualification.md',
        'docs/2026-10-31-main-context-installer-family.md',
        'docs/2026-10-31-word-stream-matching-and-port-model.md',
        'docs/2026-10-31-callbacks300-linked-comparison-adapter.md',
        'evidence/verification/cohort88-before-adoption-20261031.json',
        'evidence/attempts/cohort88-preparation-prelink-refusal-20261031.json',
        'evidence/attempts/ov005-callbacks300-adapter-base-field-failure-20261031.json',
        'replay_main_list_shapes_20261031.py', 'replay_main_list_do_shapes_20261031.py',
        'trial_main_context_declarations_20261031.py',
    ]
    for prefix in ['main-list-shapes', 'main-list-do-shapes', 'main-list-key',
                   'main-list-key-next-first', 'main-context-declarations', 'main-context-installers-preflight',
                   'main-word-stream-preflight', 'main-pcm-o3']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/attempts').glob(prefix + '*20261031.json'))
    for prefix in ['20261031-list-shapes', '20261031-list-do-shapes', '20261031-list-key',
                   '20261031-list-key-next-first', '20261031-context-declarations', '20261031-pcm-o3-expression']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'nonmatching/main-runtime' / prefix).rglob('*.c'))
    extra.extend(manifests)
    for path in manifests:
        document = read_json(ROOT / path)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            value = document.get(key)
            if isinstance(value, list):
                extra.extend(item['path'] for item in value if isinstance(item, dict) and 'path' in item)
    assert all((ROOT / path).is_file() for path in extra)
    labels = ['arm7-node-initialization216-root', 'save-initializer-query-root',
              'save-mask-merge-root', 'ov005-callbacks300-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '88', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
