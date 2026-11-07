import contextlib
import hashlib
import importlib
from unittest.mock import patch

SOURCE = 'src/runtime/parallel_wave20261106/mb-local-context-next/register/register.c'
SOURCE_SHA = '80d436b52f4ddfa6f1c5fe27cbf92470504a7ca1c09de779c1ee0badba89d475'
NAME = 'MB_RegisterFile'
ADDRESS, SIZE, STORAGE = 0x02015c70, 656, 0x020e68a4
ROUTE = 'mb_register_module_route_v1_20261106.py'
PINS = {
    ROUTE: '27e5dcae2ac06a01ebb01447940f153db084a0f8f70be1fc304c19515760b418',
    'evidence/verification/mb-register-module-route-v2-qualification-20261106.json':
        'bd1f5e122760c7385512f0675269f44005891aed568b3a9cd0cafcf15d85f489',
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def storage_contract(unit):
    expected = dict(processor='arm9', module='main', mode=None, kind='data', section='.bss',
        sourceSection='.bss', source=SOURCE, sourceSha256=SOURCE_SHA,
        symbols={'data_020e68a4': 'update$40'})
    require(all(unit.get(k) == v for k, v in expected.items()), 'Unqualified register local BSS identity')
    require(not unit.get('program') and int(unit['start'], 0) == STORAGE
        and int(unit['end'], 0) == STORAGE + 1, 'Unqualified register local BSS span')
    for name, value in (('initializedStorageCredit', 0), ('compiledBytes', 0), ('allocatedBytes', 1)):
        require(type(unit.get(name)) is int and unit[name] == value, 'Register BSS cannot receive initialized credit')
    require(not any(unit.get(k) for k in ('function', 'interiorSymbols', 'relocationOffsets',
        'nativeDataDeclaration', 'assemblyJustification', 'sectionPaddingBytes')), 'Unexpected register BSS payload')


def local_bss_profile(unit, manifest):
    if unit.get('source') != SOURCE or unit.get('kind') != 'data':
        return None
    storage_contract(unit)
    rows = [r for r in manifest['functions'] if r['sourceUnit'] == SOURCE]
    require(len(rows) == 1, 'Register BSS requires one closed source function')
    row = rows[0]
    require((row.get('program'), row['processor'], row['module'], row['mode'], int(row['address'], 0), row['bytes'])
        == (None, 'arm9', 'main', 'arm', ADDRESS, SIZE), 'Register source function namespace differs')
    require(row['sourceSha256'] == SOURCE_SHA and row['sourceDependencies'] == unit['sourceDependencies'],
        'Register local BSS source/header contract differs')
    require(row['object'] == unit['object'] and row['objectSha256'] == unit['sha256'],
        'Register local BSS historical object identity differs')
    return SOURCE, row['compilerSha256'], tuple(row['compilerFlags'])


def coalesce_layout(directory, report):
    target = directory / 'config-arm9/delinks.txt'
    content = target.read_text()
    first = f'\n{NAME}.c:\n    complete\n    .text start:0x{ADDRESS:08x} end:0x{ADDRESS + SIZE:08x}\n'
    second = f'\n{NAME}.c:\n    complete\n    .bss start:0x{STORAGE:08x} end:0x{STORAGE + 1:08x}\n'
    require(content.count(first) == content.count(second) == 1, 'Register source layout is missing or duplicated')
    content = content.replace(first, first.rstrip('\n') + '\n' + second[second.index('    .bss'):]).replace(second, '')
    symbols = directory / 'config-arm9/symbols.txt'
    text = symbols.read_text()
    line = 'update$40 kind:bss(size=0x1) addr:0x020e68a4'
    require(text.count(line) == 1 and line + ' local' not in text, 'Register local symbol is missing or duplicated')
    target.write_text(content)
    symbols.write_text(text.replace(line, line + ' local'))
    report['qualifiedRegisterLocalStorage'] = dict(functionBytes=SIZE, actualCompilerObjectUnchanged=True,
        localBssBytes=1, initializedStorageCredit=0, nativeAddress=hex(STORAGE))


@contextlib.contextmanager
def register_context(builder, root, units):
    selected = [u for u in units if u.get('source') == SOURCE]
    if not selected:
        yield
        return
    functions = [u for u in selected if u.get('function') == NAME]
    storage = [u for u in selected if u.get('kind') == 'data']
    require(len(selected) == 2 and len(functions) == len(storage) == 1, 'Exact register function/BSS pair required')
    storage_contract(storage[0])
    require(functions[0]['object'] == storage[0]['object'] and functions[0]['sha256'] == storage[0]['sha256']
        and functions[0]['sourceDependencies'] == storage[0]['sourceDependencies'], 'Register BSS must share the fresh whole object')
    def verify_pins():
        for name, expected in PINS.items():
            require(hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, 'Qualified register route changed')
    verify_pins()
    qualified = importlib.import_module(ROUTE[:-3])
    require(qualified.ROOT.resolve() == root, 'Register qualifier imported another checkout')
    qualified.check_unit(functions[0])
    with qualified.module_route(builder):
        original = builder.prepare_units
        def prepare(path, report):
            result = original(path, report)
            coalesce_layout(builder.WORK, report)
            return result
        with patch.object(builder, 'prepare_units', prepare):
            yield
    verify_pins()
