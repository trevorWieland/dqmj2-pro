import argparse

import concurrent.futures

import json

import re

from project import ROOT, configuration, now, sha256, write_json

from ledger_state import collect_matches

from sequential_state_shapes import variants

import match_runtime as compiler





def excluded(module, address):

    ranges = {'main': [(0x02048400, 0x02048600), (0x0204BC00, 0x0205C000), (0x02062000, 0x0207D000)],

              'ov001': [(0x021E3500, 0x021E6800)],

              'ov000': [(0x02209D00, 0x0220A100), (0x02214000, 0x02214200)]}

    return any(start <= address < end for start, end in ranges.get(module, []))





def candidates():

    matched, unused = collect_matches(configuration()['romSha256'])

    selected = []

    with (ROOT / 'ledger/drafts.jsonl').open(encoding='utf-8') as stream:

        for line in stream:

            row = json.loads(line)

            module, address = row['module'], int(row['address'], 0)

            if row['processor'] != 'arm9' or row['mode'] != 'arm' or module not in ('main', 'ov000', 'ov001', 'ov002', 'ov003', 'ov005', 'ov006', 'ov007'):

                continue

            if (module, 'arm', address) in matched or excluded(module, address):

                continue

            choices = []

            for item in row['implementations']:

                if not item.get('sourceCurrent') or not item.get('compiledUnderRecordedScope') or item.get('knownSemanticMismatch'):

                    continue

                if not isinstance(item.get('compiledBytes'), int) or not isinstance(item.get('matchingBytes'), int):

                    continue

                source = ROOT / item['source']

                if sha256(source) != item['sourceSha256']:

                    raise ValueError('Measured draft source changed')

                text = source.read_text(encoding='utf-8-sig')

                if len(text.splitlines()) <= 500 and re.search(r'\bswitch\s*\(', text):

                    choices.append((abs(item['compiledBytes'] - row['nativeBytes']), -item['matchingBytes'], item, text))

            if choices:

                delta, score, item, text = min(choices, key=lambda value: value[:2])

                selected.append((delta, score, row, item, text))

    return sorted(selected, key=lambda value: value[:2])





def attempt(candidate, batch):

    delta, score, identity, item, text = candidate

    folder = ROOT / 'nonmatching/sequential-states' / batch

    folder.mkdir(parents=True, exist_ok=True)

    rows = []

    for label, changed in variants(text):

        if len(changed.splitlines()) > 500:

            continue

        source = folder / (identity['module'] + '_' + identity['address'][2:] + '_' + label + '.c')

        source.write_text(changed, encoding='utf-8')

        for speed in (False, True):

            try:
                results, exact = compiler.compare(source, identity['module'], 2, 'off', speed)
            except Exception as error:
                rows.append({'comparisonFailure': type(error).__name__ + ': ' + str(error),
                             'source': source.relative_to(ROOT).as_posix(), 'sourceSha256': sha256(source),
                             'speed': speed, 'sourceCredit': 0})
                continue

            rows.extend(results)

            if exact:

                return {'id': identity['id'], 'inputSource': item['source'], 'inputSourceSha256': item['sourceSha256'],

                        'comparisons': rows, 'exactCandidates': [entry for entry, code in exact.values()]}

    return {'id': identity['id'], 'inputSource': item['source'], 'inputSourceSha256': item['sourceSha256'],

            'comparisons': rows, 'exactCandidates': []}





def main():

    parser = argparse.ArgumentParser()

    parser.add_argument('--batch', required=True)

    parser.add_argument('--limit', type=int, default=64)

    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--offset', type=int, default=0)

    options = parser.parse_args()

    report = ROOT / ('evidence/attempts/' + options.batch + '.json')

    if report.exists():

        raise ValueError('Use a new batch name to preserve experiments')

    inputs = candidates()[options.offset:options.offset + options.limit]

    output = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=options.workers) as pool:

        for row in pool.map(lambda value: attempt(value, options.batch), inputs):

            output.append(row)

            print({'id': row['id'], 'exactCandidates': len(row['exactCandidates'])}, flush=True)

    matches = [item for row in output for item in row['exactCandidates']]

    write_json(report, {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],

                        'generator': 'refine_sequential_states_20261029.py', 'generatorSha256': sha256(ROOT / 'refine_sequential_states_20261029.py'),

                        'shapeGeneratorSha256': sha256(ROOT / 'sequential_state_shapes.py'),

                        'candidates': len(inputs), 'results': output, 'matches': matches,

                        'exactFunctions': len(matches), 'exactCandidateBytes': sum(item['bytes'] for item in matches),

                        'sourceCredit': 0, 'moduleLinked': False,

                        'limitations': ['New state-chain hypotheses only; no compiler setting is generalized',

                                        'Real MW links, fresh return/state tests and coordinator module gates remain required',

                                        'Active worker intervals and all registered functions are excluded']})

    print({'candidates': len(inputs), 'exactFunctions': len(matches), 'exactCandidateBytes': sum(item['bytes'] for item in matches), 'sourceCredit': 0})





if __name__ == '__main__':

    main()

