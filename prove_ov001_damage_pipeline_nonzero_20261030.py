import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from match_ov001_damage_pipeline_20261030 import SOURCE, SOURCE_HASH
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_nonzero_cases_20261030 import vectors
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-pipeline-nonzero-20261030'
REPORT = ROOT / 'evidence/functional/ov001-damage-pipeline-nonzero-20261030.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Frozen matched source or pinned runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen pipeline source no longer exactly matches')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link'
    proof = validate(row, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'immutable-link-artifacts'
    snapshots = save_link_snapshots.freeze_link(proof)
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
            raise ValueError('Original and real-linked nonzero pipeline machines differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
    inputs = ['ov001_damage_pipeline_nonzero_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
              'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py', 'match_ov001_damage_pipeline_20261030.py']
    record = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov001', processor='arm9', mode='arm',
                  address='0x021f0578', nativeBytes=612, source=str(SOURCE.relative_to(ROOT)), sourceSha256=sha256(SOURCE),
                  sourceCredit=0, additionalSourceCredit=0, matchedSourceReference='evidence/matches/ov001-20261030-damage-pipeline01.json',
                  compilerComparison=row, nativeSymbolEntries=bindings, isolatedCallerLink=proof, frozenLinkSnapshots=snapshots,
                  moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
                  freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                  actualReturns=len(results) * 2, nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                  nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results),
                  allRegistersFlagsStackTracesAndFullRamItcmCompared=True, independentNonzeroAttackCriticalAndDispatchLcgModel=True,
                  assetHashes={name: compiler.sha(data) for name, data in assets.items()}, results=results,
                  inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in inputs],
                  generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
                  limitations=['Supplied action0 original metadata, actor attack field220=100/defense field222=20/raw signed halfword1F8=1000, valid empty record buffers and zero stage/trait/gear state',
                               'Word3 is explicitly supplied0/1; its application-level selection/chance and ordinary actor/scene reachability are not inferred',
                               'Word6 controls native random dispatcher0/3=LCG,1=zero,2=limit-minus-one; actual LCG calls/returns/SP/state are checked',
                               'Word10 explicitly selects unchanged/doubled output; no future seed, game history or save persistence is observed',
                               'All32 stage inputs and actual returns satisfy the independent arithmetic model; positive traits, equipment, status and resistance cases remain outside this corpus',
                               'The supported domain does not establish a private inherited-register ABI for other routines; original dependencies remain zero additional source credit'],
                  reproductionCommand='python prove_ov001_damage_pipeline_nonzero_20261030.py')
    write_json(REPORT, record)
    print(json.dumps({key: record[key] for key in ('actualReturns', 'nativeRngActualReturns', 'nativeProtocolActualReturns', 'additionalSourceCredit')}), flush=True)


if __name__ == '__main__':
    run()
