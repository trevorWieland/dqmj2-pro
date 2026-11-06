import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_action_retry_fixture_20261030 import TABLES
from ov001_intent_preparation_cases_20261030 import ADDRESS, vectors
from ov001_turn_order_itcm_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_intent_preparation_065d22e7827f.c'
SOURCE_HASH = '065d22e7827f7f87809a0025df97fc9cc585877a00c571ce0bb5f1aa6d723423'
WORK = ROOT / 'work/ov001-command-scheduling/20261030/intent-preparation-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-intent-preparation01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    if sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen intent preparation source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private ROM input changed')
    compiler.WORK = WORK / 'compiler'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or not rows[0].get('exactAfterDeclaredRelocation') or rows[0]['bytes'] != 380:
        raise ValueError('Frozen intent preparation no longer matches every native byte')
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
    candidate[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 380] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    names = {name for name, address, pointer in TABLES} | {'AbilityTbl.bin'}
    assets = {name: bytes(rom.getFileByName(name)) for name in names}
    table_memory = []
    for name, address, pointer in TABLES:
        table_memory += [(address, assets[name][8:]), (pointer, address.to_bytes(4, 'little'))]
    results = []
    for vector in vectors():
        memory = table_memory + vector['memory']
        draws = list(zip(vector['limits'], vector['draws']))
        original = execute(main, overlay, assets, ADDRESS, vector['arguments'], memory, vector['patches'],
                           vector['physicalR0'], vector['seed'], draws)
        rebuilt = execute(main, bytes(candidate), assets, ADDRESS, vector['arguments'], memory, vector['patches'],
                          vector['physicalR0'], vector['seed'], draws)
        if original != rebuilt:
            raise ValueError('Native/exact-linked intent preparation machine results differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')},
                        'result': original})
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=380, justifiedAssemblyBytes=0,
               signature='void(s32,void*,void*,u32 ignored)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
               oracle=dict(vectors=len(results), executions=len(results) * 2, actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                           physicalR0='Signed target-slot byte; no semantic return value is inferred for this void routine',
                           wholeMappedRamItcmStackRegistersFlagsAndTracesCompared=True,
                           independentIntentPhaseRetryFallbackAndRngModel=True, results=results,
                           limitations=['Gate0 probes use unusable actors and do not claim the748-byte chooser default path',
                                        'Gate2 probes use valid supplied record pointers and repeated action1/2 slots with raw control word0',
                                        'Gate1 reuses separately frozen candidate/validation recipes; broad live-scene reachability remains unsupported',
                                        'R3 is explicitly supplied0 at observed ordinary callers and ignored by the native body',
                                        'Only the380-byte caller gains source credit; every callee implementation remains separately accounted']))
    dependencies = ['ov001_intent_preparation_cases_20261030.py', 'ov001_turn_order_itcm_fixture_20261030.py',
                    'ov001_action_candidate_cases_20261030.py', 'ov001_action_retry_cases_20261030.py',
                    'ov001_action_retry_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
               compiler=dict(path=str(compiler.COMPILER.relative_to(ROOT)), sha256=sha256(compiler.COMPILER)),
               moduleInputSha256=overlay_metadata['sha256'], mainInputSha256=main_metadata['sha256'],
               itcmInputSha256=itcm_metadata['sha256'], assetHashes={name: compiler.sha(raw) for name, raw in assets.items()},
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_intent_preparation_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=380,
                          actualReturns=len(results) * 2)), flush=True)


if __name__ == '__main__':
    run()
