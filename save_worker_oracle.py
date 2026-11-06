import itertools
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

GLOBAL = 0x020e5500
GLOBAL_FRAME = 0x020e5400
LOCAL_FRAME = 0x02510000
GLOBAL_DESCRIPTOR = 0x02520000
LOCAL_DESCRIPTOR = 0x02521000
SOURCE = 0x02530000
DESTINATION = 0x02540000
CALLBACK = 0x02600000
STOP = 0x027ff800
PLATFORM = {0x02000b64: 'validate', 0x020072d0: 'invalidate', 0x02007308: 'clean', 0x0200732c: 'drain', 0x02011294: 'command', 0x02007ff4: 'irq-disable', 0x02008008: 'irq-restore', 0x02006924: 'queue-wake', 0x0200698c: 'thread-wake', CALLBACK: 'callback'}

def read(memory, address, size):
    for base, data in memory.items():
        if base <= address and address + size <= base + len(data):
            return bytes(data[address - base:address - base + size])
    raise AssertionError(('Reference memory read outside frame', hex(address), size))

def write(memory, address, value):
    for base, data in memory.items():
        if base <= address and address + len(value) <= base + len(data):
            data[address - base:address - base + len(value)] = value
            return
    raise AssertionError(('Reference memory write outside frame', hex(address), len(value)))

def u32(memory, address):
    return struct.unpack('<I', read(memory, address, 4))[0]

def put(memory, address, value):
    write(memory, address, struct.pack('<I', value & 0xffffffff))

def pattern(number, count):
    return bytes((number * 17 + index * 3) & 255 for index in range(count))

def command_effect(memory, backend, context):
    descriptor = u32(memory, backend)
    context['commands'] += 1
    number = context['commands']
    success = number != context['fail']
    put(memory, descriptor, 0 if success else 3)
    if success and context['final'] == 0:
        write(memory, u32(memory, descriptor + 0x10), pattern(number, u32(memory, descriptor + 0x14)))
    if number == context['cancel-after']:
        put(memory, backend + 0x114, u32(memory, backend + 0x114) | 0x40)
    return int(success)

def model(original, backend, settings):
    memory = {base: bytearray(data) for base, data in original.items()}
    context = dict(settings, commands=0)
    descriptor = u32(memory, backend)
    operation = u32(memory, backend + 0x2c)
    mode = u32(memory, backend + 0x30)
    final = u32(memory, backend + 0x34)
    global_descriptor = u32(memory, GLOBAL)
    maximum = u32(memory, global_descriptor + 0x1c) if operation == 11 else u32(memory, global_descriptor + 0x20) if operation == 15 else 256
    scratch = backend + 0x120
    trace = [('validate', 0x02000b8c)]
    while True:
        count = min(maximum, u32(memory, backend + 0x24))
        put(memory, descriptor + 0x14, count)
        if u32(memory, backend + 0x114) & 0x40:
            put(memory, backend + 0x114, u32(memory, backend + 0x114) & ~0x40)
            put(memory, descriptor, 7)
            break
        if final == 0:
            trace.append(('invalidate', scratch, count))
            put(memory, descriptor + 0xc, u32(memory, backend + 0x1c))
            put(memory, descriptor + 0x10, scratch)
        elif final in (1, 2):
            write(memory, scratch, read(memory, u32(memory, backend + 0x1c), count))
            trace.extend([('clean', scratch, count), ('drain',)])
            put(memory, descriptor + 0xc, scratch)
            put(memory, descriptor + 0x10, u32(memory, backend + 0x20))
        elif final == 3:
            put(memory, descriptor + 0xc, u32(memory, backend + 0x1c))
            put(memory, descriptor + 0x10, u32(memory, backend + 0x20))
        trace.append(('command', backend, operation, mode, count, u32(memory, descriptor + 0xc), u32(memory, descriptor + 0x10)))
        if not command_effect(memory, backend, context):
            break
        if final == 2:
            trace.append(('command', backend, 9, 1, count, u32(memory, descriptor + 0xc), u32(memory, descriptor + 0x10)))
            if not command_effect(memory, backend, context):
                break
        elif final == 0:
            write(memory, u32(memory, backend + 0x20), read(memory, scratch, count))
        put(memory, backend + 0x1c, u32(memory, backend + 0x1c) + count)
        put(memory, backend + 0x20, u32(memory, backend + 0x20) + count)
        put(memory, backend + 0x24, u32(memory, backend + 0x24) - count)
        if not u32(memory, backend + 0x24):
            break
    callback, argument = u32(memory, backend + 0x38), u32(memory, backend + 0x3c)
    trace.append(('irq-disable',))
    if settings['mutate-callback']:
        put(memory, backend + 0x38, 0)
        put(memory, backend + 0x3c, argument ^ 0xffffffff)
    put(memory, backend + 0x114, u32(memory, backend + 0x114) & ~0x4c)
    trace.append(('queue-wake', backend + 0x10c))
    if settings['wake-mode'] == 1:
        put(memory, backend + 0x114, u32(memory, backend + 0x114) | 0x10)
    elif settings['wake-mode'] == 2:
        put(memory, backend + 0x114, u32(memory, backend + 0x114) & ~0x10)
    if u32(memory, backend + 0x114) & 0x10:
        trace.append(('thread-wake', backend + 0x44))
    trace.append(('irq-restore', 0x24681357))
    if callback:
        trace.append(('callback', argument))
    return memory, trace

