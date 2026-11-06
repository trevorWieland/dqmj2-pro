from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import match_main_animation_obj352_20261101 as native
import check_main_animation_obj352_windows_20261101 as ports


def main():
    native.main();ports.main()
    report=read_json(native.REPORT);proof=read_json(ports.REPORT)
    assert proof['passed']and proof['actualPublicReturns']==4929 and proof['actualWrongPublicReturns']==19716
    dependencies=[ports.REPORT,Path(ports.__file__),ROOT/'src/ports/20261101_animation_obj352/dispatch.c']
    known={row['path']:row for row in report['replayDependencies']}
    for path in dependencies:known[path.relative_to(ROOT).as_posix()]=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path))
    report.update(generator=Path(__file__).name,generatorSha256=sha256(__file__),replayDependencies=[known[p]for p in sorted(known)],
     portableValidation=dict(windowsPositiveCalls=4929,windowsWrongCalls=19716,
      wrongRejected=sum(c['execution']['rejected']for c in proof['controls']),windowsCaseSha256=proof['windowsCaseSha256'],
      originalSourceBodiesCompiled=True,fixedLowGuestDataMapping=True,androidDeviceExecutions=0,fullGame=False),
     reproductionCommand='python match_main_animation_obj352_ports_20261101.py')
    write_json(ROOT/'evidence/matches/main-animation-obj352-ports-20261101.json',report)
    print('AnimationObj352 exact ARM source and actual Windows component execution; full game remains unproved')


if __name__=='__main__':
    main()
