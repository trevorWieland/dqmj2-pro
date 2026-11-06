import copy
from project import ROOT, read_json, write_json
import interpreted_linked_sources as linked


def main():
    path = 'evidence/matches/scripts-20261029-reset-calls.json'
    original = read_json(ROOT / path)
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    batches = linked.candidates(original, path, ['match_scr_resets_20261029_batch02.py'])
    batch = batches[0]
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    rows = []

    def reject(name, mutate, message):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        try:
            linked.validated(report, image, accepted)
        except (ValueError, KeyError, StopIteration) as error:
            if message not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), message))
            rows.append({'name': name, 'rejected': True, 'reason': str(error)})
            return
        raise AssertionError('Invalid linked SCR proof accepted: ' + name)

    reject('native-byte-credit', lambda r, b: r.update(ordinaryNativeExecutableByteCredit=1), 'unsupported execution or source credit')
    reject('complete-image-credit', lambda r, b: r.update(completeImagesRecovered=1), 'unsupported execution or source credit')
    reject('post-fault-credit', lambda r, b: r.update(postFaultStateUsedForProof=True), 'unsupported execution or source credit')
    reject('member-alias-inflation', lambda r, b: r.update(completeFunctionInstances=32), 'function-instance count differs')
    reject('authored-definition-inflation', lambda r, b: r.update(sourceFunctionDefinitions=4), 'definition count differs')
    reject('qualified-byte-inflation', lambda r, b: r.update(qualifiedRangeBytes=999), 'qualified byte count differs')
    reject('native-VM-namespace', lambda r, b: b['nativeModuleHashes'].update(main='0' * 64), 'VM namespace differs')
    reject('incomplete-call-tree', lambda r, b: r['modules'][0]['differential']['cases'][0].update(completeSourceCallTreeTerminated=False), 'function did not return')
    reject('incomplete-native-return', lambda r, b: r['modules'][0]['differential']['cases'][0]['observations'][0].update(actualReturn=False), 'incomplete calls')
    reject('unbalanced-script-stack', lambda r, b: r['modules'][0]['differential']['cases'][0]['trace'][-1].update(depthAfter=1), 'stack proof differs')
    reject('original-bytecode-compiler-input', lambda r, b: r['modules'][0]['sourceOnlyBuilds'][0].update(originalBytecodeCompilerInput=True), 'consumes original bytecode')
    reject('unexpected-compiler-input', lambda r, b: r['modules'][0]['sourceOnlyBuilds'][0]['sourceOnlyInputs'].append({'path': 'inputs/game.nds', 'sha256': r['romSha256']}), 'unexpected input files')
    reject('unreconstructed-named-target', lambda r, b: r['modules'][0]['sourceOnlyBuilds'][1]['build']['scriptBindings'].update(before_primary_flag_reset=53068), 'no reconstructed source unit')
    reject('external-interior-entry', lambda r, b: r['modules'][0]['boundaries'][0]['knownIncomingDirectReferences'].append({'sourcePc': 0, 'targetPc': 53068}), 'function interior')
    reject('shared-return-tail', lambda r, b: r['modules'][0]['boundaries'][0].update(sharedReturnTailDetected=True), 'boundary sharing')
    reject('adjacent-metadata-credit', lambda r, b: r['modules'][0]['boundaries'][0].update(adjacentEightBytesSourceCredit=8), 'boundary sharing')
    reject('wrong-scaffolding-account', lambda r, b: r['modules'][0].update(originalScaffoldBytes=0), 'scaffolding accounting differs')
    reject('unproved-whole-image-coverage', lambda r, b: r['modules'][0]['boundaries'][0].update(indirectOrOpaqueOutsideControlFlowCoverageClaimed=True), 'boundary sharing')
    reject('failed-negative-compiler-control', lambda r, b: r['compilerControls']['negativeCases'][0].update(rejectedBeforeOutput=False), 'Invalid SCR source/link accepted')
    reject('bad-aligned-binding-control', lambda r, b: r['compilerControls'].update(wrongAlignedBindingDoesNotMatchOriginal=False), 'binding controls failed')
    reject('changed-source-pin', lambda r, b: b['sourceHashes'].update(scr_c_compiler_20261029_v2='0' * 64), 'frozen registry')
    report = copy.deepcopy(original)
    command = report['modules'][0]['sourceOnlyBuilds'][0]['command']
    command[command.index('--output') + 1] = 'intentionally-missing-product.scrfunc'
    if linked.validated(report, image, batch) is not None:
        raise AssertionError('Absent linked SCR product retained source credit')
    rows.append({'name': 'missing-product-credit-withheld', 'creditUnavailable': True})
    units = [linked.validated(original, next(row for row in inventory['images'] if row['codeSha256'] == item['identity']['codeSha256']), item)
             for item in batches]
    if any(unit is None for unit in units):
        raise AssertionError('Positive linked SCR source build is unavailable')
    result = {'passed': True, 'negativeControls': rows, 'sourceInstances': len(units),
              'qualifiedBytes': sum(unit['sourceByteCredit'] for unit in units),
              'authoredDefinitions': len({unit['sourceDefinitionId'] for unit in units}),
              'nativeByteCredit': 0, 'completeImageCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-linked-source-negatives-20261029.json', result)
    print({key: value for key, value in result.items() if key != 'negativeControls'}, len(rows))


if __name__ == '__main__':
    main()
