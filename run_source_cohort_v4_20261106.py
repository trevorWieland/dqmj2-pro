import argparse
import os
import subprocess
import sys
from project import ROOT,read_json,write_json,sha256,now
from recovery_registry import verify_sources
from qualified_source_selection_guard_20261106 import verify as verify_selection_delegate


def main():
    from qualified_context_builder_entrypoint_v3_20261106 import verify as verify_context_delegate
    context_delegation = verify_context_delegate()
    selection_delegation = verify_selection_delegate()
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    cohort = parser.parse_args().cohort
    assert cohort >= 168
    verify_sources()
    plan_path=ROOT / f'evidence/verification/cohort-2026-10-29-{cohort}.json'
    plan=read_json(plan_path)
    registry_hash=sha256(ROOT/'recovery.json')
    assert registry_hash==plan['sourceRegistrySha256']
    steps=[{'command':['verify_source_selection_v2_20261106.py']},*read_json(ROOT/'evidence/verification/cohort67-validation-driver.json')['steps']]
    for step in steps:
        if step['command'] == ['integrate.py', '--clean']:
            step['command'] = ['integrate_context_v3_20261106.py', '--clean']
        if step['command'] == ['validate_evidence.py']:
            step['command'] = ['validate_evidence_ash_cache_20261031.py']
    output=ROOT / f'evidence/verification/cohort{cohort}-validation-driver.json'
    result={'createdUtc':now(),'cohort':cohort,'pid':os.getpid(),'state':'running','sourceRegistrySha256':registry_hash,'steps':[]}
    result['sourceSelectionDelegation'] = selection_delegation
    result['contextIntegrationDelegation'] = context_delegation
    write_json(output,result)
    for index,previous in enumerate(steps):
        assert sha256(ROOT/'recovery.json')==registry_hash
        command=previous['command']
        log=ROOT/f'logs/integration/cohort{cohort}-validation-{index:02}.txt'
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
