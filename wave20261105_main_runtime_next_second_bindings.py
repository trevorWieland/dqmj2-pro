import copy
import hashlib
import struct
from project import ROOT, read_json, sha256
from link_runtime_unit import verify_binding
from wave20261104_main_tail_bindings import verify_original as branch_verify
from wave20261104_main_command_forward_bindings import validate as common_validate

INPUT = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/second/data-inputs.json'
INPUT_SHA = '2637b798f6fa9990e5b4b19fed3ac81427d225679cf7cf0d3bbe490b88d2bafe'


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Frozen ordered-state data contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'relocations', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Original ordered-state inventory/image changed')
    return value


def validate(case, row, relocation, binding, image, inventory, loads):
    if case.get('minimumPrefix') != 8 or case.get('completeObjectExtent') is not None or case.get('externalStorageCredit') != 0 or case['typedAccesses'] != []:
        raise ValueError('Only8-byte state prefixes and zero storage credit are qualified')
    if case['symbol'] == 'native_data_021c36fc':
        result = common_validate(case, row, relocation, binding, image, inventory, loads)
        if row['address'] != '0x2067380' or row['bytes'] != 552 or case['fieldWidths'] != {'0': 1, '4': 4}:
            raise ValueError('Original state byte/word fields differ')
        return dict(result, minimumPrefix=8, completeObjectExtent=None, fieldWidths=case['fieldWidths'], originalStorageCredit=0)
    if tuple(row.get(k) or '' for k in ['program', 'processor', 'module', 'mode']) != ('', 'arm9', 'main', 'arm') or tuple(case.get(k) or '' for k in ['program', 'processor', 'module', 'mode']) != ('', 'arm9', 'main', 'arm'):
        raise ValueError('Ordered state caller namespace differs')
    if (row['address'], row['bytes'], row['targetSha256']) != (case['caller'], case['bytes'], case['callerSha256']) or row['address'] != '0x2067380' or row['bytes'] != 552:
        raise ValueError('Exact552-byte original ordered state caller differs')
    if case['symbol'] != 'native_data_020de23c' or case['fieldWidths'] != {'0': 4, '4': 4}:
        raise ValueError('Only two measured initialized state words are qualified')
    if tuple(binding.get(k) or '' for k in ['program', 'processor', 'module', 'mode', 'kind']) != ('', 'arm9', 'main', 'data', 'data'):
        raise ValueError('Initialized state confused with function/other namespace')
    if (relocation['symbol'], relocation['offset'], relocation['type'], relocation['addend']) != (case['symbol'], 548, 2, 0) or case['offset'] != 548:
        raise ValueError('Original initialized-state ABS32 origin/addend differs')
    if case['target'] != '0x20de23c' or int(binding['address'], 0) != 0x020de23c or int(relocation['target'], 0) != 0x020de23c or case['literalPool'] != '0x20675a4':
        raise ValueError('Original initialized-state address/pool differs')
    record = 'data_020de23c kind:data(any) addr:0x020de23c'
    load = 'from:0x020675a4 kind:load to:0x020de23c module:main'
    if case['originalInventoryRecord'] != record or record not in inventory.splitlines() or case['originalLoadRecord'] != load or load not in loads.splitlines():
        raise ValueError('Exact original initialized state inventory/load missing')
    if hashlib.sha256(image[0x67380:0x675a8]).hexdigest() != case['callerSha256'] or image[0x675a4:0x675a8] != struct.pack('<I', 0x020de23c) or case['literalWordHex'] != image[0x675a4:0x675a8].hex():
        raise ValueError('Original ordered state caller/literal changed')
    words = {12: 0xe5912004, 36: 0xe5903004, 140: 0xe5d12000, 280: 0xe5900000}
    if any(struct.unpack_from('<I', image, 0x67380 + at)[0] != word for at, word in words.items()):
        raise ValueError('Original state word/choice-byte/load fields differ')
    verify_binding(relocation['symbol'], binding)
    return dict(symbol=case['symbol'], originalInventoryRecord=record, originalLoadRecord=load, originalInstructionWords=words,
                fieldWidths=case['fieldWidths'], minimumPrefix=8, completeObjectExtent=None, originalStorageCredit=0)


def verify_original(row, bindings):
    result = branch_verify(dict(row, relocations=[r for r in row['relocations'] if r['type'] != 2]), bindings)
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    witnesses = []
    for relocation in [r for r in row['relocations'] if r['type'] == 2]:
        case = next((c for c in value['cases'] if c['symbol'] == relocation['symbol'] and c['caller'] == row['address']), None)
        if case is None:
            raise ValueError('No exact ordered-state original data witness')
        witnesses.append(validate(case, row, relocation, bindings[relocation['symbol']], image, inventory, loads))
    if len(witnesses) != 2:
        raise ValueError('Both distinct original state storage bindings are required')
    return dict(result, originalDataLoadWitnesses=witnesses, externalStorageCredit=0,
                dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA))


def negative_controls(rows):
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    results = []
    changes = [('wrong-origin', 'relocation', 'offset', 4), ('folded-field-addend', 'relocation', 'addend', 4),
               ('wrong-base', 'binding', 'address', '0x20de240'), ('function-kind', 'binding', 'kind', 'function'),
               ('function-mode', 'binding', 'mode', 'arm'), ('wrong-CPU', 'binding', 'processor', 'arm7'),
               ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
               ('wrong-prefix', 'case', 'minimumPrefix', 4), ('wrong-field-widths', 'case', 'fieldWidths', {'0': 2, '4': 2}),
               ('invented-complete-extent', 'case', 'completeObjectExtent', 8), ('invented-storage', 'case', 'externalStorageCredit', 8)]
    for case in value['cases']:
        row = rows[0]
        relocation = next(r for r in row['relocations'] if r['symbol'] == case['symbol'])
        binding = row['nativeSymbolEntries'][case['symbol']]
        for label, owner, key, wrong in changes:
            items = {name: copy.deepcopy(obj) for name, obj in [('case', case), ('row', row), ('relocation', relocation), ('binding', binding)]}
            items[owner][key] = wrong
            try:
                validate(items['case'], items['row'], items['relocation'], items['binding'], image, inventory, loads)
            except ValueError as error:
                results.append(dict(symbol=case['symbol'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid ordered-state storage witness accepted')
        changed = bytearray(image)
        changed[int(case['literalPool'], 0) - 0x02000000] ^= 4
        for label, raw, inv, records in [('changed-original-literal', bytes(changed), inventory, loads),
                                         ('missing-original-storage', image, inventory.replace(case['originalInventoryRecord'], ''), loads),
                                         ('missing-original-load', image, inventory, loads.replace(case['originalLoadRecord'], ''))]:
            try:
                validate(case, row, relocation, binding, raw, inv, records)
            except ValueError as error:
                results.append(dict(symbol=case['symbol'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed ordered-state source provenance accepted')
    return dict(status='passed', negativeCases=results, sourceOrDataStorageCredit=0, originalBranchVerifierUnchanged=True)
