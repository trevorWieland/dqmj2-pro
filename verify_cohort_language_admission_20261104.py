import argparse
import copy
import sys
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
import prepare_source_cohort_v4_20261102 as frontend


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('specification')
    parser.add_argument('--output', required=True)
    options = parser.parse_args()
    spec = read_json(ROOT / options.specification)
    after = {}
    lowercase = []
    for packet in spec['packets']:
        report = read_json(ROOT / packet['report'])
        for row in report['matches']:
            key = (row['module'], row['mode'], int(row['address'], 0))
            assert key not in after
            after[key] = dict(row, size=row['bytes'])
            if row.get('sourceLanguage') == 'c':
                lowercase.append(key)
    with patch.object(sys, 'argv', ['prepare_source_cohort_v4_20261102.py', options.specification]):
        accounting = frontend.classify(after, set(after))
    assert accounting['newOrdinaryCBytes'] + accounting['newVerifiedOriginalAssemblyBytes'] == sum(r['size'] for r in after.values())
    controls = []
    if lowercase:
        key = lowercase[0]
        variants = [
            ('lowercase-with-assembly', dict(assemblyJustification={'unsupported': True})),
            ('lowercase-cpp-extension', dict(source=after[key]['source'] + '.cpp')),
            ('lowercase-conflicting-explicit-frontend', dict(compilerFlags=[*after[key]['compilerFlags'], '-lang', 'c++'])),
            ('unknown-language-still-rejected', dict(sourceLanguage='unqualified-language'))
        ]
        for name, changes in variants:
            row = copy.deepcopy(after[key])
            row.update(changes)
            try:
                with patch.object(sys, 'argv', ['prepare_source_cohort_v4_20261102.py', options.specification]):
                    frontend.classify({key: row}, {key})
            except (AssertionError, ValueError):
                controls.append(dict(name=name, rejected=True))
            else:
                raise AssertionError('Unqualified language accepted: ' + name)
    receipt = ROOT / f'evidence/verification/cohort{spec["cohort"]}-explicit-c99-qualification-20261101.json'
    qualifications = read_json(receipt)
    assert len([q for q in qualifications['qualifications'] if q.get('reportedSourceLanguage') == 'c']) == len(lowercase)
    write_json(ROOT / options.output, dict(passed=True, sourceCredit=0, functions=len(after),
        explicitC99EquivalentLowercaseFunctions=len(lowercase), accounting=accounting, negativeControls=controls,
        qualificationReceipt=receipt.relative_to(ROOT).as_posix(), qualificationReceiptSha256=sha256(receipt),
        productionSourcesObjectsFlagsAndOriginalClassifierUnchanged=True))
    print(dict(passed=True, functions=len(after), explicitC99EquivalentLowercaseFunctions=len(lowercase),
               negativeControls=len(controls), accounting=accounting))


if __name__ == '__main__':
    main()
