import hashlib
import random
import struct

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR

ENTRY = 0x02063A0C
PROVIDER = 0x02065D88
STATE = 0x021BD000
QUEUE = 0x021C0C64
TABLE = 0x02600000
STACK = 0x027F0000
STOP = 0x027FF800
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12, UC_ARM_REG_SP, UC_ARM_REG_LR]


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def execute(body, provider, state, table, item, registers, flags):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(ENTRY, body)
    machine.mem_write(PROVIDER, provider)
    machine.mem_write(STATE, state)
    machine.mem_write(TABLE, table)
    machine.mem_write(0x021C2AB4, struct.pack('<I', TABLE))
    stack = bytes(0x8000)
    machine.mem_write(STACK - len(stack), stack)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    visits, writes = set(), []

    def observe(uc, address, size, data):
        if not ENTRY <= address < ENTRY + len(body) - 4 and not PROVIDER <= address < PROVIDER + 20:
            raise AssertionError(('Queue reader escaped body/provider or executed a literal', hex(address)))
        visits.add(address)

    def write(uc, access, address, size, value, data):
        if not STACK - len(stack) <= address < STACK:
            raise AssertionError(('Read-only queue lookup wrote outside stack', hex(address)))
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, observe)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, count=2000)
    after = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or after[13] != registers[13]:
        raise AssertionError('Queue reader did not actually return with restored SP')
    if after[4:12] != registers[4:12] or machine.reg_read(UC_ARM_REG_CPSR) & 0x3F != 0x10:
        raise AssertionError('Queue reader violated preserved register/mode ABI')
    if bytes(machine.mem_read(STATE, len(state))) != state or bytes(machine.mem_read(TABLE, len(table))) != table:
        raise AssertionError('Queue reader changed source state or item records')
    return {'registers': after, 'flags': machine.reg_read(UC_ARM_REG_CPSR),
            'writes': writes, 'stackSha256': sha(bytes(machine.mem_read(STACK - len(stack), len(stack))))}, visits


def validate(arm, compiled, real_save, real_table):
    native = arm[ENTRY - 0x02000000:ENTRY - 0x02000000 + 104]
    provider = arm[PROVIDER - 0x02000000:PROVIDER - 0x02000000 + 24]
    rng = random.Random(2026102905)
    cases = []
    ids = [0, 1, 2, 7, 14, 15, 31, 63, 64, 127, 128, 200, 254, 255]
    for category in [0, 7]:
        for item in ids:
            for position in range(12):
                queue = bytearray([item ^ 1] * 24)
                queue[(category == 7) * 12 + position] = item
                cases.append(('position-and-padding', item, category, bytes(queue), None))
    for category in range(256):
        queue = bytes([45] * 24)
        cases.append(('category-byte', 45, category, queue, None))
    for count in range(256):
        item = rng.randrange(256)
        category = rng.randrange(256)
        queue = rng.randbytes(24)
        if count % 3:
            changed = bytearray(queue)
            for index in [2, 4, 8]:
                changed[(category == 7) * 12 + index] = item
            queue = bytes(changed)
        cases.append(('random-and-duplicates', item, category, queue, None))
    for item in range(min(255, len(real_table) // 88)):
        cases.append(('captured-save-and-item-table', item, real_table[item * 88 + 44],
                      real_save[0x37D8:0x37D8 + 24], real_table))
    results, visited, differences = [], set(), set()
    for label, item, category, queue, actual_table in cases:
        state = bytearray(rng.randbytes(0x5000))
        state[QUEUE - STATE:QUEUE - STATE + 24] = queue
        table = bytearray(actual_table if actual_table is not None else rng.randbytes(88 * 256))
        table[item * 88 + 44] = category
        registers = [rng.getrandbits(32) for register in REGS]
        registers[0] = item
        registers[13:] = [STACK, STOP]
        flags = (rng.getrandbits(4) << 28) | 0x10
        offset = 12 if category == 7 else 0
        selected = queue[offset:offset + 10]
        expected = selected.index(item) if item in selected else 0xFFFFFFFF
        outputs = []
        for body in [native, compiled]:
            output, pcs = execute(body, provider, bytes(state), bytes(table), item, registers, flags)
            if output['registers'][0] != expected:
                raise AssertionError(('Queue reader result differs', label, item, category))
            outputs.append(output)
            visited.update(pcs)
        if outputs[0]['writes'] != outputs[1]['writes'] or outputs[0]['flags'] != outputs[1]['flags'] or outputs[0]['stackSha256'] != outputs[1]['stackSha256'] or outputs[0]['registers'][14] != outputs[1]['registers'][14]:
            raise AssertionError('Queue reader stack/write/flag effects differ')
        differences.update(index for index in range(13) if outputs[0]['registers'][index] != outputs[1]['registers'][index])
        results.append({'class': label, 'item': item, 'categoryByte44': category,
                        'selectedPlane': int(category == 7), 'queueBytes': queue.hex(),
                        'returnWord': expected, 'actualReturns': 2})
    return {'cases': len(results), 'nativeAndCompiledActualReturns': len(results) * 2,
            'vectors': results, 'visitedNativeOrCompiledPcs': sorted(hex(pc) for pc in visited),
            'differingCallerSavedRegisterIndices': sorted(differences),
            'originalProviderBytes': 24, 'providerSha256': sha(provider), 'providerSourceCredit': 0,
            'actualReturnRequired': True, 'freshMachinePerExecution': True, 'instructionLimit': 2000,
            'abiAndReturnEffectsPass': True, 'nativeByteEqualityRequiredForSourceAcceptance': True}
