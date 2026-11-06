import gzip
import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_fixture_20261030 import execute
from ov001_skill_mode_list11_cases_20261030 import vectors as mode_vectors
from ov001_skill_context10_cases_20261030 import scalar_vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-skill-lists11-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-skill-lists11.json'
UNITS = [('skill_mode_list_6944a2aa3175', '6944a2aa31759eaa333c57158ca42e1af6b0ec4a4ac12974f0bb6525fcb11c85', 0x02210748, 320),
         ('skill_class_list_49c3954b190e', '49c3954b190e01c4daf7c6f385f845f5d21d223968848002a15906e10b69be0e', 0x02210888, 180)]


def encoded(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def compact(results, address, source_hash, rom_hash):
    raw = encoded(dict(schemaVersion=1, romSha256=rom_hash, module='ov001', processor='arm9', mode='arm',
                       address=hex(address), sourceSha256=source_hash, results=results))
    compressed = gzip.compress(raw, mtime=0)
    digest = compiler.sha(compressed)
    path = WORK / 'raw-traces' / f'{address:08x}-{digest}.json.gz'
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != compressed:
        raise ValueError('Content-addressed exact trace differs')
    path.write_bytes(compressed)
    rows = []
    for index, row in enumerate(results):
        machine = row['result']
        record = dict(case=index, recipeSha256=compiler.sha(encoded({key: value for key, value in row.items() if key != 'result'})))
        record.update({key: machine[key] for key in ('actualReturn', 'returnBits', 'instructions', 'writes',
                       'wholeRamSha256', 'writeTraceSha256', 'pcTraceSha256', 'stackSha256', 'cpsr')})
        record.update(registersSha256=compiler.sha(encoded(machine['registers'])),
            nativeDependencyActualReturns=len(machine['protocolReturns']), protocolTraceSha256=compiler.sha(encoded([machine['protocolEntries'], machine['protocolReturns']])))
        rows.append(record)
    return rows, dict(path=str(path.relative_to(ROOT)), sha256=digest, bytes=len(compressed), format='json+gzip',
                     gzipMtime=0, uncompressedSha256=compiler.sha(raw), uncompressedBytes=len(raw))


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
            raise ValueError('Frozen ordinary list source differs')
        compiler.WORK = WORK / f'u{index}/c'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(rows) != 1 or rows[0].get('compiledBytes') != size or not rows[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Complete original list source span differs')
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
        recipes = mode_vectors(assets) if index == 0 else scalar_vectors(address, assets)
        for number, vector in enumerate(recipes):
            original = execute(main, overlay, assets, address, vector['arguments'], vector['memory'], vector['patches'],
                               vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            rebuilt = execute(main, bytes(candidate), assets, address, vector['arguments'], vector['memory'], vector['patches'],
                              vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
            if original != rebuilt:
                raise ValueError('Original and exact source-linked list machines differ')
            results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
            if number % 256 == 0:
                print(hex(address), 'actual-return exact recipes', number, flush=True)
        row['oracle'] = dict(executions=2 * len(results), actualReturns=2 * len(results),
            nativeDependencyActualReturns=2 * sum(len(v['result']['protocolReturns']) for v in results),
            maximumInstructions=max(v['result']['instructions'] for v in results), nativeRngActualReturns=0,
            hostCalleeStubs=False, freshMachinePerExecution=True, completeImageEquality=True, instructionBound=100000)
        row['oracle']['results'], row['oracle']['rawTraceArtifact'] = compact(results, address, source_hash, config['romSha256'])
        row['nativeSymbolEntries'] = bindings
        matches.append(row)
    dependencies = ['ov001_skill_mode_list11_cases_20261030.py', 'ov001_skill_context10_cases_20261030.py',
                    'ov001_damage_pipeline_fixture_20261030.py', 'ov001_award_fixture_20261029.py', 'ov001_damage_pipeline_cases_20261030.py']
    record = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        assetHashes={name: compiler.sha(data) for name, data in assets.items()},
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
        generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        limitations=['Only these two500 native bytes receive source credit; the earlier2304-byte approximate proof remains zero-credit evidence',
                    'All recognized mode IDs have matching/nonmatching original metadata fixtures, full64-byte lists and data after first zero/after the bound',
                    'Class codes0..5, duplicate IDs31/32 and signed full-word wrap/division are explicit component inputs',
                    'No null/unmapped list, game-valid actor/record or whole-scene reachability claim is made',
                    'Every exact image compares complete modeled RAM/unchanged ITCM, preserved state, scratch registers, flags, private stack and traces',
                    'Full raw outputs are deterministic hashed gzip artifacts; compact serialization does not replace execution comparisons'],
        reproductionCommand='python match_ov001_skill_lists11_20261030.py')
    write_json(REPORT, record)
    print(json.dumps(dict(functions=2, bytes=500, actualReturns=sum(m['oracle']['executions'] for m in matches),
        nativeDependencyActualReturns=sum(m['oracle']['nativeDependencyActualReturns'] for m in matches))), flush=True)


if __name__ == '__main__':
    run()
