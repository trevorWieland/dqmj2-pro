from project import ROOT, read_json, write_json, sha256


def main():
    names = ['draft_main_nitrosdk_split788_20261102.py', 'qualify_main_fscommand400_declaration_20261102.py',
        'prepare_main_sdk1188_20261102.py', 'match_main_sdk1188_20261102.py',
        'audit_main_sdk1188_interfaces_20261102.py', 'audit_main_sdk1188_boundaries_20261102.py',
        'replay_main_sdk1188_parent_20261102.py', 'freeze_main_sdk1188_packet_20261102.py',
        'docs/2026-11-02-main-sdk1188-complete-types-and-source.md',
        'evidence/attempts/main-nitrosdk-split788-20261102.json',
        'evidence/attempts/main-fscommand400-typed-table-20261102.json',
        'evidence/attempts/main-sdk1188-profile-override-refusal-20261102.json',
        'evidence/inputs/main-sdk1188-source-units-20261102.json', 'evidence/matches/main-sdk1188-20261102.json',
        'evidence/abi/main-sdk1188-source-interfaces-20261102.json',
        'evidence/abi/main-sdk1188-boundary-candidates-20261102.json',
        'evidence/verification/main-sdk1188-parent-replay-20261102.json']
    for folder in ['src/runtime/20261102_sdk1188', 'nonmatching/main/20261102-nitrosdk-split788',
        'nonmatching/main/20261102-fscommand400-typed-table']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob('*') if p.is_file()]
    names = sorted(set(names))
    assert all((ROOT / n).is_file() for n in names)
    for name in names:
        path = ROOT / name
        if path.suffix in ['.py', '.c', '.h']: assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    report = read_json(ROOT / 'evidence/matches/main-sdk1188-20261102.json')
    assert report['matchedFunctions'] == 4 and report['matchedBytes'] == 1188
    write_json(ROOT / 'provenance/main-sdk1188-ready-20261102.json', dict(sourceCredit=0,
        candidateNewFunctions=4, candidateNewBytes=1188, ordinaryCFunctions=4, actualNativeFunctionReturns=0,
        originalStorageSourceCredit=0, provisionalHeadersAbsent=True, completeParentReplayByteIdentical=True,
        configuredDirectEntryCandidates=27, configuredDirectInteriorCandidates=0,
        wholeModuleAcceptancePending=True, files=[dict(path=n, sha256=sha256(ROOT / n)) for n in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=4, candidateBytes=1188, sourceCredit=0))


if __name__ == '__main__':
    main()
