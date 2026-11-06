import json
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_fixture_20261030 import execute
from ov001_percent_provider_cases_20261030 import eligible_vectors, metadata_vectors
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

WORK = ROOT / 'work/ov001-percent-providers-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-percent-providers01.json'
UNITS = [('eligible_order_percent_4b27a6441a18', '4b27a6441a183cccf343ccd52600cbfac290dd1e80d698078b18ae8cb4a89329', 0x021EF8D0, 548, eligible_vectors),
         ('metadata_percent_c4cd817e8f87', 'c4cd817e8f876b1ab1b40d512165b3c688c0dfc110eda105b134b6bb99f61f2f', 0x021EFEDC, 340, metadata_vectors)]


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
    for index, (label, source_hash, address, size, vectors) in enumerate(UNITS):
        source = ROOT / f'src/overlays/ov001_20261030_{label}.c'
        if sha256(source) != source_hash:
            raise ValueError('Frozen ordinary C differs')
        compiler.WORK = WORK / f'u{index}/c'
        rows, unused = compiler.compare(source, 'ov001', '2', 'off', True)
        if len(rows) != 1 or rows[0].get('compiledBytes') != size or not rows[0].get('exactAfterDeclaredRelocation'):
            raise ValueError('Complete original source span does not match')
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
        for number, vector in enumerate(vectors(assets)):
            try:
                original = execute(main, overlay, assets, address, vector['arguments'], vector['memory'], vector['patches'],
                                   vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
                rebuilt = execute(main, bytes(candidate), assets, address, vector['arguments'], vector['memory'], vector['patches'],
                                  vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
                if original != rebuilt:
                    raise ValueError('Original and source-linked machines differ')
            except Exception as error:
                print(json.dumps(dict(address=hex(address), number=number,
                    recipe={key: value for key, value in vector.items() if key not in ('memory', 'patches')})), flush=True)
                raise error
            results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'result': original})
            if len(results) % 256 == 0:
                print(label, 'returning recipes', len(results), flush=True)
        row.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=size, justifiedAssemblyBytes=0,
            signature='u32(u32, s32, u8 *, u8 *, s32)' if size == 548 else 'u32(u32, u32, u8 *, u8 *)',
            nativeSymbolEntries=bindings, isolatedCallerLink=proof,
            oracle=dict(vectors=len(results), executions=2 * len(results), actualReturnRequired=True,
                freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                independentSignedWrappedProductTruncationAndAssetMaskEligibilityModel=True,
                allRegistersFlagsStackTracesAndFullRamItcmCompared=True,
                nativeRngActualReturns=2 * sum(len(item['result']['rngReturns']) for item in results),
                nativeProtocolActualReturns=2 * sum(len(item['result']['protocolReturns']) for item in results), results=results,
                limitations=['All256 original action records and original species categories0..8 are exercised with supplied actor/roster records',
                    'Synthetic percentage, item-byte and metadata cases alter only disposable emulated RAM copies; no ROM or asset file is changed',
                    'The eligibility predicate checks enabled31C, marker1FF and recordAC; no alive/HP meaning is inferred',
                    'Empty skill records avoid positive native skill2/122 suppression; no positive equipment effects or ordinary scene reachability are inferred',
                    'Opaque unused actor pointers and blocked actor/target pointers are qualified to the tested non-dereferencing paths',
                    'The original dependencies, metadata, supplied roster states and RNG receive zero duplicate source credit']))
        matches.append(row)
    inputs = ['ov001_percent_provider_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
              'ov001_damage_pipeline_cases_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=matches,
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        wholeModuleLinked=False, sourceReconstructionComplete=False,
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in inputs],
        assetHashes={name: compiler.sha(data) for name, data in assets.items()}, generator=Path(__file__).name,
        generatorSha256=sha256(Path(__file__)), reproductionCommand='python match_ov001_percent_providers_20261030.py'))
    print(json.dumps(dict(report=str(REPORT.relative_to(ROOT)), functions=2, bytes=888,
        actualReturns=sum(row['oracle']['executions'] for row in matches))), flush=True)


if __name__ == '__main__':
    run()
