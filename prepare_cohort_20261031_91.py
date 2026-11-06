from project import ROOT,read_json,write_json,write_text,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-reservation-pointer-20261031','match_main_reservation_pointer_20261031.py',False),
 ('main-field-widths-20261031','match_main_field_widths_20261031.py',False),
 ('mechanics-save-20261031-lane-packed-classify-host-bindings','adapt_packed_pointer_host_bindings_20261031.py',False),
 ('mechanics-save-20261031-lane-compare-mutex','match_mechanics_save_20261031_lane_compare_mutex.py',False),
 ('arm7-lane-mmio-poll44-20261031','match_arm7_lane_mmio_poll44_20261031.py',True),
 ('mechanics-save-20261031-lane-packed-pointer-abi-host-bindings','adapt_packed_pointer_host_bindings_20261031.py',False),
]
MIGRATIONS={address:('packed-pointer','Expose and forward the measured word-pointer input; retain prior bytes and source')
 for address in [0x02096CF8,0x02096D9C,0x02096D4C,0x02096D6C,0x02096D24,0x02096D04]}
REGISTRY_TARGET=ROOT/'work/integration/cohort91-recovery-transaction.json'
PREFERENCE_TARGET=ROOT/'work/integration/cohort91-preference-transaction.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-90.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==9010
    policies=read_json(ROOT/'source-preferences.json');assert len(policies['preferences'])==61
    fields=['module','mode','address','size','source','sourceSha256','object','objectSha256','targetSha256','report']
    write_json(ROOT/'evidence/verification/cohort91-before-adoption-20261031.json',dict(sourceRegistrySha256=sha256(REGISTRY_TARGET),
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
    registry=read_json(REGISTRY_TARGET)
    oracles={row['report']:row for row in registry['oracles']}
    for report,producer in [
        ('evidence/verification/arm7-lane-mmio-poll44-controls-20261031.json','validate_arm7_lane_mmio_poll44_20261031.py'),
        ('evidence/application/ov000-birth330-functional-20261031.json','prove_ov000_birth330_20261031.py'),
        ('evidence/application/ov000-selection333-native-20261031.json','prove_ov000_selection333_20261031.py'),
        ('evidence/application/ov000-commit336-native-20261031.json','prove_ov000_commit336_20261031.py'),
        ('evidence/arm7/lane-spi-functional1204-20261031.json','prove_arm7_spi_functional1204_20261031.py'),
    ]:
        assert (ROOT/report).is_file(),report
        oracles[report]=dict(report=report,reproduce=[producer])
    registry['oracles']=list(oracles.values())
    write_json(REGISTRY_TARGET,registry)
    assert len(migrated)==6 and len(policies['preferences'])==67
    write_json(PREFERENCE_TARGET,policies);verify_sources()
    import source_selection
    from unittest.mock import patch
    original_preferences=source_selection.preferences
    with patch.object(source_selection,'preferences',lambda namespace:original_preferences(namespace,path=PREFERENCE_TARGET)):
        after,rejected=collect_matches(configuration()['romSha256'])
    assert not rejected
    for key,row in before.items():
        if key not in migrated:assert all(after[key][field]==row[field]for field in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[key]['size']for key in added);assert len(added)==8 and new_bytes==532
    plan={key:value for key,value in old.items()if key.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),
        sourcePreferenceSha256=sha256(PREFERENCE_TARGET),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,
        newSourceFunctions=8,newOrdinaryCBytes=532,newSourceBytes=532,newMathematicalDataBytes=0,duplicateMigrationFunctions=6,duplicateMigrationBytes=140,
        expectedSourceMatchedFunctions=9018,expectedSourceLinkedBytes=679751,preferredSourceInputsRequired=67,sourceReconstructionComplete=False,
        wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,
        previousAcceptedCohort=90,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],
        allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-91.json',plan)
    print(dict(newFunctions=len(added),newOrdinaryCBytes=new_bytes,zeroCoverageMigrationBytes=140,preferredSources=67,linksPending=True))


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
