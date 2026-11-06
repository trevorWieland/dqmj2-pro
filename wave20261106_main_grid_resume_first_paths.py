from project import ROOT

SOURCE=ROOT/'src/runtime/parallel_wave20261106/main-grid-resume-next/first'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/main-grid-resume-next/first'
WORK=ROOT/'work/w6gg/first'


def assert_owned(lane,source=SOURCE,work=WORK):
    if lane.resolve()!=EVIDENCE.resolve() or source.resolve()!=SOURCE.resolve() or not work.resolve().is_relative_to(WORK.resolve()):raise ValueError('Exact new record source/evidence/work ownership differs')
    if not all(p.resolve().is_relative_to(ROOT.resolve()) for p in [SOURCE,EVIDENCE,WORK]):raise ValueError('Record materializer workspace confinement differs')


def assert_compile(source,directory):
    assert_owned(EVIDENCE)
    if not any(source.resolve().is_relative_to(p.resolve()) for p in [SOURCE,WORK]) or not directory.resolve().is_relative_to(WORK.resolve()):raise ValueError('Record compiler/materializer path escaped exact new source/work scope')
