import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_multi_action_fixture_20261030 import execute
from ov001_multi_action_model_20261030 import vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_multi_action_scheduler_8cbdd006c5b8.c'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/multi-action-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-multi-action-scheduler01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 1364:
        raise ValueError('Frozen multi-target scheduler no longer matches all native bytes')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    native = overlay[0x021EC6C0 - 0x021D7240:0x021EC6C0 - 0x021D7240 + 1364]
    results = []
    for vector in vectors():
        original = execute(main, overlay, native, bindings, vector)
        rebuilt = execute(main, overlay, linked, bindings, vector)
        if original != rebuilt:
            raise ValueError('Native and real-linked multi-target scheduling executions differ')
        results.append(original)
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=1364,
                 justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 signature='u32(void)', measuredPhysicalReturn=0,
                 oracle={'vectors': len(results), 'executions': 2 * len(results),
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'nativeCalleesExecuted': False, 'hostCalleeStubs': True,
                         'providerContract': 'Qualified-mode return-only providers preserve all registers except R0 and perform no memory writes',
                         'independentStateMemoryCallOrderAndConsumedArgumentsModel': True,
                         'wholeMappedRamAndStackCompared': True, 'instructionBound': 10000,
                         'initialStates': sorted({row['initialState'] for row in results}),
                         'finalStates': sorted({row['finalState'] for row in results}),
                         'results': results,
                         'limitations': ['Caller/provider-domain multi-target action scheduling only; external bodies are not executed',
                                         'Executor021EC03C, arithmetic, RNG, status, camera and rendering bodies are explicit providers',
                                         'Synthetic actor, descriptor, animation and state inputs are not measured current scene values',
                                         'Native callees may have additional register, memory, hardware or scheduling effects',
                                         'No complete battle, general AI decision process, encounter access or current/future RNG certified']})
    dependencies = [Path(__file__).name, 'ov001_multi_action_model_20261030.py', 'ov001_multi_action_fixture_20261030.py']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'ordinaryCallerStaticGate': {'module': 'ov001', 'mode': 'arm', 'address': '0x021ee410',
                    'bytes': 304, 'selector': 'u8(02238D7C+13)==8',
                    'directCallSite': '0x021ee4bc', 'executedHere': False}}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': 1364, 'executions': 2 * len(results),
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
