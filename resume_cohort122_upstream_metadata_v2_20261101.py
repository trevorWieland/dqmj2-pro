import ast
import subprocess
import sys
from pathlib import Path
from project import ROOT,read_json,write_json,sha256,now
from verify_frozen_sdk_wrap_metadata_v2_20261101 import classify


def main():
    driver=read_json(ROOT/'evidence/verification/cohort122-continuation-driver-v12-20261101.json')
    assert driver['state']=='failed'and len(driver['steps'])==5
    assert all(row['exitCode']==0 for row in driver['steps'][:4])and driver['steps'][4]['exitCode']!=0
    for row in driver['steps']:assert sha256(ROOT/row['log'])==row['logSha256']
    plan=read_json(ROOT/'evidence/verification/cohort-2026-10-29-122.json')
    assert not plan['linksPending']and plan['sourceMatchedFunctions']==9312 and plan['sourceLinkedBytes']==725103
    assert sha256(ROOT/'recovery.json')==plan['sourceRegistrySha256']
    assert sha256(ROOT/'source-preferences.json')==plan['sourcePreferenceSha256']
    original=(ROOT/driver['steps'][4]['log']).read_text(encoding='utf-8')
    findings=ast.literal_eval(original.split('AssertionError: ',1)[1])
    before=[row for row in findings if not row['classified']]
    assert len(before)==2
    classify(findings);assert all(row['classified']for row in findings)
    altered=dict(before[0],sha256='0'*64,classified=False)
    try:classify([altered])
    except AssertionError:pass
    else:raise AssertionError('Changed upstream metadata hash was classified')
    unknown=dict(path='src/arbitrary.c',sha256='0'*64,classified=False)
    classify([unknown]);assert not unknown['classified']
    receipt=ROOT/'evidence/verification/cohort122-upstream-metadata-resume-v2-20261101.json'
    result=dict(cohort=122,sourceCredit=0,startedUtc=now(),generator=Path(__file__).name,
        generatorSha256=sha256(__file__),state='running',reusedFourSuccessfulSteps=driver['steps'][:4],
        originalFailedDriverPreserved=True,upstreamMetadata=findings[:2],changedHashAndArbitrarySourceControlsPassed=True,
        sourceRegistryPreferenceAndCodeUnchanged=True)
    write_json(receipt,result)
    command=[sys.executable,str(ROOT/'finish_source_package_v12_20261101.py'),'--cohort','122',
        '--stage','stage_cohort122_family_v3_20261101.py','--document',
        'docs/2026-11-01-cohort122-family-sources-and-interface-migrations.md','--label','family-sources']
    log=ROOT/'logs/integration/cohort122-upstream-metadata-resume-v2-20261101.txt'
    with log.open('w',encoding='utf-8')as stream:run=subprocess.run(command,cwd=ROOT,stdout=stream,stderr=subprocess.STDOUT)
    result.update(state='packaged'if run.returncode==0 else'failed',exitCode=run.returncode,finishedUtc=now(),
        actualFinisherCommand=command,log=log.relative_to(ROOT).as_posix(),logSha256=sha256(log))
    write_json(receipt,result)
    print(dict(cohort=122,state=result['state'],sourceValidationPreserved=True))
    raise SystemExit(run.returncode)


if __name__=='__main__':
    main()
