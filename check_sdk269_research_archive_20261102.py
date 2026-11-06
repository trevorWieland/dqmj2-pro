from pathlib import Path
from project import ROOT,read_json,write_json,sha256
import validate_arm7_sdk264_wireless_large_queue_20261101 as validator

REPORT=ROOT/'evidence/verification/sdk269-research-archive-controls-20261102.json'


def main():
    validator.main();controls=read_json(validator.REPORT)
    assert controls['controlCount']==9 and all(row['rejected']for row in controls['controls'])
    source=read_json(validator.queue.REPORT)
    assert source['sourceCredit']==0 and source['compileReadyTargetRanges']==39
    assert source['relocationMaskedEqualTargets']==30 and source['allResultsUnacceptedHypotheses']
    write_json(REPORT,dict(passed=True,sourceCredit=0,generator=Path(__file__).name,generatorSha256=sha256(__file__),
     replayReportSha256=sha256(validator.queue.REPORT),controlReportSha256=sha256(validator.REPORT),
     actualRejectionControls=9,unacceptedTargetRanges=39,relocationMaskDiagnostics=30,
     originalScriptBytesPreserved=True,ordinarySourceAcceptance=False,
     reproductionCommand='python check_sdk269_research_archive_20261102.py'))
    print('SDK269 zero-credit research replay and nine rejection controls pass')


if __name__=='__main__':
    main()
