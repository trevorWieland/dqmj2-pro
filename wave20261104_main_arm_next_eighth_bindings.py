import copy
import struct
import hashlib
from link_runtime_unit import verify_binding
from project import ROOT, read_json, sha256
from wave20261104_main_command_forward_bindings import validate as common_validate
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/main-arm-next/eighth/data-inputs.json'
INPUT_SHA = '77a8ef74690614933636ee0fdca5fe13d032f23f88dddcdbf3a3c9a0e2b91366'


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
    if row['address'] != '0x20294cc' or row['bytes'] != 332 or case['symbol'] not in ['native_data_020ee04c', 'native_data_020edf90'] or case['typedAccesses'] != []:
        raise ValueError('Only the measured matrix destination/graphics flags caller is qualified')
    keys = ['matrixBase', 'graphicsStateBase', 'matrixAliasOffset', 'matrixBytes', 'flagsOffset', 'flagsWidth', 'flagsMask', 'minimumStatePrefix', 'completeObjectExtents', 'externalStorageCredit']
    expected = ['0x20ee04c', '0x20edf90', 188, 36, 252, 4, 164, 256, None, 0]
    if [case.get(k) for k in keys] != expected or int(case['matrixBase'], 0) != int(case['graphicsStateBase'], 0) + case['matrixAliasOffset']:
        raise ValueError('Measured alias/flags/width/prefix or unknown storage extent differs')
    for target in [0x020ee04c, 0x020edf90]:
        if 'data_%08x kind:bss addr:0x%08x' % (target, target) not in inventory.splitlines():
            raise ValueError('Both original overlapping BSS view identities are required')
    words = {108: 0xe59f10d0, 112: 0xe2850034, 116: 0xebff7df1, 120: 0xe59f10c8, 124: 0xe2850010, 128: 0xe59120fc, 132: 0xe3c220a4, 136: 0xe58120fc}
    for offset, word in words.items():
        if struct.unpack_from('<I', image, 0x294cc + offset)[0] != word:
            raise ValueError('Original matrix source/copy destination/flags load-mask-store differs')
    return dict(result, measuredFields=dict(zip(keys, expected)), originalInstructionWords=words, completeObjectExtents=None, externalStorageCredit=0)


def verify_original(row, bindings):
    data = [r for r in row['relocations'] if r['type'] == 2]
    result = branch_verify(dict(row, relocations=[r for r in row['relocations'] if r['type'] != 2]), bindings)
    if not data:
        return result
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    helper = value['copyHelper']
    validate_copy_helper(helper, image, inventory)
    witnesses = []
    for relocation in data:
        case = next((c for c in value['cases'] if c['caller'] == row['address'] and c['symbol'] == relocation['symbol']), None)
        if case is None:
            raise ValueError('No exact original current-pointer caller/symbol witness')
        witnesses.append(validate(case, row, relocation, bindings[relocation['symbol']], image, inventory, loads))
    return dict(result, originalDataLoadWitnesses=witnesses, externalStorageCredit=0,
                dataQualificationInput=dict(path=INPUT.relative_to(ROOT).as_posix(), sha256=INPUT_SHA))


def validate_copy_helper(helper, image, inventory):
    if tuple(helper.get(k) or '' for k in ['program', 'processor', 'module', 'mode', 'kind']) != ('', 'arm9', 'main', 'arm', 'function') or helper['address'] != '0x2008d0c' or helper['bytes'] != 28:
        raise ValueError('Inspected36-byte copy helper namespace/extent differs')
    if helper['sourceRecord'] != 'func_02008d0c kind:function(arm,size=0x1c) addr:0x02008d0c' or helper['sourceRecord'] not in inventory.splitlines():
        raise ValueError('Inspected copy helper original function inventory missing')
    expected_words = [0xe8b0100c, 0xe8a1100c] * 3 + [0xe12fff1e]
    if helper['instructionWords'] != expected_words or list(struct.unpack_from('<7I', image, 0x8d0c)) != expected_words or hashlib.sha256(image[0x8d0c:0x8d28]).hexdigest() != helper['targetSha256']:
        raise ValueError('Original three12-byte LDM/STM groups and complete helper body differ')
    if not helper['readOnlyInspection'] or helper['nativeExecution'] != 0 or helper['sourceCredit'] != 0:
        raise ValueError('Read-only helper observation cannot become execution/source credit')
    verify_binding('native_fn_02008d0c', helper)


