from project import ROOT, read_json, write_json, sha256


def main():
    names = [
        'prepare_main_texture_pattern436_20261102.py', 'preflight_main_texture_pattern436_20261102.py',
        'main_texture_pattern436_fixture_20261102.py', 'match_main_texture_pattern436_20261102.py',
        'match_main_texture_pattern436_v2_20261102.py', 'match_main_texture_pattern436_v3_20261102.py',
        'check_main_texture_pattern436_windows32_20261102.py', 'audit_main_texture_pattern436_boundaries_20261102.py',
        'freeze_main_texture_pattern436_packet_20261102.py',
        'docs/2026-11-02-texture-pattern436-native-and-windows.md',
        'evidence/attempts/main-texture-pattern436-source-preparation-20261102.json',
        'evidence/attempts/main-texture-pattern436-preflight-20261102.json',
        'evidence/attempts/main-texture-pattern436-original-preflight-20261102.json',
        'evidence/attempts/main-texture-pattern436-wrong-key-mask-overlap-20261102.json',
        'evidence/attempts/main-texture-pattern436-negative-proof-serialization-20261102.json',
        'evidence/matches/main-texture-pattern436-v3-20261102.json',
        'evidence/ports/main-texture-pattern436-windows32-20261102.json',
        'evidence/traces/main-texture-pattern436-v3-20261102.json.gz',
        'evidence/abi/main-texture-pattern436-boundary-candidates-20261102.json',
        'evidence/verification/main-texture-pattern436-parent-isolated-replay-20261102.json',
        'evidence/verification/main-texture-pattern436-code-pool-coverage-20261102.json',
        'src/ports/20261102_texture_pattern436/driver.c',
    ]
    names += [p.relative_to(ROOT).as_posix() for p in (ROOT / 'src/runtime/20261102_texture_pattern436').glob('*.c')]
    for folder in ['20261102-texture-pattern436', '20261102-texture-pattern436-v2']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / 'nonmatching/integration' / folder).glob('*/source.c')]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    for name in names:
        path = ROOT / name
        if path.suffix in ['.py', '.c']:
            assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    write_json(ROOT / 'provenance/main-texture-pattern436-windows-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=3, candidateNewBytes=436,
            ordinaryCFunctions=3, actualNativeSourceTopReturns=6144,
            actualSelectedNestedReturns=3482, actualNativeHelperReturns=15156,
            actualWindowsPreferredReturns=3072, actualWindowsWrongReturns=3072,
            observedInstructionBytes=404, observedLiteralBytes=8, unvisitedInstructionBytes=24,
            wholeModuleAcceptancePending=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=3, candidateBytes=436, sourceCredit=0))


if __name__ == '__main__':
    main()
