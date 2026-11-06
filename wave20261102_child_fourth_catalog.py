import json
import re
import reuse_utility_c as reuse
import utility_code
from wave20261102_child_fourth_index import candidates
from wave20261102_child_fourth_prepare import ROOT, LANE
from project import write_json, sha256


def main():
    wanted = {int(e['address'], 0) for e in json.loads((LANE / 'claim.json').read_text())['functions']}
    specs = [s for s in candidates() if s['module'] == 'utility-child-arm7-main' and s['address'] in wanted]
    sizes = {(s['mode'], s['bytes']) for s in specs}
    indexed = reuse.origins()
    origins, seen, raw_matches = [], set(), []
    for (mode, size), by_offsets in indexed.items():
        if not 64 <= size <= 2 * max(s['bytes'] for s in specs):
            continue
        for offsets, by_hash in by_offsets.items():
            for digest, entries in by_hash.items():
                for entry in entries:
                    identity = (entry['source'], entry.get('name', entry.get('symbol')))
                    if identity in seen:
                        continue
                    text = (ROOT / entry['source']).read_text()
                    if re.search(r'\b(?:asm|__asm|__asm__|INCBIN)\b', text):
                        continue
                    seen.add(identity)
                    origins.append(entry)
    for spec in specs:
        binary = (ROOT / spec['binary']).read_bytes()
        offset = spec['address'] - spec['base']
        native = binary[offset:offset + spec['bytes']]
        for masks, by_hash in indexed.get((spec['mode'], spec['bytes']), {}).items():
            digest = reuse.normalized(native, masks)
            for origin in by_hash.get(digest, []):
                raw_matches.append(dict(module=spec['module'], address=hex(spec['address']), bytes=spec['bytes'],
                    source=origin['source'], sourceSha256=origin['sourceSha256'],
                    name=origin.get('name', origin.get('symbol')), compiler=origin.get('compiler'),
                    compilerFlags=origin.get('compilerFlags'), normalizedFingerprint=digest))
    write_json(LANE / 'origin-catalog.json', dict(schemaVersion=1, generator=__file__, generatorSha256=sha256(__file__),
        originCount=len(origins), origins=origins, rawFingerprintMatches=raw_matches,
        sourceCredit=0, limitations=['Fingerprints nominate source experiments; every destination must be freshly compiled and genuinely linked']))
    print(dict(origins=len(origins), rawMatches=len(raw_matches),
        distinctTargets=len({e['address'] for e in raw_matches})))


if __name__ == '__main__':
    main()
