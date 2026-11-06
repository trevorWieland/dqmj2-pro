import copy
from project import ROOT, read_json, write_json, sha256
import qualify_arm9_thumb_reference_inputs_20261105 as qualifier


def main():
    name = 'evidence/matches/cohort158-parallel-wave20261105-c-gamespy-thumb-next-first-0.json'
    report = read_json(ROOT / name)
    row = report['matches'][0]
    protected = [name, 'recovery.json', 'source-preferences.json', row['source'], row['object'], row['realLink']['lcf'], row['realLink']['linkedElf']]
    before = {p: sha256(ROOT / p) for p in protected}
    controls = []
    variants = []
    for field, value in [('processor', 'arm7'), ('program', 'child.srl'), ('module', 'ov000'), ('mode', 'arm'), ('sourceSha256', '0' * 64)]:
        changed = copy.deepcopy(row)
        changed[field] = value
        variants.append((field, changed))
    for label, flags in [('missing-thumb-flag', [f for f in row['compilerFlags'] if f != '-thumb']), ('duplicate-thumb', row['compilerFlags'] + ['-thumb']), ('arm-flag', row['compilerFlags'] + ['-arm']), ('binary-input', row['compilerFlags'] + ['extract/arm9/arm9.bin']), ('forced-include', row['compilerFlags'] + ['-include', 'hidden.h']), ('wrong-cpu-target', ['arm7tdmi' if f == 'arm946e' else f for f in row['compilerFlags']]), ('concatenated-include', row['compilerFlags'] + ['-ihidden/'])]:
        changed = copy.deepcopy(row)
        changed['compilerFlags'] = flags
        variants.append((label, changed))
    for label, changed in variants:
        try:
            qualifier.compiler_inputs(changed)
        except AssertionError:
            controls.append(label)
        else:
            raise ValueError(label)
    arm = read_json(ROOT / 'evidence/matches/cohort158-parallel-wave20261105-c-main-tail-next-fifth-0.json')['matches'][0]
    try:
        qualifier.object_mode(arm)
    except AssertionError:
        controls.append('actual-arm-object-rejected-by-thumb-mapping')
    else:
        raise ValueError('Actual ARM object accepted as Thumb')
    changed = copy.deepcopy(row)
    changed['objectSha256'] = '0' * 64
    try:
        qualifier.object_mode(changed)
    except AssertionError:
        controls.append('changed-object')
    else:
        raise ValueError('changed object')
    expected = {r['address']: r['bytes'] for r in report['matches']}
    wrong = dict(expected)
    wrong[row['address']] += 2
    data = qualifier.derive()
    try:
        qualifier.qualify_report(name, wrong, ROOT / 'work/integration/thumb-input-negative-ranges', data)
    except AssertionError:
        controls.append('changed-original-range')
    else:
        raise ValueError('changed original range')
    changed = copy.deepcopy(row)
    changed['realLink']['lcfSha256'] = '0' * 64
    start = int(row['address'], 0) - 0x02000000
    try:
        qualifier.linked_output(changed, ROOT / 'work/integration/thumb-input-negative-lcf', data[start:start + row['bytes']])
    except AssertionError:
        controls.append('changed-linker-control-file')
    else:
        raise ValueError('changed LCF')
    assert before == {p: sha256(ROOT / p) for p in protected}
    write_json(ROOT / 'evidence/verification/arm9-thumb-reference-input-controls-20261105.json', dict(
        passed=True, sourceCredit=0, rejectedControls=controls, originalSourceObjectsFlagsReportsAndRegistryUnchanged=True,
        actualMwThumbMappingConventionPreserved=True, qualifierSha256=sha256(ROOT / 'qualify_arm9_thumb_reference_inputs_20261105.py'),
        completePositiveQualification='evidence/verification/cohort158-thumb-reference-inputs-20261105.json'))
    print(dict(passed=True, rejectedControls=len(controls), sourceCredit=0))


if __name__ == '__main__':
    main()
