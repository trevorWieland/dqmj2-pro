import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_cases_20261030 import vectors
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-pipeline-final-20261030'
SOURCE = ROOT / 'src/overlays/ov001_20261030_damage_pipeline_41ef44e4e955.c'
SOURCE_HASH = '41ef44e4e955a2eaf6da4ae1db8bb542c4943f26af76f0eaa6a8517b72234afc'
REPORT = ROOT / 'evidence/matches/ov001-20261030-damage-pipeline01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen source or pinned runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private measured ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 612 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen pipeline no longer matches all612 bytes')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link' / row['objectSha256']
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-link-artifacts'
    row.update(save_link_snapshots.freeze_link(proof))
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate = bytearray(overlay)
    candidate[0x021F0578 - 0x021D7240:0x021F0578 - 0x021D7240 + len(linked)] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results = []
    for vector in vectors(assets['ActTbl.bin']):
        original = execute(main, overlay, assets, 0x021F0578, vector['arguments'], vector['memory'], vector['patches'],
                           vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        rebuilt = execute(main, bytes(candidate), assets, 0x021F0578, vector['arguments'], vector['memory'], vector['patches'],
                          vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        if original != rebuilt:
            raise ValueError('Original and exact-linked pipeline machines differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=612, justifiedAssemblyBytes=0,
               signature='u32(u8 *, u8 *, u32, s32, s32, s32, s32, s32, s32, s32, s32)',
               nativeSymbolEntries=bindings, isolatedCallerLink=proof,
               oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           independentOriginalZeroModeMetadataStageOrderingAndZeroValueInvariantModel=True,
                           allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                           nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                           nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results), results=results,
                           limitations=['Original immutable action IDs6/7 have mode halfword0 and type byte1F zero; zero-filled actor/record contexts are supplied',
                                        'Modifier/critical word3 and words4/5/7/8 are zero; option6 is1/80000000/FFFFFFFF, option9 is0/1, option10 is0/1/80000000/FFFFFFFF',
                                        'The supported zero-value path executes all32 original stages and their actual returns without RNG or nonstack writes',
                                        'Healthy nonzero damage, positive skill/gear modifiers, critical RNG and inherited-register paths remain unsupported by this corpus',
                                        'Five immutable original asset tables are inputs with zero reconstructed-data credit; no callee source or scene reachability credit is inferred']))
    dependencies = ['ov001_damage_pipeline_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
               moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
               wholeModuleLinked=False, sourceReconstructionComplete=False,
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               assetHashes={name: compiler.sha(data) for name, data in assets.items()},
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_damage_pipeline_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=612,
                          actualReturns=row['oracle']['executions'], nativeStageReturns=row['oracle']['nativeProtocolActualReturns'])), flush=True)


if __name__ == '__main__':
    run()
