import os
import subprocess
import sys
from project import ROOT,read_json,write_json,sha256,now
from recovery_registry import verify_sources


def main():
    verify_sources()
    plan_path=ROOT/'evidence/verification/cohort-2026-10-29-75.json'
    plan=read_json(plan_path)
    registry_hash=sha256(ROOT/'recovery.json')
    assert registry_hash==plan['sourceRegistrySha256']
    steps=[{'command':['verify_source_selection.py']},*read_json(ROOT/'evidence/verification/cohort67-validation-driver.json')['steps']]
    output=ROOT/'evidence/verification/cohort75-validation-driver.json'
    result={'createdUtc':now(),'cohort':75,'pid':os.getpid(),'state':'running','sourceRegistrySha256':registry_hash,'steps':[]}
    write_json(output,result)
    for index,previous in enumerate(steps):
        assert sha256(ROOT/'recovery.json')==registry_hash
        command=previous['command']
        log=ROOT/f'logs/integration/cohort75-validation-{index:02}.txt'
        result['currentCommand']=command
        result['currentCommandStartedUtc']=now()
        write_json(output,result)
        print({'step':index,'command':command},flush=True)
        with log.open('w',encoding='utf-8') as stream:
            run=subprocess.run([sys.executable,str(ROOT/command[0]),*command[1:]],cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
        row={'command':command,'exitCode':run.returncode,'log':log.relative_to(ROOT).as_posix(),'logSha256':sha256(log)}
        result['steps'].append(row)
        if run.returncode:
            if command==['verify_workspace.py']:
                workspace=read_json(ROOT/'evidence/verification/workspace.json')
                allowed=workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged'] is True and workspace['isolation']['auditAvailable'] and not workspace['gitRemotes'] and workspace['isolation']['applicationObservedUnchanged'] is False
                row['externalApplicationSnapshotDifferences']=allowed
                if allowed:
                    write_json(output,result)
                    continue
            result['state']='failed'
            write_json(output,result)
            print(log.read_text(encoding='utf-8')[-5000:],flush=True)
            raise SystemExit(run.returncode)
        write_json(output,result)
    manifest=read_json(ROOT/'manifest.json')
    assert manifest['functionMatched']==plan['expectedSourceMatchedFunctions']
    assert manifest['sourceLinkedBytes']==plan['expectedSourceLinkedBytes']
    assert manifest['exactContainerMatchWithScaffolding'] is True
    assert not manifest['rejectedMatchEvidence']
    result['state']='build-and-regression-checks-passed'
    result['finishedUtc']=now()
    result['sourceMatchedFunctions']=manifest['functionMatched']
    result['sourceLinkedBytes']=manifest['sourceLinkedBytes']
    result.pop('currentCommand',None)
    result.pop('currentCommandStartedUtc',None)
    write_json(output,result)
    print({key:result[key] for key in ['state','sourceMatchedFunctions','sourceLinkedBytes']},flush=True)


if __name__=='__main__':
    main()
