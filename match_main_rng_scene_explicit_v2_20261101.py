from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import match_main_rng_scene_explicit_20261101 as native
import check_main_rng_scene_windows_20261101 as windows


def main():
    native.main();windows.main()
    report=read_json(native.REPORT)
    port=ROOT/"evidence/ports/main-rng-scene-windows-20261101.json";evidence=read_json(port)
    assert evidence["passed"]and evidence["actualPublicReturns"]==1152 and evidence["actualWrongPublicReturns"]==2304
    assert sum(r["rejected"]for r in evidence["controls"])==264
    dependencies=[port,Path(windows.__file__),ROOT/"src/ports/20261101_rng_scene/harness.c"]
    dependencies.extend(ROOT/source for source,alias in windows.SOURCES)
    known={r["path"]:r for r in report["replayDependencies"]}
    for path in dependencies:known[path.relative_to(ROOT).as_posix()]=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path))
    report.update(generator=Path(__file__).name,generatorSha256=sha256(__file__),
     replayDependencies=[known[path]for path in sorted(known)],
     portableValidation=dict(component="conditional RNG seed initialization",host="Windows x86_64",
      positiveActualReturns=1152,wrongActualReturns=2304,rejectedWrongResults=264,wholeGame=False,
      nativeTraceSha256=evidence["nativeTraceSha256"],windowsCaseSha256=evidence["windowsCaseSha256"]),
     reproductionCommand="python match_main_rng_scene_explicit_v2_20261101.py")
    write_json(ROOT/"evidence/matches/main-rng-scene-explicit-v2-20261101.json",report)
    print("RNG conditional-init exact96 migration plus native Windows component proof;zero new bytes")


if __name__=="__main__":
    main()
