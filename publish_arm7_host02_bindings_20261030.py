from pathlib import Path
from project import ROOT, configuration, read_json, sha256, write_json
import match_arm7_bulk_20261030_host02 as matcher

REPORT = ROOT / 'evidence/matches/arm7-bulk-20261030-host02.json'


def qualified_bindings(report):
    if report['romSha256'] != configuration()['romSha256'] or report['processor'] != 'arm7' or report['program']:
        raise ValueError('Host ARM7 publication namespace differs')
    result = {}
    views = report['originalInitializedDataDependencies']
    for unit in report['matches']:
        binary = (ROOT / unit['binary']).read_bytes()
        if sha256(ROOT / unit['binary']) != unit['inputModuleSha256']:
            raise ValueError('Current ARM7 module hash differs')
        base = int(unit['base'], 0) if isinstance(unit['base'], str) else unit['base']
        start = int(unit['address'], 0) - base
        body = binary[start:start + unit['bytes']]
        link = unit['realArm7Link']
        if not link['exactLinkedBytes'] or link['targetSha256'] != unit['targetSha256']:
            raise ValueError('Current real-link comparison differs')
        for rel in unit['relocations']:
            if rel['type'] != 2 or rel['format'] != 'SHT_RELA':
                raise ValueError('Unqualified host publication relocation')
            symbol = rel['symbol']
            binding = link['bindings'][symbol]
            if binding['program'] or binding['processor'] != 'arm7' or binding['module'] != unit['module'] or binding['kind'] != 'data' or binding['mode'] != 'data' or binding['region'] != 'initialized':
                raise ValueError('Host binding is not qualified initialized data')
            encoded = int.from_bytes(body[rel['offset']:rel['offset'] + 4], 'little')
            target = (encoded - rel['explicitAddend']) & 0xFFFFFFFF
            if target != int(binding['address'], 0):
                raise ValueError('Native word and unchanged addend disagree with binding')
            view = next((x for x in views if x['module'] == unit['module'] and int(x['address'], 0) <= target < int(x['address'], 0) + x['bytes']), None)
            if view is None or view['inputModuleSha256'] != unit['inputModuleSha256'] or view['recoveredDataSourceCredit'] != 0:
                raise ValueError('Original data dependency is unqualified')
            offset = int(view['address'], 0) - base
            import hashlib
            if hashlib.sha256(binary[offset:offset + view['bytes']]).hexdigest() != view['sha256']:
                raise ValueError('Original data view changed')
            record = {'symbol': symbol, **binding, 'nativeEncodedWord': hex(encoded),
                      'unchangedExplicitAddend': rel['explicitAddend'], 'sourceCredit': 0}
            if symbol in result and result[symbol] != record:
                raise ValueError('Conflicting qualified host data symbol')
            result[symbol] = record
        if set(link['bindings']) != {rel['symbol'] for rel in unit['relocations']}:
            raise ValueError('Unused or missing standalone binding')
    return [result[key] for key in sorted(result)]


def main():
    matcher.main()
    report = read_json(REPORT)
    bindings = qualified_bindings(report)
    source = {'path': Path(__file__).name, 'sha256': sha256(__file__)}
    report['nativeSymbols'] = {row['symbol']: row['address'] for row in bindings}
    report['nativeSymbolEntries'] = bindings
    report['bindingPublication'] = {**source, 'freshSourceRebuildRequired': True,
        'unchangedRelocationAddends': True, 'newCodeOrDataCredit': 0}
    report['generatorSources'].append(source)
    write_json(REPORT, report)
    print({'qualifiedPublishedDataSymbols': len(bindings), 'newSourceCredit': 0})


if __name__ == '__main__':
    main()
