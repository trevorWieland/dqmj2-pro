import argparse
from project import ROOT, read_json, write_json, sha256, now
from link_runtime_unit import validate
from recover_linked_runtime import qualified_bindings


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--batch', type=int, required=True)
    batch = parser.parse_args().batch
    assert batch > 17
    source = ROOT / f'evidence/attempts/main-breadth-small{batch}-20261101.json'
    document = read_json(source)
    assert document['state'] == 'finished'
    report_path = ROOT / f'evidence/attempts/main-breadth-small{batch}-genuine-links-20261101.json'
    assert not report_path.exists()
    report = dict(generator='link_main_breadth_small_20261101.py', generatorSha256=sha256(__file__),
        createdUtc=now(), sourceReport=source.relative_to(ROOT).as_posix(), sourceReportSha256=sha256(source),
        results=[], state='running', sourceCredit=0,
        limitations=['Only genuine isolated MWLD comparisons are attempted',
                    'C contexts and signatures remain hypotheses until independently qualified',
                    'No semantic, accepted-source, module or ROM credit'])
    write_json(report_path, report)
    for candidate in document['results']:
        rows = [row for row in candidate.get('attempts', []) if row.get('compiledBytes')]
        if not rows:
            continue
        row = max(rows, key=lambda item: item.get('matchingBytes', 0))
        assert sha256(ROOT / row['source']) == row['sourceSha256']
        assert sha256(ROOT / row['object']) == row['objectSha256']
        work = ROOT / f'work/main-breadth-small{batch}-genuine-links-20261101' / (row['mode'] + '-' + row['address'][2:])
        assert not work.exists()
        result = dict(address=row['address'], bytes=row['bytes'], mode=row['mode'], source=row['source'],
            sourceSha256=row['sourceSha256'], objectSha256=row['objectSha256'], acceptedSourceCredit=0)
        try:
            proof = validate(row, qualified_bindings(row), work)
            result.update(exact=True, genuineLinkComparison=proof)
        except Exception as error:
            result.update(exact=False, error=str(error))
            if error.args and isinstance(error.args[0], dict):
                result['genuineLinkComparison'] = error.args[0]
        binary = work / 'caller.bin'
        result['freshLinkedBinaryProduced'] = binary.is_file()
        if binary.is_file():
            result.update(linkedBytes=binary.stat().st_size, linkedSha256=sha256(binary))
        report['results'].append(result)
        write_json(report_path, report)
        print(dict(address=row['address'], exact=result['exact'], linked=result['freshLinkedBinaryProduced']), flush=True)
    report.update(state='finished', finishedUtc=now(),
        freshLinkedCandidates=sum(row['freshLinkedBinaryProduced'] for row in report['results']),
        isolatedExactHypotheses=sum(row['exact'] for row in report['results']))
    write_json(report_path, report)


if __name__ == '__main__':
    main()
