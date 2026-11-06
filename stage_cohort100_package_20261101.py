import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
import oracle_source_closure_20261031
import stage_verified_cohort


def main():
    manifests = [
        'provenance/arm7-child-irq-check-word-handoff-20261101.json',
        'provenance/arm7-child-alarm-handler256-handoff-20261101.json',
        'provenance/arm7-host-irq244-handoff-20261101.json',
        'provenance/handoffs/main-reward437-20261101.json',
        'evidence/lanes/save-core/controller-init102-ready-20261101.json',
        'provenance/handoffs/ov001-clamp453-20261101.json']
    extra = ['stage_cohort100_package_20261101.py', 'finish_source_package_20261101.py',
        'cohort100-specification-20261101.json', 'run_cohort_20261101_100.py', 'finalize_cohort_20261101_100.py',
        'prepare_cohort100_replay_compatibility_20261101.py', 'publish_cohort100_replay_compatibility_20261101.py',
        'reproduce_channel_parameters_closure_20261101.py',
        'reproduce_overlay_negative_scope_20261101.py', 'amend_cohort100_negative_scope_20261101.py',
        'evidence/verification/reward437-negative-scope-20261101.json',
        'evidence/verification/clamp453-negative-scope-20261101.json',
        'docs/2026-11-01-cohort100-stat-clamps-and-clean-replay-compatibility.md',
        'evidence/verification/channel67-closure-compatibility-20261101.json',
        'evidence/verification/clean-z-channel67-failure-classification-20261101.json']
    declared = []
    for manifest in manifests:
        extra.append(manifest)
        declared.extend(row['path'].replace(chr(92), '/') for row in read_json(ROOT / manifest)['files'])
    reference = read_json(ROOT / 'evidence/research/20261101-arm7-reserved-irqword-calico-reference.json')
    copied = {row['path']: row['sha256'] for row in reference['files']}
    authored = []
    for name in declared:
        path = (ROOT / name).resolve()
        assert path.is_relative_to(ROOT) and path.is_file()
        if path.relative_to(ROOT).parts[0] == 'deps':
            assert name in copied and sha256(path) == copied[name]
            continue
        assert path.relative_to(ROOT).parts[0] not in stage_verified_cohort.EXCLUDED
        assert path.suffix.lower() not in ['.bin', '.nds', '.sav', '.o', '.exe', '.dll']
        authored.append(name)
    dependency_receipt = 'evidence/verification/cohort100-copied-calico-reference-inputs-20261101.json'
    write_json(ROOT / dependency_receipt, dict(referenceManifest='evidence/research/20261101-arm7-reserved-irqword-calico-reference.json',
        referenceManifestSha256=sha256(ROOT / 'evidence/research/20261101-arm7-reserved-irqword-calico-reference.json'),
        copiedReadOnlyDependencies=[dict(path=name, sha256=digest) for name, digest in copied.items()],
        compilerInput=False, sourceCredit=0, copiedByCleanCheckoutInputSnapshot=True, dependencyFilesCommittedAsAuthoredSource=False))
    extra.extend([*authored, dependency_receipt])
    extra.extend(p.relative_to(ROOT).as_posix() for p in
        (ROOT / 'evidence/attempts/cohort100-initial-evidence-order-failure-20261101').glob('*') if p.is_file())
    labels = ['arm7-child-irq-word-root', 'arm7-child-alarm-handler256-root', 'arm7-host-irq244-root',
              'overlay-main-reward437-root', 'save-controller-init102-root', 'overlay-clamp453-root']
    archives = [p.relative_to(ROOT).as_posix() for label in labels
        for p in (ROOT / 'provenance/handoffs' / label).glob('*.json')]
    extra.extend(p.relative_to(ROOT).as_posix() for p in (ROOT / 'evidence/verification').glob('cohort100-*20261101.json'))
    assert all((ROOT / name).is_file() for name in extra)
    subprocess.run(['git', 'add', '--', *archives, *authored], cwd=ROOT, check=True)
    original = oracle_source_closure_20261031.collect

    def captured_collect():
        result = original()
        write_json(ROOT / 'evidence/verification/cohort100-captured-oracle-closure-20261031.json', result)
        return result

    oracle_source_closure_20261031.collect = captured_collect
    sys.argv = ['stage_verified_cohort.py', '--cohort', '100', '--extra', *sorted(set(extra))]
    stage_verified_cohort.main()
    subprocess.run(['git', 'add', '--', 'evidence/verification/cohort100-captured-oracle-closure-20261031.json'],
                   cwd=ROOT, check=True)


if __name__ == '__main__':
    main()
