from project import ROOT, read_json, write_json, sha256


def main():
    names = ['draft_main_nitrosdk_split2520_20261102.py', 'prepare_main_sdk2520_20261102.py',
        'match_main_sdk2520_20261102.py', 'audit_main_sdk2520_interfaces_20261102.py',
        'audit_main_sdk2520_boundaries_20261102.py', 'replay_main_sdk2520_parent_20261102.py',
        'freeze_main_sdk2520_packet_20261102.py', 'docs/2026-11-02-main-sdk2520-complete-source.md',
        'evidence/attempts/main-nitrosdk-split2520-20261102.json',
        'evidence/inputs/main-sdk2520-source-units-20261102.json', 'evidence/matches/main-sdk2520-20261102.json',
        'evidence/abi/main-sdk2520-source-interfaces-20261102.json',
        'evidence/abi/main-sdk2520-boundary-candidates-20261102.json',
        'evidence/verification/main-sdk2520-parent-replay-20261102.json']
    for folder in ['src/runtime/20261102_sdk2520', 'nonmatching/main/20261102-nitrosdk-split2520']:
        names += [p.relative_to(ROOT).as_posix() for p in (ROOT / folder).glob('*') if p.is_file()]
    names = sorted(set(names))
    assert all((ROOT / n).is_file() for n in names)
    for name in names:
        path = ROOT / name
        if path.suffix in ['.py', '.c', '.h']: assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    report = read_json(ROOT / 'evidence/matches/main-sdk2520-20261102.json')
    assert report['matchedFunctions'] == 4 and report['matchedBytes'] == 2520
    write_json(ROOT / 'provenance/main-sdk2520-ready-20261102.json', dict(sourceCredit=0,
        candidateNewFunctions=4, candidateNewBytes=2520, ordinaryCFunctions=4, actualNativeFunctionReturns=0,
        originalStorageSourceCredit=0, completeTypedLocalHeaders=True, provisionalHeadersAbsent=True,
        completeParentReplayByteIdentical=True, configuredDirectEntryCandidates=3,
        configuredDirectInteriorCandidates=0, wholeModuleAcceptancePending=True,
        files=[dict(path=n, sha256=sha256(ROOT / n)) for n in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=4, candidateBytes=2520, sourceCredit=0))


if __name__ == '__main__':
    main()
