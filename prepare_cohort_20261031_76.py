from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-range-reader-20261031','match_main_range_reader_20261031.py',False),
 ('arm7-lane-thread-scheduling344-20261031','match_arm7_lane_thread_scheduling_20261031.py',True),
 ('arm7-lane-messages412-20261031','match_arm7_lane_messages_20261031.py',True),
 ('arm7-lane-mutex-release152-20261031','match_arm7_lane_mutex_release_20261031.py',True),
 ('arm7-lane-child-typed180-20261031','match_arm7_lane_child_typed_20261031.py',True),
 ('arm7-lane-thread-create264-20261031','match_arm7_lane_thread_create_20261031.py',True),
 ('mechanics-save-20261031-lane-feature-siblings','match_mechanics_save_20261031_lane_feature_siblings.py',False),
 ('mechanics-save-20261031-lane-stat-clamps','match_mechanics_save_20261031_lane_stat_clamps.py',False),
 ('mechanics-save-20261031-lane-stat-scaling','match_mechanics_save_20261031_lane_stat_scaling.py',False),
 ('ov006-20261031-transition130','reproduce_ov006_transition130_20261031.py',True),
 ('ov006-20261031-predicate130','reproduce_ov006_transition130_20261031.py',True),
]
REGISTRY_TARGET=ROOT/'work/integration/cohort76-recovery-transaction.json'
BASE=ROOT/'evidence/verification/cohort76-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-75.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8865
    fields=['module','mode','address','size','source','sourceSha256','object','objectSha256','targetSha256','report']
    write_json(BASE,{'sourceRegistrySha256':sha256(REGISTRY_TARGET),'preferencesSha256':sha256(ROOT/'source-preferences.json'),'selected':[{'key':list(key),**{f:r[f] for f in fields if f in r}} for key,r in before.items()]})
    reports=[]
    for name,producer,raw in PACKETS:
        path=f'evidence/matches/{name}.json'
        if raw:register(path,[producer])
        else:
            seal_sources(path,[producer]);register(path,['seal_recovery_sources_20261031.py',path,producer])
        reports.append(path)
    registry=read_json(REGISTRY_TARGET);oracles={r['report']:r for r in registry['oracles']}
    for label,producer in [('arm7-lane-thread-scheduling344','validate_arm7_lane_thread_scheduling_20261031.py'),('arm7-lane-messages412','validate_arm7_lane_messages_20261031.py'),('arm7-lane-mutex-release152','validate_arm7_lane_mutex_release_20261031.py'),('arm7-lane-child-typed180','validate_arm7_lane_child_typed_20261031.py'),('arm7-lane-thread-create264','validate_arm7_lane_thread_create_20261031.py')]:
        path=f'evidence/verification/{label}-controls-20261031.json';oracles[path]={'report':path,'reproduce':[producer]}
    for path,producer in [('evidence/arm7/sdk-signed-division-scope-20261031.json','arm7_lane_sdk_signed_division_scope_20261031.py'),('evidence/verification/arm7-signed-division-inventory-amendment-20261031.json','amend_arm7_signed_division_inventory_20261031.py')]:
        oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(REGISTRY_TARGET,registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==23 and new_bytes==2684
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=23,newOrdinaryCBytes=2684,newSourceBytes=2684,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8888,expectedSourceLinkedBytes=659961,preferredSourceInputsRequired=27,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=75,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-76.json',plan);print({'newFunctions':23,'newOrdinaryCBytes':2684,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


if __name__=='__main__':
    import recovery_registry
    from project import write_text
    current=ROOT/'recovery.json';before=current.read_bytes();before_sha=sha256(current)
    REGISTRY_TARGET.parent.mkdir(parents=True,exist_ok=True);REGISTRY_TARGET.write_bytes(before)
    recovery_registry.REGISTRY=REGISTRY_TARGET
    main()
    assert sha256(current)==before_sha,'Concurrent registry changes prevent publication'
    write_text(current,REGISTRY_TARGET.read_text(encoding='utf-8-sig'))
    assert sha256(current)==sha256(REGISTRY_TARGET)
    print({'registryPublishedAtomically':True})