def validate(arm, save, matches, root):
    if 'save_backend_worker' not in matches:
        return {'cases': 0, 'nativeAndRecompiledCalls': 0, 'limitations': ['Worker source did not match.']}
    machines = []
    context = {}
    cases = 0
    calls = 0

    def hook(machine, address, size, user):
        role = PLATFORM[address]
        values = [machine.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        backend = context['backend']
        result = 0
        if role == 'command':
            descriptor = struct.unpack('<I', machine.mem_read(backend, 4))[0]
            count = struct.unpack('<I', machine.mem_read(descriptor + 0x14, 4))[0]
            source, destination = struct.unpack('<II', machine.mem_read(descriptor + 0xc, 8))
            context['trace'].append((role, *values, count, source, destination))
            context['commands'] += 1
            result = int(context['commands'] != context['fail'])
            machine.mem_write(descriptor, struct.pack('<I', 0 if result else 3))
            if result and context['final'] == 0:
                machine.mem_write(destination, pattern(context['commands'], count))
            if context['commands'] == context['cancel-after']:
                flags = struct.unpack('<I', machine.mem_read(backend + 0x114, 4))[0]
                machine.mem_write(backend + 0x114, struct.pack('<I', flags | 0x40))
        elif role in ('invalidate', 'clean'):
            context['trace'].append((role, *values[:2]))
        elif role in ('validate', 'irq-restore', 'queue-wake', 'thread-wake', 'callback'):
            context['trace'].append((role, values[0]))
        else:
            context['trace'].append((role,))
        if role == 'irq-disable':
            result = 0x24681357
            if context['mutate-callback']:
                argument = struct.unpack('<I', machine.mem_read(backend + 0x3c, 4))[0]
                machine.mem_write(backend + 0x38, struct.pack('<II', 0, argument ^ 0xffffffff))
        elif role == 'queue-wake':
            flags = struct.unpack('<I', machine.mem_read(backend + 0x114, 4))[0]
            if context['wake-mode'] == 1:
                flags |= 0x10
            elif context['wake-mode'] == 2:
                flags &= ~0x10
            machine.mem_write(backend + 0x114, struct.pack('<I', flags))
        machine.reg_write(UC_ARM_REG_R0, result)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    record, code = matches['save_backend_worker']
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            machine.mem_write(int(record['address'], 16), code)
        for address in PLATFORM:
            machine.hook_add(UC_HOOK_CODE, hook, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(20261027)
    grid = itertools.product([False, True], [6, 11, 15], [0, 1, 2, 3, 4], [0, 1, 255, 256, 257, 769], [4, 0x14, 0x44, 0x8000000c], [0, 1, 2])
    for number, (alias, operation, final, length, flags, fail) in enumerate(grid):
        backend = GLOBAL if alias else LOCAL_FRAME + 0x100
        descriptor = GLOBAL_DESCRIPTOR if alias else LOCAL_DESCRIPTOR
        memory = {GLOBAL_FRAME: bytearray(rng.randbytes(0x1000)), LOCAL_FRAME: bytearray(rng.randbytes(0x1000)), GLOBAL_DESCRIPTOR: bytearray(rng.randbytes(0x1000)), LOCAL_DESCRIPTOR: bytearray(rng.randbytes(0x1000)), SOURCE: bytearray(rng.randbytes(0x2000)), DESTINATION: bytearray(rng.randbytes(0x2000))}
        put(memory, GLOBAL, GLOBAL_DESCRIPTOR)
        put(memory, GLOBAL_DESCRIPTOR + 0x1c, 0x80)
        put(memory, GLOBAL_DESCRIPTOR + 0x20, 0x180)
        put(memory, backend, descriptor)
        first = SOURCE + 0x80 if final != 0 else 0x12000
        second = DESTINATION + 0x80 if final not in (1, 2) else 0x22000
        for offset, value in [(0x1c, first), (0x20, second), (0x24, length), (0x2c, operation), (0x30, 0xaabbccdd), (0x34, final), (0x38, CALLBACK if number & 1 else 0), (0x3c, 0x11223344), (0x114, flags)]:
            put(memory, backend + offset, value)
        put(memory, descriptor + 0xc, SOURCE + 0x10)
        put(memory, descriptor + 0x10, DESTINATION + 0x10)
        settings = {'backend': backend, 'final': final, 'fail': fail, 'cancel-after': 1 if number % 4 == 0 else 0, 'mutate-callback': bool(number % 3), 'wake-mode': number % 3}
        expected_memory, expected_trace = model(memory, backend, settings)
        for machine in machines:
            context.clear()
            context.update(settings)
            context.update({'commands': 0, 'trace': []})
            for address, data in memory.items():
                machine.mem_write(address, bytes(data))
            machine.reg_write(UC_ARM_REG_R0, backend)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(record['address'], 16), STOP, count=1000000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Worker execution bounds', settings))
            for address, expected in expected_memory.items():
                actual = bytes(machine.mem_read(address, len(expected)))
                if actual != expected:
                    differences = [(hex(address + i), a, b) for i, (a, b) in enumerate(zip(actual, expected)) if a != b]
                    raise AssertionError(('Worker RAM differs', operation, final, length, settings, differences[:8]))
            if context['trace'] != expected_trace:
                raise AssertionError(('Worker command/cache/callback sequence differs', operation, final, length, settings, context['trace'], expected_trace))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': ['save_backend_worker'], 'instructionLimitPerCall': 1000000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedChunkAndCleanupEffects': True, 'platformStubs': {hex(address): role for address, role in PLATFORM.items()}, 'observations': ['The workerchunks requests, prepares descriptor source/destination/count fields, handles cancellation bit0x40 and optionally issues an additional operation9 verification request.', 'Maximum chunk is256 normally, a global descriptor word at0x1C for operation11, or its word0x20 for operation15.', 'Processed pointers/remaining count advance only after successful commands; failure preserves the current unadvanced chunk.', 'Cleanup clears flags0x4C, wakes the queue, optionally wakes thread state after rereading flags, restores interrupt state and invokes the previously captured callback/argument.'], 'limitations': ['Cache operations, low-level command transport, interrupts, queue/thread waking and callbacks are controlled providers.', 'Raw operation/final/mode values and descriptor words are retained without inferring hardware models or gameplay meanings.', 'Scratch storage begins at backend offset0x120; its full allocated capacity and all legal descriptor-derived chunk bounds remain unestablished.', 'No real ARM7 FIFO exchange, physical memory card transfer or audible emulator is executed.']}
