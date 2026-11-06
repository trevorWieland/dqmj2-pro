import argparse
import sys
from pathlib import Path


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--checkout',required=True);options=parser.parse_args()
    checkout=Path(options.checkout).resolve();sys.path.insert(0,str(checkout))
    from project import ROOT,read_json,write_json,sha256
    from recovery_registry import verify_sources
    assert ROOT.resolve()==checkout
    report=read_json(ROOT/'evidence/verification/clean106-resumed-v4-20261101.json')
    assert report['state']=='failed'and report['failureAtIndex']==1092
    records=report['preservedCommandLogs']+report['steps'];latest={}
    for row in records:
        assert sha256(ROOT/row['log'])==row['logSha256'],row['log']
        latest[row['index']]=row
    assert set(latest)==set(range(report['totalPlannedCommands']))
    assert all(row['exitCode']==0 for index,row in latest.items()if index!=1092)
    assert latest[1092]['exitCode']==1
    assert all(sha256(ROOT/name)==digest for name,digest in report['sourceAndRegistryHashes'].items())
    verify_sources()
    workspace=read_json(ROOT/'evidence/verification/workspace.json')
    assert workspace['sourcePolicy']['passed']and not workspace['gitRemotes']
    assert workspace['isolation']['baselineAndInputsUnchanged']and workspace['isolation']['applicationObservedUnchanged']is False
    assert all(row['category']=='application'for row in workspace['isolation']['observedChanges'])
    roms=[p for p in(ROOT/'build').rglob('*.nds')if p.stat().st_size==175959612
        and sha256(p)=='674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'];assert roms
    write_json(ROOT/'evidence/verification/clean106-final-application-isolation-audit-20261101.json',dict(sourceCredit=0,
        generator=Path(__file__).name,generatorSha256=sha256(__file__),sourceCohort=106,originalScheduleCommands=len(latest),
        latestSuccessfulOriginalBuildOracleCommands=1092,allOriginalCommandIndicesAccounted=True,
        strictFinalWorkspaceCommandPassed=False,finalFailureOnlyObservedApplicationChanges=True,
        observedApplicationChangedFiles=len(workspace['isolation']['observedChanges']),attributionOfThoseChangesNotProven=True,
        baselineAndOriginalInputsUnchanged=True,sourcePolicyPassed=True,remotes=0,sourceAndRegistryHashesUnchanged=True,
        allRegisteredSourceHashesVerified=True,allPriorSuccessfulAndFailedLogsPreserved=True,
        originalFailureAndResumeReportsNotRewritten=True,finalResumeSha256=sha256(ROOT/'evidence/verification/clean106-resumed-v4-20261101.json'),
        workspaceReportSha256=sha256(ROOT/'evidence/verification/workspace.json'),
        exactScaffoldingRoms=[dict(path=p.relative_to(ROOT).as_posix(),sha256=sha256(p),bytes=p.stat().st_size)for p in roms],
        uninterruptedCleanReplayProven=False,latest123Or124CleanReplayProven=False,wholeSourceRom=False,fullNativeGame=False))
    print(dict(originalCommands=len(latest),buildOracleCommandsPassed=1092,strictFinalIsolation=False,
        observedApplicationChangedFiles=len(workspace['isolation']['observedChanges']),exactScaffoldingRoms=len(roms)))


if __name__=='__main__':
    main()
