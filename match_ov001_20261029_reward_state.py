import json
import sys
from pathlib import Path
import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from reward_state_fixture_20261029 import ENTRY, execute, vectors
from unicorn import __version__ as unicorn_version


SOURCE = ROOT / 'src/overlays/ov001_20261029_reward_state.c'
WORK = ROOT / 'work/ov001-reward-state/20261029'
REPORT = ROOT / 'evidence/matches/ov001-20261029-reward-state.json'


def trace_callers(metadata, overlay, config):
    from trace_application_entries import functions
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
    from capstone.arm import ARM_INS_B, ARM_INS_BL, ARM_INS_BLX, ARM_OP_IMM
    callers = []
    base = int(metadata['base'], 0)
    for function in functions(config):
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if function['mode'] == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        start = function['address'] - base
        for ins in decoder.disasm(overlay[start:start + function['bytes']], function['address']):
            if ins.id in (ARM_INS_B, ARM_INS_BL, ARM_INS_BLX) and ins.operands and ins.operands[0].type == ARM_OP_IMM and ins.operands[0].imm == ENTRY:
                callers.append({'processor': 'arm9', 'module': 'ov001', 'mode': function['mode'],
                                'moduleInputSha256': metadata['sha256'], 'function': hex(function['address']),
                                'functionBytes': function['bytes'], 'callsite': hex(ins.address),
                                'mnemonic': ins.mnemonic, 'target': hex(ENTRY)})
    return callers


def main():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, config = measured_module('ov001')
    main_metadata, main_code, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, found = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Reward state C does not match its complete native function')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    native = overlay[ENTRY - 0x021D7240:ENTRY - 0x021D7240 + entry['bytes']]
    results = []
    for vector in vectors():
        original = execute(main_code, overlay, native, bindings, vector)
        rebuilt = execute(main_code, overlay, linked, bindings, vector)
        if original != rebuilt:
            raise ValueError('Native/linked reward state registers, memory or traces differ')
        results.append(original)
    limits = ['All external callees use explicit synthetic return-only provider contracts',
              'Native reward, inventory, rendering and scene bodies are not executed by this caller fixture',
              'A returning caller does not certify game-level victory, loss, travel or encounter reachability',
              'Raw context state numbers and marker bytes have no certified gameplay names',
              'Original dependency code and all interpreted scripts receive zero new source credit']
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=1520,
                 justifiedAssemblyBytes=0, nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'nativeCalleesExecuted': False, 'hostCalleeStubs': True,
                         'instructionBound': 10000, 'results': results,
                         'independentStateTransitionAndCallOrderModel': True,
                         'wholeMappedRamAndStackCompared': True, 'limitations': limits})
    dependencies = ['match_ov001_20261029_reward_state.py', 'reward_state_fixture_20261029.py',
                    'match_runtime.py', 'link_runtime_unit.py', 'save_link_snapshots.py',
                    'recover_linked_runtime.py', 'trace_application_entries.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'module': 'ov001', 'processor': 'arm9', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'incomingDirectBranches': trace_callers(metadata, overlay, config),
              'signature': 'u32(void)', 'ordinarySceneReachabilityCertified': False,
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'limitations': limits}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 1520, 'executions': len(results) * 2,
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    main()
