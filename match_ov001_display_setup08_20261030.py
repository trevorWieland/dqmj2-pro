import json
import sys
from itertools import product
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from ov001_display_setup08_fixture_20261030 import execute
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import __version__ as unicorn_version

SOURCE = ROOT / 'src/overlays/ov001_20261030_display_resource_setup_4e3a76eaa154.c'
SOURCE_HASH = '4e3a76eaa1544019799baf711af155a587a7d2d5acb69af52fc9db3c4b77687e'
WORK = ROOT / 'work/ov001-display08-final-20261030'
REPORT = ROOT / 'evidence/matches/ov001-20261030-display-setup08.json'


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4' or sha256(SOURCE) != SOURCE_HASH:
        raise ValueError('Pinned display source/runtime differs')
    config = configuration()
    if sha256(config['rom']) != config['romSha256']:
        raise ValueError('Measured private ROM differs')
    compiler.WORK = WORK / 'c'
    rows, unused = compiler.compare(SOURCE, 'ov001', '2', 'off', True)
    if len(rows) != 1 or rows[0].get('compiledBytes') != 212 or not rows[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Complete display source span does not match')
    row = rows[0]
    bindings = qualified_bindings(row)
    directory = WORK / 'link' / row['objectSha256']
    proof = validate(row, bindings, directory)
    save_link_snapshots.DIRECTORY = WORK / 'immutable-link-artifacts'
    row.update(save_link_snapshots.freeze_link(proof))
    linked = (directory / 'caller.bin').read_bytes()
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    itcm_metadata, unused, unused = measured_module('itcm')
    candidate = bytearray(overlay)
    candidate[0x021F0F98 - 0x021D7240:0x021F0F98 - 0x021D7240 + len(linked)] = linked
    results = []
    for index, (length, initial, terminal) in enumerate(product((0, 2, 64, 512), (0, 1, 127, 255), (0, 0xFFFFFFFF, 0x80000000, 0xABCDEF12))):
        seed = 1980000 + index
        original = execute(main, overlay, seed, length, initial, terminal)
        rebuilt = execute(main, bytes(candidate), seed, length, initial, terminal)
        if original != rebuilt:
            raise ValueError('Exact source-linked display caller differs from original machine')
        results.append(dict(seed=seed, suppliedResourceBytes=length, initialRawState=initial,
                            suppliedTerminalPhysicalR0=hex(terminal), result=original))
    row['oracle'] = dict(evidenceClass='native caller with explicit provided resource/graphics boundaries and original RAM dependencies',
        executions=2 * len(results), actualReturns=2 * len(results), providedCalls=2 * sum(len(item['result']['providerCalls']) for item in results),
        nativeDependencyActualReturns=2 * sum(len(item['result']['nativeDependencyReturns']) for item in results),
        instructionBound=100000, freshMachinePerExecution=True, originalDependencies=['0x0204BBEC', '0x020848D0', '0x021F1A08', '0x0205F998', '0x02008C14', '0x021F0F60', '0x0204518C', '0x02045128', '0x0204514C'],
        hardwareEmulation=False, filesystemOpened=False, nativeProviderCredit=0, results=results)
    row['nativeSymbolEntries'] = bindings
    dependencies = ['ov001_display_setup08_fixture_20261030.py', 'ov001_damage_pipeline_fixture_20261030.py', 'ov001_award_fixture_20261029.py']
    record = dict(schemaVersion=1, createdUtc=now(), romSha256=config['romSha256'], matches=[row],
        moduleInputSha256=metadata['sha256'], mainInputSha256=main_metadata['sha256'], itcmInputSha256=itcm_metadata['sha256'],
        inputPins=[dict(path=path, sha256=sha256(ROOT / path)) for path in dependencies],
        generator=Path(__file__).name, generatorSha256=sha256(Path(__file__)),
        sourceDeclaration='void(void)', physicalR0='Opaque terminal service R0 remains observable; original return meaning is not inferred',
        limitations=['Only212 reconstructed caller bytes receive source credit; native dependencies/providers receive zero new credit',
                    'Resource loader/release and graphics/palette services are provided boundaries; their native bodies are not claimed executed',
                    'Original two-word span reader, four-pointer fill,32-record constructor sequence,48-byte RAM clear and no-op execute without substitution',
                    'The loader provides a synthetic count/offset resource view; original4518C/45128/4514C produce the actual two-word output and return pointer',
                    'Provider calls explicitly supply opaque caller-clobbered registers; supplied resource views are not observed filesystem states',
                    'Whole RAM/ITCM, actual return, preserved registers, private stack, flags and complete traces agree per exact image',
                    'No actual display scene, device, VRAM/MMIO, ordinary lifecycle reachability or rendered result is established'],
        reproductionCommand='python match_ov001_display_setup08_20261030.py')
    write_json(REPORT, record)
    print(json.dumps(dict(bytes=212, functions=1, actualReturns=row['oracle']['executions'],
        nativeDependencyActualReturns=row['oracle']['nativeDependencyActualReturns'], providedCalls=row['oracle']['providedCalls'])), flush=True)


if __name__ == '__main__':
    run()
