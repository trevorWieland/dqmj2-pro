from project import ROOT, read_json, write_json, sha256


def main():
    names = [
    "prepare_main_animation_hints292_20261102.py",
    "main_animation_hints292_fixture_20261102.py",
    "main_animation_hints292_fixture_v2_20261102.py",
    "match_main_animation_hints292_20261102.py",
    "check_main_animation_hints292_windows32_20261102.py",
    "audit_main_animation_hints292_boundaries_20261102.py",
    "freeze_main_animation_hints292_packet_20261102.py",
    "docs/2026-11-02-animation-hints292-native-and-windows.md",
    "evidence/attempts/main-animation-hints292-preflight-20261102.json",
    "evidence/attempts/main-animation-hints292-original-preflight-20261102.json",
    "evidence/attempts/main-animation-hints292-map-layout-correction-20261102.json",
    "evidence/attempts/main-animation-hints292-v2-original-preflight-20261102.json",
    "evidence/matches/main-animation-hints292-20261102.json",
    "evidence/ports/main-animation-hints292-windows32-20261102.json",
    "evidence/traces/main-animation-hints292-20261102.json.gz",
    "evidence/abi/main-animation-hints292-boundary-candidates-20261102.json",
    "evidence/verification/main-animation-hints292-parent-isolated-replay-20261102.json",
    "src/ports/20261102_animation_hints292/driver.c"
]
    names += [p.relative_to(ROOT).as_posix() for p in (ROOT / "src/runtime/20261102_animation_hints292").glob("*.c")]
    names += [p.relative_to(ROOT).as_posix() for p in (ROOT / "nonmatching/integration/20261102-animation-hints292").glob("*/source.c")]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    for name in names:
        path = ROOT / name
        if path.suffix in ['.py', '.c']:
            assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    write_json(ROOT / 'provenance/main-animation-hints292-windows-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=3, candidateNewBytes=292,
            ordinaryCFunctions=3, actualNativeSourceTopReturns=6144,
            actualSelectedNestedReturns=0, actualNativeHelperReturns=5424,
            actualWindowsPreferredReturns=3072, actualWindowsWrongReturns=3072,
            observedInstructionBytes=292, observedLiteralBytes=0, unvisitedInstructionBytes=0,
            wholeModuleAcceptancePending=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=3, candidateBytes=292, sourceCredit=0))


if __name__ == '__main__':
    main()
