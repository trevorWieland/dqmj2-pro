import hashlib
import random
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR
from match_runtime import REGISTERS

SIZES = {0x02023104: 224, 0x020231E4: 224, 0x02022CE4: 156, 0x02022B60: 388}
DATA, STACK, SP, STOP, ROUND = 0x02380000, 0x03030000, 0x03030800, 0x0F000000, 0x02022A04


def recipes(entry):
    return [dict(index=i, length=[1, 2, 3, 7, 16, 31, 32][i % 7],
                 otherLength=[1, 3, 8, 17, 30, 32][i // 7 % 6], alias=i % 5 == 0,
                 equal=i % 4 == 0, zero=i % 13 == 0) for i in range(512)]


def integer(digits):
    return int(''.join(str(value) for value in digits))


def initial(entry, item):
    rng = random.Random(entry * 1000 + item['index'])
    page = bytearray(rng.randbytes(4096))
    x_address, y_address, output = DATA + 0x200, DATA + 0x300, DATA + 0x100
    x = [rng.randrange(1, 10)] + [rng.randrange(10) for unused in range(item['length'] - 1)]
    y = [rng.randrange(1, 10)] + [rng.randrange(10) for unused in range(item['otherLength'] - 1)]
    ex = [-32768, -100, -1, 0, 1, 100, 32767][item['index'] // 9 % 7]
    ey = ex if item['index'] % 3 else [-32768, -1, 0, 1, 32767][item['index'] // 3 % 5]
    if item['equal']:
        y, ey = x[:] + [0] * (32 - len(x)), ex
    if item['zero'] and entry != 0x02022B60:
        x = [0]
    if item['index'] % 17 == 0 and entry != 0x02022B60:
        y = [0]
    if entry == 0x02022B60:
        ex, ey = item['index'] % 201 - 100, item['index'] // 3 % 201 - 100
        if item['index'] % 11 == 0:
            x, y = [9] * item['length'], [9] * item['otherLength']
        if item.get('unitProduct'):
            x, y, ex, ey = [1], [1], 0, 0
        if item['alias']:
            output = x_address
    for address, digits, exponent in [(x_address, x, ex), (y_address, y, ey)]:
        offset = address - DATA
        page[offset + 2:offset + 4] = exponent.to_bytes(2, 'little', signed=True)
        page[offset + 4] = len(digits)
        page[offset + 5:offset + 5 + len(digits)] = bytes(digits)
    expected_return, expected_digits, expected_exponent = None, None, None
    if entry in [0x02023104, 0x020231E4]:
        if item['alias']:
            y_address, y, ey = x_address, x, ex
        left_zero, right_zero = x[0] == 0, y[0] == 0
        left, right = tuple(x + [0] * (32 - len(x))), tuple(y + [0] * (32 - len(y)))
        if entry == 0x02023104:
            expected_return = int(left_zero and right_zero or not left_zero and not right_zero and ex == ey and left == right)
        else:
            expected_return = int(not right_zero and (left_zero or ex < ey or ex == ey and left < right))
        arguments = [x_address, y_address]
    elif entry == 0x02022CE4:
        length = [0, 1, 2, 7, 31, 32, 33, 40][item['index'] % 8]
        digits = [rng.randrange(10) for unused in range(length)]
        if item['index'] % 11 == 0:
            digits = [9] * length
        raw = bytes(value + 48 for value in digits) + bytes([0])
        if item['index'] % 9 == 0:
            prefix = [2] * 32
            prefix[-1] = item['index'] // 9 % 2 + 2
            tail = [[1], [4], [5], [5, 48, 48], [5, 48, 49], [6]][item['index'] // 18 % 6]
            raw = bytes(value + 48 for value in prefix) + bytes(tail) + bytes([0])
            digits = prefix
            length = 32 + len(tail)
        page[0x500:0x500 + len(raw)] = raw
        expected_digits = digits[:32]
        expected_exponent = ex
        round_up = length > 32 and (raw[32] > 5 or raw[32] == 5 and (any(value != 48 for value in raw[33:-1]) or expected_digits[-1] & 1))
        if round_up:
            number = integer(expected_digits) + 1
            expanded = str(number)
            if len(expanded) > 32:
                expected_exponent += 1
                expanded = '1' + '0' * 31
            expected_digits = [int(value) for value in expanded.zfill(32)]
        arguments = [output, DATA + 0x500, ex & 0xFFFFFFFF]
    else:
        value = integer(x) * integer(y)
        digits = str(value)
        expected_exponent = ex + ey + len(digits) - len(x) - len(y) + 1
        if len(digits) > 32:
            denominator = 10 ** (len(digits) - 32)
            quotient, remainder = divmod(value, denominator)
            quotient += remainder * 2 > denominator or remainder * 2 == denominator and quotient & 1
            digits = str(quotient)
            if len(digits) > 32:
                expected_exponent += 1
                digits = '1' + '0' * 31
        expected_digits = [int(value) for value in digits]
        arguments = [output, x_address, y_address]
    if expected_exponent is not None:
        expected_exponent = (expected_exponent + 32768) % 65536 - 32768
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:len(arguments)] = arguments
    registers[13:] = [SP, STOP | (item['index'] & 1)]
    return dict(before=bytes(page), output=output, registers=registers, returned=expected_return,
                exponent=expected_exponent, digits=expected_digits)


def execute(original, entry, code, item):
    model = initial(entry, item)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(entry, code)
    uc.mem_write(DATA, model['before'])
    for address in [STACK, STOP]:
        uc.mem_map(address, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    control = 0x10 | ((item['index'] // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, item['index'] % 16 << 28 | control)
    for register, value in zip(REGISTERS, model['registers']):
        uc.reg_write(register, value)
    pcs, writes, pending, helper_returns = set(), [], [], []
    stopped, instructions = False, 0

    def memory(engine, access, address, width, value, user):
        if DATA <= address < DATA + 4096:
            assert model['digits'] is not None and model['output'] <= address and address + width <= model['output'] + 38
            writes.append([address, width, value])

    def instruction(engine, address, width, user):
        nonlocal stopped, instructions
        instructions += 1
        if pending and address == pending[-1]:
            pending.pop()
            helper_returns.append(ROUND)
        if address == STOP:
            assert not pending
            stopped = True
            engine.emu_stop()
            return
        if address == ROUND:
            pending.append(engine.reg_read(UC_ARM_REG_LR) & ~1)
        assert entry <= address < entry + len(code) or ROUND <= address < ROUND + 76, hex(address)
        pcs.add(address)

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(entry, STOP + 4, count=30000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == SP
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((item['index'] & 1) << 5)
    for index in range(4, 12):
        assert uc.reg_read(REGISTERS[index]) == model['registers'][index]
    assert bytes(uc.mem_read(STACK, SP - STACK - 512)) == bytes([0xA5]) * (SP - STACK - 512)
    assert bytes(uc.mem_read(SP, 4096 - (SP - STACK))) == bytes([0xA5]) * (4096 - (SP - STACK))
    image = bytes(uc.mem_read(DATA, 4096))
    if model['digits'] is None:
        passed = image == model['before'] and uc.reg_read(REGISTERS[0]) == model['returned'] and not writes
        observed = dict(returned=uc.reg_read(REGISTERS[0]))
    else:
        offset = model['output'] - DATA
        record = image[offset:offset + 38]
        exponent = int.from_bytes(record[2:4], 'little', signed=True)
        digits = list(record[5:5 + record[4]])
        passed = exponent == model['exponent'] and digits == model['digits'] and record[0] == 0
        passed = passed and record[1] == model['before'][offset + 1] and record[37] == model['before'][offset + 37]
        observed = dict(exponent=exponent, digits=digits, expectedExponent=model['exponent'], expectedDigits=model['digits'])
    return dict(modelPassed=passed, observed=observed, pageSha256=hashlib.sha256(image).hexdigest(),
                writes=writes, helperReturns=helper_returns, pcs=sorted(pcs), instructions=instructions,
                registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR))
