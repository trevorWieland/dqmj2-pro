from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('sdk-atan2-20261031','match_sdk_atan2_20261031.py',False),
 ('main-mmio-view-20261031','match_main_mmio_view_20261031.py',False),
 ('arm7-lane-word-dispatch92-20261031','match_arm7_lane_word_dispatch_20261031.py',True),
 ('arm7-lane-channel-five-20261031','match_arm7_lane_channel_five_20261031.py',True),
 ('ov001-20261031-state46','match_ov001_state46_20261031.py',False),
 ('ov005-20261031-initializer47','match_ov005_initializer47_20261031.py',False),
 ('ov006-20261031-dispatch51','match_ov006_dispatch51_20261031.py',False),
 ('ov000-20261031-criteria52','match_ov000_criteria52_20261031.py',False),
 ('ov001-20261031-state58','match_ov001_state58_20261031.py',False),
 ('ov001-20261031-reroll59','match_ov001_reroll59_20261031.py',False),
 ('ov005-20261031-menu60','match_ov005_menu60_20261031.py',False),
 ('mechanics-save-20261031-lane-save-controller-v2','match_mechanics_save_20261031_lane_save_controller_v2.py',False),
]
MIGRATIONS={0x0200235C,0x02041930,0x02041944}
BASE=ROOT/'evidence/verification/cohort71-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-70.json');verify_sources();assert old['linksPending'] is False
    if not BASE.exists():
        assert sha256(ROOT/'recovery.json')==old['sourceRegistrySha256']
        selected,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(selected)==8790
        fields=['module','mode','address','size','source','sourceSha256','object','objectSha256','targetSha256','report']
        write_json(BASE,{'sourceRegistrySha256':sha256(ROOT/'recovery.json'),'preferences':read_json(ROOT/'source-preferences.json'),'selected':[{'key':list(key),**{f:row[f] for f in fields if f in row}} for key,row in selected.items()]})
    baseline=read_json(BASE);before={tuple(r['key']):r for r in baseline['selected']};policies=baseline['preferences'];reports=[];changed=set()
    for name,producer,raw in PACKETS:
        relative=f'evidence/matches/{name}.json'
        if raw:register(relative,[producer])
        else:
            seal_sources(relative,[producer]);register(relative,['seal_recovery_sources_20261031.py',relative,producer])
        reports.append(relative)
        for row in read_json(ROOT/relative)['matches']:
            address=int(row['address'],0)
            if address not in MIGRATIONS or row['module']!='main':continue
            key=('main',row['mode'],address);prior=before[key];assert row['bytes']==prior['size'] and row['targetSha256']==prior['targetSha256']
            assert sha256(ROOT/prior['source'])==prior['sourceSha256'];changed.add(key)
            identity={'processor':'arm9','module':'main','mode':row['mode'],'address':f'0x{address:08x}','bytes':row['bytes'],'targetSha256':row['targetSha256']}
            preferred={'source':row['source'],'sourceSha256':row['sourceSha256'],'report':relative};previous={f:prior[f] for f in ['source','sourceSha256','report']}
            audit=f'evidence/abi/main-{address:08x}-defined-forwarding-primary-migration-20261031.json'
            write_json(ROOT/audit,{'romSha256':configuration()['romSha256'],'identity':identity,'previous':previous,'preferred':preferred,'originalSourceUnchanged':True,'nativeBytesUnchanged':True,'newFunctionCredit':0,'newByteCredit':0,'behavioralProof':{'report':relative,'limitations':read_json(ROOT/relative)['limitations']}})
            policies['preferences'].append({**identity,**preferred,'evidence':audit,'evidenceSha256':sha256(ROOT/audit)})
    assert len(changed)==3 and len(policies['preferences'])==27;write_json(ROOT/'source-preferences.json',policies)
    registry=read_json(ROOT/'recovery.json');oracles={r['report']:r for r in registry['oracles']}
    for label,producer in [('arm7-lane-word-dispatch92','validate_arm7_lane_word_dispatch_20261031.py'),('arm7-lane-channel-five','validate_arm7_lane_channel_five_20261031.py')]:
        path=f'evidence/verification/{label}-controls-20261031.json';oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(ROOT/'recovery.json',registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():
        if key not in changed:assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==19 and new_bytes==5296
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=len(added),newOrdinaryCBytes=new_bytes,newSourceBytes=new_bytes,newMathematicalDataBytes=0,duplicateMigrationFunctions=3,duplicateMigrationBytes=56,expectedSourceMatchedFunctions=8809,expectedSourceLinkedBytes=649021,preferredSourceInputsRequired=27,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=70,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-71.json',plan);print({'newFunctions':len(added),'newOrdinaryCBytes':new_bytes,'migrationBytes':56,'linksPending':True})


if __name__=='__main__':
    main()
