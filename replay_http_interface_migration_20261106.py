import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


FIELDS = ['program', 'processor', 'module', 'mode', 'address', 'bytes', 'source', 'sourceSha256',
          'sourceDependencies', 'compiler', 'compilerSha256', 'compilerFlags', 'targetSha256',
          'relocations', 'nativeSymbolEntries']


def projection(report):
    return [{key: row[key] for key in FIELDS} for row in report['matches']]


def main():
    assert len(sys.argv) == 2
    descriptor_name = sys.argv[1]
    descriptor = read_json(ROOT / descriptor_name)
    assert descriptor['sourceCredit'] == descriptor['newByteCredit'] == 0
    assert sha256(ROOT / descriptor['ready']) == descriptor['readySha256']
    ready = read_json(ROOT / descriptor['ready'])
    assert ready['newByteCredit'] == ready['newFunctionCredit'] == 0 and ready['requiredPredecessor'] == 166
    assert sha256(ROOT / ready['sourceManifest']) == ready['sourceManifestSha256']
    manifest = read_json(ROOT / ready['sourceManifest'])
    for pin in manifest['files']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    subprocess.run([sys.executable, str(ROOT / ready['producer'][0]), *ready['producer'][1:]], cwd=ROOT, check=True)
    report = read_json(ROOT / ready['report'])
    assert report['allPassed'] and report['newByteCredit'] == report['newFunctionCredit'] == 0
    assert projection(report) == descriptor['immutableCallerProjection']
    assert len(report['matches']) == ready['migrationFunctions']
    identities = [{key: row[key] for key in ['program', 'processor', 'module', 'mode', 'address', 'bytes']}
                  for row in report['matches']]
    assert identities == descriptor['identities']
    for row in report['matches']:
        assert sha256(ROOT / row['object']) == row['objectSha256']
        assert row['realLink']['exactCallerBytes'] and row['ordinaryCBytes'] == row['bytes']
        assert row['justifiedAssemblyBytes'] == row['newFunctionCredit'] == row['newByteCredit'] == 0
    pins = {pin['path']: pin['sha256'] for pin in manifest['files']}
    for name in [descriptor_name, descriptor['ready'], ready['sourceManifest']]:
        pins[name] = sha256(ROOT / name)
    report['replayDependencies'] = [dict(path=name, sha256=digest) for name, digest in sorted(pins.items())]
    code = {pin['path']: pin['sha256'] for pin in report['generatorSources']}
    for name in code_closure([Path(__file__).name]):
        code[name] = sha256(ROOT / name)
    report.update(generator=Path(__file__).name, generatorSha256=sha256(__file__),
                  generatorSources=[dict(path=name, sha256=digest) for name, digest in sorted(code.items())],
                  originalProducer=ready['producer'], frozenMigrationReady=descriptor['ready'],
                  canonicalTransportOnly=True, migrationOnly=True, newSourceBytes=0)
    write_json(ROOT / descriptor['output'], report)
    print(dict(passed=True, migratedCallers=len(report['matches']), output=descriptor['output'], newByteCredit=0))


if __name__ == '__main__':
    main()
