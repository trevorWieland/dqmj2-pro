import json
import random
import struct
import utility_runtime
import match_lowlevel
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_CPSR
from wave20261102_child_prepare import ROOT, LANE, WORK
from project import write_json

ADDRESSES = {0x020035bc: 'previous', 0x020035e8: 'remove', 0x020036c4: 'prepend',
             0x02003720: 'append', 0x02003780: 'empty'}
BASE, LIST, OBJECT, PREVIOUS, NEXT, STOP = 0x03000000, 0x03001000, 0x03002000, 0x03003000, 0x03004000, 0x05000000


def word(memory, address, value):
    struct.pack_into('<I', memory, address - BASE, value)


def initial(kind, offset, count, variant):
    memory = bytearray(random.Random(20261102).randbytes(0x8000))
    empty = variant == 0
    previous = PREVIOUS if variant & 1 else 0
    next_object = NEXT if variant & 2 else 0
    first = 0 if empty else PREVIOUS
    last = 0 if empty else NEXT
    if kind == 'remove':
        first = OBJECT if not previous else PREVIOUS
        last = OBJECT if not next_object else NEXT
    word(memory, LIST, first)
    word(memory, LIST + 4, last)
    struct.pack_into('<HH', memory, LIST + 8 - BASE, count, offset)
    word(memory, OBJECT + offset, previous)
    word(memory, OBJECT + offset + 4, next_object)
    word(memory, PREVIOUS + offset + 4, OBJECT)
    word(memory, NEXT + offset, OBJECT)
    return memory, first, last, previous, next_object


def model(memory, kind, offset, count, variant, first, last, previous, next_object):
    output = bytearray(memory)
    returned = None
    if kind == 'previous':
        returned = last if variant == 0 else previous
    elif kind == 'remove':
        word(output, previous + offset + 4 if previous else LIST, next_object)
        word(output, next_object + offset if next_object else LIST + 4, previous)
        word(output, OBJECT + offset, 0)
        word(output, OBJECT + offset + 4, 0)
        struct.pack_into('<H', output, LIST + 8 - BASE, (count - 1) & 65535)
    else:
        if kind == 'empty' or first == 0:
            word(output, OBJECT + offset + 4, 0)
            word(output, OBJECT + offset, 0)
            word(output, LIST, OBJECT)
            word(output, LIST + 4, OBJECT)
        elif kind == 'prepend':
            word(output, OBJECT + offset, 0)
            word(output, OBJECT + offset + 4, first)
            word(output, first + offset, OBJECT)
            word(output, LIST, OBJECT)
        else:
            word(output, OBJECT + offset, last)
            word(output, OBJECT + offset + 4, 0)
            word(output, last + offset + 4, OBJECT)
            word(output, LIST + 4, OBJECT)
        struct.pack_into('<H', output, LIST + 8 - BASE, (count + 1) & 65535)
    return output, returned


def execute(payload, entry, memory, offset, count, variant, flags, helper):
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    engine.mem_map(0x02000000, 0x10000)
    engine.mem_map(BASE, 0x10000)
    engine.mem_map(STOP, 0x1000)
    address = int(entry['address'], 0)
    engine.mem_write(address, payload)
    engine.mem_write(0x02003780, helper if address != 0x02003780 else payload)
    engine.mem_write(BASE, bytes(memory))
    engine.reg_write(UC_ARM_REG_CPSR, flags | 0x13)
    values = [random.Random(20261102 + index).getrandbits(32) for index in range(15)]
    values[0] = LIST
    values[1] = 0 if ADDRESSES[address] == 'previous' and variant == 0 else OBJECT
    values[-2:] = [BASE + 0xff00, STOP]
    for register, value in zip(match_lowlevel.REGISTERS, values):
        engine.reg_write(register, value)
    visited, writes, helpers = set(), [], []
    def visit(uc, here, size, unused):
        if here == STOP:
            return
        if not (address <= here < address + len(payload) or 0x02003780 <= here < 0x02003780 + len(helper)):
            raise ValueError('Unexpected SDK callee execution')
        if here == 0x02003780 and address != here:
            helpers.append(here)
        visited.add(here)
    engine.hook_add(UC_HOOK_CODE, visit)
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, here, size, value, unused: writes.append([here, size, value]))
    engine.emu_start(address, STOP, count=512)
    if engine.reg_read(UC_ARM_REG_PC) != STOP:
        raise ValueError('List fixture failed bounded normal return')
    return dict(registers=[engine.reg_read(r) for r in match_lowlevel.REGISTERS],
                cpsr=engine.reg_read(UC_ARM_REG_CPSR), writes=writes,
                memory=bytes(engine.mem_read(BASE, len(memory))), visited=sorted(visited), helpers=helpers)


def validate(entry, linked):
    address = int(entry['address'], 0)
    if address not in ADDRESSES:
        return None
    raw = (ROOT / 'extract/utility/runtime/utility-child-arm9-main.bin').read_bytes()
    native = raw[address - 0x02000000:address - 0x02000000 + entry['bytes']]
    helper = raw[0x3780:0x3780 + 44]
    kind = ADDRESSES[address]
    variants = range(4) if kind == 'remove' else range(2) if kind in ('previous', 'prepend', 'append') else range(1)
    results, visited = [], set()
    for offset in [0, 4, 12, 32]:
        for count in [0, 1, 65535]:
            for variant in variants:
                for flags in [0, 0xf0000000]:
                    memory, first, last, previous, next_object = initial(kind, offset, count, variant)
                    expected_memory, returned = model(memory, kind, offset, count, variant, first, last, previous, next_object)
                    expected = execute(native, entry, memory, offset, count, variant, flags, helper)
                    actual = execute(linked, entry, memory, offset, count, variant, flags, helper)
                    if actual != expected or actual['memory'] != expected_memory:
                        raise ValueError('List byte/typed-model mismatch')
                    if returned is not None and actual['registers'][0] != returned:
                        raise ValueError('Previous-node result differs from typed model')
                    visited.update(actual['visited'])
                    record = dict(offset=offset, count=count, variant=variant, flags=flags,
                        memorySha256=utility_runtime.sha(actual['memory']), registers=actual['registers'],
                        cpsr=actual['cpsr'], writes=actual['writes'], visited=actual['visited'], helpers=actual['helpers'])
                    results.append(record)
    path = LANE / 'list-oracles' / ('%08x.json' % address)
    write_json(path, dict(address=hex(address), kind=kind, records=results))
    return dict(supported=True, fixtureKind='synthetic-native32-list-state', vectors=len(results),
        nativeAndRecompiledCalls=2 * len(results), instructionLimit=512, verifiedNormalReturns=True,
        verifiedTypedMemoryModel=True, trace=path.relative_to(ROOT).as_posix(),
        traceSha256=utility_runtime.sha(path.read_bytes()), visitedInstructionAddresses=[hex(a) for a in sorted(visited)],
        nativeHelperAddress='0x02003780', nativeHelperBytes=44, nativeHelperSourceCredit=0,
        limitations=['Synthetic valid mapped list nodes only; invalid pointers and concurrent mutation are untested',
                    'No DS hardware, original save or gameplay scene was executed'])
