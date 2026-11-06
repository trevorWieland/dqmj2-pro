import json
import subprocess
import sys
from pathlib import Path
from project import ROOT,sha256,write_json

def main():
    scripts=['match_arm7_sdk249_rates180_20261101.py','match_arm7_sdk251_parameters_20261101.py','validate_arm7_sdk252_rates_parameters400_20261101.py'];reports=['evidence/matches/arm7-sdk249-rates180-20261101.json','evidence/matches/arm7-sdk251-parameters220-20261101.json'];before={name:sha256(ROOT/name)for name in scripts+reports};preserved=[]
    parent=(ROOT/'work/arm7-bulk-20261030').resolve();archive=parent/'sdk253-before-cold';archive.mkdir(exist_ok=True)
    for name in('sdk249-rates180-final','sdk251-parameters220-final'):
        source=(parent/name).resolve();destination=(archive/name).resolve()
        if source.parent!=parent or not source.is_relative_to(ROOT)or destination.parent!=archive or not destination.is_relative_to(ROOT)or destination.exists():raise ValueError('Explicit cold-work preservation paths unavailable')
        source.rename(destination);preserved.append(dict(original=source.relative_to(ROOT).as_posix(),preserved=destination.relative_to(ROOT).as_posix(),freshWorkAbsent=not source.exists()))
    cwd=Path('C:/Users/trevo/Documents/Codex/2026-10-26/files-pasted-by-the-user-separate').resolve()
    if cwd==ROOT or not cwd.is_dir():raise ValueError('Independent existing CWD unavailable')
    argv=[sys.executable,str(ROOT/scripts[2])];result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=1200);directory=parent/'sdk253-cold-receipt';directory.mkdir(exist_ok=True);(directory/'stdout.txt').write_text(result.stdout,encoding='utf-8');(directory/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    if result.returncode:raise ValueError(result.stderr[-7000:])
    after={name:sha256(ROOT/name)for name in scripts+reports}
    if before!=after:raise ValueError('Frozen source/report changed during unrelated-CWD empty-WORK source rebuild')
    controls=ROOT/'evidence/verification/arm7-sdk252-rates-parameters400-controls-20261101.json';report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),before=before,after=after,explicitEmptyWork=preserved,actualArgv=argv,actualCwd=str(cwd),exitCode=result.returncode,stdout=result.stdout,controlsSha256=sha256(controls),allProductsRebuiltWithoutCopyingWorkInputs=True,wholeModuleAcceptancePending=True,sourceCredit=0)
    path=ROOT/'evidence/verification/arm7-sdk253-rates-parameters400-cold-20261101.json';write_json(path,report);print(json.dumps(dict(report=path.relative_to(ROOT).as_posix(),sha256=sha256(path),controlsSha256=sha256(controls))),flush=True)

if __name__=='__main__':main()
