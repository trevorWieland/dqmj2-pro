import copy
import hashlib
import re
import struct
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from project import ROOT, read_json, sha256
from link_runtime_unit import verify_binding
from wave20261106_dwc_main_friend_next_first_v2_compiler import NATIVE, NATIVE_SHA


def inputs():
    if sha256(NATIVE) != NATIVE_SHA:
        raise ValueError('Native friend manifest changed')
    value = read_json(NATIVE)
    for item in value['files'] + [value['claim']]:
        if sha256(ROOT / item['path']) != item['sha256']:
            raise ValueError('Original friend input changed')
    return value, (ROOT / 'extract/arm9/arm9.bin').read_bytes(), (ROOT / 'config/arm9/symbols.txt').read_text(), (ROOT / 'config/arm9/relocs.txt').read_text()


def validate(row, relocation, binding, value, image, inventory, records):
    if (row.get('program') or '', row['processor'], row['module'], row['mode']) != ('', 'arm9', 'main', 'thumb'):
        raise ValueError('Friend caller namespace differs')
    native = next((item for item in value['entries'] if item['address'] == row['address']), None)
    if native is None or (native['bytes'], native['targetSha256']) != (row['bytes'], row['targetSha256']):
        raise ValueError('Friend caller extent or input hash differs')
    address = int(row['address'], 0)
    if hashlib.sha256(image[address - 0x2000000:address - 0x2000000 + row['bytes']]).hexdigest() != row['targetSha256'] or native['canonicalInventoryRecord'] not in inventory.splitlines():
        raise ValueError('Whole original friend body/boundary changed')
    origin = address + relocation['offset']
    matches = [line for line in native['originalRelocationRecords'] if line.startswith(f'from:0x{origin:08x} ')]
    if len(matches) != 1 or matches[0] not in records.splitlines():
        raise ValueError('Unique original friend relocation origin absent')
    match = re.fullmatch(r'from:0x[0-9a-f]+ kind:(thumb_call|thumb_call_arm|load) to:(0x[0-9a-f]+) module:main', matches[0])
    if match is None:
        raise ValueError('Original friend relocation kind/module differs')
    kind, target = match[1], int(match[2], 0)
    if (binding.get('program') or '', binding['processor'], binding['module'], int(binding['address'], 0)) != ('', 'arm9', 'main', target) or int(relocation['target'], 0) != target:
        raise ValueError('Friend original target CPU/program/module/entry differs')
    word = image[origin - 0x2000000:origin - 0x2000000 + 4]
    if kind == 'load':
        if relocation['type'] != 2 or relocation['addend'] != 0 or (binding['kind'], binding['mode']) != ('data', 'data') or struct.unpack('<I', word)[0] != target:
            raise ValueError('Friend original data relocation payload differs')
        view = value['dataViews'].get(hex(target))
        if view is None:
            raise ValueError('Undeclared friend data view')
        if view['kind'] == 'format-string':
            actual = image[target - 0x2000000:target - 0x2000000 + view['bytes']]
            if actual.hex() != view['expectedHex'] or actual != b'%c%c%c%c\0':
                raise ValueError('Original complete format bytes changed')
        elif view['kind'] == 'friend-global-consumed-pointer-prefix':
            if target != 0x21d1b74 or view['controlPointerOffset'] != 12 or view['minimumBytes'] != 16 or view['storage'] != 'bss':
                raise ValueError('Measured friend pointer view differs')
        else:
            raise ValueError('Unsupported friend data view')
        witness = dict(typedView=view, originalLiteralWord=word.hex(), storageAuthorshipCredit=0)
    else:
        mode = 'arm' if kind == 'thumb_call_arm' else 'thumb'
        if relocation['type'] != 10 or relocation['addend'] != -4 or (binding['kind'], binding['mode']) != ('function', mode):
            raise ValueError('Original friend THM_CALL/mode/addend differs')
        decoded = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(word, origin))
        if len(decoded) != 1 or decoded[0].size != 4 or decoded[0].mnemonic != ('blx' if mode == 'arm' else 'bl') or decoded[0].op_str != '#' + hex(target):
            raise ValueError('Actual original friend branch opcode/entry differs')
        canonical = next((line for line in inventory.splitlines() if re.fullmatch(r'\S+ kind:function\(%s,size=0x[0-9a-f]+\) addr:0x%08x' % (mode, target), line)), None)
        if canonical is None:
            raise ValueError('Actual canonical friend callee mode/boundary absent')
        witness = dict(canonicalInventoryRecord=canonical, nativeInstruction=word.hex(), actualMnemonic=decoded[0].mnemonic, calleeSourceCredit=0)
    verify_binding(relocation['symbol'], binding)
    return dict(symbol=relocation['symbol'], origin=hex(origin), target=hex(target), originalRecord=matches[0], **witness)


def qualify(row, bindings):
    values = inputs()
    return dict(witnesses=[validate(row, rel, bindings[rel['symbol']], *values) for rel in row['relocations']], originalNativeOpcodesNamespacesAndWholeEntriesChecked=True, calleeSourceCredit=0, storageAuthorshipCredit=0)


def negatives(rows):
    values = inputs()
    selected = {}
    for row in rows:
        for rel in row['relocations']:
            binding = row['nativeSymbolEntries'][rel['symbol']]
            key = binding['kind'], binding['mode'], binding.get('address') == '0x20e018c'
            selected.setdefault(key, (row, rel, binding))
    results = []
    for key, (row, rel, binding) in selected.items():
        for label, owner, field, wrong in [('cpu', 'binding', 'processor', 'arm7'), ('program', 'binding', 'program', 'child'),
                ('module', 'binding', 'module', 'ov000'), ('mode', 'binding', 'mode', 'arm' if binding['mode'] != 'arm' else 'thumb'),
                ('interior', 'binding', 'address', hex(int(binding['address'], 0) + 2)), ('addend', 'rel', 'addend', rel['addend'] + 4),
                ('relocation-kind', 'rel', 'type', 1), ('origin', 'rel', 'offset', rel['offset'] + 2)]:
            items = {'row': copy.deepcopy(row), 'rel': copy.deepcopy(rel), 'binding': copy.deepcopy(binding)}
            items[owner][field] = wrong
            try:
                validate(items['row'], items['rel'], items['binding'], *values)
            except ValueError:
                results.append(dict(bindingKind=key, altered=label, rejected=True))
            else:
                raise ValueError('Wrong friend native binding was accepted')
    return results
