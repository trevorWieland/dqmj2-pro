import argparse
import json
import subprocess
import sys
from pathlib import Path
from project import ROOT, read_json, sha256, write_json
from finish_source_package_context import PINS, verify
from staged_git_checks import names, check


SUPPORT = ['source_packet_committed_context.py', 'resume_source_packet_closure.py',
    'qualify_ten_consumers_v2.py', 'test_ten_consumers_v2.py', 'ten-consumer-contract-v2.json',
    'evidence/verification/cohort175-main-consumer-inventory-v2-20261107.json',
    'evidence/verification/cohort175-preference-context-qualification-20261107.json',
    'evidence/verification/cohort175-committed-context-qualification-20261107.json',
    'qualify_child_snd_reference_v1_20261107.py', 'test_child_reference.py',
    'child-snd-reference-contract-v1.json']

PACKAGING_SUPPORT = ['registered_input_path_context_v1_20261107.py',
    'test_registered_input_path_context.py',
    'provenance/cohort175-registered-input-paths-v1-20261107.json',
    'evidence/verification/cohort175-child-reference-context-qualification-20261107.json',
    'evidence/lanes/parallel-wave20261106/goal-resume-source-2/layout-position/canonical-replay.log',
    'evidence/lanes/parallel-wave20261106/goal-resume-source-2/layout-position/copied-root.log',
    'evidence/lanes/parallel-wave20261106/goal-resume-source-2/layout-position/traces.json.gz',
    'work/frozen-runtime-inputs/a12b5b643da4a5a57f765094efca9da83b48d2f2a0db9f3ef07f55861080a0d8/ledger/functions.jsonl',
    'work/goal-resume-20261106/source-2-controller/lq/a/p/172f1dcc9e55c032f6f3e22ff8764d835d4e9a3fa3be647384aa3afdc0410711.lcf',
    'work/goal-resume-20261106/source-2-controller/lq/a/p/62318c5c02f4ee778b3d763375667d480407972ba130da6dd3a0f7334ad50c43.json',
    'work/goal-resume-20261106/source-2-controller/lq/a/p/98f73b835425d2ca3f11e4d4945005b0b30160287acc447e61b9fa1a9f4b4c54.json',
    'work/goal-resume-20261106/source-2-controller/lq/a/p/9cc26793317bda9280dbf336e7744ef32cc8406208f6925fc66cdecf3c1d4639.bin',
    'work/goal-resume-20261106/source-2-controller/lq/a/p/c9674aed84c286f39486b7c432e7b35d0ba363d945662908c5e9ca463846d4a5.elf',
    'work/goal-resume-20261106/source-2-controller/lq/p/main-0x2076440/e74759ec88c4b3da-3f1785c717c2/9cc26793317bda9280dbf336e7744ef32cc8406208f6925fc66cdecf3c1d4639.bin',
    'work/goal-resume-20261106/source-2-controller/lq/p/main-0x2076440/e74759ec88c4b3da-3f1785c717c2/e2e6db390dbfa134b195e06a42d4a7c15ded25cae8140b8955be09a54ca8297c.o']


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def committed(name, revision='HEAD'):
    raw = git('show', revision + ':' + name)
    if raw != (ROOT / name).read_bytes():
        raise ValueError('Closure continuation changed a committed input: ' + name)
    return raw


