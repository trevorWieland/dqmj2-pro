from project import ROOT,read_json,write_json,write_text,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-20261031-file-size250','match_main_file_size250_20261031.py',False),
 ('ov000-20261031-cleanup217','match_ov000_cleanup217_20261031.py',False),
 ('ov006-20261031-ordered218-linked','reproduce_ov006_ordered218_linked_20261031.py',True),
 ('ov006-20261031-buffer228','match_ov006_buffer228_20261031.py',False),
 ('ov006-20261031-status235','match_ov006_status235_20261031.py',False),
 ('ov006-20261031-prepare236','match_ov006_prepare236_20261031.py',False),
 ('mechanics-save-20261031-lane-object00-return','match_mechanics_save_20261031_lane_object00_return.py',False),
 ('mechanics-save-20261031-lane-pointer-sequence','match_mechanics_save_20261031_lane_pointer_sequence.py',False),
]
MIGRATIONS={0x02041800:('raw-byte-return','Expose the measured raw unsigned byte and preserve exact compare-with1 semantics'),
    0x0209BC38:('sequenced-output','Initialize the output through the original producer before reading it as the next call argument; preserve stable-global domain')}
REGISTRY_TARGET=ROOT/'work/integration/cohort82-recovery-transaction.json'
PREFERENCE_TARGET=ROOT/'work/integration/cohort82-preference-transaction.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-81.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8927
    policies=read_json(ROOT/'source-preferences.json');assert len(policies['preferences'])==28
    fields=['module','mode','address','size','source','sourceSha256','object','objectSha256','targetSha256','report']
    write_json(ROOT/'evidence/verification/cohort82-before-adoption-20261031.json',dict(sourceRegistrySha256=sha256(REGISTRY_TARGET),
        preferencesSha256=sha256(ROOT/'source-preferences.json'),preferences=policies,
        selected=[dict(key=list(key),**{field:row[field]for field in fields if field in row})for key,row in before.items()]))
    reports=[];migrated=set()
    for name,producer,raw in PACKETS:
        path=f'evidence/matches/{name}.json'
        if raw:register(path,[producer])
        else:seal_sources(path,[producer]);register(path,['seal_recovery_sources_20261031.py',path,producer])
        reports.append(path)
        for row in read_json(ROOT/path)['matches']:
            address=int(row['address'],0)
            if row['module']!='main' or address not in MIGRATIONS:continue
            key=('main',row['mode'],address);prior=before[key]
            assert row['bytes']==prior['size'] and row['targetSha256']==prior['targetSha256'] and sha256(ROOT/prior['source'])==prior['sourceSha256']
            identity=dict(processor='arm9',module='main',mode=row['mode'],address=hex(address),bytes=row['bytes'],targetSha256=row['targetSha256'])
            preferred=dict(source=row['source'],sourceSha256=row['sourceSha256'],report=path)
            label,change=MIGRATIONS[address];audit=f'evidence/abi/main-{address:08x}-{label}-primary-migration-20261031.json'
            write_json(ROOT/audit,dict(romSha256=configuration()['romSha256'],identity=identity,
                previous={field:prior[field]for field in ['source','sourceSha256','report']},preferred=preferred,
                originalSourceUnchanged=True,nativeBytesUnchanged=True,newFunctionCredit=0,newByteCredit=0,sourceApiChange=change,
                behavioralProof=dict(report=path,limitations=read_json(ROOT/path)['limitations']),
                historicalObjectHashes=dict(previous=prior['objectSha256'],preferred=row['objectSha256'])))
            policies['preferences'].append(dict(**identity,**preferred,evidence=audit,evidenceSha256=sha256(ROOT/audit)));migrated.add(key)
    assert len(migrated)==2 and len(policies['preferences'])==30
    write_json(PREFERENCE_TARGET,policies);verify_sources()
    import source_selection
    from unittest.mock import patch
    original_preferences=source_selection.preferences
    with patch.object(source_selection,'preferences',lambda namespace:original_preferences(namespace,path=PREFERENCE_TARGET)):
        after,rejected=collect_matches(configuration()['romSha256'])
    assert not rejected
    for key,row in before.items():
        if key not in migrated:assert all(after[key][field]==row[field]for field in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[key]['size']for key in added);assert len(added)==6 and new_bytes==976
    plan={key:value for key,value in old.items()if key.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),
        sourcePreferenceSha256=sha256(PREFERENCE_TARGET),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,
        newSourceFunctions=6,newOrdinaryCBytes=976,newSourceBytes=976,newMathematicalDataBytes=0,duplicateMigrationFunctions=2,duplicateMigrationBytes=56,
        expectedSourceMatchedFunctions=8933,expectedSourceLinkedBytes=667629,preferredSourceInputsRequired=30,sourceReconstructionComplete=False,
        wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,
        previousAcceptedCohort=81,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],
        allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-82.json',plan)
    print(dict(newFunctions=len(added),newOrdinaryCBytes=new_bytes,zeroCoverageMigrationBytes=56,preferredSources=30,linksPending=True))


if __name__=='__main__':
    import recovery_registry
    current=ROOT/'recovery.json';preferences=ROOT/'source-preferences.json';before=current.read_bytes();before_sha=sha256(current)
    before_preferences=preferences.read_bytes();before_preference_sha=sha256(preferences)
    REGISTRY_TARGET.parent.mkdir(parents=True,exist_ok=True);REGISTRY_TARGET.write_bytes(before);PREFERENCE_TARGET.write_bytes(before_preferences)
    recovery_registry.REGISTRY=REGISTRY_TARGET;registry_published=False;preference_published=False
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
