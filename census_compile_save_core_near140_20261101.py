import concurrent.futures
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
INTEGRATOR = ROOT.parents[1] / 'dqmj2pro-decomp'
SNAPSHOT = 'evidence/integration/root-accepted107-identities-v2-20261101.json'
HISTORY = 'evidence/lanes/save-core/historical-near-census108-20261101.json'
TARGETS = {0x0206A584, 0x02046188, 0x02040E74, 0x020CFD18, 0x020CE56C, 0x0205F920,
           0x02080340, 0x02083764, 0x020CE868, 0x020BB2B0, 0x02048E14, 0x0205D5BC}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def number(value):
    return int(value, 0) if isinstance(value, str) else value


def exclusions():
    ranges, receipts = [], []
    def add(row):
        if row.get('module') == 'main' and row.get('processor', 'arm9') in ('arm9', None):
            start = number(row['address'])
            ranges.append((start, start + number(row.get('bytes', 1))))
    path = ROOT / SNAPSHOT
    receipts.append(dict(path=SNAPSHOT, sha256=sha(path.read_bytes())))
    for row in json.loads(path.read_text())['functions']:
        add(row)
    for path in INTEGRATOR.glob('cohort*-specification-20261101.json'):
        if int(re.search(r'cohort(\d+)', path.name)[1]) < 108:
            continue
        report = json.loads(path.read_text())
        receipts.append(dict(integratorPath=path.name, sha256=sha(path.read_bytes())))
        for row in report.get('expectedAdditions', []):
            add(row)
    for path in (ROOT / 'evidence/matches').glob('*.json'):
        for row in json.loads(path.read_text()).get('matches', []):
            if isinstance(row, dict) and 'address' in row:
                add(row)
    ranges += [(0x020491F8, 0x020494BC), (0x02049794, 0x0204983C),
               (0x020444EC, 0x02044508)]
    return ranges, receipts


def worker(profile):
    path = ROOT / 'evidence/application/save_core_historical_link_20261031.py'
    spec = importlib.util.spec_from_file_location('near140_link', path)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    address = number(profile['address'])
    builder.MODULE, builder.MODE = 'main', profile['mode']
    builder.ENTRY, builder.LENGTH, builder.NAME = address, profile['bytes'], profile['name']
    builder.SOURCE = profile['source']
    builder.COMPILER, builder.COMPILER_HASH = profile['compilerPath'], profile['compilerSha256']
    builder.FLAGS = profile['flags']
    builder.WORK = f'work/save-core/near140/{address:08x}/{profile["sourceSha256"][:12]}'
    assert sha((ROOT / profile['source']).read_bytes()) == profile['sourceSha256']
    binary = builder.measured_module('main')[1]
    try:
        row, _ = builder.build(binary[address - 0x02000000:address - 0x02000000 + profile['bytes']])
        return dict(profile=profile, row=row)
    except Exception as error:
        return dict(profile=profile, error=str(error), errorType=type(error).__name__)


def main():
    ranges, receipts = exclusions()
    history = json.loads((ROOT / HISTORY).read_text())['candidates']
    selected, seen = [], set()
    for profile in sorted(history, key=lambda row: -row['historicalRatio']):
        address, length = number(profile['address']), profile['bytes']
        key = address, profile['mode']
        if address not in TARGETS or key in seen or not 0x02040000 <= address < 0x020D0000:
            continue
        if any(address < end and start < address + length for start, end in ranges):
            continue
        source = ROOT / profile['source']
        if not source.is_file() or sha(source.read_bytes()) != profile['sourceSha256']:
            continue
        if len(source.read_text().splitlines()) > 500:
            continue
        selected.append(profile)
        seen.add(key)
    census = dict(schema=1, sourceCredit=0, exclusionReceipts=receipts, history=HISTORY,
                  historySha256=sha((ROOT / HISTORY).read_bytes()), candidates=selected,
                  counts=dict(units=len(selected), nativeBytes=sum(row['bytes'] for row in selected)))
    census_path = ROOT / 'evidence/lanes/save-core/near140-census-20261101.json'
    census_path.write_text(json.dumps(census, indent=2) + '\n')
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(worker, selected))
    raw = (json.dumps(rows, indent=2) + '\n').encode()
    packed = gzip.compress(raw, mtime=0)
    archive = ROOT / 'evidence/vectors/save-core-near140-provenance-20261101.json.gz'
    archive.write_bytes(packed)
    compact = []
    for entry in rows:
        row = entry.get('row', {})
        compact.append(dict(address=entry['profile']['address'], bytes=entry['profile']['bytes'],
                            source=entry['profile']['source'], error=entry.get('error'),
                            compiledBytes=row.get('compiledBytes'), sameOffsetBytes=row.get('sameOffsetBytes'),
                            exactByteEqual=row.get('exactByteEqual'), linkedBinary=row.get('linkedBinary'),
                            linkedBinarySha256=row.get('linkedBinarySha256')))
    report = dict(schema=1, sourceCredit=0, compilerWorkers=2, census=census_path.relative_to(ROOT).as_posix(),
                  censusSha256=sha(census_path.read_bytes()), results=compact,
                  fullProvenanceSidecar=dict(path=archive.relative_to(ROOT).as_posix(), sha256=sha(packed),
                      compressedBytes=len(packed), uncompressedSha256=sha(raw), uncompressedBytes=len(raw), contexts=len(rows)))
    (ROOT / 'evidence/lanes/save-core/near140-baselines-20261101.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(census['counts']))
    for row in compact:
        print(json.dumps(row))


if __name__ == '__main__':
    main()
