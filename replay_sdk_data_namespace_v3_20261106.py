import copy
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, sha256, write_json
from seal_recovery_evidence_20261031 import code_closure


def project(report, descriptor):
    assert descriptor['sourceCredit'] == 0 and descriptor['namespaceTransportOnly'] is True
    assert report['functionMatched'] == 0 and report['functionMatches'] == []
    assert not report.get('matches') and not report.get('nativeSymbols')
    namespace = descriptor['namespace']
    assert set(namespace) == {'program', 'processor', 'module'}
    assert namespace['processor'] in ['arm9', 'arm7']
    selected = [copy.deepcopy(row) for row in report['dataMatches']
                if all(row[key] == value for key, value in namespace.items())]
    assert selected and len(selected) == descriptor['objects']
    assert sum(row['bytes'] for row in selected) == descriptor['initializedBytes']
    assert all(row['kind'] == 'data' and row['exactBytes'] is True for row in selected)
    assert len({(r['program'], r['processor'], r['module'], r['address']) for r in selected}) == len(selected)
    result = copy.deepcopy(report)
    result.update(namespace)
    result['dataMatches'] = selected
    result['dataMatchedBytes'] = sum(row['bytes'] for row in selected)
    result.pop('replayCodeSeal', None)
    assert result['dataMatches'] == [row for row in report['dataMatches']
                                   if all(row[key] == value for key, value in namespace.items())]
    result['sdkDataNamespaceTransport'] = dict(sourceCredit=0, namespace=namespace,
        originalReport=descriptor['originalReport'], originalReportSha256=sha256(ROOT / descriptor['originalReport']),
        wholeRowsUnchanged=True, sourceObjectFlagsRelocationsAndNativeProofsUnchanged=True,
        originalCompleteAggregateControlsRetained=True,
        reason='Existing ARM9 and embedded linkers route homogeneous reports by top-level program and processor')
    return result


def main():
    assert len(sys.argv) == 2
    name = sys.argv[1]
    descriptor = read_json(ROOT / name)
    old = descriptor['originalRegistrationTransport']
    assert sha256(ROOT / old) == descriptor['originalRegistrationTransportSha256']
    assert read_json(ROOT / old)['output'] == descriptor['originalReport']
    subprocess.run([sys.executable, str(ROOT / 'replay_sdk_data_registration_v2_20261106.py'), old], cwd=ROOT, check=True)
    report = project(read_json(ROOT / descriptor['originalReport']), descriptor)
    pins = {row['path']: row['sha256'] for row in report['generatorSources']}
    for path in code_closure([Path(__file__).name]):
        assert path not in pins or pins[path] == sha256(ROOT / path)
        pins[path] = sha256(ROOT / path)
    report['generatorSources'] = [dict(path=p, sha256=h) for p, h in sorted(pins.items())]
    dependencies = {row['path']: row['sha256'] for row in report['replayDependencies']}
    dependencies[name] = sha256(ROOT / name)
    report['replayDependencies'] = [dict(path=p, sha256=h) for p, h in sorted(dependencies.items())]
    write_json(ROOT / descriptor['output'], report)
    print(dict(passed=True, namespace=descriptor['namespace'], objects=len(report['dataMatches']),
               initializedBytes=report['dataMatchedBytes'], sourceCredit=0))


if __name__ == '__main__':
    main()
