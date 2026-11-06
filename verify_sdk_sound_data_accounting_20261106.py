from project import ROOT, read_json, write_json, sha256, configuration
from ledger_state import collect_matches
from qualify_sdk_sound_data_additions_20261106 import selected_data, identity, qualify


def main():
    name = 'evidence/data/sdk-sound-data-20261106.json'
    report = read_json(ROOT / name)
    before, after = selected_data(), selected_data()
    for row in report['dataMatches']:
        item = dict(report, **row)
        key = identity(item)
        assert key not in after
        after[key] = item
    functions, rejected = collect_matches(configuration()['romSha256'])
    assert not rejected
    first = sorted(set(after) - set(before))[0]
    controls = []

    def reject(label, modified, expected=report['dataMatches'], function_rows=functions):
        try:
            qualify(before, modified, expected, function_rows,
                    ROOT / 'work/integration/sdk-sound-data-accounting-controls' / label)
        except AssertionError:
            controls.append(dict(control=label, rejected=True))
        else:
            raise AssertionError('Invalid SDK data accounting accepted: ' + label)

    changed = dict(after)
    changed.pop(next(iter(before)))
    reject('missing-earlier-data', changed)
    old = next(iter(before))
    changed = dict(after)
    changed[old] = dict(changed[old], sourceSha256='0' * 64)
    reject('changed-earlier-source', changed)
    reject('duplicate-expected-identity', after, report['dataMatches'] + [report['dataMatches'][0]])
    for label, field, value in [('wrong-data-mode', 'mode', 'arm'), ('wrong-cpu', 'processor', 'arm7'),
                                 ('inflated-padding', 'measuredZeroAlignmentBytes', 1)]:
        changed = dict(after)
        changed[first] = dict(changed[first], **{field: value})
        reject(label, changed)
    function_rows = dict(functions)
    function_rows[('overlap-control',)] = dict(program=first[0], processor=first[1], module=first[2],
                                              address=hex(first[4]), size=1)
    reject('function-storage-overlap', after, function_rows=function_rows)
    wrong = ROOT / f'work/sdk-sound-data-20261106/{first[2]}-{after[first]["address"]}/wrong/data.o'
    assert wrong.is_file()
    changed = dict(after)
    changed[first] = dict(changed[first], object=wrong.relative_to(ROOT).as_posix(), objectSha256=sha256(wrong))
    reject('genuine-same-size-wrong-object', changed)
    positive = qualify(before, after, report['dataMatches'], functions,
                       ROOT / 'work/integration/sdk-sound-data-accounting-positive-final')
    write_json(ROOT / 'evidence/verification/sdk-sound-data-accounting-controls-20261106.json',
        dict(passed=True, sourceCredit=0, controls=controls, positiveQualification=positive,
             actualEarlierDataRows=len(before), actualFunctionRows=len(functions),
             originalReportSha256=sha256(ROOT / name), generatorSha256=sha256(__file__),
             qualifierSha256=sha256(ROOT / 'qualify_sdk_sound_data_additions_20261106.py')))
    print(dict(passed=True, accountingControls=len(controls), dataObjects=6, initializedBytes=3752, sourceCredit=0))


if __name__ == '__main__':
    main()
