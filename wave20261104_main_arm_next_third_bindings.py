import copy
import struct
from project import ROOT, read_json, sha256
import hashlib
from link_runtime_unit import verify_binding
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/third/data-inputs.json'
INPUT_SHA = '1d89117c3f8c801fd18459c2eb178bceea4d21893d10f2876c2c174814c43b79'


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Original conditional-pointer data contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'relocations', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Original data inventory/image changed')
    return value


def validate(case, row, relocation, binding, image, inventory, loads):
    expected = ('', 'arm9', 'main', 'arm')
    if tuple(row.get(k) or '' for k in ['program', 'processor', 'module', 'mode']) != expected:
        raise ValueError('Callable-slot caller namespace differs')
    if tuple(case.get(k) or '' for k in ['program', 'processor', 'module', 'mode']) != expected:
        raise ValueError('Callable-slot witness namespace differs')
    if (row['address'], row['bytes'], row['targetSha256']) != (case['caller'], case['bytes'], case['callerSha256']) or row['address'] != '0x202882c' or row['bytes'] != 416:
        raise ValueError('Callable-slot exact original caller differs')
    target = int(case['target'], 0)
    if target not in [0x020dd8c0, 0x020dd8b8] or case['symbol'] != 'native_data_%08x' % target:
        raise ValueError('Only the two measured initialized callable slots are qualified')
    offset, default, positions = ((408, 0x0203c05c, [140, 148, 160, 184, 192, 204]) if target == 0x020dd8c0 else (412, 0x0203c04c, [232, 240, 252]))
    if (relocation['symbol'], relocation['offset'], relocation['type'], relocation['addend']) != (case['symbol'], offset, 2, 0) or case['offset'] != offset:
        raise ValueError('Exact callable-slot ABS32 relocation/addend differs')
    if tuple(binding.get(k) or '' for k in ['program', 'processor', 'module', 'mode', 'kind']) != ('', 'arm9', 'main', 'data', 'data'):
        raise ValueError('Callable slot confused with function or other native namespace')
    if int(binding['address'], 0) != target or int(relocation['target'], 0) != target:
        raise ValueError('Callable slot data address differs')
    origin = 0x0202882c + offset
    if int(case['literalPool'], 0) != origin or case['originalLoadRecord'] != 'from:0x%08x kind:load to:0x%08x module:main' % (origin, target) or case['originalLoadRecord'] not in loads.splitlines():
        raise ValueError('Original pool-to-slot load record missing')
    if case['originalInventoryRecord'] != 'data_%08x kind:data(any) addr:0x%08x' % (target, target) or case['originalInventoryRecord'] not in inventory.splitlines():
        raise ValueError('Exact original initialized data(any) inventory missing')
    if hashlib.sha256(image[0x2882c:0x289cc]).hexdigest() != case['callerSha256']:
        raise ValueError('Complete original callable-slot caller changed')
    literal = image[origin - 0x02000000:origin - 0x02000000 + 4]
    if literal.hex() != case['literalWordHex'] or literal != struct.pack('<I', target):
        raise ValueError('Original callable-slot source literal differs')
    if case['originalInitializationRecord'] != 'from:0x%08x kind:load to:0x%08x module:main' % (target, default) or case['originalInitializationRecord'] not in loads.splitlines():
        raise ValueError('Original slot-to-default-function initialization record missing')
    initial = image[target - 0x02000000:target - 0x02000000 + 4]
    if initial.hex() != case['initialWordHex'] or initial != struct.pack('<I', default):
        raise ValueError('Actual initialized callable word/mode differs')
    function = case['defaultFunction']
    if tuple(function.get(k) or '' for k in ['program', 'processor', 'module', 'mode', 'kind']) != ('', 'arm9', 'main', 'arm', 'function') or int(function['address'], 0) != default or function['bytes'] != 8:
        raise ValueError('Default callable function identity/mode/extent differs')
    if function['sourceRecord'] != 'func_%08x kind:function(arm,size=0x8) addr:0x%08x' % (default, default) or function['sourceRecord'] not in inventory.splitlines():
        raise ValueError('Default ARM function inventory missing')
    if hashlib.sha256(image[default - 0x02000000:default - 0x02000000 + 8]).hexdigest() != function['targetSha256']:
        raise ValueError('Complete default ARM function code differs')
    if (case['pointerWidth'], case['argumentWidths'], case['returnWidth'], case['originalStorageCredit'], case['completeObjectExtent']) != (4, [4, 4, 4], 4, 0, None):
        raise ValueError('Observed callable ABI or zero storage/unknown full extent differs')
    words = {140: 0xe59f1104, 148: 0xe5913000, 160: 0xe12fff33, 184: 0xe59f10d8, 192: 0xe5913000, 204: 0xe12fff33, 232: 0xe59f20ac, 240: 0xe5923000, 252: 0xe12fff33}
    for position in positions:
        if struct.unpack_from('<I', image, 0x2882c + position)[0] != words[position]:
            raise ValueError('Original literal-load/dereference/BLX-register witness differs')
    verify_binding(relocation['symbol'], binding)
    verify_binding('native_fn_%08x' % default, function)
    return dict(symbol=case['symbol'], origin=hex(origin), target=hex(target), dataKind='data(any)', originalLoadRecord=case['originalLoadRecord'], originalInventoryRecord=case['originalInventoryRecord'], originalInitializationRecord=case['originalInitializationRecord'], defaultFunction=function, initializedWord=case['initialWordHex'], observedArgumentWidths=[4, 4, 4], observedReturnWidth=4, originalDataStorageCredit=0, originalCalleeCredit=0, arbitraryRuntimeReplacementsUnproved=True)


