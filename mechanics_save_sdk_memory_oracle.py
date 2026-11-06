import hashlib
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parent
sys.path[:0] = [str(ROOT), str(ROOT / 'deps/native')]
from unicorn import Uc, UcError, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_HOOK_MEM_INVALID, UC_MEM_WRITE, UC_MEM_WRITE_UNMAPPED, UC_MEM_WRITE_PROT
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11, UC_ARM_REG_CPSR, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

BASE = 0x02500000
SIZE = 0x8000
STOP = 0x027ff800
SAVED = (UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_R11)
SPECS = {'fill': ('saved_sdk_fill', 0x02008d78, 148), 'copy': ('saved_sdk_copy', 0x02008e0c, 304)}


def sha(data):
    return hashlib.sha256(data).hexdigest()


class BoundaryFault(Exception):
    pass


def expected_memory(initial, kind, args):
    memory = bytearray(initial)
    events = []
    def read(address, width):
        if not BASE <= address <= BASE + SIZE - width:
            raise BoundaryFault(('read', address, width))
        value = int.from_bytes(memory[address - BASE:address - BASE + width], 'little')
        events.append(('read', address, width, value))
        return value
    def write(address, width, value):
        if not BASE <= address <= BASE + SIZE - width:
            raise BoundaryFault(('write', address, width))
        value &= (1 << (8 * width)) - 1
        events.append(('write', address, width, value))
        memory[address - BASE:address - BASE + width] = value.to_bytes(width, 'little')
    try:
        if kind == 'fill':
            destination, value, count = args
            if count:
                if destination & 1:
                    low = read(destination - 1, 2) & 255
                    write(destination - 1, 2, low | (value << 8))
                    destination += 1
                    count -= 1
                if count >= 2:
                    value = (value | (value << 8)) & 0xffffffff
                    if destination & 2:
                        write(destination, 2, value)
                        destination += 2
                        count -= 2
                    if count:
                        value = (value | (value << 16)) & 0xffffffff
                        whole = count & ~3
                        count -= whole
                        for offset in range(0, whole, 4):
                            write(destination, 4, value)
                            destination += 4
                        if count & 2:
                            write(destination, 2, value)
                            destination += 2
                if count & 1:
                    high = read(destination, 2) & 0xff00
                    write(destination, 2, (value & 255) | high)
        else:
            source, destination, count = args
            if count:
                if destination & 1:
                    low = read(destination - 1, 2) & 255
                    first = read(source - 1, 2) >> 8 if source & 1 else read(source, 2)
                    write(destination - 1, 2, low | (first << 8))
                    source += 1
                    destination += 1
                    count -= 1
                if count:
                    parity = source ^ destination
                    if parity & 1:
                        source &= ~1
                        carry = read(source, 2) >> 8
                        source += 2
                        while count >= 2:
                            value = carry | (read(source, 2) << 8)
                            source += 2
                            write(destination, 2, value)
                            destination += 2
                            carry = value >> 16
                            count -= 2
                        if count & 1:
                            high = read(destination, 2) & 0xff00
                            write(destination, 2, high | carry)
                    else:
                        if parity & 2:
                            whole = count & ~1
                            count -= whole
                            width = 2
                        else:
                            if count >= 2 and destination & 2:
                                value = read(source, 2)
                                source += 2
                                write(destination, 2, value)
                                destination += 2
                                count -= 2
                            whole = count & ~3
                            count -= whole
                            width = 4
                        for offset in range(0, whole, width):
                            value = read(source, width)
                            source += width
                            write(destination, width, value)
                            destination += width
                        if count & 2:
                            value = read(source, 2)
                            source += 2
                            write(destination, 2, value)
                            destination += 2
                        if count & 1:
                            high = read(destination, 2) & 0xff00
                            value = read(source, 2) & 255
                            write(destination, 2, high | value)
    except BoundaryFault as fault:
        return bytes(memory), events, fault.args[0]
    return bytes(memory), events, None


