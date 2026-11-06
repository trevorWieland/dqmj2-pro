import copy
from project import ROOT, read_json, write_json
import interpreted_primary_sources as primary
from validate_scr_primary24_20261029_batch05 import native_proof


def main():
    original = read_json(ROOT / 'evidence/matches/scripts-20261029-primary24.json')
    registry = read_json(ROOT / 'interpreted-recovery.json')
    batch = next(row for row in registry['batches'] if row.get('proofKind') == primary.KIND)
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-primary-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    rows = []

    def reject(name, mutate, reason, scope='full'):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        try:
            if scope == 'native':
                native_proof(report)
            else:
                path = work / 'candidate.json'
                write_json(path, report)
                accepted['report'] = path.relative_to(ROOT).as_posix()
                primary.validated(report, image, accepted)
        except ValueError as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            rows.append({'name': name, 'rejected': True, 'reason': str(error)})
            return
        raise AssertionError('Invalid primary decision proof accepted: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('whole-ROM-credit', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-Python', lambda r, b: r['sourceOnlyBuild'].update(pythonExecutableSha256='0' * 64), 'Python identity differs')
    reject('erased-outside-reads', lambda r, b: r['boundariesAndLocalStorage'].update(knownOutsideReads=0), 'outside-read dominance')
    reject('false-native-return', lambda r, b: r['differential']['cases'][0]['observations'][0].update(actualReturn=False), 'Actual bounded native return', 'native')
    reject('missing-NaN-input', lambda r, b: r['differential']['cases'].pop(100), 'Complete input/branch/thread population', 'native')
    reject('unproved-natural-input', lambda r, b: r['differential'].update(naturalProducerOfContextTwelveProven=True), 'Unproved natural input scope', 'native')
    reject('forged-outer-prefix-return', lambda r, b: r['differential']['outsideReaderInitializationPrefixes'][0].update(ownerRoutineTerminated=True), 'Prefix', 'native')
    reject('prefix-source-credit', lambda r, b: r['differential']['outsideReaderInitializationPrefixes'][0].update(sourceCredit=1292), 'Prefix', 'native')
    positive = next(index for index, case in enumerate(original['differential']['cases']) if case['first']['setterCalls'])
    reject('false-byte-store', lambda r, b: r['differential']['cases'][positive]['first']['targetByteWrites'][0].update(bytes=1), 'Exact32-bit', 'native')
    reject('incorrect-reentry-elision', lambda r, b: r['differential']['cases'][positive]['second'].update(setterCalls=0), 'Nested predicate outcome', 'native')
    unit = primary.validated(original, image, batch)
    result = {'passed': True, 'controls': rows, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
              'prefixSourceCredit': 0, 'nativeByteCredit': 0, 'completeImages': 0}
    write_json(ROOT / 'evidence/verification/interpreted-primary-source-negatives-20261029.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, len(rows))


if __name__ == '__main__':
    main()
