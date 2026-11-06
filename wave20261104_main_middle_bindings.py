import copy
import struct
from project import ROOT, read_json, sha256
from wave20261104_main_command_forward_bindings import validate as common_validate
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/first/data-inputs.json'
INPUT_SHA = '10c00fd706464145cd26261015aa4a79b055298fc5d1168f0a351107b9237ff1'


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Original halfword data contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'relocations', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Original data inventory/image changed')
    return value


def validate(case, row, relocation, binding, image, inventory, loads):
    common = dict(case, typedAccesses=[])
    result = common_validate(common, row, relocation, binding, image, inventory, loads)
    if case.get('completeObjectExtent') is not None or case.get('externalStorageCredit') != 0:
        raise ValueError('Original BSS object allocation or storage credit is unproved')
    if case['symbol'] == 'native_data_020fb264':
        expected = dict(instruction='0x2047434', instructionBytesHex='b008d1e1', operation='unsigned-halfword-read',
                        width=2, offset=128, minimumPrefixBytes=130, baseRegister=1, destinationRegister=0)
        if case.get('dataRole') != 'cursor-prefix' or case.get('typedAccesses') != [expected] or 'pointerFormation' in case:
            raise ValueError('Measured cursor prefix, offset, width or extent differs')
        at = int(expected['instruction'], 0) - 0x02000000
        body = image[at:at + 4]
        word = struct.unpack('<I', body)[0]
        offset = ((word >> 8 & 15) << 4) | (word & 15)
        if body.hex() != expected['instructionBytesHex'] or word & 0xfffff0f0 != 0xe1d100b0 or offset != 128:
            raise ValueError('Actual original unsigned LDRH field instruction differs')
    elif case['symbol'] == 'native_data_020fae64':
        expected = dict(instruction='0x2047448', instructionBytesHex='80008ce0', operation='halfword-index-address',
                        elementBytes=2, baseRegister=12, indexRegister=0, destinationRegister=0)
        if case.get('dataRole') != 'output-pointer' or case.get('typedAccesses') != [] or case.get('pointerFormation') != expected:
            raise ValueError('Measured incomplete-array pointer formation differs')
        at = int(expected['instruction'], 0) - 0x02000000
        if image[at:at + 4].hex() != expected['instructionBytesHex']:
            raise ValueError('Original scaled pointer addition differs')
    else:
        raise ValueError('No qualified data role for this original symbol')
    return dict(result, typedAccesses=case['typedAccesses'], dataRole=case['dataRole'],
                pointerFormation=case.get('pointerFormation'), completeObjectExtent=None, externalStorageCredit=0)


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
            raise ValueError('No measured data contract for exact caller/symbol')
        witnesses.append(validate(case, row, relocation, bindings[relocation['symbol']], image, inventory, loads))
    return dict(result, originalDataLoadWitnesses=witnesses, externalStorageCredit=0,
                dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA))


def negative_controls(rows):
    value = frozen_inputs()
    case = value['cases'][0]
    row = next(r for r in rows if r['address'] == case['caller'])
    relocation = next(r for r in row['relocations'] if r['symbol'] == case['symbol'])
    binding = row['nativeSymbolEntries'][case['symbol']]
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    checks = []
    changes = [('wrong-origin', 'relocation', 'offset', 8), ('wrong-base', 'binding', 'address', '0x20fb2e4'),
               ('field-folded-into-addend', 'relocation', 'addend', 128), ('function-kind', 'binding', 'kind', 'function'),
               ('function-mode', 'binding', 'mode', 'arm'), ('wrong-CPU', 'binding', 'processor', 'arm7'),
               ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
               ('missing-field-proof', 'case', 'typedAccesses', []), ('invented-object-extent', 'case', 'completeObjectExtent', 130)]
    for key, wrong in [('offset', 130), ('width', 4), ('minimumPrefixBytes', 128), ('minimumPrefixBytes', 132)]:
        changes.append(('wrong-field-' + key + '-' + str(wrong), 'case', 'typedAccesses', [dict(case['typedAccesses'][0], **{key: wrong})]))
    for label, owner, key, wrong in changes:
        items = {name: copy.deepcopy(obj) for name, obj in [('case', case), ('row', row), ('relocation', relocation), ('binding', binding)]}
        items[owner][key] = wrong
        try:
            validate(items['case'], items['row'], items['relocation'], items['binding'], image, inventory, loads)
        except ValueError as error:
            checks.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Invalid halfword data contract accepted: ' + label)
    changed = bytearray(image)
    changed[int(case['literalPool'], 0) - 0x02000000] ^= 4
    for label, raw, inv, records in [('wrong-source-literal', bytes(changed), inventory, loads),
                                     ('missing-storage-inventory', image, inventory.replace(case['originalInventoryRecord'], ''), loads),
                                     ('missing-load-record', image, inventory, loads.replace(case['originalLoadRecord'], ''))]:
        try:
            validate(case, row, relocation, binding, raw, inv, records)
        except ValueError as error:
            checks.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Changed original evidence accepted: ' + label)
    return dict(status='passed', negativeCases=checks, sourceOrDataStorageCredit=0, ordinaryBranchVerifierUnchanged=True,
                reusedFrozenCommonDataValidator='wave20261104_main_command_forward_bindings.validate')
