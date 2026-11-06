import copy
import interpreted_ledger
from project import ROOT, now, read_json, write_json


def main():
    original = interpreted_ledger.REPORT
    inventory = read_json(original)
    work = ROOT / 'work/interpreted-inventory-negatives'
    work.mkdir(parents=True, exist_ok=True)
    path = work / 'inventory.json'
    results = []
    try:
        interpreted_ledger.REPORT = path
        mutations = [('source-credit', lambda row: row['images'][0].update(ordinaryScriptSourceBytesRecovered=1)),
                     ('namespace', lambda row: row.update(romSha256='0' * 64)),
                     ('content-alias', lambda row: row['images'][1].update(codeSha256=row['images'][0]['codeSha256'])),
                     ('byte-total', lambda row: row['totals'].update(uniqueCodeContainerBytes=row['totals']['uniqueCodeContainerBytes'] + 4))]
        for label, mutate in mutations:
            changed = copy.deepcopy(inventory)
            mutate(changed)
            write_json(path, changed)
            try:
                interpreted_ledger.measure(write=False)
            except ValueError:
                results.append(label)
            else:
                raise ValueError('Altered interpreted evidence was accepted: ' + label)
        changed = copy.deepcopy(inventory)
        changed['generatorSha256'] = '0' * 64
        write_json(path, changed)
        assert not interpreted_ledger.measure(write=False)['inventoryAvailable']
        results.append('stale-generator')
    finally:
        interpreted_ledger.REPORT = original
    current = interpreted_ledger.measure(write=False)
    import interpreted_sources
    accepted, unavailable = interpreted_sources.measure(inventory)
    assert current['inventoryAvailable'] and current['ordinarySourceBytesRecovered'] == sum(unit['sourceByteCredit'] for unit in accepted)
    result = {'createdUtc': now(), 'passed': True, 'negativeChecks': results,
              'uniqueImages': current['uniqueImages'], 'ordinarySourceCredit': current['ordinarySourceBytesRecovered']}
    write_json(ROOT / 'evidence/verification/interpreted-negatives-20261029.json', result)
    print(result)


if __name__ == '__main__':
    main()
