import hashlib
import struct
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC
from main_format_wrappers_native_20261030 import REGS

ENTRY, DATA, STACK, STOP, FAILURE = 0x0201CB74, 0x02500000, 0x027C0000, 0x02FF0000, 0x02620000
DEPENDENCIES = [0x0201D948, 0x0201D69C, 0x0201B338, 0x0201BB14, 0x0201B8C8,
                0x0201C410, 0x0201BE10, 0x0201B124, 0x0201B21C]


def execute(main, format_bytes, arguments, expected, capacity, alignment, tag, failure_code=None):
    memory = bytearray([0xA5]) * 0x4000
    output, context, fmt, args = DATA + 0x100 + alignment, DATA + 0x300, DATA + 0x500, DATA + 0x700
    memory[0x300:0x30C] = struct.pack('<III', output, capacity, 0)
    memory[0x500:0x500 + len(format_bytes) + 1] = format_bytes + bytes(1)
    argument_bytes = bytearray()
    count_slots = []
    for index, item in enumerate(arguments):
        pointer = DATA + 0x1000 + 0x100 * index
        if isinstance(item, bytes):
            memory[pointer - DATA:pointer - DATA + len(item) + 1] = item + bytes(1)
            argument_bytes.extend(struct.pack('<I', pointer))
        elif isinstance(item, tuple) and item[0] == 'count':
            pointer = DATA + 0x2000 + index * 16
            argument_bytes.extend(struct.pack('<I', pointer))
            count_slots.append((pointer, item[1], item[2]))
        elif isinstance(item, tuple) and item[0] == 'wide':
            raw = item[1].encode('utf-16-le') + bytes(2)
            memory[pointer - DATA:pointer - DATA + len(raw)] = raw
            argument_bytes.extend(struct.pack('<I', pointer))
        elif isinstance(item, tuple) and item[0] == 'u64':
            argument_bytes.extend(struct.pack('<Q', item[1] & 0xFFFFFFFFFFFFFFFF))
        elif isinstance(item, tuple) and item[0] == 'f64':
            argument_bytes.extend(struct.pack('<d', item[1]))
        else:
            argument_bytes.extend(struct.pack('<I', item & 0xFFFFFFFF))
    memory[0x700:0x700 + len(argument_bytes)] = argument_bytes
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (DATA, 0x4000), (FAILURE, 0x1000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    if failure_code:
        machine.mem_write(FAILURE, failure_code)
    machine.mem_write(DATA, bytes(memory))
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | 0x1F)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, value in zip(REGS[:4], [FAILURE if failure_code else 0x0201D398, context, fmt, args]):
        machine.reg_write(reg, value)
    sp = STACK + 0x6000
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    saved = [machine.reg_read(reg) for reg in REGS[4:12]]
    events, writes, steps, pending, returns = [], [], [0], [], []
    targets = set(DEPENDENCIES) | {0x0201D398, FAILURE}

    def code_hook(uc, address, size, user):
        assert not ENTRY + 2076 <= address < ENTRY + 2084
        steps[0] += 1
        if pending and address == pending[-1][1]:
            target, return_pc, saved_sp = pending.pop()
            assert uc.reg_read(UC_ARM_REG_SP) == saved_sp
            returns.append(target)
        if address in targets:
            pending.append((address, uc.reg_read(UC_ARM_REG_LR), uc.reg_read(UC_ARM_REG_SP)))
        if address == STOP:
            events.append('actual-return')
            uc.emu_stop()
        else:
            assert 0x02000000 <= address < 0x02400000 or failure_code and FAILURE <= address < FAILURE + len(failure_code)

    def store(uc, access, address, size, value, user):
        if DATA <= address < DATA + 0x4000:
            assert output <= address and address + size <= output + capacity or context <= address and address + size <= context + 12 or any(pointer <= address and address + size <= pointer + width for pointer, width, value in count_slots)
        else:
            assert STACK <= address and address + size <= STACK + 0x8000
        writes.append([address, size, value & ((1 << (8 * size)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code_hook)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    machine.emu_start(ENTRY, STOP + 4, count=1000000, timeout=2000000)
    assert not pending
    assert events == ['actual-return'] and machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == sp
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == saved
    after = bytes(machine.mem_read(DATA, 0x4000))
    result = machine.reg_read(REGS[0])
    if expected is not None:
        assert result == (0xFFFFFFFF if failure_code else len(expected)), (format_bytes, result, expected)
        predicted = bytearray(memory)
        copied = 0 if failure_code else min(capacity, len(expected))
        predicted[output - DATA:output - DATA + copied] = expected[:copied]
        predicted[0x308:0x30C] = struct.pack('<I', copied)
        for pointer, width, value in count_slots:
            predicted[pointer - DATA:pointer - DATA + width] = value.to_bytes(width, 'little')
        assert after == predicted, (format_bytes, after[0x100:0x140].hex(), expected)
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    if failure_code:
        assert bytes(machine.mem_read(FAILURE, len(failure_code))) == failure_code
    return {'return': result, 'dataSha256': hashlib.sha256(after).hexdigest(), 'writes': writes,
            'instructions': steps[0], 'registers': [machine.reg_read(reg) for reg in REGS],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'stackSha256': hashlib.sha256(bytes(machine.mem_read(STACK, 0x8000))).hexdigest(),
            'actualKnownDependencyReturns': len(returns), 'actualReturn': True, 'outputHex': after[output - DATA:output - DATA + capacity].hex()}



def vectors():
    cases = [(b'', [], b''), (b'literal', [], b'literal'), (b'%s', [b'test'], b'test'),
             (b'%d/%u/%x', [-17, 0xFFFFFFFF, 0xABCDEF], b'-17/4294967295/abcdef'),
             (b'%lld/%llx', [('u64', 0x8000000000000001), ('u64', 0xFEDCBA9876543210)], b'-9223372036854775807/fedcba9876543210'),
             (b'%hhd/%hd', [0xFF, 0x8000], b'-1/-32768'),
             (b'[%8s][%-8s][%.2s]', [b'abc', b'abc', b'abc'], b'[     abc][abc     ][ab]'),
             (b'%+08d/%#x/%%/%c', [17, 0xAB, 0xFF], b'+0000017/0xab/%/\xff'),
             (b'%ls', [('wide', 'Ascii')], b'Ascii'), (b'%.2f', [('f64', 1.5)], b'1.50'),
             (b'%a', [('f64', 1.5)], None), (b'%020a', [('f64', 1.5)], None),
             (b'unsupported=%q', [], b'unsupported=%q'), (b'[%*.*s]', [8, 2, b'abcdef'], b'[      ab]'),
             (b'%jd/%zu/%td', [('u64', 0xFFFFFFFFFFFFFFEF), 0xFFFFFFFF, 0xFFFFFFEF], b'-17/4294967295/-17'),
             (b'[%s][%ls]', [0, 0], b'[][]')]
    for width, modifier in [(4, b''), (2, b'h'), (4, b'l'), (8, b'j'), (4, b'z'), (4, b't'), (8, b'll')]:
        cases.append((b'ab%' + modifier + b'n', [('count', width, 2)], b'ab'))
    for index, (fmt, arguments, expected) in enumerate(cases):
        for capacity in [0, 1, 2, 8, 64]:
            for alignment in range(4):
                yield {'case': index, 'format': fmt, 'arguments': arguments, 'expected': expected,
                       'capacity': capacity, 'alignment': alignment, 'failure': False}
    for index, (fmt, arguments, expected) in enumerate(cases[:16]):
        if not expected:
            continue
        for capacity in [0, 1, 64]:
            yield {'case': index, 'format': fmt, 'arguments': arguments, 'expected': b'',
                   'capacity': capacity, 'alignment': 0, 'failure': True}
