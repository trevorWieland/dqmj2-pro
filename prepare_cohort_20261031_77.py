from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-archive-tables-20261031','match_main_archive_tables_20261031.py',False),
 ('mechanics-save-20261031-lane-record-sorter','match_mechanics_save_20261031_lane_record_sorter.py',False),
 ('arm7-lane-thread-init240-20261031','match_arm7_lane_thread_init_20261031.py',True),
 ('ov000-20261031-windows134','match_ov000_windows134_20261031.py',False),
 ('ov001-20261031-phase136','match_ov001_phase136_20261031.py',False),
 ('ov000-20261031-remove137','match_ov000_remove137_20261031.py',False),
 ('mechanics-save-20261031-lane-level-cache','match_mechanics_save_20261031_lane_level_cache.py',False),
 ('mechanics-save-20261031-lane-level-lookup','match_mechanics_save_20261031_lane_level_lookup.py',False),
]
REGISTRY_TARGET=ROOT/'work/integration/cohort77-recovery-transaction.json'
BASE=ROOT/'evidence/verification/cohort77-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-76.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8888
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
    for path,producer in [('evidence/verification/arm7-lane-thread-init240-controls-20261031.json','validate_arm7_lane_thread_init_20261031.py'),('evidence/arm7/sdk-stack-linker-constants-20261031.json','arm7_lane_sdk_stack_constants_20261031.py')]:
        oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(REGISTRY_TARGET,registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==10 and new_bytes==1920
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=10,newOrdinaryCBytes=1920,newSourceBytes=1920,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8898,expectedSourceLinkedBytes=661881,preferredSourceInputsRequired=27,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=76,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-77.json',plan);print({'newFunctions':10,'newOrdinaryCBytes':1920,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


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
