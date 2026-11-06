import copy
from project import ROOT, read_json, write_json
import interpreted_entry_sources as entry


def main():
    original = read_json(ROOT / 'evidence/matches/scripts-20261029-entry129.json')
    batch = entry.candidates(original, 'evidence/matches/scripts-20261029-entry129.json',
                             ['match_scr_entry129_20261029_batch07.py'])[0]
    inventory = read_json(ROOT / 'evidence/encounter/scripts-inventory-20261029.json')
    image = next(row for row in inventory['images'] if row['codeSha256'] == batch['identity']['codeSha256'])
    work = ROOT / 'work/interpreted-entry-proof-negatives'
    work.mkdir(parents=True, exist_ok=True)
    rows = []

    def reject(name, mutate, reason):
        report, accepted = copy.deepcopy(original), copy.deepcopy(batch)
        mutate(report, accepted)
        path = work / 'candidate.json'
        write_json(path, report)
        accepted['report'] = path.relative_to(ROOT).as_posix()
        try:
            entry.validated(report, image, accepted)
        except ValueError as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            rows.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'negativeControl': name, 'rejected': True}, flush=True)
            return
        raise AssertionError('Accepted invalid whole-entry evidence: ' + name)

    reject('wrong-ROM', lambda r, b: r.update(romSha256='0' * 64), 'report identity differs')
    reject('wrong-evidence-class', lambda r, b: r.update(evidenceClass='generated-disassembly'), 'report identity differs')
    reject('whole-ROM-credit', lambda r, b: r.update(wholeRomSourceMatch=True), 'partial source claims whole ROM')
    reject('wrong-native-namespace', lambda r, b: b['nativeModuleHashes'].update(main='0' * 64), 'native VM namespace differs')
    reject('changed-synthetic-zero-prerequisite', lambda r, b: r['differential']['cases'][0]['explicitSyntheticControlHalfword'].update(value=1),
           'Explicit unknown-control synthetic0 prerequisite')
    reject('false-whole-entry-return', lambda r, b: r['differential']['cases'][0]['first'].update(completeEntry129Returned=False),
           'Whole entry return/input')
    reject('callee-source-linked-claim', lambda r, b: r['qualifiedOriginalScriptCallees'][0].update(sourceLinkedCalleeClaimed=True),
           'Qualified original zero-credit script callees')
    reject('callee-byte-credit', lambda r, b: r.update(originalScriptCalleeSourceCredit=352), 'Source scope')
    reject('omitted-thread-scenario', lambda r, b: r['differential']['cases'].pop(), 'All supported input/branch/thread/reentry scenarios')
    reject('truncated-caller-range', lambda r, b: b['range'].update(bytes=756), 'frozen complete range differs')
    reject('missing-branch-outcome', lambda r, b: r['differential']['ownBranchCoverage'].__setitem__('137476', [True]),
           'branch')
    reject('forged-general-C-support', lambda r, b: r['sourceOnlyBuild'].update(generalCCompilerClaimed=True), 'language/runtime scope differs')
    unit = entry.validated(original, image, batch)
    result = {'passed': True, 'controls': rows, 'sourceUnits': 1, 'sourceBytes': unit['sourceByteCredit'],
              'originalScriptCalleeSourceCredit': 0, 'unsupportedBoundFailureReturnCredit': 0,
              'completeImages': 0, 'nativeByteCredit': 0}
    write_json(ROOT / 'evidence/verification/interpreted-entry-source-negatives-20261030.json', result)
    print({key: value for key, value in result.items() if key != 'controls'}, flush=True)


if __name__ == '__main__':
    main()
