import json
from pathlib import Path
import match_runtime
import arm7_child_alarm_engine_20261031 as engine
import link_arm7_bulk_20261030 as linker
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_REG_PC
from project import ROOT, write_json

REPORT = ROOT / 'evidence/attempts/arm7-child-irq-check-word-20261101.json'
REFERENCE = ROOT / 'evidence/research/20261101-arm7-reserved-irqword-calico-reference.json'
REFERENCE_SHA = 'b62090ab5152a9811893071c2624287de3db14bab06f892967d109273ca01883'
WORD = 0x0380FFF8


def reference():
    if engine.digest(REFERENCE.read_bytes()) != REFERENCE_SHA:
        raise ValueError('Pinned primary platform reference changed')
    manifest = json.loads(REFERENCE.read_text())
    for item in manifest['files']:
        data = (ROOT / item['path']).read_bytes()
        if len(data) != item['bytes'] or engine.digest(data) != item['sha256']:
            raise ValueError('Pinned platform reference bytes changed')
    prefix = ROOT / 'deps/references/calico-81b75e31-irq-20261101'
    text = (prefix / 'share/ds7.ld').read_text()
    expressions = ['wram    : ORIGIN = 0x37f8000, LENGTH = 0x17000',
        '__sys_start  = ORIGIN(wram) + LENGTH(wram)', '__sp_usr     = __sys_start + 0xe80',
        '__sp_irq     = __sp_usr + 0x100', '__sp_svc     = __sp_irq + 0x40',
        '__irq_flags  = __sp_svc + 0x38']
    if any(item not in text for item in expressions) or 0x037F8000 + 0x17000 + 0xE80 + 0x100 + 0x40 + 0x38 != WORD:
        raise ValueError('Primary reserved BIOS word derivation differs')
    if 'extern volatile IrqMask __irq_flags;' not in (prefix / 'include/calico/system/irq.h').read_text():
        raise ValueError('Primary volatile platform contract differs')
    return {'manifest': REFERENCE.relative_to(ROOT).as_posix(), 'sha256': REFERENCE_SHA,
        'repository': manifest['repository'], 'commit': manifest['commit'], 'accessDate': manifest['accessDate'],
        'derivedAddress': hex(WORD), 'sourceVersionEquivalenceProven': False, 'compilerInput': False}


