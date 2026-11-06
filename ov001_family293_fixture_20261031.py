import hashlib
import random
from ov001_ability28_fixture_20261031 import REGS
from ov001_family293_models_20261031 import SPECS, NATIVE, DIVIDE, construct
from ov001_reroll59_fixture_20261031 import inventory
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *
STOP, SP = (134217728, 50462464)

def execute(main, overlay, address, recipe, candidate=None):
    ENTRY=address
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for a, n in [(33554432, 4194304), (50331648, 131072), (STOP, 4096)]:
        machine.mem_map(a, n)
    machine.mem_write(33554432, main)
    machine.mem_write(35484224, overlay)
    if candidate is not None:
        if len(candidate) != SPECS[ENTRY]['bytes']:
            raise ValueError('Family293 preserve40 caller bytes')
        machine.mem_write(ENTRY, candidate)
    rng = random.Random(recipe['seed'])
    machine.mem_write(50331648, rng.randbytes(131072))
    initial, expected, services, native, result = construct(ENTRY,recipe)
    starts, ranges = inventory()
    native_addresses = set(NATIVE) | {DIVIDE}
    for a, b in initial:
        machine.mem_write(a, b)
    expected_ram = bytearray(machine.mem_read(33554432, 4194304))
    for a, b in expected:
        expected_ram[a - 33554432:a - 33554432 + len(b)] = b
    values = [rng.getrandbits(32) for r in REGS]
    values[0] = recipe['seed'] & 0xFFFFFFFF
    for r, v in zip(REGS, values):
        machine.reg_write(r, v)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 16)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    calls, entries, frames, returned, trace, writes, observed = ([], [], [], [], [], [], set())

    def before(engine, event):
        if any((bytes(engine.mem_read(a, len(b))) != b for a, b in event['before'])):
            raise ValueError('Family293 independent ordered state differs')

    def step(engine, pc, width, data):
        while frames and pc == frames[-1]['returnAddress']:
            frame = frames.pop()
            if engine.reg_read(UC_ARM_REG_SP) != frame['sp'] or [engine.reg_read(r) for r in REGS[4:12]] != frame['preserved'] or engine.reg_read(REGS[0]) != frame['expectedResult']:
                raise ValueError(('Family293 actual native return/frame differs', hex(frame['address']), hex(engine.reg_read(REGS[0])), hex(frame['expectedResult']), engine.reg_read(UC_ARM_REG_SP), frame['sp']))
            if frame['expectedRemainder'] is not None and engine.reg_read(REGS[1]) != frame['expectedRemainder']:
                raise ValueError('Family293 actual quotient/remainder pair differs')
            returned.append(dict(address=hex(frame['address']), result=engine.reg_read(REGS[0]), remainder=engine.reg_read(REGS[1]) if frame['expectedRemainder'] is not None else None))
        if pc == STOP:
            engine.emu_stop()
            return
        trace.append(pc)
        if len(trace) > 5000 or engine.reg_read(UC_ARM_REG_CPSR) & 255 != 16:
            raise ValueError('Family293 bounded ARM mode differs')
        if pc in native_addresses:
            i = len(entries)
            if i >= len(native) or native[i]['address'] != pc:
                raise ValueError('Family293 native entry order differs')
            event = native[i]
            before(engine, event)
            arguments = [engine.reg_read(REGS[k]) if k<4 else int.from_bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP)+(k-4)*4,4),'little') for k in range(len(event['arguments']))]
            if arguments != event['arguments']:
                raise ValueError('Family293 native helper arguments differ')
            entries.append(dict(address=hex(pc), arguments=arguments))
            frames.append(dict(address=pc, returnAddress=engine.reg_read(UC_ARM_REG_LR) & ~1, sp=engine.reg_read(UC_ARM_REG_SP), preserved=[engine.reg_read(r) for r in REGS[4:12]], expectedResult=event['result'], expectedRemainder=event.get('remainder')))
        if ENTRY <= pc < ENTRY + SPECS[ENTRY]['instructions']:
            observed.update(range(pc, pc + width))
            return
        index = __import__('bisect').bisect_right(starts, pc) - 1
        if index >= 0 and ranges[index][0] <= pc < ranges[index][1] and (pc not in [service['address'] for service in services]):
            return
        i = len(calls)
        if i >= len(services) or pc != services[i]['address']:
            raise ValueError(('Family293 independent provider order differs', hex(pc), i))
        event = services[i]
        before(engine, event)
        arguments = [engine.reg_read(REGS[k]) if k<4 else int.from_bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP)+(k-4)*4,4),'little') for k in range(len(event['arguments']))]
        if arguments != event['arguments']:
            raise ValueError(('Family293 independent provider arguments differ', arguments, event['arguments']))
        calls.append(dict(address=hex(pc), arguments=arguments, result=event['result'], effects=[dict(address=hex(a), bytesHex=b.hex()) for a, b in event['effects']]))
        for a, b in event['effects']:
            engine.mem_write(a, b)
        engine.reg_write(REGS[0], event['result'])
        for k in [1, 2, 3, 12]:
            engine.reg_write(REGS[k], recipe['seed'] * 2654435769 + i * 13 + k & 4294967295)
        engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))

    def written(engine, access, a, n, value, data):
        if not (50331648 <= a <= SP - n or any((base <= a and a + n <= base + len(b) for base, b in initial))):
            raise ValueError('Family293 unexpected native write region')
        writes.append((a, n, value))
    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ENTRY, STOP + 4, count=5001)
    actual = [machine.reg_read(r) for r in REGS]
    expected_returns = []
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or frames or (actual[0] != result) or (actual[4:12] != values[4:12]) or (len(returned) != len(native)) or (len(calls) != len(services)):
        raise ValueError('Family293 actual caller/native return protocol differs')
    ram = bytes(machine.mem_read(33554432, 4194304))
    if ram != expected_ram:
        raise ValueError('Family293 complete independent RAM differs')
    return dict(actualReturn=True, returnWord=actual[0], restoredSP=True, preservedRegisters=actual[4:12], nativeDependencyActualReturns=returned, providedCalls=calls, instructions=len(trace) - len(calls), observedCallerInstructionBytes=sorted(observed), ramSha256=hashlib.sha256(ram).hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(50331648, 131072))).hexdigest(), pcTrace=trace, writes=writes)
