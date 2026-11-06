from project import ROOT,read_json,write_json,write_text,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('ov000-20261031-buffer178','match_ov000_buffer178_20261031.py',False),
 ('arm7-lane-sound-init108-20261031','match_arm7_lane_sound_init_20261031.py',True),
 ('arm7-lane-thread-exit160-20261031','match_arm7_lane_thread_exit_20261031.py',True),
 ('arm7-lane-channel-locks456-20261031','match_arm7_lane_channel_locks_20261031.py',True),
 ('ov001-20261031-gate160','match_ov001_gate160_20261031.py',False),
 ('ov000-20261031-parser169','match_ov000_parser169_20261031.py',False),
 ('mechanics-save-20261031-lane-status-return','match_mechanics_save_20261031_lane_status_return.py',False),
]
REGISTRY_TARGET=ROOT/'work/integration/cohort79-recovery-transaction.json'
BASE=ROOT/'evidence/verification/cohort79-before-adoption-20261031.json'
PREFERENCE_TARGET=ROOT/'work/integration/cohort79-preference-transaction.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-78.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8902
    fields=['module','mode','address','size','source','sourceSha256','object','objectSha256','targetSha256','report']
    policies=read_json(ROOT/'source-preferences.json');assert len(policies['preferences'])==27
    write_json(BASE,dict(sourceRegistrySha256=sha256(REGISTRY_TARGET),preferencesSha256=sha256(ROOT/'source-preferences.json'),preferences=policies,selected=[dict(key=list(key),**{field:row[field] for field in fields if field in row}) for key,row in before.items()]))
    reports=[];migrated=set()
    for name,producer,raw in PACKETS:
        path=f'evidence/matches/{name}.json'
        if raw:register(path,[producer])
        else:
            seal_sources(path,[producer]);register(path,['seal_recovery_sources_20261031.py',path,producer])
        reports.append(path)
        for row in read_json(ROOT/path)['matches']:
            if row['module']!='main' or int(row['address'],0)!=0x02041814:continue
            key=('main','arm',0x02041814);prior=before[key]
            assert row['bytes']==prior['size']==20 and row['targetSha256']==prior['targetSha256']
            assert sha256(ROOT/prior['source'])==prior['sourceSha256']
            identity=dict(processor='arm9',module='main',mode='arm',address='0x02041814',bytes=20,targetSha256=row['targetSha256'])
            preferred=dict(source=row['source'],sourceSha256=row['sourceSha256'],report=path)
            audit='evidence/abi/main-02041814-raw-byte-return-primary-migration-20261031.json'
            write_json(ROOT/audit,dict(romSha256=configuration()['romSha256'],identity=identity,previous={field:prior[field] for field in ['source','sourceSha256','report']},preferred=preferred,originalSourceUnchanged=True,nativeBytesUnchanged=True,newFunctionCredit=0,newByteCredit=0,sourceApiChange='Expose actual zero-extended byte return rather than void; preserve raw0..255 and actual caller compare-with1',behavioralProof=dict(report=path,limitations=read_json(ROOT/path)['limitations']),historicalObjectHashes=dict(previous=prior['objectSha256'],preferred=row['objectSha256'])))
            policies['preferences'].append(dict(**identity,**preferred,evidence=audit,evidenceSha256=sha256(ROOT/audit)));migrated.add(key)
    assert len(migrated)==1 and len(policies['preferences'])==28
    write_json(PREFERENCE_TARGET,policies)
    registry=read_json(REGISTRY_TARGET);oracles={row['report']:row for row in registry['oracles']}
    for label,producer in [('arm7-lane-thread-exit160','validate_arm7_lane_thread_exit_20261031.py'),('arm7-lane-channel-locks456','validate_arm7_lane_channel_locks_20261031.py'),('arm7-lane-sound-init108','validate_arm7_lane_sound_init_20261031.py')]:
        path=f'evidence/verification/{label}-controls-20261031.json';oracles[path]=dict(report=path,reproduce=[producer])
    registry['oracles']=list(oracles.values());write_json(REGISTRY_TARGET,registry);verify_sources()
    import source_selection
    from unittest.mock import patch
    original_preferences=source_selection.preferences
    with patch.object(source_selection,'preferences',lambda namespace:original_preferences(namespace,path=PREFERENCE_TARGET)):
        after,rejected=collect_matches(configuration()['romSha256'])
    assert not rejected
    for key,row in before.items():
        if key not in migrated:assert all(after[key][field]==row[field] for field in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[key]['size'] for key in added);assert len(added)==9 and new_bytes==1488
    plan={key:value for key,value in old.items() if key.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),sourcePreferenceSha256=sha256(PREFERENCE_TARGET),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=9,newOrdinaryCBytes=1488,newSourceBytes=1488,newMathematicalDataBytes=0,duplicateMigrationFunctions=1,duplicateMigrationBytes=20,expectedSourceMatchedFunctions=8911,expectedSourceLinkedBytes=663965,preferredSourceInputsRequired=28,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=78,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False,nonreturningExitEvidence=dict(actualOwnedNormalReturns=0,verifiedNonreturningExitTransition=True,continuationsExcludedFromExecution=5))
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-79.json',plan)
    print(dict(newFunctions=len(added),newOrdinaryCBytes=new_bytes,zeroCoverageMigrationBytes=20,preferredSources=28,linksPending=True))


if __name__=='__main__':
    import recovery_registry
    current=ROOT/'recovery.json';preferences=ROOT/'source-preferences.json';before=current.read_bytes();before_sha=sha256(current);before_preferences=preferences.read_bytes();before_preference_sha=sha256(preferences)
    REGISTRY_TARGET.parent.mkdir(parents=True,exist_ok=True);REGISTRY_TARGET.write_bytes(before);PREFERENCE_TARGET.write_bytes(before_preferences);recovery_registry.REGISTRY=REGISTRY_TARGET
    registry_published=False;preference_published=False
    try:
        main()
        assert sha256(current)==before_sha and sha256(preferences)==before_preference_sha,'Concurrent policy changes prevent publication'
        write_text(preferences,PREFERENCE_TARGET.read_text(encoding='utf-8-sig'));preference_published=True
        write_text(current,REGISTRY_TARGET.read_text(encoding='utf-8-sig'));registry_published=True
        assert sha256(current)==sha256(REGISTRY_TARGET) and sha256(preferences)==sha256(PREFERENCE_TARGET)
    finally:
        if preference_published and not registry_published:
            assert sha256(preferences)==sha256(PREFERENCE_TARGET),'Concurrent preference changes prevent rollback'
            preferences.write_bytes(before_preferences)
