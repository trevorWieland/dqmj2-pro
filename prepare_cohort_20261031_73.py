from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-record-init-20261031','match_main_record_init_20261031.py',False),
 ('main-range-map-20261031','match_main_range_map_20261031.py',False),
 ('main-resource-load-20261031','match_main_resource_load_20261031.py',False),
 ('arm7-lane-sdk-state196-20261031','match_arm7_lane_sdk_state_20261031.py',True),
 ('arm7-lane-sdk-flow328-20261031','match_arm7_lane_sdk_flow_20261031.py',True),
 ('mechanics-save-20261031-lane-resource-readers','match_mechanics_save_20261031_lane_resource_readers.py',False),
 ('ov005-20261031-table73','match_ov005_table73_20261031.py',False),
 ('ov005-20261031-pause81','match_ov005_pause81_20261031.py',False),
]
BASE=ROOT/'evidence/verification/cohort73-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-72.json');verify_sources();assert not old['linksPending']
    assert sha256(ROOT/'recovery.json')==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8820
    fields=['module','mode','address','size','source','sourceSha256','object','objectSha256','targetSha256','report']
    write_json(BASE,{'sourceRegistrySha256':sha256(ROOT/'recovery.json'),'preferencesSha256':sha256(ROOT/'source-preferences.json'),'selected':[{'key':list(key),**{f:r[f] for f in fields if f in r}} for key,r in before.items()]})
    reports=[]
    for name,producer,raw in PACKETS:
        path=f'evidence/matches/{name}.json'
        if raw:register(path,[producer])
        else:
            seal_sources(path,[producer]);register(path,['seal_recovery_sources_20261031.py',path,producer])
        reports.append(path)
    registry=read_json(ROOT/'recovery.json');oracles={r['report']:r for r in registry['oracles']}
    for label,producer in [('arm7-lane-sdk-state196','validate_arm7_lane_sdk_state_20261031.py'),('arm7-lane-sdk-flow328','validate_arm7_lane_sdk_flow_20261031.py')]:
        path=f'evidence/verification/{label}-controls-20261031.json';oracles[path]={'report':path,'reproduce':[producer]}
    oracles['evidence/arm7/sdk-division-scope-20261031.json']={'report':'evidence/arm7/sdk-division-scope-20261031.json','reproduce':['arm7_lane_sdk_division_scope_20261031.py']}
    oracles['evidence/verification/arm7-division-inventory-amendment-20261031.json']={'report':'evidence/verification/arm7-division-inventory-amendment-20261031.json','reproduce':['amend_arm7_division_inventory_20261031.py']}
    registry['oracles']=list(oracles.values());write_json(ROOT/'recovery.json',registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==12 and new_bytes==1344
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=12,newOrdinaryCBytes=1344,newSourceBytes=1344,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8832,expectedSourceLinkedBytes=651517,preferredSourceInputsRequired=27,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=72,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-73.json',plan);print({'newFunctions':12,'newOrdinaryCBytes':1344,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


if __name__=='__main__':
    main()
