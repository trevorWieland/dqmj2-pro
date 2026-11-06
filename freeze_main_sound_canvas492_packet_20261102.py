from project import ROOT, write_json, sha256


def main():
    names = [
        'draft_main_sound_canvas_globals_20261102.py', 'draft_main_alarm_section_global_20261102.py',
        'match_main_sound_canvas492_20261102.py', 'audit_main_sound_canvas492_interfaces_20261102.py',
        'audit_main_sound_canvas492_boundaries_20261102.py', 'freeze_main_sound_canvas492_packet_20261102.py',
        'docs/2026-11-02-main-sound-canvas492-matching.md',
        'evidence/attempts/main-sound-canvas-global-interfaces-20261102.json',
        'evidence/attempts/main-alarm-section-global-interface-20261102.json',
        'evidence/matches/main-sound-canvas492-20261102.json',
        'evidence/abi/main-sound-canvas492-source-interfaces-20261102.json',
        'evidence/abi/main-sound-canvas492-boundary-candidates-20261102.json',
        'evidence/verification/main-sound-canvas492-parent-isolated-replay-20261102.json',
    ]
    for folder in ['nonmatching/main/20261102-sound-canvas-global-interfaces',
        'nonmatching/main/20261102-alarm-section-global-interface', 'src/runtime/20261102_sound_canvas492']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).rglob('*.c')]
    names = sorted(set(names))
    assert all((ROOT / name).is_file() for name in names)
    assert all(len((ROOT / name).read_text(encoding='utf-8').splitlines()) <= 500
        for name in names if (ROOT / name).suffix in ['.c', '.py'])
    write_json(ROOT / 'provenance/main-sound-canvas492-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=4, candidateNewBytes=492, ordinaryCFunctions=4,
            actualNativeBehavioralReturns=0, originalStorageSourceCredit=0, audioExecuted=False,
            interfaceAuditPassed=True, configuredBoundaryAuditPassed=True, wholeModuleAcceptancePending=True,
            files=[dict(path=name, sha256=sha256(ROOT / name)) for name in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=4, candidateBytes=492, sourceCredit=0))


if __name__ == '__main__':
    main()
