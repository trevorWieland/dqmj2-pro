import copy
import struct
from project import ROOT, read_json, sha256
from wave20261104_main_command_forward_bindings import validate as common_validate
from wave20261104_main_tail_bindings import verify_original as branch_verify

INPUT = ROOT / 'evidence/lanes/parallel-wave20261104/main-command-middle/fourth/data-inputs.json'
INPUT_SHA = '227800ea14e6bb8c799a3ac77c3de4775a4b72bd4eea767ad432cc649aedcf5d'
CALLERS = [0x02048d14, 0x02048d54, 0x02048d94, 0x02048dd4]


def frozen_inputs():
    if sha256(INPUT) != INPUT_SHA:
        raise ValueError('Original signed-byte data contract changed')
    value = read_json(INPUT)
    for key in ['inventory', 'relocations', 'image']:
        pin = value[key]
        if sha256(ROOT / pin['path']) != pin['sha256']:
            raise ValueError('Original data inventory/image changed')
    return value


def validate(case, row, relocation, binding, image, inventory, loads):
    result = common_validate(case, row, relocation, binding, image, inventory, loads)
    start = int(row['address'], 0)
    if start not in CALLERS or case['symbol'] != 'native_data_02102970' or case.get('dataRole') != 'late-signed-byte':
        raise ValueError('No qualified original late signed-byte role')
    if case.get('typedAccesses') != [] or case.get('minimumPrefixBytes') != 1 or case.get('completeObjectExtent') is not None or case.get('externalStorageCredit') != 0:
        raise ValueError('Signed-byte minimal prefix/allocation credit differs')
    words = {24: 0xe3500000, 28: 0x11a00004, 32: 0x18bd8010, 36: 0xe59f0010, 44: 0xe1d000d0}
    for offset, word in words.items():
        at = start - 0x02000000 + offset
        if struct.unpack('<I', image[at:at + 4])[0] != word:
            raise ValueError('Actual original predicate-success return or late signed LDRSB differs')
    return dict(result, dataRole='late-signed-byte', originalInstructionWords=words, signed=True, accessWidth=1,
                minimumPrefixBytes=1, completeObjectExtent=None, externalStorageCredit=0)


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
            raise ValueError('No exact original signed-byte caller/symbol witness')
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
        changes = [('wrong-origin', 'relocation', 'offset', 4), ('nonzero-addend', 'relocation', 'addend', 1),
                   ('wrong-base', 'binding', 'address', '0x2102971'), ('function-kind', 'binding', 'kind', 'function'),
                   ('function-mode', 'binding', 'mode', 'arm'), ('wrong-CPU', 'binding', 'processor', 'arm7'),
                   ('wrong-program', 'binding', 'program', 'child'), ('wrong-module', 'binding', 'module', 'ov000'),
                   ('wrong-prefix', 'case', 'minimumPrefixBytes', 2), ('invented-extent', 'case', 'completeObjectExtent', 1)]
        for label, owner, key, wrong in changes:
            items = {name: copy.deepcopy(obj) for name, obj in [('case', case), ('row', row), ('relocation', relocation), ('binding', binding)]}
            items[owner][key] = wrong
            try:
                validate(items['case'], items['row'], items['relocation'], items['binding'], image, inventory, loads)
            except ValueError as error:
                checks.append(dict(caller=case['caller'], case=label, rejected=True, reason=str(error)))
            else:
                raise ValueError('Invalid signed-byte data role accepted: ' + label)
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
                raise ValueError('Changed original signed-byte evidence accepted')
    return dict(status='passed', negativeCases=checks, sourceOrDataStorageCredit=0, ordinaryBranchVerifierUnchanged=True)
