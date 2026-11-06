from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources
from ledger_state import collect_matches
from seal_recovery_evidence_20261031 import seal

PACKETS=[('main-wide-format-parser-20261031','match_main_wide_format_parser_20261031.py'),('mechanics-save-20261031-lane-save-header','match_mechanics_save_20261031_lane_save_header.py')]


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-69.json')
    assert old['linksPending'] is False
    verify_sources()
    assert sha256(ROOT/'recovery.json')==old['sourceRegistrySha256']
    before,rejected=collect_matches(configuration()['romSha256']);assert not rejected and len(before)==8788
    keys=['processor','program','module','mode','address','size','targetSha256','source','sourceSha256','object','objectSha256','report']
    write_json(ROOT/'evidence/verification/cohort70-before-adoption-20261031.json',{'sourceRegistrySha256':sha256(ROOT/'recovery.json'),'sourcePreferencesSha256':sha256(ROOT/'source-preferences.json'),'selected':[{k:row[k] for k in keys if k in row} for row in before.values()]})
    reports=[]
    for name,producer in PACKETS:
        report=f'evidence/matches/{name}.json';seal(report,[producer]);register(report,['seal_recovery_evidence_20261031.py',report,producer]);reports.append(report)
    verify_sources()
    after,rejected=collect_matches(configuration()['romSha256']);assert not rejected
    for key,row in before.items():
        assert all(after[key][field]==row[field] for field in ['source','sourceSha256','object','objectSha256'])
    added=set(after)-set(before);new_bytes=sum(after[k]['size'] for k in added)
    assert len(added)==2 and new_bytes==1500
    plan={k:v for k,v in old.items() if k.startswith(('expectedInterpreted','expectedEmpty','expectedNonempty','expectedCopy'))}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,newSourceFunctions=2,newOrdinaryCBytes=1500,newSourceBytes=1500,newMathematicalDataBytes=0,expectedSourceMatchedFunctions=8790,expectedSourceLinkedBytes=643725,interpretedInventoryRequired=True,preferredSourceInputsRequired=24,sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,previousAcceptedCohort=69,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],allUnmigratedSourcesAndObjectsPreserved=True,fullCleanReplayOfThisCohortProven=False)
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-70.json',plan)
    print({'newFunctions':len(added),'newOrdinaryCBytes':new_bytes,'linksPending':True,'allPriorSourcesAndObjectsPreserved':True})


if __name__=='__main__':
    main()
