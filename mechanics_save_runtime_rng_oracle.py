import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

STATE = 0x020f6044
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def validate(arm, save, matches, root):
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for row, code in matches.values():
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rng = random.Random(20261027)
    seeds = [0, 1, 0xffffffff, 0x80000000, 0x7fffffff, 0x12345678] + [rng.getrandbits(32) for _ in range(256)]
    limits = [-0x80000000, -65536, -1, 0, 1, 2, 3, 10, 255, 256, 65535, 65536, 65537, 0x7fffffff]
    cases = calls = 0
    for seed in seeds:
        memory = bytearray(rng.randbytes(0x1000))
        struct.pack_into('<I', memory, STATE - 0x020f6000, seed)
        for machine in machines:
            machine.mem_write(0x020f6000, bytes(memory))
        sequence = limits + [rng.randint(-0x80000000, 0x7fffffff) for _ in range(32)]
        for limit in sequence:
            seed = (seed * 0x41c64e6d + 12345) & 0xffffffff
            expected = (seed >> 16) % limit if limit > 0 else 0
            struct.pack_into('<I', memory, STATE - 0x020f6000, seed)
            row, code = next(iter(matches.values()))
            for machine in machines:
                machine.reg_write(UC_ARM_REG_R0, limit & 0xffffffff)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(row['address'], 16), STOP, count=100000)
                if time.monotonic() - began > 1 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000:
                    raise AssertionError(('Native random bounds/stack', seed, limit))
                if machine.reg_read(UC_ARM_REG_R0) != expected or bytes(machine.mem_read(0x020f6000, len(memory))) != memory:
                    raise AssertionError(('Native random result/state/guard', seed, limit))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 1, 'returnPcAndStackVerified': True, 'independentExpectedLcgModuloAndSequentialState': True, 'platformStubs': {}, 'retainedNativeDependency': {'module': 'main', 'mode': 'ARM', 'address': '0x02026350', 'bytes': 484, 'sha256': sha(arm[0x26350:0x26534]), 'role': 'Unsigned division returns quotientR0/remainderR1; actual native runtime body executes'}, 'observations': ['Each call advances the raw32-bit state by state*0x41C64E6D+12345 with32-bit wrap.', 'For a positive signed limit, the result is unsigned(state>>16) modulo limit; a zero/negative limit returns0 after still advancing state.', '262 distinct seeds each execute46 sequential calls, covering wrap, signed limits and bounded random arguments without reseeding between calls.'], 'limitations': ['The484-byte unsigned-division runtime helper remains native ARM and receives no recovered-C credit.', 'Initial seed ownership, timing, randomness quality and gameplay probability meanings remain unknown.', 'No SDK service, clock or platform provider is substituted and no save semantics are promoted.']}
