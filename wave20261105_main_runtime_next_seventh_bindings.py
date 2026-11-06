import copy
import struct
from project import ROOT, read_json, sha256
from wave20261104_main_tail_bindings import verify_original as branch_verify
from wave20261104_main_command_forward_bindings import validate as common_validate

INPUT = ROOT / 'evidence/lanes/parallel-wave20261105/main-runtime-next/seventh/data-inputs.json'
INPUT_SHA = 'c6f8696d2bd5c820d44e92670931d8047a8016e312e178bb14e3557fcdefd409'


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
    result = common_validate(case, row, relocation, binding, image, inventory, loads)
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
