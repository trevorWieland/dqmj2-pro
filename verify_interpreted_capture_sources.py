import copy
from project import ROOT, read_json, write_json
import interpreted_capture_sources as captures


def main():
    original = read_json(ROOT / 'evidence/matches/scripts-20261029-captures.json')
    batch = captures.candidates(original, 'evidence/matches/scripts-20261029-captures.json',
                                ['match_scr_captures_20261029_batch06.py'])[0]
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    work = ROOT / 'work/interpreted-capture-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    rows = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            captures.measure(report, inventory, accepted)
        except ValueError as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            rows.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'negativeControl': name, 'rejected': True}, flush=True)
            return
        raise AssertionError('Accepted invalid capture evidence: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('whole-ROM-credit', lambda r, b: r.update(wholeRomSourceMatch=True), 'held-unit/logic/whole-ROM scope')
    reject('held-live-in-credit', lambda r, b: r.update(heldUnitSourceCredit=128), 'held-unit/logic/whole-ROM scope')
    reject('duplicate-range-declaration', lambda r, b: b['units'].append(copy.deepcopy(b['units'][0])), 'declarations differ')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(main='0' * 64), 'native VM namespace differs')
    reject('inflated-authored-definitions', lambda r, b: r.update(newAuthoredDefinitions=115), 'Copy-only family/ABI scope')
    reject('erased-held-unit', lambda r, b: r['heldUnits'].clear(), 'No held-unit credit')
    reject('false-native-return', lambda r, b: r['modules'][0]['matchedRanges'][0]['nativeCases'][0]['observations'][0].update(actualReturn=False),
           'Actual bounded native return')
    reject('missing-NaN-profile', lambda r, b: r['modules'][0]['matchedRanges'][0]['nativeCases'][0]['rawContextWords'].__setitem__(0, 0),
           'Raw binary32')
    reject('lost-other-slot-preservation', lambda r, b: r['modules'][0]['matchedRanges'][0]['nativeCases'][0].update(otherSlotsAndConditionPreserved=False),
           'Fixed-slot output and complete-return scope')
    reject('erased-current-reference-audit', lambda r, b: r['currentOutsideReferenceAudit'].update(instances=[]),
           'Current full reference/dominance inventory')
    reject('missing-native-profile', lambda r, b: r['modules'][0]['matchedRanges'][0]['nativeCases'].pop(),
           'All four threads/three profiles')
    reject('false-noncopy-credit', lambda r, b: r.update(newSubstantiveDecisionLogicBytes=7368),
           'Copy-only credit scope')
    reject('false-complete-image', lambda r, b: r['modules'][0].update(wholeImageReconstructed=True), 'Per-image source scope')
    units = captures.measure(original, inventory, batch)
    result = {'passed': True, 'controls': rows, 'sourceUnits': len(units),
              'sourceBytes': sum(unit['sourceByteCredit'] for unit in units),
              'copyOnlyUnits': sum(unit['copyOnly'] for unit in units),
              'sourceDefinitions': len({unit['sourceDefinitionId'] for unit in units}),
              'decisionLogicByteCredit': 0, 'heldUnitCredit': 0, 'completeImages': 0, 'nativeByteCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-capture-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
