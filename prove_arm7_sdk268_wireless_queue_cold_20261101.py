import json
import subprocess
import sys
from pathlib import Path
from project import ROOT,sha256,write_json

def main():
    names=['nonmatching/arm7-bulk/20261101/lane-sdk264-wireless-large-ready/profile.json','replay_arm7_sdk264_wireless_large_queue_20261101.py','validate_arm7_sdk264_wireless_large_queue_20261101.py','evidence/attempts/arm7-sdk264-wireless-large-ready-replay-20261101.json','evidence/verification/arm7-sdk264-wireless-large-queue-controls-20261101.json'];before={name:sha256(ROOT/name)for name in names};parent=(ROOT/'work/arm7-bulk-20261030').resolve();source=(parent/'sdk264-wireless-large-ready-replay').resolve();destination=(parent/'sdk268-before-cold-queue').resolve()
    if source.parent!=parent or destination.parent!=parent or not source.is_relative_to(ROOT)or not destination.is_relative_to(ROOT)or destination.exists():raise ValueError('Explicit queue cold preservation paths unavailable')
    source.rename(destination)
    if source.exists():raise ValueError('Dedicated queue output must be absent')
    cwd=Path('C:/Users/trevo/Documents/Codex/2026-10-26/files-pasted-by-the-user-separate').resolve();argv=[sys.executable,str(ROOT/'validate_arm7_sdk264_wireless_large_queue_20261101.py')];result=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,timeout=300)
    if result.returncode:raise ValueError(result.stderr[-7000:])
    after={name:sha256(ROOT/name)for name in names}
    if before!=after:raise ValueError('Source/profile/compiler evidence differs after unrelated-CWD empty-WORK rebuild')
    report=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),before=before,after=after,preservedWork=destination.relative_to(ROOT).as_posix(),emptyWorkBeforeExecution=True,actualArgv=argv,actualCwd=str(cwd),exitCode=0,stdout=result.stdout,noWorkInputsCopied=True,sourceCredit=0);path=ROOT/'evidence/verification/arm7-sdk268-wireless-large-cold-20261101.json';write_json(path,report);print(json.dumps(dict(report=path.relative_to(ROOT).as_posix(),sha256=sha256(path))),flush=True)

if __name__=='__main__':main()
