import hashlib
import random
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

ENTRY, SIZE = 0x02023DB4, 148
DATA, STACK, STOP = 0x02380000, 0x03030000, 0x0F000000


def execute(original, code, index):
    rng = random.Random(20261031022998 + index)
    page = bytearray(rng.randbytes(4096))
    values = [0, (1 << 64) - 1, 1 << (index % 64), (1 << (index % 65)) - 1,
        0x5555555555555555, 0xAAAAAAAAAAAAAAAA, rng.getrandbits(64)]
    value = values[index % len(values)]
    expected = value.bit_count()
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    uc.mem_write(DATA, bytes(page))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, bytes.fromhex('1eff2fe1'))
    control = 0x1F | (0x80 if index & 2 else 0)
    uc.reg_write(UC_ARM_REG_CPSR, control)
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:2] = [value & 0xFFFFFFFF, value >> 32]
    registers[-2:] = [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, registers):
        uc.reg_write(register, value)
    pcs, writes = set(), []
    returned = False

    def instruction(engine, address, width, user):
        nonlocal returned
        if address == STOP:
            returned = True
            engine.emu_stop()
            return
        assert ENTRY <= address < ENTRY + len(code), hex(address)
        pcs.add(address)

    def memory(engine, access, address, width, value, user):
        writes.append([address, width, value])

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(ENTRY, STOP + 4, count=1000)
    assert returned and uc.reg_read(UC_ARM_REG_SP) == STACK + 0x800
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((index & 1) << 5)
    for i in range(4, 12):
        assert uc.reg_read(REGISTERS[i]) == registers[i]
    image = bytes(uc.mem_read(DATA, 4096))
    assert bytes(uc.mem_read(STACK, 4096)) == bytes([0xA5]) * 4096
    result = uc.reg_read(REGISTERS[0])
    return dict(modelPassed=result == expected and image == bytes(page) and not writes,
        result=result, expected=expected, inputU64=value,
        pageSha256=hashlib.sha256(image).hexdigest(), writes=writes, pcs=sorted(pcs),
        registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
