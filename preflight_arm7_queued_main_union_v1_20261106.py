from unittest.mock import patch
from project import ROOT, read_json, write_json, configuration, native_dependencies, sha256, now
import link_arm7


def main():
    names = ['cohort172-parallel-wave20261105-q-specification.json',
        'cohort173-parallel-wave20261105-r-specification.json']
    protected = {name:sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json',
        'link_arm7.py', 'link_arm7_bulk_20261030.py', 'evidence/linking/arm7-latest.json', *names]}
    functions, symbols = link_arm7.accepted()
    baseline = len(functions)
    selected = []
    for name in names:
        spec = read_json(ROOT / name)
        for packet in spec['packets']:
            report = read_json(ROOT / packet['report'])
            if report.get('processor') != 'arm7' or report.get('program'):
                continue
            assert report['allPassed']
            for row in report['matches']:
                item = dict(report, **row)
                assert item['module'] == 'arm7-main' and item['mode'] == 'arm'
                assert item['exactAfterDeclaredRelocation'] and item['realLink']['exactCallerBytes']
                for key in ['source', 'object']:
                    assert sha256(ROOT / item[key]) == item[key + 'Sha256']
                selected.append(item)
            for symbol, address in report['nativeSymbols'].items():
                assert symbol not in symbols or int(symbols[symbol],0) == int(address,0)
                symbols[symbol] = address
    assert len(selected) == 48 and sum(r['bytes'] for r in selected) == 11984
    functions.extend(selected)
    identities = [(r['module'], int(r['address'],0)) for r in functions]
    assert len(identities) == len(set(identities))
    config = configuration()
    native_dependencies(config)
    module = next(r for r in read_json(ROOT / 'evidence/arm7/runtime-layout.json')['modules'] if r['name'] == 'arm7-main')
    output = ROOT / 'work/arm7-queued-main-union-preflight-v1-20261106'
    def private_failure(path, value):
        assert path == ROOT / 'evidence/linking/arm7-failed-module.json'
        write_json(output / 'failed-module.json', value)
    with patch.object(link_arm7, 'write_json', side_effect=private_failure):
        result, units = link_arm7.build_module(module, functions, symbols, config, output_root=output)
    assert result['exactBytes'] and result['symbolCheckPassed']
    assert protected == {name:sha256(ROOT / name) for name in protected}
    receipt = dict(passed=True, sourceCredit=0, createdUtc=now(), baselineFunctions=baseline,
        queuedFunctions=len(selected), queuedBytes=sum(r['bytes'] for r in selected),
        unchangedOriginalModuleBuilder=True, originalRegistryAndLinkReportsUnchanged=True,
        scaffoldedModule=True, cleanSourceOnlyModule=False, moduleResult=result,
        allSourceUnits=units, protectedInputs=protected, generatorSha256=sha256(__file__))
    write_json(ROOT / 'evidence/verification/cohort172-173-arm7-main-union-preflight-v1-20261106.json', receipt)
    print(dict(passed=True, queuedFunctions=len(selected), queuedBytes=sum(r['bytes'] for r in selected),
        completeModuleBytes=module['bytes'], strictSymbolChecks=True, sourceCredit=0))


if __name__ == '__main__':
    main()
