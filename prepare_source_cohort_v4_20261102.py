import sys
from project import ROOT, read_json, write_json, sha256
import prepare_source_cohort_v3_20261102 as base
from qualify_explicit_c_frontend_20261102 import qualify
from qualify_inline_clz_20261104 import classify as classify_with_inline_clz

CLASSIFY = base.classify_additions


def classify(after, added):
    spec = read_json(ROOT / sys.argv[1])
    cohort = spec['cohort']
    adjusted, qualifications = dict(after), []
    for key in sorted(added):
        row = after[key]
        flags = row.get('compilerFlags') or []
        if row.get('sourceLanguage') == 'c':
            assert not row.get('assemblyJustification') and (ROOT / row['source']).suffix == '.c'
            assert '-lang' not in flags
        if row.get('sourceLanguage') in (None, 'c') and not row.get('assemblyJustification') and '-lang' not in flags:
            receipt = qualify(row, ROOT / f'work/integration/cohort{cohort}-explicit-c99/{key[0]}-{key[2]:08x}')
            receipt['reportedSourceLanguage'] = row.get('sourceLanguage')
            qualifications.append(receipt)
            adjusted[key] = dict(row, sourceLanguage='C')
    result, mixed = classify_with_inline_clz(adjusted, added, CLASSIFY)
    write_json(ROOT / f'evidence/verification/cohort{cohort}-inline-clz-qualification-20261104.json',
        dict(passed=True, sourceCredit=0, qualifierSha256=sha256(ROOT / 'qualify_inline_clz_20261104.py'),
            qualifications=mixed, ordinaryClassifierRetained=True, productionSourcesObjectsFlagsAndGuardsChanged=False))
    write_json(ROOT / f'evidence/verification/cohort{cohort}-explicit-c99-qualification-20261101.json',
        dict(passed=True, sourceCredit=0, generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__),
            qualifierSha256=sha256(ROOT / 'qualify_explicit_c_frontend_20261102.py'),
            qualifications=qualifications, productionSourcesObjectsFlagsAndGuardsChanged=False))
    return result


if __name__ == '__main__':
    base.classify_additions = classify
    base.main()
