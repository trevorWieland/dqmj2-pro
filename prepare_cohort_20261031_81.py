from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('arm7-lane-pxi-recv224-20261031','match_arm7_lane_pxi_recv_20261031.py',True),
 ('arm7-lane-alarm-registration156-20261031','match_arm7_lane_alarm_registration_20261031.py',True),
 ('mechanics-save-20261031-lane-secondary-roster','match_mechanics_save_20261031_lane_secondary_roster.py',False),
 ('mechanics-save-20261031-lane-text-span','match_mechanics_save_20261031_lane_text_span.py',False),
 ('main-roster-refresh-20261031','match_main_roster_refresh_20261031.py',False),
 ('ov006-20261031-snapshot211-linked','reproduce_ov006_pair211212_linked_20261031.py',True),
 ('ov006-20261031-loop212-linked','reproduce_ov006_pair211212_linked_20261031.py',True),
]
REGISTRY_TARGET=ROOT/'work/integration/cohort81-recovery-transaction.json'
BASE=ROOT/'evidence/verification/cohort81-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-80.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8918
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
    for path,producer in [('evidence/verification/arm7-lane-alarm-registration156-controls-20261031.json','validate_arm7_lane_alarm_registration_20261031.py'),('evidence/verification/arm7-lane-pxi-recv224-controls-20261031.json','validate_arm7_lane_pxi_recv_20261031.py')]:
        oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(REGISTRY_TARGET,registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==9 and new_bytes==1624
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=9,newOrdinaryCBytes=1624,newSourceBytes=1624,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8927,expectedSourceLinkedBytes=666653,preferredSourceInputsRequired=28,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=80,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-81.json',plan);print({'newFunctions':len(added),'newOrdinaryCBytes':new_bytes,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


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
