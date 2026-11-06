from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('arm7-lane-card-control452-20261031','match_arm7_lane_card_control_20261031.py',True),
 ('arm7-lane-card-priority64-20261031','match_arm7_lane_card_priority_20261031.py',True),
 ('ov001-20261031-copy283','match_ov001_copy283_20261031.py',False),
 ('main-word-dispatch-20261031','match_main_word_dispatch_20261031.py',False),
 ('mechanics-save-20261031-lane-group-criterion','match_mechanics_save_20261031_lane_group_criterion.py',False),
 ('mechanics-save-20261031-lane-menu-setup','match_mechanics_save_20261031_lane_menu_setup.py',False),
 ('ov001-20261031-random272','match_ov001_random272_20261031.py',False),
 ('ov001-20261031-mapper280','match_ov001_mapper280_20261031.py',False),
]
REGISTRY_TARGET=ROOT/'work/integration/cohort85-recovery-transaction.json'
BASE=ROOT/'evidence/verification/cohort85-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-84.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    assert sha256(ROOT/'source-preferences.json')==old['sourcePreferenceSha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8956
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
    for path,producer in [('evidence/verification/arm7-lane-card-control452-controls-20261031.json','validate_arm7_lane_card_control_20261031.py'),('evidence/verification/arm7-card-control452-negative-returns-20261031.json','prove_arm7_card_control452_negative_returns_20261031.py'),('evidence/verification/arm7-lane-card-priority64-controls-20261031.json','validate_arm7_lane_card_priority_20261031.py'),('evidence/portability/main-word-dispatch-windows-20261031.json','check_main_word_dispatch_windows_20261031.py')]:
        oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(REGISTRY_TARGET,registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256','report'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==12 and new_bytes==1908
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=12,newOrdinaryCBytes=1908,newSourceBytes=1908,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8968,expectedSourceLinkedBytes=673781,preferredSourceInputsRequired=61,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=84,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-85.json',plan);print({'newFunctions':len(added),'newOrdinaryCBytes':new_bytes,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


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
