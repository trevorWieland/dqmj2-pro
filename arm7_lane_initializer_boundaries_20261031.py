import hashlib
import json
from pathlib import Path
import match_lowlevel
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_REG_PC

ROOT = Path(__file__).resolve().parent


def digest(data):
    return hashlib.sha256(data).hexdigest()


def boundaries(entry, layout):
    inventory_path = ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'
    inventory = json.loads(inventory_path.read_text())
    address, code_size, size = int(entry['address'], 0), entry['codeBytes'], entry['bytes']
    rows = [row for row in inventory['functions'] if row['module'] == entry['module'] and int(row['address'], 0) == address]
    if len(rows) != 1 or rows[0]['mode'] != 'arm' or [[int(value, 0) for value in pair] for pair in rows[0]['ranges']] != [[address, address + code_size]]:
        raise ValueError('Host configured root/code range differs')
    if any(address < int(row['address'], 0) < address + size for row in inventory['functions']):
        raise ValueError('Another configured function enters the full source unit')
    modules = {row['id']: row for row in layout['modules']}
    binaries = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    module = modules[entry['module']]
    base = int(module['base'], 0)
    native = binaries[entry['module']][address - base:address - base + size]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(native[:code_size], address))
    if sum(row.size for row in instructions) != code_size:
        raise ValueError('Host bounded source body has unknown bytes or callees')
    calls = [row for row in instructions if row.group(CS_GRP_CALL)]
    expected_calls = {0x037FF164: {}}
    if {row.address: row.operands[0].imm for row in calls} != expected_calls[address]:
        raise ValueError('Unqualified original SDK state-accessor call sites')
    literal_references = []
    for instruction in instructions:
        for operand in instruction.operands:
            if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                target = instruction.address + 8 + operand.mem.disp
                if not address + code_size <= target <= address + size - 4 or target % 4:
                    raise ValueError('Unreconciled PC-relative source data')
                literal_references.append({'pc': hex(instruction.address), 'storageAddress': hex(target),
                    'word': hex(int.from_bytes(native[target - address:target - address + 4], 'little'))})
    if {int(row['storageAddress'], 0) for row in literal_references} != set(range(address + code_size, address + size, 4)):
        raise ValueError('Compiler pool range includes unattributed bytes/alignment')
    references, interiors = [], []
    for row in inventory['functions']:
        if row.get('mode') not in ('arm', 'thumb'):
            continue
        other = modules[row['module']]
        raw, other_base = binaries[row['module']], int(other['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if row['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        for first, last in row['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(raw[first - other_base:last - other_base], first):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                    continue
                target = instruction.operands[0].imm & ~1
                if address <= target < address + size and not address <= instruction.address < address + code_size:
                    item = {'module': row['module'], 'sourceRoot': row['address'], 'mode': row['mode'], 'pc': hex(instruction.address), 'target': hex(target)}
                    references.append(item)
                    if target != address:
                        interiors.append(item)
    if interiors:
        raise ValueError('Configured outside flow enters a body interior/pool')
    for name, raw in binaries.items():
        for offset in range(0, len(raw) - 3, 4):
            value = int.from_bytes(raw[offset:offset + 4], 'little')
            if address < (value & ~1) < address + size:
                raise ValueError('Unreconciled initialized pointer into source body/pool')
    return {'inventorySha256': digest(inventory_path.read_bytes()), 'configuredRootCodeAndPoolQualified': True, 'instructionBytes': code_size,
        'generatedLiteralBytes': size - code_size, 'literalReferences': literal_references, 'outsideRootReferences': references,
        'outsideInteriorOrPoolReferences': [], 'paddingCredit': 0, 'instructionMode': 'arm',
        'limitations': ['Configured direct-flow and aligned initialized-word scan; opaque computed pointer producers remain outside this entry-domain proof']}

