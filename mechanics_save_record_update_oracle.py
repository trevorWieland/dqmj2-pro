import hashlib
import json
import random
import struct
import time

from elftools.elf.elffile import ELFFile
from ndspy.rom import NintendoDSRom
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_INVALID
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

MAIN = 0x021bd51c
RECORDS = 0x021bd674
TABLE = 0x02500000
INPUT = 0x02520080
EKT_STATE = 0x020f69ec
EFFECT = 0x02600000
BITS = 0x027fefa8
STOP = 0x027ff800
PLATFORM = {0x0207b460: 'skill-bits', 0x0207c2b8: 'derive24', 0x0207c3d8: 'derive26', 0x020634cc: 'next-word', 0x0207aebc: 'skill-changed'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def dependencies(root, arm):
    wanted = {0x02062a10, 0x020449d4, 0x02062ecc, 0x02008d78}
    result = {}
    for batch in json.loads((root / 'recovery.json').read_text(encoding='utf-8'))['batches']:
        document = json.loads((root / batch['report']).read_text(encoding='utf-8'))
        if document['romSha256'] != '674c5cbf3e03e1f8777d39c7bb9bb195e4a625ae278ee307176a0f60d9d38ba6':
            raise AssertionError('Record update dependency namespace differs')
        for row in document.get('matches', document.get('functionMatches', [])):
            address = int(row['address'], 16)
            if address not in wanted or row.get('module') not in ('main', 'arm9'):
                continue
            if sha((root / row['source']).read_bytes()) != row['sourceSha256'] or sha((root / row['object']).read_bytes()) != row['objectSha256']:
                raise AssertionError('Record update dependency identity differs')
            with (root / row['object']).open('rb') as stream:
                elf = ELFFile(stream)
                symbol = next(symbol for symbol in elf.get_section_by_name('.symtab').iter_symbols() if symbol.name == row['name'])
                code = bytearray(elf.get_section(symbol['st_shndx']).data()[symbol['st_value']:symbol['st_value'] + symbol['st_size']])
            for relocation in row.get('relocations', []):
                at = relocation['offset']
                target = int(relocation['target'], 16) + relocation['addend']
                previous = struct.unpack_from('<I', code, at)[0]
                value = target if relocation['type'] == 2 else (previous & 0xff000000) | (((target - address - at) >> 2) & 0xffffff)
                struct.pack_into('<I', code, at, value & 0xffffffff)
            if code != arm[address - 0x02000000:address - 0x02000000 + row['bytes']]:
                raise AssertionError('Record update dependency bytes differ')
            result[address] = (row, bytes(code))
    if not {0x02062a10, 0x020449d4, 0x02062ecc}.issubset(result):
        raise AssertionError('Accepted record update dependencies absent')
    return result

def signed(value):
    return value - 0x100000000 if value & 0x80000000 else value

def bit_pattern(species, variant, skills):
    return bytes((species + variant + sum(skills) + index * 17) & 255 for index in range(64))

def derived(block, bits, operation):
    first, second = struct.unpack_from('<HH', block)
    value = first + second * 2 + sum(bits) if operation == 'derive24' else first ^ second ^ (sum(bits) * 3)
    return (0x10000 if operation == 'derive24' else 0x20000) | (value & 65535)

def next_word(species, variant, mode):
    return 0x80000000 | (((species & 65535) * 257 + variant * 17 + mode) & 0x7fffffff)

def lookup(memory, identity):
    if identity:
        for index in range(100):
            at = RECORDS + index * 132
            if u32(memory, at + 20) == identity:
                return at
    return None

def expected(memory, table, name, first, second, third, null_kind):
    record = lookup(memory, first)
    trace = []
    if not record:
        fault = 0x02062d3c if name == 'saved_record_block20_initialize' else 0x02062f04 if name == 'saved_record_skill_nonzero_count' else None
        return 0, trace, fault
    species = struct.unpack('<h', read(memory, record + 24, 2))[0]
    variant = read(memory, record + 26, 1)[0]
    if name == 'saved_record_block20_initialize':
        bits = bit_pattern(species, variant, read(memory, record + 122, 10))
        trace.append(('skill-bits', species & 0xffffffff, variant, record + 122, BITS, sha(bits)))
        if second:
            write(memory, record + 32, read(memory, second, 32))
        elif null_kind:
            return 0, trace, None
        else:
            kind = table[species * 100:species * 100 + 100]
            write(memory, record + 32, bytes(32))
            write(memory, record + 32, kind[28:32])
            for role, offset in [('derive24', 36), ('derive26', 38)]:
                value = derived(read(memory, record + 32, 32), bits, role)
                trace.append((role, record + 32, BITS, value))
                write(memory, record + offset, struct.pack('<H', value & 65535))
            write(memory, record + 40, kind[32:40])
            write(memory, record + 48, b'\x01')
            value = next_word(species, variant, 2)
            put(memory, record + 56, value)
            trace.append(('next-word', species & 0xffffffff, variant, 2, value))
        return 1, trace, None
    if name == 'saved_record_skill_initialize':
        skill = record + 122 + second * 2
        if third:
            write(memory, skill, read(memory, third, 2))
        elif null_kind:
            return 0, trace, None
        else:
            write(memory, skill, bytes([table[species * 100 + 95], 0]))
        current = read(memory, skill, 2)
        trace.append(('skill-changed', species & 0xffffffff, current[0], current[1]))
        put(memory, EFFECT, (species * 31 + current[0] * 257 + current[1]) & 0xffffffff)
        return 1, trace, None
    if name == 'saved_record_skill_nonzero_count':
        return sum(read(memory, record + 122 + index * 2, 1)[0] != 0 for index in range(5)), trace, None
    if name == 'saved_record_skill_allocated_add':
        at = record + 123 + second * 2
        write(memory, at, bytes([(read(memory, at, 1)[0] + third) & 255]))
        return 1, trace, None
    raise AssertionError(('Unknown record update function', name))

def validate(arm, save, matches, root):
    reused = dependencies(root, arm)
    context = {}
    machines = []

    def invalid(machine, access, address, size, value, user):
        context['fault'] = machine.reg_read(UC_ARM_REG_PC)
        return False

    def provider(machine, address, size, user):
        role = PLATFORM[address]
        values = [machine.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        result = 0
        if role == 'skill-bits':
            bits = bit_pattern(signed(values[0]), values[1], machine.mem_read(values[2], 10))
            machine.mem_write(values[3], bits)
            context['trace'].append((role, *values, sha(bits)))
        elif role in ('derive24', 'derive26'):
            result = derived(machine.mem_read(values[0], 32), machine.mem_read(values[1], 64), role)
            context['trace'].append((role, *values[:2], result))
        elif role == 'next-word':
            result = next_word(signed(values[0]), values[1], values[2])
            context['trace'].append((role, *values[:3], result))
        else:
            context['trace'].append((role, *values[:3]))
            result = (signed(values[0]) * 31 + values[1] * 257 + values[2]) & 0xffffffff
            machine.mem_write(EFFECT, struct.pack('<I', result))
        for register, value in [(UC_ARM_REG_R0, result), (UC_ARM_REG_R1, 0xaabbccdd), (UC_ARM_REG_R2, 0xbbccddee), (UC_ARM_REG_R3, 0xccddeeff)]:
            machine.reg_write(register, value)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in [*matches.values(), *reused.values()]:
                machine.mem_write(int(row['address'], 16), code)
        machine.hook_add(UC_HOOK_MEM_INVALID, invalid)
        for address in PLATFORM:
            machine.hook_add(UC_HOOK_CODE, provider, begin=address, end=address)
        machines.append(machine)
    table = NintendoDSRom((root / 'inputs/game.nds').read_bytes()).getFileByName('EnmyKindTbl.bin')[8:]
    rng = random.Random(20261027)
    cases = 0
    calls = 0
    faults = 0
    for fixture in ('captured-primary', 'captured-backup', 'synthetic', 'duplicate', 'null-kind'):
        original = {0x021bd000: bytearray(rng.randbytes(0x5000)), 0x020f6900: bytearray(rng.randbytes(0x1000)), TABLE: bytearray(table + bytes(0x10000 - len(table))), 0x02520000: bytearray(rng.randbytes(0x1000)), EFFECT: bytearray(rng.randbytes(0x1000))}
        bank = 0x7100 if fixture == 'captured-backup' else 0
        write(original, MAIN, save[bank + 0x90:bank + 0x3a68])
        if not fixture.startswith('captured'):
            data = bytearray(rng.randbytes(132))
            struct.pack_into('<IhB', data, 20, 1, 0 if fixture == 'null-kind' else 139, 2)
            data[122:132] = bytes([0, 255, 1, 0, 255, 127, 4, 128, 0, 254])
            write(original, RECORDS, bytes(data))
            if fixture == 'duplicate':
                write(original, RECORDS + 132, bytes(data))
        put(original, EKT_STATE + 4, 0 if fixture == 'null-kind' else TABLE)
        identities = [u32(original, RECORDS + index * 132 + 20) for index in range(100)]
        identity = next(value for value in identities if value)
        target = lookup(original, identity)
        missing = 0xffffffff
        while missing in identities:
            missing -= 1
        vectors = []
        for name in matches:
            for key in (identity, 0, missing):
                if name == 'saved_record_block20_initialize':
                    vectors.extend((name, key, input_pointer, 0) for input_pointer in (0, INPUT, target + 32))
                elif name == 'saved_record_skill_initialize':
                    vectors.extend((name, key, slot, input_pointer) for slot in (-1, 0, 1, 4, 5) for input_pointer in (0, INPUT, target + 122 + slot * 2))
                elif name == 'saved_record_skill_allocated_add':
                    vectors.extend((name, key, slot, delta) for slot in (-1, 0, 1, 4, 5) for delta in (-257, -256, -1, 0, 1, 255, 256, 257, -0x80000000, 0x7fffffff))
                else:
                    vectors.append((name, key, 0, 0))
        for name, first, second, third in vectors:
            memory = {address: bytearray(data) for address, data in original.items()}
            result, trace, fault = expected(memory, table, name, first, second, third, fixture == 'null-kind')
            row, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                context.update({'trace': [], 'fault': None})
                for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), (first, second, third)):
                    machine.reg_write(register, value & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                try:
                    machine.emu_start(int(row['address'], 16), STOP, count=1000000)
                except UcError:
                    if fault is None:
                        raise
                if time.monotonic() - began > 2 or context['fault'] != fault or (fault is None and machine.reg_read(UC_ARM_REG_PC) != STOP):
                    raise AssertionError(('Record update execution/fault bounds', fixture, name, first, second, third, context['fault'], fault))
                if (fault is None and machine.reg_read(UC_ARM_REG_R0) != result) or context['trace'] != trace:
                    raise AssertionError(('Record update result/provider sequence differs', fixture, name, first, second, third, context['trace'], trace))
                for address, data in memory.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Record block/skills/EKT/provider/guard RAM differs', fixture, name, first, second, third))
                calls += 1
            faults += int(fault is not None)
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'expectedMalformedFaultCases': faults, 'testedFunctions': list(matches), 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcOrExpectedFaultVerified': True, 'independentExpectedRamAndProviderTrace': True, 'platformStubs': {hex(address): role for address, role in PLATFORM.items()}, 'reusedAcceptedSources': [{key: row[key] for key in ('name', 'address', 'source', 'sourceSha256', 'object', 'objectSha256')} for row, code in reused.values()], 'observations': ['The block initializer calls skill expansion before testing lookup success; absent IDs fault at native0x02062D3C before a graceful return.', 'An explicit block copies32 bytes at record0x20; default initialization clears that block, writes measured EKT words, invokes bounded derivation contracts and sets byte0x30/word0x38.', 'Skill initialization writes two bytes from explicit input or the EKT default at0x5F, zeroing its allocation and notifying the skill-change contract.', 'Nonzero skill count reads five slot IDs; absent lookup faults at native0x02062F04.', 'Allocated-point addition truncates to8 bits without a cap and returns0 only when the record lookup fails.'], 'limitations': ['Skill expansion, two derived calculations, next-word calculation and skill-change effects are explicit controlled contracts, not reconstructed mechanics.', 'Native lookup, EKT pointer, memory fill and existing slot-pointer C bodies execute.', 'Missing-record faults, out-of-five slot indices and signed-overflow additions are isolated ARM machine probes; corresponding C behavior is not a portable legal operation contract.', 'The32-byte block includes more than the16-byte saved stat array; no complete stat/XP/skill semantic implementation is claimed.', 'No new semantic partition bytes are promoted.']}
