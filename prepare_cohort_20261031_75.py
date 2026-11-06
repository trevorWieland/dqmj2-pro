from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-va-adapter-20261031','match_main_va_adapter_20261031.py',False),
 ('arm7-lane-arena120-20261031','match_arm7_lane_arena_20261031.py',True),
 ('arm7-lane-thread-lists372-20261031','match_arm7_lane_thread_lists_20261031.py',True),
 ('mechanics-save-20261031-lane-resource-metric','match_mechanics_save_20261031_lane_resource_metric.py',False),
 ('mechanics-save-20261031-lane-coordinate-bridge','match_mechanics_save_20261031_lane_coordinate_bridge.py',False),
 ('mechanics-save-20261031-lane-feature-aggregate','match_mechanics_save_20261031_lane_feature_aggregate.py',False),
 ('ov001-20261031-statea103','reproduce_overlay_counter103_20261031.py',True),
 ('ov001-20261031-stateb103','reproduce_overlay_counter103_20261031.py',True),
 ('ov001-20261031-sweep110','match_ov001_sweep110_20261031.py',False),
 ('ov000-20261031-setup116','match_ov000_setup116_20261031.py',False),
 ('ov006-20261031-restore117-linked','reproduce_ov006_restore117_linked_20261031.py',True),
]
BASE=ROOT/'evidence/verification/cohort75-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-74.json');verify_sources();assert not old['linksPending']
    assert sha256(ROOT/'recovery.json')==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8848
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
    for label,producer in [('arm7-lane-arena120','validate_arm7_lane_arena_20261031.py'),('arm7-lane-thread-lists372','validate_arm7_lane_thread_lists_20261031.py')]:
        path=f'evidence/verification/{label}-controls-20261031.json';oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(ROOT/'recovery.json',registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==17 and new_bytes==2492
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=17,newOrdinaryCBytes=2492,newSourceBytes=2492,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8865,expectedSourceLinkedBytes=657277,preferredSourceInputsRequired=27,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=74,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-75.json',plan);print({'newFunctions':17,'newOrdinaryCBytes':2492,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


if __name__=='__main__':
    main()
