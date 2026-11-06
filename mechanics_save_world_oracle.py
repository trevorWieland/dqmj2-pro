import itertools
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from save_worker_oracle import read, write, u32, put

WORLD = 0x021b9eb4
RUNTIME = 0x020f6054
CONTEXT = 0x02102dc0
POSITION = 0x02510080
HEADING = 0x02520080
STOP = 0x027ff800
PLATFORM = {0x021e07b8: ('position', POSITION), 0x021e07d4: ('heading', HEADING)}

def validate(arm, save, matches, root):
    machines = []
    context = {}

    def getter(machine, address, size, user):
        role, result = PLATFORM[address]
        if machine.reg_read(UC_ARM_REG_R0) != 0:
            raise AssertionError('Player getter index differs')
        context['trace'].append((role, 0))
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
            machine.hook_add(UC_HOOK_CODE, getter, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = []
    for counter, value, encounter in itertools.product([0, 0x2a2f, 0x2a30, 0x2a31, 0x80000000, 0xffffffff], [0, 1, 255, 256, 0x80000000, 0xffffffff], [0, 127, 128, 255]):
        vectors.append((counter, value, encounter))
    vectors += [(rng.getrandbits(32), rng.getrandbits(32), rng.getrandbits(8)) for _ in range(256)]
    vectors += [(struct.unpack_from('<I', save, bank + 0x3a6c)[0], 0, save[bank + 0x3a6a]) for bank in (0, 0x7100)]
    calls = 0
    cases = 0
    for number, (counter, value, encounter) in enumerate(vectors):
        original = {0x021b9e00: bytearray(rng.randbytes(0x200)), 0x020f6000: bytearray(rng.randbytes(0x1000)), 0x02102000: bytearray(rng.randbytes(0x1000)), 0x02510000: bytearray(rng.randbytes(0x1000)), 0x02520000: bytearray(rng.randbytes(0x1000))}
        put(original, WORLD + 4, counter)
        write(original, WORLD + 2, bytes([encounter]))
        write(original, RUNTIME + 12, bytes([number & 255]))
        write(original, CONTEXT + 2, bytes([(number * 3) & 255]))
        for offset, coordinate in enumerate([0, 0x7fffffff, 0x80000000] if number % 2 else [0xffffffff, 0, 1]):
            put(original, POSITION + offset * 4, coordinate ^ counter)
        put(original, HEADING + 4, value)
        for name, (record, code) in matches.items():
            expected = {address: bytearray(data) for address, data in original.items()}
            result = None
            trace = []
            if name == 'native_previous_map_get':
                result = read(original, CONTEXT + 2, 1)[0]
            elif name == 'saved_runtime_previous_map_exchange':
                result = read(original, CONTEXT + 2, 1)[0]
                write(expected, CONTEXT + 2, bytes([value & 255]))
            elif name == 'saved_world_time_get':
                result = counter
            elif name == 'saved_world_time_exchange':
                result = counter
                put(expected, WORLD + 4, value)
            elif name == 'saved_world_encounter_get':
                result = encounter
            elif name == 'saved_world_encounter_exchange':
                result = encounter
                write(expected, WORLD + 2, bytes([value & 255]))
            elif name == 'saved_world_time_mode_set':
                put(expected, WORLD + 4, 0x2a30 if value else 0)
            elif name == 'saved_world_time_threshold':
                result = int(counter >= 0x2a30)
            elif name == 'saved_world_capture':
                write(expected, WORLD, read(original, RUNTIME + 12, 1))
                write(expected, WORLD + 1, read(original, CONTEXT + 2, 1))
                write(expected, WORLD + 8, read(original, POSITION, 12))
                write(expected, WORLD + 20, read(original, HEADING + 4, 4))
                trace = [('position', 0), ('heading', 0)]
            else:
                raise AssertionError(('Unmodeled world function', name))
            for machine in machines:
                for address, data in original.items():
                    machine.mem_write(address, bytes(data))
                context['trace'] = []
                machine.reg_write(UC_ARM_REG_R0, value)
                machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                machine.reg_write(UC_ARM_REG_LR, STOP)
                began = time.monotonic()
                machine.emu_start(int(record['address'], 16), STOP, count=100000)
                if time.monotonic() - began > 2 or machine.reg_read(UC_ARM_REG_PC) != STOP:
                    raise AssertionError(('World execution bounds', name))
                if (result is not None and machine.reg_read(UC_ARM_REG_R0) != result) or context['trace'] != trace:
                    raise AssertionError(('World result/provider order differs', name, counter, value, encounter))
                for address, data in expected.items():
                    if bytes(machine.mem_read(address, len(data))) != data:
                        raise AssertionError(('World/position/context/guard RAM differs', name, counter, value, encounter))
                calls += 1
            cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 2, 'returnPcVerified': True, 'independentExpectedRamAndProviderOrder': True, 'platformStubs': {hex(address): 'overlay000 ' + item[0] for address, item in PLATFORM.items()}, 'observations': ['Saved section2 byte2 is an unsigned raw encounter selector; exchange returns the prior byte and truncates writes.', 'Saved section2 word4 exchanges all32 bits and threshold returns one exactly at unsigned value0x2A30 or above.', 'Time-mode setter writes either zero or0x2A30; clock units and human day/night labels remain unestablished.', 'Capture writes map byte0, previous raw map byte1, twelve position bytes at8..20 and heading word20, preserving other bytes in the52-byte section.', 'Runtime previous-map getter/exchange operate on context byte2, separately from the captured serialized byte1.'], 'limitations': ['Capture substitutes the overlay000 index0 player-position and heading getter contracts; their internal overlay state is not reconstructed here.', 'Signed coordinate bit patterns are preserved without geometry, route, heading units or collision claims.', 'Map equality does not establish live runtime/save association, travel feasibility or chronology.', 'No new semantic classification is assigned to untouched section2 bytes, section3 or section4.']}
