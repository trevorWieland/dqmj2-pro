from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import match_main_joint_scale336_20261102 as native
import check_main_joint_scale336_windows32_20261102 as ports


def main():
    native.main();ports.main()
    report=read_json(native.REPORT);proof=read_json(ports.REPORT)
    assert proof['passed']and proof['actualPublicReturns']==2048 and proof['actualWrongPublicReturns']==6144
    known={r['path']:r for r in report['replayDependencies']}
    for path in[ports.REPORT,Path(ports.__file__),ports.DRIVER]:known[path.relative_to(ROOT).as_posix()]=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path))
    report.update(generator=Path(__file__).name,generatorSha256=sha256(__file__),replayDependencies=[known[p]for p in sorted(known)],
     portableValidation=dict(target='i686-pc-windows-msvc',actualPublicReturns=2048,actualWrongPublicReturns=6144,
      windowsCaseSha256=proof['windowsCaseSha256'],sourceBodyIncludedUnmodified=True,globalStorageExplicit=True,fullGame=False),
     reproductionCommand='python match_main_joint_scale336_ports_20261102.py')
    write_json(ROOT/'evidence/matches/main-joint-scale336-ports-20261102.json',report)
    print('JointScale336 exact ARM source and actual Windows32 state/cache effects pass')


if __name__=='__main__':
    main()
