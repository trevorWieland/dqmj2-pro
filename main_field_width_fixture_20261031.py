import hashlib
import random
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS

SIZES = {0x02037750: 32, 0x02037D38: 52, 0x02037D6C: 60}
DATA, GLOBAL, STACK, SP, STOP = 0x02380000, 0x020F1000, 0x03030000, 0x03030800, 0x0F000000
ALLOCATE, THUNK = 0x0202B784, 0x02037D28
PHYSICAL = {0x0202B9DC: 24, 0x0202BA20: 84, 0x0202B9F4: 44, 0x02037D6C: 60}


def recipes():
    return [dict(index=i, allocate=i % 3 != 0, empty=i // 3 % 2 == 0,
                 count=[0, 1, 65535][i // 6 % 3], heap=[0, 1, 0xFFFFFFFF, 0x80000000][i // 18 % 4])
            for i in range(288)]


def initial(entry, item):
    rng = random.Random(entry * 1000 + item['index'])
    base, length = (GLOBAL, 4096) if entry == 0x02037750 else (DATA, 4096)
    data = bytearray(rng.randbytes(length))
    writes, calls = [], []

    def put(address, width, value, record=False):
        value &= (1 << (width * 8)) - 1
        data[address - base:address - base + width] = value.to_bytes(width, 'little')
        if record:
            writes.append([address, width, value])

    def header(address, offset, record=False):
        put(address, 4, 0, record)
        put(address + 4, 4, 0, record)
        put(address + 8, 2, 0, record)
        put(address + 10, 2, offset, record)

    if entry == 0x02037750:
        if item['index'] % 4 == 0:
            put(0x020F1F10, 4, item['index'] & 255)
        before = bytes(data)
        put(0x020F1EC8, 4, 0, True)
        put(0x020F1F10, 4, 0, True)
        returned = 0x020F1F10
    else:
        header(DATA + 4, 12)
        header(DATA + 16, 12)
        put(DATA, 4, item['heap'])
        if not item['empty']:
            put(DATA + 4, 4, DATA + 0x500)
            put(DATA + 8, 4, DATA + 0x500)
        put(DATA + 12, 2, item['count'])
        before = bytes(data)
        if entry == 0x02037D38:
            header(DATA + 4, 12, True)
            put(DATA, 4, item['heap'], True)
        calls.append([item['heap'], 20, 4])
        returned = int(item['allocate'])
        if returned:
            node = DATA + 0x200
            header(node, 0, True)
            if item['empty'] or entry == 0x02037D38:
                put(node + 16, 4, 0, True)
                put(node + 12, 4, 0, True)
                put(DATA + 4, 4, node, True)
            else:
                put(node + 12, 4, DATA + 0x500, True)
                put(node + 16, 4, 0, True)
                put(DATA + 0x510, 4, node, True)
            put(DATA + 8, 4, node, True)
            put(DATA + 12, 2, (0 if entry == 0x02037D38 else item['count']) + 1, True)
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:2] = [DATA, item['heap']]
    registers[13:] = [SP, STOP | (item['index'] & 1)]
    return dict(base=base, before=before, expected=bytes(data), writes=writes, calls=calls,
                returned=returned, registers=registers)


def execute(original, entry, code, item):
    model = initial(entry, item)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(entry, code)
    uc.mem_write(model['base'], model['before'])
    for address in [STACK, STOP]:
        uc.mem_map(address, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    control = 0x10 | ((item['index'] // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, item['index'] % 16 << 28 | control)
    for register, value in zip(REGISTERS, model['registers']):
        uc.reg_write(register, value)
    writes, calls, pending, returns, pcs = [], [], [], [], set()
    stopped, instructions, thunk_entries = False, 0, 0

    def memory(engine, access, address, width, value, user):
        if model['base'] <= address < model['base'] + 4096:
            writes.append([address, width, value])

    def instruction(engine, address, width, user):
        nonlocal stopped, instructions, thunk_entries
        instructions += 1
        if pending and address == pending[-1][1]:
            returns.append(pending.pop()[0])
        if address == STOP:
            assert not pending
            stopped = True
            engine.emu_stop()
            return
        if address == ALLOCATE:
            calls.append([engine.reg_read(register) for register in REGISTERS[:3]])
            lr = engine.reg_read(UC_ARM_REG_LR)
            for index in [1, 2, 3, 12]:
                engine.reg_write(REGISTERS[index], 0xD4380000 + index * 17)
            engine.reg_write(REGISTERS[0], DATA + 0x200 if item['allocate'] else 0)
            engine.reg_write(UC_ARM_REG_CPSR, (item['index'] % 16 << 28) | control)
            engine.reg_write(UC_ARM_REG_PC, lr)
            return
        if address == THUNK:
            thunk_entries += 1
        if address in PHYSICAL and address != entry:
            pending.append((address, engine.reg_read(UC_ARM_REG_LR) & ~1))
        allowed = [(entry, SIZES[entry] - (8 if entry == 0x02037750 else 0)), (THUNK, 12), *PHYSICAL.items()]
        assert any(start <= address < start + size for start, size in allowed), hex(address)
        pcs.add(address)

    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.emu_start(entry, STOP + 4, count=2000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == SP
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((item['index'] & 1) << 5)
    for index in range(3, 12):
        assert uc.reg_read(REGISTERS[index]) == model['registers'][index]
    assert bytes(uc.mem_read(STACK, SP - STACK - 128)) == bytes([0xA5]) * (SP - STACK - 128)
    assert bytes(uc.mem_read(SP, 4096 - (SP - STACK))) == bytes([0xA5]) * (4096 - (SP - STACK))
    data = bytes(uc.mem_read(model['base'], 4096))
    return dict(modelPassed=data == model['expected'] and writes == model['writes'] and calls == model['calls']
                and uc.reg_read(REGISTERS[0]) == model['returned'],
                pageSha256=hashlib.sha256(data).hexdigest(), writes=writes, suppliedCalls=calls,
                physicalNativeHelperReturns=returns, logicalThunkEntries=thunk_entries, pcs=sorted(pcs),
                registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR),
                instructions=instructions)
