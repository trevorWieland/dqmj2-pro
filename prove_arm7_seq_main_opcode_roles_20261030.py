import hashlib
import itertools
import json
import sys
from pathlib import Path
import arm7_runtime
import match_runtime
import arm7_seq_neighbor_opcode_roles_20261030 as isolated
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_REG_PC
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from project import write_json

ROOT = Path(__file__).resolve().parent
CONSUMERS = ROOT / 'evidence/attempts/arm7-seq-main-consumers-20261030-v2.json'
CONSUMERS_SHA = 'caca5dc539c39db67a8308a81a4823d8a9b69ab92a481a5aae0fafe7a3a2f599'
SPECS = [
    {'module': 'arm7-wram', 'pc': 0x037F8494, 'start': 0x037F8490, 'stop': 0x037F84A0, 'mask': 64, 'cmp': [1, 128], 'extend16': True},
    {'module': 'arm7-wram', 'pc': 0x037F84A8, 'start': 0x037F84A4, 'stop': 0x037F84B4, 'mask': 128, 'cmp': [1, 64], 'extend16': True},
    {'module': 'arm7-wram', 'pc': 0x037F8E38, 'start': 0x037F8E30, 'stop': 0x037F8E40, 'mask': 32, 'baseReg': 6, 'disp': 124, 'width': 2, 'literalR1': True},
    {'module': 'arm7-wram', 'pc': 0x038010AC, 'start': 0x038010A4, 'stop': 0x038010B4, 'mask': 16, 'baseReg': 8, 'disp': 0, 'width': 1, 'cmp': [4, 0]},
    {'module': 'arm7-wram', 'pc': 0x03802154, 'start': 0x03802150, 'stop': 0x0380215C, 'mask': 128, 'baseReg': 4, 'disp': 0, 'width': 1},
    {'module': 'arm7-main', 'pc': 0x027F28E8, 'start': 0x027F28E0, 'stop': 0x027F28F0, 'mask': 1, 'baseReg': 13, 'disp': 34, 'width': 2, 'cmp': [0, 0]},
    {'module': 'arm7-main', 'pc': 0x027F3D64, 'start': 0x027F3D60, 'stop': 0x027F3D6C, 'mask': 4, 'baseReg': 9, 'disp': 10, 'width': 2},
    {'module': 'arm7-main', 'pc': 0x027F3DB4, 'start': 0x027F3DB0, 'stop': 0x027F3DC4, 'mask': 2, 'baseReg': 9, 'disp': 10, 'width': 2, 'unconditionalLoad': True, 'clearOtherwise': True},
    {'module': 'arm7-main', 'pc': 0x027F3F0C, 'start': 0x027F3F08, 'stop': 0x027F3F14, 'mask': 16, 'baseReg': 9, 'disp': 10, 'width': 2},
    {'module': 'arm7-main', 'pc': 0x027F3F2C, 'start': 0x027F3F28, 'stop': 0x027F3F34, 'mask': 32, 'baseReg': 9, 'disp': 10, 'width': 2},
]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cmp_flags(left, right):
    result = (left - right) & 0xFFFFFFFF
    return (result & 0x80000000) | (int(left == right) << 30) | (int(left >= right) << 29) | (int(bool((left ^ right) & (left ^ result) & 0x80000000)) << 28)


