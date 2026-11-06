import copy
from project import ROOT, read_json, write_json, sha256, configuration
from ledger_state import collect_matches
from qualify_child_static_data_additions_20261106 import selected_data, identity, qualify, literal_payload


def main():
    report_name = 'evidence/data/child-static-assets-next-20261105.json'
    assert sha256(ROOT / report_name) == '5ceb941065aa17afafc7273e3c23f9d3cc3fe4172a3e7dc95ec1ff6fccd623f8'
    report = read_json(ROOT / report_name)
    before = selected_data()
    after = dict(before)
    for row in report['dataMatches']:
        item = dict(report, **row)
        key = identity(item)
        assert key not in after
        after[key] = item
    functions, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    expected = report['dataMatches']
    first = sorted(set(after) - set(before))[0]
    cases = []

    def reject(label, modified, wanted=expected, function_rows=functions):
        directory = ROOT / 'work/integration/child-static-data-accounting-controls-20261106' / label
        try:
            qualify(before, modified, wanted, function_rows, directory)
        except AssertionError as error:
            cases.append(dict(control=label, rejected=True, exception=type(error).__name__, reason=str(error)))
        else:
            raise AssertionError('Invalid data accounting accepted: ' + label)

    changed = dict(after)
    changed.pop(next(iter(before)))
    reject('missing-earlier-data', changed)
    changed = dict(after)
    old = next(iter(before))
    changed[old] = dict(changed[old], sourceSha256='0' * 64)
    reject('changed-earlier-source', changed)
    reject('duplicate-expected-identity', after, expected + [expected[0]])
    changed = dict(after)
    changed[first] = dict(changed[first], mode='thumb')
    reject('wrong-data-mode', changed)
    changed = dict(after)
    changed[first] = dict(changed[first], measuredZeroAlignmentBytes=after[first]['measuredZeroAlignmentBytes'] + 1)
    reject('inflated-alignment-credit', changed)
    function_rows = dict(functions)
    function_rows[('synthetic-overlap-control',)] = dict(program=first[0], processor=first[1], module=first[2],
        address=hex(first[4]), size=1)
    reject('actual-function-storage-overlap', after, function_rows=function_rows)
    wrong = ROOT / f'work/w5sa-source/{first[4]:08x}/wrong-link/input.o'
    control = next(row for row in report['controls'] if int(row['address'], 0) == first[4])
    assert sha256(wrong) == control['wrongObjectSha256']
    changed = dict(after)
    changed[first] = dict(changed[first], object=wrong.relative_to(ROOT).as_posix(), objectSha256=sha256(wrong))
    reject('genuine-same-size-wrong-data-object', changed)
    assert literal_payload('const unsigned char test[2] = {0x00,0xff,};\n', 'test', 2) == bytes([0, 255])
    invalid = [
        'const unsigned char test[2] = {0x00};',
        'const unsigned char test[2] = {0x00,0xff}; int injected(void){return 0;}',
        'const unsigned char test[2] = {0x00,OTHER};',
        'unsigned char test[2] = {0x00,0xff};',
        'const unsigned char test[3] = {0x00,0xff};',
        'const unsigned char other[2] = {0x00,0xff};',
    ]
    for source in invalid:
        try:
            literal_payload(source, 'test', 2)
        except AssertionError:
            continue
        raise AssertionError('Invalid literal declaration accepted')
    write_json(ROOT / 'evidence/verification/child-static-data-accounting-controls-20261106.json',
        dict(passed=True, sourceCredit=0, accountingControls=cases, malformedDeclarationControls=len(invalid),
             originalReportSha256=sha256(ROOT / report_name), originalEarlierDataRows=len(before),
             originalFunctionRows=len(functions), genuineWrongObjectSha256=sha256(wrong),
             generatorSha256=sha256(__file__), qualifierSha256=sha256(ROOT / 'qualify_child_static_data_additions_20261106.py')))
    print(dict(passed=True, accountingControls=len(cases), malformedDeclarations=len(invalid), sourceCredit=0))


if __name__ == '__main__':
    main()
