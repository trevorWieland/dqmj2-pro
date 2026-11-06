import copy
from project import ROOT, read_json, sha256, write_json
from arm7_state import runtime_state
from discontiguous_boundaries_20261030 import reconcile


def main():
    path = 'evidence/attempts/arm7-seq-main-boundary-amendment-proposal-20261030.json'
    policy = read_json(ROOT / path)
    modules, candidates, layout = runtime_state()
    registry_hash = sha256(ROOT / 'recovery.json')
    inventory_hash = sha256(ROOT / 'evidence/arm7/runtime-functions.json')
    positive = reconcile(candidates, modules, [(path, policy)])
    assert len(positive) == len(candidates)
    changes = [(a, b) for a, b in zip(candidates, positive) if a != b]
    assert len(changes) == 1 and changes[0][1]['size'] == 352
    assert changes[0][1]['instructionBodyBytes'] == 344 and changes[0][1]['generatedLiteralBytes'] == 8
    assert reconcile(candidates, modules, []) == candidates
    controls = []

    def reject(label, mutate):
        p, c, m = copy.deepcopy(policy), copy.deepcopy(candidates), copy.deepcopy(modules)
        mutate(p, c, m)
        try:
            reconcile(c, m, [(path, p)])
        except ValueError as error:
            controls.append({'control': label, 'rejected': True, 'reason': str(error)})
        else:
            raise AssertionError('UnreviewedBoundaryAccepted:' + label)

    reject('processor', lambda p, c, m: p.update(processor='arm9'))
    reject('program', lambda p, c, m: p.update(program='child'))
    reject('module', lambda p, c, m: p.update(module='arm7-main'))
    reject('mode', lambda p, c, m: p.update(mode='thumb'))
    reject('span', lambda p, c, m: p.update(bytes=348))
    reject('literal-accounting', lambda p, c, m: p.update(codeBytes=340, literalBytes=12))
    reject('invented-module-bytes', lambda p, c, m: p.update(additionalInitializedModuleBytes=64))
    reject('module-hash', lambda p, c, m: p.update(inputModuleSha256='0' * 64))
    reject('span-hash', lambda p, c, m: p.update(inputBytesSha256='0' * 64))
    reject('review-not-passed', lambda p, c, m: p.update(coordinatorReviewPassed=False))
    reject('proof-hash', lambda p, c, m: p['reviewEvidence'][2].update(sha256='0' * 64))
    reject('raw-inventory-hash', lambda p, c, m: p['originalRawInventory'].update(sha256='0' * 64))
    reject('prior-candidate-shape', lambda p, c, m: p['originalCandidate'].update(instructionBodyBytes=344))
    reject('duplicate-original-root', lambda p, c, m: c.append(copy.deepcopy(p['originalCandidate'])))
    reject('new-interior-root', lambda p, c, m: c.append(dict(p['originalCandidate'], address='0x03800004')))
    assert sha256(ROOT / 'recovery.json') == registry_hash
    assert sha256(ROOT / 'evidence/arm7/runtime-functions.json') == inventory_hash
    result = {'status': 'passed', 'positiveCandidateChanges': 1, 'candidateCountUnchanged': True,
              'controls': len(controls), 'results': controls, 'sourceCredit': 0, 'activeInventoryChanged': False,
              'sourceRegistryChanged': False, 'globalConsumerAbsenceClaim': False,
              'proposal': {'path': path, 'sha256': sha256(ROOT / path)},
              'generatorSources': [{'path': name, 'sha256': sha256(ROOT / name)} for name in
                  ['verify_discontiguous_boundaries_20261030.py', 'discontiguous_boundaries_20261030.py']]}
    destination = ROOT / 'evidence/verification/arm7-discontiguous-amendment-controls-20261030.json'
    write_json(destination, result)
    print({'controls': len(controls), 'allRejected': True, 'activeInventoryChanged': False, 'sourceCredit': 0})


if __name__ == '__main__':
    main()
