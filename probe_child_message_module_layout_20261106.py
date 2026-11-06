import hashlib
import os
import subprocess
from unittest.mock import patch
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256
from inspect_child_message_assets_20261105 import from_source, encode_with_recipe


def main():
    config = configuration()
    native_dependencies(config)
    import ndspy.bmg as bmg
    import match_runtime as compiler
    import utility_runtime
    import link_arm7
    from elftools.elf.elffile import ELFFile
    layout, unused = utility_runtime.derive()
    module = next(row for row in layout['modules'] if row['id'] == 'utility-child-arm9-main')
    native = (ROOT / module['binary']).read_bytes()
    assert sha256(ROOT / module['binary']) == module['sha256']
    semantic = read_json(ROOT / 'evidence/lanes/parallel-wave20261105/source95-data-inspection/semantic-roundtrip.json')
    protected = {name: sha256(ROOT / name) for name in ['recovery.json', 'source-preferences.json', 'link_arm7.py']}
    output = ROOT / 'work/source95-child-message-module-layout'
    env = dict(os.environ, LM_LICENSE_FILE=str(config['license']))
    assert sha256(compiler.COMPILER) == compiler.COMPILER_PINS[compiler.COMPILER.relative_to(ROOT).as_posix()]
    attempts = []
    for alignment in (1, 4):
        directory = output / f'align{alignment}'
        directory.mkdir(parents=True, exist_ok=True)
        rows, assets = [], []
        for asset in semantic['assets']:
            pin = ROOT / asset['sourcePath']
            assert sha256(pin) == asset['sourceSha256']
            source = read_json(pin)
            encoded = encode_with_recipe(from_source(source['source'], bmg), source['compressionRecipe'])
            assert hashlib.sha256(encoded).hexdigest() == asset['originalEncodedSha256']
            address = int(asset['address'], 0)
            size = (len(encoded) + alignment - 1) // alignment * alignment
            expected = encoded + bytes(size - len(encoded))
            offset = address - int(module['base'], 0)
            assert native[offset:offset + size] == expected
            name = f'native_child_message_layout_{address:08x}'
            unit, obj = directory / f'{address:08x}.c', directory / f'{address:08x}.o'
            lines = [f'const unsigned char {name}[{size}] = {{']
            lines += ['    ' + ', '.join(f'0x{v:02x}' for v in encoded[start:start + 16]) + ','
                      for start in range(0, len(encoded), 16)]
            unit.write_text('\n'.join(lines + ['};', '']), encoding='utf-8')
            command = [str(compiler.COMPILER), *compiler.FLAGS, '-c', str(unit), '-o', str(obj)]
            run = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, timeout=60)
            assert run.returncode == 0, run.stdout + run.stderr
            with obj.open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(s for s in elf.get_section_by_name('.symtab').iter_symbols() if s.name == name)
                section = elf.get_section(symbol['st_shndx'])
                assert symbol['st_info']['type'] == 'STT_OBJECT' and symbol['st_size'] == size
                assert section['sh_type'] == 'SHT_PROGBITS' and not section['sh_flags'] & 4
                assert section.data()[symbol['st_value']:symbol['st_value'] + size] == expected
                assert not any(s['sh_flags'] & 4 and s['sh_size'] for s in elf.iter_sections())
            rows.append(dict(name=name, kind='data', mode='data', program=utility_runtime.PROGRAM,
                             processor='arm9', module=module['id'], address=hex(address), bytes=size,
                             source=unit.relative_to(ROOT).as_posix(), sourceSha256=sha256(unit),
                             object=obj.relative_to(ROOT).as_posix(), objectSha256=sha256(obj), section=section.name))
            assets.append(dict(address=hex(address), encodedBytes=len(encoded), storageBytes=size,
                               measuredZeroAlignmentBytes=size - len(encoded), semanticSource=asset['sourcePath']))
        def private_failure(path, value):
            assert path == ROOT / 'evidence/linking/arm7-failed-module.json'
            write_json(directory / 'failed-module.json', value)
        try:
            with patch.object(link_arm7, 'write_json', side_effect=private_failure):
                result, units = link_arm7.build_module(module, rows, {}, config, output_root=directory)
            assert result['exactBytes'] and result['symbolCheckPassed'] and len(units) == 8
            attempt = dict(exactModule=True, moduleSha256=result['outputSha256'], moduleResult=result)
        except ValueError as error:
            assert (directory / 'failed-module.json').is_file()
            attempt = dict(exactModule=False, reason=str(error), failedReport=(directory / 'failed-module.json').relative_to(ROOT).as_posix())
        attempts.append(dict(alignment=alignment, assets=assets, payloadBytes=sum(r['encodedBytes'] for r in assets),
                             measuredZeroAlignmentBytes=sum(r['measuredZeroAlignmentBytes'] for r in assets),
                             sourceRows=rows, **attempt))
    assert attempts[-1]['exactModule']
    assert protected == {name: sha256(ROOT / name) for name in protected}
    receipt = dict(passed=True, sourceCredit=0, dataSourceCredit=0, sourceDataAdmissionImplemented=False,
                   executableBytes=0, functionCredit=0, scaffoldingAssisted=True, attempts=attempts,
                   generator=__file__.split('\\')[-1], generatorSha256=sha256(__file__), protectedInputs=protected)
    write_json(ROOT / 'evidence/lanes/parallel-wave20261105/source95-data-inspection/module-layout-probe.json', receipt)
    print(dict(passed=True, moduleExact=[r['exactModule'] for r in attempts], payloadBytes=attempts[-1]['payloadBytes'],
               measuredZeroAlignmentBytes=attempts[-1]['measuredZeroAlignmentBytes'], sourceCredit=0))


if __name__ == '__main__':
    main()
