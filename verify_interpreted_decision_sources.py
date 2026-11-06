import copy
from project import ROOT, read_json, write_json
import interpreted_decision_sources as decision


def main():
    path = 'evidence/matches/scripts-20261029-runtime-decisions.json'
    original = read_json(ROOT / path)
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    batches = decision.candidates(original, path, ['match_scr_decisions_20261029_batch03.py'])
    batch = batches[0]
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    rows = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        try:
            decision.validated(report, image, accepted)
        except ValueError as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            rows.append({'name': name, 'rejected': True, 'reason': str(error)})
            return
        raise AssertionError('Invalid SCR decision proof accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'namespace differs')
    reject('native-credit', lambda r, b: r.update(ordinaryNativeExecutableByteCredit=1), 'unsupported credit')
    reject('complete-image-credit', lambda r, b: r.update(completeImagesRecovered=1), 'unsupported credit')
    reject('unqualified-runtime-API', lambda r, b: r['namedRuntimeApiLinks']['get_primary_flag'].update(nativeModuleSha256='0' * 64), 'API identity differs')
    reject('unproved-branches', lambda r, b: r.update(allSupportedOriginalBranchOutcomesTested=False), 'branch proof is incomplete')
    reject('member-inflation', lambda r, b: r.update(completeFunctionInstances=16), 'instance/image count differs')
    reject('definition-inflation', lambda r, b: r.update(sourceFunctionDefinitions=16), 'definition count differs')
    reject('bad-compiler-control', lambda r, b: r['compilerControls']['rejectedSourcesOrProfiles'][0].update(rejectedBeforeOutput=False), 'source/profile control failed')
    reject('bad-allocation-control', lambda r, b: r['compilerControls'].update(wrongAllocationProfileDoesNotMatchOriginal=False), 'allocation/CLI controls failed')
    reject('external-interior-transfer', lambda r, b: r['modules'][0]['boundaries']['knownIncomingDirectReferences'].append({'sourcePc': 0, 'targetPc': 57136}), 'transfer enters an interior')
    reject('shared-return', lambda r, b: r['modules'][0]['boundaries'].update(sharedReturnTailDetected=True), 'direct sharing or inflated coverage')
    reject('original-compiler-bytecode-input', lambda r, b: r['modules'][0]['sourceOnlyBuild'].update(originalBytecodeCompilerInput=True), 'consumes bytecode')
    reject('unexpected-input-closure', lambda r, b: r['modules'][0]['sourceOnlyBuild']['sourceOnlyInputClosure'].append({'path': 'inputs/game.nds', 'sha256': r['romSha256']}), 'unexpected inputs')
    reject('wrong-slot-profile', lambda r, b: r['modules'][0]['sourceOnlyBuild']['build'].update(localAllocationBase=95), 'local allocation differs')
    reject('external-slot-reference', lambda r, b: r['modules'][0]['boundaries']['runtimeVariable']['knownDirectSlotReferences'][0].update(pc=0), 'slot references or coverage differ')
    reject('interleaved-call-claim', lambda r, b: r['modules'][0]['differential'].update(interleavedOrReentrantScratchSemanticsCertified=True), 'scratch-call ABI differs')
    reject('missing-repeated-state-model', lambda r, b: r['modules'][0]['differential']['cases'][0].update(independentSecondInvocationSeesClearedFlag=False), 'repeated-state model differs')
    reject('premature-termination', lambda r, b: r['modules'][0]['differential']['cases'][0]['first'].update(completeFunctionTerminated=False), 'independent branch/effect model differs')
    reject('spurious-false-path-write', lambda r, b: r['modules'][0]['differential']['cases'][0]['first']['targetByteWrites'].append([0, 1]), 'independent branch/effect model differs')
    reject('wrong-runtime-Boolean', lambda r, b: r['modules'][0]['differential']['cases'][0]['first'].update(runtimeBooleanSlotWord=0x7FC00000), 'independent branch/effect model differs')
    absent = copy.deepcopy(original)
    command = absent['modules'][0]['sourceOnlyBuild']['command']
    command[command.index('--output') + 1] = 'intentionally-absent-decision-product.scrfunc'
    if decision.validated(absent, image, batch) is not None:
        raise AssertionError('Absent SCR decision product retained source credit')
    rows.append({'name': 'missing-product-withholds-credit', 'creditUnavailable': True})
    units = [decision.validated(original, next(row for row in inventory['images'] if row['codeSha256'] == item['identity']['codeSha256']), item)
             for item in batches]
    if any(unit is None for unit in units):
        raise AssertionError('Positive SCR decision source build unavailable')
    result = {'passed': True, 'controls': rows, 'sourceInstances': len(units),
              'qualifiedBytes': sum(unit['sourceByteCredit'] for unit in units),
              'authoredDefinitions': len({unit['sourceDefinitionId'] for unit in units}), 'nativeByteCredit': 0, 'completeImages': 0}
    write_json(ROOT / 'evidence/verification/interpreted-decision-source-negatives-20261029.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, len(rows))


if __name__ == '__main__':
    main()
