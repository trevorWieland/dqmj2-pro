from project import ROOT
SOURCE=ROOT/'src/runtime/parallel_wave20261106/ov001-state-controllers-next/second'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/ov001-state-controllers-next/second'
WORK=ROOT/'work/w6o1s/second'
def assert_owned(lane,source=SOURCE,work=WORK):
    if lane.resolve()!=EVIDENCE.resolve()or source.resolve()!=SOURCE.resolve()or not work.resolve().is_relative_to(WORK.resolve()):raise ValueError('Exact new ov001 source/evidence/work ownership differs')
    if not all(p.resolve().is_relative_to(ROOT.resolve())for p in[SOURCE,EVIDENCE,WORK]):raise ValueError('Ov001 workspace confinement differs')
def assert_compile(source,directory):
    assert_owned(EVIDENCE)
    if not any(source.resolve().is_relative_to(p.resolve())for p in[SOURCE,WORK])or not directory.resolve().is_relative_to(WORK.resolve()):raise ValueError('Ov001 compiler/materializer escaped ownership')
