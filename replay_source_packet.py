import argparse
import copy
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from seal_recovery_evidence_20261031 import code_closure
from source_packet_contracts import local, pin, producer_command, validate_rows

def replay(descriptor_name, refresh=True):
    path = local(descriptor_name)
    descriptor = read_json(path)
    worker = local(descriptor['workerReport'] if refresh else descriptor['initialReport'])
    target = local(descriptor['canonicalReport'], existing=False)
    expected_target = f'evidence/matches/cohort{descriptor["cohort"]}-packet-{descriptor["packetId"]}.json'
    if descriptor['canonicalReport'] != expected_target:
        raise ValueError('Canonical packet target differs from its cohort identity')
    if target in (worker, local(descriptor['initialReport'])) or not target.is_relative_to(ROOT / 'evidence/matches'):
        raise ValueError('Canonical packet requires a separate evidence report')
    producer = producer_command(descriptor['producer'], sys.executable)
    pins = {}
    for item in descriptor['frozenInputs']:
        pin(item['path'], item['sha256'])
        pins[item['path']] = item['sha256']
    if not pins:
        raise ValueError('Immutable source packet inputs required')
    if refresh:
        subprocess.run([sys.executable, str(local(producer[0])), *producer[1:]], cwd=ROOT, check=True)
    else:
        pin(descriptor['initialReport'], descriptor['initialReportSha256'])
    report = read_json(worker)
    if report['romSha256'] != descriptor['romSha256']:
        raise ValueError('Source packet ROM namespace differs')
    rows, routes = validate_rows(report, descriptor['identities'])
    result = copy.deepcopy(report)
    result['matches'] = [row for row in rows if row.get('kind') != 'data']
    if any(row.get('kind') == 'data' for row in rows):
        result['dataMatches'] = [row for row in rows if row.get('kind') == 'data']
    for item in report.get('generatorSources',[]):
        pin(item['path'], item['sha256'])
        if item['path'] in pins and pins[item['path']] != item['sha256']:
            raise ValueError('Conflicting source generator pins')
        pins[item['path']] = item['sha256']
    for name in code_closure([producer[0], 'replay_source_packet.py']):
        digest = sha256(local(name))
        if name in pins and pins[name] != digest:
            raise ValueError('Frozen source producer implementation differs')
        pins[name] = digest
    for item in descriptor['frozenInputs']:
        pin(item['path'], item['sha256'])
    pins[path.relative_to(ROOT).as_posix()] = sha256(path)
    metadata_only = descriptor['route'] == 'metadata-compiler-profile'
    result.update(generatorSources=[dict(path=name,sha256=value) for name,value in sorted(pins.items())],
        canonicalPacketDescriptor=descriptor_name, trueProducer=producer,
        originalIntake=descriptor['originalIntake'], canonicalAdapterRoutes=routes,
        canonicalReportRefreshedFromFreshWorkerObjects=bool(refresh and not metadata_only),
        originalFrozenWorkerObjectPreserved=bool(not refresh or metadata_only),
        metadataAdapterCompilerOrCpuOracleRerun=False if metadata_only else None,
        sourceCreditPendingSharedAcceptance=True)
    write_json(target, result)
    return dict(report=descriptor['canonicalReport'], functions=len(result['matches']),
        dataObjects=len(result.get('dataMatches',[])), producerExecuted=refresh,
        canonicalObjectsRefreshed=bool(refresh and not metadata_only), registered=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('descriptor')
    parser.add_argument('--existing', action='store_true')
    args = parser.parse_args()
    print(replay(args.descriptor, not args.existing))

if __name__ == '__main__':
    main()
