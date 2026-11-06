import hashlib
import random
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS


ENTRY, SIZE = 0x02023EF8, 104
DATA, STACK, STOP = 0x02380000, 0x03030000, 0x0F000000


def execute(original, code, index):
    rng = random.Random(20261031023 + index)
    page = bytearray(rng.randbytes(4096))
    length = [0, 1, 2, 3, 31, 63, 128][index // 256 % 7]
    left = bytes([index % 256]) + bytes(rng.randrange(1, 256) for unused in range(length)) + bytes([0])
    if index % 4 == 0:
        right = bytes(value + 32 if 65 <= value <= 90 else value - 32 if 97 <= value <= 122 else value for value in left)
    elif index % 4 == 1:
        right = left
    elif index % 4 == 2:
        right = bytes([(index + 1) % 256]) + left[1:]
    else:
        right = bytes([rng.randrange(256)]) + left[1:]
    a, b = DATA + 0x100, DATA + 0x400
    page[0x100:0x100 + len(left)] = left
    page[0x400:0x400 + len(right)] = right
    if index % 17 == 0:
        b, right = a, left
    fold = lambda text: bytes(value + 32 if 65 <= value <= 90 else value for value in text.split(bytes([0]), 1)[0])
    first, second = fold(left), fold(right)
    expected = ((first > second) - (first < second)) & 0xFFFFFFFF
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
    control = 0x10 | ((index // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:2] = [a, b]
    registers[-2:] = [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, registers):
        uc.reg_write(register, value)
    pcs, writes = set(), []
    stopped = False

    def instruction(engine, address, width, user):
        nonlocal stopped
        if address == STOP:
            stopped = True
            engine.emu_stop()
            return
        assert ENTRY <= address < ENTRY + len(code), hex(address)
        pcs.add(address)

    def memory(engine, access, address, width, value, user):
        assert STACK + 0x700 <= address and address + width <= STACK + 0x800
        writes.append([address, width, value])

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(ENTRY, STOP + 4, count=10000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == STACK + 0x800
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((index & 1) << 5)
    for i in range(4, 12):
        assert uc.reg_read(REGISTERS[i]) == registers[i]
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 0x800)) == bytes([0xA5]) * 0x800
    image = bytes(uc.mem_read(DATA, 4096))
    result = uc.reg_read(REGISTERS[0])
    return dict(modelPassed=result == expected and image == bytes(page), result=result,
        expected=expected, left=left.hex(), right=right.hex(), aliased=a == b,
        pageSha256=hashlib.sha256(image).hexdigest(), writes=writes, pcs=sorted(pcs),
        registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
