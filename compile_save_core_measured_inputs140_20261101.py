import concurrent.futures
import gzip
import json
from pathlib import Path

import census_compile_save_core_near140_20261101 as C

ROOT = Path(__file__).resolve().parent


def worker(profile):
    original = C.worker(profile)
    return original


def main():
    profile_path = ROOT / 'evidence/lanes/save-core/measured-inputs140-profile-20261101.json'
    profiles = json.loads(profile_path.read_text())['rows']
    with concurrent.futures.ProcessPoolExecutor(max_workers=2) as pool:
        rows = list(pool.map(worker, profiles))
    raw = (json.dumps(rows, indent=2) + '\n').encode()
    packed = gzip.compress(raw, mtime=0)
    archive = ROOT / 'evidence/vectors/save-core-measured-inputs140-provenance-20261101.json.gz'
    archive.write_bytes(packed)
    compact = []
    for entry in rows:
        row = entry.get('row', {})
        compact.append(dict(address=entry['profile']['address'], error=entry.get('error'),
                            source=row.get('source'), sourceSha256=row.get('sourceSha256'),
                            compiledBytes=row.get('compiledBytes'), sameOffsetBytes=row.get('sameOffsetBytes'),
                            exactByteEqual=row.get('exactByteEqual'), linkedBinary=row.get('linkedBinary'),
                            realLinkSnapshot=row.get('realLinkSnapshot')))
    report = dict(schema=1, sourceCredit=0, compilerWorkers=2, profile=profile_path.relative_to(ROOT).as_posix(),
                  profileSha256=C.sha(profile_path.read_bytes()), results=compact,
                  fullProvenanceSidecar=dict(path=archive.relative_to(ROOT).as_posix(), sha256=C.sha(packed),
                      compressedBytes=len(packed), uncompressedSha256=C.sha(raw), uncompressedBytes=len(raw), contexts=len(rows)))
    (ROOT / 'evidence/lanes/save-core/measured-inputs140-compile-20261101.json').write_text(json.dumps(report, indent=2) + '\n')
    for row in compact:
        print(json.dumps({k: v for k, v in row.items() if k != 'realLinkSnapshot'}))


if __name__ == '__main__':
    main()
