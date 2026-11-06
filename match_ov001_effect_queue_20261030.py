import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_effect_queue_cases_20261030 import queue_vectors, constructor_vectors
from ov001_effect_queue_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-command-scheduling/20261030/effect-queue-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-effect-queue01.json'
UNITS = [('effect_queue_slot_6d6ed92d1440', '6d6ed92d1440e5650e494d38f0423ead1ba64d190c4071aaec2dfba58e98faf6', 0x021E9CD8, 72),
         ('effect_resource_constructor_74c8a98915b2', '74c8a98915b2f05b4c8de44ab59037b9ca193d3eda9b687c63baead097da9073', 0x021EEC7C, 252)]


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Private measured ROM differs')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    if int.from_bytes(main[0x5CA08:0x5CA0C], 'little') != 0x021043AC:
        raise ValueError('Original32-slot pool base changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin')}
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
        cases = queue_vectors() if size == 72 else constructor_vectors()
        results = []
        for vector in cases:
            original = execute(main, overlay, assets, address, vector['arguments'], vector['memory'], vector['patches'],
                               vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            rebuilt = execute(main, bytes(candidate), assets, address, vector['arguments'], vector['memory'], vector['patches'],
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
                   signature='u32(u32, u8 *, s32)' if size == 72 else 's32(u32, u8 *, s32)',
                   nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                   oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                               freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                               independentFirstMinusOneQueueSlotSignedKindAndFullNativePoolFailureModel=True,
                               allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                               nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                               nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results),
                               results=results, limitations=[
                                   'Queue returns one after invoking the constructor, even when the stored result remains0xFFFFFFFF',
                                   'Negative kinds execute the original constructor rejection; nonnegative kinds execute original full32-slot allocator failure',
                                   'Opaque IDs/pointers are deliberately not dereferenced on the tested failure paths; game-valid inputs are not inferred',
                                   'Successful resource initialization, category-based adjustment and actor attachment remain unsupported by this corpus',
                                   'Original dependencies execute with nested actual-return/argument checks and no host providers or duplicate source credit']))
        matches.append(row)
    dependencies = ['ov001_effect_queue_cases_20261030.py', 'ov001_effect_queue_fixture_20261030.py',
                    'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
               moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'],
               itcmInputSha256=itcm_metadata['sha256'], wholeModuleLinked=False, sourceReconstructionComplete=False,
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               assetHashes={name: compiler.sha(data) for name, data in assets.items()},
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               reproductionCommand='python match_ov001_effect_queue_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=2, bytes=324,
                          actualReturns=sum(row['oracle']['executions'] for row in matches))), flush=True)


if __name__ == '__main__':
    run()
