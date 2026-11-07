import copy
import hashlib
import re
import struct
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from project import ROOT, read_json, sha256
from link_runtime_unit import verify_binding
from wave20261106_dwc_main_friend_next_second_compiler import NATIVE, NATIVE_SHA


def inputs():
    if sha256(NATIVE) != NATIVE_SHA:
        raise ValueError('Second native manifest changed')
    value = read_json(NATIVE)
    for item in value['files'] + [value['claim']]:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('Original second caller input changed')
    return value, (ROOT / 'extract/arm9/arm9.bin').read_bytes(), (ROOT / 'config/arm9/symbols.txt').read_text(), (ROOT / 'config/arm9/relocs.txt').read_text()


def validate(row, relocation, binding, value, image, inventory, records):
    if (row.get('program') or '', row['processor'], row['module'], row['mode']) != ('', 'arm9', 'main', 'thumb'):
        raise ValueError('Second caller namespace differs')
    native = next((item for item in value['entries'] if item['address'] == row['address']), None)
    if native is None or (native['bytes'], native['targetSha256']) != (row['bytes'], row['targetSha256']):
        raise ValueError('Second native extent/hash differs')
    address = int(row['address'], 0)
    if hashlib.sha256(image[address - 0x2000000:address - 0x2000000 + row['bytes']]).hexdigest() != row['targetSha256'] or native['canonicalInventoryRecord'] not in inventory.splitlines():
        raise ValueError('Original complete caller bytes/boundary differ')
    origin = address + relocation['offset']
    candidates = [line for line in native['originalRelocationRecords'] if line.startswith(f'from:0x{origin:08x} ')]
    if len(candidates) != 1 or candidates[0] not in records.splitlines():
        raise ValueError('Original unique relocation origin absent')
    match = re.fullmatch(r'from:0x[0-9a-f]+ kind:(thumb_call|thumb_call_arm|load) to:(0x[0-9a-f]+) module:main', candidates[0])
    if match is None:
        raise ValueError('Original second relocation kind/module differs')
    kind, target = match[1], int(match[2], 0)
    word = image[origin - 0x2000000:origin - 0x2000000 + 4]
    if (binding.get('program') or '', binding['processor'], binding['module']) != ('', 'arm9', 'main'):
        raise ValueError('Original second binding CPU/program/module differs')
    if kind == 'load' and hex(target) in value['functionPointerViews']:
        entry = int(value['functionPointerViews'][hex(target)], 0)
        if (binding['kind'], binding['mode'], int(binding['address'], 0)) != ('function', 'thumb', entry):
            raise ValueError('Original Thumb callback pointer mode/entry differs')
        if relocation['type'] != 2 or relocation['addend'] != 0 or int(relocation['target'], 0) != target or struct.unpack('<I', word)[0] != target or target != entry | 1:
            raise ValueError('Original source-visible callback relocation payload differs')
        canonical = next((line for line in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(thumb,size=0x[0-9a-f]+\) addr:0x%08x' % entry, line)), None)
        if canonical is None:
            raise ValueError('Original callback whole Thumb entry absent')
        extra = dict(callbackPointer=True, nativePointerWord=word.hex(), canonicalInventoryRecord=canonical, suppliedCallbackCredit=0)
    elif kind == 'load':
        base, addend = int(binding['address'], 0), relocation['addend']
        if (binding['kind'], binding['mode']) != ('data', 'data') or relocation['type'] != 2 or int(relocation['target'], 0) != base or target != base + addend or struct.unpack('<I', word)[0] != target:
            raise ValueError('Original data base/addend/payload differs')
        view = value['dataViews'].get(hex(base))
        if view is None:
            raise ValueError('Unqualified second data base')
        if view['kind'] == 'game-key-field-array-view':
            if base != 0x21d1ba8 or view['recordStride'] != 12 or addend not in [0, 1, 2, 4, 8] or addend not in view['fieldAddends']:
                raise ValueError('Original12-byte key record field relocation differs')
        elif view['kind'] == 'main-global-consumed-prefix':
            if base != 0x21d19e0 or addend != 0 or view['minimumBytes'] != 8 or view['controlPointerOffset'] != 0 or view['lastSocketErrorOffset'] != 4:
                raise ValueError('Original main global consumed-prefix view differs')
        elif view['kind'] == 'NAT-negotiation-magic':
            if addend or view['bytes'] != 6 or image[base - 0x2000000:base - 0x2000000 + 6].hex() != view['expectedHex']:
                raise ValueError('Original complete NAT magic changed')
        else:
            raise ValueError('Unsupported second data view')
        extra = dict(typedView=view, genuineSourceBase=hex(base), genuineRelocationAddend=addend,
            actualNativeWord=word.hex(), sourceStorageCredit=0)
    else:
        mode = 'arm' if kind == 'thumb_call_arm' else 'thumb'
        if relocation['type'] != 10 or relocation['addend'] != -4 or int(relocation['target'], 0) != target or (binding['kind'], binding['mode'], int(binding['address'], 0)) != ('function', mode, target):
            raise ValueError('Original branch ABI mode/type/addend/entry differs')
        decoded = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(word, origin))
        if len(decoded) != 1 or decoded[0].size != 4 or decoded[0].mnemonic != ('blx' if mode == 'arm' else 'bl') or decoded[0].op_str != '#' + hex(target):
            raise ValueError('Actual original branch opcode/mode/entry differs')
        canonical = next((line for line in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x' % (mode, target), line)), None)
        if canonical is None:
            raise ValueError('Original configured whole function entry absent')
        extra = dict(nativeInstruction=word.hex(), actualMnemonic=decoded[0].mnemonic, canonicalInventoryRecord=canonical, calleeSourceCredit=0)
    verify_binding(relocation['symbol'], binding)
    return dict(symbol=relocation['symbol'], origin=hex(origin), target=hex(target), originalRecord=candidates[0], **extra)


def qualify(row, bindings):
    values = inputs()
    return dict(witnesses=[validate(row, rel, bindings[rel['symbol']], *values) for rel in row['relocations']],
        originalFullCallerAndRelocationNamespacesChecked=True, sourceRelocationBaseAndAddendsRetained=True,
        syntheticDataAliases=0, suppliedCalleeOrStorageCredit=0)


def negatives(rows):
    values = inputs()
    selected = {}
    for row in rows:
        for rel in row['relocations']:
            binding = row['nativeSymbolEntries'][rel['symbol']]
            key = binding['kind'], binding['mode'], rel['type'], rel['addend'] != 0, binding['address']
            selected.setdefault(key, (row, rel, binding))
    categories = {}
    for key, item in selected.items():
        categories.setdefault(key[:4], item)
    output = []
    for category, (row, rel, binding) in categories.items():
        cases = [('cpu', 'binding', 'processor', 'arm7'), ('program', 'binding', 'program', 'child'),
            ('module', 'binding', 'module', 'ov000'), ('mode', 'binding', 'mode', 'arm' if binding['mode'] != 'arm' else 'thumb'),
            ('interior', 'binding', 'address', hex(int(binding['address'], 0) + 2)), ('origin', 'rel', 'offset', rel['offset'] + 2),
            ('type', 'rel', 'type', 1), ('addend', 'rel', 'addend', rel['addend'] + 4)]
        for label, owner, field, wrong in cases:
            items = {'row': copy.deepcopy(row), 'rel': copy.deepcopy(rel), 'binding': copy.deepcopy(binding)}
            items[owner][field] = wrong
            try:
                validate(items['row'], items['rel'], items['binding'], *values)
            except ValueError:
                output.append(dict(category=category, altered=label, rejected=True))
            else:
                raise ValueError('Wrong original second binding accepted')
    return output
