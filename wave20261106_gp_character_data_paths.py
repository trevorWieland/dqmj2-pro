from project import ROOT

SOURCE=ROOT/'src/runtime/parallel_wave20261106/gamespy-gp-character-data'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data'
WORK=ROOT/'work/w6gp'


def assert_owned():
    if SOURCE.resolve()!=(ROOT/'src/runtime/parallel_wave20261106/gamespy-gp-character-data').resolve()or EVIDENCE.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261106/gamespy-gp-character-data').resolve()or WORK.resolve()!=(ROOT/'work/w6gp').resolve():raise ValueError('Exact admitted GP character source/evidence/work directory differs')
    if not all(x.resolve().is_relative_to(ROOT.resolve())for x in [SOURCE,EVIDENCE,WORK]):raise ValueError('GP character path escaped repository')


def assert_work(path):
    assert_owned()
    if not path.resolve().is_relative_to(WORK.resolve()):raise ValueError('GP character diagnostic escaped private work root')
