import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_native_scalar_cases_20261030 import vectors
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-native-scalar-final-20261030'
SOURCE = ROOT / 'src/overlays/ov001_20261030_native_scalar_sequence_9ccd1179f3f3.c'
SOURCE_HASH = '9ccd1179f3f3aa7fa5943c6252a970ad3ff46a941d4790dc949570831f2d27b6'
REPORT = ROOT / 'evidence/matches/ov001-20261030-native-scalar-sequence01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen source or pinned runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private measured ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 576 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen scalar sequence no longer matches all576 bytes')
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
    candidate[0x021EF638 - 0x021D7240:0x021EF638 - 0x021D7240 + len(linked)] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results = []
    for vector in vectors(assets['ActTbl.bin']):
        original = execute(main, overlay, assets, 0x021EF638, vector['arguments'], vector['memory'], vector['patches'],
                           vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        rebuilt = execute(main, bytes(candidate), assets, 0x021EF638, vector['arguments'], vector['memory'], vector['patches'],
                          vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        if original != rebuilt:
            raise ValueError('Original and real-linked scalar-sequence machines differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
        if len(results) % 128 == 0:
            print('returning vectors', len(results), flush=True)
    abi = dict(module='ov001', processor='arm9', mode='arm', address='0x021dbd24', bytes=12,
               nativeSpanSha256=compiler.sha(overlay[0x021DBD24 - 0x021D7240:0x021DBD24 - 0x021D7240 + 12]),
               moduleInputSha256=metadata['sha256'], input='R0 actor pointer', output='R0 full-word sign extension of actor+1F0 signed halfword',
               newSourceCredit=0, originalCDeclarationUnknown=True)
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=576, justifiedAssemblyBytes=0,
               signature='u32(u32, u32, u8 *, u8 *, u32, s32, s32, s32)', nativeSymbolEntries=bindings,
               isolatedCallerLink=proof, qualifiedNativeGetterAbi=abi,
               oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           independentSignedFractionsWrappedPercentNativeIdGuardDispatchAndScaleModel=True,
                           allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                           nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                           nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results), results=results,
                           limitations=['Original action43/8/78 special branches run with supplied zero trait/status/gear records and raw scene0',
                                        'Other recipes explicitly override copied action253 native-ID/format/range fields in emulated RAM; original ROM/asset files remain unchanged',
                                        'All ten sequential selector outcomes, inactive formats, signed-halfword extremes, word wrap and final double/triple controls are exercised',
                                        'Native getters, random dispatcher, special providers and default generator execute original instructions with actual argument/return checks',
                                        'Positive record/gear/status modifiers, unsupported special-action variants and scene reachability remain unproved',
                                        'Dependencies, supplied metadata and assets have zero duplicate reconstructed-source credit']))
    dependencies = ['ov001_native_scalar_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
                    'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
               moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
               wholeModuleLinked=False, sourceReconstructionComplete=False,
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               assetHashes={name: compiler.sha(data) for name, data in assets.items()},
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_native_scalar_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=576,
                          actualReturns=row['oracle']['executions'], nativeRngActualReturns=row['oracle']['nativeRngActualReturns'])), flush=True)


if __name__ == '__main__':
    run()
