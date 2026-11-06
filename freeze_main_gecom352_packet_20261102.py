from project import ROOT, write_json, sha256


def main():
    names = [
        'draft_main_sdk_uncovered1112_20261102.py',
        'repair_main_gecom_declaration_closure_20261102.py', 'repair_main_gecom_declaration_closure_v2_20261102.py',
        'draft_main_gecom352_section_view_20261102.py', 'draft_main_gecom352_section_view_v2_20261102.py',
        'match_main_gecom352_20261102.py', 'verify_main_gecom_storage_layout_20261102.py',
        'audit_main_gecom352_interfaces_20261102.py', 'audit_main_gecom352_boundaries_20261102.py',
        'freeze_main_gecom352_packet_20261102.py', 'docs/2026-11-02-main-gecom352-matching.md',
        'evidence/attempts/main-sdk-uncovered1112-closure-20261102.json',
        'evidence/attempts/main-gecom-declaration-closure-20261102.json',
        'evidence/attempts/main-gecom-declaration-closure-v2-20261102.json',
        'evidence/attempts/main-gecom352-section-view-20261102.json',
        'evidence/attempts/main-gecom352-section-view-v2-20261102.json',
        'evidence/matches/main-gecom352-20261102.json',
        'evidence/abi/main-gecom352-source-interfaces-20261102.json',
        'evidence/abi/main-gecom352-boundary-candidates-20261102.json',
        'evidence/abi/main-gecom352-original-storage-layout-20261102.json',
        'evidence/verification/main-gecom352-parent-isolated-replay-20261102.json',
    ]
    for folder in ['nonmatching/main/20261102-gecom-declaration-closure',
        'nonmatching/main/20261102-gecom-declaration-closure-v2',
        'nonmatching/main/20261102-gecom-section-view', 'nonmatching/main/20261102-gecom-section-view-v2',
        'src/runtime/20261102_gecom352']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*.c')]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    assert all(len((ROOT / name).read_text(encoding='utf-8').splitlines()) <= 500
        for name in names if (ROOT / name).suffix in ['.c', '.py'])
    write_json(ROOT / 'provenance/main-gecom352-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=3, candidateNewBytes=352, ordinaryCFunctions=3,
            actualNativeBehavioralReturns=0, originalStorageSourceCredit=0, interfaceAuditPassed=True,
            configuredBoundaryAuditPassed=True, wholeModuleAcceptancePending=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=3, candidateBytes=352, sourceCredit=0))


if __name__ == '__main__':
    main()
