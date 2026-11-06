from pathlib import Path
from project import ROOT, sha256, read_json, write_json


def main():
    original = ROOT / 'audit_next_wave_eligibility_parallel_wave20261102.py'
    if sha256(original) != '45d5d93583b4a923d731d36a161469e770fc20dcc064d0e1ccd9381d0fd03163':
        raise ValueError('Frozen46-function auditor changed')
    text = original.read_text()
    old = "for lane in ['ov006', 'main-sdk-next', 'main-sdk-second']:"
    assert text.count(old) == 1
    text = text.replace(old, "for lane in ['main-sdk-third']:")
    text = text.replace('wave20261102_main_sdk_second_compiler.py', 'wave20261102_main_sdk_third_compiler.py')
    needle = "    seed = read_json(ROOT / 'provenance/seed-manifest.json')"
    insertion = '''    for name in ['ov006', 'main-sdk-next', 'main-sdk-second', 'utility-child-third']:
        previous = read_json(ROOT / 'evidence/lanes/parallel-wave20261102' / name / 'ready.json')
        reserved.extend((identity(row), row['bytes']) for row in previous['identities'])
'''
    assert text.count(needle) == 1
    text = text.replace(needle, insertion + needle)
    text = text.replace('next-wave-eligibility.json', 'main-sdk-third-eligibility.json')
    text = text.replace('Committed2325bb90 cohort147 plus reserved immutable298-function cohort148 proposal',
        'Committed2325bb90 cohort147 plus reserved298-function148 and other82 next-wave functions')
    target = ROOT / 'evidence/verification/parallel-wave20261102/main-sdk-third-eligibility.json'
    if target.exists():
        raise ValueError('Refusing to overwrite completed SDK-third audit')
    exec(compile(text, str(original), 'exec'), dict(__name__='__main__', __file__=str(original)))
    result = read_json(target)
    result.update(generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        frozenBaseAuditorSha256=sha256(original), scope='Read-only SDK-third audit reuses immutable46-function auditor with exact lane/adapter/reserved-set substitutions')
    write_json(target, result)


if __name__ == '__main__':
    main()
