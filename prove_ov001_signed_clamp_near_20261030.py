import json
import struct
import sys
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module, validate
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'nonmatching/ov001/20261030-action-effect-application01/clamp-signed-word.c'
SOURCE_HASH = '402f3d43c74d5d3a2496a5cb76560243ac872ce647178243a1b1a54debc6e8e5'
WORK = ROOT / 'work/ov001-clamp-near-20261030'
REPORT = ROOT / 'evidence/functional/ov001-signed-clamp-near-20261030.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Pinned execution runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '1', 'off', False)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 56 or rows[0].get('matchingBytes') != 46:
        raise ValueError('Frozen clamp hypothesis differs')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link'
    try:
        validate(row, bindings, directory)
    except ValueError as error:
        failure = error.args[0]
    else:
        raise ValueError('Near clamp unexpectedly became exact')
    linked = (directory / 'caller.bin').read_bytes()
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate = bytearray(overlay)
    candidate[0x021F0534 - 0x021D7240:0x021F0534 - 0x021D7240 + len(linked)] = linked
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results = []
    for action in (0, 255):
        for cap in (-32768, -1, 0, 1, 9999, 32767):
            for value in (-2147483648, -10000, -1, 0, 1, 9998, 9999, 10000, 32767, 2147483647):
                expected = min(value, cap if cap > 0 else 9999) & 0xFFFFFFFF
                memory = [(0x02320000 + action * 40 + 0x1C, struct.pack('<h', cap))]
                protocol = [dict(address=0x0207AFEC, arguments=[action], returnWord=0x02320000 + action * 40)]
                original = execute(main, overlay, assets, 0x021F0534, [value, action], memory, [], expected, 1550000 + len(results), [], protocol)
                rebuilt = execute(main, bytes(candidate), assets, 0x021F0534, [value, action], memory, [], expected, 1550000 + len(results), [], protocol)
                for key in ('returnBits', 'rngReturns', 'protocolReturns', 'protocolEntries'):
                    if original[key] != rebuilt[key]:
                        raise ValueError(('Native and near clamp behavior differs', key))
                if original['registers'][4:12] != rebuilt['registers'][4:12]:
                    raise ValueError('Native and near clamp preserved registers differ')
                results.append(dict(action=action, suppliedSignedCap=cap, suppliedSignedValue=value, expectedReturnWord=hex(expected),
                                    original=original, candidate=rebuilt))
    inputs = ['ov001_damage_pipeline_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    record = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='ov001', processor='arm9', mode='arm',
                  address='0x021f0534', nativeBytes=56, source=str(SOURCE.relative_to(ROOT)), sourceSha256=sha256(SOURCE),
                  sourceCredit=0, exactMatch=False, compilerComparison=row, actualLinkMismatch=failure, nativeSymbolEntries=bindings,
                  moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
                  actualReturns=len(results) * 2, nativeGetterActualReturns=len(results) * 2, results=results,
                  freshMachinePerExecution=True, hostCalleeStubs=False, instructionBound=100000,
                  assetHashes={name: compiler.sha(data) for name, data in assets.items()},
                  inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in inputs],
                  generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
                  limitations=['Signed cap halfword in the emulated copied ActTbl records is synthetic; original ROM and asset files are unchanged',
                               'R0 is the complete32-bit word for signed min(value, positive-cap-or9999); negative values are preserved without a zero lower bound',
                               'Native main getter consumes action word0/255 and returns the measured table-record pointer',
                               'Full RAM and unchanged ITCM are modeled independently per image; scratch registers, flags and private stacks may differ',
                               'Original source declaration cannot be identified from physical return bits alone; the typed signed model remains unaccepted ordinary C'],
                  reproductionCommand='python prove_ov001_signed_clamp_near_20261030.py')
    write_json(REPORT, record)
    print(json.dumps({'actualReturns': record['actualReturns'], 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    run()
