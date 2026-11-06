import argparse
import concurrent.futures
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256

BASE = ROOT / 'nonmatching/overlay-lane/20261102-battle852'


def one(index):
    import match_runtime as c
    from link_runtime_unit import validate
    from recover_linked_runtime import qualified_bindings
    item = read_json(BASE / 'queue.json')['functions'][index]
    source = ROOT / item['directory'] / 'source.c'
    assert sha256(source) == item['sourceSha256']
    assert sha256(source.with_name('context.h')) == item['contextSha256']
    directory = ROOT / 'work/ol852' / item['address'][2:] / item['variant']
    c.WORK = directory / 'compile'
    result = dict(input=item, sourceCredit=0)
    try:
        rows, unused = c.compare(source, 'ov001', '2', 'off', int(item['address'], 0) != 0x021EAE04)
        result['rows'] = []
        for row in rows:
            value = dict(source=row)
            if not row.get('compileFailed'):
                try:
                    value['genuineLink'] = validate(row, qualified_bindings(row), directory / 'link')
                except Exception as error:
                    value['genuineLink'] = error.args[0] if error.args and isinstance(error.args[0], dict) else dict(failure=str(error))
            result['rows'].append(value)
    except Exception as error:
        result['failure'] = str(error)
    write_json(source.parent / 'results.json', result)
    print(item['address'], item['variant'], [(r.get('genuineLink', {}).get('matchingBytes'), r.get('genuineLink', {}).get('linkedBytes'), r.get('genuineLink', {}).get('exact')) for r in result.get('rows', [])], result.get('failure'), flush=True)


def run():
    items = read_json(BASE / 'queue.json')['functions']
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        pending = [pool.submit(subprocess.run, [sys.executable, __file__, '--one', str(index)], cwd=ROOT, capture_output=True, text=True) for index in range(len(items))]
        for future in concurrent.futures.as_completed(pending):
            result = future.result()
            print(result.stdout, result.stderr[:1000], flush=True)
            if result.returncode:
                raise ValueError('852 isolated compiler worker failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--one', type=int)
    parser.add_argument('--run', action='store_true')
    options = parser.parse_args()
    if options.one is not None:
        one(options.one)
    if options.run:
        run()
