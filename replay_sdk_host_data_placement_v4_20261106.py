import copy
import re
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


def placement(row, descriptor):
    assert (row['program'], row['processor'], row['module'], row['kind'], row['mode']) == ('', 'arm9', 'main', 'data', 'data')
    symbols = ROOT / 'config/arm9/symbols.txt'
    assert sha256(symbols) == descriptor['originalConfiguredSymbolsSha256']
    assert 'nativeAlias' not in row and 'nativeDataDeclaration' not in row
    address = int(row['address'], 0)
    assert address % 4 == 0 and row['bytes'] > 0 and row['exactBytes'] is True
    lines = symbols.read_text().splitlines()
    pattern = r'^(\S+) kind:([^ ]+) addr:0x' + f'{address:08x}' + r'(?:\s|$)'
    entries = [re.match(pattern, line) for line in lines if re.match(pattern, line)]
    assert len(entries) <= 1
    if entries:
        original = entries[0][1]
        assert entries[0][2].startswith('data(')
        declaration = None
    else:
        original = 'data_' + f'{address:08x}'
        assert not any(line.split()[0] == original for line in lines if line.strip())
        claim_name = descriptor['dataClaim']
        assert sha256(ROOT / claim_name) == descriptor['dataClaimSha256']
        claimed = read_json(ROOT / claim_name)['claimedStorage']
        matching = [r for r in claimed if all(r[k] == row[k] for k in ['program', 'processor', 'module', 'address', 'bytes', 'targetSha256'])]
        assert len(matching) == 1
        declaration = dict(name=original, address=hex(address), kind='data(word)')
    result = copy.deepcopy(row)
    result['nativeAlias'] = original
    if declaration:
        result['nativeDataDeclaration'] = declaration
    return result, dict(address=row['address'], bytes=row['bytes'], existingConfiguredDataSymbol=bool(entries),
        nativeAlias=original, generatedConfigOnlyDataDeclaration=declaration, sourceOrFunctionSymbolCredit=0)


def main():
    assert len(sys.argv) == 2
    name = sys.argv[1]
    descriptor = read_json(ROOT / name)
    assert descriptor['sourceCredit'] == 0 and descriptor['placementMetadataOnly']
    previous = descriptor['originalNamespaceDescriptor']
    assert sha256(ROOT / previous) == descriptor['originalNamespaceDescriptorSha256']
    subprocess.run([sys.executable, str(ROOT / 'replay_sdk_data_namespace_v3_20261106.py'), previous], cwd=ROOT, check=True)
    old = read_json(ROOT / previous)
    report = read_json(ROOT / old['output'])
    before = copy.deepcopy(report['dataMatches'])
    rows, proofs = [], []
    for row in before:
        item, proof = placement(row, descriptor)
        assert {k: v for k, v in item.items() if k not in ['nativeAlias', 'nativeDataDeclaration']} == row
        rows.append(item)
        proofs.append(proof)
    report['dataMatches'] = rows
    pins = {r['path']: r['sha256'] for r in report['generatorSources']}
    for path in code_closure([Path(__file__).name]):
        assert path not in pins or pins[path] == sha256(ROOT / path)
        pins[path] = sha256(ROOT / path)
    report['generatorSources'] = [dict(path=p, sha256=h) for p, h in sorted(pins.items())]
    deps = {r['path']: r['sha256'] for r in report['replayDependencies']}
    for path in [name, previous, descriptor['dataClaim'], 'config/arm9/symbols.txt']:
        deps[path] = sha256(ROOT / path)
    report['replayDependencies'] = [dict(path=p, sha256=h) for p, h in sorted(deps.items())]
    report['sdkHostDataPlacementTransport'] = dict(sourceCredit=0, originalReport=old['output'],
        originalReportSha256=sha256(ROOT / old['output']), initializedBytesUnchanged=True,
        originalSourceObjectCompilerFlagsAndNativeProofsUnchanged=True, placementProofs=proofs,
        generatedDataDeclarationsUseIndependentlyClaimedExactObjectBoundaries=True,
        originalConfiguredFilesUnchanged=True, actualCGlobalExportNamesUnchanged=True)
    report.pop('replayCodeSeal', None)
    write_json(ROOT / descriptor['output'], report)
    print(dict(passed=True, objects=len(rows), initializedBytes=report['dataMatchedBytes'], sourceCredit=0))


if __name__ == '__main__':
    main()
