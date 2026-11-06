from unittest.mock import patch
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256


def main():
    config = configuration()
    native_dependencies(config)
    import utility_runtime
    import link_arm7
    names = ['evidence/data/child-message-semantic-20261106.json',
             'evidence/data/child-static-assets-next-20261105.json']
    pins = {name: sha256(ROOT / name) for name in names}
    rows = [row for name in names for row in read_json(ROOT / name)['dataMatches']]
    assert len(rows) == 45 and sum(row['bytes'] for row in rows) == 54264
    layout, unused_files = utility_runtime.derive()
    module = next(row for row in layout['modules'] if row['id'] == 'utility-child-arm9-main')
    original = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', 'link_arm7.py']}
    output = ROOT / 'work/integration/child-semantic-assets-whole-module-preflight-20261106'
    output.mkdir(parents=True, exist_ok=True)

    def private_failure(path, value):
        assert path == ROOT / 'evidence/linking/arm7-failed-module.json'
        write_json(output / 'failed-module.json', value)

    with patch.object(link_arm7, 'write_json', side_effect=private_failure):
        result, units = link_arm7.build_module(module, rows, {}, config, output_root=output)
    assert result['exactBytes'] and result['symbolCheckPassed'] and len(units) == 45
    assert result['outputSha256'] == module['sha256']
    assert original == {name: sha256(ROOT / name) for name in original}
    assert pins == {name: sha256(ROOT / name) for name in pins}
    write_json(ROOT / 'evidence/verification/child-semantic-assets-whole-module-preflight-20261106.json',
        dict(passed=True, sourceCredit=0, dataObjects=45, initializedBytes=54264,
             originalWholeModuleLinkerUnchanged=True, selectedCandidateObjectsUsedUnmodified=True,
             scaffoldAssisted=True, nativeWindowsGameProven=False, reportPins=pins,
             protectedInputs=original, module=result, generatorSha256=sha256(__file__)))
    print(dict(passed=True, exactModule=True, dataObjects=45, initializedBytes=54264, sourceCredit=0))


if __name__ == '__main__':
    main()
