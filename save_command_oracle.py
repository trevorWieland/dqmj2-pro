import itertools
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

BACKEND = 0x02510080
DESCRIPTOR = 0x02520080
STOP = 0x027ff800
PLATFORM = {0x0200a41c: 'ready', 0x0200a440: 'send', 0x02008064: 'pause', 0x02007308: 'clean', 0x0200732c: 'drain', 0x020072d0: 'invalidate', 0x02007ff4: 'irq-disable', 0x02008008: 'irq-restore', 0x020068d4: 'queue-wait'}

class Provider:
    def __init__(self, load, store, settings):
        self.load = load
        self.store = store
        self.settings = settings
        self.trace = []
        self.ready = 0
        self.sent = 0
        self.completed = 0
        self.waits = 0

    def word(self, address):
        return struct.unpack('<I', self.load(address, 4))[0]

    def put(self, address, value):
        self.store(address, struct.pack('<I', value & 0xffffffff))

    def complete(self):
        statuses = self.settings['statuses']
        self.put(DESCRIPTOR, statuses[min(self.completed, len(statuses) - 1)])
        self.completed += 1
        self.put(BACKEND + 0x114, self.word(BACKEND + 0x114) & ~0x20)

    def invoke(self, role, values):
        count = {'ready': 2, 'send': 3, 'pause': 1, 'clean': 2, 'drain': 0, 'invalidate': 2, 'irq-disable': 0, 'irq-restore': 1, 'queue-wait': 1}[role]
        self.trace.append((role, *values[:count]))
        result = 0
        if role == 'ready':
            result = int(self.ready >= self.settings['ready-failures'])
            self.ready += 1
        elif role == 'send':
            self.sent += 1
            result = 0xffffffff if self.sent % (self.settings['send-failures'] + 1) else 0
        elif role == 'irq-disable':
            self.waits = 0
            result = 0x12345678
            if not self.settings['wait-count']:
                self.complete()
        elif role == 'queue-wait':
            self.waits += 1
            if self.waits == self.settings['wait-count']:
                self.complete()
        return result

def model(provider, operation, attempts):
    if not provider.word(BACKEND + 0x114) & 2:
        provider.put(BACKEND + 0x114, provider.word(BACKEND + 0x114) | 2)
        if not provider.invoke('ready', (11, 1)):
            while True:
                provider.invoke('pause', (100,))
                if provider.invoke('ready', (11, 1)):
                    break
        model(provider, 0, 1)
    provider.invoke('clean', (provider.word(BACKEND), 0x60))
    provider.invoke('drain', ())
    while True:
        provider.put(BACKEND + 4, operation)
        provider.put(BACKEND + 0x114, provider.word(BACKEND + 0x114) | 0x20)
        while provider.invoke('send', (11, operation, 1)) & 0x80000000:
            pass
        if not operation:
            descriptor = provider.word(BACKEND)
            while provider.invoke('send', (11, descriptor, 1)) & 0x80000000:
                pass
        token = provider.invoke('irq-disable', ())
        while provider.word(BACKEND + 0x114) & 0x20:
            provider.invoke('queue-wait', (0,))
        provider.invoke('irq-restore', (token,))
        provider.invoke('invalidate', (provider.word(BACKEND), 0x60))
        status = provider.word(DESCRIPTOR)
        if status != 4:
            break
        attempts -= 1
        if attempts <= 0:
            break
    return int(status == 0)

def validate(arm, save, matches, root):
    if 'save_backend_command' not in matches:
        return {'cases': 0, 'nativeAndRecompiledCalls': 0, 'limitations': ['Command source did not match.']}
    record, code = matches['save_backend_command']
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
            machine.mem_write(int(record['address'], 16), code)
        for address in PLATFORM:
            machine.hook_add(UC_HOOK_CODE, hook, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(20261027)
    cases = 0
    calls = 0
    grid = itertools.product([0, 2, 0x80000016], [0, 6, 8, 9, 11], [-1, 0, 1, 2, 3], [0, 2], [0, 2], [0, 2], [(0,), (3,), (4, 0), (4, 4, 0), (4, 3)])
    for flags, operation, attempts, ready, sent, waits, statuses in grid:
        original = {0x02510000: bytearray(rng.randbytes(0x1000)), 0x02520000: bytearray(rng.randbytes(0x1000))}
        struct.pack_into('<I', original[0x02510000], BACKEND - 0x02510000, DESCRIPTOR)
        struct.pack_into('<I', original[0x02510000], BACKEND + 0x114 - 0x02510000, flags)
        expected = {address: bytearray(data) for address, data in original.items()}

        def load(address, size):
            base = address & ~0xfff
            return bytes(expected[base][address - base:address - base + size])

        def store(address, value):
            base = address & ~0xfff
            expected[base][address - base:address - base + len(value)] = value

        settings = {'ready-failures': ready, 'send-failures': sent, 'wait-count': waits, 'statuses': statuses}
        reference = Provider(load, store, settings)
        result = model(reference, operation, attempts)
        for machine in machines:
            for address, data in original.items():
                machine.mem_write(address, bytes(data))
            provider = Provider(machine.mem_read, machine.mem_write, settings)
            active['provider'] = provider
            machine.reg_write(UC_ARM_REG_R0, BACKEND)
            machine.reg_write(UC_ARM_REG_R1, operation)
            machine.reg_write(UC_ARM_REG_R2, attempts & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(int(record['address'], 16), STOP, count=100000)
            if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                raise AssertionError(('Command bounds', settings))
            if machine.reg_read(UC_ARM_REG_R0) != result or provider.trace != reference.trace:
                raise AssertionError(('Command result/transport sequence differs', flags, operation, attempts, settings, provider.trace, reference.trace))
            for address, data in expected.items():
                if bytes(machine.mem_read(address, len(data))) != data:
                    raise AssertionError(('Command descriptor/backend/guard RAM differs', settings))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': ['save_backend_command'], 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRamAndTransportTrace': True, 'platformStubs': {hex(address): role for address, role in PLATFORM.items()}, 'observations': ['Initialization sets bit2 before an operation0 recursive handshake and ignores that handshake return.', 'The descriptor is cleaned once per invocation and invalidated after each completed command.', 'FIFO send failures repeat until nonnegative; operation0 additionally sends the captured descriptor pointer.', 'Status4 retries according to the signed attempt counter, including one attempt for initial nonpositive counters; other statuses stop immediately.', 'Interrupt state is restored after completion, and only descriptor status0 returns true.'], 'limitations': ['FIFO readiness/send, cache, interrupts, pauses and queue waiting are controlled providers.', 'Completion providers clear flags0x20 and update descriptor status; actual interrupt/ARM7 transport remains unverified.', 'Infinite hardware stalls are not induced; tested send/ready/wait providers finish within explicit bounds.']}
