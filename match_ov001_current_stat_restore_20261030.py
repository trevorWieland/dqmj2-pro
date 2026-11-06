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

SOURCE = ROOT / 'src/overlays/ov001_20261030_current_stat_restore_14ad03143564.c'
SOURCE_SHA256 = '14ad03143564251c49276f9d403889aced95a99a5a18829ad13af7fff0dbde48'
WORK = ROOT / 'work/ov001-actor-sync/20261030/final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-current-stat-restore01.json'
ADDRESS, ACTOR, RECORD = 0x021D9D0C, machine_model.OUTPUT, 0x02330000


def short(value):
    return (value + 0x8000) % 0x10000 - 0x8000


def divide(value, denominator):
    return abs(value) // denominator * (-1 if value < 0 else 1)


def cases():
    bases = [0, 1, 100, 9999]
    modifiers = [-32768, -10000, -100, -1, 0, 1, 100, 32767]
    currents = [-32768, -1, 0, 1, 99, 100, 9999, 32767]
    for index in range(256):
        hp_base, mp_base = bases[index % 4], bases[(index // 4) % 4]
        hp_delta, mp_delta = modifiers[(index // 16) % 8], modifiers[(index * 3 + index // 8) % 8]
        hp, mp = currents[(index + index // 8) % 8], currents[(index // 8 + index // 64) % 8]
        combined_hp, combined_mp = hp_base + hp_delta, mp_base + mp_delta
        hp_out = 0 if combined_hp <= 0 else short(divide(hp * hp_base + combined_hp - 1, combined_hp))
        mp_out = 0 if combined_mp <= 0 else short(divide(mp * mp_base + combined_mp - 1, combined_mp))
        if hp_out > 0:
            hp_out = min(hp_out, hp_base)
        mp_out = min(mp_out, mp_base)
        rng = random.Random(202610300276 + index)
        actor, record = bytearray(rng.randbytes(0x440)), bytearray(rng.randbytes(0x210))
        actor[0x1EC:0x20C] = bytes(32)
        struct.pack_into('<I', actor, 0x1E8, RECORD + 4)
        struct.pack_into('<4h', actor, 0x1EC, hp_base, mp_base, hp, mp)
        struct.pack_into('<2h', actor, 0x21C, hp_delta, mp_delta)
        record[0x4A:0x8A] = bytes(64)
        yield {'ordinal': index, 'baseHpMp': [hp_base, mp_base], 'initialHpMp': [hp, mp],
               'hpMpModifiers': [hp_delta, mp_delta], 'combinedHpMpMaxima': [combined_hp, combined_mp],
               'expectedHpMp': [hp_out, mp_out], 'physicalFinalR0': mp_base << 16,
               'semanticReturnMeaningEstablished': False}, bytes(actor), bytes(record)


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_SHA256:
        raise ValueError('Pinned interpreter/Unicorn/frozen source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    extra = {name: bytes(rom.getFileByName(name)) for name in ['ItemTbl.bin', 'EquipTbl.bin']}
    blobs = assets()
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('bytes') != 276 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen current-stat restore no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 276] = linked
    results = []
    for index, (case, actor, record) in enumerate(cases()):
        memory = [(ACTOR, actor), (RECORD, record), (0x020F69E4, bytes(4))]
        for name, address, pointer in [('ItemTbl.bin', 0x02340000, 0x021C2AB4), ('EquipTbl.bin', 0x02350000, 0x021C6BF4)]:
            memory += [(address, extra[name][8:]), (pointer, struct.pack('<I', address))]
        patches = [(ACTOR + 0x1F0, struct.pack('<2h', *case['expectedHpMp']))]
        native = machine_model.execute(main, overlay, blobs, ADDRESS, [ACTOR], memory, patches,
                                       case['physicalFinalR0'], 202610309276 + index)
        source = machine_model.execute(main, bytes(rebuilt), blobs, ADDRESS, [ACTOR], memory, patches,
                                       case['physicalFinalR0'], 202610309276 + index)
        if native != source:
            raise ValueError('Original/source current-stat normalization differs')
        results.append({'case': case, **native})
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=276, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True,
                         'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True,
                         'independentSignedRatioNarrowingAndDistinctHpMpClampModel': True,
                         'physicalFinalR0ComparedWithoutSemanticReturnClaim': True,
                         'instructionBound': 100000, 'results': results})
    dependencies = ['prove_reward_return_abi_20261029.py', 'ov001_award_cases_20261029.py',
                    'ov001_award_fixture_20261029.py', 'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {SOURCE.relative_to(ROOT).as_posix(): sha256(SOURCE)},
              'assetHashes': {name: compiler.sha(value) for name, value in {**blobs, **extra}.items()},
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'nativeSymbolEntries': bindings, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Empty traits, measured item0 and bounded nonnegative base HP/MP are the supported getter context',
                  'Signed extreme current values and modifier fields are synthetic malformed components, not valid save/scene claims',
                  'Only actor current HP/MP change; this function does not serialize or write the prepared record',
                  'Void C reproduces physical R0 residue without proving a C return contract',
                  'Other traits/items, aliases, inaccessible pointers and full caller/scene reachability remain unsupported']}
    write_json(REPORT, report)
    print(json.dumps({'functions': 1, 'bytes': 276, 'executions': len(results) * 2,
                      'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