def validate(arm, save, matches, root):
    required = {value[0] for value in SPECS.values()}
    if set(matches) != required:
        raise AssertionError('SDK memory oracle requires both complete reassembled source functions')
    candidates = {kind: matches[name] for kind, (name, address, size) in SPECS.items()}
    for row, code in candidates.values():
        for field in ('source', 'object'):
            if sha((root / row[field]).read_bytes()) != row[field + 'Sha256']:
                raise AssertionError('SDK memory source/object identity differs')
        actual = (root / row['isolatedCallerBinary']).read_bytes()
        if sha(actual) != row['isolatedCallerBinarySha256'] or actual != code or row['sourceLanguage'] != 'assembly' or row['ordinaryCBytes'] != 0:
            raise AssertionError('SDK memory real MW linked source/classification differs')
    machines = []
    records = [{'trace': [], 'fault': None, 'coverage': set()} for engine in range(2)]
    for engine in range(2):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        for address, size in ((0x02008000, 0x1000), (BASE, SIZE), (0x02600000, 0x2000), (0x027f0000, 0x10000)):
            machine.mem_map(address, size)
        for index, (kind, (name, address, size)) in enumerate(SPECS.items()):
            code = arm[address - 0x02000000:address - 0x02000000 + size] if engine == 0 else candidates[kind][1]
            machine.mem_write(address, code)
        def access(uc, access, address, size, value, user, engine=engine):
            if access == UC_MEM_WRITE:
                event = ('write', address, size, value & ((1 << (size * 8)) - 1))
            else:
                event = ('read', address, size, int.from_bytes(uc.mem_read(address, size), 'little'))
            records[engine]['trace'].append(event)
        def fault(uc, access, address, size, value, user, engine=engine):
            records[engine]['fault'] = ('write' if access in (UC_MEM_WRITE_UNMAPPED, UC_MEM_WRITE_PROT) else 'read', address, size)
            return False
        def observe(uc, address, size, user, engine=engine):
            records[engine]['coverage'].add(address)
        machine.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, access, begin=BASE, end=BASE + SIZE - 1)
        machine.hook_add(UC_HOOK_MEM_INVALID, fault)
        machine.hook_add(UC_HOOK_CODE, observe)
        machines.append(machine)
    rng = random.Random(2026102794)
    cases = calls = 0
    malformed = []
    def invoke(kind, args, initial=None, simple=False):
        nonlocal cases, calls
        initial = rng.randbytes(SIZE) if initial is None else initial
        expected, trace, fault = expected_memory(initial, kind, args)
        if simple:
            independent = bytearray(initial)
            if kind == 'fill':
                destination, value, count = args
                independent[destination - BASE:destination - BASE + count] = bytes([value]) * count
            else:
                source, destination, count = args
                independent[destination - BASE:destination - BASE + count] = initial[source - BASE:source - BASE + count]
            if bytes(independent) != expected:
                raise AssertionError('SDK native-width and independent byte expectations differ')
        stack = rng.randbytes(0x10000)
        saved = [rng.getrandbits(32) for register in SAVED]
        fault_pcs = []
        for engine, machine in enumerate(machines):
            records[engine]['trace'] = []
            records[engine]['fault'] = None
            machine.mem_write(BASE, initial)
            machine.mem_write(0x027f0000, stack)
            for register, value in zip(SAVED, saved):
                machine.reg_write(register, value)
            for register, value in zip((UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2), args):
                machine.reg_write(register, value)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP | (cases & 1))
            start = SPECS[kind][1]
            began = time.monotonic()
            try:
                machine.emu_start(start, STOP, count=1000000)
            except UcError:
                fault_pcs.append(hex(machine.reg_read(UC_ARM_REG_PC)))
                if fault is None or records[engine]['fault'] != fault:
                    raise AssertionError(('Memory unexpected fault', kind, args, fault, records[engine]['fault']))
            else:
                if fault is not None or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000 or [machine.reg_read(register) for register in SAVED] != saved or bool(machine.reg_read(UC_ARM_REG_CPSR) & 32) != bool(cases & 1):
                    raise AssertionError(('Memory return/fault/ABI differs', kind, args))
            if time.monotonic() - began > 2 or bytes(machine.mem_read(BASE, SIZE)) != expected or bytes(machine.mem_read(0x027f0000, 0x10000)) != stack:
                raise AssertionError(('Memory complete arena/stack/bound differs', kind, args))
            observed = records[engine]['trace']
            if observed != trace:
                raise AssertionError(('Memory access-width/order trace differs', kind, args, next(((i, a, b) for i, (a, b) in enumerate(zip(trace, observed)) if a != b), None), len(trace), len(observed)))
            calls += 1
        if fault:
            malformed.append({'kind': kind, 'arguments': args, 'expectedFault': fault, 'nativeAndCandidateFaultPcs': fault_pcs, 'nativeAndReassembledPartialArenaAndAccessTracesEqual': True})
        cases += 1
    for value in range(256):
        for alignment in range(4):
            for length in (0, 1, 2, 3, 7, 8, 9, 16):
                invoke('fill', (BASE + 0x3000 + alignment, value, length), simple=True)
    for value in (0x100, 0x101, 0xff00, 0x1020304, 0x80000000, 0xffffffff):
        for alignment in range(4):
            for length in (0, 1, 2, 3, 4, 7, 8, 9, 31, 32, 33, 255, 256, 1024, 4096):
                invoke('fill', (BASE + 0x3000 + alignment, value, length))
    for source_alignment in range(4):
        for destination_alignment in range(4):
            for length in (*range(21), 31, 32, 33, 63, 64, 65, 255, 256, 257, 1024, 4096):
                invoke('copy', (BASE + 0x1000 + source_alignment, BASE + 0x3000 + destination_alignment, length), simple=True)
    for delta in range(-12, 13):
        for alignment in range(4):
            for length in (0, 1, 2, 3, 4, 7, 8, 9, 15, 16, 17, 31, 32, 33, 63, 64, 65):
                invoke('copy', (BASE + 0x2000 + alignment, BASE + 0x2000 + alignment + delta, length))
    for kind, args in (('fill', (0, 255, 0)), ('copy', (0, 0, 0)), ('fill', (0, 255, 1)), ('fill', (0, 255, 2)), ('copy', (0, BASE + 0x3000, 1)), ('copy', (BASE + 0x1000, 0, 1)), ('fill', (BASE + SIZE - 1, 0x41, 2)), ('copy', (BASE + SIZE - 2, BASE + 0x3000, 3))):
        invoke(kind, args)
    overlap_examples = []
    for delta, count, expected_hex in ((1, 6, '000000020304050708090a0b0c0d0e0f'), (2, 8, '000100010001000100010a0b0c0d0e0f'), (4, 12, '00010203000102030001020300010203')):
        initial = bytearray(rng.randbytes(SIZE))
        initial[0x2000:0x2020] = bytes(range(32))
        args = (BASE + 0x2000, BASE + 0x2000 + delta, count)
        expected, trace, fault = expected_memory(initial, 'copy', args)
        if expected[0x2000:0x2010].hex() != expected_hex or fault:
            raise AssertionError('Independent literal overlapping transfer fixture differs')
        invoke('copy', args, bytes(initial))
        overlap_examples.append({'sourceRelativeToExample': 0, 'destinationRelativeToExample': delta, 'count': count, 'initial32ByteHex': bytes(range(32)).hex(), 'resultFirst16ByteHex': expected_hex})
    summaries = []
    for kind, (name, address, size) in SPECS.items():
        row = dict(candidates[kind][0])
        native = arm[address - 0x02000000:address - 0x02000000 + size]
        if native != candidates[kind][1] or row['bytes'] != size:
            raise AssertionError('SDK memory oracle source bytes differ from complete native span')
        row['matchingBytesAtNativeOffset'] = size
        row['nativeSpanSha256'] = sha(native)
        row['allNativeInstructionsReached'] = all(pc in records[0]['coverage'] for pc in range(address, address + size, 4))
        if not row['allNativeInstructionsReached']:
            raise AssertionError(('Memory native instruction coverage incomplete', kind))
        summaries.append(row)
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndReassembledCalls': calls, 'instructionLimitPerCall': 1000000, 'secondsLimitPerCall': 2, 'sourceFunctions': summaries, 'fullArenaStackAndReadWriteAddressWidthValueOrderVerified': True, 'malformedPartialStateCases': malformed, 'independentLiteralOverlapExamples': overlap_examples, 'retainedNativeEntries': [], 'platformStubs': {}, 'originalSdkAssemblyBodies': 2, 'ordinaryCBytes': 0, 'justifiedAssemblyBytes': 452, 'bothArmAndThumbReturnStatesVerified': True, 'limitations': ['All reads/writes, including preserved neighbor halfwords and partial malformed effects, are target-instruction behavior; no physical cache/VRAM timing claim follows.', 'Overlap fixtures describe forward native16/32-bit transfer effects rather than portable C memcpy/memmove guarantees.', 'Full byte equivalence is independently established by assembly and real MW linking, and these bodies are separately classified as justified original SDK assembly.']}
