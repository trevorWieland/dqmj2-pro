from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('main-digit-rounding-20261031','match_main_digit_rounding_20261031.py',False),
 ('arm7-lane-channel-factor96-20261031','match_arm7_lane_channel_factor_20261031.py',True),
 ('arm7-lane-mmio-pair136-20261031','match_arm7_lane_mmio_pair_20261031.py',True),
 ('ov003-20261031-descriptor61','match_ov003_descriptor61_20261031.py',False),
 ('ov005-20261031-bucket64','match_ov005_bucket64_20261031.py',False),
 ('ov005-20261031-refresh65','match_ov005_refresh65_20261031.py',False),
 ('ov005-20261031-stop69','match_ov005_stop69_20261031.py',False),
 ('mechanics-save-20261031-lane-resource-release','match_mechanics_save_20261031_lane_resource_release.py',False),
]
BASE=ROOT/'evidence/verification/cohort72-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-71.json');verify_sources();assert not old['linksPending']
    assert sha256(ROOT/'recovery.json')==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8809
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
    for label,producer in [('arm7-lane-channel-factor96','validate_arm7_lane_channel_factor_20261031.py'),('arm7-lane-mmio-pair136','validate_arm7_lane_mmio_pair_20261031.py')]:
        path=f'evidence/verification/{label}-controls-20261031.json';oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(ROOT/'recovery.json',registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==11 and new_bytes==1152
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=11,newOrdinaryCBytes=1152,newSourceBytes=1152,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8820,expectedSourceLinkedBytes=650173,preferredSourceInputsRequired=27,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=71,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-72.json',plan);print({'newFunctions':11,'newOrdinaryCBytes':1152,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


if __name__=='__main__':
    main()
