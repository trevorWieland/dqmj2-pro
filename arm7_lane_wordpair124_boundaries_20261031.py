import json
from pathlib import Path
import match_lowlevel
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from project import ROOT, sha256

ROLE = 'evidence/arm7/lane-child-divide-wordpair-scope-20261031.json'
ROLE_SHA = '9d1951d47676c59ea4b5c8cdae84150f6d169fbbfda92f3c5467435ebf536e7c'
HISTORY = 'evidence/attempts/arm7-wordpair124-declaration-closure-20261031.json'
ADDRESS = 0x027F6A48


def boundaries(entry):
    if (entry['program'], entry['processor'], entry['module'], entry['mode'], int(entry['address'], 0), entry['bytes'], entry['codeBytes']) != (utility_runtime.PROGRAM, 'arm7', 'utility-child-arm7-main', 'arm', ADDRESS, 124, 124):
        raise ValueError('Caller full qualified entry differs')
    if sha256(ROOT / ROLE) != ROLE_SHA:
        raise ValueError('Measured original two-word divide/code role changed')
    role = json.loads((ROOT / ROLE).read_text())
    history = json.loads((ROOT / HISTORY).read_text())
    old = history['unchangedAcceptedLowWordConsumer']
    if sha256(ROOT / old['path']) != old['sha256'] or history['newDistinctTwoWordView']['sha256'] != entry['sourceSha256']:
        raise ValueError('Accepted low-word declaration or distinct pair-view source changed')
    if history['newDistinctTwoWordView']['symbol'] not in (ROOT / entry['source']).read_text():
        raise ValueError('Source does not use its measured separate two-word view')
    layout, unused = utility_runtime.derive()
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    images = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    inventory_path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(inventory_path.read_text())
    root = next(row for row in inventory['functions'] if row['module'] == entry['module'] and int(row['address'], 0) == ADDRESS)
    if root['mode'] != 'arm' or root['bodyBytes'] != 124 or [[int(value, 0) for value in extent] for extent in root['ranges']] != [[ADDRESS, ADDRESS + 124]]:
        raise ValueError('Original configured complete caller extent differs')
    metadata = modules[entry['module']]
    base = int(metadata['base'], 0)
    image = images[entry['module']]
    native = image[ADDRESS - base:ADDRESS - base + 124]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(native, ADDRESS))
    if len(instructions) != 31:
        raise ValueError('Caller contains undecoded bytes')
    calls = {row.address: row.operands[0].imm for row in instructions if row.group(CS_GRP_CALL)}
    if calls != {0x027F6A70: 0x03805184, 0x027F6A80: 0x03805184, 0x027F6A98: 0x03805184, 0x027F6AB4: 0x03805184}:
        raise ValueError('Caller four qualified actual divide links differ')
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
                if ADDRESS <= target < ADDRESS + 124 and not ADDRESS <= instruction.address < ADDRESS + 124:
                    item = {'program': utility_runtime.PROGRAM, 'processor': 'arm7', 'module': row['module'], 'mode': row['mode'],
                        'root': row['address'], 'pc': hex(instruction.address), 'target': hex(target)}
                    incoming.append(item)
                    if target != ADDRESS:
                        interior.append(item)
    for name, data in images.items():
        for offset in range(0, len(data) - 3, 4):
            value = int.from_bytes(data[offset:offset + 4], 'little')
            if ADDRESS < value & ~1 < ADDRESS + 124:
                opaque.append({'module': name, 'offset': hex(offset), 'value': hex(value)})
    if interior or opaque:
        raise ValueError('Unreconciled direct/word interior entry into full caller')
    return {'inventory': inventory_path.relative_to(ROOT).as_posix(), 'inventorySha256': sha256(inventory_path),
        'configuredRoot': root, 'instructionBytes': 124, 'literalOrAlignmentBytes': 0, 'actualCalls': [{'pc': hex(key), 'target': hex(value)} for key, value in calls.items()],
        'qualifiedIncomingReferences': incoming, 'outsideInteriorReferences': interior, 'opaqueInteriorWords': opaque,
        'helperRole': {'path': ROLE, 'sha256': ROLE_SHA, 'configuredEntryBytesUnchanged': role['configuredEntryBytesUnchanged'],
            'actualExecutedCodeBytes': role['actualExecutedCodeBytes'], 'sourceCredit': 0, 'canonicalFunctionBoundaryEnlarged': False},
        'declarationClosure': {'path': HISTORY, 'sha256': sha256(ROOT / HISTORY), 'acceptedLowWordSourceChanged': False,
            'pairAlias': history['newDistinctTwoWordView']['symbol'], 'sameMeasuredNativeAddress': '0x03805184'},
        'limitations': ['Full caller boundary/known direct references are measured; opaque indirect program-wide absence and complete enclosing caller reachability are unproved',
            'Native divide source, complete ordinary function boundary and all-divisor behavior remain outside caller credit']}
