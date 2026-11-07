import contextlib
import copy
import hashlib
import shutil
from pathlib import Path
from unittest.mock import patch
from project import ROOT, read_json, write_json, sha256
from link_runtime_unit import relocation_rows

READY = 'evidence/lanes/parallel-wave20261106/mb-local-context-next/register-packet/ready.json'
READY_SHA = 'f319e62f2a87952d1e196b17e34b627e9307192eade19ef5eb5aede9a2c11c63'
INPUTS = 'evidence/lanes/parallel-wave20261106/mb-local-context-next/register-packet/inputs-v2.json'
INPUTS_SHA = 'ad7d1246d03c3a498187b34a0cc61367dbd4fad4191ffa3483957ff9ceab3dec'
NAME = 'MB_RegisterFile'
ADDRESS = 0x02015c70
SIZE = 656
STORAGE = 0x020e68a4


def contract():
    assert sha256(ROOT / READY) == READY_SHA and sha256(ROOT / INPUTS) == INPUTS_SHA
    ready, inputs = read_json(ROOT / READY), read_json(ROOT / INPUTS)
    assert ready['functions'] == 1 and ready['bytes'] == SIZE and ready['initializedStorageBytes'] == 0
    descriptor = ready['canonicalDescriptor']
    assert sha256(ROOT / descriptor['path']) == descriptor['sha256']
    row, = inputs['entries']
    assert (row.get('program') or '', row['processor'], row['module'], row['mode'], int(row['address'], 0), row['bytes']) == ('', 'arm9', 'main', 'arm', ADDRESS, SIZE)
    assert sha256(ROOT / row['source']) == row['sourceSha256']
    for pin in row['sourceDependencies']:
        assert sha256(ROOT / pin['path']) == pin['sha256']
    return row


def inspect_object(path):
    from elftools.elf.elffile import ELFFile
    from qualify_arm9_thumb_reference_inputs_20261105 import derive
    expected = contract()
    with Path(path).open('rb') as stream:
        elf = ELFFile(stream)
        assert elf.elfclass == 32 and elf.little_endian and elf['e_machine'] == 'EM_ARM'
        symbols = list(elf.get_section_by_name('.symtab').iter_symbols())
        functions = [s for s in symbols if s['st_info']['type'] == 'STT_FUNC' and s['st_size']]
        assert len(functions) == 1
        function = functions[0]
        assert function.name == NAME and function['st_info']['bind'] == 'STB_GLOBAL'
        assert function['st_size'] == SIZE and function['st_value'] == 0
        text = elf.get_section(function['st_shndx'])
        assert text.name == '.text' and text['sh_type'] == 'SHT_PROGBITS' and text['sh_size'] == SIZE and text['sh_flags'] == 6
        assert any(s.name == '$a' and s['st_value'] == 0 and s['st_shndx'] == function['st_shndx'] for s in symbols)
        storage = elf.get_section_by_name('.bss')
        assert storage['sh_type'] == 'SHT_NOBITS' and storage['sh_size'] == storage['sh_addralign'] == 1
        assert storage['sh_flags'] == 3
        objects = [s for s in symbols if s['st_info']['type'] == 'STT_OBJECT' and s['st_shndx'] == elf.get_section_index('.bss')]
        assert len(objects) == 1
        local = objects[0]
        assert local.name == 'update$40' and local['st_value'] == 0 and local['st_size'] == 1
        assert local['st_info']['bind'] == 'STB_LOCAL' and local['st_other']['visibility'] == 'STV_DEFAULT'
        allocated = [s for s in elf.iter_sections() if s['sh_flags'] & 2 and s['sh_size']]
        assert {s.name for s in allocated} == {'.text', '.bss'} and len(allocated) == 2
        body = text.data()
    relocations = relocation_rows(path, NAME)
    assert relocations == expected['originalObjectRelocations']
    retained = [r for r in relocations if r['symbol'] == '.bss']
    assert len(retained) == 1 and (retained[0]['offset'], retained[0]['type'], retained[0]['explicitAddend']) == (652, 2, 0)
    image = derive()
    native = image[ADDRESS - 0x02000000:ADDRESS - 0x02000000 + SIZE]
    assert hashlib.sha256(native).hexdigest() == expected['targetSha256']
    assert int.from_bytes(native[652:656], 'little') == STORAGE
    ignored = {r['offset'] + i for r in relocations for i in range(4)}
    assert all(a == b for i, (a, b) in enumerate(zip(body, native)) if i not in ignored)
    return dict(body=body, relocations=relocations, localName=local.name)


