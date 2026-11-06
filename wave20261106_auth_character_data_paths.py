from project import ROOT

SOURCE=ROOT/'src/runtime/parallel_wave20261106/auth-character-data'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/auth-character-data'
WORK=ROOT/'work/w6ac'


def assert_owned():
    if SOURCE.resolve()!=(ROOT/'src/runtime/parallel_wave20261106/auth-character-data').resolve()or EVIDENCE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/auth-character-data').resolve()or WORK.resolve()!=(ROOT/'work/w6ac').resolve():raise ValueError('Exact admitted Auth character source/evidence/work directories differ')
    if not all(path.resolve().is_relative_to(ROOT.resolve())for path in [SOURCE,EVIDENCE,WORK]):raise ValueError('Auth character paths escaped repository')


def assert_work(path):
    assert_owned()
    if not path.resolve().is_relative_to(WORK.resolve()):raise ValueError('Auth character output escaped private work root')
