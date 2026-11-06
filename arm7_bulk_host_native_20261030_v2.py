import hashlib
import random
import struct
import match_lowlevel
import arm7_runtime
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_CPU_ARM_TI925T

ROOT = match_lowlevel.ROOT
TABLE = 0x03807028
TABLE_STORAGE = 0x03806FA9
TABLE_STORAGE_BYTES = 160
STATUS, CONTROL, COMMAND = 0x040001A4, 0x040001A1, 0x040001A8
STACK, RETURN = 0x023E0000, 0x023FF000


def digest(data):
    return hashlib.sha256(data).hexdigest()


def profiles(address):
    if address == 0x037FEE58:
        rows = [{'phase': phase, 'tableByte': None, 'seed': seed} for phase in range(256) for seed in range(4)]
        rows += [{'phase': phase, 'tableByte': value, 'seed': seed} for phase in (1, 33, 65, 97, 129, 160, 192, 224, 255) for value in (0, 127, 128, 255) for seed in (0, 1)]
        return rows
    if address == 0x03802F9C:
        return [{'first': first, 'second': second, 'clearAfterReads': delay, 'seed': seed} for first, second in
            ((0, 0), (0xFFFFFFFF, 0x80000000), (0x12345678, 0xA5C3F00D), (0x80000000, 1)) for delay in (0, 1, 7) for seed in range(8)]
    raise ValueError('Unsupported independent host ARM7 model')


def table_index(phase):
    if phase < 32:
        return phase, False
    if phase < 64:
        return 64 - phase, False
    if phase < 96:
        return phase - 64, True
    return 128 - phase, True


def signed_byte(value):
    return (value & 255) - (256 if value & 128 else 0)


def execute(entry, body, profile, code_bytes, limit=512, never_clear=False):
    address = int(entry['address'], 0)
    u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    maps = [(0x027E0000, 0x20000), (0x037F8000, 0x18000), (0x02380000, 0x1000),
        (STACK, 0x10000), (RETURN, 0x1000), (0x04000000, 0x1000)]
    for start, length in maps:
        u.mem_map(start, length)
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    for module in layout['modules']:
        binary = (ROOT / module['binary']).read_bytes()
        if digest(binary) != module['sha256']:
            raise ValueError('Original host ARM7 runtime module changed')
        u.mem_write(int(module['base'], 0), binary)
    rng = random.Random(20261030 + profile['seed'])
    u.mem_write(STACK, rng.randbytes(0x10000))
    u.mem_write(0x04000000, rng.randbytes(0x1000))
    u.mem_write(address, body)
    registers = [rng.getrandbits(32) for register in match_lowlevel.REGISTERS]
    registers[-2:] = [STACK + 0xFFF0, RETURN]
    expected_return, expected_stores, selected_byte = None, [], None
    status_low = rng.getrandbits(31)
    if address == 0x037FEE58:
        registers[0] = profile['phase'] & 0xFFFFFFFF
        index, negate = table_index(profile['phase'])
        if profile.get('tableByte') is not None:
            u.mem_write(TABLE + index, bytes([profile['tableByte']]))
        selected_byte = u.mem_read(TABLE + index, 1)[0]
        expected_return = signed_byte(-signed_byte(selected_byte)) if negate else signed_byte(selected_byte)
        expected_return &= 0xFFFFFFFF
    else:
        registers[:2] = [profile['first'], profile['second']]
        u.mem_write(STATUS, struct.pack('<I', status_low | (0x80000000 if profile['clearAfterReads'] or never_clear else 0)))
        expected_stores = [[CONTROL, 1, 0xC0]] + [[COMMAND + index, 1, value] for index, value in enumerate(
            profile['first'].to_bytes(4, 'big') + profile['second'].to_bytes(4, 'big'))]
    before = {start: bytes(u.mem_read(start, length)) for start, length in maps}
    u.reg_write(UC_ARM_REG_CPSR, ((profile['seed'] & 15) << 28) | 0xD3)
    for register, value in zip(match_lowlevel.REGISTERS, registers):
        u.reg_write(register, value)
    stores, visited, table_reads, status_reads, hardware = [], [], [], [], []
    def code(machine, pc, size, unused):
        if not address <= pc < address + code_bytes:
            raise ValueError('Host ARM7 execution escaped its code boundary or entered its pool')
        visited.append(pc)
    def read(machine, access, location, size, value, unused):
        if address == 0x037FEE58 and TABLE_STORAGE <= location < TABLE_STORAGE + TABLE_STORAGE_BYTES:
            table_reads.append([location, size, int.from_bytes(machine.mem_read(location, size), 'little')])
        if address == 0x03802F9C and location == STATUS:
            if not never_clear and len(status_reads) >= profile['clearAfterReads']:
                machine.mem_write(STATUS, struct.pack('<I', status_low))
                hardware.append({'readIndex': len(status_reads), 'address': STATUS, 'word': status_low})
            status_reads.append([location, size, int.from_bytes(machine.mem_read(location, size), 'little')])
    u.hook_add(UC_HOOK_CODE, code)
    u.hook_add(UC_HOOK_MEM_READ, read)
    u.hook_add(UC_HOOK_MEM_WRITE, lambda machine, access, location, size, value, unused: stores.append([location, size, value]))
    error = None
    try:
        u.emu_start(address, RETURN, count=limit, timeout=100000)
    except UcError as exception:
        error = exception.errno
    returned = error is None and u.reg_read(UC_ARM_REG_PC) == RETURN
    final = [u.reg_read(register) for register in match_lowlevel.REGISTERS]
    if returned:
        if expected_return is not None and final[0] != expected_return:
            raise ValueError('Native signed-byte/full-word lookup model differs')
        if stores != expected_stores:
            raise ValueError('Independent native host write ordering differs')
        if any(final[index] != registers[index] for index in range(4, 14)):
            raise ValueError('Host ARM7 leaf changed a callee-saved register or stack pointer')
        expected_memory = {start: bytearray(value) for start, value in before.items()}
        if address == 0x03802F9C:
            struct.pack_into('<I', expected_memory[0x04000000], STATUS - 0x04000000, status_low)
        for location, size, value in expected_stores:
            start = next(start for start, length in maps if start <= location and location + size <= start + length)
            expected_memory[start][location - start:location - start + size] = value.to_bytes(size, 'little')
        if any(bytes(u.mem_read(start, length)) != expected_memory[start] for start, length in maps):
            raise ValueError('Native host model has unexpected full-map memory effects')
    return {'actualReturn': returned, 'fault': error, 'pc': u.reg_read(UC_ARM_REG_PC), 'registers': final, 'cpsr': u.reg_read(UC_ARM_REG_CPSR),
        'maps': [{'base': start, 'bytes': length, 'sha256': digest(bytes(u.mem_read(start, length)))} for start, length in maps],
        'stores': stores, 'visited': visited, 'tableReads': table_reads, 'selectedTableByte': selected_byte, 'statusReads': status_reads,
        'syntheticHardwareWrites': hardware, 'instructionLimit': limit, 'fullMapFieldModelPassed': returned}


