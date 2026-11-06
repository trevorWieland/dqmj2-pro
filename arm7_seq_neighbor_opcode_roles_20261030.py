import hashlib
import json
import random
from pathlib import Path
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_REG_PC
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
MAIN_SHA = 'ba72b9926ea8d39a387005abcad9c3baa593dbd7e9f77777de7680a15f6a3416'
WORDS = {0x027F00D0: (0x03800A0A, 0xA000), 0x027F00EC: (0x03800A09, 0x9000)}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def execute(pc, word, mask, flags, seed):
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    base = pc & ~0xFFF
    cpu.mem_map(base, 0x1000)
    cpu.mem_write(pc, word.to_bytes(4, 'little'))
    rng = random.Random(20261030 + seed)
    before = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    before[0] = (0, 1, 0xFFFFFFFF, 0x12345678, 0xA000, 0x9000)[seed]
    status = flags << 28 | 0xD3
    cpu.reg_write(UC_ARM_REG_CPSR, status)
    for register, value in zip(match_runtime.REGISTERS, before):
        cpu.reg_write(register, value)
    cpu.emu_start(pc, pc + 4, count=1, timeout=100000)
    expected = list(before)
    if flags & 4:
        expected[0] |= mask
    actual = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    if actual != expected or cpu.reg_read(UC_ARM_REG_PC) != pc + 4 or cpu.reg_read(UC_ARM_REG_CPSR) != status:
        raise ValueError('Original conditional ORR instruction/boundary model differs')
    if bytes(cpu.mem_read(pc, 4)) != word.to_bytes(4, 'little'):
        raise ValueError('Opcode role probe modified code')
    return {'flags': flags, 'seed': seed, 'pcAfter': pc + 4, 'r0After': actual[0], 'actualBoundaryStop': True, 'functionReturnCredit': 0}


