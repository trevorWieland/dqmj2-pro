import copy
import hashlib
import struct
from project import ROOT, read_json, sha256
from link_runtime_unit import verify_binding
from wave20261104_main_command_forward_bindings import validate as common_validate
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/first/data-inputs.json'
INPUT_SHA = '226a62ea21b41aa4caf21db96092320ce091bd51ff405c15e9955d25f0fec4a0'


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Frozen UI table/context contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'relocations', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Pinned original UI inventory/image differs')
    return value


def validate(case, row, relocation, binding, image, inventory, loads):
    if case.get('completeObjectExtent') is not None or case.get('externalStorageCredit') != 0 or case['typedAccesses'] != []:
        raise ValueError('No complete original UI data extent/storage credit is qualified')
    if case['symbol'] == 'native_data_021c9698':
        result = common_validate(case, row, relocation, binding, image, inventory, loads)
        if (row['address'], row['bytes'], case['role']) not in [('0x20602ec', 256, 'opaque-format-context'), ('0x20603ec', 72, 'opaque-format-context')]:
            raise ValueError('Opaque formatter context escaped measured caller family')
        return dict(result, completeObjectExtent=None, externalStorageCredit=0, role=case['role'])
    if tuple(row.get(k) or '' for k in ['program', 'processor', 'module', 'mode']) != ('', 'arm9', 'main', 'arm') or tuple(case.get(k) or '' for k in ['program', 'processor', 'module', 'mode']) != ('', 'arm9', 'main', 'arm'):
        raise ValueError('UI table caller namespace differs')
    if (row['address'], row['bytes'], row['targetSha256']) != (case['caller'], case['bytes'], case['callerSha256']) or row['address'] != '0x20602ec' or row['bytes'] != 256:
        raise ValueError('UI table must retain exact original256-byte caller')
    if case['symbol'] != 'native_data_020dbc18' or case['role'] != 'bounded-unsigned-halfword-table':
        raise ValueError('Only the measured unsigned-halfword UI table is qualified')
    if tuple(binding.get(k) or '' for k in ['program', 'processor', 'module', 'mode', 'kind']) != ('', 'arm9', 'main', 'data', 'data'):
        raise ValueError('UI table storage confused with function/other namespace')
    if (relocation['symbol'], relocation['offset'], relocation['type'], relocation['addend']) != (case['symbol'], 248, 2, 0) or case['offset'] != 248:
        raise ValueError('Original UI table ABS32 origin/addend differs')
    if case['target'] != '0x20dbc18' or int(binding['address'], 0) != 0x020dbc18 or int(relocation['target'], 0) != 0x020dbc18 or case['literalPool'] != '0x20603e4':
        raise ValueError('Original table address/pool differs')
    record = 'data_020dbc18 kind:data(any) addr:0x020dbc18'
    load = 'from:0x020603e4 kind:load to:0x020dbc18 module:main'
    if case['originalInventoryRecord'] != record or record not in inventory.splitlines() or case['originalLoadRecord'] != load or load not in loads.splitlines():
        raise ValueError('Exact original initialized-data inventory/load record missing')
    if hashlib.sha256(image[0x602ec:0x603ec]).hexdigest() != case['callerSha256'] or image[0x603e4:0x603e8] != struct.pack('<I', 0x020dbc18) or case['literalWordHex'] != image[0x603e4:0x603e8].hex():
        raise ValueError('Original UI caller or source literal changed')
    fields = ['indexMinimum', 'indexMaximum', 'elementWidth', 'indexStride', 'minimumInitializedPrefix', 'metadataFieldOffset', 'metadataFieldWidth', 'metadataNibbleShift', 'metadataNibbleWidth']
    expected = [392, 407, 2, 2, 816, 4, 2, 4, 4]
    if [case.get(key) for key in fields] != expected or len(image[0xdbc18:0xdbc18 + 816]) != 816:
        raise ValueError('Original nibble/index/element-width/minimum initialized prefix differs')
    words = {52: 0xe1d700b4, 64: 0xe1a00c00, 68: 0xe1a00e20, 72: 0xe280000d, 76: 0xe1a00800, 80: 0xe1a00820, 84: 0xe280007b, 88: 0xe2800c01, 92: 0xe1a00080, 96: 0xe19130b0}
    if any(struct.unpack_from('<I', image, 0x602ec + at)[0] != word for at, word in words.items()):
        raise ValueError('Actual original unsigned nibble/index/halfword-load sequence differs')
    verify_binding(relocation['symbol'], binding)
    return dict(symbol=case['symbol'], originalInventoryRecord=record, originalLoadRecord=load, measuredFields=dict(zip(fields, expected)),
                originalInstructionWords=words, completeObjectExtent=None, originalStorageCredit=0)


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
            raise ValueError('No exact original caller/table/context data witness')
        witnesses.append(validate(case, row, relocation, bindings[relocation['symbol']], image, inventory, loads))
    return dict(result, originalDataLoadWitnesses=witnesses, externalStorageCredit=0,
                dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA))


