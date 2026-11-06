from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import match_main_resource_binding1808_20261102 as native
import check_main_resource_binding1808_windows32_v2_20261102 as ports


def main():
    native.main();ports.main()
    report=read_json(native.REPORT);proof=read_json(ports.REPORT)
    assert proof['passed']and proof['actualPreferredPublicCalls']==4352 and proof['actualWrongPublicCalls']==21760
    assert proof['preferred']['actualCompiledDivisionSetterCalls']==1892
    known={r['path']:r for r in report['replayDependencies']}
    for path in[ports.REPORT,Path(ports.__file__),ports.DRIVER]:known[path.relative_to(ROOT).as_posix()]=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path))
    report.update(generator=Path(__file__).name,generatorSha256=sha256(__file__),replayDependencies=[known[p]for p in sorted(known)],
     portableValidation=dict(target='i686-pc-windows-msvc',actualPreferredPublicCalls=4352,actualWrongPublicCalls=21760,
      actualCompiledDivisionSetterCalls=1892,hardwareModeledAfterCompiledSetter=True,
      nativeControlSubsetsExact=True,sourceBodiesIncludedUnmodified=True,fullGame=False,renderedScene=False),
     reproductionCommand='python match_main_resource_binding1808_ports_20261102.py')
    write_json(ROOT/'evidence/matches/main-resource-binding1808-ports-20261102.json',report)
    print('Resource1808 exact ARM source and actual Windows32 data/backend effects pass')


if __name__=='__main__':
    main()
