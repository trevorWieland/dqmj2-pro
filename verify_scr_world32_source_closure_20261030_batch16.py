import copy
import json
from project import ROOT, read_json, write_json
from validate_scr_world32_source_closure_20261030_batch16 import validate


def main():
    original = read_json(ROOT / 'evidence/matches/scripts-20261030-world32-source-closure.json')
    directory = ROOT / 'work/script-source/20261030/batch16/negative-validation'
    directory.mkdir(parents=True, exist_ok=True)
    controls = []

    def reject(name, mutate, reason):
        report = copy.deepcopy(original)
        mutate(report)
        path = directory / 'candidate.json'
        write_json(path, report)
        try:
            validate(ROOT, path.relative_to(ROOT).as_posix())
        except (ValueError, AssertionError, OSError, KeyError, IndexError) as error:
            if reason not in str(error):
                raise AssertionError((name, 'Unexpected rejection', str(error), reason))
            controls.append({'name': name, 'rejected': True, 'reason': str(error)})
            print({'rejected': name}, flush=True)
            return
        raise AssertionError('Invalid source closure accepted: ' + name)

    reject('wrong-ROM', lambda r: r.update(romSha256='0' * 64), 'Current original ROM/script identity')
    reject('frozen-source-closure-tamper', lambda r: r['sourceClosure'][0].update(sha256='0' * 64), 'Frozen source-link proof identity/closure')
    reject('original-callee-used', lambda r: r['sourceLinking'].update(originalScrCalleeBodiesUsedForSevenLinks=1), 'Seven source-only links')
    reject('non-source-link', lambda r: r['sourceLinking']['derivedSourceLinkProfile']['reset_shared_flags'].update(dependencyKind='qualified-original'),
        'Seven source-only links')
    reject('changed-link-argument-ABI', lambda r: r['sourceLinking']['derivedSourceLinkProfile']['apply_saved_world_argument'].update(argumentTypes=[]),
        'Seven source-only links')
    reject('false-global-closure', lambda r: r['sourceLinking'].update(opaqueNativeOrComputedGlobalClosureProven=True), 'Seven source-only links')
    reject('missing-source-callee', lambda r: r['products'].pop(), 'Complete eight-range source closure')
    reject('truncated-source-range', lambda r: r['products'][1].update(endExclusivePc=1264), 'Current qualified reused source range')
    reject('source-input-unavailable', lambda r: r['products'][1]['inputs'].pop(), 'Exact source-only compilation input set')
    reject('source-product-unavailable', lambda r: r['products'][1]['emittedBody'].update(path=
        'work/script-source/20261030/batch16/negative-validation/missing.scrfunc'), 'missing.scrfunc')
    reject('per-product-duplicate-credit', lambda r: r['products'][1].update(newSourceRangeCredit=220), 'Current qualified reused source range')
    reject('false-root-return', lambda r: r['differential']['cases'][0]['first'].update(entry32Returned=False), 'Whole caller return')
    reject('missing-direct-call', lambda r: r['differential']['cases'][0]['first']['directScriptCalls'].pop(), 'Ordered seven calls')
    reject('global-duplicate-credit', lambda r: r.update(newSourceByteCredit=10308), 'Zero duplicate/native/full-image credit')
    reject('false-complete-image', lambda r: r.update(completeImageCredit=1), 'Zero duplicate/native/full-image credit')
    result = validate()
    result.update(passed=True, controls=controls)
    write_json(ROOT / 'evidence/verification/scr-world32-source-closure-negatives-20261030.json', result)
    print(json.dumps({key: value for key, value in result.items() if key != 'controls'}), flush=True)


if __name__ == '__main__':
    main()
