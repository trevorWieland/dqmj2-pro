import hashlib
import random
import struct
import match_runtime
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_LR
from match_runtime import REGISTERS


DATA, STACK, STOP = 0x02380000, 0x03030000, 0x0F000000


def execute(original, code, entry, index):
    rng = random.Random(entry * 10000 + index)
    page = bytearray(rng.randbytes(4096))
    heap, node_count = DATA + 0x40, index % 7
    nodes = [DATA + 0x200 + offset * 0x200 for offset in range(node_count)]
    rng.shuffle(nodes)
    sizes = [rng.randrange(0, 97) * 4 for unused in nodes]
    size = [0, 1, 3, 4, 7, 16, 31, 64, 128, 384][index // 7 % 10]
    alignment = [1, 2, 4, 8, 16, 32, 64][index // 10 % 7]
    flags = rng.randrange(0x10000) & ~1 | (index // 70 & 1)
    struct.pack_into('<II', page, heap - DATA + 0x24, nodes[0] if nodes else 0, nodes[-1] if nodes else 0)
    struct.pack_into('<H', page, heap - DATA + 0x36, flags)
    for position, node in enumerate(nodes):
        struct.pack_into('<I', page, node - DATA + 4, sizes[position])
        struct.pack_into('<II', page, node - DATA + 8, nodes[position - 1] if position else 0,
            nodes[position + 1] if position + 1 < len(nodes) else 0)
    backwards = entry == 0x0202B0F8
    ordered = list(reversed(list(zip(nodes, sizes)))) if backwards else list(zip(nodes, sizes))
    eligible = []
    for node, capacity in ordered:
        body = node + 16
        start = ((body + capacity - size) & ~(alignment - 1)) if backwards else ((body + alignment - 1) & ~(alignment - 1))
        if (start >= body if backwards else capacity >= size + start - body):
            eligible.append((node, capacity, start))
    chosen = (min(eligible, key=lambda item: item[1]) if flags & 1 else eligible[0]) if eligible else None
    outcome = rng.getrandbits(32)
    expected = [] if chosen is None else [[heap + 0x24, chosen[0], chosen[2], size, int(backwards)]]
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.ctl_set_cpu_model(UC_CPU_ARM_946)
    uc.mem_map(0x02000000, 0x400000)
    uc.mem_write(0x02000000, original)
    uc.mem_write(entry, code)
    uc.mem_write(DATA, bytes(page))
    uc.mem_map(STACK, 4096)
    uc.mem_write(STACK, bytes([0xA5]) * 4096)
    uc.mem_map(STOP, 4096)
    uc.mem_write(STOP, bytes.fromhex('1eff2fe1'))
    control = 0x10 | (index % 4 << 6)
    uc.reg_write(UC_ARM_REG_CPSR, index % 16 << 28 | control)
    initial = [rng.getrandbits(32) for unused in REGISTERS]
    initial[:3], initial[-2:] = [heap, size, alignment], [STACK + 0x800, STOP | (index & 1)]
    for register, value in zip(REGISTERS, initial):
        uc.reg_write(register, value)
    stopped, calls, pcs = False, [], set()

    def instruction(engine, address, width, user):
        nonlocal stopped
        if address == STOP:
            stopped = True
            engine.emu_stop()
        elif address == 0x0202AE9C:
            words = [engine.reg_read(register) for register in REGISTERS[:4]]
            words.append(int.from_bytes(engine.mem_read(engine.reg_read(REGISTERS[-2]), 4), 'little'))
            calls.append(words)
            for register in [*REGISTERS[:4], REGISTERS[12]]:
                engine.reg_write(register, rng.getrandbits(32))
            engine.reg_write(REGISTERS[0], outcome)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
        else:
            assert entry <= address < entry + len(code), hex(address)
            pcs.add(address)

    def memory(engine, access, address, width, value, user):
        assert STACK + 0x700 <= address and address + width <= STACK + 0x800

    uc.hook_add(UC_HOOK_CODE, instruction)
    uc.hook_add(UC_HOOK_MEM_WRITE, memory)
    uc.emu_start(entry, STOP + 4, count=10000)
    assert stopped and uc.reg_read(REGISTERS[-2]) == STACK + 0x800
    assert all(uc.reg_read(REGISTERS[i]) == initial[i] for i in range(4, 12))
    assert bytes(uc.mem_read(STACK, 0x700)) == bytes([0xA5]) * 0x700
    assert bytes(uc.mem_read(STACK + 0x800, 0x800)) == bytes([0xA5]) * 0x800
    actual = bytes(uc.mem_read(DATA, 4096))
    result = uc.reg_read(REGISTERS[0])
    return dict(modelPassed=calls == expected and result == (outcome if chosen is not None else 0) and actual == bytes(page),
        result=result, calls=calls, expectedCalls=expected, nodes=nodes, sizes=sizes, flags=flags,
        requestedBytes=size, alignment=alignment, backingSha256=hashlib.sha256(actual).hexdigest(),
        observedOwnPcs=sorted(pcs), actualReturns=1, suppliedCommitCalls=len(calls))
