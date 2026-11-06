import hashlib
import random
import struct
import time

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_LR, UC_ARM_REG_SP

MAIN = 0x02530000
ARENA = 0x02540000
OUTPUT = ARENA + 0x80
WORD = 0x02510000
TAIL = WORD + 0x10
RECORDS = 0x02520000
EVENTS = 0x021c0e20
STOP = 0x027ff800
FLAG_INDICES = [0xac, 0xad, 0xae, 0xaf, 0xb2, 0xb1, 0x22f]

def validate(arm, save, matches, root):
    name = 'save_header_summary'
    if name not in matches:
        return {'cases': 0, 'nativeAndRecompiledCalls': 0, 'limitations': ['No source match was accepted.']}
    record, code = matches[name]
    machines = []
    context = {}
    counts = {'summaryCases': 0}
    boundaries = {0x020633bc: 'word-pointer', 0x02062aa0: 'byte-query', 0x02062a50: 'slot-pointer', 0x020630b0: 'record-byte-query', 0x02063e80: 'tail-pointer'}

    def boundary(machine, address, size, user):
        role = boundaries[address]
        argument = machine.reg_read(UC_ARM_REG_R0)
        context['trace'].append((role, argument))
        if role == 'word-pointer':
            result = WORD
        elif role == 'byte-query':
            result = context['byte']
        elif role == 'tail-pointer':
            result = TAIL
        elif role == 'slot-pointer':
            if argument >= 3:
                raise AssertionError(('Unexpected slot', argument))
            result = RECORDS + argument * 0x100 if context['mask'] & (1 << argument) else 0
        else:
            result = context['queries'][argument]
        machine.reg_write(UC_ARM_REG_R0, result)
        machine.reg_write(UC_ARM_REG_PC, machine.reg_read(UC_ARM_REG_LR))

    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(0x02000000, arm)
        if rebuilt:
            machine.mem_write(int(record['address'], 16), code)
        for address in boundaries:
            machine.hook_add(UC_HOOK_CODE, boundary, begin=address, end=address)
        machines.append(machine)
    rng = random.Random(20261027)
    event_vectors = [('zero', bytes(192)), ('ff', bytes([255]) * 192), ('real-bank-0', save[0x3994:0x3a54]), ('real-bank-1', save[0xaa94:0xab54])]
    for bits in range(128):
        values = bytearray(rng.randbytes(192))
        for bit, index in enumerate(FLAG_INDICES):
            mask = 1 << (index & 7)
            values[index >> 3] = (values[index >> 3] & ~mask) | (mask if bits & (1 << bit) else 0)
        event_vectors.append((f'flags-{bits}', bytes(values)))
    cases = 0
    calls = 0
    for label, events in event_vectors:
        for live_mask in range(8):
            for match_query in (False, True):
                main = rng.randbytes(0x100)
                arena = rng.randbytes(0x200)
                records = bytearray(rng.randbytes(0x300))
                queries = {index: 0x100 + index for index in range(256)}
                for slot in range(3):
                    identifier = 17 + slot
                    records[slot * 0x100 + 0x1c] = identifier
                    queries[identifier] = records[slot * 0x100 + 0x30] if match_query else 0x100 + identifier
                word = rng.getrandbits(32)
                byte_value = rng.getrandbits(32)
                tail = rng.randrange(256)
                expected = bytearray(arena)
                base = OUTPUT - ARENA
                expected[base + 4:base + 0x18] = main[8:0x1c]
                struct.pack_into('<I', expected, base, word)
                expected[base + 0x5d] = byte_value & 255
                expected[base + 0x5e] = tail
                flags = sum(((events[index >> 3] >> (index & 7)) & 1) << bit for bit, index in enumerate(FLAG_INDICES))
                expected[base + 0x5f] = flags
                for slot in range(3):
                    source = slot * 0x100
                    if live_mask & (1 << slot):
                        expected[base + 0x18 + slot * 0x14:base + 0x2c + slot * 0x14] = records[source:source + 0x14]
                        value = records[source + 0x30]
                        expected[base + 0x5a + slot] = value | (0x80 if match_query else 0)
                        expected[base + 0x54 + slot * 2:base + 0x56 + slot * 2] = records[source + 0x18:source + 0x1a]
                    else:
                        expected[base + 0x18 + slot * 0x14:base + 0x1a + slot * 0x14] = b'\xe3\x1b'
                        expected[base + 0x5a + slot] = 0
                        expected[base + 0x54 + slot * 2:base + 0x56 + slot * 2] = bytes(2)
                for machine in machines:
                    context.update({'mask': live_mask, 'queries': queries, 'byte': byte_value, 'trace': []})
                    machine.mem_write(MAIN, main)
                    machine.mem_write(ARENA, arena)
                    machine.mem_write(WORD, struct.pack('<I', word))
                    machine.mem_write(TAIL, bytes([tail]))
                    machine.mem_write(RECORDS, bytes(records))
                    machine.mem_write(EVENTS, events)
                    machine.reg_write(UC_ARM_REG_R0, OUTPUT)
                    machine.reg_write(UC_ARM_REG_R1, MAIN)
                    machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
                    machine.reg_write(UC_ARM_REG_LR, STOP)
                    began = time.monotonic()
                    machine.emu_start(int(record['address'], 16), STOP, count=100000)
                    if machine.reg_read(UC_ARM_REG_PC) != STOP or time.monotonic() - began > 1:
                        raise AssertionError('Header summary exceeded execution bounds')
                    if bytes(machine.mem_read(ARENA, 0x200)) != expected:
                        raise AssertionError(('Summary bytes differ', label, live_mask, match_query))
                    for address, value in [(MAIN, main), (RECORDS, records), (EVENTS, events)]:
                        if bytes(machine.mem_read(address, len(value))) != value:
                            raise AssertionError('Header summary modified an input')
                    slots = [argument for role, argument in context['trace'] if role == 'slot-pointer']
                    if slots != [0, 1, 2]:
                        raise AssertionError(('Slot request sequence', slots))
                    queries_seen = [argument for role, argument in context['trace'] if role == 'record-byte-query']
                    if queries_seen != [17 + slot for slot in range(3) if live_mask & (1 << slot)]:
                        raise AssertionError(('Record query sequence', queries_seen))
                    calls += 1
                cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'counts': {'allSevenFlagCombinations': 128, 'slotPresencePatterns': 8, 'queryMatchStates': 2}, 'instructionLimitPerCall': 100000, 'elapsedSecondsLimit': 1, 'returnPcVerified': True, 'independentExpectedSummaryBytes': True, 'guardBytesCompared': 0x200, 'inputFramesUnchanged': True, 'eventVectors': [{'name': name, 'sha256': hashlib.sha256(data).hexdigest()} for name, data in event_vectors], 'boundaryStubs': {hex(address): role for address, role in boundaries.items()}, 'limitations': ['Native pointer/value providers and record-byte queries are controlled boundary stubs; their own selection logic and gameplay meanings remain unknown.', 'The native event reader executes against explicit event bytes; seven raw event indices are not assigned story or quest meanings.', 'Null-slot summaries preserve the unassigned bytes observed in the native writer rather than inventing a fully cleared record.', 'The emitted header summary is separate from persistent live monster identity or complete progression understanding.']}
