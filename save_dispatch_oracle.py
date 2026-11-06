import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

STOP = 0x027ff800
STACK = 0x027ff000
PRESERVED = [UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11]
SIGNATURES = [
    (0x02027420, 1, 0, 8, 10, 1), (0x02027464, 1, 0, 7, 10, 1), (0x020274a8, 1, 0, 8, 10, 1),
    (0x020274ec, 1, 1, 8, 10, 1), (0x02027530, 1, 1, 7, 10, 1), (0x02027574, 1, 1, 8, 10, 1),
    (0x020275b8, 1, 0, 9, 1, 1), (0x020275f8, 1, 0, 9, 1, 1), (0x02027638, 1, 0, 9, 1, 1),
    (0x02027678, 1, 1, 9, 1, 1), (0x020276b8, 1, 1, 9, 1, 1), (0x020276f8, 1, 1, 9, 1, 1),
    (0x02027738, 1, 0, 8, 10, 2), (0x0202777c, 1, 0, 7, 10, 2), (0x020277c0, 1, 0, 8, 10, 2),
    (0x02027804, 1, 1, 8, 10, 2), (0x0202784c, 1, 1, 7, 10, 2), (0x02027894, 1, 1, 8, 10, 2),
    (0x020278dc, 0, 0, 6, 1, 0), (0x02027910, 0, 0, 6, 1, 0), (0x02027944, 0, 0, 6, 1, 0),
    (0x02027978, 0, 1, 6, 1, 0), (0x020279ac, 0, 1, 6, 1, 0), (0x020279e0, 0, 1, 6, 1, 0),
]

def validate(arm, save, matches, root):
    machines = []
    context = {}
    cases = 0
    calls = 0
    touched = set()

    def transfer(machine, address, size, user):
        registers = [machine.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        stack = struct.unpack('<IIIII', machine.mem_read(machine.reg_read(UC_ARM_REG_SP), 20))
        context['calls'].append([*registers, *stack])
        machine.reg_write(UC_ARM_REG_R0, context['return'])
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for record, code in matches.values():
                machine.mem_write(int(record['address'], 16), code)
        machine.hook_add(UC_HOOK_CODE, transfer, begin=0x020108a8, end=0x020108a8)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = [[0] * 5, [0xffffffff] * 5, [1, 2, 3, 4, 5], [0x7100, 0x02500000, 0x70d0, 0x11223344, 0x55667788]]
    vectors.extend([rng.getrandbits(32) for index in range(5)] for _ in range(256))
    for address, swap, asynchronous, operation, mode, last in SIGNATURES:
        name = f'save_transfer_{address:08x}'
        if name not in matches:
            continue
        for number, values in enumerate(vectors):
            expected = [values[1], values[0], values[2]] if swap else values[:3]
            expected += [values[3], values[4], 1] if asynchronous else [0, 0, 0]
            expected += [operation, mode, last]
            return_value = [0, 1, 0x80000000, 0xffffffff][number % 4]
            preserved = [rng.getrandbits(32) for _ in PRESERVED]
            caller_stack = struct.pack('<I', values[4]) + rng.randbytes(60)
            guard = rng.randbytes(0x1000)
            for machine in machines:
                context.update({'calls': [], 'return': return_value})
                machine.mem_write(STACK, caller_stack)
                machine.mem_write(0x02500000, guard)
                for reg, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3), values[:4]):
                    machine.reg_write(reg, value)
                for reg, value in zip(PRESERVED, preserved):
                    machine.reg_write(reg, value)
                machine.reg_write(UC_ARM_REG_SP, STACK)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(address, STOP, count=10000)
                if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK or time.monotonic() - began > 1:
                    raise AssertionError((name, 'Execution bounds or stack balance differs'))
                if context['calls'] != [expected] or machine.reg_read(UC_ARM_REG_R0) != return_value:
                    raise AssertionError((name, 'SDK request or return differs', context['calls'], expected))
                if [machine.reg_read(reg) for reg in PRESERVED] != preserved:
                    raise AssertionError((name, 'Callee-saved registers changed'))
                if bytes(machine.mem_read(STACK, len(caller_stack))) != caller_stack or bytes(machine.mem_read(0x02500000, len(guard))) != guard:
                    raise AssertionError((name, 'Caller arguments or guard bytes changed'))
                calls += 1
            cases += 1
        touched.add(name)
    if touched != set(matches):
        raise AssertionError(('Untested source matches', set(matches) - touched))
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': sorted(touched), 'instructionLimitPerCall': 10000, 'elapsedSecondsLimit': 1, 'returnPcVerified': True, 'stackBalanceAndCalleeSavedRegistersVerified': True, 'independentExpectedNineArgumentPackets': True, 'platformStubs': {'0x020108a8': 'native nine-argument backup transfer entry'}, 'limitations': ['This establishes source reconstruction and ABI request marshalling for the24 wrappers, not physical transfer timing or command side effects.', 'Operation/mode/final constants remain raw native identifiers rather than inferred hardware product labels.', 'Input pointer values are arbitrary scalar ABI probes; the controlled transfer provider does not dereference them or touch a device.']}
