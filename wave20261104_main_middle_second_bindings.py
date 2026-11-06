import copy
import struct
from project import ROOT, read_json, sha256
from wave20261104_main_command_forward_bindings import validate as common_validate
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/second/data-inputs.json'
INPUT_SHA = '6f980868156078933d93f7fa1bc0c853b4abb282eb412691d7724e7eaf4b3210'


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Original byte/record data contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'relocations', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Original data inventory/image changed')
    return value


def validate(case, row, relocation, binding, image, inventory, loads):
    result = common_validate(case, row, relocation, binding, image, inventory, loads)
    if case.get('typedAccesses') != [] or case.get('completeObjectExtent') is not None or case.get('externalStorageCredit') != 0:
        raise ValueError('Unknown complete BSS allocation or storage credit claimed')
    start = int(row['address'], 0)
    if start == 0x02047ac0:
        expected = dict(minimumPrefixBytes=130, indexBoundExclusive=128, maximumByteOffset=129, accessWidth=1)
        role, symbol = 'byte-stream-prefix', 'native_data_020fb264'
        words = {0x08: 0xe35a0080, 0x20: 0xe7d7100a, 0x30: 0x05d90001,
                 0x44: 0xe5d90001, 0x5c: 0xe5d90002, 0x94: 0xe5d90000, 0xbc: 0xe35a0080}
    elif start in [0x0204837c, 0x020483c0]:
        expected = dict(recordStride=0x3744, wordOffset=0x3544, words=128, accessWidth=4,
                        counterBits=16, counterSigned=True, recordCount=None)
        role, symbol = 'word-clear-record', 'native_data_020fbae8'
        words = {0x10: 0xe02e2190, 0x20: 0xe1a01800, 0x24: 0xe2820a03,
                 0x28: 0xe1a0c841, 0x2c: 0xe5803544, 0x30: 0xe35c0080, 0x40: 0x3744}
    else:
        raise ValueError('No byte/record data role for this caller')
    if case['symbol'] != symbol or case['dataRole'] != role or case.get('layout') != expected:
        raise ValueError('Original data base, field, width, stride, bound or prefix differs')
    for offset, expected_word in words.items():
        at = start - 0x02000000 + offset
        if struct.unpack('<I', image[at:at + 4])[0] != expected_word:
            raise ValueError('Actual original indexed access, signed counter, bound or stride differs')
    return dict(result, dataRole=role, measuredTypedLayout=expected, originalInstructionWords=words,
                completeObjectExtent=None, externalStorageCredit=0)


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
            raise ValueError('No exact original data caller/symbol witness')
        witnesses.append(validate(case, row, relocation, bindings[relocation['symbol']], image, inventory, loads))
    return dict(result, originalDataLoadWitnesses=witnesses, externalStorageCredit=0,
                dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA))


def negative_controls(rows):
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    checks = []
    for case in value['cases']:
        row = next(r for r in rows if r['address'] == case['caller'])
        relocation = next(r for r in row['relocations'] if r['symbol'] == case['symbol'])
        binding = row['nativeSymbolEntries'][case['symbol']]
        changes = [('wrong-origin', 'relocation', 'offset', 4), ('nonzero-addend', 'relocation', 'addend', 4),
                   ('wrong-base', 'binding', 'address', hex(int(case['target'], 0) + 4)),
                   ('function-kind', 'binding', 'kind', 'function'), ('function-mode', 'binding', 'mode', 'arm'),
                   ('wrong-CPU', 'binding', 'processor', 'arm7'), ('wrong-program', 'binding', 'program', 'child'),
                   ('wrong-module', 'binding', 'module', 'ov000'), ('invented-extent', 'case', 'completeObjectExtent', 130)]
        for key, number in case['layout'].items():
            wrong = dict(case['layout'], **{key: 0 if number is None else not number if isinstance(number, bool) else number + 1})
            changes.append(('wrong-layout-' + key, 'case', 'layout', wrong))
        for label, owner, key, wrong in changes:
            items = {name: copy.deepcopy(obj) for name, obj in [('case', case), ('row', row), ('relocation', relocation), ('binding', binding)]}
            items[owner][key] = wrong
            try:
                validate(items['case'], items['row'], items['relocation'], items['binding'], image, inventory, loads)
            except ValueError as error:
                checks.append(dict(caller=case['caller'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid data role accepted: ' + label)
        changed = bytearray(image)
        changed[int(case['literalPool'], 0) - 0x02000000] ^= 4
        for label, raw, inv, records in [('wrong-source-literal', bytes(changed), inventory, loads),
                                         ('missing-storage-inventory', image, inventory.replace(case['originalInventoryRecord'], ''), loads),
                                         ('missing-load-record', image, inventory, loads.replace(case['originalLoadRecord'], ''))]:
            try:
                validate(case, row, relocation, binding, raw, inv, records)
            except ValueError as error:
                checks.append(dict(caller=case['caller'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed native byte/record evidence accepted')
    return dict(status='passed', negativeCases=checks, sourceOrDataStorageCredit=0, ordinaryBranchVerifierUnchanged=True)
