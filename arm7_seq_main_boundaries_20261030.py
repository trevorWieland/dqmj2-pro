import hashlib
import json
from pathlib import Path
import match_lowlevel
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_REG_PC

ROOT = Path(__file__).resolve().parent
EVIDENCE = [
    ('evidence/attempts/arm7-seq-main-layout-20261030.json', '22b69194749a7a6caa9fef28d38a6bb2d044065e48ea4a24dd17416f6ddf9884'),
    ('evidence/attempts/arm7-seq-main-consumers-20261030-v2.json', 'caca5dc539c39db67a8308a81a4823d8a9b69ab92a481a5aae0fafe7a3a2f599'),
    ('evidence/attempts/arm7-seq-main-opcode-word-roles-20261030.json', '5467f8d858d739901957686fe54e1039c4c6d10afeb0ff6d8bddb2373a75847f'),
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def boundaries(entry, layout):
    evidence = []
    for name, sha in EVIDENCE:
        if digest((ROOT / name).read_bytes()) != sha:
            raise ValueError('Frozen discontiguous review/loader/instruction-role evidence differs')
        evidence.append(json.loads((ROOT / name).read_text()))
    loader, consumers, roles = evidence
    inventory_path = ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'
    if digest(inventory_path.read_bytes()) != loader['inventorySha256']:
        raise ValueError('Raw original discontiguous inventory changed before separate migration approval')
    if entry['program'] != '' or entry['processor'] != 'arm7' or entry['module'] != 'arm7-wram' or entry['mode'] != 'arm':
        raise ValueError('Proposed sequence-main processor/module/mode identity differs')
    address, code, size = int(entry['address'], 0), entry['codeBytes'], entry['bytes']
    if (address, code, size) != (0x037FFF54, 344, 352):
        raise ValueError('Full discontiguous review span differs')
    modules = {row['id']: row for row in layout['modules']}
    binaries = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    base = int(modules['arm7-wram']['base'], 0)
    native = binaries['arm7-wram'][address - base:address - base + size]
    if digest(native) != loader['candidate']['spanSha256'] or modules['arm7-wram'] != loader['owner']:
        raise ValueError('Actually loaded original proposal ownership or bytes differ')
    inventory = json.loads(inventory_path.read_text())
    raw_row = next(row for row in inventory['functions'] if row['module'] == 'arm7-wram' and int(row['address'], 0) == address)
    if raw_row != loader['configuredFunction'] or raw_row['bodyBytes'] != 280:
        raise ValueError('Original discontiguous row changed before coordinator approval')
    instructions_decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    instructions_decoder.detail = True
    instructions = list(instructions_decoder.disasm(native[:code], address))
    if len(instructions) != 86:
        raise ValueError('Full proposed ARM code has unknown words')
    expected_calls = {0x037FFFDC: 0x03800CF0, 0x037FFFEC: 0x03800B00, 0x03800050: 0x03800A7C, 0x03800064: 0x03800B98}
    actual_calls = {row.address: row.operands[0].imm for row in instructions if row.group(CS_GRP_CALL)}
    if actual_calls != expected_calls:
        raise ValueError('Full proposed caller original call-site identities differ')
    literals = []
    for instruction in instructions:
        for operand in instruction.operands:
            if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                target = instruction.address + 8 + operand.mem.disp
                if not address + code <= target <= address + size - 4 or target % 4:
                    raise ValueError('Proposed source has unexplained code/pool/data overlap')
                literals.append({'pc': hex(instruction.address), 'storage': hex(target),
                    'word': hex(int.from_bytes(native[target - address:target - address + 4], 'little'))})
    if literals != loader['literalReferences']:
        raise ValueError('Complete proposed source literal reads differ')
    qualified = {(row['identity']['module'], int(row['identity']['pc'], 0), int(row['identity']['word'], 0)): row for row in roles['roles']}
    raw_words = []
    for name, raw in binaries.items():
        module_base = int(modules[name]['base'], 0)
        for offset in range(0, len(raw) - 3, 4):
            value = int.from_bytes(raw[offset:offset + 4], 'little')
            if address < (value & ~1) < address + size:
                key = (name, module_base + offset, value)
                if key not in qualified or not qualified[key]['knownInstructionRoleQualified']:
                    raise ValueError('New or unqualified raw initialized word resembles proposed source interior')
                raw_words.append({'module': name, 'pc': hex(module_base + offset), 'word': hex(value),
                    'opaqueDualUseDataAbsenceClaim': False, 'sourceCredit': 0})
    if len(raw_words) != 10 or roles['knownPcRelativeDataReadsAddressingSpecificOpcodeWords']:
        raise ValueError('Specific original opcode-word roles/data-use state changed')
    outside_interiors = []
    for function in inventory['functions']:
        mode = function.get('mode')
        if mode not in ('arm', 'thumb'):
            continue
        module = modules[function['module']]
        raw, module_base = binaries[function['module']], int(module['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if mode == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for first, last in function['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(raw[first - module_base:last - module_base], first):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                    continue
                target = instruction.operands[0].imm & ~1
                if address < target < address + size and not (function['module'] == 'arm7-wram' and address <= instruction.address < address + code):
                    outside_interiors.append({'module': function['module'], 'pc': hex(instruction.address), 'target': hex(target)})
    if outside_interiors or consumers['configuredOverlapConflicts'] or consumers['additionalConfiguredRootsInsideCodeOrPool']:
        raise ValueError('Unreconciled proposed-boundary conflict or outside interior entry')
    return {'originalInventorySha256': loader['inventorySha256'], 'originalConfiguredRanges': raw_row['ranges'],
        'originalConfiguredInstructionBytes': 280, 'newlyConfirmedExcludedInstructionBytes': 64,
        'proposedFullInstructionBytes': code, 'generatedLiteralBytes': size - code, 'literalReferences': literals,
        'actualOriginalLoaderOwnershipVerified': True, 'reviewEvidence': [{'path': p, 'sha256': sha} for p, sha in EVIDENCE],
        'tenSpecificOpcodeWordRoles': raw_words, 'outsideInteriorOrPoolFlows': [], 'paddingCredit': 0,
        'migrationApproved': False, 'sourceCreditWithheldPendingSeparateCoordinatorBoundaryReview': True,
        'limitations': ['Proposed complete source-unit proof does not mutate or approve the original discontiguous inventory',
            'Known direct flows/raw words/current original literal uses audited; opaque/computed/global consumers remain outside the entry-domain claim']}
