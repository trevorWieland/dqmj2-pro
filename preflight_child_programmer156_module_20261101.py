from project import ROOT, configuration, read_json, sha256, write_json, native_dependencies
from utility_state import runtime_state
from link_utility import accepted
from link_program import build_cpu
from link_arm7_child_alarm_programmer156_scope_20261031 import guard


def main():
    config = configuration()
    native_dependencies(config)
    assert sha256(config['linker']) == 'bd8a36a81d79af96f02fdd06e114ae97ea47acc801775a0701f93b7be139fa74'
    registry_sha = sha256(ROOT / 'recovery.json')
    path = ROOT / 'evidence/matches/arm7-child-alarm-programmer156-20261031.json'
    report = read_json(path)
    assert len(report['matches']) == 1
    row = report['matches'][0]
    guard(row)
    modules, unused, layout = runtime_state()
    functions, symbols, bindings, unused = accepted(layout['program'])
    assert not any(item['module'] == row['module'] and item['address'] == row['address'] for item in functions)
    functions.append({**report, **row})
    for name, address in report['nativeSymbols'].items():
        assert name not in symbols or int(symbols[name], 0) == int(address, 0)
        symbols[name] = address
    existing = {item['name']: item for item in bindings}
    for item in report.get('nativeSymbolBindings', []):
        assert item['program'] == layout['program']
        assert item['name'] not in existing or existing[item['name']] == item
        existing[item['name']] = item
    selected = [module for module in modules if module['processor'] == 'arm7']
    processor = next(p for p in layout['processors'] if p['processor'] == 'arm7')
    work = ROOT / 'work/child-programmer156-module-preflight-20261101'
    work.mkdir(parents=True, exist_ok=True)
    results, units = build_cpu(selected, functions, symbols, list(existing.values()), config, work, processor['resetEntry'])
    assert len(results) == 3 and all(r['exactBytes'] and r['symbolCheckPassed'] for r in results)
    assert sha256(ROOT / 'recovery.json') == registry_sha
    write_json(ROOT / 'evidence/verification/child-programmer156-module-preflight-20261101.json', dict(
        generator='preflight_child_programmer156_module_20261101.py', generatorSha256=sha256(__file__),
        sourceRegistrySha256=registry_sha, candidateReport=path.relative_to(ROOT).as_posix(),
        candidateReportSha256=sha256(path), modules=results, sourceUnits=units,
        allThreeArm7ModuleBytesAndSymbolsExact=True, candidateOrdinaryCBytes=156,
        registryChanged=False, acceptedSourceCredit=0, callbackSourceCredit=0,
        originalObjectScaffoldingStillUsed=True, initializedDenominatorDelta=0,
        limitations=['Read-only preflight adds the single validated programmer row to current accepted utility rows in memory',
            'Callback16 remains separately qualified original-gap executable code with zero recovered-source credit',
            'This does not publish the candidate, complete the executable inventory or prove a source-only game']))
    print(dict(modulesExact=3, candidateBytes=156, sourceCredit=0, callbackSourceCredit=0))


if __name__ == '__main__':
    main()
