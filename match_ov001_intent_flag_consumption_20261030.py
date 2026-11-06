import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_turn_order_itcm_fixture_20261030 import execute
from ov001_intent_flag_consumption_cases_20261030 import vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_intent_flag_consumption_360af664b4c7.c'
SOURCE_HASH = '360af664b4c781edb16c4996b946662517577da0a8f84b1d5c4333ae9374c9bc'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/intent-flag-consumption-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-intent-flag-consumption01.json'
ADDRESS, TEAMS = 0x021DCBE4, (0x02236F6C, 0x022362AC)


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
    if len(rows) != 1 or not rows[0].get('exactAfterDeclaredRelocation') or rows[0]['bytes'] != 236:
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
    candidate[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 236] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin')}
    results = []
    for vector in vectors():
        original = execute(main, overlay, assets, ADDRESS, [], vector['memory'], vector['patches'],
                           vector['physicalR0'], vector['seed'], [])
        rebuilt = execute(main, bytes(candidate), assets, ADDRESS, [], vector['memory'], vector['patches'],
                          vector['physicalR0'], vector['seed'], [])
        if original != rebuilt:
            raise ValueError('Native/exact-linked actor flag machine results differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches', 'context')},
                        'context': {key: value for key, value in vector['context'].items() if key != 'memory'}, 'result': original})
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=236, justifiedAssemblyBytes=0,
               signature='void(void)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
               oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           independentUsabilityFlagMarkerConditionalNativeReselectionAndFullRamModel=True,
                           wholeMappedRamItcmStackRegistersFlagsAndTracesCompared=True, results=results,
                           physicalR0='Last visited actor: cleared flag byte when usable with bit4 set; zero otherwise. Direct semantic return is not assigned.',
                           limitations=['Actor+35D bit0x04 and intent+4 marker control the measured branch; meanings and persistence remain qualified',
                                        'All three actors on each of two native getter-selected teams are supplied components',
                                        'Reselection executes original021E8398/021E6A6C with actor+235=1, which produces action6, same side, slot0 without RNG',
                                        'Healthy scoring, inherited-register paths, scene lifecycle, save persistence and network reachability remain unproved']))
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
               compiler=dict(path=str(compiler.COMPILER.relative_to(ROOT)), sha256=sha256(compiler.COMPILER)),
               moduleInputSha256=overlay_metadata['sha256'], mainInputSha256=main_metadata['sha256'],
               itcmInputSha256=itcm_metadata['sha256'],
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in
                          ('ov001_intent_flag_consumption_cases_20261030.py', 'ov001_turn_order_itcm_fixture_20261030.py',
                           'ov001_turn_order_itcm_cases_20261030.py', 'ov001_award_fixture_20261029.py')],
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_intent_flag_consumption_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=236, actualReturns=2 * len(results))), flush=True)


if __name__ == '__main__':
    run()
