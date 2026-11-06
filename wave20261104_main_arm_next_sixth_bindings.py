import copy
import struct
from project import ROOT, read_json, sha256
from wave20261104_main_command_forward_bindings import validate as common_validate
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/sixth/data-inputs.json'
INPUT_SHA = '9fbff7a6ff6e976ad4c9997b680aa3f8cfb77662222416e52d0c49c808ffa6ca'


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
    result = common_validate(case, row, relocation, binding, image, inventory, loads)
    fields = {0x02038d88: 8, 0x02038dec: 12, 0x02038e50: 16, 0x02038eb4: 20, 0x02038f18: 36, 0x02038f7c: 24, 0x02038fe0: 32}
    start = int(row['address'], 0)
    if start not in fields or case['symbol'] != 'native_data_020f4c44' or case['typedAccesses'] != []:
        raise ValueError('Only the measured manager-pointer table lookup family is qualified')
    names = ['globalPointerWidth', 'managerFieldOffset', 'managerFieldWidth', 'managerMinimumPrefix', 'blobTableFieldOffset', 'blobTableFieldWidth', 'blobMinimumPrefix', 'tableCountWidth', 'tableItemOffset', 'tableItemStride', 'completeObjectExtents', 'externalStorageCredit']
    expected = [4, 140, 4, 144, fields[start], 4, 40, 4, 4, 4, None, 0]
    if [case.get(k) for k in names] != expected:
        raise ValueError('Measured manager/blob/count/item fields or unknown extent/zero storage differs')
    words = {4: 0xe5913000, 8: 0xe593208c, 12: 0xe5921000 | fields[start], 40: 0xe3500000, 44: 0xb3a00000, 48: 0xb12fff1e, 52: 0xe5921000, 56: 0xe1500001, 60: 0x23a00000, 64: 0x212fff1e, 68: 0xe0820100, 72: 0xe5901004, 76: 0xe593008c}
    for offset, word in words.items():
        if struct.unpack_from('<I', image, start - 0x02000000 + offset)[0] != word:
            raise ValueError('Original manager field/count guard/item stride/load sequence differs')
    return dict(result, measuredFields=dict(zip(names, expected)), originalInstructionWords=words, completeObjectExtents=None, externalStorageCredit=0)


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
    results = []
    changes = [('wrong-origin', 'relocation', 'offset', 4), ('folded-addend', 'relocation', 'addend', 4),
               ('wrong-global-address', 'binding', 'address', '0x20f4c48'), ('function-kind', 'binding', 'kind', 'function'),
               ('function-mode', 'binding', 'mode', 'arm'), ('wrong-CPU', 'binding', 'processor', 'arm7'),
               ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
               ('wrong-manager-field', 'case', 'managerFieldOffset', 136), ('wrong-manager-width', 'case', 'managerFieldWidth', 2),
               ('wrong-manager-prefix', 'case', 'managerMinimumPrefix', 140), ('wrong-global-width', 'case', 'globalPointerWidth', 2),
               ('wrong-blob-field', 'case', 'blobTableFieldOffset', 0), ('wrong-blob-width', 'case', 'blobTableFieldWidth', 2),
               ('wrong-blob-prefix', 'case', 'blobMinimumPrefix', 36), ('wrong-count-width', 'case', 'tableCountWidth', 2),
               ('wrong-item-offset', 'case', 'tableItemOffset', 0), ('wrong-item-stride', 'case', 'tableItemStride', 2),
               ('invented-extents', 'case', 'completeObjectExtents', [4, 144, 40]), ('invented-storage', 'case', 'externalStorageCredit', 4)]
    for case in value['cases']:
        row = next(r for r in rows if r['address'] == case['caller'])
        relocation = next(r for r in row['relocations'] if r['symbol'] == case['symbol'])
        binding = row['nativeSymbolEntries'][case['symbol']]
        for label, owner, key, wrong in changes:
            items = {name: copy.deepcopy(obj) for name, obj in [('case', case), ('row', row), ('relocation', relocation), ('binding', binding)]}
            items[owner][key] = wrong
            try:
                validate(items['case'], items['row'], items['relocation'], items['binding'], image, inventory, loads)
            except ValueError as error:
                results.append(dict(caller=case['caller'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid manager/table load accepted: ' + label)
        changed = bytearray(image)
        changed[int(case['literalPool'], 0) - 0x02000000] ^= 4
        for label, raw, inv, records in [('changed-source-literal', bytes(changed), inventory, loads),
                                         ('missing-global-inventory', image, inventory.replace(case['originalInventoryRecord'], ''), loads),
                                         ('missing-load-record', image, inventory, loads.replace(case['originalLoadRecord'], ''))]:
            try:
                validate(case, row, relocation, binding, raw, inv, records)
            except ValueError as error:
                results.append(dict(caller=case['caller'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed manager/table original provenance accepted')
    return dict(status='passed', negativeCases=results, sourceOrDataStorageCredit=0, ordinaryBranchVerifierUnchanged=True)

