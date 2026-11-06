import json
import sys
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_scalar_special_near_cases_20261030 import vectors
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from prove_ov001_provider_sdiv_20261030 import run as prove_runtime_abi
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'nonmatching/ov001/20261030-pipeline-providers03/021ef224-default-first-switch.c'
SOURCE_HASH = 'de4630436c453c89437125bfda49158d9f0ca94fa6a3f0b1a08fb4b964446cbe'
WORK = ROOT / 'work/ov001-scalar-special-near-20261030'
REPORT = ROOT / 'evidence/functional/ov001-scalar-special-near-20261030.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Pinned execution runtime differs')
    prove_runtime_abi()
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 372 or rows[0].get('matchingBytes') != 334:
        raise ValueError('Frozen near special provider differs')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link'
    try:
        validate(row, bindings, directory)
    except ValueError as error:
        failure = error.args[0]
    else:
        raise ValueError('Near source unexpectedly became exact')
    linked = (directory / 'caller.bin').read_bytes()
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate = bytearray(overlay)
    candidate[0x021EF224 - 0x021D7240:0x021EF224 - 0x021D7240 + len(linked)] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results = []
    for vector in vectors(assets, main):
        original = execute(main, overlay, assets, 0x021EF224, vector['arguments'], vector['memory'], vector['patches'],
                           vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        rebuilt = execute(main, bytes(candidate), assets, 0x021EF224, vector['arguments'], vector['memory'], vector['patches'],
                          vector['physicalR0'], vector['seed'], vector['draws'], vector['protocols'])
        for key in ('returnBits', 'rngReturns', 'protocolReturns', 'protocolEntries'):
            if original[key] != rebuilt[key]:
                raise ValueError(('Native and near scalar special behavior differs', key))
        if original['registers'][4:12] != rebuilt['registers'][4:12]:
            raise ValueError('Near source preserved registers differ')
        results.append({**{key: value for key, value in vector.items() if key not in ('memory', 'patches')}, 'original': original, 'candidate': rebuilt})
    dependencies = ['ov001_scalar_special_near_cases_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py',
                    'ov001_award_fixture_20261029.py', 'ov001_damage_pipeline_cases_20261030.py', 'prove_ov001_provider_sdiv_20261030.py']
    record = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov001', processor='arm9', mode='arm',
                  address='0x021ef224', nativeBytes=372, source=str(SOURCE.relative_to(ROOT)), sourceSha256=sha256(SOURCE),
                  sourceCredit=0, exactMatch=False, compilerComparison=row, actualLinkMismatch=failure, nativeSymbolEntries=bindings,
                  moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
                  actualReturns=2 * len(results), nativeRngActualReturns=sum(len(item[image]['rngReturns']) for item in results for image in ('original', 'candidate')),
                  nativeProtocolActualReturns=sum(len(item[image]['protocolReturns']) for item in results for image in ('original', 'candidate')),
                  freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000, results=results,
                  runtimeAbiReference='evidence/application/ov001-provider-main-signed-divide-abi-20261030.json', separateRuntimeAbiReturns=147,
                  assetHashes={name: compiler.sha(data) for name, data in assets.items()},
                  inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
                  generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
                  limitations=['All four recognized actions43/151/152/248 and invalid signed/full-word actions are tested with explicit component inputs',
                               'Raw global flag0/1/255, side0/1/255, signed-halfword extremes and unused opaque actor/target words are path-qualified',
                               'Empty skill records and original item0 imply no positive luck/gear retry modifiers; whole-scene reachability is not established',
                               'Signed variable division calls the measured original two-word runtime and preserves its zero-denominator passthrough',
                               'Full RAM/unchanged ITCM are independently modeled per image; scratch registers, flags, private stacks and code windows remain separate',
                               'Default return-zero dispatcher layout is nonmatching; no fake input is added to the zero-input global flag getter to force an early MOV'],
                  reproductionCommand='python prove_ov001_scalar_special_near_20261030.py')
    write_json(REPORT, record)
    print(json.dumps({key: record[key] for key in ('actualReturns', 'nativeRngActualReturns', 'nativeProtocolActualReturns', 'sourceCredit')}), flush=True)


if __name__ == '__main__':
    run()
