import hashlib
import json
from pathlib import Path
import match_runtime
import utility_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP

ROOT = Path(__file__).resolve().parent
FIRST, LAST = 0x027F7F74, 0x027F7F94
MODULE_SHA = 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def classify():
    layout, unused = utility_runtime.derive()
    modules = {row['id']: row for row in layout['modules'] if row.get('processor') == 'arm7'}
    module = modules['utility-child-arm7-main']
    base = int(module['base'], 0)
    if not base <= FIRST < LAST <= base + module['bytes'] or module['sha256'] != MODULE_SHA:
        raise ValueError('Whole CRC table must lie in the measured initialized child ARM7 module')
    images = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    if digest(images['utility-child-arm7-main']) != MODULE_SHA:
        raise ValueError('Measured initialized child-main image changed')
    path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(path.read_text())
    overlaps, branches, words = [], [], []
    for row in inventory['functions']:
        if row['module'] not in modules or row.get('mode') not in ('arm', 'thumb'):
            continue
        origin = int(modules[row['module']]['base'], 0)
        raw = images[row['module']]
        decoder = Cs(CS_ARCH_ARM, CS_MODE_THUMB if row['mode'] == 'thumb' else CS_MODE_ARM)
        decoder.detail = True
        for first, last in row['ranges']:
            first, last = int(first, 0), int(last, 0)
            if row['module'] == 'utility-child-arm7-main' and first < LAST and FIRST < last:
                overlaps.append(row)
            for instruction in decoder.disasm(raw[first - origin:last - origin], first):
                if not (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) or not instruction.operands or instruction.operands[0].type != 2:
                    continue
                target = instruction.operands[0].imm & ~1
                if FIRST <= target < LAST:
                    branches.append({'module': row['module'], 'mode': row['mode'], 'root': row['address'], 'pc': hex(instruction.address), 'target': hex(target)})
    for name, raw in images.items():
        origin = int(modules[name]['base'], 0)
        for offset in range(0, len(raw) - 3, 4):
            value = int.from_bytes(raw[offset:offset + 4], 'little')
            if FIRST <= value < LAST:
                words.append({'module': name, 'address': hex(origin + offset), 'rawValue': hex(value)})
    if overlaps or branches:
        raise ValueError('CRC data proposal intersects a configured function or known direct code target')
    if words != [{'module': 'utility-child-arm7-main', 'address': '0x27e9444', 'rawValue': '0x27f7f74'}]:
        raise ValueError('Additional unreviewed aligned table-range address words found')
    code = images['utility-child-arm7-main'][0x027E93D4 - base:0x027E9444 - base]
    if digest(code) != '855a586286d0bb406082bb67e3ae580396ba799403b18b74ad855e3e2f0d9942':
        raise ValueError('Measured direct table consumer code changed')
    return {'program': utility_runtime.PROGRAM, 'processor': 'arm7', 'module': 'utility-child-arm7-main', 'kind': 'initialized-data', 'mode': 'data',
        'start': hex(FIRST), 'end': hex(LAST), 'bytes': 32, 'inputModule': module['binary'], 'inputModuleSha256': MODULE_SHA,
        'moduleBase': hex(base), 'initializedModuleEnd': hex(base + module['bytes']),
        'inventory': path.relative_to(ROOT).as_posix(), 'inventorySha256': digest(path.read_bytes()),
        'configuredCodeOverlaps': overlaps, 'knownDirectBranchesIntoRange': branches, 'alignedAddressWordsIntoRange': words,
        'consumer': {'address': '0x027e93d4', 'mode': 'arm', 'codeBytes': 112, 'codeSha256': digest(code),
            'halfwordLoadPcs': ['0x027e93e0', '0x027e93fc', '0x027e941c', '0x027e9430'], 'indexDomain': list(range(16)), 'ordinarySourceFunctionCredit': 0},
        'originalTotalObjectExtentClaimed': False, 'configuredBoundariesOrSymbolsChanged': False,
        'initializedCoverageDenominatorIncrease': 0, 'ordinaryExecutableBytesCredit': 0,
        'limitations': ['One exact32-byte indexed read span; original variable name and any larger original object extent remain unproved',
            'No known configured function/direct code target overlaps; opaque indirect program-wide absence remains unproved',
            'Data classification is a proposal for review, with no shared inventory or boundary promotion']}
