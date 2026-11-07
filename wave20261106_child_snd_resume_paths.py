from project import ROOT
SOURCE=ROOT/'src/utility/parallel_wave20261106/child-snd-resume-next'
EVIDENCE=ROOT/'evidence/lanes/parallel-wave20261106/child-snd-resume-next'
WORK=ROOT/'work/w6sr'


def assert_owned(lane=EVIDENCE,source=SOURCE,work=WORK):
    if lane.resolve()!=EVIDENCE.resolve()or source.resolve()!=SOURCE.resolve()or not work.resolve().is_relative_to(WORK.resolve()):raise ValueError('Exact newly admitted SND scope differs')
    if not all(p.resolve().is_relative_to(ROOT.resolve())for p in[SOURCE,EVIDENCE,WORK]):raise ValueError('SND workspace confinement differs')


def assert_compile(source,directory):
    assert_owned()
    if not any(source.resolve().is_relative_to(p.resolve())for p in[SOURCE,WORK])or not directory.resolve().is_relative_to(WORK.resolve()):raise ValueError('SND compiler escaped source/work ownership')
