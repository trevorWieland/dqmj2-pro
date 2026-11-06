import copy
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from auth_context_route_v2_20261106 import contract, validation_route, CONTRACT
import link_runtime_unit


def main():
    assert len(sys.argv) == 2
    descriptor_name = sys.argv[1]
    descriptor = read_json(ROOT / descriptor_name)
    assert descriptor['sourceCredit'] == descriptor['contextDataCredit'] == 0
    declared = contract()
    assert descriptor['contract'] == CONTRACT and sha256(ROOT / CONTRACT) == descriptor['contractSha256']
    original_descriptor = descriptor['originalReplayDescriptor']
    assert sha256(ROOT / original_descriptor) == descriptor['originalReplayDescriptorSha256']
    old = read_json(ROOT / original_descriptor)
    assert old['canonicalReport'] == declared['originalCanonicalReport']
    subprocess.run([sys.executable, str(ROOT / 'replay_parallel_packet.py'), original_descriptor], cwd=ROOT, check=True)
    report = read_json(ROOT / old['canonicalReport'])
    before = copy.deepcopy(report['matches'])
    rows = [row for row in report['matches'] if row['name'] == declared['name']]
    assert len(rows) == 1 and len(report['matches']) == 3
    row = rows[0]
    for key in ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'name', 'source', 'sourceSha256', 'object', 'objectSha256']:
        assert row[key] == declared[key]
    original_link = copy.deepcopy(row['realLink'])
    assert original_link['unchangedWholeCompilerObject'] and original_link['contextExactOriginalBytes']
    original_bindings = copy.deepcopy(row['nativeSymbolEntries'])
    assert original_bindings['.data'] == original_bindings['native_data_020deb2c']
    del row['nativeSymbolEntries']['.data']
    changes = []
    for relocation in row['relocations']:
        if relocation['symbol'] == '.data':
            assert relocation['offset'] == 156 and relocation['type'] == 2 and relocation['addend'] == 0
            assert relocation['target'] == '0x20deb2c'
            changes.append(copy.deepcopy(relocation))
            relocation['symbol'] = 'native_data_020deb2c'
    assert len(changes) == 1
    with validation_route():
        row['realLink'] = link_runtime_unit.validate(row, row['nativeSymbolEntries'],
            ROOT / 'work/integration/auth-context-canonical-v2')
    row['originalWholeCompilerContextLink'] = original_link
    row['contextReferenceNormalization'] = dict(sourceCredit=0, contextDataCredit=0,
        rawCompilerRelocations=next(r['relocations'] for r in before if r['name'] == row['name']),
        rawCompilerBindings=original_bindings, canonicalReferenceUsesActualDefinedObject=True,
        sourceCompilerObjectAndFlagsUnchanged=True, originalCompilerObjectRewritten=False,
        semanticMeaningOrProviderImplementationCredit=0)
    exempt = {'realLink', 'nativeSymbolEntries', 'relocations', 'originalWholeCompilerContextLink', 'contextReferenceNormalization'}
    for old_row, new_row in zip(before, report['matches']):
        if old_row['name'] != declared['name']:
            assert old_row == new_row
        else:
            assert {k: v for k, v in old_row.items() if k not in exempt} == {k: v for k, v in new_row.items() if k not in exempt}
    pins = {r['path']: r['sha256'] for r in report['generatorSources']}
    for path in code_closure([Path(__file__).name]):
        assert path not in pins or pins[path] == sha256(ROOT / path)
        pins[path] = sha256(ROOT / path)
    report['generatorSources'] = [dict(path=p, sha256=h) for p, h in sorted(pins.items())]
    dependencies = {r['path']: r['sha256'] for r in report.get('replayDependencies', [])}
    for name in [descriptor_name, CONTRACT, original_descriptor, declared['ready']]:
        dependencies[name] = sha256(ROOT / name)
    report['replayDependencies'] = [dict(path=p, sha256=h) for p, h in sorted(dependencies.items())]
    report.pop('replayCodeSeal', None)
    report['contextCanonicalTransport'] = dict(sourceCredit=0, contextDataCredit=0,
        originalReport=old['canonicalReport'], originalReportSha256=sha256(ROOT / old['canonicalReport']),
        contract=CONTRACT, contractSha256=sha256(ROOT / CONTRACT),
        originalWholeCompilerObjectsAndSourceAndFlagsUnchanged=True,
        otherTwoFunctionRowsUnchanged=True, normalizedActualDataObjectReferences=changes)
    write_json(ROOT / descriptor['output'], report)
    print(dict(passed=True, functions=3, bytes=sum(r['bytes'] for r in report['matches']),
               normalizedCallerBytes=192, contextDataCredit=0, sourceCredit=0))


if __name__ == '__main__':
    main()
