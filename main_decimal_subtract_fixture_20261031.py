import hashlib
import random
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR
from match_runtime import REGISTERS

ENTRY, SIZE = 0x020232C4, 676
DATA, STACK, SP, STOP = 0x02380000, 0x03030000, 0x03030800, 0x0F000000


def integer(digits):
    return int(''.join(str(value) for value in digits))


def normalize(x, exponent_x, y, exponent_y):
    sx, sy = exponent_x - len(x) + 1, exponent_y - len(y) + 1
    scale = min(sx, sy)
    value = integer(x) * 10 ** (sx - scale) - integer(y) * 10 ** (sy - scale)
    assert value > 0
    difference = exponent_x - exponent_y
    assert 0 <= difference <= 31
    precision = min(max(len(x), len(y)) + difference, 32)
    cut = exponent_x - precision + 1
    minuend = integer(x) * 10 ** (sx - cut)
    subtrahend = integer(y) * 10 ** (sy - cut) if sy >= cut else integer(y) // 10 ** (cut - sy)
    retained = minuend - subtrahend
    discarded = precision - difference
    if discarded < len(y):
        first = y[discarded]
        if first < 5:
            retained -= 10 ** (precision - difference - 1)
        elif first == 5 and not any(y[discarded + 1:]) and retained & 1:
            retained -= 1
    assert retained > 0
    digits = str(retained)
    exponent = len(digits) - 1 + cut
    digits = digits.rstrip('0')
    return exponent, [int(value) for value in digits]


def recipes():
    result = []
    for index in range(384):
        rng = random.Random(0x232C4000 + index)
        x = [rng.randrange(1, 10)] + [rng.randrange(10) for unused in range([1, 2, 7, 16, 31, 32][index % 6] - 1)]
        y = [rng.randrange(1, 10)] + [rng.randrange(10) for unused in range([1, 3, 9, 17, 30, 32][index // 3 % 6] - 1)]
        exponent_x = index % 25 - 12
        exponent_y = exponent_x - [0, 1, 2, 7, 16, 31, 31, 31][index // 6 % 8]
        sx, sy = exponent_x - len(x) + 1, exponent_y - len(y) + 1
        scale = min(sx, sy)
        if integer(x) * 10 ** (sx - scale) <= integer(y) * 10 ** (sy - scale):
            x, y, exponent_x, exponent_y = y, x, exponent_y, exponent_x
            if x == y and exponent_x == exponent_y:
                x = [9, 9]
                y = [1]
        if index % 19 == 0:
            y = [0]
        result.append(dict(index=index, x=x, y=y, exponentX=exponent_x, exponentY=exponent_y, alias=index % 3 == 0))
    for index, item in enumerate([
        ([1], 31, [1], 0), ([1], 31, [1, 5], 0), ([1, 2], 31, [1, 5], 0),
        ([1], 8, [1], 0), ([9] * 32, 31, [5], 0), ([1, 0, 0, 1], 3, [1], 0),
        ([1], 31, [2, 5], 0), ([1], 31, [1, 5, 1], 0),
        ([1, 0, 5] + [0] * 28 + [1], 0, [5] + [0] * 29 + [1], -2),
    ], start=len(result)):
        x, exponent_x, y, exponent_y = item
        result.append(dict(index=index, x=x, y=y, exponentX=exponent_x, exponentY=exponent_y, alias=False))
    return result


def execute(original, code, item):
    rng = random.Random(0xDEC00000 + item['index'])
    page = bytearray(rng.randbytes(4096))
    x_address, y_address = DATA + 0x200, DATA + 0x300
    output = x_address if item['alias'] else DATA + 0x100
    for address, digits, exponent in [(x_address, item['x'], item['exponentX']), (y_address, item['y'], item['exponentY'])]:
        offset = address - DATA
        page[offset + 2:offset + 4] = exponent.to_bytes(2, 'little', signed=True)
        page[offset + 4] = len(digits)
        page[offset + 5:offset + 5 + len(digits)] = bytes(digits)
    first = bytes(page[x_address - DATA:x_address - DATA + 38])
    if item['y'][0] == 0:
        expected_exponent, expected_digits = item['exponentX'], item['x']
    else:
        expected_exponent, expected_digits = normalize(item['x'], item['exponentX'], item['y'], item['exponentY'])
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    uc.mem_write(DATA, bytes(page))
    for address in [STACK, STOP]:
        uc.mem_map(address, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    control = 0x10 | ((item['index'] // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, item['index'] % 16 << 28 | control)
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:3], registers[13:] = [output, x_address, y_address], [SP, STOP | (item['index'] & 1)]
    for register, value in zip(REGISTERS, registers):
        uc.reg_write(register, value)
    pcs, writes = set(), []
    stopped, instructions = False, 0

    def memory(engine, access, address, width, value, user):
        if DATA <= address < DATA + 4096:
            assert output <= address and address + width <= output + 38
            writes.append([address, width, value])

    def instruction(engine, address, width, user):
        nonlocal stopped, instructions
        instructions += 1
        if address == STOP:
            stopped = True
            engine.emu_stop()
            return
        assert ENTRY <= address < ENTRY + SIZE, hex(address)
        pcs.add(address)

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(ENTRY, STOP + 4, count=10000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == SP
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((item['index'] & 1) << 5)
    for index in range(4, 12):
        assert uc.reg_read(REGISTERS[index]) == registers[index]
    assert bytes(uc.mem_read(STACK, SP - STACK - 256)) == bytes([0xA5]) * (SP - STACK - 256)
    assert bytes(uc.mem_read(SP, 4096 - (SP - STACK))) == bytes([0xA5]) * (4096 - (SP - STACK))
    image = bytes(uc.mem_read(DATA, 4096))
    record = image[output - DATA:output - DATA + 38]
    exponent = int.from_bytes(record[2:4], 'little', signed=True)
    digits = list(record[5:5 + record[4]])
    passed = exponent == expected_exponent and digits == expected_digits and record[:2] == first[:2] and record[37] == first[37]
    if item['y'][0] == 0:
        passed = passed and record == first
    return dict(modelPassed=passed, exponent=exponent, digits=digits, expectedExponent=expected_exponent,
        expectedDigits=expected_digits, pageSha256=hashlib.sha256(image).hexdigest(), writes=writes,
        registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR),
        pcs=sorted(pcs), instructions=instructions)
