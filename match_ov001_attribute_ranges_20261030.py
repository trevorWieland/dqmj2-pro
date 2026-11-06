import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_attribute_range_cases_20261030 import nibble_vectors, range_vectors
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-attribute-ranges-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-attribute-ranges01.json'
UNITS = [('attribute_nibbles_521f0ee3b8de', '521f0ee3b8ded8431ada9c8734d6fd3d609c4035ccc53e2d0c24c9a18e79f597', 0x021F08EC, 100),
         ('special_ranges_d54ff3e2223f', 'd54ff3e2223f4782c86560054ce55389624bd98e169268d78a3cf2e53b29bbaa', 0x021EF0B0, 372)]


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    matches = []
    for index, (label, source_hash, address, size) in enumerate(UNITS):
        source = ROOT / f'src/overlays/ov001_20261030_{label}.c'
        if sha256(source) != source_hash:
            raise ValueError('Frozen ordinary source differs')
        compiler.WORK = WORK / f'u{index}' / 'c'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(rows) != 1 or rows[0].get('compiledBytes') != size or not rows[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Frozen source no longer matches the complete native span')
        row = rows[0]
        bindings = qualified_bindings(row)
        directory = WORK / f'u{index}' / 'link' / row['objectSha256']
        proof = validate(row, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / f'u{index}' / 'immutable-link-artifacts'
        row.update(save_link_snapshots.freeze_link(proof))
        candidate = bytearray(overlay)
        candidate[address - 0x021D7240:address - 0x021D7240 + size] = linked
        results = []
        for vector in (nibble_vectors(assets['ActTbl.bin']) if size == 100 else range_vectors(assets['ActTbl.bin'])):
            original = execute(main, overlay, assets, address, vector['arguments'], vector['memory'], vector['patches'],
                               vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            rebuilt = execute(main, bytes(candidate), assets, address, vector['arguments'], vector['memory'], vector['patches'],
                              vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            if original != rebuilt:
                raise ValueError('Original and real-linked attribute/range machines differ')
            results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
            if len(results) % 256 == 0:
                print(label, 'returning vectors', len(results), flush=True)
        row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
                   signature='u32(u8 *, u32)' if size == 100 else 'u32(u8 *, u8 *, s32, s32)',
                   nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                   oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                               freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                               independentImmutableMetadataNibblesAndNativeDispatchRangeArithmeticModel=True,
                               allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                               nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                               nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results), results=results,
                               limitations=['Attribute getter covers all256 immutable action records, raw side0/1/255 and supplied raw scene0/7',
                                            'Raw scene7 selects the original mode path that never dereferences the actor pointer; supplied null/FFFFFFFF pointers are qualified to that path',
                                            'Range provider covers every recognized action plus0/6/255 default, counter0/1/127/255 and dispatcher0/1/2/3/FFFFFFFF',
                                            'Actors/records have zero trait/status/gear state; no positive modifiers, ordinary scene reachability or future RNG state is inferred',
                                            'All asset files remain original; dependencies and supplied state receive zero duplicate source credit']))
        matches.append(row)
    inputs = ['ov001_attribute_range_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
              'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
               moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
               wholeModuleLinked=False, sourceReconstructionComplete=False,
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in inputs],
               assetHashes={name: compiler.sha(data) for name, data in assets.items()}, generator=Path(__file__).name,
               generatorSha256=sha256(Path(__file__)), reproductionCommand='python match_ov001_attribute_ranges_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=2, bytes=472,
                          actualReturns=sum(row['oracle']['executions'] for row in matches))), flush=True)


if __name__ == '__main__':
    run()
