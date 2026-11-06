import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_classified_scalar_cases_20261030 import vectors
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from prove_ov001_provider_byte_returns_20261030 import run as prove_byte_returns
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-classified-scalar-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-classified-scalar01.json'
UNITS = [('classified_scalar_d6e9698e76bd', 'd6e9698e76bd69f3447bc810f5b0639e007773ef609b73e6ce33d4bf6c066a4b', 0x021F0D5C, 344, None),
         ('classified_scalar_wrapper_b091d29f5234', 'b091d29f5234e615cd9ab7db122f0086e9e8b5dd2c62eb2526d7b4c6e3dfb5ab', 0x021F0030, 84,
          ROOT / 'tools/mwccarm/mwccarm/2.0/sp1p6/mwccarm.exe')]


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured ROM differs')
    prove_byte_returns()
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    matches = []
    for index, (label, source_hash, address, size, executable) in enumerate(UNITS):
        source = ROOT / f'src/overlays/ov001_20261030_{label}.c'
        if sha256(source) != source_hash:
            raise ValueError('Frozen ordinary C differs')
        compiler.WORK = WORK / f'u{index}/c'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True, False, executable)
        if len(rows) != 1 or rows[0].get('compiledBytes') != size or not rows[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Complete source span does not match')
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
        for number, vector in enumerate(vectors(assets, wrapper=index == 1)):
            try:
                original = execute(main, overlay, assets, address, vector['arguments'], vector['memory'], vector['patches'],
                                   vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
                rebuilt = execute(main, bytes(candidate), assets, address, vector['arguments'], vector['memory'], vector['patches'],
                                  vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
                if original != rebuilt:
                    raise ValueError('Original and real-linked machines differ')
            except Exception as error:
                print(json.dumps(dict(address=hex(address), number=number,
                    recipe={key: value for key, value in vector.items() if key not in ('memory', 'patches')})), flush=True)
                raise error
            results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
            if len(results) % 256 == 0:
                print(label, 'returning recipes', len(results), flush=True)
        row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
            signature='u32(u32, u8 *, u8 *, u32, s32, u32 *, s32, s32, s32)' if size == 344 else 'u32(u32, u32, u8 *, u8 *, s32, u32 *, s32, s32, s32)',
            nativeSymbolEntries=bindings, isolatedCallerLink=proof,
            oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                independentByteModesClassificationChanceWordArithmeticAndAliasedOutputModel=True,
                allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results), results=results,
                limitations=['All action-mode/classification/coefficient data are supplied emulated copies; initialized remap tables and ROM/assets stay original',
                    'Active modes1/2 use modifier0 to avoid the unmodeled positive 0220E3A8 modifier path; inactive mode0 covers modifier words0/1/FFFFFFFF',
                    'Target status bytes22C are zero, so caller-tier tests use the direct attribute row; signed remapping is covered separately by3072 original-only ABI returns',
                    'Empty skill/gear state avoids chance retries; no positive actor modifier effects, ordinary scene or future RNG state are inferred',
                    'Aligned output alias88 clears saved mode bytes before their read; no unaligned output addresses are claimed',
                    'Malformed tier255 uses explicitly supplied mapped BSS bytes and does not establish a valid game record',
                    'Wrapper passes four register words and five stack words, preserving control/output and inverting the nonzero flag to0',
                    'Native dependencies and the3072 original-only ABI prerequisite receive zero duplicate source credit']))
        matches.append(row)
    inputs = ['ov001_classified_scalar_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
              'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py', 'prove_ov001_provider_byte_returns_20261030.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        wholeModuleLinked=False, sourceReconstructionComplete=False, separateOriginalOnlyAbiPrerequisiteActualReturns=3072,
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in inputs],
        assetHashes={name: compiler.sha(data) for name, data in assets.items()}, generator=Path(__file__).name,
        generatorSha256=sha256(Path(__file__)), reproductionCommand='python match_ov001_classified_scalar_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=2, bytes=428,
        actualReturns=sum(row['oracle']['executions'] for row in matches))), flush=True)


if __name__ == '__main__':
    run()
