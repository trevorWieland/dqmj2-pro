import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_damage_word_wrapper_fixture_20261030 import execute, vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_damage_word_wrapper_fa27114789b9.c'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/damage-wrapper-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-damage-word-wrapper01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 64:
        raise ValueError('Frozen wrapper no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    native = overlay[0x021F0818 - 0x021D7240:0x021F0818 - 0x021D7240 + 64]
    results = []
    for vector in vectors():
        original = execute(main, overlay, native, bindings, vector)
        rebuilt = execute(main, overlay, linked, bindings, vector)
        if original != rebuilt:
            raise ValueError('Original and real-linked wrapper executions differ')
        results.append(original)
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=64,
                 justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 signature='u32(u32,u32,u32,u32,u32,u32,u32,u32)',
                 argumentWordCount=8, forwardedCoreArgumentWordCount=11,
                 forwardedCoreWords=['arg0', 'arg1', 'arg2', 'arg3', 0, 'arg4', 0, 0, 'arg5', 'arg6', 'arg7'],
                 oracle={'vectors': len(results), 'executions': 2 * len(results),
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'nativeCalleesExecuted': False, 'hostCalleeStubs': True,
                         'providerContract': 'Qualified ARM core return-only provider preserves all registers except R0 and performs no memory writes',
                         'independentElevenWordCallPacketAndCompleteFrameModel': True,
                         'wholeMappedRamAndStackCompared': True, 'instructionBound': 1000,
                         'results': results,
                         'limitations': ['Core021F0578 and downstream arithmetic/RNG do not execute here',
                                         'This proves physical argument slots and result forwarding, not every argument semantic meaning',
                                         'No whole action, cooperative-mode inherited R4 meaning, AI or scene reachability certified']})
    dependencies = [Path(__file__).name, 'ov001_damage_word_wrapper_fixture_20261030.py']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']}}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': 64, 'executions': 2 * len(results),
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
