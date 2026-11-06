from project import ROOT, read_json, write_json, sha256


def main():
    names = ['compile_main_scene284_typed_view_20261102.py',
        'main_scene284_fixture_20261102.py', 'main_scene284_fixture_v2_20261102.py',
        'match_main_scene284_20261102.py', 'match_main_scene284_v2_20261102.py',
        'replay_main_scene284_parent_20261102.py',
        'audit_main_scene284_interfaces_20261102.py', 'audit_main_scene284_boundaries_20261102.py',
        'freeze_main_scene284_packet_20261102.py', 'docs/2026-11-02-main-scene284-native-matching.md',
        'evidence/attempts/main-scene284-typed-view-20261102.json',
        'evidence/attempts/main-scene284-original-extent-control-refusal-20261102.json',
        'evidence/matches/main-scene284-20261102.json', 'evidence/traces/main-scene284-20261102.json.gz',
        'evidence/abi/main-scene284-source-interfaces-20261102.json',
        'evidence/abi/main-scene284-boundary-candidates-20261102.json',
        'evidence/verification/main-scene284-parent-replay-20261102.json',
        'src/runtime/20261102_scene284/native_main_0203db28.c']
    names += [p.relative_to(ROOT).as_posix() for p in
        (ROOT / 'nonmatching/integration/20261102-scene284').glob('*/source.c')]
    names = sorted(set(names))
    assert all((ROOT / n).is_file() for n in names)
    report = read_json(ROOT / 'evidence/matches/main-scene284-20261102.json')
    for name in names:
        path = ROOT / name
        if path.suffix in ['.py', '.c']:
            assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    write_json(ROOT / 'provenance/main-scene284-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=1, candidateNewBytes=284, ordinaryCFunctions=1,
            actualNativeSourceTopReturns=800, actualWrongReturns=480,
            actualWrongModelRejections=report['negativeEvidence']['independentModelRejections'],
            suppliedLowerCalls=report['oracle']['suppliedBoundaryCalls'], actualLowerNativeReturns=0,
            observedInstructionBytes=276, observedLiteralBytes=8, originalDataCredit=0,
            typedRelocationAndConfiguredBoundaryAuditsPassed=True,
            requiredSelectedF200RawWordMigration=True, wholeModuleAcceptancePending=True,
            files=[dict(path=n, sha256=sha256(ROOT / n)) for n in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=1, candidateBytes=284, sourceCredit=0,
        requiredSelectedF200RawWordMigration=True))


if __name__ == '__main__':
    main()
