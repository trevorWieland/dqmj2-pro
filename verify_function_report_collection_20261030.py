import copy
from project import ROOT, read_json, write_json
import build_modules


def main():
    original_work = build_modules.WORK
    work = ROOT / 'work/function-report-collection-20261030'
    work.mkdir(parents=True, exist_ok=True)
    report = read_json(ROOT / 'evidence/matches/main-heap-sort-20261030.json')
    rows = report.pop('functionMatches')
    actual = []
    build_modules.WORK = work
    try:
        for key in ['functionMatches', 'matches', 'functions']:
            document = copy.deepcopy(report)
            document[key] = rows
            path = work / (key + '.json')
            write_json(path, document)
            result = read_json(build_modules.collect_units(None, [path]))
            assert len(result['units']) == 1
            unit = result['units'][0]
            assert int(unit['start'], 0) == 0x0201D470 and int(unit['end'], 0) == 0x0201D5D4
            assert unit['source'] == rows[0]['source'] and unit['sha256'] == rows[0]['objectSha256']
            actual.append({field: unit[field] for field in ['module', 'start', 'end', 'source', 'sourceSha256', 'object', 'sha256']})
        assert actual[0] == actual[1] == actual[2]
        wrong = copy.deepcopy(report)
        wrong['functionMatches'] = {'unexpected': rows[0]}
        path = work / 'invalid-record-container.json'
        write_json(path, wrong)
        try:
            build_modules.collect_units(None, [path])
        except ValueError as error:
            assert 'array' in str(error)
        else:
            raise AssertionError('InvalidRecordContainerAccepted')
    finally:
        build_modules.WORK = original_work
    write_json(ROOT / 'evidence/verification/function-report-collection-20261030.json',
               {'romSha256': report['romSha256'], 'allThreeSupportedSchemasCollectedIdentically': True,
                'complete356ByteSpanRequired': True, 'actualSourceObjectRequired': True,
                'invalidRecordContainerRejected': True, 'sourceCredit': 0})
    print({'schemas': 3, 'identicalActualSourceUnits': True, 'invalidContainerRejected': True})


if __name__ == '__main__':
    main()
