import itertools
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

BACKEND = 0x020e5500
INITIALIZED = 0x020e5480
IDENTITY = 0x020e33e4
DESCRIPTOR = 0x02520000
CALLBACK = 0x02600000
STOP = 0x027ff800
PLATFORM = {0x02000b64: 'validate', 0x02008430: 'failure', 0x02007ff4: 'irq-disable', 0x02008008: 'irq-restore', 0x020068d4: 'queue-wait', 0x02006924: 'queue-wake', 0x0200698c: 'thread-wake', 0x02010334: 'descriptor-select', 0x02011294: 'command', CALLBACK: 'callback'}

class Provider:
    def __init__(self, load, store, settings):
        self.load = load
        self.store = store
        self.settings = settings
        self.trace = []
        self.interrupts = 0
        self.waits = 0

    def word(self, address):
        return struct.unpack('<I', self.load(address, 4))[0]

    def put(self, address, value):
        self.store(address, struct.pack('<I', value & 0xffffffff))

    def invoke(self, role, values):
        arity = {'validate': 1, 'failure': 0, 'irq-disable': 0, 'irq-restore': 1, 'queue-wait': 1, 'queue-wake': 1, 'thread-wake': 1, 'descriptor-select': 1, 'command': 3, 'callback': 1}[role]
        self.trace.append((role, *values[:arity]))
        result = 0
        if role == 'irq-disable':
            self.interrupts += 1
            result = 0x10000000 + self.interrupts
            if self.interrupts == 2 and self.settings['mutate']:
                self.put(BACKEND + 0x38, 0)
                self.put(BACKEND + 0x3c, 0xdecafbad)
        elif role == 'queue-wait':
            self.waits += 1
            if self.waits == self.settings['waits']:
                self.put(BACKEND + 0x114, self.word(BACKEND + 0x114) & ~4)
        elif role == 'descriptor-select':
            self.put(BACKEND, DESCRIPTOR)
            self.put(DESCRIPTOR, 0x12345678)
        elif role == 'command':
            if values[1] == 6:
                self.put(DESCRIPTOR, self.settings['status'])
                if self.settings['inject']:
                    self.put(BACKEND + 0x38, CALLBACK)
                    self.put(BACKEND + 0x3c, 0x11223344)
            result = int(values[1] == 6 and not self.settings['status'])
        elif role == 'queue-wake':
            flags = self.word(BACKEND + 0x114)
            if self.settings['wake'] == 1:
                flags |= 0x10
            elif self.settings['wake'] == 2:
                flags &= ~0x10
            self.put(BACKEND + 0x114, flags)
        return result

def model(memory, name, arguments, settings):
    provider = Provider(lambda at, size: read(memory, at, size), lambda at, data: write(memory, at, data), settings)
    result = None
    if name == 'save_backend_initialized_get':
        result = u32(memory, INITIALIZED)
    elif name == 'save_backend_initialized_set':
        put(memory, INITIALIZED, arguments[0])
    elif name == 'save_backend_initialized_check':
        if not u32(memory, INITIALIZED):
            provider.invoke('failure', ())
    elif name == 'save_backend_complete':
        result = int(not (u32(memory, BACKEND + 0x114) & 4))
    elif name == 'save_backend_fifo_callback':
        if arguments[0] == 11 and arguments[2]:
            identity = u32(memory, BACKEND + 0x104)
            put(memory, BACKEND + 0x114, u32(memory, BACKEND + 0x114) & ~0x20)
            provider.invoke('thread-wake', (identity,))
    else:
        configure = name == 'save_backend_configure'
        if configure:
            provider.invoke('validate', (0x02000b8c,))
            if not arguments[0]:
                provider.invoke('failure', ())
            if not u32(memory, INITIALIZED):
                provider.invoke('failure', ())
        token = provider.invoke('irq-disable', ())
        while u32(memory, BACKEND + 0x114) & 4:
            provider.invoke('queue-wait', (BACKEND + 0x10c,))
        if configure:
            put(memory, BACKEND + 0x114, u32(memory, BACKEND + 0x114) | 4)
            put(memory, BACKEND + 0x38, 0)
            put(memory, BACKEND + 0x3c, 0)
        provider.invoke('irq-restore', (token,))
        if configure:
            provider.invoke('descriptor-select', (arguments[0],))
            put(memory, BACKEND + 0x104, u32(memory, IDENTITY + 4))
            provider.invoke('command', (BACKEND, 2, 1))
            put(memory, DESCRIPTOR + 0xc, 0)
            put(memory, DESCRIPTOR + 0x10, BACKEND + 0x120)
            put(memory, DESCRIPTOR + 0x14, 1)
            provider.invoke('command', (BACKEND, 6, 1))
            callback, argument = u32(memory, BACKEND + 0x38), u32(memory, BACKEND + 0x3c)
            token = provider.invoke('irq-disable', ())
            put(memory, BACKEND + 0x114, u32(memory, BACKEND + 0x114) & ~0x4c)
            provider.invoke('queue-wake', (BACKEND + 0x10c,))
            if u32(memory, BACKEND + 0x114) & 0x10:
                provider.invoke('thread-wake', (BACKEND + 0x44,))
            provider.invoke('irq-restore', (token,))
            if callback:
                provider.invoke('callback', (argument,))
        result = int(u32(memory, DESCRIPTOR) == 0)
    return result, provider.trace

