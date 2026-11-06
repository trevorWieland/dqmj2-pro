from unittest.mock import patch
from project import ROOT,read_json,write_json,sha256,configuration,now
from recovery_registry import register,verify_sources,batches
from ledger_state import collect_matches
from seal_recovery_evidence_20261031 import seal

PACKETS = [
 ('arm7-channel-parameters-20261030-67','match_arm7_channel_parameters_20261030_67.py'),
 ('ov006-20261030-display17','match_ov006_display17_20261030.py'),
 ('mechanics-save-20261030-lane-menu-refresh','match_mechanics_save_20261030_lane_menu_refresh.py'),
 ('ov005-20261030-slider20','match_ov005_slider20_20261030.py'),
 ('mechanics-save-20261030-lane-roster-cache','match_mechanics_save_20261030_lane_roster_cache.py'),
 ('arm7-lane-driver-leaves-20261030','match_arm7_lane_driver_leaves_20261030.py'),
 ('mechanics-save-20261030-lane-word-arrays','match_mechanics_save_20261030_lane_word_arrays.py'),
 ('arm7-lane-timing-20261031','match_arm7_lane_timing_20261031.py'),
 ('arm7-lane-initializer-20261031','match_arm7_lane_initializer_20261031.py'),
]


def main():
    old=read_json(ROOT/'evidence/verification/cohort-2026-10-29-67.json')
    verify_sources()
    packet_paths={f'evidence/matches/{name}.json' for name,_ in PACKETS}
    baseline_batches=[row for row in batches() if row['report'] not in packet_paths]
    with patch('recovery_registry.batches',return_value=baseline_batches):
        before,rejected=collect_matches(configuration()['romSha256'])
    assert not rejected and len(before)==old['sourceMatchedFunctions']
    reports=[]
    for name,producer in PACKETS:
        report=f'evidence/matches/{name}.json'
        seal(report,[producer])
        register(report,['seal_recovery_evidence_20261031.py',report,producer])
        reports.append(report)
    after,rejected=collect_matches(configuration()['romSha256'])
    assert not rejected
    assert all(after[key]['sourceSha256']==row['sourceSha256'] and after[key]['objectSha256']==row['objectSha256'] for key,row in before.items())
    added=set(after)-set(before)
    new_bytes=sum(after[key]['size'] for key in added)
    plan={key:value for key,value in old.items() if key.startswith('expectedInterpreted') or key.startswith('expectedEmpty') or key.startswith('expectedNonempty') or key.startswith('expectedCopy')}
    plan.update(schemaVersion=1,createdUtc=now(),reports=reports,interpretedReports=[],
        sourceRegistrySha256=sha256(ROOT/'recovery.json'),sourcePreferenceSha256=sha256(ROOT/'source-preferences.json'),
        interpretedRegistrySha256=sha256(ROOT/'interpreted-recovery.json'),linksPending=True,
        sourceReconstructionComplete=False,wholeRomMatchedFromSource=False,
        newSourceFunctions=len(added),newSourceBytes=new_bytes,freshStandaloneFunctions=len(added),freshStandaloneBytes=new_bytes,
        duplicateMigrationFunctions=0,duplicateMigrationBytes=0,
        expectedSourceMatchedFunctions=len(after),expectedSourceLinkedBytes=old['sourceLinkedBytes']+new_bytes,
        interpretedInventoryRequired=True,preferredSourceInputsRequired=old['preferredSourceInputsRequired'],oldSourceVariantsRetained=True,
        sourceOnlyRomProven=False,fullWindowsGameFromSourceProven=False,androidDeviceExecutionCount=0,
        previousAcceptedCohort=67,previousAcceptedFunctions=len(before),previousAcceptedBytes=old['sourceLinkedBytes'],
        priorSelectedSourcesAndObjectsPreserved=True,replayCodeSealed=True)
    assert len(added)==14 and new_bytes==2920
    assert sum(row['size'] for row in after.values())-sum(row['size'] for row in before.values())==new_bytes
    write_json(ROOT/'evidence/verification/cohort-2026-10-29-68.json',plan)
    print({'candidateFunctions':len(after),'candidateBytes':plan['expectedSourceLinkedBytes'],'newFunctions':len(added),'newBytes':new_bytes,'linksPending':True})


if __name__=='__main__':
    main()
