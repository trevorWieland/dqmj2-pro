import hashlib
import random
from project import configuration, native_dependencies
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_READ, UC_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC
from match_runtime import REGISTERS

ENTRY, SIZE = 0x0203A1D4, 140
DATA, GLOBAL, STACK, SP, STOP = 0x02380000, 0x020F4000, 0x03030000, 0x03030800, 0x0F000000
BASE, LOCK, ACTIVE, CALLBACK = 0x020F552C, 0x020F5508, 0x020F4C84, 0x02400000
DETACH, RELEASE = 0x0203A078, 0x0203A554
PROVIDERS = {0x0200708C, 0x02007110, 0x0203B854, 0x0203A5EC, CALLBACK}


def recipes():
    priorities = [-2147483648, -1, 0, 1, 2147483647]
    return [dict(index=i, slot=i % 8, old=i // 8 % 3, available=i // 24 % 3,
                 flags=i // 3 % 4, current=priorities[i // 7 % 5], incoming=priorities[i // 11 % 5],
                 active=i // 5 % 2, alias=i % 17 == 0) for i in range(768)]


def initial(item):
    rng = random.Random(0xA1D40000 + item['index'])
    pages = {DATA: bytearray(rng.randbytes(4096)), GLOBAL: bytearray(rng.randbytes(12288))}
    slot = BASE + item['slot'] * 0x174
    handle = slot + 0x14C if item['alias'] else DATA
    old = [0, DATA + 0x200, slot][item['old']]
    writes, calls = [], []

    def area(address):
        for base, content in pages.items():
            if base <= address < base + len(content):
                return content, address - base
        raise ValueError(hex(address))

    def put(address, value, record=False):
        content, offset = area(address)
        value &= 0xFFFFFFFF
        content[offset:offset + 4] = value.to_bytes(4, 'little')
        if record:
            writes.append([address, 4, value])

    def get(address):
        content, offset = area(address)
        return int.from_bytes(content[offset:offset + 4], 'little')

    flags = rng.getrandbits(32) & ~3 | item['flags']
    active = DATA + 0x700 if item['active'] else 0
    put(DATA + 0x200, 0)
    put(slot, 0)
    put(slot + 0x12C, [0, 1, 0xFFFFFFFF][item['available']])
    put(slot + 0x110, flags)
    put(slot + 0x150, item['current'])
    put(slot + 0x170, CALLBACK)
    put(ACTIVE + 4, active)
    put(handle, old)
    before = {base: bytes(value) for base, value in pages.items()}
    if old:
        put(old + 0x14C, 0, True)
        put(handle, 0, True)
    returned = 0
    if get(slot + 0x12C) and not (flags & 1 and item['incoming'] < item['current']):
        if flags & 1:
            calls.append([0x0200708C, LOCK])
            if active:
                calls.append([0x0200708C, active + 0x4C8])
            if flags & 2:
                calls.append([0x0203B854, slot])
            calls.extend([[CALLBACK, slot], [0x0203A5EC, slot], [0x02007110, LOCK]])
            if active:
                calls.append([0x02007110, active + 0x4C8])
        put(slot + 0x150, item['incoming'], True)
        put(slot + 0x110, get(slot + 0x110) & ~1 | 1, True)
        put(slot + 0x14C, handle, True)
        put(handle, slot, True)
        returned = slot
    registers = [rng.getrandbits(32) for unused in REGISTERS]
    registers[:3] = [handle, item['slot'], item['incoming'] & 0xFFFFFFFF]
    registers[13:] = [SP, STOP | (item['index'] & 1)]
    return before, {base: bytes(value) for base, value in pages.items()}, writes, calls, returned, registers


def execute(original, code, item):
    before, expected, writes, calls, returned, registers = initial(item)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, (len(original) + 4095) & ~4095)
    uc.mem_write(0x02000000, original)
    uc.mem_write(ENTRY, code)
    for page in range(GLOBAL, GLOBAL + 12288, 4096):
        if not any(start <= page and page + 4095 <= end for start, end, protection in uc.mem_regions()):
            uc.mem_map(page, 4096)
    for address, size in [(DATA, 4096), (STACK, 4096), (STOP, 4096), (CALLBACK, 4096)]:
        uc.mem_map(address, size)
    for base, value in before.items():
        uc.mem_write(base, value)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    control = 0x10 | ((item['index'] // 16 & 3) << 6)
    uc.reg_write(UC_ARM_REG_CPSR, (item['index'] % 16 << 28) | control)
    for register, value in zip(REGISTERS, registers):
        uc.reg_write(register, value)
    observed_writes, observed_calls, memory_events, pcs, pending, helper_returns = [], [], [], set(), [], []
    stopped, instructions = False, 0

    def data_address(address):
        return any(base <= address < base + len(value) for base, value in before.items())

    def memory(engine, access, address, size, value, user):
        if data_address(address):
            memory_events.append([access, address, size, value if access == UC_MEM_WRITE else int.from_bytes(engine.mem_read(address, size), 'little')])
            if access == UC_MEM_WRITE:
                observed_writes.append([address, size, value])

    def instruction(engine, address, width, user):
        nonlocal stopped, instructions
        instructions += 1
        if pending and address == pending[-1][1]:
            helper_returns.append(pending.pop()[0])
        if address == STOP:
            assert not pending
            stopped = True
            engine.emu_stop()
            return
        if address in PROVIDERS:
            observed_calls.append([address, engine.reg_read(REGISTERS[0])])
            lr = engine.reg_read(UC_ARM_REG_LR)
            for index in [0, 1, 2, 3, 12]:
                engine.reg_write(REGISTERS[index], (0xD4300000 + len(observed_calls) * 31 + index) & 0xFFFFFFFF)
            engine.reg_write(UC_ARM_REG_CPSR, (len(observed_calls) % 16 << 28) | control)
            engine.reg_write(UC_ARM_REG_LR, lr)
            engine.reg_write(UC_ARM_REG_PC, lr)
            return
        if address in [DETACH, RELEASE]:
            pending.append((address, engine.reg_read(UC_ARM_REG_LR) & ~1))
        assert (ENTRY <= address < ENTRY + 136 or DETACH <= address < DETACH + 24 or RELEASE <= address < RELEASE + 144), hex(address)
        pcs.add(address)

    uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, memory)
    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.emu_start(ENTRY, STOP + 4, count=2000)
    assert stopped and uc.reg_read(UC_ARM_REG_SP) == SP
    assert uc.reg_read(UC_ARM_REG_CPSR) & 255 == control | ((item['index'] & 1) << 5)
    for index in range(3, 12):
        assert uc.reg_read(REGISTERS[index]) == registers[index]
    assert bytes(uc.mem_read(STACK, SP - STACK - 128)) == bytes([0xA5]) * (SP - STACK - 128)
    assert bytes(uc.mem_read(SP, 4096 - (SP - STACK))) == bytes([0xA5]) * (4096 - (SP - STACK))
    pages = {base: bytes(uc.mem_read(base, len(value))) for base, value in before.items()}
    result = dict(returned=uc.reg_read(REGISTERS[0]), modelPassed=pages == expected and observed_writes == writes
                  and observed_calls == calls and uc.reg_read(REGISTERS[0]) == returned,
                  pagesSha256={hex(base): hashlib.sha256(value).hexdigest() for base, value in pages.items()},
                  writes=observed_writes, suppliedCalls=observed_calls, nativeHelperReturns=helper_returns,
                  registers=[uc.reg_read(register) for register in REGISTERS], cpsr=uc.reg_read(UC_ARM_REG_CPSR),
                  memoryEvents=memory_events, pcs=sorted(pcs), instructions=instructions)
    return result
