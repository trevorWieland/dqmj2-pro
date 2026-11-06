from copy import deepcopy
from pathlib import Path
import tempfile
from project import ROOT, read_json, write_json, sha256
from declare_utility_replay_inputs import amend


def main():
    work = ROOT / 'work/parallel-wave20261102/utility-replay-input-controls'
    work.mkdir(parents=True, exist_ok=True)
    controls = []
    with tempfile.TemporaryDirectory(dir=work) as folder:
        root = Path(folder)
        inventories = ['evidence/arm9.json', 'evidence/arm7.json']
        for name in inventories:
            write_json(root / name, dict(qualified=True))
        namespace = 'a' * 64
        provider, consumer, host = 'z-startup.json', 'a-child.json', 'b-host.json'
        documents = {provider: dict(romSha256=namespace, matches=[]),
            consumer: dict(romSha256=namespace, matches=[dict(module='utility-child-arm9-main')]),
            host: dict(romSha256=namespace, matches=[dict(module='arm7-main')])}
        for name, value in documents.items():
            write_json(root / name, value)
        registry = dict(batches=[dict(report=name, reproduce=['unchanged.py', '--same'],
            sourceHashes={'utility_code.py': 'b' * 64}) for name in documents])
        pins = dict(romSha256=namespace, startupReport=provider,
            frozenInputs=[dict(path=name, sha256=sha256(root / name)) for name in inventories])
        result, changes = amend(registry, pins, root)
        assert changes == [consumer]
        assert result['batches'][0] == registry['batches'][0]
        assert result['batches'][2] == registry['batches'][2]
        assert result['batches'][1]['replayRequires'] == [provider]
        assert result['batches'][1]['reproduce'] == registry['batches'][1]['reproduce']
        again, changes = amend(result, pins, root)
        assert again == result
        controls.append(dict(name='ordered-idempotent-child-only-source-preserving-repair', passed=True))

        def rejects(name, current, current_pins):
            try:
                amend(current, current_pins, root)
            except (ValueError, FileNotFoundError) as error:
                controls.append(dict(name=name, rejected=True, reason=str(error)))
                return
            raise AssertionError('Unsafe replay repair accepted: ' + name)

        bad = deepcopy(registry)
        bad['batches'] = bad['batches'][1:]
        rejects('missing-startup-provider', bad, pins)
        bad = deepcopy(pins)
        bad['romSha256'] = 'c' * 64
        rejects('wrong-startup-build', registry, bad)
        bad = deepcopy(pins)
        bad['frozenInputs'][0]['sha256'] = '0' * 64
        rejects('changed-inventory-content', registry, bad)
        bad = deepcopy(pins)
        bad['frozenInputs'][0]['path'] = 'missing.json'
        rejects('absent-inventory', registry, bad)
        bad = deepcopy(registry)
        bad['batches'][1]['sourceHashes'][inventories[0]] = '0' * 64
        rejects('refuse-replacing-old-inventory-identity', bad, pins)
        bad = deepcopy(registry)
        bad['batches'][1]['replayRequires'] = provider
        rejects('malformed-prerequisite-list', bad, pins)
        write_json(root / consumer, dict(documents[consumer], romSha256='c' * 64))
        rejects('wrong-consumer-build', registry, pins)
        write_json(root / consumer, documents[consumer])
        write_json(root / provider, dict(documents[provider], replayRequires=[consumer]))
        rejects('introduced-dependency-cycle', registry, pins)
    write_json(ROOT / 'evidence/verification/parallel-wave20261102/utility-replay-input-controls.json',
        dict(passed=True, sourceCredit=0, controls=controls, liveRegistryAndSourcesChanged=False))
    print(dict(passed=True, controls=len(controls)))


if __name__ == '__main__':
    main()
