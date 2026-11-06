from copy import deepcopy
from pathlib import Path
import json
import declare_utility_replay_inputs as repair
from project import ROOT, read_json, sha256, write_json


def main():
    registry = ROOT / 'recovery.json'
    before = sha256(registry)
    old = read_json(registry)
    untouched = deepcopy(old)
    pins = read_json(ROOT / 'provenance/parallel-wave20261102-utility-replay-inputs.json')
    new, consumers = repair.amend(old, pins)
    assert old == untouched and sha256(registry) == before
    repeated, again = repair.amend(new, pins)
    assert repeated == new and consumers == again
    assert {k: v for k, v in old.items() if k != 'batches'} == {k: v for k, v in new.items() if k != 'batches'}
    for earlier, later in zip(old['batches'], new['batches']):
        if earlier['report'] not in consumers:
            assert earlier == later
            continue
        assert {k: v for k, v in earlier.items() if k not in ['sourceHashes', 'replayRequires']} == {k: v for k, v in later.items() if k not in ['sourceHashes', 'replayRequires']}
        assert all(later['sourceHashes'][name] == digest for name, digest in earlier['sourceHashes'].items())
        assert all(later['sourceHashes'][pin['path']] == pin['sha256'] for pin in pins['frozenInputs'])
        assert later['replayRequires'] == list(dict.fromkeys([*earlier.get('replayRequires', []), pins['startupReport']]))
    controls = read_json(ROOT / 'evidence/verification/parallel-wave20261102/utility-replay-input-controls.json')
    config = read_json(ROOT / 'provenance/parallel-wave20261102-next-packets.json')
    spec = read_json(ROOT / 'cohort149-parallel-wave20261102-next-specification.json')
    assert spec['postSealCommands'] == config['postSealCommands']
    descriptor = read_json(ROOT / 'provenance/cohort149-parallel-wave20261102-next-utility-child-third-0-replay.json')
    frozen = {row['path']: row['sha256'] for row in descriptor['frozenInputs']}
    assert all(frozen[row['path']] == row['sha256'] == sha256(ROOT / row['path']) for row in pins['frozenInputs'])
    child = [row for row in spec['expectedAdditions'] if row['module'] == 'utility-child-arm9-main']
    assert len(child) == 36 and all(row['processor'] == 'arm9' and row['program'] == 'dwc/utility.bin/move/child.srl' for row in child)
    assert sha256(registry) == before
    result = dict(passed=True, scope='Read-only independent in-memory metadata repair audit', sourceCredit=0,
        sourceRegistrySha256=before, liveRegistryUnchanged=True, callerInputObjectUnchanged=True,
        idempotent=True, nonconsumerBatchesAndAllOriginalSourceObjectProducerContractsPreserved=True,
        currentConsumers=consumers, currentConsumerCount=len(consumers), childThirdFullNamespacePreserved=True,
        rootDescriptorMandatoryInventoryPins=True, frozenWorkerHelpersModified=False,
        repairGeneratorSha256=sha256(ROOT / 'declare_utility_replay_inputs.py'),
        suppliedControlReceiptSha256=sha256(ROOT / 'evidence/verification/parallel-wave20261102/utility-replay-input-controls.json'),
        suppliedControls=controls, generatorSha256=sha256(Path(__file__)),
        fullFreshReplayProven=False, sourceOnlyRomProven=False)
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/utility-replay-metadata-audit.json', result)
    print(json.dumps({k: v for k, v in result.items() if k != 'suppliedControls'}, indent=2))


if __name__ == '__main__':
    main()
