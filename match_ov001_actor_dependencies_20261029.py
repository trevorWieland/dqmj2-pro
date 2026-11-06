import json
import random
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import prove_reward_return_abi_20261029 as machine_model
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_award_cases_20261029 import assets
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCES = {
    0x021D9E20: ('src/overlays/ov001_20261029_actor_priority_sort_68c144cb901f.c',
                 '68c144cb901f2b974a4b3eb5259f3adb10df80bc3e8d511bb978105ba9aaab01', 124),
    0x021D9E9C: ('src/overlays/ov001_20261029_actor_stat_copy_4df01600e56f.c',
                 '4df01600e56f08c60a351987964b71cbce9fb01567146a5a3c3c2b3c1a63b4c7', 212),
}
WORK = ROOT / 'work/ov001-actor-dependencies/20261029/final'
REPORT = ROOT / 'evidence/matches/ov001-20261029-actor-dependencies01.json'
OUTPUT, INPUT, TABLE = machine_model.OUTPUT, 0x02330000, 0x02340000


def cases(address, actions):
    if address == 0x021D9E20:
        counts = [-2147483648, -1, 0, 1, 2, 3, 7, 12, 24, 32]
        for index in range(100):
            rng = random.Random(202610309920 + index)
            count = counts[index % len(counts)]
            original = list(rng.randbytes(32))
            if index % 3 == 0:
                original = [[0, 1, 7, 31, 32, 127, 128, 255][value % 8] for value in original]
            if index % 5 == 0:
                original.sort(key=lambda value: actions[value * 40 + 36], reverse=True)
            output, swaps = original[:], 0
            for first in range(max(0, count)):
                for second in range(first + 1, count):
                    if actions[output[first] * 40 + 36] > actions[output[second] * 40 + 36]:
                        output[first], output[second] = output[second], output[first]
                        swaps += 1
            length = max(0, count)
            if sorted(original[:length]) != sorted(output[:length]) or any(actions[output[i] * 40 + 36] > actions[output[i + 1] * 40 + 36] for i in range(max(0, length - 1))):
                raise ValueError('Independent sort model violated permutation/priority invariants')
            memory = [(OUTPUT, bytes(original)), (TABLE, actions), (0x021C6748, struct.pack('<I', TABLE))]
            patches = [(OUTPUT, bytes(output))]
            yield {'ordinal': index, 'count': count, 'initialIndices': original, 'finalIndices': output,
                   'expectedSwapCount': swaps, 'permutationAndNondecreasingPrioritiesChecked': True}, [OUTPUT, count], memory, patches, swaps
    else:
        values = [-32768, -1, 0, 1, 9998, 9999, 10000, 32767]
        for index in range(72):
            rng = random.Random(202610309996 + index)
            actor, record = bytearray(rng.randbytes(0x440)), bytearray(rng.randbytes(0x200))
            initial = [values[(index + number) % len(values)] for number in range(16)]
            source = struct.pack('<16h', *initial)
            exact_alias = index % 9 == 0
            input_address = OUTPUT + 0xD0 if exact_alias else INPUT
            if exact_alias:
                actor[0x1EC:0x20C] = source
                memory = [(OUTPUT, bytes(actor))]
            else:
                record[0x11C:0x13C] = source
                memory = [(OUTPUT, bytes(actor)), (INPUT, bytes(record))]
            final = initial[:]
            for number in [0, 1, 2, 4, 5, 6, 7]:
                final[number] = min(final[number], 9999)
            yield {'ordinal': index, 'initialSixteenHalfwords': initial, 'finalSixteenHalfwords': final,
                   'exactStatBlockAlias': exact_alias, 'semanticReturnMeaningEstablished': False}, [OUTPUT, input_address], memory, [(OUTPUT + 0x1EC, struct.pack('<16h', *final))], OUTPUT + 0x100


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    action_asset = bytes(rom.getFileByName('ActTbl.bin'))
    actions, blobs = action_asset[8:], assets()
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    matches = []
    for address, (relative, expected_hash, size) in SOURCES.items():
        source = ROOT / relative
        if sha256(source) != expected_hash:
            raise ValueError('Frozen actor dependency source changed')
        compiler.WORK = WORK / f'{address:08x}' / 'compiler'
        records, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(records) != 1 or records[0].get('bytes') != size or not records[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Frozen actor dependency no longer matches every native byte')
        entry = records[0]
        bindings = qualified_bindings(entry)
        directory = WORK / f'{address:08x}' / 'link' / entry['objectSha256']
        proof = validate(entry, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
        entry.update(save_link_snapshots.freeze_link(proof))
        rebuilt = bytearray(overlay)
        rebuilt[address - 0x021D7240:address - 0x021D7240 + size] = linked
        results = []
        for index, (case, arguments, memory, patches, expected) in enumerate(cases(address, actions)):
            native = machine_model.execute(main, overlay, blobs, address, arguments, memory, patches, expected, 202610310000 + address + index)
            source_result = machine_model.execute(main, bytes(rebuilt), blobs, address, arguments, memory, patches, expected, 202610310000 + address + index)
            if native != source_result:
                raise ValueError('Native/source actor dependency state differs')
            results.append({'case': case, **native})
        entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
                     nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle={'vectors': len(results), 'executions': len(results) * 2,
                             'actualReturnRequired': True, 'freshMachinePerExecution': True,
                             'wholeMappedRamAndStackAndRegistersCompared': True,
                             'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True,
                             'independentPrioritySwapModel': address == 0x021D9E20,
                             'independentBlockCopyAndSignedUpperCaps': address == 0x021D9E9C,
                             'instructionBound': 100000, 'results': results})
        matches.append(entry)
    dependencies = ['prove_reward_return_abi_20261029.py', 'ov001_award_cases_20261029.py',
                    'ov001_award_fixture_20261029.py', 'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': matches,
              'sourceHashes': {row[0]: row[1] for row in SOURCES.values()},
              'assetHashes': {**{name: compiler.sha(value) for name, value in blobs.items()}, 'ActTbl.bin': compiler.sha(action_asset)},
              'nativeSymbols': {row['symbol']: row['target'] for entry in matches for row in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Sort counts are signed and bounded at32; nonpositive counts skip reads/writes',
                  'Sort uses a measured accessible table; arbitrary aliases and inaccessible pointers remain unsupported',
                  'Stat block pointers are word-aligned; disjoint and exact-stat-block aliases are tested, partial overlaps remain unsupported',
                  'Void stat-copy C preserves measured R0 residue without asserting pointer-return meaning',
                  'The source-only functions and connected actor caller have separate credit; synthetic components do not establish scene reachability']}
    write_json(REPORT, result)
    print(json.dumps({'functions': 2, 'bytes': sum(x['bytes'] for x in matches),
                      'executions': sum(x['oracle']['executions'] for x in matches),
                      'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
