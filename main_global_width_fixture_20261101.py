import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

DATA = 0x02400000
STACK = 0x03030000
STOP = 0x0F000000
GLOBALS = [0x020EC588, 0x020EC36C, 0x020E535C, 0x020DD60C, 0x020DD610,
    0x020DD614, 0x021D71EC, 0x020DCB40, 0x020E3300, 0x020E5358, 0x020DCB58]
PROVIDERS = {0x02019898: 1, 0x020065F0: 6, 0x0200698C: 1, 0x020156CC: 1,
    0x02008E0C: 4, 0x020102C4: 1, 0x020102E0: 1, 0x02008C14: 3,
    0x0202A498: 2, 0x0200C344: 1}
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, entry, body, index, bound=4096):
    rng = random.Random(entry ^ (index * 0x10001))
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x200000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(entry, body)
    machine.mem_map(DATA, 65536)
    initial_page = rng.randbytes(65536)
    machine.mem_write(DATA, initial_page)
    machine.mem_map(STACK, 8192)
    initial_stack = rng.randbytes(8192)
    machine.mem_write(STACK, initial_stack)
    machine.mem_map(0x04000000, 4096)
    machine.mem_map(STOP, 4096)
    initial_registers = [rng.getrandbits(32) for unused in REGISTERS]
    for register, value in zip(REGISTERS, initial_registers):
        machine.reg_write(register, value)
    cpsr = [0x1F, 0x9F, 0x5F, 0xDF][index % 4] | ((index % 16) << 28)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    machine.reg_write(UC_ARM_REG_SP, STACK + 4096)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    predicate = (index // 3) % 2
    argument = DATA + 0x1000
    selector = [9, 10, 1, 0, 2, 0xFFFFFFFF][index % 6]
    word = [0, 1, 0x12345678, 0xFFFF0000, 0xFFFFFFFF, 0x80000100][(index // 6) % 6]
    base = DATA + 0x4000
    globals_before = {address: rng.getrandbits(32) for address in GLOBALS}
    globals_before[0x020EC588] = [0, DATA + 0x2000, 0x80000000][index % 3]
    globals_before[0x020EC36C] = 0 if index % 3 == 0 else base
    globals_before[0x020E535C] = word
    globals_before[0x020DD60C] = word
    globals_before[0x020DD610] = word ^ 0x12345678
    globals_before[0x020DD614] = word ^ 0xFEDCBA98
    globals_before[0x021D71EC] = [0, 0x02403000, 0x80000000][index % 3]
    globals_before[0x020E5358] = [0, 1, 0x80000000][index % 3]
    for address, value in globals_before.items():
        machine.mem_write(address, struct.pack('<I', value))
    slot = index % 8 + 1
    flag = [0, 7, 8, 0x80000007][(index // 2) % 4]
    machine.mem_write(base + (slot - 1) * 4 + 0x14E8, struct.pack('<I', flag))
    display = rng.getrandbits(32)
    machine.mem_write(0x04000000, struct.pack('<I', display))
    if entry in [0x0201434C, 0x020143D0]:
        arguments = [slot]
    elif entry == 0x0200C2C8:
        arguments = [argument, selector]
    elif entry == 0x0202E958:
        arguments = [argument, word]
    elif entry == 0x02014324:
        arguments = [word]
    elif entry in [0x0201980C, 0x0200BCDC]:
        arguments = [argument]
    else:
        arguments = []
    if entry == 0x02014324:
        globals_before[0x020EC36C] = base
        machine.mem_write(0x020EC36C, struct.pack('<I', base))
    for register, value in zip(REGISTERS, arguments):
        machine.reg_write(register, value)
    expected_page = bytearray(machine.mem_read(DATA, 65536))
    expected_globals = dict(globals_before)
    expected_calls = []
    expected_result = None
    expected_display = display

    def expected_call(address, values):
        expected_calls.append([address, values])

    if entry == 0x0201980C:
        if not globals_before[0x020EC588]:
            expected_globals[0x020EC588] = argument
            expected_call(0x02019898, [argument + 0xC4])
            expected_call(0x02019898, [0x020EC58C])
            struct.pack_into('<I', expected_page, argument + 0xC0 - DATA, 0)
            expected_call(0x020065F0, [argument, 0x020198AC, argument, 0x020EC9B0, 0x400, 0x14])
            expected_call(0x0200698C, [argument])
        expected_result = 0x80
    elif entry == 0x0201434C:
        expected_result = 0
        if globals_before[0x020EC36C]:
            expected_call(0x020156CC, [slot])
            if predicate:
                source = base + 0x1340 + (slot - 1) * 0x16
                destination = base + 0x1772
                expected_call(0x02008E0C, [source, destination, 0x16, base])
                expected_page[destination - DATA:destination - DATA + 0x16] = expected_page[source - DATA:source - DATA + 0x16]
                expected_result = destination
    elif entry == 0x020143D0:
        if globals_before[0x020EC36C]:
            expected_call(0x020156CC, [slot])
        expected_result = int(bool(globals_before[0x020EC36C] and predicate and flag == 7))
    elif entry == 0x0200C2C8:
        if selector in [9, 10]:
            expected_call(0x020102C4 if selector == 9 else 0x020102E0, [word & 0xFFFF])
        expected_result = 0 if selector in [9, 10] else 4 if selector == 1 else 8
    elif entry == 0x0202E958:
        expected_call(0x02008C14, [0, argument, 0x54])
        expected_page[0x1000:0x1054] = bytes(0x54)
        for offset, value in [(0xC, globals_before[0x020DD614]), (0x14, globals_before[0x020DD610]),
                (0x1C, word), (4, word)]:
            struct.pack_into('<I', expected_page, 0x1000 + offset, value)
        expected_result = word
    elif entry == 0x020D34FC:
        if globals_before[0x021D71EC]:
            expected_call(0x0202A498, [1, globals_before[0x021D71EC]])
        expected_result = int(bool(globals_before[0x021D71EC] and predicate))
        if expected_result:
            expected_globals[0x021D71EC] = 0
    elif entry == 0x02002C14:
        expected_globals[0x020DCB40] &= 0xFFFF0000
        expected_globals[0x020E3300] = (expected_globals[0x020E3300] & 0xFFFF0000) | ((display >> 16) & 3)
        expected_result = expected_display = display & ~0x30000
    elif entry == 0x0200BCDC:
        expected_result = argument
        if not globals_before[0x020E5358]:
            expected_globals[0x020E5358] = 1
            expected_call(0x0200C344, [argument])
            expected_result = argument ^ 0x13579BDF
    elif entry == 0x02014324:
        struct.pack_into('<I', expected_page, base + 0x14E4 - DATA, word)
        expected_result = 0x80
    elif entry == 0x02006DE4:
        expected_globals[0x020DCB58] = 0x82000001
        expected_result = 0x82000001
    else:
        raise ValueError(hex(entry))
    calls, writes, owned, helpers = [], [], set(), set()
    actual_irq_returns = 0
    irq_return_pcs = set()

    def code(unused, address, size, context):
        nonlocal actual_irq_returns
        if entry <= address < entry + len(body):
            owned.update(range(address, address + size))
        if 0x02007FF4 <= address < 0x02008020:
            helpers.update(range(address, address + size))
        if address in irq_return_pcs:
            actual_irq_returns += 1
            irq_return_pcs.remove(address)
        if address in [0x02007FF4, 0x02008008]:
            irq_return_pcs.add(machine.reg_read(UC_ARM_REG_LR))
        if address not in PROVIDERS:
            return
        count = PROVIDERS[address]
        values = [machine.reg_read(register) for register in REGISTERS[:min(4, count)]]
        if count > 4:
            values.extend(struct.unpack('<' + 'I' * (count - 4), machine.mem_read(machine.reg_read(UC_ARM_REG_SP), (count - 4) * 4)))
        calls.append([address, values])
        if address == 0x02008E0C:
            machine.mem_write(values[1], bytes(machine.mem_read(values[0], values[2])))
        elif address == 0x02008C14:
            machine.mem_write(values[1], bytes([values[0] & 255]) * values[2])
        result = predicate if address in [0x020156CC, 0x0202A498] else values[0] ^ 0x13579BDF
        machine.reg_write(UC_ARM_REG_R0, result)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    def write(unused, access, address, size, value, context):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK + 4096
    for register, value in zip(REGISTERS[4:12], initial_registers[4:12]):
        assert machine.reg_read(register) == value
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0xDF == cpsr & 0xDF
    stack = bytes(machine.mem_read(STACK, 8192))
    assert stack[:4000] == initial_stack[:4000] and stack[4096:] == initial_stack[4096:]
    page = bytes(machine.mem_read(DATA, 65536))
    globals_after = {address: struct.unpack('<I', machine.mem_read(address, 4))[0] for address in GLOBALS}
    result = machine.reg_read(UC_ARM_REG_R0)
    display_after = struct.unpack('<I', machine.mem_read(0x04000000, 4))[0]
    passed = result == expected_result and page == expected_page and globals_after == expected_globals
    passed &= calls == expected_calls and display_after == expected_display
    return dict(modelPassed=bool(passed), result=result, expectedResult=expected_result,
        registers=[machine.reg_read(register) for register in REGISTERS], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        globals=globals_after, display=display_after, calls=calls, orderedStores=writes,
        pageSha256=hashlib.sha256(page).hexdigest(), stackSha256=hashlib.sha256(stack).hexdigest(),
        ownedObserved=sorted(owned), irqObserved=sorted(helpers), actualIrqReturns=actual_irq_returns)
