import json
import re
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_fixture_20261030 import execute
from ov001_pipeline_stages05_cases_20261030 import vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-stage05-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-pipeline-stages05.json'
UNITS = [('random_flag_scalar_b5a05585f6ab', 'b5a05585f6aba63ece2d2bf497243d27362f51bc13c357654821d197c63f4b76', 0x021EF878, 88),
         ('category_three_halves_be3c6250cc8a', 'be3c6250cc8a652982f5269d38eb69d9b52c0831ed7bb792eaffc8b23bdc64fb', 0x021EFB14, 88),
         ('byte_divisor_dispatch_0207c6e51480', '0207c6e514805b9183ffe6a76b520deb015035765aff30c43aab662eb6e33d7a', 0x021EFB88, 108),
         ('stage_table_scalar_a31f0ba45e52', 'a31f0ba45e5254a3a9e49fa91f665e77c48beac8e0eacb3f5de1d72d36dd3066', 0x021EFBF4, 136),
         ('stage_counter_bonus_a170a4fd98fc', 'a170a4fd98fc83d34e625bf065f846d2c118ed385e6baab04ff1d14120522229', 0x021EFC7C, 124),
         ('category_mode_scalar_2a572b7f8781', '2a572b7f87812a6f17967a719ec320ba77fffbc93a0e3680b7114096778132de', 0x021EFCF8, 144),
         ('intent_count_divisor_093fefeb0e0f', '093fefeb0e0f38cc07e12b9a8192b1fbb38d02428556b7013ca4ea1828834cbe', 0x021F0254, 52),
         ('stage_seven_tenths_f68363519f8a', 'f68363519f8a8aaae3d01dde87373a2ca889a4f1eb02f0a38ba3b4020bb66c0f', 0x021F040C, 80)]


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured ROM differs')
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
        compiler.WORK = WORK / f'u{index}/c'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(rows) != 1 or rows[0].get('compiledBytes') != size or not rows[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Complete compiler/ELF span does not match')
        row = rows[0]
        bindings = qualified_bindings(row)
        directory = WORK / f'u{index}/link' / row['objectSha256']
        proof = validate(row, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / f'u{index}/immutable-link-artifacts'
        row.update(save_link_snapshots.freeze_link(proof))
        candidate = bytearray(overlay)
        candidate[address - 0x021D7240:address - 0x021D7240 + size] = linked
        results = []
        for number, vector in enumerate(vectors(address, assets, overlay)):
            try:
                original = execute(main, overlay, assets, address, vector['arguments'], vector['memory'], vector['patches'],
                                   vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
                rebuilt = execute(main, bytes(candidate), assets, address, vector['arguments'], vector['memory'], vector['patches'],
                                  vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
                if original != rebuilt:
                    raise ValueError('Original and real-source-linked machines differ')
            except Exception as error:
                print(json.dumps(dict(address=hex(address), number=number,
                    recipe={key: value for key, value in vector.items() if key not in ('memory', 'patches')})), flush=True)
                raise error
            results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
            if len(results) % 256 == 0:
                print(hex(address), 'returning recipes', len(results), flush=True)
        signature = re.search(r'u32 native_ov001_[0-9a-f]+\(([^()]*)\)', source.read_text())[1]
        row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
            signature='u32(' + signature + ')', nativeSymbolEntries=bindings, isolatedCallerLink=proof,
            oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                independentImmutableAssetMasksWordArithmeticNativeDispatchAndIntentCountModel=True,
                allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results), results=results,
                limitations=['Original all256 action records are tested per entry; synthetic branches alter only supplied RAM copies of metadata/species flags',
                    'Original two coefficient tables remain native data inputs and receive zero new authored-data credit; table stage fixtures stay-4..4',
                    'Count reader EEF98 receives actor and requestedAction explicitly, with observed signed16 return and actual intent selection; count<=1 bypasses signed division',
                    'Byte-divisor108 negative clamp is unreachable for denominator2..255 under ordinary signed-division range; no fake helper return is used to enter it',
                    'Empty skill records avoid positive native skill2/122 suppression; no positive equipment effects or whole-scene/current/future state is inferred',
                    'Opaque actor/target pointers are restricted to tested mask/mode paths that do not dereference them',
                    'All dependencies, native tables and the previously measured signed runtime ABI receive zero duplicate source credit']))
        matches.append(row)
    inputs = ['ov001_pipeline_stages05_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
              'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py', 'prove_ov001_provider_sdiv_20261030.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        wholeModuleLinked=False, sourceReconstructionComplete=False,
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in inputs],
        nativeDataDependencies=[dict(module='ov001', address=hex(address), bytes=12,
                                    sha256=compiler.sha(overlay[address - 0x021D7240:address - 0x021D7240 + 12]), sourceCredit=0)
                                for address in (0x0222DF40, 0x0222DF4C)],
        assetHashes={name: compiler.sha(data) for name, data in assets.items()}, generator=Path(__file__).name,
        generatorSha256=sha256(Path(__file__)), reproductionCommand='python match_ov001_pipeline_stages05_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=8, bytes=820,
        actualReturns=sum(row['oracle']['executions'] for row in matches))), flush=True)


if __name__ == '__main__':
    run()
