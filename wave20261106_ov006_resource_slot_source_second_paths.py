from project import ROOT
SOURCE=ROOT/'src/runtime/parallel_wave20261106/ov006-resource-slot-next/second'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/ov006-resource-slot-next/second'
WORK=ROOT/'work/w6rs/second'


def assert_owned(lane=EVIDENCE,source=SOURCE,work=WORK):
    if lane.resolve()!=EVIDENCE.resolve()or source.resolve()!=SOURCE.resolve()or not work.resolve().is_relative_to(WORK.resolve()):raise ValueError('Exact newly admitted overlay reuse scope differs')
    if not all(p.resolve().is_relative_to(ROOT.resolve())for p in[SOURCE,EVIDENCE,WORK]):raise ValueError('Overlay reuse workspace confinement differs')


def assert_compile(source,directory):
    assert_owned()
    if not any(source.resolve().is_relative_to(p.resolve())for p in[SOURCE,WORK])or not directory.resolve().is_relative_to(WORK.resolve()):raise ValueError('Overlay compiler escaped exact source/work ownership')
