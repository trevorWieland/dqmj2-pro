import copy
import struct
from project import ROOT, read_json, sha256
from wave20261104_main_tail_bindings import verify_original as branch_verify
from link_runtime_unit import verify_binding
import hashlib

INPUT = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/eleventh/data-inputs.json'
INPUT_SHA = '812dcd157dd1924e327663c99effaf9c44b446fe40ce72f44466ca37babc8a1a'


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Original collection data contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'relocations', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Original collection inventory/image changed')
    return value


def validate(case, row, relocation, binding, image, inventory, loads):
    if tuple(row.get(k) or '' for k in ['program', 'processor', 'module', 'mode']) != ('', 'arm9', 'main', 'arm'):
        raise ValueError('Readonly table caller namespace differs')
    if tuple(binding.get(k) or '' for k in ['program', 'processor', 'module', 'mode', 'kind']) != ('', 'arm9', 'main', 'data', 'data'):
        raise ValueError('Readonly table is not original main ARM9 data')
    if (row['address'], row['bytes'], row['targetSha256']) != (case['caller'], case['bytes'], case['callerSha256']):
        raise ValueError('Exact readonly table caller differs')
    if (relocation['symbol'], relocation['offset'], relocation['type'], relocation['addend']) != (case['symbol'], case['offset'], 2, 0):
        raise ValueError('Readonly table ABS32 origin/type/addend differs')
    target = int(case['target'], 0)
    origin = int(row['address'], 0) + relocation['offset']
    if int(relocation['target'], 0) != target or int(binding['address'], 0) != target or origin != int(case['literalPool'], 0):
        raise ValueError('Readonly table target/origin differs')
    expected_record = 'data_%08x kind:data(any) addr:0x%08x' % (target, target)
    expected_load = 'from:0x%08x kind:load to:0x%08x module:main' % (origin, target)
    if case['originalInventoryRecord'] != expected_record or expected_record not in inventory.splitlines() or case['originalLoadRecord'] != expected_load or expected_load not in loads.splitlines():
        raise ValueError('Exact original raw readonly table inventory/load missing')
    start = int(row['address'], 0) - 0x02000000
    if hashlib.sha256(image[start:start + row['bytes']]).hexdigest() != case['callerSha256']:
        raise ValueError('Whole original readonly lookup caller changed')
    literal = image[origin - 0x02000000:origin - 0x02000000 + 4]
    if literal.hex() != case['literalWordHex'] or struct.unpack('<I', literal)[0] != target:
        raise ValueError('Original readonly table literal changed')
    verify_binding(relocation['symbol'], binding)
    result = dict(symbol=case['symbol'], origin=hex(origin), target=case['target'], originalInventoryRecord=expected_record, originalLoadRecord=expected_load, originalDataStorageCredit=0)
    original = next((x for x in frozen_inputs()['cases'] if (x['caller'], x['symbol']) == (case['caller'], case['symbol'])), None)
    if original is None or case != original or case['typedAccesses'] or case['completeObjectExtent'] is not None or case['externalStorageCredit'] != 0:
        raise ValueError('Exact prefix/layout/zero-credit collection contract differs')
    start = int(row['address'], 0) - 0x02000000
    for at, word in case['instructionWords'].items():
        if struct.unpack_from('<I', image, start + int(at))[0] != word:
            raise ValueError('Original paired-halfword/byte/stride/field instruction differs')
    return dict(result, minimumPrefix=case['minimumPrefix'], layout=case['layout'], instructionWords=case['instructionWords'], completeObjectExtent=None)


def verify_original(row, bindings):
    result = branch_verify(dict(row, relocations=[r for r in row['relocations'] if r['type'] != 2]), bindings)
    value = frozen_inputs()
    image, inventory, loads = [(ROOT / value[k]['path']).read_bytes() if k == 'image' else (ROOT / value[k]['path']).read_text() for k in ['image', 'inventory', 'relocations']]
    expected = [x for x in value['cases'] if x['caller'] == row['address']]
    data = [r for r in row['relocations'] if r['type'] == 2]
    if len(expected) != len(data):
        raise ValueError('All exact original collection data origins are required')
    witnesses = []
    for rel in data:
        case = next((x for x in expected if x['symbol'] == rel['symbol']), None)
        if case is None:
            raise ValueError('Unqualified collection data input')
        witnesses.append(validate(case, row, rel, bindings[rel['symbol']], image, inventory, loads))
    return dict(result, originalDataLoadWitnesses=witnesses, externalStorageCredit=0, dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA))


def negative_controls(rows):
    value = frozen_inputs()
    image, inventory, loads = [(ROOT / value[k]['path']).read_bytes() if k == 'image' else (ROOT / value[k]['path']).read_text() for k in ['image', 'inventory', 'relocations']]
    results = []
    for case in value['cases']:
        row = next(x for x in rows if x['address'] == case['caller'])
        rel = next(x for x in row['relocations'] if x['symbol'] == case['symbol'])
        binding = row['nativeSymbolEntries'][case['symbol']]
        changes = [('wrong-origin', 'rel', 'offset', rel['offset'] - 4), ('wrong-addend', 'rel', 'addend', 4),
                   ('wrong-base', 'binding', 'address', hex(int(binding['address'], 0) + 4)), ('function-kind', 'binding', 'kind', 'function'),
                   ('function-mode', 'binding', 'mode', 'arm'), ('wrong-CPU', 'binding', 'processor', 'arm7'),
                   ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
                   ('wrong-prefix', 'case', 'minimumPrefix', case['minimumPrefix'] + 1), ('wrong-layout', 'case', 'layout', {}),
                   ('invented-extent', 'case', 'completeObjectExtent', case['minimumPrefix']), ('invented-storage', 'case', 'externalStorageCredit', 1)]
        for label, owner, key, wrong in changes:
            items = {k: copy.deepcopy(v) for k, v in [('case', case), ('row', row), ('rel', rel), ('binding', binding)]}
            items[owner][key] = wrong
            try:
                validate(items['case'], items['row'], items['rel'], items['binding'], image, inventory, loads)
            except ValueError as error:
                results.append(dict(caller=row['address'], symbol=case['symbol'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid collection data contract accepted')
        changed = bytearray(image)
        changed[int(case['literalPool'], 0) - 0x02000000] ^= 4
        for label, raw, inv, records in [('changed-original-literal', bytes(changed), inventory, loads), ('missing-inventory', image, inventory.replace(case['originalInventoryRecord'], ''), loads), ('missing-load', image, inventory, loads.replace(case['originalLoadRecord'], ''))]:
            try:
                validate(case, row, rel, binding, raw, inv, records)
            except ValueError as error:
                results.append(dict(caller=row['address'], symbol=case['symbol'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed original collection provenance accepted')
    return dict(status='passed', negativeCases=results, sourceOrStorageCredit=0)
