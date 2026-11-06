import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_LR
from match_runtime import REGISTERS


SIZES = {0x02038148: 44, 0x0202A44C: 40}
DATA, STACK, STOP = 0x02380000, 0x03030000, 0x0F000000


def execute(original, code, entry, index):
    rng = random.Random(entry * 1000 + index)
    page = bytearray(rng.randbytes(4096))
    expected = page[:]
    arguments = [rng.getrandbits(32) for unused in range(3)]
    calls, pcs, reads, writes, own_writes = [], set(), [], [], []
    helper_returns, pending, stopped, injected, change_pending = [], [], False, False, False
    handle, first, second = DATA + 0x100, DATA + 0x200, DATA + 0x300
    input_value, extra = arguments[1:]
    tick, allocation = rng.getrandbits(32), DATA + 0x500
    if entry == 0x02038148:
        initial_pointer = 0 if index // 256 == 0 else first
        struct.pack_into('<I', page, 0x100, initial_pointer)
        page[0x22C], page[0x32C] = index % 256, (index % 256) ^ 0x5A
        expected = page[:]
        arguments[0] = handle
        replace_handle = initial_pointer != 0 and index // 256 == 2
        used = second if replace_handle else first
        if replace_handle:
            struct.pack_into('<I', expected, 0x100, second)
        active = initial_pointer != 0 and expected[used - DATA + 0x2C] != 2
        if active:
            struct.pack_into('<IIII', expected, used - DATA + 0x1C, tick, input_value << 8 & 0xFFFFFFFF, 0, extra)
    else:
        length = [0, 1, 2, 3, 7, 16, 31, 128][index % 8]
        arguments = [rng.getrandbits(32), length, [-32, -4, 0, 4, 8, 64, -0x80000000][index % 7] & 0xFFFFFFFF]
        allocation = 0 if index % 5 == 0 else allocation
        if allocation:
            expected[0x500:0x500 + length] = bytes(length)
        replace_handle, active = False, False
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(entry, code)
    uc.mem_write(DATA, bytes(page))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, bytes.fromhex('1eff2fe1'))
    control = 0x10 | ((index % 4) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, (index % 16 << 28) | control)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[:3], initial[-2:] = arguments, [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, initial):
        uc.reg_write(register, value)

    def instruction(engine, address, width, user):
        nonlocal stopped, injected, change_pending
        if change_pending:
            engine.mem_write(handle, second.to_bytes(4, 'little'))
            change_pending, injected = False, True
        while pending and address == pending[-1][1]:
            helper_returns.append(pending.pop()[0])
        if address == STOP:
            stopped = True
            engine.emu_stop()
            return
        pcs.add(address)
        if address in [0x0202A37C, 0x020379EC]:
            words = [engine.reg_read(register) for register in REGISTERS[:3]]
            calls.append(dict(address=hex(address), arguments=words, supplied=True))
            result = allocation if address == 0x0202A37C else tick
            engine.reg_write(REGISTERS[0], result)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        elif address in [0x020379C4, 0x02008D78]:
            calls.append(dict(address=hex(address), arguments=[engine.reg_read(register) for register in REGISTERS[:3]], supplied=False))
            pending.append((hex(address), engine.reg_read(UC_ARM_REG_LR) & ~1))
        else:
            assert entry <= address < entry + len(code) or 0x020379C4 <= address < 0x020379EC or 0x02008C00 <= address < 0x02008F00, hex(address)

    def memory_read(engine, access, address, width, value, user):
        nonlocal change_pending
        if entry == 0x02038148 and address == handle and width == 4:
            reads.append(address)
            if len(reads) == 1 and replace_handle:
                change_pending = True

    def memory_write(engine, access, address, width, value, user):
        assert (STACK + 0x600 <= address and address + width <= STACK + 0x800) or (DATA <= address and address + width <= DATA + 4096)
        if DATA <= address < DATA + 4096:
            writes.append([address, width, value])

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_READ, memory_read)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory_write)
    uc.emu_start(entry, STOP + 4, count=20000)
    assert stopped and not pending and uc.reg_read(REGISTERS[-2]) == STACK + 0x800
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert bytes(uc.mem_read(STACK, 0x600)) == bytes([0xA5]) * 0x600
    assert bytes(uc.mem_read(STACK + 0x800, 0x800)) == bytes([0xA5]) * 0x800
    actual = bytes(uc.mem_read(DATA, 4096))
    if entry == 0x02038148:
        expected_reads = 1 if initial_pointer == 0 else 2
        expected_calls = [] if not active else [dict(address='0x20379c4', arguments=[used + 0x1C, input_value << 8 & 0xFFFFFFFF, extra], supplied=False), dict(address='0x20379ec', supplied=True)]
        contract_passed = len(reads) == expected_reads and len(calls) == len(expected_calls)
        if active:
            contract_passed &= calls[0] == expected_calls[0] and calls[1]['address'] == expected_calls[1]['address']
    else:
        contract_passed = calls[0]['address'] == '0x202a37c' and calls[0]['arguments'] == arguments
        contract_passed &= len(calls) == (2 if allocation else 1) and uc.reg_read(REGISTERS[0]) == allocation
        if allocation:
            contract_passed &= calls[1]['address'] == '0x2008d78' and calls[1]['arguments'] == [allocation, 0, length]
    return dict(modelPassed=actual == bytes(expected) and bool(contract_passed), backingSha256=hashlib.sha256(actual).hexdigest(),
        calls=calls, nativeHelperReturns=helper_returns, writes=writes, handleReads=len(reads), pointerReplacementSupplied=injected,
        pcs=sorted(pcs), registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
