from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import match_main_anim_graph1004_20261102 as native
import check_main_anim_graph1004_windows32_20261102 as ports


def main():
    native.main();ports.main()
    report=read_json(native.REPORT);proof=read_json(ports.REPORT)
    assert proof['passed']and proof['actualWindowsGameFunctionReturns']==640 and proof['actualWrongPublicReturns']==3840
    known={row['path']:row for row in report['replayDependencies']}
    for path in[ports.REPORT,Path(ports.__file__),ROOT/ports.DRIVER,ROOT/ports.DICTIONARY]:
        known[path.relative_to(ROOT).as_posix()]=dict(path=path.relative_to(ROOT).as_posix(),sha256=sha256(path))
    report.update(generator=Path(__file__).name,generatorSha256=sha256(__file__),replayDependencies=[known[p]for p in sorted(known)],
     candidateNewFunctions=5,candidateNewBytes=928,zeroCreditMigration=dict(module='main',mode='arm',address='0x020343FC',bytes=76,
      reason='Shared typed void callback interface, identical native bytes, old raw-view source retained; no named selected incoming C calls'),
     portableValidation=dict(windowsTarget='i686-pc-windows-msvc',actualPublicReturns=640,actualWrongPublicReturns=3840,
      reconstructedBodiesCompiled=6,selectedDictionaryCompiled=True,explicitCpuFillBackend=True,relocatedInitFunctionPointers=True,
      storedNativeCalculationIdsNeverInvoked=True,windowsCaseSha256=proof['windowsCaseSha256'],fullGame=False,androidDeviceExecutions=0),
     reproductionCommand='python match_main_anim_graph1004_ports_20261102.py')
    write_json(ROOT/'evidence/matches/main-anim-graph1004-ports-20261102.json',report)
    print('Five new ARM C bodies928B plus zero-credit76B callback migration; actual Windows32 component graph passes')


if __name__=='__main__':
    main()
