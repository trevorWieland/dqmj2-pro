import json
from pathlib import Path
import match_lowlevel
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from project import ROOT, sha256

def boundaries(entry):
    address = int(entry['address'], 0)
    size = {0x027E94C8: 32, 0x027E94E8: 44}.get(address)
    if (entry['program'], entry['processor'], entry['module'], entry['mode'], entry['bytes'], entry['codeBytes']) != (utility_runtime.PROGRAM, 'arm7', 'utility-child-arm7-main', 'arm', size, size) or size is None:
        raise ValueError('Full child halfword-byte primitive identity differs')
    layout, unused = utility_runtime.derive()
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    images = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    inventory_path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(inventory_path.read_text())
    root = next(row for row in inventory['functions'] if row['module'] == entry['module'] and int(row['address'], 0) == address)
    if root['mode'] != 'arm' or root['bodyBytes'] != size or [[int(value, 0) for value in extent] for extent in root['ranges']] != [[address, address + size]]:
        raise ValueError('Original configured complete caller extent differs')
    metadata = modules[entry['module']]
    base = int(metadata['base'], 0)
    image = images[entry['module']]
    native = image[address - base:address - base + size]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(native, address))
    if len(instructions) != size // 4:
        raise ValueError('Caller contains undecoded bytes')
    calls = {row.address: row.operands[0].imm for row in instructions if row.group(CS_GRP_CALL)}
    if calls:
        raise ValueError('Leaf primitive acquired a callee')
    incoming, interior, opaque = [], [], []
    for row in inventory['functions']:
        if row['module'] not in modules or row.get('mode') not in ('arm', 'thumb'):
            continue
        data = images[row['module']]
        origin = int(modules[row['module']]['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if row['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        for first, last in row['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(data[first - origin:last - origin], first):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                    continue
                target = instruction.operands[0].imm & ~1
                if address <= target < address + size and not address <= instruction.address < address + size:
                    item = {'program': utility_runtime.PROGRAM, 'processor': 'arm7', 'module': row['module'], 'mode': row['mode'],
                        'root': row['address'], 'pc': hex(instruction.address), 'target': hex(target)}
                    incoming.append(item)
                    if target != address:
                        interior.append(item)
    for name, data in images.items():
        for offset in range(0, len(data) - 3, 4):
            value = int.from_bytes(data[offset:offset + 4], 'little')
            if address < value & ~1 < address + size:
                opaque.append({'module': name, 'offset': hex(offset), 'value': hex(value)})
    if interior or opaque:
        raise ValueError('Unreconciled direct/word interior entry into full caller')
    return {'inventory': inventory_path.relative_to(ROOT).as_posix(), 'inventorySha256': sha256(inventory_path),
        'configuredRoot': root, 'instructionBytes': size, 'literalOrAlignmentBytes': 0, 'actualCalls': [{'pc': hex(key), 'target': hex(value)} for key, value in calls.items()],
        'qualifiedIncomingReferences': incoming, 'outsideInteriorReferences': interior, 'opaqueInteriorWords': opaque,
        'abi': {'arguments': ['u32 address'] if address == 0x027E94C8 else ['u32 address', 'u32 value'], 'return': 'u32 selected byte' if address == 0x027E94C8 else 'u32 unchanged address', 'alignment': 'address lowbit selects one byte through aligned halfword access'},
        'limitations': ['Complete own extents and known direct/aligned-word references are measured; opaque indirect program-wide absence and enclosing scene reachability remain unproved']}