def negative_controls(rows):
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    checks = []
    common = [('wrong-origin', 'relocation', 'offset', 4), ('folded-addend', 'relocation', 'addend', 2),
              ('wrong-base', 'binding', 'address', '0x20dbc1a'), ('function-kind', 'binding', 'kind', 'function'),
              ('function-mode', 'binding', 'mode', 'arm'), ('wrong-CPU', 'binding', 'processor', 'arm7'),
              ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
              ('invented-full-extent', 'case', 'completeObjectExtent', 816), ('invented-storage', 'case', 'externalStorageCredit', 2)]
    for case in value['cases']:
        row = next(r for r in rows if r['address'] == case['caller'])
        relocation = next(r for r in row['relocations'] if r['symbol'] == case['symbol'])
        binding = row['nativeSymbolEntries'][case['symbol']]
        changes = list(common)
        if case['symbol'] == 'native_data_020dbc18':
            changes += [('wrong-index-min', 'case', 'indexMinimum', 391), ('wrong-index-max', 'case', 'indexMaximum', 408),
                        ('wrong-element-width', 'case', 'elementWidth', 1), ('wrong-index-stride', 'case', 'indexStride', 4),
                        ('wrong-initialized-prefix', 'case', 'minimumInitializedPrefix', 814), ('wrong-metadata-offset', 'case', 'metadataFieldOffset', 2),
                        ('wrong-metadata-width', 'case', 'metadataFieldWidth', 1), ('wrong-nibble-shift', 'case', 'metadataNibbleShift', 8),
                        ('wrong-nibble-width', 'case', 'metadataNibbleWidth', 8)]
        for label, owner, key, wrong in changes:
            items = {name: copy.deepcopy(obj) for name, obj in [('case', case), ('row', row), ('relocation', relocation), ('binding', binding)]}
            items[owner][key] = wrong
            try:
                validate(items['case'], items['row'], items['relocation'], items['binding'], image, inventory, loads)
            except ValueError as error:
                checks.append(dict(caller=case['caller'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid UI table/context data witness accepted')
        changed = bytearray(image)
        changed[int(case['literalPool'], 0) - 0x02000000] ^= 4
        for label, raw, inv, records in [('changed-original-literal', bytes(changed), inventory, loads),
                                         ('missing-original-data', image, inventory.replace(case['originalInventoryRecord'], ''), loads),
                                         ('missing-original-load', image, inventory, loads.replace(case['originalLoadRecord'], ''))]:
            try:
                validate(case, row, relocation, binding, raw, inv, records)
            except ValueError as error:
                checks.append(dict(caller=case['caller'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed original UI data evidence accepted')
    return dict(status='passed', negativeCases=checks, sourceOrDataStorageCredit=0, ordinaryBranchVerifierUnchanged=True)
