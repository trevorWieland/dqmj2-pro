import json
import re
import struct
import sys
from itertools import product
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from unicorn import __version__ as unicorn_version

REPORT = ROOT / 'evidence/application/ov001-provider-byte-return-abi-20261030.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned execution runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured ROM differs')
    main_metadata, main, unused = measured_module('main')
    metadata, overlay, symbols = measured_module('ov001')
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    proofs = []
    for address, table, width in ((0x021D908C, 0x02232B91, 3), (0x021D90C4, 0x02232B90, 2)):
        mode, size = re.search(r'kind:function\((arm),size=(0x[0-9a-f]+)\) addr:' + f'0x{address:08x}$', symbols, re.M).groups()
        size, results = int(size, 0), []
        positive_map, negative_map, measured_table = struct.unpack_from('<III', overlay, address - 0x021D7240 + size - 12)
        if measured_table != table:
            raise ValueError('Native byte-table literal differs')
        for value, state, attribute in product(range(256), (-1, 0, 1), (0, 12)):
            mapping = positive_map if state > 0 else negative_map
            mapped = struct.unpack_from('<I', overlay, mapping - 0x021D7240 + attribute * 8)[0] if state else attribute
            if not 0 <= mapped <= 12:
                raise ValueError('Unsupported original mapping row')
            tier = (value + attribute) % 8
            arguments = [attribute, tier, state] if width == 3 else [attribute, state]
            byte_address = table + mapped * 9 + (tier if width == 3 else 0)
            memory = [(byte_address, bytes([value]))]
            result = execute(main, overlay, assets, address, arguments, memory, [], value, 1770000 + len(results), [], [])
            results.append(dict(value=value, state=state, attribute=attribute, tier=tier if width == 3 else None,
                                mappedRow=mapped, byteAddress=hex(byte_address), arguments=[word & 0xFFFFFFFF for word in arguments], result=result))
        proofs.append(dict(processor='arm9', module='ov001', address=hex(address), mode=mode, bytes=size,
            nativeSpanSha256=compiler.sha(overlay[address - 0x021D7240:address - 0x021D7240 + size]),
            returnRepresentation='R0 fully zero-extended u8, all values 0..255', inputWords=width,
            positiveMappingAddress=hex(positive_map), negativeMappingAddress=hex(negative_map),
            actualReturns=len(results), freshMachinePerExecution=True, hostCalleeStubs=False, fullRamItcmUnchanged=True,
            results=results))
    dependencies = ['ov001_damage_pipeline_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], moduleInputSha256=metadata['sha256'],
        mainInputSha256=main_metadata['sha256'], proofs=proofs, sourceCredit=0, originalOnly=True,
        actualReturns=sum(row['actualReturns'] for row in proofs),
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
        generatorSha256=sha256(Path(__file__)), reproductionCommand='python prove_ov001_provider_byte_returns_20261030.py',
        limitations=['BSS row bytes are supplied runtime data, not immutable ROM assets or observed scene state; both initialized remap tables remain original',
                     'Qualified attributes 0/12, tiers 0..7 and state -1/0/1 exercise both conditional mappings and the direct path',
                     'Invalid/unmapped pointers and rows are unsupported; zero source/assembly authorship credit']))
    print(json.dumps(dict(actualReturns=sum(row['actualReturns'] for row in proofs), sourceCredit=0, report=str(REPORT.relative_to(ROOT)))), flush=True)


if __name__ == '__main__':
    run()
