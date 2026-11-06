import json
import re
import sys
from itertools import product
from pathlib import Path

import match_runtime as compiler
from link_runtime_unit import measured_module
from ndspy.rom import NintendoDSRom
from ov001_damage_pipeline_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from unicorn import __version__ as unicorn_version

REPORT = ROOT / 'evidence/application/ov001-provider-main-signed-divide-abi-20261030.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned execution runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM differs')
    main_metadata, main, symbols = measured_module('main')
    module_metadata, overlay, unused = measured_module('ov001')
    mode, size = re.search(r'kind:function\((arm),size=(0x[0-9a-f]+)\) addr:0x02026144$', symbols, re.M).groups()
    size = int(size, 0)
    rom = NintendoDSRom(config['rom'].read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'AbilityTbl.bin', 'ActTbl.bin', 'ItemTbl.bin', 'EquipTbl.bin')}
    results = []
    for numerator, denominator, scratch in product((0, 1, 7, -7, -2147483648, 2147483647, -2147483647),
                                                   (0, 1, -1, 2, -3, -2147483648, 2147483647), (0, 1, 0xDEADBEEF)):
        quotient = numerator
        if denominator:
            quotient = abs(numerator) // abs(denominator)
            if (numerator < 0) != (denominator < 0):
                quotient = -quotient
        remainder = numerator - quotient * denominator if denominator else 0
        result = execute(main, overlay, assets, 0x02026144, [numerator, denominator, scratch], [], [], quotient & 0xFFFFFFFF,
                         1750000 + len(results), [], [])
        if result['registers'][1] != remainder & 0xFFFFFFFF:
            raise ValueError('Original signed runtime remainder differs from the independent model')
        results.append(dict(numerator=numerator, denominator=denominator, initialScratchR2=hex(scratch),
                            expectedQuotient=hex(quotient & 0xFFFFFFFF), expectedRemainder=hex(remainder & 0xFFFFFFFF), result=result))
    dependencies = ['ov001_damage_pipeline_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    write_json(REPORT, dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], module='main', processor='arm9',
               mode=mode, address='0x02026144', bytes=size, moduleInputSha256=main_metadata['sha256'],
               nativeSpanSha256=compiler.sha(main[0x26144:0x26144 + size]), overlayFixtureInputSha256=module_metadata['sha256'],
               actualReturns=len(results), sourceCredit=0, hostCalleeStubs=False, freshMachinePerExecution=True,
               inputWords='R0 signed numerator, R1 signed denominator; R2 is varied initial caller scratch, not a third argument',
               outputWords='R0 quotient, R1 remainder; zero denominator returns the original numerator and zero remainder',
               results=results, instructionBound=100000,
               inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
               generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
               limitations=['Original machine code only, with zero reconstructed-source or original-assembly credit',
                            'INT_MIN/-1 returns wrapped quotient0x80000000 with remainder0; the explicit runtime call preserves this and zero-denominator behavior',
                            'R2 variations leave R0/R1 behavior unchanged; the native entry assigns R2 before division-loop uses and zero-denominator paths do not use it',
                            'These measurements qualify this build/address only and do not authorize an unsigned-helper alias'],
               reproductionCommand='python prove_ov001_provider_sdiv_20261030.py'))
    print(json.dumps(dict(actualReturns=len(results), sourceCredit=0, report=str(REPORT.relative_to(ROOT)))), flush=True)


if __name__ == '__main__':
    run()
