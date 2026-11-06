from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources,batches
from ledger_state import collect_matches
from seal_recovery_evidence_20261031 import seal

CODE=[
 ('mechanics-save-20261031-lane-uid-comparator','match_mechanics_save_20261031_lane_uid_comparator.py'),
 ('ov001-20261031-ability28','replay_overlay_packet28_integrator_20261031.py'),
 ('ov006-20261031-summary28','replay_overlay_packet28_integrator_20261031.py'),
 ('arm7-lane-setting-20261031','match_arm7_lane_setting_20261031.py'),
 ('mechanics-save-20261031-lane-view-parts','match_mechanics_save_20261031_lane_view_parts.py'),
 ('arm7-lane-alarm-selector-20261031','match_arm7_lane_alarm_selector_20261031.py'),
 ('ov006-20261031-menu33','match_ov006_menu33_20261031.py'),
 ('ov006-20261031-setup38','match_ov006_setup38_20261031.py'),
 ('sdk-trig-wrappers-20261031','match_sdk_trig_wrappers_20261031.py'),
]
MIGRATIONS=[
 ('mechanics-save-20261031-lane-row-forward-abi','match_mechanics_save_20261031_lane_row_forward_abi.py'),
 ('mechanics-save-20261031-lane-comparator-abi','match_mechanics_save_20261031_lane_comparator_abi.py'),
]
BASE=ROOT/'evidence/verification/cohort69-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-68.json')
    namespace=configuration()['romSha256']
    verify_sources()
    if not BASE.exists():
        before,rejected=collect_matches(namespace)
        assert not rejected and len(before)==old['sourceMatchedFunctions']
        assert sha256(ROOT/'recovery.json')==old['sourceRegistrySha256']
        write_json(BASE,{'sourceRegistrySha256':sha256(ROOT/'recovery.json'),'sourcePreferences':read_json(ROOT/'source-preferences.json'),'selected':list(before.values())})
    baseline=read_json(BASE)
    before={(x['module'],x['mode'],x['address']):x for x in baseline['selected']}
    from replay_overlay_packet28_integrator_20261031 import main as replay_pair
    replay_pair()
    reports=[]
    for name,producer in CODE+MIGRATIONS:
        relative=f'evidence/matches/{name}.json'
        if producer=='replay_overlay_packet28_integrator_20261031.py':
            register(relative,[producer])
        elif name=='sdk-trig-wrappers-20261031':
            register(relative,[producer])
        else:
            seal(relative,[producer])
            register(relative,['seal_recovery_evidence_20261031.py',relative,producer])
        reports.append(relative)
    data='evidence/data/sdk-trig-table-20261031.json'
    register(data,['match_sdk_trig_data_20261031.py']);reports.append(data)
    policies=baseline['sourcePreferences']
    migration_keys=set()
    for name,producer in MIGRATIONS:
        relative=f'evidence/matches/{name}.json';document=read_json(ROOT/relative)
        for row in document['matches']:
            key=row['module'],row['mode'],int(row['address'],0)
            previous=before[key];migration_keys.add(key)
            assert row['bytes']==previous['size'] and row['targetSha256']==previous['targetSha256']
            assert sha256(ROOT/previous['source'])==previous['sourceSha256']
            identity={'processor':row['processor'],'module':row['module'],'mode':row['mode'],'address':f'0x{key[2]:08x}','bytes':row['bytes'],'targetSha256':row['targetSha256']}
            preferred={'source':row['source'],'sourceSha256':row['sourceSha256'],'report':relative}
            prior={k:previous[k] for k in ['source','sourceSha256','report']}
            evidence=f'evidence/abi/main-{key[2]:08x}-defined-c-primary-migration-20261031.json'
            audit={'romSha256':namespace,'identity':identity,'previous':prior,'preferred':preferred,'originalSourceUnchanged':True,'nativeBytesUnchanged':True,'newFunctionCredit':0,'newByteCredit':0,'behavioralProof':{'report':relative,'oracle':document['oracle'],'limitations':document['limitations']}}
            write_json(ROOT/evidence,audit)
            policies['preferences'].append({**identity,**preferred,'evidence':evidence,'evidenceSha256':sha256(ROOT/evidence)})
    assert len(migration_keys)==4 and len(policies['preferences'])==24
    write_json(ROOT/'source-preferences.json',policies)
    registry=read_json(ROOT/'recovery.json')
    more=read_json(ROOT/'provenance/next-cohort-control-replay-20261031.json')['oracles']
    more += [{'report':f'evidence/verification/arm7-lane-{name}-controls-20261031.json','reproduce':[f'validate_arm7_lane_{name.replace("-","_")}_20261031.py']} for name in ['setting','alarm-selector','child-counter']]
    more += [{'report':'evidence/functional/ov001-ability-native30-20261031.json','reproduce':['prove_ov001_ability_native30_20261031.py']}]
    existing={x['report']:x for x in registry.get('oracles',[])}
    existing.update({x['report']:x for x in more});registry['oracles']=list(existing.values());write_json(ROOT/'recovery.json',registry)
    verify_sources()
    after,rejected=collect_matches(namespace);assert not rejected
    for key,row in before.items():
        if key not in migration_keys:assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_code=sum(after[key]['size'] for key in added)
    data_bytes=sum(x['bytes'] for x in read_json(ROOT/data)['dataMatches'])
    assert len(added)==11 and new_code==5260 and data_bytes==16384
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,newSourceFunctions=len(added),newSourceBytes=new_code+data_bytes,newOrdinaryCBytes=new_code,newMathematicalDataBytes=data_bytes,freshStandaloneFunctions=15,freshStandaloneBytes=5764,duplicateMigrationFunctions=4,duplicateMigrationBytes=504,duplicateRetainedProofFunctions=1,duplicateRetainedProofBytes=76,expectedSourceMatchedFunctions=len(after),expectedSourceLinkedBytes=old['sourceLinkedBytes']+new_code+data_bytes,interpretedInventoryRequired=True,preferredSourceInputsRequired=24,oldSourceVariantsRetained=True,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=68,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-69.json',plan)
    print({'newFunctions':len(added),'newCodeBytes':new_code,'newDataBytes':data_bytes,'sourceFunctionsTarget':len(after),'sourceInitializedBytesTarget':plan['expectedSourceLinkedBytes'],'linksPending':True,'preferredImplementations':24})


if __name__=='__main__':
    main()