def run(script, cohort, log):
    with (ROOT / log).open('wb') as stream:
        subprocess.run([sys.executable, '-B', str(ROOT / script), '--cohort', str(cohort)],
                       cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cohort', type=int, required=True)
    parser.add_argument('--transaction-commit', required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--qualification', required=True)
    args = parser.parse_args()
    if args.cohort < 175:
        raise ValueError('Historical closures retain their frozen finishers')
    verify()
    source = git('rev-parse', 'HEAD').decode().strip()
    if source != args.source_commit or names(subprocess, ROOT):
        raise ValueError('Resume requires the exact reviewed committed source/support frontier and empty index')
    transaction = git('rev-parse', args.transaction_commit + '^{commit}').decode().strip()
    subprocess.run(['git', 'merge-base', '--is-ancestor', transaction, source], cwd=ROOT, check=True)
    changed = set(filter(None, git('diff', '--name-only', '-z', transaction, source).decode().split('\0')))
    if changed != set(SUPPORT + PACKAGING_SUPPORT) | {args.qualification}:
        raise ValueError('Continuation changed source transaction inputs or unreviewed support files')
    for name in SUPPORT + PACKAGING_SUPPORT + [args.qualification]:
        committed(name)
    qualification = read_json(ROOT / args.qualification)
    if qualification.get('passed') is not True or qualification.get('sourceCredit') != 0:
        raise ValueError('Preference context qualification is not passed and zero-credit')
    if (qualification['testsPassed'] != 126
            or qualification['testCounts'] != dict(referenceTests=49, preferenceTests=32, registeredPathTests=45)):
        raise ValueError('Reviewed reference, preference and path-context test counts differ')
    if qualification['helperSha256'] != sha256(ROOT / SUPPORT[0]):
        raise ValueError('Qualified preference helper identity differs')
    if qualification['resumeHelperSha256'] != sha256(ROOT / SUPPORT[1]):
        raise ValueError('Qualified continuation helper identity differs')
    if (len(qualification['referenceSupport']) != 4
            or {pin['path'] for pin in qualification['referenceSupport']} != set(SUPPORT[2:6])):
        raise ValueError('Current-reference qualification support scope differs')
    for pin in qualification['referenceSupport']:
        if pin['path'] not in SUPPORT or sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Qualified current-reference support input differs')
    if (len(qualification['childReferenceSupport']) != 3
            or {pin['path'] for pin in qualification['childReferenceSupport']} != set(SUPPORT[8:])):
        raise ValueError('Child-reference qualification support scope differs')
    for pin in qualification['childReferenceSupport']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Qualified child-reference support input differs')
    if ({pin['path'] for pin in qualification['registeredInputPathSupport']} != set(PACKAGING_SUPPORT[:3])
            or len(qualification['registeredInputPathSupport']) != 3
            or {pin['path'] for pin in qualification['packagedProofInputs']} != set(PACKAGING_SUPPORT[4:])
            or len(qualification['packagedProofInputs']) != 11):
        raise ValueError('Registered input packaging support scope differs')
    for pin in qualification['registeredInputPathSupport'] + qualification['packagedProofInputs']:
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Registered input packaging qualification pin differs')
    prior_child = qualification['priorChildReferenceQualification']
    if prior_child['path'] != PACKAGING_SUPPORT[3] or sha256(ROOT / prior_child['path']) != prior_child['sha256']:
        raise ValueError('Frozen prior child-reference qualification differs')
    prefix = f'evidence/verification/cohort{args.cohort}'
    plan_name = f'evidence/verification/cohort-2026-10-29-{args.cohort}.json'
    driver_name = prefix + '-validation-driver.json'
    snapshot_name = f'evidence/verification/accepted-cohort{args.cohort}-identities-v2-20261101.json'
    for name in [plan_name, driver_name, snapshot_name, 'recovery.json', 'source-preferences.json',
                 'manifest.json', 'ledger/functions.jsonl', prefix + '-captured-oracle-closure-20261031.json']:
        committed(name, transaction)
        committed(name)
    plan, driver, snapshot = map(lambda name: read_json(ROOT / name), [plan_name, driver_name, snapshot_name])
    manifest = read_json(ROOT / 'manifest.json')
    if (plan['linksPending'] or plan['moduleComparisonsExact'] != 20
            or driver['state'] != 'build-and-regression-checks-passed' or len(driver['steps']) != 16
            or plan['negativeAcceptanceChecksPassed'] is not True or plan['sourcePolicyPassed'] is not True
            or plan['baselineAndInputsUnchanged'] is not True
            or (plan['checksumVectors'], plan['checksumActualReturns'], plan['checksumExactMatches'],
                plan['getterComparisons']) != (36, 144, 2, 5117)
            or plan['sourceMatchedFunctions'] != plan['expectedSourceMatchedFunctions']
            or plan['sourceLinkedBytes'] != plan['expectedSourceLinkedBytes']
            or manifest['functionMatched'] != plan['sourceMatchedFunctions']
            or manifest['sourceLinkedBytes'] != plan['sourceLinkedBytes']
            or sha256(ROOT / 'manifest.json') != plan['manifestSha256']
            or sha256(ROOT / 'recovery.json') != plan['sourceRegistrySha256']
            or sha256(ROOT / 'source-preferences.json') != plan['sourcePreferenceSha256']
            or snapshot['ledgerSha256'] != sha256(ROOT / 'ledger/functions.jsonl')
            or snapshot['acceptedEvidenceSha256'] != sha256(ROOT / plan_name)):
        raise ValueError('Original finalized source, snapshot or sixteen-stage predicates differ')
    exact = ROOT / 'build/exact-layout.nds'
    if (not manifest['exactContainerMatchWithScaffolding'] or exact.stat().st_size != plan['exactRom']['bytes']
            or sha256(exact) != plan['exactRom']['sha256']):
        raise ValueError('Original finalizer exact scaffold-assisted container predicate differs')
    run(SUPPORT[0], args.cohort, f'logs/integration/cohort{args.cohort}-source-input-audit-resumed-20261107.txt')
    run('verify_captured_oracle_closure_20261031.py', args.cohort,
        f'logs/integration/cohort{args.cohort}-captured-closure-audit-resumed-20261107.txt')
    reports = [prefix + '-committed-source-inputs-v14-20261105.json',
               prefix + '-captured-oracle-closure-verification-20261031.json',
               prefix + '-overlay-reference-context-v11-20261107.json']
    for name in reports:
        report = read_json(ROOT / name)
        proof = report.get('committedVerification', report)
        if proof.get('passed') is not True or proof.get('commit') != source:
            raise ValueError('Fresh closure component does not bind this exact source/support commit')
    context = read_json(ROOT / reports[-1])
    native = context['namespaceQualifiedOverlayReference']
    if (native['functions'] != 39 or not native['allC99FunctionBytesRelocationsMappingsAndFreshNativeLinksEqual']
            or not context['allOriginalContextV9AndUnderlyingCommittedGlobalAuditsCompleted']
            or not native['preferenceAppendExtension']['allOriginalPreferenceRecordsPreserved']):
        raise ValueError('Complete original overlay and preference qualification did not finish')
    current = native['currentMainReferenceQualification']
    fresh = current['liveQualification']
    if (fresh['passed'] is not True or fresh['sourceCredit'] != 0
            or fresh['functions'] != 10 or fresh['bytes'] != 2100
            or len(fresh['qualifications']) != 10 or not fresh['originalRegistryGateUnchanged']
            or current['transientMainLedgerOriginalConsumers'] != 26
            or current['transientMainLedgerAdditionalConsumers'] != 10
            or not current['canonicalRegistryAndLedgerUnmodified']):
        raise ValueError('Complete current main-reference qualification did not finish')
    if (not current['projectionEvents'] or any(len(event) != 10
            or sum(len(row['removed']) for row in event) != 7 for event in current['projectionEvents'])):
        raise ValueError('Exact ten-consumer seven-overlay projection was not exercised')
    child = native['childArm9ReferenceQualification']
    qualified_child = child['liveQualification']
    if (qualified_child['passed'] is not True or qualified_child['sourceCredit'] != 0
            or (qualified_child['functions'], qualified_child['bytes']) != (1, 196)
            or qualified_child['report'] != 'evidence/matches/cohort174-parallel-wave20261105-s-child-snd-resume-0.json'
            or qualified_child['sourceOnlyCompilerInput']['originalCodeCompilerInput'] is not False
            or not qualified_child['originalRegistryGateUnchanged']
            or not qualified_child['canonicalRegistryReportsSourcesObjectsAndProfilesUnmodified']
            or not qualified_child['prescribedFinalO4pToO0Rejected']
            or len(qualified_child['freshGenuineLink']['bindings']) != 8
            or not child['projectionAfterExistingCanonicalRegistryGate']
            or not child['exactTenAndOldNamespaceChecksUnmodified']):
        raise ValueError('Complete separate child ARM9 reference qualification did not finish')
    if (not child['childProjectionEvents'] or any(event['report'] != qualified_child['report']
            or event['removed'] != read_json(ROOT / SUPPORT[-1])['referencePins']
            for event in child['childProjectionEvents'])):
        raise ValueError('Exact one-child two-reference projection was not exercised')
    registered = native['registeredInputPathQualification']
    registered_contract = read_json(ROOT / PACKAGING_SUPPORT[2])
    canonical = registered_contract['canonicalSource']
    if (registered['passed'] is not True or registered['sourceCredit'] != 0
            or registered['setup']['ready'] is not True or registered['setup']['revision'] != source
            or registered['setup']['inputsChecked'] != 25
            or registered['setup']['missingCurrent'] or registered['setup']['missingCommitted']
            or registered['setup']['proofInputCount'] != 11
            or registered['setup']['proofInputBytes'] != 32672592
            or len(registered['events']) != 7
            or {event['path'] for event in registered['events']}
            != {row['path'] for row in registered_contract['evidenceViews']}
            or any(event != dict(path=event['path'], field='previous.source', before=canonical['rawPath'],
                after=canonical['path'], sourceSha256=canonical['sha256'], allOtherFieldsIdentical=True)
                for event in registered['events'])
            or registered['observedAccounting'] != dict(rawLogicalAliasCount=21439, canonicalPathCount=21438,
                removedDuplicateKeys=1, canonicalSourceQueries=1, sourceCredit=0)):
        raise ValueError('Exact seven-evidence path identity and eleven-proof packaging qualification did not finish')
    if git('rev-parse', 'HEAD').decode().strip() != source or names(subprocess, ROOT):
        raise ValueError('Committed frontier or index changed during closure audits')
    for name in [plan_name, driver_name, snapshot_name, 'recovery.json', 'source-preferences.json', 'manifest.json',
                 'ledger/functions.jsonl', prefix + '-captured-oracle-closure-20261031.json',
                 *SUPPORT, *PACKAGING_SUPPORT, args.qualification]:
        committed(name)
    closure_name = prefix + '-expanded-source-closure-20261101.json'
    if (ROOT / closure_name).exists():
        raise ValueError('Cannot overwrite an existing expanded closure')
    write_json(ROOT / closure_name, dict(cohort=args.cohort, sourceCommit=source,
        sourceAcceptanceTransactionCommit=transaction, passed=True, sourceCredit=0, fullCleanReplayProven=False,
        reports=[dict(path=name, sha256=sha256(ROOT / name)) for name in reports],
        finisherContext=dict(originalFinisher='finish_source_package_v25_20261106.py', pinnedEntrypoints=PINS,
            originalSixteenGatesAndFinalizerAndCommittedSourceTransactionRetained=True,
            duplicateSourceStagingOrAcceptanceCommit=False, continuationGenerator=Path(__file__).name,
            continuationGeneratorSha256=sha256(__file__), qualification=dict(path=args.qualification,
                sha256=sha256(ROOT / args.qualification)),
            committedSupport=[dict(path=name, sha256=sha256(ROOT / name)) for name in SUPPORT + PACKAGING_SUPPORT], sourceCredit=0)))
    subprocess.run(['git', 'add', '--', *reports, closure_name], cwd=ROOT, check=True)
    staged = names(subprocess, ROOT)
    if set(staged) != set(reports + [closure_name]):
        raise ValueError('Closure commit contains paths outside its reviewed components')
    command = ['git', '-c', 'core.whitespace=cr-at-eol', 'diff', '--cached', '--check']
    result = check(subprocess, ROOT, command, staged)
    if result.returncode:
        raise ValueError('New closure component whitespace check failed')
    verify()
    subprocess.run(['git', 'commit', '-m', f'Verify cohort {args.cohort} committed source and oracle closure'],
                   cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
    for name in reports + [closure_name]:
        committed(name)
    print(json.dumps(dict(cohort=args.cohort, sourceCommit=source, transactionCommit=transaction,
        closureCommit=git('rev-parse', 'HEAD').decode().strip(), sourceFunctions=plan['sourceMatchedFunctions'],
        sourceBytes=plan['sourceLinkedBytes'], packaged=True)))


if __name__ == '__main__':
    main()
