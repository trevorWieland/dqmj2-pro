import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

BASE, ENTRY, STACK, STOP = 0x02000000, 0x020D0AD8, 0x03030000, 0x0F000000
RECORDS, PARTY, RESERVE, LOOKUP, PAGE = 0x021BD674, 0x021BD540, 0x021BD54C, 0x02500000, 0x021D6B5D
HELPERS = {0x02062A10: 64, 0x02062A50: 24, 0x02062A88: 24, 0x02062AA0: 48,
    0x02062AD0: 48, 0x020CFA78: 88, 0x0207CD98: 32}
SERVICE = 0x02065818
REGS = [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4,
    UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9,
    UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_R12]


def execute(image, body, index, bound=30000):
    rng = random.Random(0xD0AD8000 + index)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(BASE, 0x800000)
    uc.mem_write(BASE, image)
    uc.mem_write(ENTRY, body)
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, rng.randbytes(4096))
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, b'\x70\x00\x20\xe1')
    first_count, second_count = index % 4, index // 4 % 4
    page = [0, 1, 7, 8, 9, 255][index // 16 % 6]
    ids = [0x10010 + i * 17 for i in range(6)]
    first = ids[:first_count]
    second = (ids[:second_count] if index // 96 % 2 else ids[3:3 + second_count])
    uc.mem_write(RECORDS, rng.randbytes(13200))
    for i in range(100): uc.mem_write(RECORDS + i * 132 + 20, struct.pack('<I', ids[i] if i < 6 else 0))
    uc.mem_write(PARTY, struct.pack('<3I', *(first + [0] * (3 - len(first)))))
    uc.mem_write(RESERVE, struct.pack('<3I', *(second + [0] * (3 - len(second)))))
    lookup = [ids[(i + index) % 6] if i % 4 else 0x100001 + i for i in range(100)]
    uc.mem_write(LOOKUP, struct.pack('<100I', *lookup))
    pointer = int.from_bytes(image[0x7CDB4:0x7CDB8], 'little')
    uc.mem_write(pointer, struct.pack('<I', LOOKUP))
    uc.mem_write(PAGE, bytes([page]))
    initial_ram = bytes(uc.mem_read(BASE, 0x800000))
    registers = [rng.getrandbits(32) for _ in REGS]
    handles = registers[:2]
    for reg, value in zip(REGS, registers): uc.reg_write(reg, value)
    uc.reg_write(UC_ARM_REG_CPSR, (rng.getrandbits(4) << 28) | 0x10)
    uc.reg_write(UC_ARM_REG_SP, STACK + 0x800)
    uc.reg_write(UC_ARM_REG_LR, STOP)
    state = dict(returned=False, calls=[], writes=[], own=set(), helpers={})

    def code(machine, address, size, unused):
        if address == STOP:
            state['returned'] = True
            machine.emu_stop()
            return
        if ENTRY <= address < ENTRY + len(body) - 4:
            state['own'].add(address)
            return
        if address == SERVICE:
            state['calls'].append([machine.reg_read(r) for r in REGS[:3]])
            for reg in [UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R12]:
                machine.reg_write(reg, rng.getrandbits(32))
            machine.reg_write(UC_ARM_REG_CPSR, (rng.getrandbits(4) << 28) | 0x10)
            machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))
            return
        allowed = next((base for base, length in HELPERS.items() if base <= address < base + length), None)
        assert allowed is not None, hex(address)
        if address == allowed: state['helpers'][hex(address)] = state['helpers'].get(hex(address), 0) + 1

    def write(machine, access, address, size, value, unused):
        assert STACK <= address < STACK + 4096, ('Unexpected nonstack write', hex(address))
        state['writes'].append((address, size, value))

    uc.hook_add(UC_HOOK_CODE, code)
    uc.hook_add(UC_HOOK_MEM_WRITE, write)
    uc.emu_start(ENTRY, STOP + 4, count=bound)
    assert state['returned'], 'Bounded prefix is not a return'
    expected = []
    for item in range(12):
        position = page * 12 + item
        identifier = lookup[position] if position < 100 else 0
        x, y = (item % 4 * 40 + 48) // 8, ((item // 4 + 1) * 40) // 8
        if identifier in first: expected.append([handles[0], x, y])
        if identifier in second: expected.append([handles[1], x, y])
    result = [uc.reg_read(r) for r in REGS]
    ram = bytes(uc.mem_read(BASE, 0x800000))
    passed = ram == initial_ram and state['calls'] == expected and result[4:12] == registers[4:12]
    passed &= uc.reg_read(UC_ARM_REG_SP) == STACK + 0x800
    return dict(actualReturn=True, modelPassed=bool(passed), registers=result, flags=uc.reg_read(UC_ARM_REG_CPSR),
        suppliedCalls=state['calls'], writes=state['writes'], observedInstructionAddresses=sorted(state['own']),
        logicalNativeHelperEntries=state['helpers'], physicalNativeHelperReturnCredit=0,
        ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(uc.mem_read(STACK, 4096))).hexdigest(),
        context=dict(partyCount=first_count, reserveCount=second_count, page=page, sharedGroups=index // 96 % 2))