def check_unit(unit):
    expected = contract()
    assert (unit.get('processor'), unit['module'], unit.get('mode'), unit.get('kind'), unit.get('function'), int(unit['start'], 0), int(unit['end'], 0)) == ('arm9', 'main', 'arm', 'function', NAME, ADDRESS, ADDRESS + SIZE)
    assert unit['source'] == expected['source'] and unit['sourceSha256'] == expected['sourceSha256']
    assert unit['sourceDependencies'] == expected['sourceDependencies']
    assert unit['symbols'] == {'func_02015c70': NAME} and not unit.get('interiorSymbols')
    assert not unit.get('sectionPaddingBytes') and unit['section'] == unit['sourceSection'] == '.text'
    assert sha256(ROOT / unit['object']) == unit['sha256']
    return inspect_object(ROOT / unit['object'])


@contextlib.contextmanager
def module_route(builder):
    import native_bindings
    original_collect, original_prepare, original_split = builder.collect_units, builder.prepare_units, builder.split_symbol
    active = {}

    def collect(source_units, reports):
        found = []
        for path in reports:
            document = read_json(path)
            for row in document.get('functionMatches', document.get('matches', [])):
                retained = [r for r in row.get('relocations', []) if r.get('symbol') == '.bss']
                if not retained:
                    continue
                assert row['name'] == NAME and row['source'] == contract()['source'] and len(retained) == 1
                assert retained[0]['binding'] == 'retained-source-local-section' and int(retained[0]['target'], 0) == STORAGE
                found.append(row)
        if not found:
            return original_collect(source_units, reports)
        assert len(found) == 1
        previous = native_bindings.merge_target

        def merge(bindings, name, value):
            if name == '.bss':
                assert int(value, 0) == STORAGE
                return
            return previous(bindings, name, value)

        with patch.object(native_bindings, 'merge_target', merge):
            result = original_collect(source_units, reports)
        spec = read_json(result)
        selected = [u for u in spec['units'] if u.get('function') == NAME]
        assert len(selected) == 1 and '.bss' not in spec.get('nativeSymbols', {})
        unit = selected[0]
        check_unit(unit)
        permitted = {str(r['offset']) for r in found[0]['relocations'] if r['symbol'] in found[0]['nativeSymbolEntries']}
        assert set(unit.get('relocationAliases', {})) <= permitted
        unit.pop('relocationAliases', None)
        storage = copy.deepcopy(unit)
        storage.update(kind='data', mode=None, section='.bss', sourceSection='.bss', start=hex(STORAGE), end=hex(STORAGE + 1), symbols={'data_020e68a4': 'update$40'})
        for key in ['function', 'typedFunctionBindings', 'targetSha256']:
            storage.pop(key, None)
        storage['initializedStorageCredit'] = 0
        spec['units'].append(storage)
        write_json(result, spec)
        active[unit['unit']] = unit
        return result

    def split(elf, name, output, *extra, **options):
        if name != NAME:
            return original_split(elf, name, output, *extra, **options)
        assert extra in [({}, None, 0), (None, None, 0)] and options == {'target_section': None}
        source = Path(elf.stream.name)
        record = inspect_object(source)
        shutil.copyfile(source, output)
        assert sha256(source) == sha256(output)
        return record['body'], [r['offset'] for r in record['relocations']]

    def prepare(path, report):
        result = original_prepare(path, report)
        if not active:
            return result
        assert len(active) == 1
        name = next(iter(active))
        target = builder.WORK / 'config-arm9/delinks.txt'
        content = target.read_text()
        first = f'\n{name}:\n    complete\n    .text start:0x{ADDRESS:08x} end:0x{ADDRESS + SIZE:08x}\n'
        second = f'\n{name}:\n    complete\n    .bss start:0x{STORAGE:08x} end:0x{STORAGE + 1:08x}\n'
        assert content.count(first) == content.count(second) == 1
        target.write_text(content.replace(first, first.rstrip('\n') + '\n' + second[second.index('    .bss'):]).replace(second, ''))
        target = builder.WORK / 'config-arm9/symbols.txt'
        content = target.read_text()
        line = 'update$40 kind:bss(size=0x1) addr:0x020e68a4'
        assert content.count(line) == 1
        target.write_text(content.replace(line, line + ' local'))
        report['qualifiedRegisterLocalStorage'] = dict(functionBytes=SIZE, actualCompilerObjectUnchanged=True,
            localBssBytes=1, initializedStorageCredit=0, nativeAddress=hex(STORAGE), contractReadySha256=READY_SHA)
        return result

    with patch.object(builder, 'collect_units', collect), patch.object(builder, 'split_symbol', split), patch.object(builder, 'prepare_units', prepare):
        yield
