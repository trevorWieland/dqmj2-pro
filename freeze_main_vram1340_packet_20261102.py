from project import ROOT, write_json, sha256


def main():
    names = [
        'draft_main_vram_globals_20261102.py', 'draft_main_vram_section_globals_20261102.py',
        'match_main_vram832_20261102.py', 'match_main_vram1340_20261102.py',
        'audit_main_vram832_interfaces_20261102.py', 'audit_main_vram832_boundaries_20261102.py',
        'audit_main_vram1340_interfaces_20261102.py', 'audit_main_vram1340_boundaries_20261102.py',
        'freeze_main_vram1340_packet_20261102.py', 'docs/2026-11-02-main-vram1340-matching.md',
        'evidence/attempts/main-vram-global-interfaces-20261102.json',
        'evidence/attempts/main-vram-section-global-interfaces-20261102.json',
        'evidence/matches/main-vram832-20261102.json', 'evidence/matches/main-vram1340-20261102.json',
        'evidence/abi/main-vram832-source-interfaces-20261102.json',
        'evidence/abi/main-vram832-boundary-candidates-20261102.json',
        'evidence/abi/main-vram1340-source-interfaces-20261102.json',
        'evidence/abi/main-vram1340-boundary-candidates-20261102.json',
        'evidence/verification/main-vram1340-parent-isolated-replay-20261102.json',
    ]
    for folder in ['nonmatching/main/20261102-vram-global-interfaces',
        'nonmatching/main/20261102-vram-section-global-interfaces',
        'src/runtime/20261102_vram832', 'src/runtime/20261102_vram1340']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*.c')]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    assert all(len((ROOT / name).read_text(encoding='utf-8').splitlines()) <= 500
        for name in names if (ROOT / name).suffix in ['.c', '.py'])
    write_json(ROOT / 'provenance/main-vram1340-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=9, candidateNewBytes=1340, ordinaryCFunctions=9,
            actualNativeBehavioralReturns=0, originalStorageSourceCredit=0, interfaceAuditPassed=True,
            configuredBoundaryAuditPassed=True, wholeModuleAcceptancePending=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=9, candidateBytes=1340, sourceCredit=0))


if __name__ == '__main__':
    main()
