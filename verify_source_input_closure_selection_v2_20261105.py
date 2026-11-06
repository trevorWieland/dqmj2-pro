import copy
from unittest.mock import patch
import select_source_input_closure_v2_20261105 as selection
from project import ROOT, read_json, write_json, sha256


def main():
    for cohort in [153, 154, 155, 156]:
        expanded = read_json(ROOT / f'evidence/verification/cohort{cohort}-expanded-source-closure-20261101.json')
        selection.select(expanded, cohort)
    base = read_json(ROOT / 'evidence/verification/cohort154-expanded-source-closure-20261101.json')
    entry = next(r for r in base['reports'] if 'committed-source-inputs' in r['path'])
    controls = []
    variants = []
    wrong = copy.deepcopy(base);wrong['passed'] = False;variants.append(('failed-closure', wrong, 154))
    wrong = copy.deepcopy(base);wrong['reports'].append(copy.deepcopy(entry));variants.append(('duplicate-audit', wrong, 154))
    wrong = copy.deepcopy(base);wrong['sourceCommit'] = '0' * 40;variants.append(('other-source-commit', wrong, 154))
    wrong = copy.deepcopy(base);wrong['reports'] = [dict(entry, path=entry['path'].replace('-v9-', '-v99-'))];variants.append(('unknown-version', wrong, 154))
    wrong = copy.deepcopy(base);wrong['reports'] = [dict(entry, sha256='0' * 64)];variants.append(('changed-proof', wrong, 154))
    variants.append(('other-cohort', base, 155))
    for label, value, cohort in variants:
        try:
            selection.select(value, cohort)
        except AssertionError:
            controls.append(label)
        else:
            raise AssertionError(label)
    proof = read_json(ROOT / entry['path'])
    for field, value in [('passed', False), ('previousEightInputVerifierUnchanged', False), ('sourceCredit', 1)]:
        wrong = dict(proof, **{field: value})
        with patch.object(selection, 'read_json', return_value=wrong):
            try:
                selection.select(base, 154)
            except AssertionError:
                controls.append(field)
            else:
                raise AssertionError(field)
    write_json(ROOT / 'evidence/verification/source-input-closure-selection-v2-controls-20261105.json',
        dict(passed=True, sourceCredit=0, positiveCohorts=[153, 154, 155, 156], rejectedControls=controls,
             selectorSha256=sha256(ROOT / 'select_source_input_closure_v2_20261105.py')))
    print(dict(passed=True, positiveCohorts=4, rejectedControls=len(controls)))


if __name__ == '__main__':
    main()
