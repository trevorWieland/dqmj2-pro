import argparse
from pathlib import Path
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure


def local(name):
    path = (ROOT / name).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Packet path escaped the private project')
    return path


def identity(row):
    return (row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('descriptor')
    options = parser.parse_args()
    descriptor_path = local(options.descriptor)
    descriptor = read_json(descriptor_path)
    target = local(descriptor['canonicalReport'])
    worker = local(descriptor['workerReport'])
    if target == worker or not target.is_relative_to(ROOT / 'evidence/matches') or target.suffix != '.json':
        raise ValueError('Canonical packet report must be a separate evidence/matches JSON')
    producer = descriptor['producer']
    if not descriptor['frozenInputs']:
        raise ValueError('Packet requires an immutable input manifest')
    executable = local(producer[0])
    if executable.suffix != '.py' or not executable.is_file():
        raise ValueError('Packet producer is not a local Python entrypoint')
    for pin in descriptor['frozenInputs']:
        if sha256(local(pin['path'])) != pin['sha256']:
            raise ValueError('Frozen packet input changed: ' + pin['path'])
    subprocess.run([sys.executable, str(executable), *producer[1:]], cwd=ROOT, check=True)
    report = read_json(worker)
    if report['romSha256'] != descriptor['romSha256']:
        raise ValueError('Replayed ROM identity differs')
    if report.get('failed') or report.get('allPassed') is False or not report.get('matches'):
        raise ValueError('Worker packet did not reproduce complete matches')
    expected = {identity(row): row for row in descriptor['identities']}
    actual = {identity(row): row for row in report['matches']}
    if len(expected) != len(descriptor['identities']) or set(actual) != set(expected) or len(actual) != len(report['matches']):
        raise ValueError('Replayed packet identity set differs')
    for key, row in actual.items():
        contract = expected[key]
        for key in ('bytes', 'source', 'sourceSha256', 'targetSha256'):
            if row[key] != contract[key]:
                raise ValueError('Replayed source/native contract differs: ' + key)
        if not row.get('exactAfterDeclaredRelocation') or not row.get('realLink', {}).get('exactCallerBytes'):
            raise ValueError('Replayed packet lacks complete matching and genuine linking')
        for field, hash_field in [('source', 'sourceSha256'), ('object', 'objectSha256')]:
            if sha256(local(row[field])) != row[hash_field]:
                raise ValueError('Fresh source/object hash differs')
        for dependency in row.get('sourceDependencies', []):
            if sha256(local(dependency['path'])) != dependency['sha256']:
                raise ValueError('Fresh source include changed')
    pins = {row['path']: row['sha256'] for row in report.get('generatorSources', [])}
    for name in code_closure([producer[0], Path(__file__).name]):
        digest = sha256(local(name))
        if name in pins and pins[name] != digest:
            raise ValueError('Producer implementation changed: ' + name)
        pins[name] = digest
    pins[descriptor_path.relative_to(ROOT).as_posix()] = sha256(descriptor_path)
    for pin in descriptor['frozenInputs']:
        if sha256(local(pin['path'])) != pin['sha256']:
            raise ValueError('Packet producer changed an immutable input')
        pins[pin['path']] = pin['sha256']
    report.update(generatorSources=[dict(path=path, sha256=digest) for path, digest in sorted(pins.items())],
        canonicalPacketDescriptor=options.descriptor, workerReport=descriptor['workerReport'],
        trueProducer=producer, canonicalReportRefreshedFromFreshWorkerObjects=True,
        sourceCreditPendingSharedAcceptance=True)
    write_json(target, report)
    print(dict(report=descriptor['canonicalReport'], functions=len(actual),
        bytes=sum(row['bytes'] for row in actual.values()), canonicalObjectsRefreshed=True))


if __name__ == '__main__':
    main()
