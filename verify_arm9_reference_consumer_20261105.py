import copy
from project import ROOT, read_json, write_json, sha256
from qualify_arm9_reference_consumer_20261105 import REPORT, compiler_inputs


def main():
    rows = read_json(ROOT / REPORT)['matches']
    assert len(rows) == 8
    for row in rows:
        compiler_inputs(row)
    changes = [('cpu', ['processor'], 'arm7'), ('program', ['program'], 'wrong-child'),
        ('module', ['module'], 'ov001'), ('mode', ['mode'], 'thumb'),
        ('executable-source', ['source'], 'extract/arm9/arm9.bin'),
        ('changed-source', ['sourceSha256'], '0' * 64),
        ('unclosed-includes', ['sourceDependencies'], []),
        ('changed-header', ['sourceDependencies', 0, 'sha256'], '0' * 64),
        ('external-header', ['sourceDependencies', 0, 'path'], 'extract/arm9/arm9.bin'),
        ('native-compiler-input', ['compilerFlags'], rows[0]['compilerFlags'] + ['extract/arm9/arm9.bin']),
        ('implicit-prefix', ['compilerFlags'], rows[0]['compilerFlags'] + ['-prefix'])]
    rejected = []
    for name, keys, value in changes:
        wrong = copy.deepcopy(rows[0])
        target = wrong
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = value
        try:
            compiler_inputs(wrong)
        except AssertionError:
            rejected.append(name)
        else:
            raise AssertionError('Invalid compiler input contract admitted: ' + name)
    output = 'evidence/verification/cohort154-arm9-reference-consumer-controls-20261105.json'
    write_json(ROOT / output, dict(passed=True, sourceCredit=0, positiveFunctions=8,
        rejectedControls=rejected, originalSourceObjectsAndCanonicalReportUnchanged=True,
        qualifierSha256=sha256(ROOT / 'qualify_arm9_reference_consumer_20261105.py')))
    print(dict(passed=True, functions=8, rejectedControls=len(rejected)))


if __name__ == '__main__':
    main()
