import hashlib
import random
from project import ROOT, configuration, native_dependencies, sha256, write_json
native_dependencies(configuration())
from link_runtime_unit import measured_module
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR
from main_format_wrappers_native_20261030 import REGS

STACK, STOP = 0x027C0000, 0x02FF0000


def execute(main, entry, numerator, denominator, tag, thumb=False, masks=0):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for address, size in [(0x02000000, 0x400000), (STACK, 0x8000), (STOP, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(STACK, bytes([0x5A]) * 0x8000)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | 0x1F | masks)
    for index, reg in enumerate(REGS):
        machine.reg_write(reg, (0x13579BDF * (index + 1) + tag) & 0xFFFFFFFF)
    for reg, value in zip(REGS[:4], [numerator & 0xFFFFFFFF, numerator >> 32, denominator & 0xFFFFFFFF, denominator >> 32]):
        machine.reg_write(reg, value)
    saved = [machine.reg_read(reg) for reg in REGS[4:12]]
    sp = STACK + 0x6000
    machine.reg_write(UC_ARM_REG_SP, sp)
    machine.reg_write(UC_ARM_REG_LR, STOP | int(thumb))
    returned, visited, stores, joins = [], set(), [], []
    initial = [machine.reg_read(r) for r in REGS]
    initial_lr = STOP | int(thumb)

    def code(uc, address, size, user):
        visited.add(address)
        if address == 0x020260F0:
            assert uc.reg_read(UC_ARM_REG_SP) == sp - 28
            assert uc.reg_read(REGS[4]) == int(entry == 0x020260E8)
            import struct
            expected_frame = [initial[i] for i in [4, 5, 6, 7, 11, 12]] + [initial_lr]
            assert list(struct.unpack('<7I', bytes(uc.mem_read(sp - 28, 28)))) == expected_frame
            joins.append(True)
        if address == STOP:
            returned.append(True)
            uc.emu_stop()
        else:
            assert 0x02000000 <= address < 0x02400000

    def store(uc, access, address, size, value, user):
        assert STACK <= address and address + size <= STACK + 0x8000
        stores.append([address, size, value & ((1 << (8 * size)) - 1)])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, store)
    try:
        machine.emu_start(entry, STOP + 4, count=200000, timeout=1000000)
    except Exception as error:
        raise ValueError({'entry': hex(entry), 'numerator': hex(numerator), 'denominator': hex(denominator), 'pc': hex(machine.reg_read(UC_ARM_REG_PC)), 'sp': hex(machine.reg_read(UC_ARM_REG_SP)), 'registers': [hex(machine.reg_read(r)) for r in REGS], 'cause': str(error)}) from error
    assert returned == [True] and joins == [True] and machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_LR) == initial_lr
    assert machine.reg_read(UC_ARM_REG_CPSR) & 0xFF == 0x1F | masks | (0x20 if thumb else 0)
    assert machine.reg_read(UC_ARM_REG_SP) == sp
    assert [machine.reg_read(reg) for reg in REGS[4:12]] == saved
    actual = machine.reg_read(REGS[0]) | machine.reg_read(REGS[1]) << 32
    expected = numerator if denominator == 0 else numerator // denominator if entry == 0x020260DC else numerator % denominator
    assert actual == expected, (hex(entry), numerator, denominator, actual, expected)
    assert bytes(machine.mem_read(0x02000000, len(main))) == main
    return {'actualReturn': True, 'independentJoinFrame': True, 'returnMode': 'thumb' if thumb else 'arm', 'interruptMasks': masks, 'result': actual, 'visited': [hex(x) for x in sorted(visited)],
            'cpsr': machine.reg_read(UC_ARM_REG_CPSR), 'storeCount': len(stores),
            'orderedStoresSha256': hashlib.sha256(repr(stores).encode()).hexdigest()}


def main():
    metadata, binary, config = measured_module('main')
    parent = 'func_020260dc kind:function(arm,size=0x48) addr:0x020260dc'
    alternate = '.L_020260e8 kind:label(arm) addr:0x020260e8'
    assert parent in config.splitlines() and alternate in config.splitlines()
    rng = random.Random(0x260E8)
    values = [0, 1, 2, 7, 8, 10, 16, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF, 0x100000000,
              0x7FFFFFFFFFFFFFFF, 0x8000000000000000, 0xFFFFFFFFFFFFFFFF]
    pairs = [(a, b) for a in values for b in values]
    pairs += [(rng.getrandbits(64), rng.getrandbits(64)) for unused in range(128)]
    rows = []
    for entry in [0x020260DC, 0x020260E8]:
        for numerator, denominator in pairs:
            result = execute(binary, entry, numerator, denominator, len(rows))
            rows.append({'entry': hex(entry), 'numerator': hex(numerator), 'denominator': hex(denominator), 'result': result})
    destination = ROOT / 'evidence/entrypoints/main-unsigned64-initial-model-20261030.json'
    write_json(destination, {'schemaVersion': 1, 'romSha256': configuration()['romSha256'], 'processor': 'arm9', 'module': 'main',
                            'mode': 'arm', 'moduleInputSha256': metadata['sha256'], 'parent': {'address': '0x020260dc', 'bytes': 72,
                            'configuredIdentity': parent, 'spanSha256': hashlib.sha256(binary[0x260DC:0x26124]).hexdigest()},
                            'alternateConfiguredLabel': alternate, 'pairsPerEntry': len(pairs), 'actualNativeReturns': len(rows),
                            'sourceCredit': 0, 'alternateBindingActivated': False, 'rows': rows,
                            'limitations': ['Initial direct native ABI model only; no new typed-binding policy or source acceptance',
                                            'Zero divisor is measured as numerator passthrough, not a language-level division contract']})
    print({'actualNativeReturns': len(rows), 'sourceCredit': 0, 'bindingActivated': False, 'reportSha256': sha256(destination)})


if __name__ == '__main__':
    main()
