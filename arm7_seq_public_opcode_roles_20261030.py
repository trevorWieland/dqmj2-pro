import hashlib
import json
from pathlib import Path
import match_runtime
import arm7_seq_neighbor_opcode_roles_20261030 as isolated
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import ARM_REG_PC
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_HOOK_CODE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR

ROOT = Path(__file__).resolve().parent
RAW_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
PC, WORD, MASK = 0x038047EC, 0x03800406, 0x06000000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def segment(raw, module_base, control, input_word, seed):
    start, stop, output = 0x038047E0, 0x038047F4, 0x023D0040
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(0x03804000, 0x1000)
    cpu.mem_write(0x03804000, raw[0x03804000 - module_base:0x03805000 - module_base])
    cpu.mem_map(output & ~0xFFF, 0x1000)
    initial = bytearray(bytes([0xA5]) * 0x1000)
    initial[0x40:0x44] = input_word.to_bytes(4, 'little')
    cpu.mem_write(output & ~0xFFF, bytes(initial))
    registers = [0x13579BDF + index for index in range(len(match_runtime.REGISTERS))]
    registers[0], registers[4], registers[7] = (0, 0xFFFFFFFF, 0x87654321)[seed], control, output
    for register, value in zip(match_runtime.REGISTERS, registers):
        cpu.reg_write(register, value)
    cpu.reg_write(UC_ARM_REG_CPSR, seed << 28 | 0xD3)
    reads, writes, visited = [], [], []
    def read(machine, access, address, size, value, unused):
        reads.append([address, size])
    def write(machine, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(machine, pc, size, unused):
        if not start <= pc < stop:
            raise ValueError('Public SDK opcode segment escaped its explicit boundary')
        visited.append(pc)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.emu_start(start, stop, count=5, timeout=100000)
    result = (control - 2) & 0xFFFFFFFF
    status = (result & 0x80000000) | (int(control == 2) << 30) | (int(control >= 2) << 29)
    status |= (int(bool((control ^ 2) & (control ^ result) & 0x80000000)) << 28) | 0xD3
    expected = list(registers)
    if control == 2:
        expected[0] = input_word | MASK
        initial[0x40:0x44] = expected[0].to_bytes(4, 'little')
    expected_reads = [[output, 4]] if control == 2 else []
    expected_writes = [[output, 4, expected[0]]] if control == 2 else []
    if [cpu.reg_read(register) for register in match_runtime.REGISTERS] != expected or cpu.reg_read(UC_ARM_REG_CPSR) != status:
        raise ValueError('Original CMP/conditional mask segment register/flag model differs')
    if cpu.reg_read(UC_ARM_REG_PC) != stop or reads != expected_reads or writes != expected_writes:
        raise ValueError('Original opcode segment actual boundary/read/store model differs')
    if bytes(cpu.mem_read(output & ~0xFFF, 0x1000)) != bytes(initial):
        raise ValueError('Opcode-role synthetic target-page memory guard differs')
    return {'controlWord': control, 'inputWord': input_word, 'seed': seed, 'visited': visited,
        'conditionalStoreExecuted': control == 2, 'actualBoundaryStop': True, 'functionReturnCredit': 0,
        'reads': reads, 'writes': writes, 'syntheticOutputPage': True, 'physicalIoPerformed': False}


def evidence(layout):
    modules = {row['id']: row for row in layout['modules']}
    current = modules['arm7-wram']
    raw = (ROOT / current['binary']).read_bytes()
    if digest(raw) != RAW_SHA:
        raise ValueError('Public SDK opcode-role original WRAM image differs')
    inventory = json.loads((ROOT / 'evidence/arm7/ghidra-runtime-inventory.json').read_text())
    enclosing = next(row for row in inventory['functions'] if row['module'] == 'arm7-wram' and row['address'] == '0x38046ac')
    if enclosing['mode'] != 'arm' or enclosing['ranges'] != [['0x38046ac', '0x3804890']]:
        raise ValueError('Public SDK opcode-role configured enclosing range differs')
    base = int(current['base'], 0)
    if int.from_bytes(raw[PC - base:PC - base + 4], 'little') != WORD:
        raise ValueError('Specific original opcode-word value differs')
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    instructions = list(decoder.disasm(raw[PC - base:PC - base + 8], PC))
    if [(row.mnemonic, row.op_str) for row in instructions] != [('orreq', 'r0, r0, #0x6000000'), ('streq', 'r0, [r7]')]:
        raise ValueError('Public SDK opcode-word decoded mask/store role differs')
    literal_refs = []
    for function in inventory['functions']:
        if function.get('mode') not in ('arm', 'thumb'):
            continue
        module = modules[function['module']]
        module_base, data = int(module['base'], 0), (ROOT / module['binary']).read_bytes()
        mode = function['mode']
        decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM if mode == 'arm' else CS_MODE_THUMB)
        decoder.detail = True
        for first, last in function['ranges']:
            first, last = int(first, 0), int(last, 0)
            for instruction in decoder.disasm(data[first - module_base:last - module_base], first):
                for operand in instruction.operands:
                    if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                        pc_base = instruction.address + 8 if mode == 'arm' else (instruction.address + 4) & ~3
                        target = pc_base + operand.mem.disp
                        if target & ~3 == PC:
                            literal_refs.append({'pc': hex(instruction.address), 'target': hex(target)})
    if literal_refs:
        raise ValueError('Opcode coincidence also has unresolved known PC-relative data use')
    probes = [isolated.execute(PC, WORD, MASK, flags, seed) for flags in range(16) for seed in range(6)]
    segments = [segment(raw, base, control, value, seed) for control in (0, 1, 2, 3, 0x7FFFFFFF, 0x80000000, 0x80000001, 0xFFFFFFFF)
        for value in (0, 1, MASK, 0xFFFFFFFF, 0x12345678) for seed in range(3)]
    return {'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()), 'moduleSha256': RAW_SHA,
        'probe': {'module': 'arm7-wram', 'processor': 'arm7', 'program': '', 'pc': hex(PC), 'mode': 'arm', 'word': hex(WORD),
            'operation': 'ORREQ r0,r0,0x06000000', 'followingInstruction': 'STREQ r0,[r7]',
            'enclosingConfiguredRoot': '0x38046ac', 'codeRange': ['0x38046ac', '0x3804890'], 'records': probes},
        'originalEnclosingSegment': {'range': ['0x38047e0', '0x38047f4'], 'records': segments, 'actualBoundaryStops': len(segments),
            'functionReturnCredit': 0}, 'knownPcRelativeDataReferencesToOpcodeWords': [], 'functionOrSourceCredit': 0,
        'limitations': ['This specific word is independently executed as an original conditional bit-setting instruction',
            'Synthetic target page only; no physical peripheral operations or complete enclosing484-byte function return',
            'No absence of opaque computed producers or global dual-use-data claim']}


def qualify(layout, module, pc, word):
    if (module, pc, word) != ('arm7-wram', PC, WORD):
        raise ValueError('Unqualified raw word resembling a public-SDK function interior')
    proof = evidence(layout)
    return dict(proof['probe'], originalEnclosingSegment=proof['originalEnclosingSegment'],
        knownPcRelativeDataReferencesToOpcodeWords=[], opaqueDualUseDataAbsenceClaim=False, sourceOrFunctionReturnCredit=0)
