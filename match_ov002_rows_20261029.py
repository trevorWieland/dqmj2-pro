import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from ov002_rows_fixture_20261029 import ENTRY, OBJECT, execute, vectors
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov002_20261029_rows.c'
WORK = ROOT / 'work/ov002-final/rows252'
REPORT = ROOT / 'evidence/matches/ov002-20261029-rows.json'


def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, unused = measured_module('ov002')
    unused, main_code, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, found = compiler.compare(SOURCE, 'ov002', 2, 'off', True,
                                     compiler=ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p5/mwccarm.exe')
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Overlay2 row caller source does not match all252 bytes')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    native = overlay[ENTRY - 0x021D7240:ENTRY - 0x021D7240 + entry['bytes']]
    results = []
    for vector, (arguments, field) in enumerate(vectors()):
        original = execute(main_code, overlay, native, arguments, field, vector)
        rebuilt = execute(main_code, overlay, linked, arguments, field, vector)
        if original != rebuilt:
            raise ValueError('Overlay2 native/linked caller state, registers or traces differ')
        results.append(original)
    boundary_args = [OBJECT, 0, 256, 1, 1, 1, 0]
    stopped = [execute(main_code, overlay, code, boundary_args, 0, 1000, False) for code in (native, linked)]
    if stopped[0] != stopped[1]:
        raise ValueError('Overlay2 wrapping-count boundary behavior differs')
    limits = ['The two external callees have explicit return-only word-argument providers',
              'No real UI/resource/record side effects are certified by the caller fixture',
              'Counts0/1/2/6/127/128/250/255 return; count256 hits the instruction cap and receives no return credit',
              'Function return type is void; the final raw R0 word is not a caller API promise',
              'No ordinary game scene or portable-host ABI claim follows']
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=252, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'independentCompleteCallWordModel': True, 'nativeCalleesExecuted': False,
                         'hostCalleeStubs': True, 'instructionBound': 20000, 'results': results,
                         'boundedNonreturningCount256': stopped, 'nonreturningProbesReceiveReturnCredit': False,
                         'limitations': limits})
    dependencies = ['match_ov002_rows_20261029.py', 'ov002_rows_fixture_20261029.py', 'reward_state_fixture_20261029.py',
                    'match_runtime.py', 'link_runtime_unit.py', 'save_link_snapshots.py', 'recover_linked_runtime.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'module': 'ov002', 'processor': 'arm9', 'moduleInputSha256': metadata['sha256'],
              'matches': [entry], 'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False, 'limitations': limits}
    write_json(REPORT, report)
    print({'functions': 1, 'bytes': 252, 'actualReturns': len(results) * 2, 'nonreturnProbes': 2})


if __name__ == '__main__':
    main()
