import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_turn_start_cases_20261030 import snapshot_vectors, turn_vectors
from ov001_turn_start_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-command-scheduling/20261030/turn-start-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-turn-start01.json'
UNITS = [('status_snapshot_7032fcedf41d', '7032fcedf41d4c3baf0dffcea4b9cc4ad0464a41bf863ff26ee569eef25a7985', 0x021DCABC, 136),
         ('turn_start_7b881c7cb50c', '7b881c7cb50c45e1e770065e83ddae5aa71d303147136761c68c4a9a0d7e4b95', 0x021DE598, 172)]


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private measured ROM differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    if overlay[0x021DE590 - 0x021D7240:0x021DE598 - 0x021D7240] != bytes.fromhex('0000a0e31eff2fe1'):
        raise ValueError('Original continuation predicate is no longer the measured return-zero body')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin')}
    if any(assets['ActTbl.bin'][8 + action * 40 + 38] != 0 for action in (0, 6)):
        raise ValueError('Prepared and blocked actions no longer share the modeled ordering class')
    matches = []
    for label, source_hash, address, size in UNITS:
        source = ROOT / f'src/overlays/ov001_20261030_{label}.c'
        if sha256(source) != source_hash:
            raise ValueError('Frozen ordinary turn source changed')
        compiler.WORK = WORK / label / 'compiler'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(rows) != 1 or not rows[0].get('exactAfterDeclaredRelocation') or rows[0]['bytes'] != size:
            raise ValueError('Frozen source no longer matches the complete native span')
        row = rows[0]
        bindings = qualified_bindings(row)
        directory = WORK / label / 'link' / row['objectSha256']
        proof = validate(row, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / label / 'immutable-link-artifacts'
        row.update(save_link_snapshots.freeze_link(proof))
        candidate = bytearray(overlay)
        candidate[address - 0x021D7240:address - 0x021D7240 + size] = linked
        cases = snapshot_vectors() if size == 136 else turn_vectors(assets['ActTbl.bin'][8:], overlay)
        results = []
        for vector in cases:
            original = execute(main, overlay, assets, address, [], vector['memory'], vector['patches'],
                               vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            rebuilt = execute(main, bytes(candidate), assets, address, [], vector['memory'], vector['patches'],
                              vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            if original != rebuilt:
                raise ValueError('Original and exact-linked turn-start machine results differ')
            recipe = {key: value for key, value in vector.items() if key not in ('memory', 'patches', 'context')}
            if 'context' in vector:
                recipe['context'] = {key: value for key, value in vector['context'].items() if key != 'memory'}
            results.append({**recipe, 'result': original})
            if len(results) % 160 == 0:
                print(label, 'returning vectors', len(results), flush=True)
        row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
                   signature='void(void)' if size == 136 else 'u32(void)',
                   nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                   oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                               freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                               independentSnapshotFlagsIntentsContextFillOrderLcgModel=True,
                               allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                               nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                               nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results),
                               results=results, limitations=[
                                   'Snapshot ranges and flag bytes are measured; field meanings and save persistence remain unproved',
                                   'The parent seeds only raw scene2 from the supplied main context+C word; current/future scene seed is not inferred',
                                   'Reselection uses supplied actor+235=1 and executes original blocked action6 path; healthy scoring is outside this corpus',
                                   'Counts0..3 and five raw scene/ITCM contexts are supplied components, not complete scene reachability',
                                   'Snapshot physical R0 is the final original copy source-end pointer; its exposed C interface is void',
                                   'Original dependencies execute without duplicate source/function credit']))
        matches.append(row)
    dependencies = ['ov001_turn_start_cases_20261030.py', 'ov001_turn_start_fixture_20261030.py',
                    'ov001_turn_order_itcm_cases_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
               moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'],
               itcmInputSha256=itcm_metadata['sha256'], wholeModuleLinked=False, sourceReconstructionComplete=False,
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               assetHashes={name: compiler.sha(data) for name, data in assets.items()},
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_turn_start_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=2, bytes=308,
                          actualReturns=sum(row['oracle']['executions'] for row in matches))), flush=True)


if __name__ == '__main__':
    run()
