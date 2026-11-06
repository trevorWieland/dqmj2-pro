import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_LR
from match_runtime import REGISTERS


SIZES = {0x0202A37C: 172, 0x0202B334: 48}
DEFAULT, FLAGS, SLOTS = 0x020DD580, 0x020EDD54, 0x020EDD64
STACK, STOP = 0x03030000, 0x0F000000
LENGTHS = [0, 1, 2, 3, 4, 7, 31, 0xFFFFFFFD, 0xFFFFFFFF]
ALIGNMENTS = [0, 1, 4, 32, -1, -4, -32, -0x80000000, 0x7FFFFFFF]


def execute(original, patches, entry, index):
    rng = random.Random(entry * 10000 + index)
    default_page, slot_page = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    heap_index = [0xFFFFFFFF, 0, 1, 7, 15, 16, 31, 127, 128, 255][index % 10]
    default_raw = [0, 1, 15, 16, 127, 128, 255][index // 10 % 7]
    default_page[DEFAULT & 4095] = default_raw
    enabled = index % 4 != 0
    count = [0, 1, 0x7FFFFFFF, 0xFFFFFFFF][index // 4 % 4]
    heap_word, allocated = rng.getrandbits(32), 0 if index % 5 == 0 else rng.getrandbits(32) | 1
    length, alignment = LENGTHS[index // 10 % len(LENGTHS)], ALIGNMENTS[index % len(ALIGNMENTS)]
    arguments = [heap_index if entry == 0x0202A37C else heap_word, length, alignment & 0xFFFFFFFF]
    selected = default_raw if default_raw < 128 else default_raw - 256
    if heap_index != 0xFFFFFFFF:
        selected = heap_index
    valid = (selected & 255) < 16
    if valid:
        at = (SLOTS & 4095) + selected * 20
        struct.pack_into('<I', slot_page, at, rng.getrandbits(32) | 1 if enabled else 0)
        struct.pack_into('<I', slot_page, at + 12, count)
        struct.pack_into('<I', slot_page, at + 16, heap_word)
    expected_default, expected_slots = default_page[:], slot_page[:]
    calls_expected = entry == 0x0202B334 or valid and enabled
    result = allocated if calls_expected else 0
    if entry == 0x0202A37C:
        expected_slots[(FLAGS & 4095) + 2] = 1 if not calls_expected else 0 if allocated else 5
        if calls_expected and allocated:
            struct.pack_into('<I', expected_slots, at + 12, (count + 1) & 0xFFFFFFFF)
    rounded = ((length if length else 1) + 3) & 0xFFFFFFFC
    target = 0x0202B044 if alignment >= 0 else 0x0202B0F8
    lower_arguments = [heap_word, rounded, (alignment if alignment >= 0 else -alignment) & 0xFFFFFFFF]
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    for address, code in patches.items():
        uc.mem_write(address, code)
    uc.mem_write(DEFAULT & ~4095, bytes(default_page))
    uc.mem_write(SLOTS & ~4095, bytes(slot_page))
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
    stopped, calls, returns, pending, writes, pcs = False, [], [], [], [], set()

    def instruction(engine, address, width, user):
        nonlocal stopped
        while pending and address == pending[-1]:
            returns.append(pending.pop())
        if address == STOP:
            stopped = True
            engine.emu_stop()
        elif address in [0x0202B044, 0x0202B0F8]:
            calls.append(dict(address=hex(address), arguments=[engine.reg_read(register) for register in REGISTERS[:3]]))
            for register in [*REGISTERS[:4], REGISTERS[12]]:
                engine.reg_write(register, rng.getrandbits(32))
            engine.reg_write(REGISTERS[0], allocated)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        else:
            assert any(start <= address < start + len(code) for start, code in patches.items()), hex(address)
            pcs.add(address)
            if entry == 0x0202A37C and address == 0x0202B334:
                pending.append(engine.reg_read(UC_ARM_REG_LR) & ~1)

    def memory(engine, access, address, width, value, user):
        assert (STACK + 0x700 <= address and address + width <= STACK + 0x800) or (SLOTS & ~4095) <= address and address + width <= (SLOTS & ~4095) + 4096
        if not STACK <= address < STACK + 4096:
            writes.append([address, width, value])

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(entry, STOP + 4, count=10000)
    assert stopped and not pending and uc.reg_read(REGISTERS[-2]) == STACK + 0x800
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 0x800)) == bytes([0xA5]) * 0x800
    actual_default = bytes(uc.mem_read(DEFAULT & ~4095, 4096))
    actual_slots = bytes(uc.mem_read(SLOTS & ~4095, 4096))
    expected_calls = [dict(address=hex(target), arguments=lower_arguments)] if calls_expected else []
    return dict(modelPassed=actual_default == bytes(expected_default) and actual_slots == bytes(expected_slots)
        and calls == expected_calls and uc.reg_read(REGISTERS[0]) == result,
        arguments=arguments, defaultByte=default_raw, slotEnabled=enabled, slotCounter=count, slotHeap=heap_word,
        suppliedAllocationResult=allocated, result=uc.reg_read(REGISTERS[0]), calls=calls,
        defaultSha256=hashlib.sha256(actual_default).hexdigest(), slotsSha256=hashlib.sha256(actual_slots).hexdigest(),
        nativeNestedReturns=len(returns), writes=writes, pcs=sorted(pcs),
        registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
