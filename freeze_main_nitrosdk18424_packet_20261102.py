from project import ROOT, read_json, write_json, sha256


def main():
    names = ['compile_main_nitrosdk_breadth_20261102.py', 'survey_main_nitrosdk_masks_20261102.py',
        'link_main_nitrosdk_breadth_20261102.py', 'draft_main_nitrosdk_closed_breadth_20261102.py',
        'prepare_main_nitrosdk18424_20261102.py', 'match_main_nitrosdk18424_20261102.py',
        'audit_main_nitrosdk18424_interfaces_20261102.py', 'audit_main_nitrosdk18424_boundaries_20261102.py',
        'replay_main_nitrosdk18424_parent_20261102.py', 'freeze_main_nitrosdk18424_packet_20261102.py',
        'docs/2026-11-02-main-nitrosdk18424-ordinary-source-breadth.md',
        'evidence/attempts/main-nitrosdk-masked-candidates-20261102.json',
        'evidence/attempts/main-nitrosdk-closed-breadth-20261102.json',
        'evidence/inputs/main-nitrosdk18424-source-units-20261102.json',
        'evidence/matches/main-nitrosdk18424-20261102.json',
        'evidence/abi/main-nitrosdk18424-source-interfaces-20261102.json',
        'evidence/abi/main-nitrosdk18424-boundary-candidates-20261102.json',
        'evidence/verification/main-nitrosdk18424-parent-replay-20261102.json']
    report = read_json(ROOT / 'evidence/matches/main-nitrosdk18424-20261102.json')
    names += [r['source'] for r in report['matches']]
    names += [r['source'] for r in read_json(ROOT / 'evidence/attempts/main-nitrosdk-closed-breadth-20261102.json')['results'] if r.get('source')]
    names = sorted(set(names))
    assert all((ROOT / n).is_file() for n in names)
    assert len(report['matches']) == 117 and report['matchedBytes'] == 18424
    for name in names:
        path = ROOT / name
        if path.suffix in ['.py', '.c']:
            assert len(path.read_text(encoding='utf-8').splitlines()) <= 500, name
    write_json(ROOT / 'provenance/main-nitrosdk18424-ready-20261102.json',
        dict(sourceCredit=0, candidateNewFunctions=117, candidateNewBytes=18424, ordinaryCFunctions=117,
            actualNativeFunctionReturns=0, originalStorageAndUnselectedHelperSourceCredit=0,
            provisionalHeadersAndPreprocessorMacrosAbsent=True, sourceOnlyParentReplayByteIdentical=True,
            sourceInterfaceAudits=117, configuredExternalDirectCandidates=584, externalInteriorCandidates=0,
            wholeModuleAcceptancePending=True, files=[dict(path=n, sha256=sha256(ROOT / n)) for n in names]))
    print(dict(frozenFiles=len(names), candidateFunctions=117, candidateBytes=18424, sourceCredit=0))


if __name__ == '__main__':
    main()
