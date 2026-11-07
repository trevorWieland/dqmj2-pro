import copy
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

WORDS = {0x02213e60: '74209fe5', 0x02213e64: '68109fe5',
         0x02213e68: '0a30a0e3', 0x02213e6c: '0000c2e5',
         0x02213e90: '44009fe5', 0x02213e94: '0000d0e5'}


def validate(row, rel, binding, image, inventory, base):
    identity = row.get('program') or '', row['processor'], row['module'], row['mode'], row['address'], row['bytes']
    if identity != ('', 'arm9', 'ov001', 'arm', '0x2213da8', 312):
        raise ValueError('Initialized-byte import is limited to the exact admitted caller')
    expected = dict(symbol='native_data_ov001_0222f1c8', offset=0x134, type=2,
                    addend=0, target='0x222f1c8')
    if any(rel.get(key) != value for key, value in expected.items()):
        raise ValueError('Exact scalar data relocation/origin/type/addend differs')
    if (binding.get('program') or '', binding['processor'], binding['module'],
        binding['kind'], binding['mode'], binding['address']) != ('', 'arm9', 'ov001', 'data', 'data', '0x222f1c8'):
        raise ValueError('Initialized scalar import namespace/kind/mode differs')
    canonical = 'data_ov001_0222f1c8 kind:data(any) addr:0x0222f1c8'
    if canonical not in inventory.splitlines():
        raise ValueError('Original initialized data entry absent')
    if not base <= 0x0222f1c8 < base + len(image):
        raise ValueError('Byte is outside initialized overlay storage')
    if struct.unpack_from('<I', image, 0x02213edc - base)[0] != 0x0222f1c8:
        raise ValueError('Original cached-byte ABS32 literal differs')
    for address, word in WORDS.items():
        if image[address - base:address - base + 4].hex() != word:
            raise ValueError('Original cache pointer/byte-width/def-use instruction differs')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    witnesses = []
    for address in [0x02213e60, 0x02213e90]:
        instruction = next(decoder.disasm(image[address - base:address - base + 4], address))
        displacement = 0x74 if address == 0x02213e60 else 0x44
        if address + 8 + displacement != 0x02213edc:
            raise ValueError('Actual original PC literal origin differs')
        witnesses.append(dict(address=hex(address), instruction=instruction.mnemonic + ' ' + instruction.op_str,
                              literal='0x2213edc', target='0x222f1c8'))
    return dict(status='passed', sourceCredit=0, storageCredit=0, calleeCredit=0,
                originalCanonicalRecord=canonical, initializedConsumedBytes=1,
                nativeInitialByte=image[0x0222f1c8 - base], literalWitnesses=witnesses,
                store=dict(address='0x2213e6c', width=1, valueRegister='r0', baseRegister='r2'),
                load=dict(address='0x2213e94', width=1, zeroExtended=True, baseRegister='r0'),
                fullOriginalDefUseWords=WORDS,
                limits='One mutable borrowed byte, no source/storage credit or reconstructed payload. The actual C declaration and independent full caller fixtures must preserve upper adjacent bytes.')


def negative_controls(row):
    from wave20261106_ov001_state_controllers_source_second_bindings import inputs
    value, image, inventory, records, main_inventory = inputs()
    base = int(value['base'], 0)
    rel = next(r for r in row['relocations'] if r['symbol'] == 'native_data_ov001_0222f1c8')
    binding = row['nativeSymbolEntries'][rel['symbol']]
    positive = validate(row, rel, binding, image, inventory, base)
    cases = []
    for address in WORDS:
        changed = bytearray(image)
        changed[address - base] ^= 1
        try:
            validate(row, rel, binding, changed, inventory, base)
        except ValueError as error:
            cases.append(dict(case='actual-origin-register-or-byte-word', address=hex(address), rejected=True, reason=str(error)))
        else:
            raise ValueError('Changed actual import access instruction admitted')
    for label, address, replacement in [('word-store', 0x02213e6c, 0xe5820000),
                                         ('word-load', 0x02213e94, 0xe5900000),
                                         ('signed-load', 0x02213e94, 0xe1d000d0)]:
        changed = bytearray(image)
        struct.pack_into('<I', changed, address - base, replacement)
        try:
            validate(row, rel, binding, changed, inventory, base)
        except ValueError as error:
            cases.append(dict(case=label, address=hex(address), rejected=True, reason=str(error)))
        else:
            raise ValueError('Incorrect actual byte load/store width/sign admitted')
    wrong_inventory = inventory.replace('data_ov001_0222f1c8 kind:data(any)', 'data_ov001_0222f1c8 kind:function(arm,size=0x4)')
    try:
        validate(row, rel, binding, image, wrong_inventory, base)
    except ValueError as error:
        cases.append(dict(case='function-vs-data', rejected=True, reason=str(error)))
    else:
        raise ValueError('Executable entry admitted as mutable byte')
    for key, wrong in [('processor', 'arm7'), ('program', 'child'), ('module', 'ov000'),
                       ('mode', 'thumb'), ('kind', 'function'), ('address', '0x222f1c9')]:
        changed = copy.deepcopy(binding)
        changed[key] = wrong
        try:
            validate(row, rel, changed, image, inventory, base)
        except ValueError as error:
            cases.append(dict(case=key, rejected=True, reason=str(error)))
        else:
            raise ValueError('Incorrect initialized import binding admitted')
    return dict(status='passed', sourceCredit=0, positive=positive, negativeControls=cases)
