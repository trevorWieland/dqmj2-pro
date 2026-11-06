import json
import re
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from related_state_fixture_20261029 import execute, vectors
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-related-states/20261029'
REPORT = ROOT / 'evidence/matches/ov001-20261029-related-states.json'
SOURCES = [('selector', 'src/overlays/ov001_20261029_entry_selector.c'),
           ('exit', 'src/overlays/ov001_20261029_exit_state.c')]


def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main_code, unused = measured_module('main')
    matches = []
    limits = ['Every external call uses a declared synthetic return-only provider',
              'UI, reward, inventory, currency and scene dependencies are not executed natively',
              'Raw state numbers, context fields and selector reasons have no new gameplay names',
              'The fixture amount domain is 0/1/300/65535 and excludes signed-negation overflow',
              'Exact caller bytes and synthetic transitions do not certify ordinary scene reachability']
    for kind, relative in SOURCES:
        source = ROOT / relative
        arities = {}
        for name, arguments in re.findall(r'extern u32 (\w+)\(([^()]*)\);', source.read_text()):
            arities[name] = 0 if arguments.strip() in ('void', '') else len(arguments.split(','))
        compiler.WORK = WORK / kind / 'compiler'
        records, found = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Related state source does not match its entire native function')
        entry = records[0]
        bindings = qualified_bindings(entry)
        directory = WORK / kind / 'link' / entry['objectSha256']
        proof = validate(entry, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / kind / 'link-artifacts'
        entry.update(save_link_snapshots.freeze_link(proof))
        address = int(entry['address'], 0)
        native = overlay[address - 0x021D7240:address - 0x021D7240 + entry['bytes']]
        results = []
        for vector in vectors(kind):
            original = execute(kind, main_code, overlay, native, entry, bindings, arities, vector)
            rebuilt = execute(kind, main_code, overlay, linked, entry, bindings, arities, vector)
            if original != rebuilt:
                raise ValueError('Related state native/recompiled registers, memory or traces differ')
            results.append(original)
        entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=entry['bytes'],
                     justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle={'vectors': len(results), 'executions': len(results) * 2,
                             'actualReturnRequired': True, 'freshMachinePerExecution': True,
                             'nativeCalleesExecuted': False, 'hostCalleeStubs': True,
                             'independentStateTransitionAndCallArgumentModel': True,
                             'fifthStackArgumentCompared': kind == 'selector',
                             'wholeMappedRamAndStackCompared': True,
                             'instructionBound': 10000, 'results': results, 'limitations': limits})
        matches.append(entry)
    dependencies = ['match_ov001_20261029_related_states.py', 'related_state_fixture_20261029.py',
                    'reward_state_fixture_20261029.py', 'match_runtime.py', 'link_runtime_unit.py',
                    'save_link_snapshots.py', 'recover_linked_runtime.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'module': 'ov001', 'processor': 'arm9', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': matches,
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {rel['symbol']: rel['target'] for row in matches for rel in row['relocations']},
              'limitations': limits}
    write_json(REPORT, report)
    print(json.dumps({'functions': len(matches), 'bytes': sum(row['bytes'] for row in matches),
                      'executions': sum(row['oracle']['executions'] for row in matches)}))


if __name__ == '__main__':
    main()
