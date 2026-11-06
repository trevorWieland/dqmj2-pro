import gzip
import hashlib
import json

from project import ROOT


def encode(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def store(results, address, source_hash, rom_hash, directory):
    raw = encode(dict(schemaVersion=1, romSha256=rom_hash, module='ov001', processor='arm9', mode='arm',
                      address=hex(address), sourceSha256=source_hash, results=results))
    compressed = gzip.compress(raw, mtime=0)
    path = directory / f'{address:08x}-{digest(compressed)}.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != compressed:
        raise ValueError('Content-addressed raw proof differs')
    path.write_bytes(compressed)
    summaries = []
    for index, row in enumerate(results):
        machine = row['result']
        item = dict(case=index, recipeSha256=digest(encode({key: value for key, value in row.items() if key != 'result'})))
        item.update({key: machine[key] for key in ('actualReturn', 'returnBits', 'instructions', 'writes',
                     'wholeRamSha256', 'writeTraceSha256', 'pcTraceSha256', 'stackSha256', 'cpsr')})
        item.update(registersSha256=digest(encode(machine['registers'])),
            nativeRngActualReturns=len(machine['rngReturns']), rngTraceSha256=digest(encode(machine['rngReturns'])),
            nativeDependencyActualReturns=len(machine['protocolReturns']),
            protocolTraceSha256=digest(encode([machine['protocolEntries'], machine['protocolReturns']])))
        summaries.append(item)
    return summaries, dict(path=str(path.relative_to(ROOT)), sha256=digest(compressed), bytes=len(compressed), format='json+gzip',
                            gzipMtime=0, uncompressedSha256=digest(raw), uncompressedBytes=len(raw))
