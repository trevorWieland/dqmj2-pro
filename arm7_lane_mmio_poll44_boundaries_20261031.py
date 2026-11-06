import hashlib
import json
from pathlib import Path
import arm7_runtime
import match_lowlevel
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_REG_PC

ROOT = Path(__file__).resolve().parent
ADDRESS = 0x037FB300


def digest(data):
    return hashlib.sha256(data).hexdigest()


def boundaries(entry):
    if (entry['program'], entry['processor'], entry['module'], entry['mode'], int(entry['address'], 0), entry['bytes'], entry['codeBytes']) != ('', 'arm7', 'arm7-wram', 'arm', ADDRESS, 44, 40):
        raise ValueError('Poll full qualified code/pool identity differs')
    inventory_path = ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'
    inventory = json.loads(inventory_path.read_text())
    root = next(row for row in inventory['functions'] if row['module'] == 'arm7-wram' and int(row['address'], 0) == ADDRESS)
    if root['mode'] != 'arm' or root['bodyBytes'] != 40 or root['ranges'] != [['0x37fb300', '0x37fb328']]:
        raise ValueError('Configured poll entry/instruction extent differs')
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    modules = {row['id']: row for row in layout['modules']}
    binaries = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    raw = binaries['arm7-wram']
    base = int(modules['arm7-wram']['base'], 0)
    body = raw[ADDRESS - base:ADDRESS - base + 44]
    if digest(body) != entry['targetSha256'] or int.from_bytes(body[-4:], 'little') != 0x0480819C:
        raise ValueError('Native poll full range or sole hardware-address pool word differs')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(body[:40], ADDRESS))
    if len(instructions) != 10 or any(row.group(CS_GRP_CALL) for row in instructions):
        raise ValueError('Poll ARM instructions or no-callee contract differs')
    literals = []
    for row in instructions:
        for operand in row.operands:
            if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                storage = row.address + 8 + operand.mem.disp
                literals.append({'pc': hex(row.address), 'pool': hex(storage), 'word': hex(int.from_bytes(body[storage - ADDRESS:storage - ADDRESS + 4], 'little'))})
    if literals != [{'pc': hex(ADDRESS), 'pool': hex(ADDRESS + 40), 'word': '0x480819c'}]:
        raise ValueError('Poll own address-literal attribution differs')
    references, interiors = [], []
    for function in inventory['functions']:
        module = modules[function['module']]
        image = binaries[function['module']]
        origin = int(module['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if function['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        for first, last in function['ranges']:
            first, last = int(first, 0), int(last, 0)
            decoded = list(decoder.disasm(image[first - origin:last - origin], first))
            for index, instruction in enumerate(decoded):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                    continue
                target = instruction.operands[0].imm & ~1
                if ADDRESS <= target < ADDRESS + 44 and not ADDRESS <= instruction.address < ADDRESS + 40:
                    item = {'program': '', 'processor': 'arm7', 'module': function['module'], 'callerRoot': function['address'],
                        'mode': function['mode'], 'pc': hex(instruction.address), 'target': hex(target),
                        'followingInstructions': [{'pc': hex(row.address), 'mnemonic': row.mnemonic, 'operands': row.op_str} for row in decoded[index + 1:index + 4]]}
                    references.append(item)
                    if target != ADDRESS:
                        interiors.append(item)
    if interiors or [(row['module'], row['callerRoot'], row['pc'], row['mode']) for row in references] != [('arm7-wram', '0x37f8de0', '0x37f913c', 'arm')]:
        raise ValueError('Poll configured caller/interior references differ')
    suffix = raw[0x037F913C - base:0x037F914C - base]
    expected_suffix = bytes.fromhex('6f0800eb08d08de2f840bde81eff2fe1')
    if suffix != expected_suffix:
        raise ValueError('Original caller BL/pop/raw-R0-forwarding suffix changed')
    opaque = []
    for name, image in binaries.items():
        for offset in range(0, len(image) - 3, 4):
            value = int.from_bytes(image[offset:offset + 4], 'little')
            if ADDRESS < value & ~1 < ADDRESS + 44:
                opaque.append({'module': name, 'offset': hex(offset), 'word': hex(value)})
    if opaque:
        raise ValueError('Unreconciled initialized word references poll body/pool interior')
    return {'inventory': inventory_path.relative_to(ROOT).as_posix(), 'inventorySha256': digest(inventory_path.read_bytes()),
        'configuredFunction': root, 'originalModuleSha256': digest(raw), 'fullRangeSha256': digest(body),
        'instructions': [{'pc': hex(row.address), 'mnemonic': row.mnemonic, 'operands': row.op_str} for row in instructions],
        'instructionBytes': 40, 'literalBytes': 4, 'alignmentOrPaddingCredit': 0, 'literalReferences': literals,
        'qualifiedConfiguredCallers': references, 'outsideInteriorBranches': interiors, 'opaqueInteriorWords': opaque,
        'callerSuffix': {'address': '0x037f913c', 'bytes': 16, 'sha256': digest(suffix),
            'observedContract': 'Actual BL to poll, stack-frame restoration and BX LR leave returned R0 untouched', 'completeCallerOrPrefixCredit': 0},
        'entryRegisterInputs': ['LR for return'], 'initialArgumentOrFlagInputs': [],
        'partialStorageView': {'address': '0x0480819c', 'accessBytes': 2, 'volatile': True, 'originalObjectExtentKnown': False, 'sourceDataCredit': 0},
        'limitations': ['Configured direct references and aligned initialized words were examined; global absence of opaque/dynamic consumers is unproved',
            'Caller full-function reachability and physical MMIO/device interpretation remain unproved']}
