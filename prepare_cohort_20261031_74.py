from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-decimal-pad-20261031','match_main_decimal_pad_20261031.py',False),
 ('main-range-keys-20261031','match_main_range_keys_20261031.py',False),
 ('arm7-lane-bank384-20261031','match_arm7_lane_bank_20261031.py',True),
 ('arm7-lane-heap-constructors380-20261031','match_arm7_lane_heap_constructors_20261031.py',True),
 ('arm7-lane-heap-lists548-20261031','match_arm7_lane_heap_lists_20261031.py',True),
 ('arm7-lane-heap-check416-20261031','match_arm7_lane_heap_check_20261031.py',True),
 ('mechanics-save-20261031-lane-byte-exchange','match_mechanics_save_20261031_lane_byte_exchange.py',False),
 ('mechanics-save-20261031-lane-wide-number','match_mechanics_save_20261031_lane_wide_number.py',False),
 ('ov006-20261031-layout91','match_ov006_layout91_20261031.py',False),
 ('ov001-20261031-gate95','reproduce_overlay_packet95_20261031.py',True),
 ('ov006-20261031-dialog95','reproduce_overlay_packet95_20261031.py',True),
]
BASE=ROOT/'evidence/verification/cohort74-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-73.json');verify_sources();assert not old['linksPending']
    assert sha256(ROOT/'recovery.json')==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8832
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
    for label,producer in [('arm7-lane-bank384','validate_arm7_lane_bank_20261031.py'),('arm7-lane-heap-constructors380','validate_arm7_lane_heap_constructors_20261031.py'),('arm7-lane-heap-lists548','validate_arm7_lane_heap_lists_20261031.py'),('arm7-lane-heap-check416','validate_arm7_lane_heap_check_20261031.py')]:
        path=f'evidence/verification/{label}-controls-20261031.json';oracles[path]={'report':path,'reproduce':[producer]}
    path='evidence/functional/save-core-connected-serialization-replay-20261031.json'
    assert (ROOT/path).is_file()
    oracles[path]={'report':path,'reproduce':['prove_save_core_connected_serialization_20261031.py']}
    registry['oracles']=list(oracles.values());write_json(ROOT/'recovery.json',registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==16 and new_bytes==3268
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=16,newOrdinaryCBytes=3268,newSourceBytes=3268,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8848,expectedSourceLinkedBytes=654785,preferredSourceInputsRequired=27,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=73,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-74.json',plan);print({'newFunctions':16,'newOrdinaryCBytes':3268,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


if __name__=='__main__':
    main()
