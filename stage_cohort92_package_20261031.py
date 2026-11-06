import subprocess
import sys
from project import ROOT, read_json
import stage_verified_cohort


def main():
    manifests = [
        'evidence/lanes/save-core/stride-words-ready-20261031.json',
        'evidence/lanes/save-core/masked-callers-ready-20261031.json',
        'evidence/lanes/save-core/root-initializer-ready-20261031.json',
        'provenance/arm7-child-wordpair124-handoff-20261031.json',
        'provenance/arm7-child-divide-scope-handoff-20261031.json',
        'provenance/arm7-child-record-check172-handoff-20261031.json',
        'provenance/arm7-child-halfword-bytes76-handoff-20261031.json',
        'provenance/arm7-child-crc120-handoff-20261031.json',
        'provenance/handoffs/ov001-scout340-20261031.json',
    ]
    extra = [
        'prepare_cohort_20261031_92.py', 'run_cohort_20261031_92.py', 'finalize_cohort_20261031_92.py',
        'stage_cohort92_package_20261031.py', 'match_main_halfword_zeroarg_20261031.py',
        'replay_main_profile_trials_20261031.py', 'replay_arm7_child_divide_scope_clean_20261031.py',
        'docs/2026-10-31-main-halfword-and-zero-argument.md',
        'docs/2026-10-31-cohort92-codecs-and-typed-roots.md',
        'evidence/verification/cohort92-before-adoption-20261031.json',
    ]
    for prefix in ['main-halfword-', 'main-slot-named-views-', 'main-slot-generation-', 'main-slot-pointer-argument-']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/attempts').glob(prefix + '*20261031.json'))
    for folder in ['20261031-halfword-copy-profiles', '20261031-halfword-copy-lifetimes',
                   '20261031-halfword-first-probe', '20261031-zeroarg-call', '20261031-slot-named-views',
                   '20261031-slot-generation', '20261031-slot-pointer-argument']:
        extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'nonmatching/main-runtime' / folder).rglob('*.c'))
    for manifest in manifests:
        document = read_json(ROOT / manifest)
        extra.append(manifest)
        for key in ['files', 'closure', 'requiredFiles', 'runtimeClosure']:
            values = document.get(key)
            if isinstance(values, list):
                extra.extend(item['path'] for item in values if isinstance(item, dict) and 'path' in item)
    assert all((ROOT / name).is_file() for name in extra)
    labels = ['save-stride-words-root', 'save-masked-callers-root', 'save-root-initializer-root',
              'arm7-child-wordpair124-root', 'arm7-child-divide-scope-root', 'arm7-child-record-check172-root',
              'arm7-child-halfword-bytes76-root', 'arm7-child-crc120-root', 'ov001-scout340-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
                for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    subprocess.run(['git', 'add', '--', *archives], cwd=ROOT, check=True)
    sys.argv = ['stage_verified_cohort.py', '--cohort', '92', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()


if __name__ == '__main__':
    main()