def references(layout):
    path = ROOT / 'evidence/utility/ghidra-arm7.json'
    inventory = json.loads(path.read_text())['functions']
    modules = {item['id']: item for item in layout['modules'] if item.get('processor') == 'arm7'}
    binaries = {name: (ROOT / item['binary']).read_bytes() for name, item in modules.items()}
    rows = []
    for function in inventory:
        if function['module'] not in modules or function['mode'] not in ('arm', 'thumb'):
            continue
        binary = binaries[function['module']]
        base = int(modules[function['module']]['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if function['mode'] == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for begin, end in function['ranges']:
            begin, end = int(begin, 0), int(end, 0)
            for instruction in decoder.disasm(binary[begin-base:end-base], begin):
                for operand in instruction.operands:
                    if operand.type != 3 or operand.mem.base != ARM_REG_PC:
                        continue
                    pc_base = instruction.address + 8 if function['mode'] == 'arm' else (instruction.address + 4) & ~3
                    literal = pc_base + operand.mem.disp
                    offset = literal - base
                    if not 0 <= offset <= len(binary) - 4 or int.from_bytes(binary[offset:offset+4], 'little') != WORD:
                        continue
                    width = 4 if function['mode'] == 'arm' else 2
                    scope_count = 4 if function['mode'] == 'arm' else 5
                    scope = binary[instruction.address-base:instruction.address-base+width*scope_count]
                    rows.append({'module': function['module'], 'entry': function['address'], 'mode': function['mode'],
                        'pc': hex(instruction.address), 'literal': hex(literal), 'literalValue': hex(WORD),
                        'followingInstructions': [{'pc': hex(item.address), 'mnemonic': item.mnemonic, 'operands': item.op_str}
                            for item in decoder.disasm(scope, instruction.address)], 'scopeSha256': engine.digest(scope)})
    expected = {0x037F9510, 0x037FBADC, 0x037FD92C, 0x037FDE88, 0x03803EF8}
    if {int(item['pc'], 0) for item in rows} != expected or len(rows) != len(expected):
        raise ValueError('Current qualified original literal references differ')
    return {'inventorySha256': engine.digest(path.read_bytes()), 'references': rows,
        'literalReferenceScopeOnly': True, 'separateOriginalClearOrWaitConsumerProven': False}


def native(case, seed, budget=100000):
    machine = engine.setup({}, seed)
    cpu = machine['cpu']
    cpu.mem_write(0x038059AC, bytes(4))
    cpu.mem_write(0x027FFC3C, case['counter'].to_bytes(4, 'little'))
    cpu.mem_write(WORD - 4, bytes.fromhex('12345678') + case['flags'].to_bytes(4, 'little') + bytes.fromhex('89abcdef'))
    before = machine['snapshot']()
    result = machine['invoke'](0x037FBAAC, [], budget)
    if not result['actualReturn']:
        return dict(actualReturn=False, case=case, execution=result, returnCredit=0)
    expected = [[0x027FFC3C, 4, (case['counter'] + 1) & 0xFFFFFFFF], [WORD, 4, case['flags'] | 1]]
    actual = [item for item in result['writes'] if not engine.STACK <= item[0] < engine.STACK + 0x4000]
    if actual != expected or [item for item in result['reads'] if item[0] == WORD] != [[WORD, 4]]:
        raise ValueError('Independent original VBlank read/OR/write model differs')
    for address, width, value in expected:
        for base, data in before.items():
            if base <= address and address + width <= base + len(data):
                data[address-base:address-base+width] = value.to_bytes(width, 'little')
                break
        else:
            raise ValueError('Original model write escaped mapped context')
    if any(bytes(cpu.mem_read(base, len(data))) != bytes(data) for base, data in before.items()):
        raise ValueError('Original flag neighbor/context model differs')
    return dict(actualReturn=True, case=case, expectedOrderedWrites=expected, execution=result)


def proof():
    layout = engine.measured_layout()
    modules, unused = linker.namespace('dwc/utility.bin/move/child.srl')
    owners = [name for name, item in modules.items() if int(item['base'], 0) <= WORD < int(item['base'], 0) + item['bytes']
        or int(item['bssStart'], 0) <= WORD < int(item['bssEnd'], 0)]
    if owners:
        raise ValueError('Reserved runtime word unexpectedly belongs to initialized/module BSS')
    try:
        linker.data_binding({'program': 'dwc/utility.bin/move/child.srl'}, WORD, modules)
    except ValueError as error:
        refusal = str(error)
    else:
        raise ValueError('Unchanged unknown-data guard unexpectedly accepted reserved word')
    cases = [{'flags': flags, 'counter': counter} for flags in (0, 1, 16, 0x80000000, 0xFFFFFFFF) for counter in (0, 0xFFFFFFFF)]
    records = [native(case, seed) for seed, case in enumerate(cases)]
    if not all(item['actualReturn'] for item in records):
        raise ValueError('Supported original read/write context did not return')
    cap = native(cases[0], 0, 1)
    if cap['actualReturn']:
        raise ValueError('Exhausted original prefix acquired return credit')
    return {'program': 'dwc/utility.bin/move/child.srl', 'processor': 'arm7', 'address': hex(WORD), 'width': 4,
        'mode': 'data', 'classification': 'fixed-platform-reserved-interrupt-check-word',
        'inputModuleSha256': engine.WRAM_SHA, 'moduleStorageOwnership': [],
        'sourceDataExtentCredit': 0, 'initializedDenominatorDelta': 0, 'sourceCredit': 0,
        'primaryReference': reference(), 'originalReferences': references(layout),
        'unchangedDataGuardRefusal': refusal, 'originalReturnRecords': records, 'actualOriginalReturns': len(records),
        'providerReplacements': [], 'unsupportedControls': [cap], 'unsupportedReturnCredit': 0,
        'limitations': ['Synthetic mapped ARM7 context only; no BIOS input, execution or physical IRQ/concurrency proof',
            'Five direct canonical literal-reference sites are bounded; opaque address production is not exhaustively inventoried',
            'Independent original VBlank producer proves read-modify-write/preservation; original clear/wait consumer remains unproved',
            'Only the four-byte platform word is characterized, never surrounding reserved storage or arbitrary absolute ordinary data']}


def main():
    report = dict(schemaVersion=1, generator=Path(__file__).name, generatorSha256=engine.digest(Path(__file__).read_bytes()), **proof())
    write_json(REPORT, report)
    print(json.dumps(dict(report=REPORT.relative_to(ROOT).as_posix(), sha256=engine.digest(REPORT.read_bytes()), actualOriginalReturns=report['actualOriginalReturns'], sourceCredit=0)))


if __name__ == '__main__':
    main()