def segment(spec, module, raw, flags, value, control):
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    base = int(module['base'], 0)
    cpu.mem_map(base, (len(raw) + 0xFFF) // 0x1000 * 0x1000)
    cpu.mem_write(base, raw)
    data, pointer = 0x023D0000, 0x023D0100
    cpu.mem_map(data, 0x1000)
    memory = bytearray(bytes([0xA5]) * 0x1000)
    registers = [0x12345678 + index for index in range(len(match_runtime.REGISTERS))]
    registers[0] = value if spec.get('extend16') else 0x87654321
    width = spec.get('width', 0)
    if width:
        registers[spec['baseReg']] = pointer
        target = pointer + spec['disp']
        masked = value & ((1 << (width * 8)) - 1)
        memory[target - data:target - data + width] = masked.to_bytes(width, 'little')
    if spec.get('cmp'):
        registers[spec['cmp'][0]] = control
        status = cmp_flags(control, spec['cmp'][1]) | 0xD3
    else:
        status = flags << 28 | 0xD3
    cpu.mem_write(data, bytes(memory))
    for register, word in zip(match_runtime.REGISTERS, registers):
        cpu.reg_write(register, word)
    cpu.reg_write(UC_ARM_REG_CPSR, flags << 28 | 0xD3)
    expected = list(registers)
    eq = bool(status & 0x40000000)
    expected_reads, expected_writes = [], []
    if width and (eq or spec.get('unconditionalLoad')):
        expected[0] = masked
        expected_reads.append([target, width])
    if eq:
        expected[0] |= spec['mask']
        if spec.get('extend16'):
            expected[0] &= 0xFFFF
    elif spec.get('clearOtherwise'):
        expected[0] &= ~spec['mask']
    if width and (eq or spec.get('clearOtherwise')):
        stored = expected[0] & ((1 << (width * 8)) - 1)
        memory[target - data:target - data + width] = stored.to_bytes(width, 'little')
        expected_writes.append([target, width, stored])
    if spec.get('literalR1'):
        pc = 0x037F8E34
        word = int.from_bytes(raw[pc - base:pc - base + 4], 'little')
        literal = pc + 8 + (word & 0xFFF)
        expected[1] = int.from_bytes(raw[literal - base:literal - base + 4], 'little')
        expected_reads.insert(1 if eq else 0, [literal, 4])
    reads, writes, visited = [], [], []
    def read(machine, access, address, size, word, unused):
        reads.append([address, size])
    def write(machine, access, address, size, word, unused):
        writes.append([address, size, word & ((1 << (size * 8)) - 1)])
    def code(machine, pc, size, unused):
        if not spec['start'] <= pc < spec['stop']:
            raise ValueError('Original opcode-role window escaped its explicit boundaries')
        visited.append(pc)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.emu_start(spec['start'], spec['stop'], count=16, timeout=100000)
    if [cpu.reg_read(register) for register in match_runtime.REGISTERS] != expected or cpu.reg_read(UC_ARM_REG_CPSR) != status:
        raise ValueError('Independent original conditional-mask window full-register/flag model differs')
    if cpu.reg_read(UC_ARM_REG_PC) != spec['stop'] or reads != expected_reads or writes != expected_writes:
        raise ValueError('Original opcode-role read/write/actual-boundary model differs')
    if bytes(cpu.mem_read(data, 0x1000)) != bytes(memory) or bytes(cpu.mem_read(base, len(raw))) != raw:
        raise ValueError('Original opcode-role whole-memory preservation/model differs')
    return {'flags': flags, 'inputWord': value, 'control': control, 'actualBoundaryStop': True,
        'visited': visited, 'reads': reads, 'writes': writes, 'functionReturnCredit': 0, 'noPhysicalIo': True}


def main():
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned original opcode-window runtime differs')
    if digest(CONSUMERS.read_bytes()) != CONSUMERS_SHA:
        raise ValueError('Frozen explicit raw-word consumer audit changed')
    consumers = json.loads(CONSUMERS.read_text())
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    modules = {row['id']: row for row in layout['modules']}
    binaries = {name: (ROOT / row['binary']).read_bytes() for name, row in modules.items()}
    inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    if {(row['module'], int(row['storage'], 0)) for row in consumers['rawInteriorOrPoolWords']} != {(row['module'], row['pc']) for row in SPECS}:
        raise ValueError('Specific ten opcode-word identity set differs')
    results, controls = [], []
    for spec in SPECS:
        module, raw = modules[spec['module']], binaries[spec['module']]
        if digest(raw) != module['sha256']:
            raise ValueError('Measured opcode-role source module changed')
        base = int(module['base'], 0)
        owners = [row for row in inventory['functions'] if row['module'] == spec['module'] and row['mode'] == 'arm'
            and any(int(a, 0) <= spec['pc'] < int(b, 0) for a, b in row['ranges'])]
        if len(owners) != 1:
            raise ValueError('Opcode word has no unique configured ARM instruction owner')
        word = int.from_bytes(raw[spec['pc'] - base:spec['pc'] - base + 4], 'little')
        decoded = next(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(raw[spec['pc'] - base:spec['pc'] - base + 4], spec['pc']))
        operand_text = 'r0, r0, #' + (hex(spec['mask']) if spec['mask'] >= 10 else str(spec['mask']))
        if decoded.mnemonic != 'orreq' or decoded.op_str != operand_text:
            raise ValueError('Specific native raw-word conditional ORR semantics differ')
        probes = [isolated.execute(spec['pc'], word, spec['mask'], flags, seed) for flags in range(16) for seed in range(6)]
        selected_controls = [spec['cmp'][1], 0 if spec['cmp'][1] else 1, 0xFFFFFFFF] if spec.get('cmp') else [0]
        records = [segment(spec, module, raw, flags, value, control) for flags, value, control in itertools.product(range(16),
            (0, 1, 0xFFFF, 0xFFFFFFFF, 0x12345678), selected_controls)]
        changed = bytearray(raw)
        changed[spec['pc'] - base:spec['pc'] - base + 4] = (0xE1A00000).to_bytes(4, 'little')
        try:
            segment(spec, module, bytes(changed), 4, 0, spec['cmp'][1] if spec.get('cmp') else 0)
        except Exception as error:
            controls.append({'module': spec['module'], 'pc': hex(spec['pc']), 'name': 'omitted-original-conditional-bit-set',
                'rejected': True, 'reason': str(error)})
        else:
            raise ValueError('Omitted original opcode instruction escaped independent window model')
        results.append({'identity': {'program': '', 'processor': 'arm7', 'module': spec['module'], 'mode': 'arm',
            'pc': hex(spec['pc']), 'word': hex(word), 'inputModuleSha256': module['sha256']},
            'owner': owners[0], 'operation': decoded.mnemonic + ' ' + decoded.op_str, 'isolatedInstructionBoundaryStops': probes,
            'originalWindow': {'start': hex(spec['start']), 'stop': hex(spec['stop']), 'records': records},
            'knownInstructionRoleQualified': True, 'opaqueDualUseDataAbsenceClaim': False, 'sourceOrFunctionReturnCredit': 0})
    data_refs = []
    targets = {(row['module'], row['pc']) for row in SPECS}
    for function in inventory['functions']:
        mode = function.get('mode')
        if mode not in ('arm', 'thumb'):
            continue
        raw, module = binaries[function['module']], modules[function['module']]
        base = int(module['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if mode == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for first, last in function['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(raw[first - base:last - base], first):
                for operand in instruction.operands:
                    if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                        pc_base = instruction.address + 8 if mode == 'arm' else (instruction.address + 4) & ~3
                        target = pc_base + operand.mem.disp
                        if (function['module'], target & ~3) in targets:
                            data_refs.append({'module': function['module'], 'pc': hex(instruction.address), 'target': hex(target)})
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorDependencies': [{'path': name, 'sha256': digest((ROOT / name).read_bytes())} for name in ('arm7_runtime.py', 'match_runtime.py', 'match_lowlevel.py', 'arm7_seq_neighbor_opcode_roles_20261030.py', 'project.py')],
        'runtime': {'python': '.'.join(map(str, sys.version_info[:3])), 'unicorn': unicorn.__version__, 'cpu': 'TI925T ARMv4T surrogate'},
        'romSha256': consumers['romSha256'], 'consumerAudit': {'path': CONSUMERS.relative_to(ROOT).as_posix(), 'sha256': CONSUMERS_SHA},
        'roles': results, 'knownPcRelativeDataReadsAddressingSpecificOpcodeWords': data_refs,
        'isolatedInstructionBoundaryStops': sum(len(row['isolatedInstructionBoundaryStops']) for row in results),
        'originalEnclosingWindowBoundaryStops': sum(len(row['originalWindow']['records']) for row in results),
        'negativeControls': controls, 'allControlsRejected': all(row['rejected'] for row in controls),
        'sourceOrFunctionReturnCredit': 0, 'migrationApproved': False, 'sharedFilesEdited': False,
        'limitations': ['Only these ten exact original words/instruction owners and bounded neighboring instruction windows are qualified',
            'No blanket executable-section exclusion, complete containing-function execution or global opaque/computed-data absence is claimed',
            'Original modules and all accepted code remain unchanged; synthetic RAM replaces no whole-game provider and performs no physical I/O']}
    destination = ROOT / 'evidence/attempts/arm7-seq-main-opcode-word-roles-20261030.json'
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'specificWords': len(results), 'isolatedBoundaryStops': report['isolatedInstructionBoundaryStops'],
        'originalWindowBoundaryStops': report['originalEnclosingWindowBoundaryStops'], 'controls': len(controls),
        'pcRelativeDataReads': len(data_refs), 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
