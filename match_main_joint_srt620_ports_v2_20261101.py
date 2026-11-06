from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import match_main_joint_srt620_20261101 as native
import check_main_joint_srt620_ports_v2_20261101 as ports


def main():
    native.main();ports.main()
    report=read_json(native.REPORT);port=ROOT/"evidence/ports/main-joint-srt620-windows-android-20261101.json";proof=read_json(port)
    assert proof["passed"]and proof["windowsActualPublicReturns"]==2304 and proof["windowsActualWrongCReturns"]==2304
    assert proof["android"]["deviceExecutions"]==0 and proof["android"]["compiledAndLinked"]
    dependencies=[port,Path(ports.__file__),ROOT/ports.COLLECTOR]
    known={row["path"]:row for row in report["replayDependencies"]}
    for path in dependencies:known[path.relative_to(ROOT).as_posix()]=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path))
    report.update(generator=Path(__file__).name,generatorSha256=sha256(__file__),replayDependencies=[known[p]for p in sorted(known)],
     portableValidation=dict(windowsPositiveCalls=2304,windowsWrongCalls=2304,
      wrongRejected=sum(c["rejected"]for c in proof["controls"]),windowsCaseSha256=proof["windowsCaseSha256"],
      androidTarget=proof["android"]["target"],androidCompiledAndLinked=True,androidDeviceExecutions=0,
      collectorExplicit=True,fullGame=False),reproductionCommand="python match_main_joint_srt620_ports_v2_20261101.py")
    write_json(ROOT/"evidence/matches/main-joint-srt620-ports-v2-20261101.json",report)
    print("JointSRT620 exactARM source and boundedWindows component;Android crossbuild only")


if __name__=="__main__":
    main()
