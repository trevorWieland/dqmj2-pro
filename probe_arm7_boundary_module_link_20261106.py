from project import ROOT, read_json, write_json, sha256, configuration, native_dependencies, now
from source_dependencies import dependencies_current
import link_arm7
from unittest.mock import patch


def main():
    config = configuration()
    native_dependencies(config)
    candidate_path = ROOT / 'work/w5ab-source/genuine-qualified-second/row.json'
    candidate = read_json(candidate_path)
    candidate_hash = sha256(candidate_path)
    assert (candidate['program'], candidate['processor'], candidate['module'], candidate['mode'],
            int(candidate['address'], 0), candidate['bytes']) == ('', 'arm7', 'arm7-main', 'arm', 0x027e0898, 4464)
    assert candidate['targetSha256'] == 'acb3b83aa6853d01ac2efc2a06b7dc16b8c9b49935bf1886ede49c0d7c55f30c'
    assert candidate['exactAfterDeclaredRelocation'] and candidate['realLink']['exactCallerBytes']
    assert dependencies_current(candidate, candidate)
    for key in ('source', 'object'):
        assert sha256(ROOT / candidate[key]) == candidate[key + 'Sha256']
    protected = ['recovery.json', 'source-preferences.json', 'link_arm7.py',
                 'link_arm7_bulk_20261030.py', 'project.json']
    protected = {name: sha256(ROOT / name) for name in protected if (ROOT / name).is_file()}
    functions, symbols = link_arm7.accepted()
    assert not any(row['module'] == 'arm7-main' and int(row['address'], 0) < 0x027e1a08 and
                   int(row['address'], 0) + row.get('bytes', row.get('size')) > 0x027e0898 for row in functions)
    for name, row in candidate['nativeSymbolEntries'].items():
        address = int(row['address'], 0)
        assert row['program'] == '' and row['processor'] == 'arm7'
        if row['kind'] == 'function':
            assert row['mode'] == 'arm' and address & 3 == 0
        assert name not in symbols or int(symbols[name], 0) == address
        symbols[name] = hex(address)
    module = next(row for row in read_json(ROOT / 'evidence/arm7/runtime-layout.json')['modules']
                  if row['name'] == 'arm7-main')
    output = ROOT / 'work/arm7-boundary-module-preflight-20261106'
    def private_failure(path, value):
        assert path == ROOT / 'evidence/linking/arm7-failed-module.json'
        write_json(output / 'failed-module.json', value)
    with patch.object(link_arm7, 'write_json', side_effect=private_failure):
        result, units = link_arm7.build_module(module, functions + [candidate], symbols, config, output_root=output)
    added = [row for row in units if row['start'] == candidate['address']]
    assert len(added) == 1 and added[0]['compiledBytes'] == 4464
    assert result['exactBytes'] and result['symbolCheckPassed']
    assert protected == {name: sha256(ROOT / name) for name in protected}
    assert sha256(candidate_path) == candidate_hash
    receipt = dict(passed=True, sourceCredit=0, acceptedBytes=0, createdUtc=now(),
                   generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__),
                   candidate=candidate_path.relative_to(ROOT).as_posix(), candidateSha256=sha256(candidate_path),
                   candidateBytes=4464, candidateTargetSha256=candidate['targetSha256'],
                   originalGlobalLinkerUnchanged=True, registryAndPreferencesUnchanged=True,
                   scaffoldingAssisted=True, wholeCleanSourceReplay=False, protectedInputs=protected,
                   moduleResult=result, uncreditedCandidateSourceUnit=added[0])
    write_json(ROOT / 'evidence/lanes/parallel-wave20261105/arm7-boundary-next/coordinator-module-preflight.json', receipt)
    print(dict(passed=True, module=module['name'], candidateBytes=4464, sourceCredit=0))


if __name__ == '__main__':
    main()
