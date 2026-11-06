from project import ROOT, now, read_json, write_json
from linker_layout_regions import annotate, current, recipe_valid


def main():
    report = read_json(ROOT / 'evidence/linking/latest.json')
    annotate(report, ROOT / 'build/link-work')
    rows = report.get('generatedLinkerLayoutRegions', [])
    if not rows:
        raise ValueError('No production linker metadata region was measured')
    checks = []
    overlapping = {**report, 'sourceUnits': report['sourceUnits'] +
                   [{'module': 'ov007', 'start': '0x21da0b0', 'end': '0x21da0b4'}]}
    try:
        annotate(overlapping, ROOT / 'build/link-work')
    except ValueError as error:
        if 'overlaps an authored source unit' not in str(error):
            raise
    else:
        raise ValueError('An authored source overlap retained linker-layout eligibility')
    checks.append('authored-source-overlap')
    for row in rows:
        assert current(row, report)
        for key, value in [('address', '0x21da0b4'), ('moduleInputSha256', '0' * 64),
                           ('lcfSha256', '0' * 64), ('ordinaryFunctionCredit', 1),
                           ('sourceMatchedByteCredit', 16), ('inputObjectReferencesInRecipe', 1)]:
            assert not current({**row, key: value}, report)
            checks.append(key)
        text = (ROOT / 'build/link-work/arm9.lcf').read_text()
        assert recipe_valid(text, 'OV007', 32)
        bad = text.replace('OV007_CTOR_START = .;\n        \n        WRITEW(0);',
                           'OV007_CTOR_START = .;\n        \n        WRITEW(1);')
        assert not recipe_valid(bad, 'OV007', 32)
        bad = text.replace('OV007_CTOR_END = .;\n        . = ALIGN(32);',
                           'OV007_CTOR_END = .;\n        . = ALIGN(16);')
        assert not recipe_valid(bad, 'OV007', 32)
        checks.extend(['nonzero-constructor', 'wrong-alignment'])
    result = {'createdUtc': now(), 'productionModuleCompared': True,
              'rangeBytes': sum(row['bytes'] for row in rows), 'negativeChecks': checks,
              'passed': True, 'ordinarySourceByteCredit': 0}
    write_json(ROOT / 'evidence/verification/linker-layout-negatives-20261029.json', result)
    print(result)


if __name__ == '__main__':
    main()
