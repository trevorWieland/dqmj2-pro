import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_fixture_20261030 import execute
from ov001_rank_frontier07_cases_20261030 import direct_vectors, wrapper_vectors, MODE_SKILLS
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-rank07-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-rank-frontier07.json'
UNITS = [('skill_mode_ranks_545f45c93d7c', '545f45c93d7ca11f0a083fece6c56a6a773e18ef4df0a1a7d7d53109ada273c1', 0x0220E3A8, 1384),
         ('record_mode_rank_9f20d4d8fc66', '9f20d4d8fc66e73f45fedcafe752ddeb0451e07841d3a9ccd6cf46b1395f73b7', 0x021F0CA0, 112),
         ('action_mode_rank_8253d56b9bc6', '8253d56b9bc6d68d2e458187d2af8208bf3383d6090f7febc1c89cc05aa99a96', 0x021F0D10, 76)]


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned execution runtime differs')
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
            raise ValueError('Complete source/compiler span does not match')
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
        recipes = direct_vectors() if index == 0 else wrapper_vectors(assets, action_wrapper=index == 2)
        for number, vector in enumerate(recipes):
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
        row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
            nativeSymbolEntries=bindings, isolatedCallerLink=proof,
            oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                independentSignedMinAndNativeSkillIdOccurrenceModel=True,
                allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results),
                nativeRngActualReturns=0, results=results,
                limitations=['Positive modifiers execute all original skill queries over supplied zero-terminated64-byte native-ID lists, including duplicate/full-length lists',
                    'All28 mapped specific IDs test primary and secondary branches; universal118, equal-mode priority, unknown IDs and zero terminators are modeled independently',
                    'Actor byte261 bypass suppresses skill-record reads; opaque record pointers are qualified only to that bypass',
                    'Direct1384 function preserves negative full-word rank inputs; no unconditional u8 return is inferred for that public entry',
                    'Wrapper modes/ranks are supplied saved/action-record copies; successful return bounds do not establish valid game records, loaded scene or future state',
                    'No RNG is entered and complete RAM/ITCM stay unchanged; original dependencies receive zero duplicate source credit']))
        matches.append(row)
    inputs = ['ov001_rank_frontier07_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
              'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        wholeModuleLinked=False, sourceReconstructionComplete=False,
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in inputs],
        nativeSkillReader=dict(address='0x0207B674', bytes=56,
            nativeSpanSha256=compiler.sha(main[0x7B674:0x7B6AC]), inputWords=2, maximumBytesRead=64,
            terminator=0, returnRepresentation='R0 full-word occurrence count0..64', sourceCredit=0),
        modeSkillIds=[dict(skill=skill, mode=mode) for skill, mode in MODE_SKILLS],
        assetHashes={name: compiler.sha(data) for name, data in assets.items()}, generator=Path(__file__).name,
        generatorSha256=sha256(Path(__file__)), reproductionCommand='python match_ov001_rank_frontier07_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=3, bytes=1572,
        actualReturns=sum(row['oracle']['executions'] for row in matches))), flush=True)


if __name__ == '__main__':
    run()
