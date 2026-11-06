import subprocess
import sys
from project import ROOT,read_json,write_json,sha256,now


def main():
    previous_name='evidence/verification/cohort172-continuation-driver-v44-20261105.json'
    previous=read_json(ROOT/previous_name)
    assert previous['state']=='failed'and len(previous['steps'])==5
    assert all(s['exitCode']==0 for s in previous['steps'][:4])and previous['steps'][-1]['exitCode']==1
    assert previous['steps'][-1]['command'][0]=='finish_source_package_v25_20261106.py'
    for step in previous['steps']:assert sha256(ROOT/step['log'])==step['logSha256']
    validation=read_json(ROOT/'evidence/verification/cohort172-validation-driver.json')
    assert validation['state']=='build-and-regression-checks-passed'and len(validation['steps'])==16
    for step in validation['steps']:
        assert step['exitCode']==0 or step.get('externalApplicationSnapshotDifferences')is True
        assert sha256(ROOT/step['log'])==step['logSha256']
    plan=read_json(ROOT/'evidence/verification/cohort-2026-10-29-172.json')
    assert not plan['linksPending']and plan['newSourceFunctions']==30 and plan['newSourceBytes']==8720
    assert sha256(ROOT/'recovery.json')==plan['sourceRegistrySha256']
    assert sha256(ROOT/'source-preferences.json')==plan['sourcePreferenceSha256']
    repair_name='evidence/verification/cohort172-superseded-index-repair-v1-20261106.json'
    repair=read_json(ROOT/repair_name);assert repair['passed']and repair['originalGuardUnchanged']and repair['workingFilesUnchanged']
    assert len(repair['unstagedOnly'])==9
    assert not subprocess.check_output(['git','diff','--cached','--name-only','--','src/runtime/parallel_wave20261106/gp-core-resume-next/first/'],cwd=ROOT,text=True).strip()
    output=ROOT/'evidence/verification/cohort172-sealing-resume-v1-20261106.json';assert not output.exists()
    command=['finish_source_package_v25_20261106.py','--cohort','172','--stage','stage_parallel_packet_wave172_v2_20261106.py','--document','docs/2026-11-06-parallel-wave-q-acceptance.md','--label','parallel-wave-q']
    result=dict(state='running',sourceCredit=0,startedUtc=now(),previousTerminalFailedDriver=previous_name,previousDriverSha256=sha256(ROOT/previous_name),originalSixteenSharedStagesCompleted=True,preparationPublicationValidationFinalizationNotRepeated=True,originalPackagingStageAndBothCommittedAuditsWillRun=True,originalFinisherUnchanged=True,indexRepair=repair_name,indexRepairSha256=sha256(ROOT/repair_name),command=command)
    write_json(output,result)
    log=ROOT/'logs/integration/cohort172-sealing-resume-v1-20261106.txt'
    with log.open('w',encoding='utf-8')as stream:run=subprocess.run([sys.executable,str(ROOT/command[0]),*command[1:]],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    result.update(state='packaged'if run.returncode==0 else'failed',finishedUtc=now(),exitCode=run.returncode,log=log.relative_to(ROOT).as_posix(),logSha256=sha256(log));write_json(output,result)
    if run.returncode:raise SystemExit(run.returncode)
    receipt='evidence/verification/cohort172-expanded-source-closure-20261101.json';assert read_json(ROOT/receipt)['passed']
    assert subprocess.check_output(['git','show','HEAD:'+receipt],cwd=ROOT)==(ROOT/receipt).read_bytes()
    result['committedClosureVerified']=True;write_json(output,result)


if __name__=='__main__':main()
