import copy
import interpreted_sources as source
from project import ROOT, now, read_json, write_json


def main():
    registry = read_json(source.REGISTRY)
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    batch = next(row for row in registry['batches'] if 'proofKind' not in row)
    report = read_json(ROOT / batch['report'])
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    cases = [
        ('foreign-rom', lambda r: r.update(romSha256='0' * 64)),
        ('member-credit-inflation', lambda r: r.update(matchedScriptSourceUnits=8, matchedScriptSourceBytes=1920)),
        ('native-byte-credit', lambda r: r.update(ordinaryNativeExecutableByteCredit=240)),
        ('whole-image-credit', lambda r: r.update(wholeImageDecompiled=True)),
        ('original-bytecode-compiler-input', lambda r: r['compilerBuild'].update(originalRomOrBytecodeInputToCompiler=True)),
        ('interior-entry', lambda r: r['boundaries'].update(externalDirectInteriorEntries=1)),
        ('shared-tail', lambda r: r['boundaries'].update(sharedTailDetected=True)),
        ('source-output-mismatch', lambda r: r['compilerBuild']['build'].update(outputSha256='0' * 64)),
        ('boundary-drift', lambda r: r['matchedRange'].update(endExclusivePc=r['matchedRange']['endExclusivePc'] + 4)),
        ('post-fault-state', lambda r: r.update(postFaultStateUsedForProof=True)),
        ('scaffolding-credit', lambda r: r.update(sourceCreditForScaffolding=1)),
        ('native-vm-namespace', lambda r: r['nativeModuleHashes'].update(main='0' * 64)),
        ('compiler-python-identity', lambda r: r['compilerBuild']['build'].update(pythonExecutableSha256='0' * 64)),
    ]
    results = []
    for name, mutate in cases:
        candidate = copy.deepcopy(report)
        mutate(candidate)
        try:
            source.validated(candidate, image, batch)
        except ValueError as error:
            results.append({'case': name, 'rejected': True, 'reason': str(error)})
        else:
            raise AssertionError('Interpreted source negative was accepted: ' + name)
    duplicate = copy.deepcopy(registry)
    duplicate['batches'].append(copy.deepcopy(batch))
    try:
        source.measure(inventory, duplicate)
    except ValueError as error:
        results.append({'case': 'duplicate-content-instance', 'rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('Duplicate interpreted source inflated coverage')
    stale = copy.deepcopy(batch)
    stale['sourceHashes'][next(iter(stale['sourceHashes']))] = '0' * 64
    try:
        source.validated(report, image, stale)
    except ValueError as error:
        results.append({'case': 'changed-source-compiler-pin', 'rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('Changed interpreted source/compiler was accepted')
    absent = copy.deepcopy(report)
    absent['rebuiltDecodedImage']['path'] = 'work/interpreted-negatives/absent-rebuilt-image.bin'
    if source.validated(absent, image, batch) is not None:
        raise AssertionError('Missing regenerated image retained current source credit')
    results.append({'case': 'absent-generated-product', 'currentSourceCreditUnavailable': True})
    units, unavailable = source.measure(inventory)
    if unavailable or not units:
        raise AssertionError('Current interpreted source evidence is unavailable')
    output = {'createdUtc': now(), 'passed': True, 'checks': results,
              'sourceUnits': len(units), 'sourceBytes': sum(unit['sourceByteCredit'] for unit in units),
              'nativeByteCredit': 0, 'completeImages': 0, 'overallGameCompletionPercentage': None}
    write_json(ROOT / 'evidence/verification/interpreted-source-negatives-20261029.json', output)
    print({'passed': True, 'negativeChecks': len(results), 'sourceBytes': output['sourceBytes']})


if __name__ == '__main__':
    main()
