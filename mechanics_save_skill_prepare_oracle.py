import hashlib
import itertools
import random
import struct
import time

from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, put
from verify_record_features import compiled

EKT = 0x02500000
OUTPUT = 0x02530080
WORD = 0x021b9e9c
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def expected(memory, levels, name, first, second, third, success):
    trace = []
    if name == 'saved_skill_ids_normalize':
        if not first or not 1 <= second <= 5:
            return 0, trace
        values = read(memory, first, second * 2)[::2]
        normalized = list(dict.fromkeys(value for value in values if value))
        if not normalized:
            write(memory, first, b'\x8e')
        else:
            normalized += [0] * (second - len(normalized))
            for index, value in enumerate(normalized):
                write(memory, first + index * 2, bytes([value]))
        return 1, trace
    if not third:
        return 0, trace
    kind = EKT + first * 100
    write(memory, third, bytes(32))
    for index, source in enumerate((28, 30, 28, 30, 32, 34, 36, 38)):
        write(memory, third + index * 2, read(memory, kind + source, 2))
    write(memory, third + 16, b'\1')
    curve = read(memory, kind + 67, 1)[0]
    offset = curve * 400 + 4
    trace.append(('LevelUpTbl.bin', WORD, 4, offset, success))
    value = struct.unpack_from('<I', levels, offset)[0] if success else 0
    if success:
        put(memory, WORD, value)
    put(memory, third + 24, value)
    return 1, trace

def validate(arm, save, matches, root):
    wanted = {0x020449d4, 0x02044f9c, 0x020634cc}
    reused = {address: item for address, item in compiled(arm).items() if address in wanted}
    if set(reused) != wanted:
        raise AssertionError('Skill preparation required source absent')
    rom = NintendoDSRom((root / 'inputs/game.nds').read_bytes())
    assets = {name: bytes(rom.getFileByName(name)) for name in ('EnmyKindTbl.bin', 'LevelUpTbl.bin')}
    ekt = assets['EnmyKindTbl.bin'][8:]
    levels = assets['LevelUpTbl.bin']
    context = {}

    def resource(machine, address, size, user):
        first, destination, count, offset = [machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        if machine.mem_read(first, 15) != b'LevelUpTbl.bin\0' or destination != WORD or count != 4 or offset + count > len(levels):
            raise AssertionError('Skill prepare resource contract differs')
        context['trace'].append(('LevelUpTbl.bin', destination, count, offset, context['success']))
        if context['success']:
            machine.mem_write(destination, levels[offset:offset + 4])
        for register, value in [(UC_ARM_REG_R0, int(context['success'])), (UC_ARM_REG_R1, 0x11223344), (UC_ARM_REG_R2, 0x22334455), (UC_ARM_REG_R3, 0x33445566)]:
            machine.reg_write(register, value)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*reused.values(), *matches.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machine.hook_add(UC_HOOK_CODE, resource, begin=0x0202a818, end=0x0202a818)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = []
    for name in matches:
        if name == 'saved_default_block20':
            vectors.extend((name, species, species % 3, OUTPUT, True, None) for species in range(512))
            vectors.extend((name, species, variant, destination, success, None) for species in (0, 139, 353, 500, 511) for variant in (0, 2) for destination in (0, OUTPUT, EKT + species * 100 + 16, EKT + species * 100 + 40) for success in (False, True))
        else:
            vectors.extend((name, OUTPUT, count, 0, True, bytes(value for pair in zip(ids, (13, 27, 59, 131, 255)) for value in pair)) for ids in itertools.product((0, 1, 142, 255), repeat=5) for count in range(1, 6))
            vectors.extend((name, destination, count, 0, True, rng.randbytes(10)) for destination in (0, OUTPUT) for count in (-0x80000000, -1, 0, 1, 5, 6, 0x7fffffff))
    cases = calls = 0
    for name, first, second, third, success, skills in vectors:
        original = {0x020f6900: bytearray(rng.randbytes(0x1000)), 0x021b9000: bytearray(rng.randbytes(0x1000)), EKT: bytearray(ekt + bytes(0x10000 - len(ekt))), 0x02530000: bytearray(rng.randbytes(0x1000))}
        put(original, 0x020f69f0, EKT)
        if skills is not None:
            write(original, OUTPUT, skills)
        memory = {address: bytearray(data) for address, data in original.items()}
        result, trace = expected(memory, levels, name, first, second, third, success)
        row, code = matches[name]
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            context.update({'trace': [], 'success': success})
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), (first, second, third)):
                machine.reg_write(register, value & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(row['address'], 16), STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Skill preparation bounds', name, first, second, third))
            if machine.reg_read(UC_ARM_REG_R0) != result or context['trace'] != trace:
                raise AssertionError(('Skill preparation return/resource trace', name, first, second, third))
            for address, data in memory.items():
                if bytes(machine.mem_read(address, len(data))) != data:
                    raise AssertionError(('Skill preparation block/ID/allocation/table/scratch/guard RAM', name, first, second, third))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedBlockLevelTableAndStableUniqueIds': True, 'platformStubs': {'0x0202a818': 'bounded read-only LevelUpTbl resource reader'}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': '0x02008d78', 'bytes': 148, 'sha256': sha(arm[0x8d78:0x8e0c]), 'role': 'SDK fill'}, 'assetSha256': {name: sha(blob) for name, blob in assets.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['Default block clears32 bytes, repeats EKT initial0/1 in the first four halfwords, copies the remaining initial halfwords, sets byte16 to1 and obtains the level2 table word at byte24.', 'Null output returns0; resource failure leaves scratch unchanged but stores0 in the cleared output word.', 'Normalization accepts only counts1..5, inserts native ID142 when all selected IDs are zero, otherwise preserves the first occurrence order of nonzero IDs and clears the trailing IDs.', 'Normalization moves only ID bytes; every allocated-point byte remains at its original slot.', 'All512 EKT species, all five lengths and every five-ID sequence over0/1/142/255, null/boundary lengths and aliasing block/EKT outputs are checked.'], 'limitations': ['The resource service remains a controlled read-only contract and SDK fill remains retained native code.', 'Aliasing block/EKT tests are isolated ARM observations rather than legal asset-edit operations; missing EKT data with nonnull output is outside this proof.', 'Native ID142 and the raw block fields have no newly promoted gameplay labels or save semantics.']}