def verify_original(row, bindings):
    data = [r for r in row['relocations'] if r['type'] == 2]
    result = branch_verify(dict(row, relocations=[r for r in row['relocations'] if r['type'] != 2]), bindings)
    if not data:
        return result
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    witnesses = []
    for relocation in data:
        case = next((c for c in value['cases'] if c['caller'] == row['address'] and c['symbol'] == relocation['symbol']), None)
        if case is None:
            raise ValueError('No exact original current-pointer caller/symbol witness')
        witnesses.append(validate(case, row, relocation, bindings[relocation['symbol']], image, inventory, loads))
    return dict(result, originalDataLoadWitnesses=witnesses, externalStorageCredit=0,
                dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA))


def negative_controls(rows):
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    checks = []
    changes = [('wrong-origin', 'relocation', 'offset', 4), ('folded-addend', 'relocation', 'addend', 4),
               ('wrong-type', 'relocation', 'type', 28), ('wrong-slot', 'binding', 'address', '0x20dd8c4'),
               ('function-kind', 'binding', 'kind', 'function'), ('function-mode', 'binding', 'mode', 'arm'),
               ('wrong-CPU', 'binding', 'processor', 'arm7'), ('wrong-program', 'binding', 'program', 'child'),
               ('wrong-module', 'binding', 'module', 'ov000'), ('wrong-caller-mode', 'row', 'mode', 'thumb'),
               ('wrong-source-name', 'case', 'symbol', 'native_data_020dd8c4'),
               ('wrong-pointer-width', 'case', 'pointerWidth', 2), ('wrong-arguments', 'case', 'argumentWidths', [4, 4]),
               ('wrong-return-width', 'case', 'returnWidth', 2), ('invented-storage-credit', 'case', 'originalStorageCredit', 4),
               ('invented-full-extent', 'case', 'completeObjectExtent', 4),
               ('default-Thumb', 'defaultFunction', 'mode', 'thumb'), ('default-data', 'defaultFunction', 'kind', 'data'),
               ('default-overlay', 'defaultFunction', 'module', 'ov000'), ('default-CPU', 'defaultFunction', 'processor', 'arm7'),
               ('default-program', 'defaultFunction', 'program', 'child'), ('default-interior', 'defaultFunction', 'address', '0x203c060'),
               ('default-short-extent', 'defaultFunction', 'bytes', 4)]
    for case in value['cases']:
        row = next(r for r in rows if r['address'] == case['caller'])
        relocation = next(r for r in row['relocations'] if r['symbol'] == case['symbol'])
        binding = row['nativeSymbolEntries'][case['symbol']]
        for label, owner, key, wrong in changes:
            items = {name: copy.deepcopy(obj) for name, obj in [('case', case), ('row', row), ('relocation', relocation), ('binding', binding)]}
            target = items['case']['defaultFunction'] if owner == 'defaultFunction' else items[owner]
            target[key] = wrong
            try:
                validate(items['case'], items['row'], items['relocation'], items['binding'], image, inventory, loads)
            except ValueError as error:
                checks.append(dict(symbol=case['symbol'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid callable slot accepted: ' + label)
        bad_literal = bytearray(image)
        bad_literal[int(case['literalPool'], 0) - 0x02000000] ^= 4
        bad_initial = bytearray(image)
        bad_initial[int(case['target'], 0) - 0x02000000] ^= 1
        bad_code = bytearray(image)
        bad_code[int(case['defaultFunction']['address'], 0) - 0x02000000] ^= 1
        variants = [('changed-original-source-literal', bytes(bad_literal), inventory, loads),
                    ('changed-initial-callable-mode', bytes(bad_initial), inventory, loads),
                    ('changed-default-body', bytes(bad_code), inventory, loads),
                    ('missing-data-any-inventory', image, inventory.replace(case['originalInventoryRecord'], ''), loads),
                    ('missing-function-inventory', image, inventory.replace(case['defaultFunction']['sourceRecord'], ''), loads),
                    ('missing-pool-load-record', image, inventory, loads.replace(case['originalLoadRecord'], '')),
                    ('missing-slot-initialization-record', image, inventory, loads.replace(case['originalInitializationRecord'], ''))]
        for label, raw, inv, records in variants:
            try:
                validate(case, row, relocation, binding, raw, inv, records)
            except ValueError as error:
                checks.append(dict(symbol=case['symbol'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed original callable-slot evidence accepted: ' + label)
    return dict(status='passed', negativeCases=checks, sourceOrDataStorageCredit=0, ordinaryBranchVerifierUnchanged=True)

