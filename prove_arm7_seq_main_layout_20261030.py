import hashlib
import json
import random
import struct
import sys
from pathlib import Path
import arm7_runtime
import match_runtime
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_GRP_CALL, CS_GRP_JUMP
from capstone.arm import ARM_REG_PC
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_TI925T, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from project import write_json

ROOT = Path(__file__).resolve().parent
ROM_SHA = '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6'
START, GAP, STOP, END = 0x037FFF54, 0x03800000, 0x038000AC, 0x038000B4


def digest(data):
    return hashlib.sha256(data).hexdigest()


def loader(image, layout):
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(arm7_runtime.BASE, 0x28000)
    cpu.mem_write(arm7_runtime.BASE, image)
    expected, before = {}, {}
    for module in layout['modules'][1:]:
        base = int(module['base'], 0)
        size = ((module['inputBytes'] + module['bssBytes'] + 0xFFF) // 0x1000) * 0x1000
        cpu.mem_map(base, size)
        initial = bytes([0xA5]) * size
        cpu.mem_write(base, initial)
        before[base] = initial
        content = image[module['inputFileOffset']:module['inputFileOffset'] + module['inputBytes']]
        expected[base] = content + bytes(module['bssBytes']) + initial[module['inputBytes'] + module['bssBytes']:]
    return_address = 0x05000000
    cpu.mem_map(return_address, 0x1000)
    registers = [0x12345678 + index for index in range(len(match_runtime.REGISTERS))]
    registers[-1] = return_address
    for register, value in zip(match_runtime.REGISTERS, registers):
        cpu.reg_write(register, value)
    cpu.reg_write(UC_ARM_REG_CPSR, 0xD3)
    expected_hash, observed_hash = hashlib.sha256(), hashlib.sha256()
    total_writes = 0
    for module in layout['modules'][1:]:
        base = int(module['base'], 0)
        for offset in range(0, module['inputBytes'] + module['bssBytes'], 4):
            value = int.from_bytes(expected[base][offset:offset + 4], 'little')
            expected_hash.update(struct.pack('<III', base + offset, 4, value))
            total_writes += 1
    observed_writes, instructions = 0, 0
    def write(machine, access, address, size, value, unused):
        nonlocal observed_writes
        if size != 4 or not any(base <= address < base + len(data) for base, data in expected.items()):
            raise ValueError('Original autoload wrote outside measured module allocations')
        observed_hash.update(struct.pack('<III', address, size, value & 0xFFFFFFFF))
        observed_writes += 1
    def code(machine, pc, size, unused):
        nonlocal instructions
        if not 0x02380118 <= pc < 0x02380184 and pc != 0x02380188:
            raise ValueError('Original autoload left its measured ARM startup routine')
        instructions += 1
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.emu_start(0x02380118, return_address, count=600000, timeout=5000000)
    if cpu.reg_read(UC_ARM_REG_PC) != return_address or observed_writes != total_writes or observed_hash.digest() != expected_hash.digest():
        raise ValueError('Actual original autoload return/copy-zero ordered effects differ')
    if bytes(cpu.mem_read(arm7_runtime.BASE, len(image))) != image:
        raise ValueError('Original autoload changed its source image')
    observed = {}
    for base, data in expected.items():
        actual = bytes(cpu.mem_read(base, len(data)))
        if actual != data:
            raise ValueError('Original autoload whole module/BSS/guard contents differ')
        observed[base] = actual
    return observed, {'originalEntry': '0x2380118', 'actualReturn': True, 'instructionCount': instructions,
        'instructionLimit': 600000, 'timeoutMicroseconds': 5000000, 'sourceImageUnchanged': True,
        'actualWordStores': observed_writes, 'orderedCopyZeroStoresSha256': observed_hash.hexdigest(),
        'fullDestinationAndBssAndGuardChecks': True, 'sourceCredit': 0, 'assemblyCredit': 0}


def gap_probe(wram, fields, shared_present, player_id, increment, seed):
    base, data, player, shared = 0x037F8000, 0x023C0000, 0x023C0100, 0x023C1000
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(base, len(wram))
    cpu.mem_write(base, wram)
    cpu.mem_map(data, 0x4000)
    expected = bytearray(random.Random(20261030 + seed).randbytes(0x4000))
    expected[player - data + 1] = player_id
    for offset, value in zip((0x18, 0x1A, 0x1C), fields):
        expected[player - data + offset:player - data + offset + 2] = value.to_bytes(2, 'little')
    cpu.mem_write(data, bytes(expected))
    pointer = shared if shared_present else 0
    cpu.mem_write(0x03807EDC, pointer.to_bytes(4, 'little'))
    registers = [0x13579BDF + index for index in range(len(match_runtime.REGISTERS))]
    registers[4], registers[7] = player, increment
    for register, value in zip(match_runtime.REGISTERS, registers):
        cpu.reg_write(register, value)
    cpu.reg_write(UC_ARM_REG_CPSR, 0xD3)
    writes, visited, expected_writes = [], [], []
    if shared_present:
        address = shared + player_id * 36 + 0x40
        old = int.from_bytes(expected[address - data:address - data + 4], 'little')
        value = (old + increment) & 0xFFFFFFFF
        expected[address - data:address - data + 4] = value.to_bytes(4, 'little')
        expected_writes.append([address, 4, value])
    product = fields[0] * fields[1] & 0xFFFFFFFF
    signed_product = product - 0x100000000 if product & 0x80000000 else product
    result = (fields[2] + (signed_product >> 8)) & 0xFFFFFFFF
    expected[player - data + 0x1C:player - data + 0x1E] = (result & 0xFFFF).to_bytes(2, 'little')
    expected_writes.append([player + 0x1C, 2, result & 0xFFFF])
    def write(machine, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def code(machine, pc, size, unused):
        if not GAP <= pc < GAP + 64:
            raise ValueError('Original excluded ARM segment escaped its declared boundary')
        visited.append(pc)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.emu_start(GAP, GAP + 64, count=64, timeout=100000)
    predicted = list(registers)
    predicted[:3] = [result, product, fields[0]]
    flags = 0x200000D3 if shared_present else 0x600000D3
    if [cpu.reg_read(register) for register in match_runtime.REGISTERS] != predicted or cpu.reg_read(UC_ARM_REG_CPSR) != flags:
        raise ValueError('Original excluded ARM segment full register/flag model differs')
    if cpu.reg_read(UC_ARM_REG_PC) != GAP + 64 or writes != expected_writes or bytes(cpu.mem_read(data, 0x4000)) != bytes(expected):
        raise ValueError('Original excluded ARM segment memory/store/boundary model differs')
    expected_wram = bytearray(wram)
    expected_wram[0x03807EDC - base:0x03807EDC - base + 4] = pointer.to_bytes(4, 'little')
    if bytes(cpu.mem_read(base, len(wram))) != bytes(expected_wram):
        raise ValueError('Original excluded segment changed executable/module/BSS input')
    return {'fields': fields, 'sharedPresent': shared_present, 'playerId': player_id, 'rawIncrement': increment,
        'visited': visited, 'actualBoundaryStop': True, 'functionReturnCredit': 0, 'writes': writes,
        'rawAdjacencyContext': player_id == 255, 'noPhysicalIo': True}


def main():
    import unicorn
    if sys.version_info[:3] != (3, 13, 5) or unicorn.__version__ != '2.1.4':
        raise ValueError('Pinned ARM7 layout execution runtime differs')
    rom = ROOT / 'inputs/game.nds'
    with rom.open('rb') as stream:
        rom_hash = hashlib.file_digest(stream, 'sha256').hexdigest()
        stream.seek(0x30)
        offset, entry, load, length = struct.unpack('<IIII', stream.read(16))
        stream.seek(offset)
        arm7_image = stream.read(length)
    if rom_hash != ROM_SHA or entry != arm7_runtime.BASE or load != arm7_runtime.BASE:
        raise ValueError('Qualified original ARM7 ROM header differs')
    image = (ROOT / 'extract/arm7/arm7.bin').read_bytes()
    if arm7_image != image:
        raise ValueError('ROM stored ARM7 image and measured loader input differ')
    layout = arm7_runtime.derive(image)
    owners = [row for row in layout['modules'] if int(row['base'], 0) <= START and END <= int(row['runtimeEnd'], 0)]
    if len(owners) != 1 or owners[0]['id'] != 'arm7-wram':
        raise ValueError('Candidate full span has no unique initialized ARM7 loader module')
    owner, base = owners[0], int(owners[0]['base'], 0)
    inventory_path = ROOT / 'evidence/arm7/ghidra-runtime-inventory.json'
    inventory = json.loads(inventory_path.read_text())
    function = next(row for row in inventory['functions'] if row['module'] == 'arm7-wram' and int(row['address'], 0) == START)
    if function['ranges'] != [['0x37fff54', '0x3800000'], ['0x3800040', '0x38000ac']] or function['bodyBytes'] != 280:
        raise ValueError('Original discontiguous configured function changed')
    raw = (ROOT / owner['binary']).read_bytes()
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    instructions = list(decoder.disasm(raw[START - base:STOP - base], START))
    if len(instructions) != 86 or any(row.size != 4 for row in instructions):
        raise ValueError('Full contiguous ARM instruction proposal contains unknown data')
    literal_refs, branches = [], []
    for instruction in instructions:
        if (instruction.group(CS_GRP_CALL) or instruction.group(CS_GRP_JUMP)) and instruction.operands[0].type == 2:
            branches.append({'pc': hex(instruction.address), 'mnemonic': instruction.mnemonic, 'target': hex(instruction.operands[0].imm)})
        for operand in instruction.operands:
            if operand.type == 3 and operand.mem.base == ARM_REG_PC:
                address = instruction.address + 8 + operand.mem.disp
                if not STOP <= address <= END - 4:
                    raise ValueError('Unreconciled proposed sequence-main literal')
                literal_refs.append({'pc': hex(instruction.address), 'storage': hex(address),
                    'word': hex(int.from_bytes(raw[address - base:address - base + 4], 'little'))})
    if {int(row['storage'], 0) for row in literal_refs} != {STOP, STOP + 4}:
        raise ValueError('Proposed eight-byte pool does not match all current literal reads')
    if not any(row['pc'] == '0x37ffff0' and row['target'] == '0x3800000' for row in branches):
        raise ValueError('Direct native entry into excluded block changed')
    mapped, loader_proof = loader(image, layout)
    current = mapped[base]
    if current[START - base:END - base] != raw[START - base:END - base]:
        raise ValueError('Actually loaded proposed span differs from measured WRAM module')
    probes = [gap_probe(current, fields, shared, player_id, count, seed) for seed, (fields, shared, player_id, count) in enumerate(
        (fields, shared, player_id, count) for fields in ((0, 0, 0), (1, 256, 239), (65535, 65535, 65535), (32768, 32768, 1), (0, 65535, 65535))
        for shared in (False, True) for player_id in (0, 15, 255) for count in (0, 1, 0xFFFFFFFF))]
    report = {'schemaVersion': 1, 'generator': Path(__file__).name, 'generatorSha256': digest(Path(__file__).read_bytes()),
        'generatorDependencies': [{'path': name, 'sha256': digest((ROOT / name).read_bytes())}
            for name in ('arm7_runtime.py', 'match_runtime.py', 'match_lowlevel.py', 'project.py')],
        'runtime': {'python': '.'.join(map(str, sys.version_info[:3])), 'unicorn': unicorn.__version__, 'cpu': 'TI925T ARMv4T surrogate'},
        'romSha256': rom_hash, 'program': '', 'processor': 'arm7', 'module': 'arm7-wram', 'mode': 'arm',
        'arm7Header': {'romOffset': offset, 'entry': hex(entry), 'loadAddress': hex(load), 'storedBytes': length},
        'loaderImageSha256': digest(image), 'actualOriginalLoader': loader_proof, 'owner': owner,
        'ownership': 'Unique original ARM7 autoload descriptor and actual original copy/zero execution; not ARM9 or utility-child namespace',
        'configuredFunction': function, 'inventorySha256': digest(inventory_path.read_bytes()),
        'candidate': {'start': hex(START), 'codeEnd': hex(STOP), 'fullEnd': hex(END), 'existingConfiguredCodeBytes': 280,
            'newlyConfirmedExcludedCodeBytes': 64, 'proposedInstructionBytes': 344, 'proposedGeneratedOrOriginalPoolBytes': 8,
            'fullInitializedSpanBytes': 352, 'additionalInitializedModuleBytes': 0, 'spanSha256': digest(raw[START - base:END - base]),
            'originalArm7ImageFileOffset': owner['inputFileOffset'] + START - base,
            'originalRomFileOffset': offset + owner['inputFileOffset'] + START - base},
        'directBranchesAndCalls': branches, 'literalReferences': literal_refs, 'excludedBlock': {'start': hex(GAP), 'bytes': 64,
            'sha256': digest(raw[GAP - base:GAP - base + 64]), 'records': probes, 'actualBoundaryStops': len(probes), 'functionReturnCredit': 0},
        'sourceCredit': 0, 'assemblyCredit': 0, 'configEdits': False, 'boundaryMigrationApproved': False,
        'limitations': ['Discontiguous range repair proposal only; no ordinary-C, complete entry return or source credit',
            'Current contiguous-merge helper is not applied; overlapping/opaque/interior consumers still require separate full audit',
            'Raw selected fields/counter arithmetic is not assigned timing, story, area or renewal meaning']}
    destination = ROOT / 'evidence/attempts/arm7-seq-main-layout-20261030.json'
    write_json(destination, report)
    print(json.dumps({'report': destination.relative_to(ROOT).as_posix(), 'sha256': digest(destination.read_bytes()),
        'actualOriginalAutoloadReturn': loader_proof['actualReturn'], 'actualGapBoundaryStops': len(probes),
        'newlyConfirmedExcludedCodeBytes': 64, 'sourceCredit': 0}), flush=True)


if __name__ == '__main__':
    main()
