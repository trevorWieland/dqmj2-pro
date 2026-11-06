from project import ROOT, read_json, write_json, sha256


def main():
    names = ['draft_main_fifo256_void_view_20261102.py', 'draft_main_fifo256_c99_ipa_20261102.py',
        'draft_main_tp256_reference_20261102.py', 'compile_main_tp256_reference_profiles_20261102.py',
        'qualify_main_tp256_measured_layout_20261102.py', 'main_tp256_fixture_20261102.py',
        'match_main_tp256_20261102.py', 'replay_main_tp256_parent_20261102.py',
        'audit_main_tp256_interfaces_20261102.py', 'audit_main_tp256_boundaries_20261102.py',
        'freeze_main_tp256_packet_20261102.py', 'docs/2026-11-02-main-tp256-native-matching.md',
        'evidence/attempts/main-fifo256-void-view-20261102.json',
        'evidence/attempts/main-fifo256-c99-ipa-20261102.json',
        'evidence/attempts/main-tp256-reference-20261102.json',
        'evidence/attempts/main-tp256-reference-profiles-20261102.json',
        'evidence/attempts/main-tp256-measured-layout-20261102.json',
        'evidence/matches/main-tp256-20261102.json', 'evidence/traces/main-tp256-20261102.json.gz',
        'evidence/abi/main-tp256-source-interfaces-20261102.json',
        'evidence/abi/main-tp256-boundary-candidates-20261102.json',
        'evidence/verification/main-tp256-parent-replay-20261102.json',
        'src/runtime/20261102_tp256/native_main_0200ded8.c']
    for folder in ['nonmatching/main/20261102-fifo256-void-view', 'nonmatching/main/20261102-fifo256-c99-ipa',
        'nonmatching/main/20261102-tp256-reference', 'nonmatching/integration/20261102-tp256']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*.c')]
    names = sorted(set(names))
    assert all((ROOT / n).is_file() for n in names)
    report = read_json(ROOT / 'evidence/matches/main-tp256-20261102.json')
    for name in names:
        path = ROOT / name
        if path.suffix in ['.py', '.c']: assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    write_json(ROOT / 'provenance/main-tp256-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=1, candidateNewBytes=256, ordinaryCFunctions=1,
            actualNativeSourceTopReturns=6720, actualWrongReturns=720, actualWrongModelRejections=467,
            suppliedLowerCalls=report['oracle']['suppliedBoundaryCalls'], actualNativeLowerReturns=0,
            observedInstructionBytes=252, observedLiteralBytes=4, originalStorageSourceCredit=0,
            sourceOnlyParentReplayByteIdentical=True, wholeModuleAcceptancePending=True,
            files=[dict(path=n, sha256=sha256(ROOT / n)) for n in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=1, candidateBytes=256, sourceCredit=0))


if __name__ == '__main__':
    main()
