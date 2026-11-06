import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


FIELDS = ['program', 'processor', 'module', 'kind', 'mode', 'address', 'bytes', 'size', 'compiledBytes',
          'source', 'sourceSha256', 'object', 'objectSha256', 'targetSha256', 'sourceDependencies',
          'compiler', 'compilerSha256', 'compilerFlags', 'encodedAssetBytes', 'measuredZeroAlignmentBytes']


def projection(report):
    assert report['functionMatched'] == 0 and report['functionMatches'] == [] and not report.get('matches')
    rows = report['dataMatches']
    assert rows and report['dataMatchedBytes'] == sum(row['bytes'] for row in rows)
    for row in rows:
        assert row['kind'] == row['mode'] == 'data'
        assert row['ordinaryFunctionCredit'] == row['executableSectionBytes'] == row['allocatedZeroFillBytes'] == 0
        assert row['relocations'] == []
    return [{key: row[key] for key in FIELDS} for row in rows]


def main():
    assert len(sys.argv) == 2
    descriptor = read_json(ROOT / sys.argv[1])
    assert descriptor['sourceCredit'] == 0 and descriptor['transportOnly'] is True
    output = (ROOT / descriptor['output']).resolve()
    assert output.is_relative_to(ROOT / 'evidence/matches')
    assert sha256(ROOT / descriptor['ready']) == descriptor['readySha256']
    ready = read_json(ROOT / descriptor['ready'])
    assert ready['functionCount'] == 0 and ready['report'] == descriptor['originalReport']
    assert ready['producer'] == descriptor['originalProducer']
    assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
    for pin in read_json(ROOT / ready['sourceManifest'])['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    subprocess.run([sys.executable, str(ROOT / ready['producer'][0]), *ready['producer'][1:]], cwd=ROOT, check=True)
    report = read_json(ROOT / ready['report'])
    assert projection(report) == descriptor['immutableDataProjection']
    pins = {row['path']: row['sha256'] for row in report['generatorSources']}
    for name in code_closure([__file__.split('\\')[-1], *[ready['producer'][0]]]):
        assert name not in pins or pins[name] == sha256(ROOT / name)
        pins[name] = sha256(ROOT / name)
    report['generatorSources'] = [dict(path=name, sha256=digest) for name, digest in sorted(pins.items())]
    dependencies = {pin['path']: pin['sha256'] for pin in report.get('replayDependencies', [])}
    for name in [sys.argv[1], descriptor['ready'], ready['sourceManifest']]:
        assert name not in dependencies or dependencies[name] == sha256(ROOT / name)
        dependencies[name] = sha256(ROOT / name)
    report['replayDependencies'] = [dict(path=name, sha256=digest) for name, digest in sorted(dependencies.items())]
    report['initializedDataTransport'] = dict(sourceCredit=0, originalReport=ready['report'],
        originalReportSha256=sha256(ROOT / ready['report']), descriptor=sys.argv[1],
        descriptorSha256=sha256(ROOT / sys.argv[1]), dataProjectionUnchanged=True,
        originalProducerUnchanged=True, originalSourceManifestSha256=ready['sourceManifestSha256'])
    write_json(output, report)
    print(dict(passed=True, dataObjects=len(report['dataMatches']), initializedBytes=report['dataMatchedBytes'],
               functionCredit=0, canonicalReport=descriptor['output'], sourceCredit=0))


if __name__ == '__main__':
    main()
