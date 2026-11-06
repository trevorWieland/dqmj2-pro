import json
from pathlib import Path
import subprocess
import sys
import time
from project import ROOT,sha256,write_json

def run():
    p=subprocess.run([sys.executable,str(ROOT/'validate_arm7_sdk313_task_command_family_20261102.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=420)
    if p.returncode:raise ValueError(p.stdout+p.stderr)
    return p.stdout

def main():
    warm=run();report=ROOT/'evidence/matches/arm7-sdk312-task-command-family1224-20261102.json';controls=ROOT/'evidence/verification/arm7-sdk313-task-command-controls-20261102.json';before=(sha256(report),sha256(controls));work=(ROOT/'work/arm7-bulk-20261030/sdk312-task-command-family').resolve();parent=(ROOT/'work/arm7-bulk-20261030').resolve();archive=(parent/'sdk314-cold-archives'/str(time.time_ns())).resolve()
    if work!=parent/'sdk312-task-command-family'or not archive.is_relative_to(parent)or not work.is_dir()or work.is_junction()or work.is_symlink():raise ValueError('Exact source-only WORK/archive path guard failed')
    archive.parent.mkdir(parents=True,exist_ok=True);work.rename(archive)
    if work.exists():raise ValueError('Dedicated matcher WORK is not empty')
    cold=run();after=(sha256(report),sha256(controls))
    if before!=after:raise ValueError('Unrelated-CWD empty-WORK replay changed current measurements/products')
    result=dict(generator=Path(__file__).name,generatorSha256=sha256(__file__),entry='python validate_arm7_sdk313_task_command_family_20261102.py',actualCwd=str(ROOT.parent),dedicatedWork='work/arm7-bulk-20261030/sdk312-task-command-family',priorProductsPreservedOutsideDedicatedWork=True,noCachedProductsCopied=True,canonicalReportSha256=after[0],controlsSha256=after[1],sameCanonicalAndControlBytes=True,warmStdout=warm,coldStdout=cold,sourceCreditPendingIntegratorModuleAcceptance=0);write_json(ROOT/'evidence/verification/arm7-sdk314-task-command-cold-20261102.json',result);print(json.dumps(dict(reportSha256=after[0],controlsSha256=after[1],coldReportSha256=sha256(ROOT/'evidence/verification/arm7-sdk314-task-command-cold-20261102.json'),sameBytes=True)),flush=True)

if __name__=='__main__':main()
