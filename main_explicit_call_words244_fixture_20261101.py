import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

DATA = 0x02400000
STACK = 0x03030000
STOP = 0x0F000000
OS_PAGE = 0x027FF000
ENTRIES = {0x02039F2C: 120, 0x020193F8: 36, 0x0203A4FC: 88}
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
NATIVE = {0x02006018: 12, 0x02005FF8: 32, 0x02005F08: 0xF0, 0x02008008: 24}


def cmp_flags(a, b):
    value = (a - b) & 0xFFFFFFFF
    return ((value >> 31) << 31) | (int(value == 0) << 30) | (int(a >= b) << 29) | ((((a ^ b) & (a ^ value)) >> 31) << 28)


def execute(image, entry, body, index, bound=4096):
    rng = random.Random(entry ^ (index * 0x10001))
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x100000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(entry, body)
    initial_main = bytes(machine.mem_read(0x02000000, 0x100000))
    machine.mem_map(DATA, 4096)
    page = bytearray(rng.randbytes(4096))
    obj, record = DATA + 0x100, DATA + 0x800
    machine.mem_map(OS_PAGE, 4096)
    os_data = bytearray(rng.randbytes(4096))
    struct.pack_into('<H', os_data, 0xFEC, 1)
    machine.mem_write(OS_PAGE, bytes(os_data))
    values = [0, 1, 255, 256, 65535, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]
    input_cpsr = 0x1F | ((index % 2) << 7) | ((index % 16) << 28)
    machine.reg_write(UC_ARM_REG_CPSR, input_cpsr)
    initial_registers = [rng.getrandbits(32) for register in REGISTERS]
    for register, value in zip(REGISTERS, initial_registers):
        machine.reg_write(register, value)
    if entry == 0x02039F2C:
        args = [obj, values[index % 8], values[(index // 8) % 8], rng.getrandbits(32), rng.getrandbits(32)]
        found = index % 4 != 0
        page[0x805], page[0x806] = index & 255, (index * 7) & 255
    elif entry == 0x020193F8:
        first = 0 if index % 5 == 0 else values[3 + index % 5]
        args = [first, record]
        status = [0, 1, 0x80000000, 0xFFFFFFFF][index % 4]
        restore = 0x80 if index % 3 else 0
        struct.pack_into('<II', page, 0x800, status, restore)
    else:
        args = [obj, values[(index // 2) % 8]]
        flags = rng.getrandbits(32)
        flags = (flags | 2) if index % 2 else (flags & ~2)
        struct.pack_into('<I', page, 0x210, flags)
    expected = bytearray(page)
    machine.mem_write(DATA, bytes(page))
    machine.mem_map(STACK, 4096)
    stack = bytearray(rng.randbytes(4096))
    if len(args) > 4:
        struct.pack_into('<I', stack, 2048, args[4])
    machine.mem_write(STACK, bytes(stack))
    machine.mem_map(STOP, 4096)
    for register, value in zip(REGISTERS, args[:4]):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 2048)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, own, helper_seen = [], [], set(), set()
    native_returns, return_waiting = [], []
    def put(address, value):
        machine.mem_write(address, struct.pack('<I', value))
        writes.append([address, 4, value])
    def supplied(address, words):
        calls.append(dict(address=address, words=words))
        result = 0
        if address == 0x02038F18:
            result = record if found else 0
        elif address == 0x0203A28C:
            result = (sum(words) + 0xA28C0000) & 0xFFFFFFFF
            put(obj + 0x24, words[2] ^ words[3])
        elif address == 0x0203A554:
            result = (words[0] ^ 0xA5540000) & 0xFFFFFFFF
            if words[0] == obj:
                put(obj + 0x154, 0x76540000 + index)
        elif address == 0x020379C4:
            put(obj + 0xE8, words[2])
            current = struct.unpack('<I', machine.mem_read(obj + 0x110, 4))[0]
            put(obj + 0x110, current ^ 0x4000)
        for register in [UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
            machine.reg_write(register, rng.getrandbits(32))
        machine.reg_write(UC_ARM_REG_R0, result)
        machine.reg_write(UC_ARM_REG_CPSR, ((index + len(calls)) % 16) << 28 | 0x1F | (input_cpsr & 0x80))
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
    def code(uc, address, size, unused):
        if return_waiting and address == return_waiting[-1][0]:
            native_returns.append(return_waiting.pop()[1])
        if entry <= address < entry + len(body):
            own.add(address)
            return
        counts = {0x02038F18: 1, 0x0203A28C: 10, 0x0203A554: 1, 0x020379C4: 3}
        if address in counts:
            count = counts[address]
            words = [uc.reg_read(register) for register in REGISTERS[:min(4, count)]]
            if count > 4:
                words += list(struct.unpack('<6I', uc.mem_read(uc.reg_read(UC_ARM_REG_SP), 24)))
            supplied(address, words)
            return
        assert entry == 0x020193F8 and any(base <= address < base + length for base, length in NATIVE.items()), hex(address)
        if address == 0x02005F08:
            calls.append(dict(address=address, words=[uc.reg_read(register) for register in REGISTERS[:4]], originalNative=True))
            return_waiting.append((uc.reg_read(UC_ARM_REG_LR), address))
        elif address == 0x02008008:
            calls.append(dict(address=address, words=[uc.reg_read(UC_ARM_REG_R0)], originalNative=True))
            return_waiting.append((uc.reg_read(UC_ARM_REG_LR), address))
        helper_seen.add(address)
    def write(uc, access, address, size, value, unused):
        if STACK <= address and address + size <= STACK + 4096:
            assert STACK + 1920 <= address and address + size <= STACK + 2048
        else:
            writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP, 'Bounded prefix is not return'
    assert not return_waiting and machine.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert all(machine.reg_read(register) == value for register, value in zip(REGISTERS[4:12], initial_registers[4:12]))
    after_stack = bytes(machine.mem_read(STACK, 4096))
    assert after_stack[:1920] == stack[:1920] and after_stack[2048:] == stack[2048:]
    assert bytes(machine.mem_read(0x02000000, 0x100000)) == initial_main
    assert bytes(machine.mem_read(OS_PAGE, 4096)) == os_data
    expected_calls, expected_writes, flags_passed = [], [], True
    if entry == 0x02039F2C:
        expected_calls.append(dict(address=0x02038F18, words=[args[3]]))
        result = 0
        if found:
            sixth = page[0x806] if args[1] & 0x80000000 else args[1]
            fifth = page[0x805] if args[2] & 0x80000000 else args[2]
            words = [obj, record, sixth, fifth, args[3], args[4], 0, 0, 0, 0]
            expected_calls.append(dict(address=0x0203A28C, words=words))
            result = (sum(words) + 0xA28C0000) & 0xFFFFFFFF
            expected_writes = [[obj + 0x24, 4, sixth ^ fifth]]
    elif entry == 0x020193F8:
        if status == 0:
            expected_calls.append(dict(address=0x02005F08, words=[args[0], 0x027FFFE8, 0x0200605C, 1], originalNative=True))
        expected_calls.append(dict(address=0x02008008, words=[restore], originalNative=True))
        result = input_cpsr & 0x80
        flag_expected = cmp_flags(args[0], 1) if status == 0 else cmp_flags(status, 0)
        expected_cpsr = (input_cpsr & 0x0FFFFF7F) | flag_expected | restore
        flags_passed = machine.reg_read(UC_ARM_REG_CPSR) == expected_cpsr
    else:
        if flags & 2 and args[1] != 0:
            expected_calls = [dict(address=0x020379C4, words=[obj + 0xE8, 0, args[1]])]
            expected_writes = [[obj + 0xE8, 4, args[1]], [obj + 0x110, 4, flags ^ 0x4000],
                [obj + 0x110, 4, (flags ^ 0x4000) | 8], [obj + 0x150, 4, 0]]
            result = 0
        else:
            expected_calls = [dict(address=0x0203A554, words=[obj])]
            expected_writes = [[obj + 0x154, 4, 0x76540000 + index]]
            result = obj ^ 0xA5540000
    for address, size, value in expected_writes:
        expected[address - DATA:address - DATA + size] = value.to_bytes(size, 'little')
    after = bytes(machine.mem_read(DATA, 4096))
    passed = flags_passed and calls == expected_calls and writes == expected_writes and after == expected and machine.reg_read(UC_ARM_REG_R0) == result
    return dict(modelPassed=passed, actualReturn=True, arguments=args, result=machine.reg_read(UC_ARM_REG_R0),
        calls=calls, writes=writes, registers=[machine.reg_read(register) for register in REGISTERS],
        cpsr=machine.reg_read(UC_ARM_REG_CPSR), pageSha256=hashlib.sha256(after).hexdigest(),
        stackSha256=hashlib.sha256(after_stack).hexdigest(), ownedObserved=sorted(own), helperObserved=sorted(helper_seen),
        actualNativeReturns=len(native_returns), nativeReturnEntries=native_returns,
        providedCalls=sum(not row.get('originalNative', False) for row in calls))
