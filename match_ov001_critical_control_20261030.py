import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_critical_control_cases_20261030 import vectors
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-critical-final-20261030'
SOURCE = ROOT / 'src/overlays/ov001_20261030_critical_control_892908518d69.c'
SOURCE_HASH = '892908518d69cd0d2f1de77ee4cc46f1c506adfcb95715d6d57afdcfd7b23417'
REPORT = ROOT / 'evidence/matches/ov001-20261030-critical-control01.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen source or pinned runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private measured ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 248 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen control stage no longer exactly matches all248 bytes')
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
    candidate[0x021F00C4 - 0x021D7240:0x021F00C4 - 0x021D7240 + len(linked)] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results = []
    for vector in vectors(assets['ActTbl.bin']):
        original = execute(main, overlay, assets, 0x021F00C4, vector['arguments'], vector['memory'], vector['patches'],
                           vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        rebuilt = execute(main, bytes(candidate), assets, 0x021F00C4, vector['arguments'], vector['memory'], vector['patches'],
                          vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        if original != rebuilt:
            raise ValueError('Original and real-linked critical-control machines differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
        if len(results) % 128 == 0:
            print('returning vectors', len(results), flush=True)
    row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=248, justifiedAssemblyBytes=0,
               signature='u32(s32, u8 *, u8 *, u32, s32, s32)', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
               oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                           freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                           independentSignedWrappedScaleAttackClampClassificationGuardAndLcgModel=True,
                           allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                           nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                           nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results), results=results,
                           limitations=['Action0/6 original metadata and disjoint supplied actor/record components with zero skill/gear/status state',
                                        'Classification bytes0/1/255 in BSS table2232B90 are supplied synthetic component state, not observed initialized scene data',
                                        'Modes0/5/7, zero/nonzero/FFFFFFFF control, both sides, zero-limit RNG, signed extremes and overflowing12x products are covered',
                                        'Main0203D294 consumes one input word; generated extra R1/R2 arguments were temporary division-register artifacts',
                                        'The original attack getter clamps successful supplied field220 cases to1..9999; its original C return declaration is not inferred',
                                        'Original dependencies and immutable assets have zero additional source credit; ordinary critical selection probability and scene reachability remain unproved']))
    dependencies = ['ov001_critical_control_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
                    'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
               moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
               wholeModuleLinked=False, sourceReconstructionComplete=False,
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               assetHashes={name: compiler.sha(data) for name, data in assets.items()},
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_critical_control_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=1, bytes=248,
                          actualReturns=row['oracle']['executions'], nativeRngActualReturns=row['oracle']['nativeRngActualReturns'])), flush=True)


if __name__ == '__main__':
    run()
