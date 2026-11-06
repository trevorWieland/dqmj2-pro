import json
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_policy_helper_cases_20261030 import history_vectors, target_vectors
from ov001_policy_helper_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-command-scheduling/20261030/policy-helpers-final'
REPORT = ROOT / 'evidence/matches/ov001-20261030-policy-helpers01.json'
UNITS = [('action_history_8fc39b040ba8', 0x021E6DB4, 140, history_vectors),
         ('target_packet_f2e25d73829a', 0x021E7244, 76, target_vectors)]


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python and Unicorn required')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM identity differs')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in
              ('EnmyKindTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin', 'AbilityTbl.bin')}
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    matches, sources = [], {}
    for label, address, size, cases in UNITS:
        source = ROOT / f'src/overlays/ov001_20261030_{label}.c'
        sources[str(source.relative_to(ROOT))] = sha256(source)
        compiler.WORK = WORK / label / 'compiler'
        records, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation') or records[0]['bytes'] != size:
            raise ValueError('Frozen helper no longer matches all native bytes')
        entry = records[0]
        bindings = qualified_bindings(entry)
        directory = WORK / label / 'link' / entry['objectSha256']
        proof = validate(entry, bindings, directory)
        linked = (directory / 'caller.bin').read_bytes()
        save_link_snapshots.DIRECTORY = WORK / label / 'link-artifacts'
        entry.update(save_link_snapshots.freeze_link(proof))
        rebuilt = bytearray(overlay)
        rebuilt[address - 0x021D7240:address - 0x021D7240 + size] = linked
        rebuilt = bytes(rebuilt)
        results = []
        for vector in cases():
            original = execute(main, overlay, assets, address, vector)
            candidate = execute(main, rebuilt, assets, address, vector)
            if original != candidate:
                raise ValueError('Original native versus linked policy helper differs')
            results.append(original)
        entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
                     nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                     oracle={'vectors': len(results), 'executions': 2 * len(results),
                             'actualReturnRequired': True, 'freshMachinePerExecution': True,
                             'nativeCalleesExecuted': True, 'hostCalleeStubs': False,
                             'independentReturnAndCompleteReadOnlyRamModel': True,
                             'wholeMappedRamAndStackCompared': True, 'instructionBound': 100000,
                             'actualProtocolReturnsBothImages': 2 * sum(len(row['protocolReturns']) for row in results),
                             'results': results,
                             'limitations': ['Synthetic raw metadata tables in overlay BSS do not establish loaded asset provenance or scene reachability',
                                             'History domain is side0/1 and slots0..2; action IDs0,1,40,255 and supplied flag/history/intent words are synthetic',
                                             'Target domain supplies actor+322=1 and record+A9 tiers0..4; gate lifecycle and probabilistic tier branch remain unproved',
                                             'Target callbacks0,1,8 are verified original native return0 bodies, never host replacements; callback9 reads actual actor slot',
                                             'Other callbacks, current RNG, legal targets and whole-combat behavior are outside this corpus',
                                             'The packet helper callback words are address/module/mode-qualified; indirect targets gain no duplicate source credit']})
        matches.append(entry)
    table = overlay[0x0222FA20 - 0x021D7240:0x0222FA20 - 0x021D7240 + 40]
    callback_proofs = []
    for index in (0, 1, 8, 9):
        address = struct.unpack_from('<I', table, index * 4)[0]
        size = 12 if index == 9 else 8
        body = overlay[address - 0x021D7240:address - 0x021D7240 + size]
        expected = [0xE5900000, 0xE5D0031F, 0xE12FFF1E] if index == 9 else [0xE3A00000, 0xE12FFF1E]
        if list(struct.unpack('<' + 'I' * len(expected), body)) != expected:
            raise ValueError('Original native callback body proof differs')
        callback_proofs.append({'index': index, 'module': 'ov001', 'processor': 'arm9', 'mode': 'arm',
                                'address': hex(address), 'bytes': size, 'spanSha256': compiler.sha(body),
                                'actualOriginalNativeBody': True, 'hostReplacement': False,
                                'additionalSourceCredit': 0})
    dependencies = [Path(__file__).name, 'ov001_policy_helper_cases_20261030.py',
                    'ov001_policy_helper_fixture_20261030.py', 'ov001_action_candidate_cases_20261030.py',
                    'ov001_action_retry_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    report = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': config['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': matches, 'sourceHashes': sources,
              'callbackTable': {'address': '0x0222fa20', 'bytes': 40, 'sha256': compiler.sha(table),
                                'entries': callback_proofs, 'sourceDataCredit': 0},
              'syntheticMetadata': [{'address': '0x022430c8', 'recordStride': 5, 'flagOffset': 4},
                                    {'address': '0x02243dc8', 'lookupStride': 8, 'constantSelectorFixtures': [0, 1, 8, 9]}],
              'assetHashes': {name: compiler.sha(raw) for name, raw in assets.items()},
              'sourceReconstructionComplete': False, 'wholeModuleLinked': False,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'replayDependencies': [{'path': path, 'sha256': sha256(ROOT / path)} for path in dependencies],
              'nativeSymbols': {row['symbol']: row['target'] for entry in matches for row in entry['relocations']}}
    write_json(REPORT, report)
    print(json.dumps({'functions': len(matches), 'bytes': sum(row['bytes'] for row in matches),
                      'executions': sum(row['oracle']['executions'] for row in matches),
                      'protocolReturns': sum(row['oracle']['actualProtocolReturnsBothImages'] for row in matches),
                      'report': str(REPORT.relative_to(ROOT))}))


if __name__ == '__main__':
    run()
