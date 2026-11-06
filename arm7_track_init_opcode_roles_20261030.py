import hashlib
import json
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_opcode_roles_20261030 as previous_roles
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_REG_PC
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
PC, WORD, MASK = 0x027E68EC, 0x03800902, 0x8000
MAIN_SHA = 'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def segment(raw, base, selector, halfword, input_word):
    start, stop, context, stack = 0x027E68D8, 0x027E6900, 0x023D0000, 0x023E0000
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    for first in (0x027E6000, context, stack):
        cpu.mem_map(first, 0x1000)
    cpu.mem_write(0x027E6000, raw[0x027E6000 - base:0x027E7000 - base])
    cpu.mem_write(context + 0x1C, selector.to_bytes(4, 'little'))
    cpu.mem_write(context + 0x7C, (0x87654321).to_bytes(4, 'little'))
    original_stack = bytearray([0xA5] * 0x1000)
    original_stack[0x15C:0x15E] = halfword.to_bytes(2, 'little')
    cpu.mem_write(stack, bytes(original_stack))
    registers = [0x12345678 + index for index in range(len(match_runtime.REGISTERS))]
    registers[6], registers[11], registers[-2] = input_word, context, stack + 0x100
    cpu.reg_write(UC_ARM_REG_CPSR, 0xD3)
    for register, value in zip(match_runtime.REGISTERS, registers):
        cpu.reg_write(register, value)
    writes, visited = [], []
    def write(machine, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(machine, pc, size, unused):
        if not start <= pc < stop:
            raise ValueError('Initializer opcode-role segment escaped stated bounds')
        visited.append(pc)
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.emu_start(start, stop, count=64, timeout=100000)
    result = halfword | MASK if selector == 1 else halfword
    expected = list(registers)
    expected[:4] = [stack + 0x160, input_word & 65535, result, 0x87654321]
    status = (((selector - 1) & 0xFFFFFFFF) >> 31 << 31) | (int(selector == 1) << 30) | (int(selector >= 1) << 29) | 0xD3
    expected_writes = [[stack + 0x15C, 2, result]] if selector == 1 else []
    expected_stack = bytearray(original_stack)
    expected_stack[0x15C:0x15E] = result.to_bytes(2, 'little')
    if [cpu.reg_read(register) for register in match_runtime.REGISTERS] != expected or cpu.reg_read(UC_ARM_REG_CPSR) != status:
        raise ValueError('Original initializer-role bounded segment register/flag model differs')
    if cpu.reg_read(UC_ARM_REG_PC) != stop or writes != expected_writes or bytes(cpu.mem_read(stack, 0x1000)) != bytes(expected_stack):
        raise ValueError('Original initializer-role bounded segment stack/store/boundary model differs')
    return {'selector': selector, 'initialHalfword': halfword, 'inputWord': input_word, 'result': result, 'visited': visited,
        'actualBoundaryStop': True, 'functionReturnCredit': 0, 'selectedPath': 'set8000' if selector == 1 else 'unchanged'}


def evidence(layout):
    modules = {row['id']: row for row in layout['modules']}
    module = modules['arm7-main']
    raw, base = (ROOT / module['binary']).read_bytes(), int(module['base'], 0)
    if digest(raw) != MAIN_SHA or int.from_bytes(raw[PC - base:PC - base + 4], 'little') != WORD:
        raise ValueError('Specific original initializer-role word/module changed')
    inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    enclosing = next(row for row in inventory['functions'] if row['module'] == 'arm7-main' and row['address'] == '0x27e6434')
    if enclosing['mode'] != 'arm' or enclosing['ranges'] != [['0x27e6434', '0x27e6924']]:
        raise ValueError('Specific enclosing configured ARM function changed')
    pair = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(raw[PC - base:PC - base + 8], PC))
    if [(row.mnemonic, row.op_str) for row in pair] != [('orreq', 'r0, r0, #0x8000'), ('strheq', 'r0, [sp, #0x5c]')]:
        raise ValueError('Initializer-specific conditional opcode/store role changed')
    binaries = {name: (ROOT / meta['binary']).read_bytes() for name, meta in modules.items()}
    refs = []
    for function in inventory['functions']:
        if function.get('mode') not in ('arm', 'thumb'):
            continue
        mode = function['mode']
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if mode == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        current_base = int(modules[function['module']]['base'], 0)
        for first, last in function['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(binaries[function['module']][first - current_base:last - current_base], first):
                for operand in instruction.operands:
                    if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                        pc_base = instruction.address + 8 if mode == 'arm' else (instruction.address + 4) & ~3
                        if (pc_base + operand.mem.disp) & ~3 == PC:
                            refs.append(hex(instruction.address))
    if refs:
        raise ValueError('Initializer opcode word has unresolved known literal-data use')
    records = [previous_roles.execute(PC, WORD, MASK, flags, seed) for flags in range(16) for seed in range(6)]
    segments = [segment(raw, base, selector, value, word) for selector in (0, 1, 0x101)
        for value in (0, 1, 0x7FFF, 0x8000, 0xFFFF) for word in (0, 0xFFFFFFFF, 0x12345678)]
    return {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'mainModuleSha256': MAIN_SHA,
        'processor': 'arm7', 'program': '', 'module': 'arm7-main', 'mode': 'arm', 'pc': hex(PC), 'word': hex(WORD),
        'enclosingConfiguredRoot': '0x27e6434', 'knownPcRelativeDataReferences': [], 'isolatedInstructionRecords': records,
        'actualInstructionBoundaryStops': len(records), 'originalSegment': {'range': ['0x27e68d8', '0x27e6900'], 'records': segments,
            'actualBoundaryStops': len(segments), 'functionReturnCredit': 0}, 'opaqueDualUseDataAbsenceClaim': False,
        'sourceOrFunctionReturnCredit': 0, 'limitations': ['Only this exact original opcode/context is reconciled; no blanket code-section pointer exclusion',
            'No enclosing1264-byte function return/reconstructed source or global computed dual-use-data absence is claimed']}


def qualify(layout, module, pc, word):
    if (module, pc, word) != ('arm7-main', PC, WORD):
        raise ValueError('Unqualified initializer raw word resembling an interior pointer')
    return evidence(layout)