def verify(entry, native, rebuilt, code_bytes):
    address = int(entry['address'], 0)
    records, visited = [], set()
    for profile in profiles(address):
        original, source = execute(entry, native, profile, code_bytes), execute(entry, rebuilt, profile, code_bytes)
        if original != source or not original['actualReturn']:
            raise ValueError('Native/source host ARM7 actual returns or full effects differ')
        visited.update(original['visited'])
        records.append({'profile': profile, 'actualOriginalAndRecompiledReturns': 2, 'stateSha256': digest(repr(original).encode()),
            'rawR0': original['registers'][0], 'tableReads': original['tableReads'], 'statusReads': original['statusReads'],
            'syntheticHardwareWrites': original['syntheticHardwareWrites'], 'stores': original['stores'], 'fieldModelPassed': True})
    exhausted = execute(entry, native, profiles(address)[0], code_bytes, limit=1)
    source_exhausted = execute(entry, rebuilt, profiles(address)[0], code_bytes, limit=1)
    if exhausted['actualReturn'] or exhausted != source_exhausted:
        raise ValueError('Exhausted host ARM7 frame received return credit')
    controls = {'oneInstructionExhaustion': exhausted}
    if address == 0x03802F9C:
        busy = execute(entry, native, profiles(address)[0], code_bytes, limit=512, never_clear=True)
        source_busy = execute(entry, rebuilt, profiles(address)[0], code_bytes, limit=512, never_clear=True)
        if busy['actualReturn'] or busy['stores'] or busy != source_busy:
            raise ValueError('Uncleared busy status wrote commands or received return credit')
        controls['busyNeverCleared'] = busy
    return {'supported': True, 'vectors': len(records), 'actualOriginalAndRecompiledReturns': 2 * len(records), 'verifiedReturn': True,
        'allGpCpsrFullMappedMemoryAndOrderedWritesEqual': True, 'independentFieldModelPassed': True, 'freshMachinePerExecution': True,
        'cpuModel': 'Unicorn TI925T ARMv4T surrogate, not DS hardware', 'instructionLimit': 512, 'timeoutMicroseconds': 100000,
        'nativeCalleeCalls': 0, 'syntheticMmioReadSchedule': address == 0x03802F9C, 'records': records,
        'visitedAddresses': sorted(visited), 'unvisitedInstructionAddresses': [pc for pc in range(address, address + code_bytes, 4) if pc not in visited],
        'unsupportedControls': controls, 'unsupportedReturnCredit': 0,
        'limitations': ['Only the declared input/data/hardware schedule domain is functionally qualified',
            'Table byte overrides affect only a copied machine context; source/extract/original input files remain unchanged',
            'No physical cartridge I/O, bus ownership, hardware timing, scene or caller reachability assertion']}


