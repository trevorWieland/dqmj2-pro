import json
import subprocess
import sys
from pathlib import Path
from project import ROOT,sha256,write_json

def main():
    names=['arm7_sdk273_frame_constructors_native_20261101.py','compile_arm7_sdk274_frame_builders_20261101.py','link_arm7_sdk274_frame_builders_20261101.py','match_arm7_sdk274_frame_builders_20261101.py','validate_arm7_sdk275_frame_builders_20261101.py','evidence/matches/arm7-sdk274-frame-builders1304-20261101.json','evidence/verification/arm7-sdk275-frame-builders1304-controls-20261101.json'];before={name:sha256(ROOT/name)for name in names};parent=(ROOT/'work/arm7-bulk-20261030').resolve();source=(parent/'sdk274-frame-builders1304-final').resolve();destination=(parent/'sdk276-before-cold-frame-builders').resolve()
    if source.parent!=parent or destination.parent!=parent or not source.is_relative_to(ROOT)or not destination.is_relative_to(ROOT)or destination.exists():raise ValueError('Explicit frame cold preservation paths unavailable')
    source.rename(destination)
    if source.exists():raise ValueError('Dedicated frame WORK path must be absent')
    cwd=Path('C:/Users/trevo/Documents/Codex/2026-10-26/files-pasted-by-the-user-separate').resolve();argv=[sys.executable,str(ROOT/'validate_arm7_sdk275_frame_builders_20261101.py')];result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=2400);directory=parent/'sdk276-cold-receipt';directory.mkdir(exist_ok=True);(directory/'stdout.txt').write_text(result.stdout,encoding='utf-8');(directory/'stderr.txt').write_text(result.stderr,encoding='utf-8')
    if result.returncode:raise ValueError(result.stderr[-7000:])
    after={name:sha256(ROOT/name)for name in names}
    if before!=after:raise ValueError('Source/positive/control hashes changed after unrelated-CWD empty-WORK replay')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),before=before,after=after,preservedWork=destination.relative_to(ROOT).as_posix(),freshOutputPath=source.relative_to(ROOT).as_posix(),explicitEmptyWorkBeforeExecution=True,actualArgv=argv,actualCwd=str(cwd),exitCode=result.returncode,stdout=result.stdout,allProductsRebuiltWithoutCopyingWorkInputs=True,wholeModuleAcceptancePending=True,sourceCredit=0);path=ROOT/'evidence/verification/arm7-sdk276-frame-builders1304-cold-20261101.json';write_json(path,report);print(json.dumps(dict(report=path.relative_to(ROOT).as_posix(),sha256=sha256(path))),flush=True)

if __name__=='__main__':main()
