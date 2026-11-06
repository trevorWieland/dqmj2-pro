import hashlib
import random
import struct
import match_runtime
from match_runtime import REGISTERS
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_LR

ENTRY, TARGET, SERVICE = 0x020380E4, 0x020385A0, 0x02009128
DATA, STACK, STOP = 0x02380000, 0x03030000, 0x0F000000


def execute(original, code, index):
    rng = random.Random(ENTRY * 10000 + index)
    page = bytearray(rng.randbytes(4096))
    handle, resource = DATA + 0x40, DATA + 0x100 if index % 11 else 0
    current, identifier = index % 256, rng.randrange(256)
    value = [current, current ^ 1, current + 256, 0, 255, 256, 0xFFFFFFFF, 0x80000000][index // 256 % 8]
    struct.pack_into('<I', page, handle - DATA, resource)
    if resource:
        page[resource - DATA + 0x2E], page[resource - DATA + 0x3C] = current, identifier
    expected = bytearray(page)
    changed = bool(resource and value != current)
    if changed:
        expected[resource - DATA + 0x2E] = value & 255
    outcome = rng.getrandbits(32)
    expected_result = outcome if changed else current if resource else 0
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    uc.mem_write(DATA, bytes(page))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_map(STOP, 4096)
    control = 0x10 | (index % 4 << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[:2], initial[-2:] = [handle, value], [STACK + 0x800, STOP | (index & 1)]
    for register, number in zip(REGISTERS, initial):
        uc.reg_write(register, number)
    stopped, target_entered, target_returned, calls, pcs = False, False, False, [], set()

    def instruction(engine, address, width, user):
        nonlocal stopped, target_entered, target_returned
        if address == STOP:
            stopped = True
            target_returned = target_entered
            engine.emu_stop()
        elif address == SERVICE:
            calls.append(engine.reg_read(REGISTERS[0]))
            for register in [*REGISTERS[:4], REGISTERS[12]]:
                engine.reg_write(register, rng.getrandbits(32))
            engine.reg_write(REGISTERS[0], outcome)
            engine.reg_write(UC_ARM_REG_CPSR, rng.randrange(16) << 28 | control)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        else:
            assert ENTRY <= address < ENTRY + len(code) or TARGET <= address < TARGET + 40, hex(address)
            target_entered |= address == TARGET
            pcs.add(address)

    def memory(engine, access, address, width, number, user):
        assert DATA <= address and address + width <= DATA + 4096 or STACK + 0x700 <= address and address + width <= STACK + 0x800

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(ENTRY, STOP + 4, count=10000)
    assert stopped and target_returned and uc.reg_read(REGISTERS[-2]) == STACK + 0x800
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert uc.reg_read(UC_ARM_REG_CPSR) & 0xDF == control
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 0x800)) == bytes([0xA5]) * 0x800
    actual = bytes(uc.mem_read(DATA, 4096))
    result = uc.reg_read(REGISTERS[0])
    return dict(modelPassed=result == expected_result and actual == bytes(expected) and calls == ([identifier] if changed else []),
        actualReturns=1, actualTargetReturns=1, suppliedServiceCalls=len(calls), rawR0=result,
        registers=[uc.reg_read(r) for r in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR),
        backingSha256=hashlib.sha256(actual).hexdigest(), calls=calls, inputValue=value, currentByte=current,
        nullResource=not resource, observedPcs=sorted(pcs), definedCReturnValueClaim=False)
