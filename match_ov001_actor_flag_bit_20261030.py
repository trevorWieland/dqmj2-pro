import json
import random
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_turn_order_itcm_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_actor_flag_bit_d1b5d1e2ca3a.c'
SOURCE_HASH = 'd1b5d1e2ca3aff5ae0f7995e7279abd2de26bacea7598b58565a7beb218f5f81'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/actor-flag-bit-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-actor-flag-bit01.json'
ADDRESS, TEAMS = 0x021DCCD0, (0x02236F6C, 0x022362AC)


def vectors():
    result = []
    for word in (0, 1, 2, 3, 4, 127, 128, 255, 256, 257, 0x80000000, 0x80000001, 0xFFFFFFFF):
        for variant in range(8):
            seed = 1350000 + len(result)
            randomizer = random.Random(seed)
            memory, patches, flags = [], [], []
            for side, base in enumerate(TEAMS):
                for slot in range(3):
                    actor = bytearray(randomizer.randbytes(1088))
                    before = (0, 4, 251, 255, 85, 170, 1, 128)[(variant + side * 3 + slot) % 8]
                    actor[0x35D] = before
                    after = before & ~4 | (word & 1) << 2
                    memory.append((base + slot * 1088, bytes(actor)))
                    patches.append((base + slot * 1088 + 0x35D, bytes([after])))
                    flags.append(dict(side=side, slot=slot, before=before, after=after))
            result.append(dict(seed=seed, word=word, variant=variant, memory=memory, patches=patches, flags=flags))
    return result


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    if sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen actor flag source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private ROM input changed')
    compiler.WORK = WORK / 'compiler'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or not rows[0].get('exactAfterDeclaredRelocation') or rows[0]['bytes'] != 104:
        raise ValueError('Frozen flag helper no longer matches every native byte')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-link-artifacts'
    row.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    overlay_metadata, overlay, unused = measured_module('ov001')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate = bytearray(overlay)
    candidate[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 104] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin')}
    results = []
    for vector in vectors():
        original = execute(main, overlay, assets, ADDRESS, [vector['word']], vector['memory'], vector['patches'],
                           TEAMS[1] + 3 * 1088, vector['seed'], [])
        rebuilt = execute(main, bytes(candidate), assets, ADDRESS, [vector['word']], vector['memory'], vector['patches'],
                          TEAMS[1] + 3 * 1088, vector['seed'], [])
        if original != rebuilt:
            raise ValueError('Native/exact-linked actor flag machine results differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=104, justifiedAssemblyBytes=0,
               signature='void(u32)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
               oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           independentLowBitFlagByteAndUntouchedActorModel=True,
                           wholeMappedRamItcmStackRegistersFlagsAndTracesCompared=True, results=results,
                           physicalR0='Base of side1 actor array plus3*1088; void semantic return is not inferred',
                           limitations=['Only bit0x04 of actor+35D is interpreted; other bits and actor bytes remain opaque',
                                        'All three actors on each of two native getter-selected teams are supplied components',
                                        'No scene lifecycle, save persistence or network semantics is established']))
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
               compiler=dict(path=str(compiler.COMPILER.relative_to(ROOT)), sha256=sha256(compiler.COMPILER)),
               moduleInputSha256=overlay_metadata['sha256'], mainInputSha256=main_metadata['sha256'],
               itcmInputSha256=itcm_metadata['sha256'],
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in
                          ('ov001_turn_order_itcm_fixture_20261030.py', 'ov001_award_fixture_20261029.py')],
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_actor_flag_bit_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=104, actualReturns=2 * len(results))), flush=True)


if __name__ == '__main__':
    run()
