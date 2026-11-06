from project import ROOT,read_json,write_json,sha256,now,configuration
from recovery_registry import verify_sources


def main():
    verify_sources()
    path=ROOT/'evidence/verification/cohort-2026-10-29-74.json'
    plan=read_json(path)
    driver=read_json(ROOT/'evidence/verification/cohort74-validation-driver.json')
    manifest=read_json(ROOT/'manifest.json')
    workspace=read_json(ROOT/'evidence/verification/workspace.json')
    freshness=read_json(ROOT/'evidence/verification/evidence-freshness.json')
    checksum=read_json(ROOT/'evidence/matches/checksum.json')
    getters=read_json(ROOT/'evidence/save/native-getter-results.json')
    assert driver['state']=='build-and-regression-checks-passed'
    assert plan['sourceRegistrySha256']==sha256(ROOT/'recovery.json')==driver['sourceRegistrySha256']
    assert manifest['functionMatched']==plan['expectedSourceMatchedFunctions']==8848
    assert manifest['sourceLinkedBytes']==plan['expectedSourceLinkedBytes']==654785
    assert manifest['exactContainerMatchWithScaffolding'] and not manifest['rejectedMatchEvidence']
    assert freshness['passed'] and freshness['restoredSourceFunctions']==8848
    assert workspace['sourcePolicy']['passed'] and workspace['isolation']['baselineAndInputsUnchanged']
    assert checksum['oracle']['vectors']==36 and checksum['oracle']['executions']==144
    assert checksum['oracle']['verifiedReturn'] and checksum['oracle']['isolatedState'] and len(checksum['functionMatches'])==2
    assert getters['totalComparisons']==5117 and getters['sourceFilesUnchanged']
    output=ROOT/'build/exact-layout.nds'
    assert output.stat().st_size==175959612 and sha256(output)==configuration()['romSha256']
    total=sum(row['bytes'] for row in manifest['modules'])
    comparisons=sum(manifest[key] for key in ['currentHostArm9ModuleLinksExact','arm7RuntimeModuleLinksExact','currentUtilityModuleLinksExact'])
    assert comparisons==20
    plan.update(linksPending=False,acceptedBuildCreatedUtc=now(),sourceMatchedFunctions=manifest['functionMatched'],
        sourceLinkedBytes=manifest['sourceLinkedBytes'],manifestSha256=sha256(ROOT/'manifest.json'),moduleComparisonsExact=comparisons,
        exactRom={'bytes':output.stat().st_size,'sha256':sha256(output)},negativeAcceptanceChecksPassed=freshness['passed'],
        sourcePolicyPassed=workspace['sourcePolicy']['passed'],baselineAndInputsUnchanged=workspace['isolation']['baselineAndInputsUnchanged'],
        applicationObservedUnchanged=workspace['isolation']['applicationObservedUnchanged'],getterComparisons=getters['totalComparisons'],
        getterReportSha256=sha256(ROOT/'evidence/save/native-getter-results.json'),sourceCoveragePercentage=100*manifest['sourceLinkedBytes']/total,
        initializedModuleByteDenominator=total,unresolvedInitializedModuleBytes=total-manifest['sourceLinkedBytes'],
        executableOnlyDenominatorProven=False,overallGameCompletionPercentage=None,checksumVectors=36,checksumActualReturns=144,
        checksumExactMatches=2,sourceFunctionBytesIncludingPools=manifest['sourceMatchedFunctionBytes'],sourceDataBytes=manifest['sourceMatchedDataBytes'],
        strictWholeWorkspaceIsolationPassed=workspace['isolation']['allRecordedFilesUnchanged'],
        fullCleanReplayOfThisCohortProven=False)
    write_json(path,plan)
    print({key:plan[key] for key in ['sourceMatchedFunctions','sourceLinkedBytes','sourceCoveragePercentage','moduleComparisonsExact','linksPending']})


if __name__=='__main__':
    main()
