import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_LR
from match_runtime import REGISTERS


SIZES = {0x0203FCEC: 284, 0x0203D52C: 280}
STACK, STOP, PAGE = 0x03030000, 0x0F000000, 0x020F6000
CALLS = {
    0x0203FCEC: [0x02212180, 0x021E4380, 0x022138D8, 0x02210968, 0x021E7290,
        0x021E889C, 0x021D9AF4, 0x021DEA64, 0x021DD4F8, 0x021DA470, 0x021E4DB8,
        0x021D95A0, 0x021D90F0, 0x02066EE0, 0x02066D10, 0x0202AC4C, 0x0203D318, 0x0203D32C, 0x0203D340],
    0x0203D52C: [0x0202ABD8, 0x0203D30C, 0x0203D320, 0x0203D334, 0x0203CB2C,
        0x020033E8, 0x020035C0, 0x02002E5C, 0x02002C98, 0x0203D50C, 0x02008C58,
        0x02029C88, 0x02029CC4, 0x02029CF8, 0x02029D2C, 0x02029D5C],
}
ARGS = {0x0202AC4C: [0x020F60A8], 0x0202ABD8: [3, 0x10000], 0x020033E8: [11],
    0x020035C0: [16], 0x02002E5C: [96], 0x02002C98: [1, 0, 1], 0x0203D50C: [0],
    0x02008C58: [0, 0x06000000, 0x80000], 0x02029C88: [0, 0, 0], 0x02029CC4: [31],
    0x02029CF8: [63], 0x02029D2C: [0], 0x02029D5C: [0x7FFF]}
MAPPING = {0: 6, 1: 13, 2: 15, 4: 14, 5: 17, 6: 16, 9: 7, 10: 9, 11: 8, 12: 51}


def execute(original, overlay, code, entry, index):
    rng = random.Random(entry * 1000 + index)
    page, io = bytearray(rng.randbytes(4096)), bytearray(rng.randbytes(4096))
    page[0x5C] = index % 256
    expected_page, expected_io = page[:], io[:]
    if entry == 0x0203FCEC and index % 256 in MAPPING:
        expected_page[0x5E] = MAPPING[index % 256]
    if entry == 0x0203D52C:
        for offset, mode in [(10, 0xD00), (12, 0xE00)]:
            value = struct.unpack_from('<H', expected_io, offset)[0]
            struct.pack_into('<H', expected_io, offset, value & 0x43 | mode)
        value = struct.unpack_from('<I', expected_io)[0]
        struct.pack_into('<I', expected_io, 0, value & ~0x1F00 | 0xF00)
        for offset, mode in [(10, 0), (14, 1), (12, 2), (8, 3)]:
            value = struct.unpack_from('<H', expected_io, offset)[0]
            struct.pack_into('<H', expected_io, offset, value & ~3 | mode)
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(0x021D7240, overlay)
    uc.mem_write(entry, code)
    uc.mem_write(PAGE, bytes(page))
    uc.mem_map(0x04000000, 4096)
    uc.mem_write(0x04000000, bytes(io))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, bytes.fromhex('1eff2fe1'))
    control = 0x10 | (index % 4 << 6)
    uc.reg_write(UC_ARM_REG_CPSR, (index % 16 << 28) | control)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[-2:] = [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, initial):
        uc.reg_write(register, value)
    calls, pcs, writes, stopped = [], set(), [], False

    def instruction(engine, address, width, user):
        nonlocal stopped
        if address == STOP:
            stopped = True
            engine.emu_stop()
        elif entry <= address < entry + len(code):
            pcs.add(address)
        elif address in CALLS[entry]:
            assert address == CALLS[entry][len(calls)]
            arguments = [engine.reg_read(register) for register in REGISTERS[:4]]
            expected_arguments = ARGS.get(address, [])
            assert arguments[:len(expected_arguments)] == expected_arguments
            returned = [rng.getrandbits(32) for unused in range(5)]
            calls.append(dict(address=hex(address), arguments=arguments, suppliedOutputs=returned))
            for register, value in zip([*REGISTERS[:4], REGISTERS[12]], returned):
                engine.reg_write(register, value)
            engine.reg_write(UC_ARM_REG_CPSR, rng.randrange(16) << 28 | control)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        else:
            raise ValueError('Unexpected instruction: ' + hex(address))

    def memory(engine, access, address, width, value, user):
        assert (STACK + 0x700 <= address and address + width <= STACK + 0x800) or (PAGE <= address and address + width <= PAGE + 4096) or (0x04000000 <= address and address + width <= 0x04001000)
        if not STACK <= address < STACK + 4096:
            writes.append([address, width, value])

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(entry, STOP + 4, count=10000)
    assert stopped and len(calls) == len(CALLS[entry])
    assert uc.reg_read(REGISTERS[-2]) == initial[-2]
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 0x800)) == bytes([0xA5]) * 0x800
    actual_page = bytes(uc.mem_read(PAGE, 4096))
    actual_io = bytes(uc.mem_read(0x04000000, 4096))
    return dict(modelPassed=actual_page == bytes(expected_page) and actual_io == bytes(expected_io),
        pageSha256=hashlib.sha256(actual_page).hexdigest(), ioSha256=hashlib.sha256(actual_io).hexdigest(),
        calls=calls, writes=writes, pcs=sorted(pcs), registers=[uc.reg_read(register) for register in REGISTERS],
        cpsr=uc.reg_read(UC_ARM_REG_CPSR), actualReturns=1, actualHelperReturns=0)
