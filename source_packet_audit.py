import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def local(name):
    path = (ROOT / name.replace('\\', '/')).resolve()
    if not path.is_relative_to(ROOT) or not path.is_file():
        raise ValueError('Missing or escaping input: ' + name)
    return path

def identity(row):
    return (row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0))

def snapshot_link(row, pin):
    snapshot = row.get('realLinkSnapshot')
    if not snapshot or not row.get('exactByteEqual') or not row.get('genuineMWLinked'):
        raise ValueError('Nonmatching row cannot enter acceptance: ' + row['name'])
    if row.get('program') or row['processor'] != 'arm9' or row['mode'] != 'arm':
        raise ValueError('Native snapshot schema currently supports host ARM9 ARM only')
    for name in ('isolatedCallerBinary', 'isolatedCallerLinkValidation', 'isolatedCallerLinkSnapshotManifest',
                 'isolatedCallerLinkedElf', 'isolatedCallerLinkLcf'):
        pin(snapshot[name], snapshot[name + 'Sha256'])
    manifest = read(local(snapshot['isolatedCallerLinkSnapshotManifest']))
    proof = read(local(snapshot['isolatedCallerLinkValidation']))
    for record in manifest['artifacts']:
        pin(record['path'], record['sha256'])
    for field in ('name','module','processor','address','bytes','sourceSha256'):
        if proof[field] != row[field]:
            raise ValueError('Native snapshot identity differs: ' + field)
    if not proof['exactCallerBytes'] or proof['sourceObjectSha256'] != row['objectSha256']:
        raise ValueError('Native snapshot source object differs')
    if proof['linkedCallerSha256'] != row['targetSha256'] or proof['nativeSpanSha256'] != row['targetSha256']:
        raise ValueError('Native snapshot target differs')
    binary = local(snapshot['isolatedCallerBinary']).read_bytes()
    if len(binary) != row['bytes'] or hashlib.sha256(binary).hexdigest() != row['targetSha256']:
        raise ValueError('Native snapshot output extent differs')
    if proof['linkerAttempt']['exitCode'] != 0:
        raise ValueError('Native snapshot linker failed')
    return 'verified-native-snapshot-needs-canonical-schema-adapter'

def audit(config):
    revision = config['baselineRevision']
    ledger_bytes = subprocess.check_output(['git', 'show', revision + ':ledger/functions.jsonl'], cwd=ROOT)
    if (ROOT / 'ledger/functions.jsonl').read_bytes() != ledger_bytes:
        raise ValueError('Live function ledger differs from the committed baseline')
    ledger = [json.loads(line) for line in ledger_bytes.splitlines()]
    accepted = {identity(row): row for row in ledger if row['states']['functionMatched']}
    pins, packets, rows, seen = {}, [], [], set()
    def pin(name, expected):
        path = local(name)
        name = path.relative_to(ROOT).as_posix()
        actual = pins.setdefault(name, digest(path))
        if actual != expected:
            raise ValueError('Frozen input hash differs: ' + name)
    for correction in config.get('requiredCorrections', []):
        pin(correction['path'], correction['sha256'])
    for declaration in config['readyPackets']:
        pin(declaration['path'], declaration['sha256'])
        ready = read(local(declaration['path']))
        if ready['status'] not in ('ready-for-coordinator-acceptance', 'ready-for-coordinator-metadata-adapter-review'):
            raise ValueError('Packet is not ready')
        for record in ready['files']:
            pin(record['path'], record['sha256'])
        for index, packet in enumerate(ready['packets']):
            report = read(local(packet['report']))
            if report.get('failed') or report.get('allPassed') is not True:
                raise ValueError('Packet has no passing complete report: ' + packet['report'])
            descriptors = ready.get('canonicalDescriptors') or ([ready['canonicalDescriptor']] if ready.get('canonicalDescriptor') else [])
            packets.append(dict(ready=declaration['path'], packetIndex=index, report=packet['report'],
                producer=packet['producer'], canonicalDescriptors=descriptors,
                metadataOnly=ready['status'] == 'ready-for-coordinator-metadata-adapter-review'))
            for kind, group in [('function', report.get('matches', [])), ('data', report.get('dataMatches', []))]:
                for row in group:
                    item = {**report, **row}
                    key = identity(item)
                    if key in seen:
                        raise ValueError('Duplicate pending identity: ' + str(key))
                    seen.add(key)
                    size = row['bytes']
                    if not isinstance(size, int) or size <= 0 or row['compiledBytes'] != size:
                        raise ValueError('Incomplete emitted extent')
                    route = 'standard-matching-schema'
                    if not row.get('exactAfterDeclaredRelocation'):
                        route = snapshot_link(row, pin)
                    link = row.get('realLink', {})
                    if route == 'standard-matching-schema' and not (link.get('exactCallerBytes') if kind == 'function' else link.get('exactDataBytes') and link.get('exactDataAddress')):
                        raise ValueError('Missing genuine native placement proof')
                    for field in ('source', 'object'):
                        pin(row[field], row[field + 'Sha256'])
                    for dependency in row.get('sourceDependencies', []):
                        pin(dependency['path'], dependency['sha256'])
                    previous = accepted.get(key)
                    action = 'data' if kind == 'data' else 'new' if previous is None else 'migration'
                    if previous and (previous['bytes'] != size or previous['inputBytesSha256'] != row['targetSha256']):
                        raise ValueError('Migration changes its native identity')
                    rows.append(dict(identity=list(key), bytes=size, action=action,
                        route=route,
                        report=packet['report'], ready=declaration['path'], source=row['source'],
                        sourceSha256=row['sourceSha256'], targetSha256=row['targetSha256'],
                        previousSource=previous.get('sourceUnit') if previous else None))
    ordered = sorted(rows, key=lambda r: (r['identity'][:3], r['identity'][4]))
    for first, second in zip(ordered, ordered[1:]):
        if first['identity'][:3] == second['identity'][:3] and first['identity'][4] + first['bytes'] > second['identity'][4]:
            raise ValueError('Pending physical byte ranges overlap')
    totals = dict(newFunctions=sum(r['action'] == 'new' for r in rows),
        newFunctionBytes=sum(r['bytes'] for r in rows if r['action'] == 'new'),
        newDataObjects=sum(r['action'] == 'data' for r in rows),
        newDataBytes=sum(r['bytes'] for r in rows if r['action'] == 'data'),
        migrationFunctions=sum(r['action'] == 'migration' for r in rows),
        migrationBytes=sum(r['bytes'] for r in rows if r['action'] == 'migration'))
    if totals != config['expected']:
        raise ValueError('Derived queue totals differ: ' + json.dumps(totals))
    return dict(status='all-pending-packets-rehashed-and-classified-not-prepared',
        baselineRevision=revision, cohort=config['cohort'], totals=totals, packets=packets,
        rows=rows, verifiedPins=[dict(path=p, sha256=s) for p,s in sorted(pins.items())],
        uniquePins=len(pins), sourceCreditAdded=0, registryChanged=False, prepared=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = ROOT / args.output
    if output.exists():
        raise ValueError('Audit output already exists')
    result = audit(read(local(args.config)))
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k:result[k] for k in ('status','totals','uniquePins','sourceCreditAdded','prepared')}))

if __name__ == '__main__':
    main()
