from project import ROOT, write_json, sha256


def main():
    names = [
        'draft_remaining_main_sdk_breadth_20261102.py',
        'match_main_sdk_breadth2236_20261102.py', 'match_main_sdk_breadth3176_20261102.py',
        'tune_main_sdk_remaining_profiles_20261102.py', 'tune_main_sdk_word_ranks_20261102.py',
        'tune_main_sdk_global_externs_20261102.py',
        'audit_main_sdk_breadth2236_interfaces_20261102.py', 'audit_main_sdk_breadth2236_boundaries_20261102.py',
        'audit_main_sdk_breadth3176_interfaces_20261102.py', 'audit_main_sdk_breadth3176_boundaries_20261102.py',
        'freeze_main_sdk_breadth3176_packet_20261102.py',
        'docs/2026-11-02-main-sdk-breadth3176-matching.md',
        'evidence/attempts/main-sdk-remaining-breadth-20261102.json',
        'evidence/attempts/main-sdk-remaining-profile-tuning-20261102.json',
        'evidence/attempts/main-sdk-word-rank-tuning-20261102.json',
        'evidence/attempts/main-sdk-global-externs-20261102.json',
        'evidence/matches/main-sdk-breadth2236-20261102.json',
        'evidence/matches/main-sdk-breadth3176-20261102.json',
        'evidence/abi/main-sdk-breadth2236-source-interfaces-20261102.json',
        'evidence/abi/main-sdk-breadth2236-boundary-candidates-20261102.json',
        'evidence/abi/main-sdk-breadth3176-source-interfaces-20261102.json',
        'evidence/abi/main-sdk-breadth3176-boundary-candidates-20261102.json',
        'evidence/verification/main-sdk-breadth3176-parent-isolated-replay-20261102.json',
    ]
    for folder in ['nonmatching/main/20261102-sdk-remaining-breadth',
        'nonmatching/main/20261102-sdk-word-ranks', 'nonmatching/main/20261102-sdk-external-global',
        'src/runtime/20261102_sdk_breadth2236', 'src/runtime/20261102_sdk_breadth3176']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob('*.c')]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    assert all(len((ROOT / name).read_text(encoding='utf-8').splitlines()) <= 500
        for name in names if (ROOT / name).suffix in ['.c', '.py'])
    write_json(ROOT / 'provenance/main-sdk-breadth3176-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=20, candidateNewBytes=3176,
            ordinaryCFunctions=20, actualNativeBehavioralReturns=0,
            interfaceAuditPassed=True, configuredBoundaryAuditPassed=True,
            wholeModuleAcceptancePending=True, inferredGameplaySemantics=False,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=20, candidateBytes=3176, sourceCredit=0))


if __name__ == '__main__':
    main()
