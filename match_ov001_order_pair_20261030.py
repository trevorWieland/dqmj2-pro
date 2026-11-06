import json
import random
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from project import ROOT, configuration, now, sha256, write_json
from prove_reward_return_abi_20261029 import execute
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_order_pair_82579b501d26.c'
SOURCE_HASH = '82579b501d266ee2d268531cf25c66766928d2febaffdd1d28e24fdbd89d7448'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/order-pair-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-order-pair01.json'
ADDRESS, TABLE, OUTPUT = 0x021E8178, 0x02238D40, 0x02379000


def vectors():
    result = []
    for index in range(6):
        for side, slot in ((0, 0), (1, 2), (127, 128), (128, 127), (255, 255), (255, 0), (0, 255), (2, 1)):
            base = TABLE + index * 4
            layouts = [(0, 0), (OUTPUT, 0), (0, OUTPUT + 1), (OUTPUT, OUTPUT + 1),
                       (OUTPUT, OUTPUT), (base + 1, OUTPUT + 1), (OUTPUT, base),
                       (base + 1, base), (base, base + 1)]
            for side_out, slot_out in layouts:
                seed = 1280000 + len(result)
                rng = random.Random(seed)
                data = bytearray(rng.randbytes(24))
                output = bytearray(rng.randbytes(2))
                data[index * 4:index * 4 + 2] = bytes([side, slot])
                memory = [(TABLE, bytes(data)), (OUTPUT, bytes(output))]
                for pointer, offset in ((side_out, index * 4), (slot_out, index * 4 + 1)):
                    if pointer:
                        value = data[offset]
                        if TABLE <= pointer < TABLE + 24:
                            data[pointer - TABLE] = value
                        else:
                            output[pointer - OUTPUT] = value
                patches = []
                for pointer in {side_out, slot_out} - {0}:
                    value = data[pointer - TABLE] if TABLE <= pointer < TABLE + 24 else output[pointer - OUTPUT]
                    patches.append((pointer, bytes([value])))
                expected = data[index * 4] | data[index * 4 + 1] << 8
                result.append({'seed': seed, 'index': index, 'rawSide': side, 'rawSlot': slot,
                               'arguments': [index, side_out, slot_out], 'memory': memory,
                               'patches': patches, 'returnWord': expected})
    return result


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    if sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen order-pair source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM identity differs')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin')}
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != 88:
        raise ValueError('Frozen order-pair getter no longer matches all native bytes')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 88] = linked
    results = []
    for vector in vectors():
        arguments = vector['arguments']
        original = execute(main, overlay, assets, ADDRESS, arguments, vector['memory'], vector['patches'], vector['returnWord'], vector['seed'])
        candidate = execute(main, bytes(rebuilt), assets, ADDRESS, arguments, vector['memory'], vector['patches'], vector['returnWord'], vector['seed'])
        if original != candidate:
            raise ValueError('Original native versus linked order-pair behavior differs')
        results.append({'seed': vector['seed'], 'index': vector['index'], 'rawSide': vector['rawSide'],
                        'rawSlot': vector['rawSlot'], **original})
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=88, justifiedAssemblyBytes=0,
                 signature='u32(u32,s8*,s8*)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': 2 * len(results),
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'hostCalleeStubs': False, 'nativeCallees': 0,
                         'independentSequentialSignedByteStoreAliasingAndPacked16Model': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True, 'instructionBound': 100000,
                         'returnRepresentation': 'R0 zero-extended16-bit word: final raw side byte | final raw slot byte<<8',
                         'sourceDataCredit': 0, 'results': results,
                         'limitations': ['Index0..5 and supplied24-byte runtime order table are the supported component domain',
                                         'Raw high-bit side/slot rows measure representation and aliases rather than legal game positions',
                                         'Null, separate, identical and source-field-alias output pointers are bounded mapped cases; arbitrary invalid pointers remain unsupported',
                                         'The two other row bytes are preserved and semantically unknown',
                                         'Table production/order/lifecycle and whole-scene reachability remain unproved']})
    dependencies = [Path(__file__).name, 'prove_reward_return_abi_20261029.py', 'ov001_award_fixture_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {str(SOURCE.relative_to(ROOT)): sha256(SOURCE)},
              'runtimeDataLayout': {'address': hex(TABLE), 'records': 6, 'stride': 4,
                                    'sideOffset': 0, 'slotOffset': 1, 'unknownOffsets': [2, 3], 'sourceDataCredit': 0},
              'assetHashes': {name: compiler.sha(raw) for name, raw in assets.items()},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']}}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 88, 'executions': entry['oracle']['executions'],
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
