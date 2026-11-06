import copy
import json
from project import ROOT, read_json, write_json
import interpreted_empty_sources as empty
import interpreted_numeric_sources as numeric
from validate_scr_empty_family_20261029_batch04 import native_case


def main():
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    registry = read_json(ROOT / 'interpreted-recovery.json')
    group = next(row for row in registry['batches'] if row.get('proofKind') == empty.KIND)
    number = next(row for row in registry['batches'] if row.get('proofKind') == numeric.KIND)
    empty_report, numeric_report = read_json(ROOT / group['report']), read_json(ROOT / number['report'])
    image = next(row for row in inventory['images'] if row['codeSha256'] == number['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-bulk-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    rows = []

    def reject(kind, name, mutation, reason):
        report = copy.deepcopy(empty_report if kind == 'empty' else numeric_report)
        accepted = copy.deepcopy(group if kind == 'empty' else number)
        mutation(report, accepted)
        path = work / (kind + '.json')
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            if kind == 'empty':
                empty.measure(report, inventory, accepted)
            else:
                numeric.validated(report, image, accepted)
        except (ValueError, FileNotFoundError) as error:
            if reason not in str(error):
                raise AssertionError((kind, name, 'Unexpected rejection', str(error), reason))
            rows.append({'kind': kind, 'name': name, 'rejected': True, 'reason': str(error)})
            return
        raise AssertionError('Invalid grouped source proof accepted: ' + name)

    reject('empty', 'wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('empty', 'native-VM-namespace', lambda r, b: b['nativeModuleHashes'].update(main='0' * 64), 'namespace differs')
    reject('empty', 'alias-credit', lambda r, b: r.update(memberAliasesGiveNoDuplicateCredit=False), 'alias/whole-ROM scope differs')
    reject('empty', 'whole-ROM-credit', lambda r, b: r.update(wholeRomSourceMatch=True), 'alias/whole-ROM scope differs')
    reject('empty', 'frozen-validator-change', lambda r, b: b['sourceHashes'].update(validate_scr_empty_family_20261029_batch04='0' * 64), 'closure changed')
    reject('empty', 'duplicate-unit', lambda r, b: b['units'].append(copy.deepcopy(b['units'][0])), 'range declarations differ')
    reject('empty', 'range-drift', lambda r, b: b['units'][0]['range'].update(endExclusivePc=0), 'range declarations differ')
    reject('empty', 'invented-definition-credit', lambda r, b: r.update(newAuthoredDefinitions=1109), 'Credit scope')
    reject('empty', 'invented-logic-credit', lambda r, b: r.update(newSubstantiveDecisionLogicBytes=17744), 'Credit scope')
    reject('empty', 'native-credit', lambda r, b: r.update(ordinaryNativeExecutableByteCredit=17744), 'Credit scope')
    reject('empty', 'post-fault-proof', lambda r, b: r.update(postFaultStateUsedForProof=True), 'Native proof scope')
    reject('empty', 'missing-generated-product', lambda r, b: r['sourceOnlyBuild']['generatedArtifact'].update(path='work/intentionally-absent-empty-product.json'), 'intentionally-absent-empty-product')
    module = empty_report['modules'][0]
    case, region = copy.deepcopy(module['nativeDifferentialCases'][0]), module['matchedRanges'][0]
    case['observations'][0]['actualReturn'] = False
    try:
        native_case(case, region, 1)
    except ValueError as error:
        rows.append({'kind': 'empty', 'name': 'false-native-return', 'rejected': True, 'reason': str(error)})
    else:
        raise AssertionError('Incomplete empty function received credit')
    reject('numeric', 'wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('numeric', 'whole-ROM-credit', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('numeric', 'wrong-Python', lambda r, b: r['sourceOnlyBuild'].update(pythonExecutableSha256='0' * 64), 'Python identity differs')
    reject('numeric', 'interleaved-call-claim', lambda r, b: r['sourceOnlyBuild'].update(interleavedOrReentrantSemanticsClaimed=True), 'language/runtime scope differs')
    reject('numeric', 'false-native-return', lambda r, b: r['differential']['cases'][0]['observations'][0].update(actualReturn=False), 'Actual bounded native return')
    reject('numeric', 'missing-NaN-scenario', lambda r, b: r['differential']['cases'].pop(100), 'All branch/thread/byte/NaN cases')
    reject('numeric', 'unproved-natural-producer', lambda r, b: r['differential'].update(naturalGameProducerOfContextValue60Proven=True), 'Natural reachability scope')
    reject('numeric', 'invented-source-credit', lambda r, b: r.update(ordinaryNativeExecutableByteCredit=352), 'Evidence credit scope')
    positive = empty.measure(empty_report, inventory, group)
    unit = numeric.validated(numeric_report, image, number)
    if len(positive) != 1109 or unit['sourceByteCredit'] != 352:
        raise AssertionError('Positive grouped source validation differs')
    result = {'passed': True, 'controls': rows, 'emptyInstances': len(positive),
              'emptyPhysicalBytes': sum(row['sourceByteCredit'] for row in positive),
              'numericInstances': 1, 'numericPhysicalBytes': unit['sourceByteCredit'],
              'newEmptyDefinitions': 0, 'newEmptyImplementationFamilies': 0, 'nativeByteCredit': 0, 'completeImages': 0}
    write_json(ROOT / 'evidence/verification/interpreted-bulk-source-negatives-20261029.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, len(rows))


if __name__ == '__main__':
    main()
