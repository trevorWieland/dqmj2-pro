import hashlib
from pathlib import Path
import random
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_LR, UC_CPU_ARM_TI925T

ROOT = Path(__file__).resolve().parent
BASE, ADDRESS, STATE, RESERVED = 0x037F8000, 0x037FD34C, 0x038078A8, 0x03807894
IO, STACK, RETURN = 0x04000000, 0x02300000, 0x02500000
MODULE = 'extract/arm7/runtime/arm7-wram.bin'
MODULE_SHA = 'e4597aa1fd4d193e1c06544f43d499a7dbe51dabff217154f2913532f569878c'
CALLEES = {0x037FD10C: 24, 0x037FB928: 56, 0x037FB8D8: 20}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def cases():
    return [{'initialized': initialized, 'reserved': reserved, 'ie': ie, 'ime': ime}
        for initialized in (0, 1, 2, 0x7FFF, 0x8000, 0xFFFF)
        for reserved in (0, 1, 2, 0x8000, 0xFFFF)
        for ie in (0, 0x10, 0x80000000, 0xFFFFFFFF) for ime in (0, 1, 0xFFFF)]


def execute(body, case, seed, budget=10000):
    raw = (ROOT / MODULE).read_bytes()
    if digest(raw) != MODULE_SHA or len(body) != 68:
        raise ValueError('Qualified host alarm initializer/native module differs')
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.ctl_set_cpu_model(UC_CPU_ARM_TI925T)
    cpu.mem_map(BASE, 0x20000)
    cpu.mem_write(BASE, raw)
    cpu.mem_write(ADDRESS, body)
    cpu.mem_map(IO, 0x1000)
    cpu.mem_map(STACK, 0x1000)
    rng = random.Random(20261031 + seed)
    memory, io, stack = bytearray(rng.randbytes(0x1000)), bytearray(rng.randbytes(0x1000)), rng.randbytes(0x1000)
    memory[STATE - 0x03807000:STATE - 0x03807000 + 2] = case['initialized'].to_bytes(2, 'little')
    memory[RESERVED - 0x03807000:RESERVED - 0x03807000 + 2] = case['reserved'].to_bytes(2, 'little')
    io[0x208:0x20A] = case['ime'].to_bytes(2, 'little')
    io[0x210:0x214] = case['ie'].to_bytes(4, 'little')
    cpu.mem_write(0x03807000, bytes(memory))
    cpu.mem_write(IO, bytes(io))
    cpu.mem_write(STACK, stack)
    initial = [rng.getrandbits(32) for register in match_runtime.REGISTERS]
    initial[-2:] = [STACK + 0xF00, RETURN]
    cpu.reg_write(UC_ARM_REG_CPSR, seed % 16 << 28 | 0xD3)
    for register, value in zip(match_runtime.REGISTERS, initial):
        cpu.reg_write(register, value)
    reads, writes, visited, entries, returns, active = [], [], [], [], [], []

    def code(machine, pc, width, unused):
        if active and pc == active[-1]['returnPc']:
            frame = active.pop()
            returns.append(dict(frame, result=machine.reg_read(match_runtime.REGISTERS[0])))
        if pc in CALLEES:
            frame = {'entry': pc, 'returnPc': machine.reg_read(UC_ARM_REG_LR),
                'arguments': [machine.reg_read(register) for register in match_runtime.REGISTERS[:4]]}
            active.append(frame)
            entries.append(frame)
        if not (ADDRESS <= pc < ADDRESS + 64 or any(start <= pc < start + size for start, size in CALLEES.items())):
            raise ValueError('Original initializer escaped qualified own/callee instructions')
        visited.append(pc)

    def read(machine, access, location, width, value, unused):
        reads.append([location, width])

    def write(machine, access, location, width, value, unused):
        writes.append([location, width, value & ((1 << (width * 8)) - 1)])

    cpu.hook_add(UC_HOOK_CODE, code)
    cpu.hook_add(UC_HOOK_MEM_READ, read)
    cpu.hook_add(UC_HOOK_MEM_WRITE, write)
    cpu.emu_start(ADDRESS, RETURN, count=budget, timeout=1000000)
    actual = [cpu.reg_read(register) for register in match_runtime.REGISTERS]
    returned = cpu.reg_read(UC_ARM_REG_PC) == RETURN
    expected_memory, expected_io = bytearray(memory), bytearray(io)
    expected_writes, result = [], case['initialized']
    if case['initialized'] == 0:
        expected_memory[STATE - 0x03807000:STATE - 0x03807000 + 2] = b'\x01\x00'
        expected_memory[RESERVED - 0x03807000:RESERVED - 0x03807000 + 2] = (case['reserved'] | 2).to_bytes(2, 'little')
        expected_memory[STATE - 0x03807000 + 4:STATE - 0x03807000 + 12] = bytes(8)
        expected_io[0x210:0x214] = (case['ie'] & ~0x10).to_bytes(4, 'little')
        expected_writes = [[STATE, 2, 1], [RESERVED, 2, case['reserved'] | 2], [STATE + 4, 4, 0], [STATE + 8, 4, 0],
            [IO + 0x208, 2, 0], [IO + 0x210, 4, case['ie'] & ~0x10], [IO + 0x208, 2, case['ime']]]
        result = case['ie']
    effects = [row for row in writes if not STACK <= row[0] < STACK + 0x1000]
    expected_returns = [] if case['initialized'] else [(0x037FD10C, case['reserved'] | 2), (0x037FB8D8, case['ime']), (0x037FB928, case['ie'])]
    arguments = [(row['entry'], row['arguments'][0]) for row in entries if row['entry'] != 0x037FB8D8]
    expected_args = [] if case['initialized'] else [(0x037FD10C, 1), (0x037FB928, 16)]
    if returned and (actual[0] != result or actual[4:12] != initial[4:12] or actual[-2:] != initial[-2:]
        or bytes(cpu.mem_read(0x03807000, 0x1000)) != bytes(expected_memory)
        or bytes(cpu.mem_read(IO, 0x1000)) != bytes(expected_io) or effects != expected_writes or arguments != expected_args
        or [(row['entry'], row['result']) for row in returns] != expected_returns or active):
        raise ValueError('Actual initializer violates independent state/required-argument/return model')
    if any(not STACK + 0xEF0 <= address < STACK + 0xF00 for address, width, value in writes if STACK <= address < STACK + 0x1000):
        raise ValueError('Initializer wrote outside measured 16-byte nested frame')
    return {'returned': returned, 'registers': actual, 'cpsr': cpu.reg_read(UC_ARM_REG_CPSR), 'reads': reads, 'writes': writes,
        'memorySha256': digest(bytes(cpu.mem_read(0x03807000, 0x1000))), 'ioSha256': digest(bytes(cpu.mem_read(IO, 0x1000))),
        'stackSha256': digest(bytes(cpu.mem_read(STACK, 0x1000))), 'visited': visited, 'calleeEntries': entries, 'calleeReturns': returns,
        'expectedResult': result, 'expectedEffects': expected_writes}


