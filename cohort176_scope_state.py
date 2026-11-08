from copy import deepcopy
from datetime import datetime
import hashlib
import json
from pathlib import PurePosixPath

PENDING_SHA = 'fb4454849a40683fce80cfff9a43e9d7aaafc9a2e87f2973537ec416101d26de'
DRIVER_SHA = 'ba6d931869ba8838932b6b454852adad9bb20c49a56094973e6dc78433a6d218'
WORKSPACE_SHA = 'af5bb0b30e19bc8608f91cd1f7bef16dcd91a13c2fa6b1466bfd9e11487ed3a1'
ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'


def require(value, message):
    if not value:
        raise ValueError(message)


def encode(record):
    return (json.dumps(record, indent=2, ensure_ascii=True, allow_nan=False) + '\n').encode('utf-8')


def pin(path, raw):
    return dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


def reference(row):
    require(type(row) is dict and type(row.get('path')) is str and bool(row['path'])
            and not PurePosixPath(row['path']).is_absolute() and '\\' not in row['path']
            and '..' not in PurePosixPath(row['path']).parts, 'reference path invalid')
    require(type(row.get('bytes')) is int and row['bytes'] > 0 and type(row.get('sha256')) is str
            and len(row['sha256']) == 64 and all(c in '0123456789abcdef' for c in row['sha256']), 'reference pin invalid')


