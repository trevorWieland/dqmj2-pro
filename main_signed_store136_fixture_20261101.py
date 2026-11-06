import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY = 0x02037DC8
GLOBAL = 0x020F1F64
STACK = 0x03030000
STOP = 0x0F000000
REGISTERS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
    UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8,
    UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]
HELPERS = {0x020094B4: 0x38, 0x020389D8: 0x1C, 0x02037750: 0x20}
PROVIDERS = {0x0200F218: 1, 0x0200F230: 1, 0x02038248: 0}


def word(image, address):
    return struct.unpack_from('<I', image, address - 0x02000000)[0]


def execute(image, body, index, bound=512):
    rng = random.Random(0x37DC8000 + index)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x100000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(ENTRY, body)
    globals_found = [word(image, address) for address in [0x020094E4, 0x020389F0, 0x02037768, 0x0203776C]]
    assert all(0x02000000 <= address < 0x02100000 - 16 for address in globals_found)
    for address in [GLOBAL, *globals_found]:
        machine.mem_write(address, rng.randbytes(64))
    state = 0 if index % 2 == 0 else [1, 0x80000000, 0xFFFFFFFF, 0x12345678][(index // 2) % 4]
    initialized = [1, 0x80000000, 0xFFFFFFFF][(index // 8) % 3]
    machine.mem_write(GLOBAL + 12, struct.pack('<I', state))
    machine.mem_write(globals_found[0], struct.pack('<I', initialized))
    before = bytes(machine.mem_read(0x02000000, 0x100000))
    machine.mem_map(STACK, 4096)
    initial_stack = rng.randbytes(4096)
    machine.mem_write(STACK, initial_stack)
    machine.mem_map(STOP, 4096)
    cpsr = 0x10 | ((index % 16) << 28)
    machine.reg_write(UC_ARM_REG_CPSR, cpsr)
    initial_registers = [rng.getrandbits(32) for register in REGISTERS]
    for register, value in zip(REGISTERS, initial_registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 2048)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, writes, observed, helper_observed, returned, pending = [], [], set(), set(), [], []
    def code(uc, address, size, unused):
        if pending and address == pending[-1][0]:
            returned.append(pending.pop()[1])
        if ENTRY <= address < ENTRY + len(body):
            observed.add(address)
            return
        if address in PROVIDERS:
            count = PROVIDERS[address]
            arguments = [uc.reg_read(register) for register in REGISTERS[:count]]
            calls.append(dict(address=address, arguments=arguments))
            for register in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
                uc.reg_write(register, rng.getrandbits(32))
            flags = ((index + len(calls)) % 16) << 28
            uc.reg_write(UC_ARM_REG_CPSR, (uc.reg_read(UC_ARM_REG_CPSR) & 0x0FFFFFFF) | flags)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
            return
        if address in HELPERS:
            pending.append((uc.reg_read(UC_ARM_REG_LR), address))
        assert any(base <= address < base + length for base, length in HELPERS.items()), hex(address)
        helper_observed.add(address)
    def write(uc, access, address, size, value, unused):
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(ENTRY, STOP, count=bound)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP, 'Bound exhaustion is not return'
    assert not pending and machine.reg_read(UC_ARM_REG_SP) == STACK + 2048
    assert machine.reg_read(UC_ARM_REG_LR) == (STOP if state else ENTRY + 0x5C)
    assert all(machine.reg_read(register) == value for register, value in zip(REGISTERS[4:12], initial_registers[4:12]))
    stack = bytes(machine.mem_read(STACK, 4096))
    assert stack[:2032] == initial_stack[:2032] and stack[2048:] == initial_stack[2048:]
    expected = bytearray(before)
    expected_writes = []
    if state == 0:
        expected_writes = [[GLOBAL + 12, 4, 1], [GLOBAL + 16, 4, 0x02037FAC],
            [GLOBAL + 20, 4, 0], [GLOBAL + 28, 4, 0x02037FE4], [GLOBAL + 32, 4, 0],
            [globals_found[1] + 8, 4, 0], [globals_found[1], 4, 0], [globals_found[1] + 4, 4, 0],
            [globals_found[2], 4, 0], [globals_found[3], 4, 0], [GLOBAL, 1, 255], [GLOBAL + 4, 4, 1]]
        for address, size, value in expected_writes:
            expected[address - 0x02000000:address - 0x02000000 + size] = value.to_bytes(size, 'little')
    expected_calls = [] if state else [dict(address=0x0200F218, arguments=[GLOBAL + 16]),
        dict(address=0x0200F230, arguments=[GLOBAL + 28]), dict(address=0x02038248, arguments=[])]
    after = bytes(machine.mem_read(0x02000000, 0x100000))
    nonstack = [event for event in writes if not STACK <= event[0] < STACK + 4096]
    expected_helpers = [] if state else [0x020094B4, 0x020389D8, 0x02037750]
    result = machine.reg_read(UC_ARM_REG_R0)
    passed = result == GLOBAL and after == expected and nonstack == expected_writes and calls == expected_calls and returned == expected_helpers
    return dict(index=index, initialState=state, lowerInitializationFlag=initialized, result=result, modelPassed=passed,
        actualReturn=True, registers=[machine.reg_read(register) for register in REGISTERS], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        mainMemorySha256=hashlib.sha256(after).hexdigest(), stackSha256=hashlib.sha256(stack).hexdigest(),
        writes=writes, calls=calls, actualNativeHelperReturns=len(returned), helpersReturned=returned,
        ownedObserved=sorted(observed), helperObserved=sorted(helper_observed))
