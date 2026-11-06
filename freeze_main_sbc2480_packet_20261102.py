from project import ROOT, write_json, sha256


def main():
    names = [
        'draft_main_sbc2480_external_storage_20261102.py', 'match_main_sbc2480_20261102.py',
        'audit_main_sbc2480_interfaces_20261102.py', 'audit_main_sbc2480_boundaries_20261102.py',
        'freeze_main_sbc2480_packet_20261102.py', 'docs/2026-11-02-main-sbc2480-matching.md',
        'reproduce_main_sbc_environment_section_view_20261102.py',
        'evidence/verification/main-sbc-environment-section-view-reproduction-20261102.json',
        'evidence/attempts/main-sbc2480-external-storage-20261102.json',
        'evidence/attempts/main-sbc-environment-section-view-20261102.json',
        'evidence/matches/main-sbc2480-20261102.json',
        'evidence/abi/main-sbc2480-source-interfaces-20261102.json',
        'evidence/abi/main-sbc2480-boundary-candidates-20261102.json',
        'evidence/verification/main-sbc2480-parent-isolated-replay-20261102.json',
    ]
    for folder in ['nonmatching/main/20261102-sbc-external-storage',
        'nonmatching/main/20261102-sbc-environment-section-view', 'src/runtime/20261102_sbc2480']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*') if p.suffix in ['.c', '.h']]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    assert all(len((ROOT / name).read_text(encoding='utf-8').splitlines()) <= 500
        for name in names if (ROOT / name).suffix in ['.c', '.h', '.py'])
    write_json(ROOT / 'provenance/main-sbc2480-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=3, candidateNewBytes=2480, ordinaryCFunctions=3,
            actualNativeBehavioralReturns=0, originalStaticStorageSourceCredit=0,
            interfaceAuditPassed=True, configuredBoundaryAuditPassed=True, wholeModuleAcceptancePending=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=3, candidateBytes=2480, sourceCredit=0))


if __name__ == '__main__':
    main()