def build_records(pending_plan, scope_proof, failed_driver, references, accepted_build_created_utc):
    pending, proof, refs = pending_plan, scope_proof, references
    for name in ('originalPendingPlan', 'originalFailedDriver', 'originalWorkspace', 'contract', 'proof',
                 'manifest', 'getters', 'exactRom'):
        reference(refs[name])
    require(refs['originalPendingPlan']['sha256'] == PENDING_SHA and refs['originalPendingPlan']['bytes'] == 2486
            and refs['originalFailedDriver']['sha256'] == DRIVER_SHA
            and refs['originalWorkspace']['sha256'] == WORKSPACE_SHA, 'original provenance differs')
    require(refs['exactRom']['sha256'] == ROM_SHA and refs['exactRom']['bytes'] == 175959612, 'ROM differs')
    require(type(accepted_build_created_utc) is str
            and datetime.fromisoformat(accepted_build_created_utc).utcoffset() is not None
            and proof['qualificationCompletedUtc'] == accepted_build_created_utc, 'qualification time differs')
    require(pending['linksPending'] is True and pending['previousAcceptedCohort'] == 175
            and pending['previousAcceptedFunctions'] == 11652 and pending['previousAcceptedBytes'] == 1265646
            and pending['newSourceFunctions'] == 8 and pending['newSourceBytes'] == 1412
            and pending['expectedSourceMatchedFunctions'] == 11660
            and pending['expectedSourceLinkedBytes'] == 1267058, 'pending scope differs')
    require(type(pending['duplicateMigrationFunctions']) is int and pending['duplicateMigrationFunctions'] == 0
            and pending.get('migrationReports', []) == [], 'migration scope differs')
    require(proof['cohort'] == 176 and proof['MainMatchingWorkspaceScopePassed'] is True
            and proof['preservedSuccessfulGates'] == 15 and proof['historicalOriginalGateExitCode'] == 1
            and proof['sourceCreditAddedByScopeRepair'] == 0, 'scope proof not qualified')
    for name in ('allRecordedFilesUnchanged', 'baselineAndInputsUnchanged', 'applicationObservedUnchanged',
                 'strictWholeWorkspaceIsolationPassed', 'fullToolDelivery', 'fullCleanReplayOfThisCohortProven'):
        require(proof[name] is False, 'historical/delivery status hidden')
    require(proof['sourceRegistrySha256'] == pending['sourceRegistrySha256'] == failed_driver['sourceRegistrySha256']
            and proof['sourcePreferenceSha256'] == pending['sourcePreferenceSha256']
            and proof['contractSha256'] == refs['contract']['sha256'], 'scope identity differs')
    require(proof['sourceMatchedFunctions'] == 11660 and proof['sourceLinkedBytes'] == 1267058
            and proof['moduleComparisonsExact'] == 20 and proof['checksumVectors'] == 36
            and proof['checksumActualReturns'] == 144 and proof['getterComparisons'] == 5117
            and proof['sourceReconstructionComplete'] is False, 'qualified acceptance facts differ')
    require(refs['proof'] == pin(refs['proof']['path'], encode(proof)), 'proof serialization differs')
    require(failed_driver['state'] == 'failed' and len(failed_driver['steps']) == 16
            and all(type(r['exitCode']) is int and r['exitCode'] == 0 for r in failed_driver['steps'][:15])
            and failed_driver['steps'][-1]['command'] == ['verify_workspace.py']
            and type(failed_driver['steps'][-1]['exitCode']) is int and failed_driver['steps'][-1]['exitCode'] == 1,
            'original gate history differs')
    require(set(refs['scopedDriver']) == {'path'}, 'driver self-pin forbidden')
    reference(dict(path=refs['scopedDriver']['path'], bytes=1, sha256='0' * 64))
    driver = dict(schemaVersion=1, cohort=176, state='QUALIFIED_CURRENT_MAIN_MATCHING_INPUTS',
        acceptanceScope='current-main-matching-inputs', originalGateExitCode=1,
        originalFailedDriver=deepcopy(refs['originalFailedDriver']), originalWorkspace=deepcopy(refs['originalWorkspace']),
        originalPendingPlan=deepcopy(refs['originalPendingPlan']), scopeContract=deepcopy(refs['contract']),
        workspaceScopeProof=deepcopy(refs['proof']), sourceRegistrySha256=proof['sourceRegistrySha256'],
        preservedSuccessfulGates=15, reusedPassedSteps=deepcopy(failed_driver['steps'][:15]),
        scopeSummary=deepcopy(proof), committedClosureRequired=True, sourceCreditAddedByScopeRepair=0)
    facts = refs['manifestFacts']
    require(facts['initializedModuleByteDenominator'] == 2512636
            and all(type(facts[n]) is int and 0 <= facts[n] <= 1267058
                    for n in ('sourceMatchedFunctionBytes', 'sourceMatchedDataBytes')), 'manifest facts differ')
    current = deepcopy(pending)
    current.update(linksPending=False, transactionPreparedOnly=False, acceptedBuildCreatedUtc=accepted_build_created_utc,
        acceptanceScope='current-main-matching-inputs', sourceMatchedFunctions=11660, sourceLinkedBytes=1267058,
        manifestSha256=refs['manifest']['sha256'], moduleComparisonsExact=20, exactRom=deepcopy(refs['exactRom']),
        negativeAcceptanceChecksPassed=True, sourcePolicyPassed=True, baselineAndInputsUnchanged=False,
        applicationObservedUnchanged=False, allRecordedFilesUnchanged=False, strictWholeWorkspaceIsolationPassed=False,
        fullToolDelivery=False, MainMatchingWorkspaceScopePassed=True, missingCachePins=deepcopy(proof['missingCachePins']),
        getterComparisons=5117, getterReportSha256=refs['getters']['sha256'], checksumVectors=36,
        checksumActualReturns=144, checksumExactMatches=2, sourceCoveragePercentage=100 * 1267058 / 2512636,
        initializedModuleByteDenominator=2512636, unresolvedInitializedModuleBytes=2512636 - 1267058,
        sourceFunctionBytesIncludingPools=facts['sourceMatchedFunctionBytes'], sourceDataBytes=facts['sourceMatchedDataBytes'],
        executableOnlyDenominatorProven=False, overallGameCompletionPercentage=None,
        fullCleanReplayOfThisCohortProven=False, sourceCreditAddedByScopeRepair=0, committedClosureRequired=True,
        migrationReports=[], originalPendingPlan=deepcopy(refs['originalPendingPlan']),
        originalFailedDriver=deepcopy(refs['originalFailedDriver']), originalWorkspace=deepcopy(refs['originalWorkspace']),
        scopeContract=deepcopy(refs['contract']), workspaceScopeProof=deepcopy(refs['proof']),
        scopedDriver=pin(refs['scopedDriver']['path'], encode(driver)))
    return driver, current
