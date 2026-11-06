from project import ROOT, read_json, write_json, sha256


def main():
    names = ['externalize_sdk_storage_v1_20261102.py',
        'survey_main_nitrosdk_visibility_v1_20261102.py', 'survey_main_nitrosdk_visibility_v2_20261102.py',
        'draft_main_nitrosdk_visibility_closed_20261102.py', 'prepare_main_nitrosdk14376_20261102.py',
        'match_main_nitrosdk14376_20261102.py', 'audit_main_nitrosdk14376_interfaces_20261102.py',
        'audit_main_nitrosdk14376_boundaries_20261102.py', 'replay_main_nitrosdk14376_parent_20261102.py',
        'freeze_main_nitrosdk14376_packet_20261102.py', 'docs/2026-11-02-main-nitrosdk14376-storage-closure.md',
        'evidence/attempts/main-nitrosdk-visibility-v1-breadth-20261102.json',
        'evidence/attempts/main-nitrosdk-visibility-v2-breadth-20261102.json',
        'evidence/attempts/main-nitrosdk-visibility-v1-linked-archive-20261102.json',
        'evidence/attempts/main-nitrosdk-visibility-closed-20261102.json',
        'evidence/inputs/main-nitrosdk14376-source-units-20261102.json',
        'evidence/matches/main-nitrosdk14376-20261102.json',
        'evidence/abi/main-nitrosdk14376-source-interfaces-20261102.json',
        'evidence/abi/main-nitrosdk14376-boundary-candidates-20261102.json',
        'evidence/verification/main-nitrosdk14376-parent-replay-20261102.json',
        'evidence/verification/main-nitrosdk-visibility-mask-replay-20261102.json']
    for folder in ['src/runtime/20261102_nitrosdk14376', 'nonmatching/main/20261102-nitrosdk-visibility-closed',
        'generated/recovery/20261102-nitrosdk-visibility-archive']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob('*.c')]
    names = sorted(set(names))
    assert all((ROOT / n).is_file() for n in names)
    for name in names:
        path = ROOT / name
        if path.suffix == '.py' or path.suffix == '.c' and not name.startswith('generated/'):
            assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    report = read_json(ROOT / 'evidence/matches/main-nitrosdk14376-20261102.json')
    assert report['matchedFunctions'] == 79 and report['matchedBytes'] == 14376
    write_json(ROOT / 'provenance/main-nitrosdk14376-ready-20261102.json', dict(sourceCredit=0,
        candidateNewFunctions=79, candidateNewBytes=14376, ordinaryCFunctions=79, actualNativeFunctionReturns=0,
        sourceStorageCredit=0, generatedArchivesSourceCredit=0, provisionalHeadersAndMacrosAbsent=True,
        sourceOnlyParentReplayByteIdentical=True, configuredDirectEntryCandidates=324,
        configuredDirectInteriorCandidates=0, wholeModuleAcceptancePending=True,
        files=[dict(path=n, sha256=sha256(ROOT / n)) for n in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=79, candidateBytes=14376, sourceCredit=0))


if __name__ == '__main__':
    main()