def segment(raw, module_base, control, input_word, index):
    start, stop, context, output = 0x027F00A8, 0x027F0100, 0x023D0000, 0x04808000
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(0x027F0000, 0x1000)
    cpu.mem_write(0x027F0000, raw[0x027F0000 - module_base:0x027F1000 - module_base])
    cpu.mem_map(context, 0x1000)
    cpu.mem_write(context + 0x14, control.to_bytes(2, 'little'))
    cpu.mem_map(output, 0x1000)
    cpu.mem_write(output, bytes([0xA5]) * 0x1000)
    registers = [0x12345678 + offset for offset in range(len(match_runtime.REGISTERS))]
    registers[5], registers[8], registers[10] = input_word, context, index
    for register, value in zip(match_runtime.REGISTERS, registers):
        cpu.reg_write(register, value)
    cpu.reg_write(UC_ARM_REG_CPSR, 0xD3)
    writes, visited = [], []
    def write(machine, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(machine, pc, size, unused):
        if not start <= pc < stop:
            raise ValueError('Opcode-role original segment escaped its stated boundaries')
        visited.append(pc)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.emu_start(start, stop, count=64, timeout=100000)
    masked = input_word & 0x3FFF
    selector = control & 0xC
    if selector == 4:
        result, status, path = (masked >> 1) | 0xA000, 0x600000D3, 'A000'
    else:
        selector = control & 0xFC
        path = '9000' if selector == 0x50 else '8000'
        result = (masked >> 1) | (0x9000 if selector == 0x50 else 0x8000)
        status = (((selector - 0x50) & 0xFFFFFFFF) >> 31 << 31) | (int(selector == 0x50) << 30) | (int(selector >= 0x50) << 29) | 0xD3
    expected = list(registers)
    expected[:5] = [result, masked >> 1, masked, output + 0xA0 + index * 4, control]
    expected_output = bytearray([0xA5] * 0x1000)
    expected_output[0xA0 + index * 4:0xA2 + index * 4] = result.to_bytes(2, 'little')
    if [cpu.reg_read(register) for register in match_runtime.REGISTERS] != expected or cpu.reg_read(UC_ARM_REG_CPSR) != status:
        raise ValueError('Original enclosing segment register/flag model differs')
    if cpu.reg_read(UC_ARM_REG_PC) != stop or writes != [[output + 0xA0 + index * 4, 2, result]]:
        raise ValueError('Original enclosing segment boundary/store model differs')
    if bytes(cpu.mem_read(output, 0x1000)) != bytes(expected_output):
        raise ValueError('Synthetic peripheral-page guard/model differs')
    return {'controlHalfword': control, 'inputWord': input_word, 'index': index, 'selectedPath': path, 'result': result,
        'visited': visited, 'actualBoundaryStop': True, 'functionReturnCredit': 0,
        'syntheticOutputPage': True, 'physicalIoPerformed': False}


def evidence(layout):
    modules = {row['id']: row for row in layout['modules']}
    main = modules['arm7-main']
    raw = (ROOT / main['binary']).read_bytes()
    if digest(raw) != MAIN_SHA:
        raise ValueError('Opcode-role original main module changed')
    inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    function = next(row for row in inventory['functions'] if row['module'] == 'arm7-main' and row['address'] == '0x27eff00')
    if function['mode'] != 'arm' or function['ranges'] != [['0x27eff00', '0x27f0114']]:
        raise ValueError('Opcode-role enclosing configured ARM code range changed')
    base = int(main['base'], 0)
    probes = []
    for pc, (word, mask) in WORDS.items():
        value = int.from_bytes(raw[pc - base:pc - base + 4], 'little')
        pair = list(Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(raw[pc - base:pc - base + 8], pc))
        if value != word or [(row.mnemonic, row.op_str) for row in pair] != [('orreq', 'r0, r0, #' + hex(mask)), ('strheq', 'r0, [r3]')]:
            raise ValueError('Specific opcode role or conditional store context changed')
        records = [execute(pc, word, mask, flags, seed) for flags in range(16) for seed in range(6)]
        probes.append({'module': 'arm7-main', 'processor': 'arm7', 'program': '', 'pc': hex(pc), 'mode': 'arm',
            'word': hex(word), 'operation': 'ORREQ r0,r0,' + hex(mask), 'followedBy': 'STRHEQ r0,[r3]',
            'enclosingConfiguredRoot': '0x27eff00', 'codeRange': ['0x27eff00', '0x27f0114'],
            'records': records, 'actualInstructionBoundaryStops': len(records), 'functionReturnCredit': 0})
    literal_refs = []
    targets = set(WORDS)
    binaries = {key: (ROOT / value['binary']).read_bytes() for key, value in modules.items()}
    for function in inventory['functions']:
        if function.get('mode') not in ('arm', 'thumb'):
            continue
        mode, data = function['mode'], binaries[function['module']]
        module_base = int(modules[function['module']]['base'], 0)
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if mode == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for first, last in function['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(data[first - module_base:last - module_base], first):
                for operand in instruction.operands:
                    if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                        pc_base = instruction.address + 8 if mode == 'arm' else (instruction.address + 4) & ~3
                        target = pc_base + operand.mem.disp
                        if target & ~3 in targets:
                            literal_refs.append({'pc': hex(instruction.address), 'target': hex(target)})
    if literal_refs:
        raise ValueError('Opcode coincidence also has an unresolved PC-relative data use')
    segments = [segment(raw, base, control, value, index) for control in (0, 4, 0x50, 0x54, 0xFC)
        for value in (0, 1, 0xFFFFFFFF, 0x12345678) for index in (0, 1, 7)]
    if {row['selectedPath'] for row in segments} != {'8000', '9000', 'A000'}:
        raise ValueError('Opcode-role original segment branch outcomes incomplete')
    return {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'mainModuleSha256': MAIN_SHA,
        'probes': probes, 'originalEnclosingSegment': {'range': ['0x27f00a8', '0x27f0100'], 'records': segments,
            'actualBoundaryStops': len(segments), 'functionReturnCredit': 0},
        'knownPcRelativeDataReferencesToOpcodeWords': [], 'functionOrSourceCredit': 0,
        'limitations': ['Specific raw words are decoded and independently executed as conditional bit-setting instructions',
            'No enclosing532-byte function return, reconstructed C or global computed/dual-use-data absence is claimed']}


def qualify(layout, module, pc, word):
    if module != 'arm7-main' or pc not in WORDS or WORDS[pc][0] != word:
        raise ValueError('Unqualified initialized word resembling a function interior')
    proof = evidence(layout)
    probe = next(row for row in proof['probes'] if int(row['pc'], 0) == pc)
    return dict(probe, originalEnclosingSegment=proof['originalEnclosingSegment'],
        knownPcRelativeDataReferencesToOpcodeWords=proof['knownPcRelativeDataReferencesToOpcodeWords'],
        opaqueDualUseDataAbsenceClaim=False, sourceOrFunctionReturnCredit=0)