def validate(arm, save, matches, root):
    machines = []
    active = {}

    def hook(machine, address, size, user):
        values = [machine.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2)]
        result = active['provider'].invoke(PLATFORM[address], values)
        machine.reg_write(UC_ARM_REG_R0, result)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            for record, code in matches.values():
                machine.mem_write(int(record['address'], 16), code)
        for address in PLATFORM:
            machine.hook_add(UC_HOOK_CODE, hook, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(20261027)
    cases = 0
    calls = 0
    grid = itertools.product([0, 2, 4, 0x14, 0xffffffff], [0, 1, 0x80, 0xffffffff], [0, 3, 4], [1, 3], [False, True], [0, 1, 2])
    for number, (flags, value, status, waits, inject, wake) in enumerate(grid):
        names = list(matches) if number % 4 == 0 else ['save_backend_configure']
        for name in names:
            original = {0x020e3300: bytearray(rng.randbytes(0x1000)), 0x020e5400: bytearray(rng.randbytes(0x1000)), DESCRIPTOR: bytearray(rng.randbytes(0x1000))}
            put(original, BACKEND, DESCRIPTOR)
            put(original, BACKEND + 0x114, flags)
            put(original, INITIALIZED, value)
            put(original, DESCRIPTOR, status)
            put(original, IDENTITY + 4, 0x23456780)
            arguments = [value, 0xfedcba98, int(inject)]
            if name == 'save_backend_fifo_callback':
                arguments[0] = [0, 10, 11, 12, 0xffffffff][number % 5]
            settings = {'status': status, 'waits': waits, 'inject': inject, 'wake': wake, 'mutate': bool(number & 1)}
            expected = {address: bytearray(data) for address, data in original.items()}
            result, trace = model(expected, name, arguments, settings)
            record, code = matches[name]
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                provider = Provider(machine.mem_read, machine.mem_write, settings)
                active['provider'] = provider
                for register, argument in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), arguments):
                    machine.reg_write(register, argument)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(record['address'], 16), STOP, count=100000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('Configuration bounds', name, settings))
                if (result is not None and machine.reg_read(UC_ARM_REG_R0) != result) or provider.trace != trace:
                    raise AssertionError(('Configuration return/callback trace differs', name, settings, provider.trace, trace))
                for address, data in expected.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('Configuration backend/descriptor/guard RAM differs', name, settings))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRamAndCallbackTrace': True, 'platformStubs': {hex(address): role for address, role in PLATFORM.items()}, 'observations': ['Configuration serializes through busy bit4, zeros callback metadata, selects the descriptor, sends operation2 then a one-byte operation6 request, and returns final descriptor status0.', 'Command return values are ignored by configuration; the final descriptor status determines success.', 'Cleanup captures callback metadata before interrupt disable and reloads flags after queue waking.', 'The FIFO callback acts only on channel11 with a nonzero third argument, clears flags0x20 and wakes the stored identity.', 'Initialization word, completion predicate and blocking completion helpers preserve unrelated RAM.'], 'limitations': ['Descriptor selection, command transport, interrupts, queue/thread wakes and callbacks are isolated controlled providers.', 'The failure provider returns to permit bounded observation after zero type/uninitialized checks; actual fatal behavior is not exercised.', 'No physical device configuration, asynchronous hardware completion or ARM7 execution is claimed.']}
