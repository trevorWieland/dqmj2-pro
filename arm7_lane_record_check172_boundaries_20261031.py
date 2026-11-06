import json
from pathlib import Path
import match_lowlevel
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from project import ROOT, sha256

ROLE = 'evidence/arm7/lane-halfword-runtime-pointer-20261031.json'
ROLE_SHA = '368e444be97b6a9cd49a2eb1c0993e5c153c5073fb12dff67ebdd282f0f5bbf7'
HISTORY = 'evidence/attempts/arm7-record-check172-declaration-closure-20261031.json'
ADDRESS = 0x027F5B10


def boundaries(entry):
    if (entry['program'], entry['processor'], entry['module'], entry['mode'], int(entry['address'], 0), entry['bytes'], entry['codeBytes']) != (utility_runtime.PROGRAM, 'arm7', 'utility-child-arm7-main', 'arm', ADDRESS, 172, 164):
        raise ValueError('Caller full qualified entry differs')
    if sha256(ROOT / ROLE) != ROLE_SHA:
        raise ValueError('Measured absolute runtime pointer-word provenance changed')
    history = json.loads((ROOT / HISTORY).read_text())
    old = history['historicalArrayHypothesis']
    if sha256(ROOT / old['path']) != old['sha256'] or history['newDistinctScalarWordView']['sha256'] != entry['sourceSha256']:
        raise ValueError('Historical array hypothesis or distinct scalar source view changed')
    if history['newDistinctScalarWordView']['symbol'] not in (ROOT / entry['source']).read_text():
        raise ValueError('Source does not use its separate measured scalar pointer-word view')
    layout, unused = utility_runtime.derive()
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    images = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    inventory_path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(inventory_path.read_text())
    root = next(row for row in inventory['functions'] if row['module'] == entry['module'] and int(row['address'], 0) == ADDRESS)
    if root['mode'] != 'arm' or root['bodyBytes'] != 164 or [[int(value, 0) for value in extent] for extent in root['ranges']] != [[ADDRESS, ADDRESS + 164]]:
        raise ValueError('Original configured complete caller extent differs')
    metadata = modules[entry['module']]
    base = int(metadata['base'], 0)
    image = images[entry['module']]
    native = image[ADDRESS - base:ADDRESS - base + 164]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(native, ADDRESS))
    if len(instructions) != 41:
        raise ValueError('Caller contains undecoded bytes')
    pool = image[ADDRESS - base + 164:ADDRESS - base + 172]
    if pool != bytes.fromhex('f4ff8003d6010000'):
        raise ValueError('Own pointer/upper-limit literal pool differs')
    calls = {row.address: row.operands[0].imm for row in instructions if row.group(CS_GRP_CALL)}
    if calls != {0x027F5B58: 0x027E94C8, 0x027F5B6C: 0x027E93D4}:
        raise ValueError('Caller two qualified original primitive links differ')
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
                if ADDRESS <= target < ADDRESS + 172 and not ADDRESS <= instruction.address < ADDRESS + 172:
                    item = {'program': utility_runtime.PROGRAM, 'processor': 'arm7', 'module': row['module'], 'mode': row['mode'],
                        'root': row['address'], 'pc': hex(instruction.address), 'target': hex(target)}
                    incoming.append(item)
                    if target != ADDRESS:
                        interior.append(item)
    for name, data in images.items():
        for offset in range(0, len(data) - 3, 4):
            value = int.from_bytes(data[offset:offset + 4], 'little')
            if ADDRESS < value & ~1 < ADDRESS + 172:
                opaque.append({'module': name, 'offset': hex(offset), 'value': hex(value)})
    if interior or opaque:
        raise ValueError('Unreconciled direct/word interior entry into full caller')
    return {'inventory': inventory_path.relative_to(ROOT).as_posix(), 'inventorySha256': sha256(inventory_path),
        'configuredRoot': root, 'instructionBytes': 164, 'generatedLiteralBytes': 8, 'paddingCredit': 0, 'literalPool': {'start': hex(ADDRESS + 164), 'bytes': pool.hex(), 'sha256': __import__('hashlib').sha256(pool).hexdigest(), 'references': [['0x027f5b1c', '0x027f5bb4'], ['0x027f5b34', '0x027f5bb8'], ['0x027f5b80', '0x027f5bb4']]}, 'actualCalls': [{'pc': hex(key), 'target': hex(value)} for key, value in calls.items()],
        'qualifiedIncomingReferences': incoming, 'outsideInteriorReferences': interior, 'opaqueInteriorWords': opaque,
        'runtimePointerWord': {'path': ROLE, 'sha256': ROLE_SHA, 'absoluteAddress': '0x0380fff4', 'storageBytes': 4,
            'moduleBssOwnershipCredit': 0, 'sourceDataCredit': 0, 'incomingDescriptorOriginMeasured': True},
        'declarationClosure': {'path': HISTORY, 'sha256': sha256(ROOT / HISTORY), 'historicalSourcesChanged': False,
            'scalarWordAlias': history['newDistinctScalarWordView']['symbol'], 'sameMeasuredAddress': '0x0380fff4'},
        'limitations': ['Complete own boundary and known direct/word references are measured; absence of all opaque indirect entries and enclosing scene reachability remain unproved',
            'Byte getter, CRC step, nibble table and external descriptor-word contents receive zero reconstructed-source/data credit']}
