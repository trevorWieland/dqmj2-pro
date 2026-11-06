import argparse
import concurrent.futures
import hashlib
import re
import subprocess
import sys
from project import ROOT, read_json, write_json, sha256
from sequential_overlay_shapes843_20261102 import convert

BASE = ROOT / 'nonmatching/overlay-lane/20261102-sequential844'
PLAN = BASE / 'queue.json'
SNAPSHOT = ROOT / 'evidence/verification/accepted-cohort137-identities-v2-20261101.json'


def prepare():
    if PLAN.exists():
        raise ValueError('844 queue already exists')
    accepted = read_json(SNAPSHOT)['functions']
    entries = []
    rejected = []
    for batch in ['20261102-battle816', '20261102-battle825']:
        queue = read_json(ROOT / f'nonmatching/overlay-lane/{batch}/queue.json')
        for original in queue['functions']:
            address = int(original['address'], 0)
            size = original['bytes']
            source = ROOT / original['directory'] / 'strong/source.c'
            if not source.is_file() or 'switch (' not in source.read_text():
                continue
            if address in [0x021F35F0, 0x021F2878]:
                continue
            for row in accepted:
                if row.get('processor') == 'arm9' and row.get('module') == 'ov001' and not row.get('program'):
                    other = int(str(row['address']), 0)
                    if other == address or max(address, other) < min(address + size, other + (row.get('bytes') or 0)):
                        raise ValueError(('844 accepted overlap', original, row))
            assembly = ROOT / original['directory'] / 'input.s'
            if re.search(r'add\w*\s+pc\s*,\s*pc|ldr\w*\s+pc\s*,', assembly.read_text(), re.I):
                rejected.append(dict(address=hex(address), reason='Native PC-dispatch requires separate topology analysis'))
                continue
            if address in [0x021F84A0, 0x02216CFC]:
                rejected.append(dict(address=hex(address), reason='Unresolved saved-register input remains unsupported'))
                continue
            source_text = source.read_text()
            header = source.with_name('context.h')
            overrides = {
                0x021F7D70: '20261102-stack819/021f7d70/stack-and-word-table',
                0x021E00B4: '20261102-word-table824/native-word-table',
            }
            if address in overrides:
                repaired = ROOT / 'nonmatching/overlay-lane' / overrides[address] / 'source.c'
                if repaired.is_file():
                    source = repaired
                    source_text = repaired.read_text()
                    header = repaired.with_name('context.h')
            try:
                transformed, records = convert(source_text)
                if not records:
                    raise ValueError('No remaining switch in the selected repaired hypothesis')
                if len(transformed.splitlines()) > 500:
                    raise ValueError('Transformed source needs a separate fragment design')
                directory = BASE / f'{address:08x}'
                directory.mkdir(parents=True, exist_ok=False)
                (directory / 'source.c').write_text(transformed)
                (directory / 'context.h').write_bytes(header.read_bytes())
                entries.append(dict(identity=original, source=source.relative_to(ROOT).as_posix(), sourceSha256=sha256(source), context=header.relative_to(ROOT).as_posix(), contextSha256=sha256(header), assembly=assembly.relative_to(ROOT).as_posix(), assemblySha256=sha256(assembly), directory=directory.relative_to(ROOT).as_posix(), transformedSha256=sha256(directory / 'source.c'), transforms=records, sourceCredit=0))
            except Exception as error:
                rejected.append(dict(address=hex(address), reason=str(error)))
    write_json(PLAN, dict(schemaVersion=1, sourceCredit=0, snapshot=SNAPSHOT.relative_to(ROOT).as_posix(), snapshotSha256=sha256(SNAPSHOT), functions=entries, rejected=rejected, limits=['Ordinary C control-flow hypotheses; native/model proof and exact compiler/link comparisons are still required.', 'Default position and explicit fallthrough are preserved by path expansion; internal conditional breaks reject rather than silently change behavior.']))
    print('prepared', len(entries), sum(row['identity']['bytes'] for row in entries), 'rejected', rejected)


def one(index):
    import match_runtime as c
    from link_runtime_unit import validate
    from recover_linked_runtime import qualified_bindings
    item = read_json(PLAN)['functions'][index]
    source = ROOT / item['directory'] / 'source.c'
    if sha256(source) != item['transformedSha256']:
        raise ValueError('844 source changed after preparation')
    attempts = []
    for speed in [False, True]:
        directory = ROOT / 'work/ol844' / item['identity']['address'][2:] / str(speed)
        c.WORK = directory / 'compile'
        attempt = dict(speed=speed, sourceCredit=0, semanticTested=False)
        try:
            rows, unused = c.compare(source, 'ov001', '2', 'off', speed)
            attempt['rows'] = []
            for row in rows:
                result = dict(source=row)
                if not row.get('compileFailed'):
                    try:
                        result['genuineLink'] = validate(row, qualified_bindings(row), directory / 'link')
                    except Exception as error:
                        result['genuineLink'] = error.args[0] if error.args and isinstance(error.args[0], dict) else dict(failure=str(error))
                attempt['rows'].append(result)
        except Exception as error:
            attempt['failure'] = str(error)
        attempts.append(attempt)
    write_json(ROOT / item['directory'] / 'results.json', dict(input=item, attempts=attempts, sourceCredit=0))
    print(item['identity']['address'], [(a['speed'], a.get('failure'), [(r.get('genuineLink', {}).get('matchingBytes'), r.get('genuineLink', {}).get('candidateBytes')) for r in a.get('rows', [])]) for a in attempts], flush=True)


def run():
    entries = read_json(PLAN)['functions']
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        pending = [pool.submit(subprocess.run, [sys.executable, __file__, '--one', str(index)], cwd=ROOT, capture_output=True, text=True) for index in range(len(entries))]
        for future in concurrent.futures.as_completed(pending):
            result = future.result()
            print(result.stdout, result.stderr[:1200], flush=True)
            if result.returncode:
                raise ValueError('844 isolated compile worker failed')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--prepare', action='store_true')
    parser.add_argument('--run', action='store_true')
    parser.add_argument('--one', type=int)
    options = parser.parse_args()
    if options.prepare:
        prepare()
    if options.one is not None:
        one(options.one)
    if options.run:
        run()
