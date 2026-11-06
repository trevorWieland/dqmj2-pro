from unittest.mock import patch
import struct
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256


def main():
    config = configuration()
    native_dependencies(config)
    import link_arm7
    import utility_runtime
    report_name = 'evidence/data/sdk-constant-data-20261106.json'
    report = read_json(ROOT / report_name)
    selected = report['dataMatches']
    main_module = dict(next(row for row in read_json(ROOT / 'provenance/seed-manifest.json')['modules']
                            if row['name'] == 'main'), processor='arm9',
                       runtimeEntry=hex(struct.unpack_from('<I', config['rom'].read_bytes(), 0x24)[0]))
    layout, unused = utility_runtime.derive()
    child = next(row for row in layout['modules'] if row['id'] == 'utility-child-arm7-main')
    before = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', 'link_arm7.py', report_name]}
    output = ROOT / 'work/integration/sdk-constant-data-complete-module-preflight'
    output.mkdir(parents=True, exist_ok=True)
    results = []

    def private_failure(path, value):
        assert path == ROOT / 'evidence/linking/arm7-failed-module.json'
        write_json(output / 'failed-module.json', value)

    for module in [main_module, child]:
        with patch.object(link_arm7, 'write_json', side_effect=private_failure):
            result, units = link_arm7.build_module(module, selected, {}, config, output_root=output)
        assert result['exactBytes'] and result['symbolCheckPassed']
        assert result['outputSha256'] == module['sha256']
        results.append(dict(module=module['name'], sourceObjects=len(units), result=result))
    assert sum(row['sourceObjects'] for row in results) == 3
    assert before == {name: sha256(ROOT / name) for name in before}
    write_json(ROOT / 'evidence/verification/sdk-constant-data-complete-module-preflight-20261106.json',
        dict(passed=True, sourceCredit=0, sourceObjects=3, initializedBytes=562, modules=results,
             originalWholeModuleLinkerUnchanged=True, completeModuleBytesAndSymbolsExact=True,
             scaffoldingAssisted=True, protectedInputs=before, generatorSha256=sha256(__file__)))
    print(dict(passed=True, exactModules=2, sourceObjects=3, initializedBytes=562, sourceCredit=0))


if __name__ == '__main__':
    main()
