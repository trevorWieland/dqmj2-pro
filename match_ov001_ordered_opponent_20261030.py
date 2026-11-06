import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_ordered_opponent_cases_20261030 import ADDRESS, vectors
from ov001_turn_order_itcm_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_ordered_opponent_preparation_d70a4cdc31e7.c'
SOURCE_HASH = 'd70a4cdc31e7cc28fdf2745ea12e015c9a61c0f720452e3546cf9cc81561c198'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/ordered-opponent-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-ordered-opponent01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    if sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen ordered opponent source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private ROM input changed')
    compiler.WORK = WORK / 'compiler'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or not rows[0].get('exactAfterDeclaredRelocation') or rows[0]['bytes'] != 280:
        raise ValueError('Frozen ordered opponent source no longer matches every native byte')
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
    candidate[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 280] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin')}
    if assets['ActTbl.bin'][8 + 6 * 40 + 38] != 0:
        raise ValueError('Native reset action6 priority differs from independent class0 recipe')
    results = []
    for vector in vectors(assets['ActTbl.bin'][8:], overlay):
        original = execute(main, overlay, assets, ADDRESS, [], vector['memory'], vector['patches'],
                           vector['own'] + vector['opposing'], vector['seed'], vector['draws'])
        rebuilt = execute(main, bytes(candidate), assets, ADDRESS, [], vector['memory'], vector['patches'],
                          vector['own'] + vector['opposing'], vector['seed'], vector['draws'])
        if original != rebuilt:
            raise ValueError('Native/exact-linked ordered opponent machine results differ')
        recipe = {key: value for key, value in vector.items() if key not in ('memory', 'patches', 'context')}
        recipe['context'] = {key: value for key, value in vector['context'].items() if key != 'memory'}
        results.append({**recipe, 'result': original})
        if len(results) % 240 == 0:
            print('returning vectors', len(results), flush=True)
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=280, justifiedAssemblyBytes=0,
               signature='u32(void)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
               oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                           wholeMappedRamItcmStackRegistersFlagsAndTracesCompared=True,
                           independentResetFlagOrderUsabilitySelectionAndIntentModel=True, results=results,
                           limitations=['Raw constructor/actor/scene components are supplied; whole-scene reachability remains unproved',
                                        'Opponent preparation uses native gate3 fallback; active gate0 chooser default/R6 remains outside this proof',
                                        'Counts0..3 per side and five mode/selector contexts are bounded',
                                        'All native dependencies execute original code and receive no duplicate source credit']))
    dependencies = ['ov001_ordered_opponent_cases_20261030.py', 'ov001_turn_order_itcm_fixture_20261030.py',
                    'ov001_turn_order_itcm_cases_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
               compiler=dict(path=str(compiler.COMPILER.relative_to(ROOT)), sha256=sha256(compiler.COMPILER)),
               moduleInputSha256=overlay_metadata['sha256'], mainInputSha256=main_metadata['sha256'],
               itcmInputSha256=itcm_metadata['sha256'], assetHashes={name: compiler.sha(raw) for name, raw in assets.items()},
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_ordered_opponent_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=280,
                          actualReturns=2 * len(results))), flush=True)


if __name__ == '__main__':
    run()
