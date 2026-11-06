import hashlib
import math
import random
import struct
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from link_runtime_unit import measured_module
from project import ROOT, write_json, sha256, configuration
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
from main_irq_guarded_getters_fixture_v2_20261101 import REGS

STACK, STOP = 0x027F0000, 0x027FF000


def words(value):
    return list(struct.unpack('<II', struct.pack('<d', value)))


def execute(image, entry, arguments, index):
    rng = random.Random(entry * 10000 + index)
    registers = [rng.getrandbits(32) for unused in REGS]
    registers[:len(arguments)] = arguments
    guards = rng.randbytes(8192)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_write(0x02000000, image)
    machine.mem_write(STACK - 4096, guards)
    machine.reg_write(UC_ARM_REG_CPSR, (index % 16 << 28) | 0x1F)
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    observed, writes, target_words = set(), [], []

    def code(uc, address, size, unused):
        assert 0x02000000 <= address < 0x02000000 + len(image), hex(address)
        observed.update(range(address, address + size))
        if address == 0x020212F8:
            target_words.append([uc.reg_read(register) for register in REGS[:4]])

    def write(uc, access, address, size, value, unused):
        assert STACK - 4096 <= address and address + size <= STACK
        writes.append([address, size, value])

    machine.hook_add(UC_HOOK_CODE, code)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(entry, STOP, timeout=1000000, count=100000)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP
    assert machine.reg_read(UC_ARM_REG_SP) == STACK
    assert [machine.reg_read(register) for register in REGS[4:12]] == registers[4:12]
    assert bytes(machine.mem_read(STACK - 4096, 256)) == guards[:256]
    assert bytes(machine.mem_read(STACK + 4096 - 256, 256)) == guards[-256:]
    result = dict(index=index, entry=hex(entry), arguments=arguments,
        resultWords=[machine.reg_read(register) for register in REGS[:2]],
        actualReturn=True, nativeTargetWords=target_words, stackWrites=writes,
        stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK - 4096, 8192))).hexdigest(),
        observedAddresses=sorted(observed), suppliedCalls=0)
    del machine
    return result


def main():
    metadata, image, unused = measured_module('main')
    cases = []
    rng = random.Random(2444394)
    integers = [0, 1, -1, 0x7FFFFFFF, -0x80000000] + [rng.randrange(-0x80000000, 0x80000000) for unused in range(123)]
    for index, value in enumerate(integers):
        row = execute(image, 0x020244C4, [value & 0xFFFFFFFF], index)
        row['expectedWords'] = words(float(value))
        assert row['resultWords'] == row['expectedWords'], row
        cases.append(row)
    floats = [0.0, -0.0, 1.9, -1.9, 0.1, -0.1, 2147483647.0, -2147483648.0,
        math.ldexp(1.0, -1074), -math.ldexp(1.0, -1074)] + [rng.uniform(-1e9, 1e9) for unused in range(118)]
    for index, value in enumerate(floats):
        row = execute(image, 0x02024394, words(value), index)
        row['expectedR0'] = math.trunc(value) & 0xFFFFFFFF
        assert row['resultWords'][0] == row['expectedR0'], row
        cases.append(row)
    for index, (power, exponent) in enumerate((p, e) for p in [-5, -1, 0, 1, 5] for e in [-5, -1, 0, 1, 5]):
        arguments = words(math.ldexp(1.0, power)) + words(float(exponent))
        row = execute(image, 0x0202298C, arguments, index)
        row['expectedWords'] = words(math.ldexp(1.0, power * exponent))
        assert row['resultWords'] == row['expectedWords'] and row['nativeTargetWords'] == [arguments], row
        cases.append(row)
    for exponent in range(10):
        arguments = words(10.0) + words(float(exponent))
        row = execute(image, 0x0202298C, arguments, exponent + 25)
        row['expectedWords'] = words(float(10 ** exponent))
        assert row['resultWords'] == row['expectedWords'] and row['nativeTargetWords'] == [arguments], row
        cases.append(row)
        converted = execute(image, 0x02024394, row['resultWords'], exponent + 128)
        converted['expectedR0'] = 10 ** exponent
        assert converted['resultWords'][0] == converted['expectedR0'], converted
        cases.append(converted)
    report = dict(generator=Path(__file__).name, generatorSha256=sha256(__file__),
        module='main', processor='arm9', mode='arm', moduleSha256=metadata['sha256'],
        romSha256=configuration()['romSha256'],
        passed=True, actualNativeReturns=len(cases), sourceCredit=0, suppliedCalls=0, cases=cases,
        measuredContracts=[dict(address='0x020244c4', domain='All sampled signed32 words', interpretation='R0 signed32 to binary64 words in R0 low/R1 high'),
            dict(address='0x02024394', domain='Sampled finite binary64 inside signed32 conversion range', interpretation='R0 low/R1 high to truncated signed32 in R0; R1 scratch'),
            dict(address='0x0202298c', target='0x020212f8', domain='Positive power-of-two bases and five signed integral exponents; base10 exponent0..9 and subsequent conversion', interpretation='Four words forwarded unchanged; binary64 result agrees with exact power on these samples')],
        limitations=['Finite native probes establish no full math-library semantics, function boundaries or source qualification',
            'No selected C caller has been compiled or linked by this probe',
            'NaNs, infinities, overflow, out-of-range conversions and general power rounding remain unproved'])
    path = ROOT / 'evidence/abi/main-float-word-contracts-20261101.json'
    write_json(path, report)
    print(dict(passed=True, actualNativeReturns=len(cases), sourceCredit=0, report=path.relative_to(ROOT).as_posix(), sha256=sha256(path)))


if __name__ == '__main__':
    main()
