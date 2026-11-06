from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_sources_20261031 import seal_sources

PACKETS=[
 ('arm7-lane-halfword-control80-20261031',['match_arm7_lane_halfword_control_20261031.py'],True),
 ('mechanics-save-20261031-lane-state-loop',['match_mechanics_save_20261031_lane_state_loop.py'],False),
 ('mechanics-save-20261031-lane-width-leaves',['match_mechanics_save_20261031_lane_width_leaves.py'],False),
 ('mechanics-save-20261031-lane-packed-sweep',['match_mechanics_save_20261031_lane_packed_sweep.py'],False),
 ('ov005-20261031-controller295',['match_ov005_controller295_20261031.py'],False),
 ('main-word-pattern-20261031',['match_main_word_pattern_20261031.py'],False),
 ('main-header-append-20261031',['match_main_header_append_20261031.py'],False),
 ('ov005-20261031-callbacks296-source-data',['adapt_ov005_callbacks296_data_20261031.py'],False),
]
REGISTRY_TARGET=ROOT/'work/integration/cohort87-recovery-transaction.json'
BASE=ROOT/'evidence/verification/cohort87-before-adoption-20261031.json'


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-86.json');verify_sources();assert not old['linksPending']
    assert sha256(REGISTRY_TARGET)==old['sourceRegistrySha256']
    assert sha256(ROOT/'source-preferences.json')==old['sourcePreferenceSha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8975
    fields=['module','mode','address','size','source','sourceSha256','object','objectSha256','targetSha256','report']
    write_json(BASE,{'sourceRegistrySha256':sha256(REGISTRY_TARGET),'preferencesSha256':sha256(ROOT/'source-preferences.json'),'selected':[{'key':list(key),**{f:r[f] for f in fields if f in r}} for key,r in before.items()]})
    reports=[]
    for name,command,raw in PACKETS:
        path=f'evidence/matches/{name}.json'
        if raw:register(path,command)
        else:
            seal_sources(path,command);register(path,['seal_recovery_sources_20261031.py',path,*command])
        reports.append(path)
    registry=read_json(REGISTRY_TARGET);oracles={r['report']:r for r in registry['oracles']}
    for path,producer in [('evidence/verification/arm7-lane-halfword-control80-controls-20261031.json','validate_arm7_lane_halfword_control_20261031.py'),('evidence/portability/main-word-pattern-windows32-20261031.json','check_main_word_pattern_windows32_20261031.py')]:
        oracles[path]={'report':path,'reproduce':[producer]}
    registry['oracles']=list(oracles.values());write_json(REGISTRY_TARGET,registry);verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():assert all(after[key][f]==row[f] for f in ['source','sourceSha256','object','objectSha256','report'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added);assert len(added)==9 and new_bytes==1102
    data=read_json(ROOT/'evidence/matches/ov005-20261031-callbacks296-source-data.json')
    assert len(data['dataMatches'])==1 and data['dataMatches'][0]['bytes']==24 and data['authoredExecutableCodeBytes']==0 and not data['matches']
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(REGISTRY_TARGET),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=9,newOrdinaryCBytes=1102,newSourceBytes=1126,newSymbolicInitializedDataBytes=24,newMathematicalDataBytes=0,duplicateMigrationFunctions=0,duplicateMigrationBytes=0,expectedSourceMatchedFunctions=8984,expectedSourceLinkedBytes=676023,preferredSourceInputsRequired=61,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=86,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-87.json',plan);print({'newFunctions':len(added),'newOrdinaryCBytes':new_bytes,'allPriorSourcesAndObjectsPreserved':True,'linksPending':True})


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
