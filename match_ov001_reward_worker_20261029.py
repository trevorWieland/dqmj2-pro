import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_reward_worker_fixture_20261029 import execute
from ov001_reward_worker_model_20261029 import vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCES = {
    0x021E54A0: ('src/overlays/ov001_20261029_reward_021e54a0_f6e7c5a824e7.c', True),
    0x021E5638: ('src/overlays/ov001_20261029_reward_021e5638_797ad45ac440.c', True),
    0x021E5E04: ('src/overlays/ov001_20261029_reward_021e5e04_9d34bd8fa477.c', False),
    0x021E5F88: ('src/overlays/ov001_20261029_reward_021e5f88_78a5150e4d13.c', True),
    0x021E634C: ('src/overlays/ov001_20261029_reward_021e634c_eeb1a9e2590e.c', False),
}
WORK = ROOT / 'work/ov001-reward-worker/20261029/accepted-candidates'
REPORT = ROOT / 'evidence/matches/ov001-20261029-reward-worker01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    matches = []
    for address, (source_path, speed) in SOURCES.items():
        source = ROOT / source_path
        compiler.WORK = WORK / f'{address:08x}' / 'compiler'
        records, code = compiler.compare(source, 'ov001', '2', 'off', speed)
        if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Frozen reward source no longer matches every native byte')
        entry = records[0]
        bindings = qualified_bindings(entry)
        directory = WORK / f'{address:08x}' / 'link' / entry['objectSha256']
        proof = validate(entry, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
        entry.update(save_link_snapshots.freeze_link(proof))
        native = overlay[address - 0x021D7240:address - 0x021D7240 + entry['bytes']]
        results = []
        for vector in vectors(address):
            original = execute(main, overlay, address, native, bindings, vector)
            rebuilt = execute(main, overlay, address, linked, bindings, vector)
            if original != rebuilt:
                raise ValueError('Native/source reward registers, memory or traces differ')
            results.append(original)
        entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=entry['bytes'],
                     justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle={'vectors': len(results), 'executions': len(results) * 2,
                             'actualReturnRequired': True, 'freshMachinePerExecution': True,
                             'nativeCalleesExecuted': False, 'hostCalleeStubs': True,
                             'providerContract': 'Qualified-mode return-only providers preserve all registers except R0 and perform no memory writes',
                             'independentStateTransitionCallOrderAndArgumentModel': True,
                             'wholeMappedRamAndStackCompared': True, 'instructionBound': 10000, 'results': results,
                             'limitations': ['Provider-domain caller behavior only; native external callee bodies are not executed',
                                             'No full-scene/reward/inventory/encounter reachability or game semantics certified',
                                             'Native callees can have additional register/memory/hardware effects outside these contracts',
                                             'Synthetic fixture seeds are not measured current or future game RNG state']})
        matches.append(entry)
        write_json(WORK / f'{address:08x}' / 'result.json', entry)
        print(json.dumps({'address': hex(address), 'bytes': entry['bytes'], 'executions': len(results) * 2}), flush=True)
    dependencies = [Path(__file__).name, 'ov001_reward_worker_model_20261029.py', 'ov001_reward_worker_fixture_20261029.py']
    signature = ROOT / 'src/transplants/ov001-reuse01/native_ov001_021e3564.c'
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'],
              'sourceHashes': {path: sha256(ROOT / path) for path, speed in SOURCES.values()},
              'matches': matches, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for entry in matches for row in entry['relocations']},
              'verifiedArityDependency': {'module': 'ov001', 'mode': 'arm', 'address': '0x021e3564',
                    'source': str(signature.relative_to(ROOT)), 'sourceSha256': sha256(signature),
                    'signature': 'u32(u32,u32)', 'calleeSourceCredit': 0},
              'ordinarySceneReachabilityCertified': False}
    write_json(REPORT, result)
    print(json.dumps({'functions': len(matches), 'bytes': sum(entry['bytes'] for entry in matches),
                      'executions': sum(entry['oracle']['executions'] for entry in matches),
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
