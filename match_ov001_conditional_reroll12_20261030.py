import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_compact_proof12_20261030 import store
from ov001_conditional_reroll12_cases_20261030 import vectors
from ov001_scalar_frontier07_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_conditional_reroll_41e7e443b4bf.c'
SOURCE_HASH = '41e7e443b4bf6a7b751c5ab0fee6c80882cf10dfcee664b5fd1a2fa9a843894e'
WORK = ROOT / 'work/ov001-reroll12-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-conditional-reroll12.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Pinned conditional-reroll source/runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 216 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Complete conditional-reroll source span differs')
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
    candidate[0x02210AD0 - 0x021D7240:0x02210AD0 - 0x021D7240 + 216] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results = []
    for number, vector in enumerate(vectors()):
        try:
            original = execute(main, overlay, assets, 0x02210AD0, vector['arguments'], vector['memory'], vector['patches'],
                               vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            rebuilt = execute(main, bytes(candidate), assets, 0x02210AD0, vector['arguments'], vector['memory'], vector['patches'],
                              vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            if original != rebuilt:
                raise ValueError('Exact conditional-reroll machines differ')
        except Exception as error:
            print(json.dumps(dict(number=number, recipe={key: value for key, value in vector.items() if key not in ('memory', 'patches')})), flush=True)
            raise error
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
        if number % 256 == 0:
            print('actual-return reroll recipes', number, flush=True)
    row['oracle'] = dict(executions=2 * len(results), actualReturns=2 * len(results),
        nativeRngActualReturns=2 * sum(len(v['result']['rngReturns']) for v in results),
        nativeDependencyActualReturns=2 * sum(len(v['result']['protocolReturns']) for v in results),
        maximumInstructions=max(v['result']['instructions'] for v in results),
        hostCalleeStubs=False, freshMachinePerExecution=True, completeImageEquality=True, instructionBound=100000)
    row['oracle']['results'], row['oracle']['rawTraceArtifact'] = store(results, 0x02210AD0, SOURCE_HASH, config['romSha256'], WORK / 'raw-traces')
    row['nativeSymbolEntries'] = bindings
    dependencies = ['ov001_conditional_reroll12_cases_20261030.py', 'ov001_compact_proof12_20261030.py',
                    'ov001_scalar_frontier07_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    record = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        assetHashes={name: compiler.sha(data) for name, data in assets.items()},
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
        generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        limitations=['Only216 native bytes receive proposed source credit; dependencies receive no new credit',
                    'Skills40/41, duplicate/zero/full64 lists, signed thresholds/limits and raw signed current/upper-limited maximum scalar are explicit inputs',
                    'Form byte1FD is0; the alternative nonzero-form trait gate requires separate metadata and is not established',
                    'No live or future scene seed, valid-save record or ordinary battle reachability is inferred',
                    'Full original/source checks execute before compact serialization; complete raw results remain deterministically compressed and hashed'],
        reproductionCommand='python match_ov001_conditional_reroll12_20261030.py')
    write_json(REPORT, record)
    print(json.dumps({key: row['oracle'][key] for key in ('executions', 'nativeRngActualReturns', 'nativeDependencyActualReturns', 'maximumInstructions')}), flush=True)


if __name__ == '__main__':
    run()
