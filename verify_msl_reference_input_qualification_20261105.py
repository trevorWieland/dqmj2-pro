import copy
from unittest.mock import patch
import qualify_msl_reference_inputs_20261105 as qualifier
from recovery_registry import batches
from project import ROOT, read_json, write_json, sha256


def main():
    original = batches()
    frozen = copy.deepcopy(original)
    projected, proof = qualifier.qualify(original)
    assert original == frozen and len(proof) == 4
    assert all(not (set(b['sourceHashes']) & qualifier.APPROVED.keys()) for b in projected)
    index = next(i for i, b in enumerate(original) if set(b['sourceHashes']) & qualifier.APPROVED.keys())
    batch = original[index]
    name = next(n for n in batch['sourceHashes'] if n in qualifier.APPROVED)
    report_path = ROOT / batch['report']
    report = read_json(report_path)
    rejected = []
    bad = copy.deepcopy(original)
    bad[index]['sourceHashes'][name] = '0' * 64
    variants = [('changed-registered-hash', bad)]
    bad = copy.deepcopy(original)
    for item in bad:
        item['sourceHashes'].pop(name, None)
    variants.append(('missing-reference-consumer', bad))
    for label, value in variants:
        try:
            qualifier.qualify(value)
        except AssertionError:
            rejected.append(label)
        else:
            raise ValueError(label)
    for field, value in [('source', name), ('sourceDependencies', [dict(path=name, sha256=qualifier.APPROVED[name])]), ('compilerFlags', ['-include', name])]:
        changed = copy.deepcopy(report)
        changed.get('matches', changed.get('functionMatches'))[0][field] = value
        reader = qualifier.read_json
        with patch.object(qualifier, 'read_json', side_effect=lambda p: changed if p == report_path else reader(p)):
            try:
                qualifier.qualify(original)
            except AssertionError:
                rejected.append('production-' + field)
            else:
                raise ValueError(field)
    hasher = qualifier.sha256
    with patch.object(qualifier, 'sha256', side_effect=lambda p: '0' * 64 if p == ROOT / name else hasher(p)):
        try:
            qualifier.qualify(original)
        except AssertionError:
            rejected.append('changed-actual-text')
        else:
            raise ValueError('changed actual text')
    unknown = 'work/unqualified-reference/unknown.c'
    bad = copy.deepcopy(original)
    bad[index]['sourceHashes'][unknown] = '0' * 64
    preserved, unused = qualifier.qualify(bad)
    assert preserved[index]['sourceHashes'][unknown] == '0' * 64
    assert original == frozen
    write_json(ROOT / 'evidence/verification/msl-reference-input-controls-20261105.json', dict(
        passed=True, sourceCredit=0, exactQualifiedTextInputs=4, rejectedControls=rejected,
        unknownWorkingPathStillSubjectToOriginalCommittedBlobCheck=True,
        originalRegistryBatchesUnmodified=True, qualifierSha256=sha256(ROOT / 'qualify_msl_reference_inputs_20261105.py')))
    print(dict(passed=True, qualifiedTextInputs=4, rejectedControls=len(rejected), unknownPathsStillChecked=True))


if __name__ == '__main__':
    main()
