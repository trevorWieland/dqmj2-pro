from project import ROOT, write_json, sha256


def main():
    names = [
        'draft_main_alarm_section_global_20261102.py', 'reproduce_main_alarm_section_view_20261102.py',
        'match_main_alarm72_20261102.py', 'audit_main_alarm72_interfaces_20261102.py',
        'audit_main_alarm72_boundaries_20261102.py', 'freeze_main_alarm72_packet_20261102.py',
        'docs/2026-11-02-main-alarm72-matching.md',
        'evidence/attempts/main-alarm-section-global-interface-20261102.json',
        'evidence/attempts/main-alarm-section-view-20261102.json',
        'evidence/matches/main-alarm72-20261102.json',
        'evidence/abi/main-alarm72-source-interfaces-20261102.json',
        'evidence/abi/main-alarm72-boundary-candidates-20261102.json',
        'evidence/verification/main-alarm72-parent-isolated-replay-20261102.json',
        'evidence/verification/main-alarm-section-view-reproduction-20261102.json',
    ]
    for folder in ['nonmatching/main/20261102-alarm-section-global-interface',
        'nonmatching/main/20261102-alarm-section-view', 'src/runtime/20261102_alarm72']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*.c')]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    write_json(ROOT / 'provenance/main-alarm72-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=1, candidateNewBytes=72, ordinaryCFunctions=1,
            actualNativeBehavioralReturns=0, originalStorageSourceCredit=0, audioExecuted=False,
            interfaceAuditPassed=True, configuredBoundaryAuditPassed=True, wholeModuleAcceptancePending=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=1, candidateBytes=72, sourceCredit=0))


if __name__ == '__main__':
    main()