def negative_controls(rows):
    value = frozen_inputs()
    image = (ROOT / value['image']['path']).read_bytes()
    inventory = (ROOT / value['inventory']['path']).read_text()
    loads = (ROOT / value['relocations']['path']).read_text()
    results = []
    changes = [('wrong-origin', 'relocation', 'offset', 4), ('folded-alias-addend', 'relocation', 'addend', 188),
               ('wrong-base', 'binding', 'address', '0x20ee050'), ('function-kind', 'binding', 'kind', 'function'),
               ('function-mode', 'binding', 'mode', 'arm'), ('wrong-CPU', 'binding', 'processor', 'arm7'),
               ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
               ('wrong-matrix-base', 'case', 'matrixBase', '0x20ee050'), ('wrong-state-base', 'case', 'graphicsStateBase', '0x20edf94'),
               ('wrong-alias-offset', 'case', 'matrixAliasOffset', 184), ('wrong-matrix-size', 'case', 'matrixBytes', 32),
               ('wrong-flags-offset', 'case', 'flagsOffset', 248), ('wrong-flags-width', 'case', 'flagsWidth', 2),
               ('wrong-flags-mask', 'case', 'flagsMask', 32), ('wrong-state-prefix', 'case', 'minimumStatePrefix', 252),
               ('invented-complete-extents', 'case', 'completeObjectExtents', [36, 256]), ('invented-storage', 'case', 'externalStorageCredit', 36)]
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
                raise ValueError('Invalid matrix/flags original-data qualification accepted')
        changed = bytearray(image)
        changed[int(case['literalPool'], 0) - 0x02000000] ^= 4
        for label, raw, inv, records in [('changed-original-literal', bytes(changed), inventory, loads),
                                         ('missing-matrix-view', image, inventory.replace('data_020ee04c kind:bss addr:0x020ee04c', ''), loads),
                                         ('missing-state-view', image, inventory.replace('data_020edf90 kind:bss addr:0x020edf90', ''), loads),
                                         ('missing-load-record', image, inventory, loads.replace(case['originalLoadRecord'], ''))]:
            try:
                validate(case, row, relocation, binding, raw, inv, records)
            except ValueError as error:
                results.append(dict(symbol=case['symbol'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Changed overlapping original BSS qualification accepted')
    helper = value['copyHelper']
    for label, key, wrong in [('copy-wrong-CPU', 'processor', 'arm7'), ('copy-wrong-mode', 'mode', 'thumb'),
                              ('copy-wrong-address', 'address', '0x2008d10'), ('copy-short-body', 'bytes', 24),
                              ('copy-wrong-hash', 'targetSha256', '0' * 64), ('copy-code-as-data', 'kind', 'data'),
                              ('copy-invented-execution', 'nativeExecution', 1), ('copy-invented-source-credit', 'sourceCredit', 28)]:
        bad = copy.deepcopy(helper)
        bad[key] = wrong
        try:
            validate_copy_helper(bad, image, inventory)
        except ValueError as error:
            results.append(dict(case=label, rejected=True, reason=str(error)))
        else:
            raise ValueError('Invalid read-only copy-helper witness accepted')
    changed = bytearray(image)
    changed[0x8d0c] ^= 1
    try:
        validate_copy_helper(helper, bytes(changed), inventory)
    except ValueError as error:
        results.append(dict(case='changed-actual-copy-helper-body', rejected=True, reason=str(error)))
    else:
        raise ValueError('Changed actual copy-helper code accepted')
    return dict(status='passed', negativeCases=results, sourceOrDataStorageCredit=0, ordinaryBranchVerifierUnchanged=True)
