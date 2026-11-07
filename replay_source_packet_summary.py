import argparse
import copy
from project import read_json, write_json, sha256
from source_packet_contracts import local
from replay_source_packet import replay

COLLECTIONS = ('matches', 'functionMatches', 'functions', 'dataMatches', 'containerMatches', 'linkageMatches')

def normalize(document, expected):
    if not isinstance(expected, dict) or set(expected) != {'functions'}:
        raise ValueError('Only the explicitly declared function summary is supported')
    count = expected['functions']
    if type(count) is not int or count < 0 or type(document.get('functions')) is not int:
        raise ValueError('The original function summary must be a nonnegative integer')
    rows = document.get('matches')
    if not isinstance(rows, list) or any(not isinstance(row, dict) or row.get('kind') == 'data' for row in rows):
        raise ValueError('Canonical function records must remain an explicit object list')
    if document['functions'] != count or len(rows) != count:
        raise ValueError('The declared function summary differs from the actual records')
    for key in COLLECTIONS:
        if key != 'functions' and key in document and not isinstance(document[key], list):
            raise ValueError('Unexpected non-list canonical collection: ' + key)
    result = copy.deepcopy(document)
    if 'workerSummaryCounts' in result or 'canonicalSummaryNormalization' in result:
        raise ValueError('Summary normalization must not replace existing evidence')
    result['workerSummaryCounts'] = {'functions': result.pop('functions')}
    result['canonicalSummaryNormalization'] = dict(originalField='functions', originalValue=count,
        canonicalRows='matches', canonicalRowsUnchanged=True, sourceCredit=0)
    return result

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('descriptor')
    parser.add_argument('--existing', action='store_true')
    args = parser.parse_args()
    descriptor = read_json(local(args.descriptor))
    expected = descriptor.get('workerSummaryCounts')
    initial = read_json(local(descriptor['initialReport']))
    normalize(initial, expected)
    replay(args.descriptor, not args.existing)
    target = local(descriptor['canonicalReport'])
    result = normalize(read_json(target), expected)
    name = 'replay_source_packet_summary.py'
    pins = {row['path']: row['sha256'] for row in result['generatorSources']}
    digest = sha256(local(name))
    if name in pins and pins[name] != digest:
        raise ValueError('Canonical summary adapter implementation changed')
    pins[name] = digest
    result['generatorSources'] = [dict(path=path, sha256=value) for path, value in sorted(pins.items())]
    result['canonicalReportRefreshedFromFreshWorkerObjects'] = False
    result['canonicalSummaryNormalization']['compilerOrCpuOracleRerunClaimed'] = False
    write_json(target, result)
    print(dict(report=descriptor['canonicalReport'], functions=len(result['matches']),
        originalWorkerSummaryPreserved=True, sourceRecordsUnchanged=True, registered=False))

if __name__ == '__main__':
    main()
