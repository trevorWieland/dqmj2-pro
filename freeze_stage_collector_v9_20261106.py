import argparse
from project import ROOT,read_json,write_json,sha256,now
from qualify_oracle_path_cache_v3_20261106 import LANE
import stage_declared_source_package_v9_20261106 as stage


OUTPUT=LANE/'stage-v9-handoff.json'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');args=parser.parse_args();proof=read_json(LANE/'stage-v9-compatibility.json');collector=read_json(LANE/'collector-v3-qualification.json')
    if not proof['passed'] or not collector['passed'] or proof['sourceCredit'] or collector['sourceCredit'] or proof['gitCallsPerFixture']!=4 or not all(proof[k] for k in ['gitBoundaryOnlyMocked','exactFullGitArgvStdinOrderEqual','exactCapturedClosureAndDeclaredReferenceDiagnosticMetadataEqual','collectorRestoredAfterSuccess','originalFailurePropagatedAndCollectorRestored']):raise ValueError('Qualified collector/stager scope differs')
    if proof['newStageSha256']!=sha256(ROOT/'stage_declared_source_package_v9_20261106.py') or proof['generatorSha256']!=sha256(ROOT/'verify_stage_collector_v9_20261106.py'):raise ValueError('New stager/fixture source changed')
    for name,digest in stage.PINS.items():
        if sha256(ROOT/name)!=digest:raise ValueError('Staging/collector/guard pin differs: '+name)
    for row in collector['files']:
        if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen full collector qualification changed: '+row['path'])
    if args.verify:
        result=read_json(OUTPUT)
        for row in result['files']:
            if sha256(ROOT/row['path'])!=row['sha256']:raise ValueError('Frozen stagehandoff file changed: '+row['path'])
    else:
        if OUTPUT.exists():raise ValueError('Stagev9handoff already frozen; use --verify')
        names=['stage_declared_source_package_v9_20261106.py','verify_stage_collector_v9_20261106.py','freeze_stage_collector_v9_20261106.py']+list(stage.PINS)+[(LANE/name).relative_to(ROOT).as_posix() for name in ['collector-v3-qualification.json','stage-v9-compatibility.json']]
        write_json(OUTPUT,dict(passed=True,sourceCredit=0,frozenUtc=now(),files=[dict(path=name,sha256=sha256(ROOT/name)) for name in dict.fromkeys(names)],collectorPaths=22833,collectorOutputSha256=collector['fullClosureSha256'],meaningfulLookupControls=16,stageGitBoundaryCases=4,successFailureRestoration=True,coordinatorReviewRequiredBeforeProductionAdoption=True,productionAdopted=False,currentWrappersAndJobsAndGitIndexUntouched=True,entry=['python','stage_declared_source_package_v9_20261106.py','<declared-source-package.json>'],privateCompatibilityCli=['python','verify_stage_collector_v9_20261106.py'],integrationSteps=['Root reviews and selects the new thin delegate only before a future capture starts.','Stage all new runtime helpers and qualification receipts; preserve original/v2/v3/v7/v8 files.','If164capture has begun, retain its selectedcollector and use165or later; never interrupt a current job.'],limits=['Guarded static source-closure/staging qualification only; native/source/data/ROM credit remains0.','Historicalv2/v3 fulltimings were not consecutive paired runs; no universal production speed promise.']))
    print(dict(passed=True,path=OUTPUT.relative_to(ROOT).as_posix(),sha256=sha256(OUTPUT)))


if __name__=='__main__':main()
