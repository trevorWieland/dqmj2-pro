from project import ROOT

SOURCE=ROOT/'src/runtime/parallel_wave20261105/itcm-reset-next'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261105/itcm-reset-next'
WORK=ROOT/'work/w6ir'


def assert_owned(lane=EVIDENCE,source=SOURCE,work=WORK):
    if lane.resolve()!=(ROOT/'evidence/lanes/parallel-wave20261105/itcm-reset-next').resolve() or source.resolve()!=(ROOT/'src/runtime/parallel_wave20261105/itcm-reset-next').resolve() or not work.resolve().is_relative_to((ROOT/'work/w6ir').resolve()):raise ValueError('Exact ITCM reset source/evidence/work ownership differs')
    if not all(p.resolve().is_relative_to(ROOT.resolve()) for p in [lane,source,work]):raise ValueError('ITCM reset path escaped repository')


def assert_compile(source,directory):
    assert_owned()
    if not any(source.resolve().is_relative_to(p.resolve()) for p in [SOURCE,WORK]) or not directory.resolve().is_relative_to(WORK.resolve()):raise ValueError('ITCM reset compiler path escaped exclusive source/work')