def producer():
    rows = [{'phaseWord': (phase << 8) | (phase ^ 0xA5), 'amplitude': 1, 'scale': 1, 'limit': phase, 'position': phase} for phase in range(256)]
    rows += [{'phaseWord': phase, 'amplitude': amplitude, 'scale': 255, 'limit': limit, 'position': position} for phase in (0, 0x8000, 0xFFFF)
        for amplitude, limit, position in ((0, 0, 0), (1, 1, 0))]
    results = []
    layout = arm7_runtime.derive((ROOT / 'extract/arm7/arm7.bin').read_bytes())
    for index, profile in enumerate(rows):
        u = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        u.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
        for first, length in ((0x027E0000, 0x20000), (0x037F8000, 0x18000), (0x02380000, 0x1000),
            (0x02200000, 0x10000), (STACK, 0x10000), (RETURN, 0x1000)):
            u.mem_map(first, length)
        for module in layout['modules']:
            u.mem_write(int(module['base'], 0), (ROOT / module['binary']).read_bytes())
        state = 0x02201000
        data = bytearray(32)
        data[2:4] = bytes([profile['amplitude'], profile['scale']])
        struct.pack_into('<3H', data, 4, profile['limit'], profile['position'], profile['phaseWord'])
        u.mem_write(state, bytes(data))
        u.reg_write(UC_ARM_REG_CPSR, ((index & 15) << 28) | 0xD3)
        for register, value in zip(match_lowlevel.REGISTERS, [state, 0x80000000 | index, 0xFFFFFFFF, 0x12345678] + [index] * 9 + [STACK + 0xFFF0, RETURN]):
            u.reg_write(register, value)
        captures = []
        def code(machine, pc, size, unused):
            if pc == 0x037FEE58:
                captures.append({'pc': pc, 'lr': machine.reg_read(match_lowlevel.REGISTERS[-1]),
                    'arguments': [machine.reg_read(register) for register in match_lowlevel.REGISTERS[:4]]})
                machine.emu_stop()
            elif not 0x037FFE14 <= pc < 0x037FFE64:
                raise ValueError('Native producer escaped its original caller/helper boundary')
        u.hook_add(UC_HOOK_CODE, code)
        u.emu_start(0x037FFE14, RETURN, count=512, timeout=100000)
        reached = bool(captures)
        expected = profile['amplitude'] != 0 and profile['position'] >= profile['limit']
        actual_return = u.reg_read(UC_ARM_REG_PC) == RETURN
        if reached != expected or reached == actual_return:
            raise ValueError('Native producer branch/boundary classification differs')
        if reached and (captures[0]['arguments'][0] != profile['phaseWord'] >> 8 or captures[0]['arguments'][1] != profile['position'] or captures[0]['lr'] != 0x037FFE4C):
            raise ValueError('Actual native high-byte producer/remaining R1/LR differs')
        if actual_return and u.reg_read(match_lowlevel.REGISTERS[0]) != 0:
            raise ValueError('Native gated producer did not return raw zero')
        if bytes(u.mem_read(state, len(data))) != data:
            raise ValueError('Native producer unexpectedly changed its synthetic state')
        results.append({'profile': profile, 'originalHelperBoundaryReached': reached, 'actualEarlyCallerReturn': actual_return,
            'boundaryStopReceivesOuterReturnCredit': False, 'capture': captures, 'sourceCredit': 0})
    return {'program': '', 'processor': 'arm7', 'module': 'arm7-wram', 'caller': '0x037ffe14', 'callSite': '0x037ffe48',
        'callee': '0x037fee58', 'capturedArgument0Values': list(range(256)), 'qualifiedBoundaryStops': 256, 'actualEarlyCallerReturns': 6,
        'boundaryStopOuterReturnCredit': 0, 'newSourceCredit': 0, 'records': results,
        'limitations': ['Original native caller with synthetic amplitude/threshold/phase fields; not enclosing scene reachability',
            'Execution deliberately stops at the actual BL target without executing the helper; these stops are not whole caller returns']}