def oracle(address, original, linked):
    if address != ADDRESS:
        raise ValueError('Unexpected alarm initializer entry')
    records, coverage, nested = [], set(), 0
    for seed, case in enumerate(cases()):
        native, rebuilt = execute(original, case, seed), execute(linked, case, seed)
        if native != rebuilt or not native['returned']:
            raise ValueError('Actual native/source-linked initializer differs or did not return')
        coverage.update(native['visited'])
        nested += len(native['calleeReturns']) + len(rebuilt['calleeReturns'])
        records.append({'case': case, 'native': native, 'compiled': rebuilt})
    own = sorted(pc for pc in coverage if ADDRESS <= pc < ADDRESS + 64)
    if own != list(range(ADDRESS, ADDRESS + 64, 4)):
        raise ValueError('Complete own initializer instruction coverage missing')
    return {'vectors': len(records), 'actualOriginalAndCompiledReturns': len(records) * 2,
        'actualOriginalCalleeReturns': nested, 'nativeCalleeReturnsAreOwnReturns': False,
        'all16InitialApsrCombinations': True, 'allOwnInstructionsVisited': True, 'ownInstructionAddresses': own,
        'providersReplaced': [], 'cpuModel': 'Unicorn TI925T ARMv4T surrogate', 'instructionLimit': 10000, 'timeoutMicroseconds': 1000000,
        'records': records, 'limitations': ['Static synthetic IME/IE backing only; no physical IRQ delivery or concurrency claim',
            'All original reservation/mask helpers execute; their source/data receive zero additional credit',
            'Twelve-byte state is a uniquely named measured view, not proof of full original object extent or enclosing lifecycle']}
