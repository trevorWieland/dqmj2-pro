import json
import subprocess
import sys
from pathlib import Path
from project import ROOT,sha256,write_json

def main():
    names=['arm7_sdk262_element804_native_20261101.py','compile_arm7_sdk263_element804_20261101.py','link_arm7_sdk263_element804_20261101.py','match_arm7_sdk263_element804_20261101.py','validate_arm7_sdk265_element804_20261101.py','evidence/matches/arm7-sdk263-element804-20261101.json','evidence/verification/arm7-sdk265-element804-controls-20261101.json'];before={name:sha256(ROOT/name)for name in names};parent=(ROOT/'work/arm7-bulk-20261030').resolve();source=(parent/'sdk263-element804-final').resolve();destination=(parent/'sdk266-before-cold-element804').resolve()
    if source.parent!=parent or destination.parent!=parent or not source.is_relative_to(ROOT)or not destination.is_relative_to(ROOT)or destination.exists():raise ValueError('Explicit cold preservation paths unavailable')
    source.rename(destination)
    if source.exists():raise ValueError('Dedicated output path must be empty before full source replay')
    cwd=Path('C:/Users/trevo/Documents/Codex/2026-10-26/files-pasted-by-the-user-separate').resolve();argv=[sys.executable,str(ROOT/'validate_arm7_sdk265_element804_20261101.py')];result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=1800);directory=parent/'sdk266-cold-receipt';directory.mkdir(exist_ok=True);(directory/'stdout.txt').write_text(result.stdout,encoding='utf-8');(directory/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    if result.returncode:raise ValueError(result.stderr[-7000:])
    after={name:sha256(ROOT/name)for name in names}
    if before!=after:raise ValueError('Source/positive/controls changed during unrelated-CWD empty-WORK rebuild')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),before=before,after=after,preservedWork=destination.relative_to(ROOT).as_posix(),freshOutputPath=source.relative_to(ROOT).as_posix(),explicitEmptyWorkBeforeExecution=True,actualArgv=argv,actualCwd=str(cwd),exitCode=result.returncode,stdout=result.stdout,allProductsRebuiltWithoutCopyingWorkInputs=True,wholeModuleAcceptancePending=True,sourceCredit=0);path=ROOT/'evidence/verification/arm7-sdk266-element804-cold-20261101.json';write_json(path,report);print(json.dumps(dict(report=path.relative_to(ROOT).as_posix(),sha256=sha256(path))),flush=True)

if __name__=='__main__':main()
