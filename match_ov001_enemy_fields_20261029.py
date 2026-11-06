import json
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import prove_reward_return_abi_20261029 as machine_model
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_award_cases_20261029 import assets
from ov001_enemy_initialization_fixture_20261029 import initial, vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261029_enemy_fields_84c7d458ace3.c'
SOURCE_SHA256 = '84c7d458ace3e5f3fd3f78f405d6321b1a7545bdeb4cd8770ddce42cd6de5bf4'
WORK = ROOT / 'work/ov001-enemy-initialization/20261029/fields-final'
REPORT = ROOT / 'evidence/matches/ov001-20261029-enemy-fields01.json'
ADDRESS, ROW, TABLE = 0x021E8D28, 0x02330000, 0x02340000


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    if sha256(SOURCE) != SOURCE_SHA256:
        raise ValueError('Frozen enemy fields source changed')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM changed')
    rom = NintendoDSRom(config['rom'].read_bytes())
    enemies = bytes(rom.getFileByName('BtlEnmyPrm2.bin'))
    action_asset = bytes(rom.getFileByName('ActTbl.bin'))
    actions = action_asset[8:]
    if len(actions) < 256 * 40:
        raise ValueError('Action table lacks all byte-indexed entries')
    compiler.WORK = WORK / 'compiler'
    records, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or records[0].get('bytes') != 120 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen enemy fields C no longer matches every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, unused = measured_module('ov001')
    rebuilt = bytearray(overlay)
    rebuilt[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + 120] = linked
    blobs = assets()
    results = []
    for index, vector in enumerate(vectors(enemies)):
        row, destination = initial(vector)
        row = bytearray(row)
        if index >= 96:
            for number in range(6):
                struct.pack_into('<H', row, 6 + number * 4, [0, 1, 127, 255, 256, 257, 65535][(index + number) % 7])
        fields = [struct.unpack_from('<H', row, 6 + number * 4)[0] & 255 for number in range(6)]
        null_table_skipped = index % 4 == 0
        if null_table_skipped:
            row[99] = 255
        enabled = vector['enhancementFlag']
        if not enabled:
            expected_r0 = 0
        elif row[99]:
            expected_r0 = row[99]
        else:
            fields = [actions[value * 40 + 35] for value in fields]
            expected_r0 = TABLE
        memory = [(machine_model.OUTPUT, destination), (ROW, bytes(row)), (TABLE, actions),
                  (0x021C6748, struct.pack('<I', 0 if null_table_skipped else TABLE)),
                  (0x020F69E4, struct.pack('<I', 8 if enabled else 0))]
        patches = [(machine_model.OUTPUT + 12, bytes(fields))]
        arguments = [machine_model.OUTPUT, ROW]
        native = machine_model.execute(main, overlay, blobs, ADDRESS, arguments, memory, patches, expected_r0, vector['machineSeed'])
        source = machine_model.execute(main, bytes(rebuilt), blobs, ADDRESS, arguments, memory, patches, expected_r0, vector['machineSeed'])
        if native != source:
            raise ValueError('Native/source enemy field state differs')
        results.append({'ordinal': index, 'enemyId': vector['enemyId'], 'sourceRowSha256': compiler.sha(bytes(row)),
                        'enabled': enabled, 'suppressionByte': row[99], 'nullTableSafelySkipped': null_table_skipped,
                        'expectedSixBytes': fields, 'sourceLanguageReturnMeaningEstablished': False, **native})
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=120, justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2,
                         'actualReturnRequired': True, 'freshMachinePerExecution': True,
                         'wholeMappedRamAndStackAndRegistersCompared': True,
                         'nativeGameplayStubs': 0, 'nativeCalleesExecuted': True,
                         'independentWordTruncationAndConditionalByteRemapModel': True,
                         'physicalFinalR0ComparedWithoutSourceReturnContract': True,
                         'instructionBound': 100000, 'results': results})
    dependencies = ['prove_reward_return_abi_20261029.py', 'ov001_enemy_initialization_fixture_20261029.py',
                    'ov001_award_cases_20261029.py', 'ov001_award_fixture_20261029.py',
                    'config/arm9/symbols.txt', 'config/arm9/overlays/ov001/symbols.txt']
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {SOURCE.relative_to(ROOT).as_posix(): sha256(SOURCE)},
              'assetHashes': {**{name: compiler.sha(value) for name, value in blobs.items()},
                              'BtlEnmyPrm2.bin': compiler.sha(enemies), 'ActTbl.bin': compiler.sha(action_asset)},
              'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'nativeSymbolEntries': bindings, 'wholeModuleLinked': False, 'sourceReconstructionComplete': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'limitations': ['Void C matches all bytes; varied physical R0 residues are checked without asserting semantic return meaning',
                  'The measured direct main caller discards R0; indirect or other-mode caller coverage remains unresolved',
                  'Nonnull action pointer is required when remapping executes; a null pointer is only tested with guards that skip it',
                  'Application reachability, encounter selection and current flags remain unproved by synthetic components',
                  'Native dependencies receive zero new source credit; arbitrary aliases and inaccessible pointers remain unsupported']}
    write_json(REPORT, result)
    print(json.dumps({'functions': 1, 'bytes': 120, 'executions': len(results) * 2,
                      'report': REPORT.relative_to(ROOT).as_posix()}))


if __name__ == '__main__':
    run()
