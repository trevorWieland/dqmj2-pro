import bisect
import hashlib
import random
import re
import struct
from functools import cache

from ov001_ability28_fixture_20261031 import REGS
from link_runtime_unit import measured_module
from project import ROOT
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import *

ENTRY, STOP, SP, STATE = 0x021D7860, 0x08000000, 0x0301FF00, 0x0220EB04
PALETTE, GATE, MODE = 0x020FB2E8, 0x020DCB40, 0x020E3300
NATIVE = {0x02002C98, 0x02008C58, 0x0201D444, 0x02048308}


@cache
def inventory():
    result = []
    for module, file in [('main', 'config/arm9/symbols.txt'), ('ov006', 'config/arm9/overlays/ov006/symbols.txt')]:
        for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', (ROOT / file).read_text()):
            start = int(address, 0)
            result.append((start, start + int(size, 0), module, mode))
    unused, image, config = measured_module('itcm')
    for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', config):
        start = int(address, 0)
        result.append((start, start + int(size, 0), 'itcm', mode))
    result.sort()
    return [item[0] for item in result], result


def recipes():
    return [dict(seed=0x138000 + index, gate=gate, variant=variant, dmaSelector=0xFFFFFFFF)
        for index, (gate, variant) in enumerate((gate, variant) for gate in (0, 1, 65535) for variant in range(2))]


def execute(main, overlay, recipe, source_bytes=None):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in [(0x01FF8000, 0x8000), (0x02000000, 0x400000), (0x03000000, 0x20000), (0x04000000, 0x2000),
        (0x05000000, 0x1000), (0x06000000, 0x80000), (STOP, 0x1000)]:
        machine.mem_map(start, size)
    machine.mem_write(0x02000000, main)
    unused, itcm, unused = measured_module('itcm')
    machine.mem_write(0x01FF8000, itcm)
    machine.mem_write(0x021D7240, overlay)
    if source_bytes is not None:
        machine.mem_write(ENTRY, source_bytes)
    if struct.unpack_from('<III', main, 0x2CF4) != (GATE, MODE, 0xFFF0FFF0):
        raise ValueError('Setup38 native video-mode globals/mask differ')
    rng = random.Random(recipe['seed'])
    for address, size in [(STATE, 0xA0), (PALETTE, 0x800), (0x03000000, 0x20000), (0x05000000, 0x1000), (0x06000000, 0x80000)]:
        machine.mem_write(address, rng.randbytes(size))
    machine.mem_write(GATE, struct.pack('<H', recipe['gate']))
    machine.mem_write(0x020DCB44, struct.pack('<I', recipe['dmaSelector']))
    machine.mem_write(MODE, rng.randbytes(4))
    initial_io = bytearray(0x2000)
    struct.pack_into('<I', initial_io, 0, rng.getrandbits(32))
    for offset in (8, 10, 12, 14):
        struct.pack_into('<H', initial_io, offset, rng.getrandbits(16))
    machine.mem_write(0x04000000, bytes(initial_io))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    expected_ram[MODE - 0x02000000:MODE - 0x02000000 + 2] = struct.pack('<H', 1)
    expected_ram[STATE - 0x02000000:STATE - 0x02000000 + 0xA0] = bytes(0xA0)
    expected_io = bytearray(initial_io)
    control = struct.unpack_from('<I', initial_io, 0)[0] & 0xFFF0FFF0 | (0x10000 if recipe['gate'] else 0)
    struct.pack_into('<I', expected_io, 0, control & ~0x1F00 | 0x1B00)
    for offset, bits in [(8, 0x4007), (10, 0x212), (14, 0x518)]:
        struct.pack_into('<H', expected_io, offset, struct.unpack_from('<H', initial_io, offset)[0] & 0x40 | bits)
    expected_palette = bytearray(machine.mem_read(0x05000000, 0x1000))
    palette = bytes(machine.mem_read(PALETTE, 0x800))
    for destination, source in [(0, 0x600), (0x200, 0x400), (0x400, 0), (0x600, 0x200)]:
        expected_palette[destination:destination + 512] = palette[source:source + 512]
    filenames = [(address, overlay[address - 0x021D7240:].split(b'\0', 1)[0]) for address in (0x0220CB04, 0x0220CB1C)]
    if any(b'%' in name or len(name) >= 32 for address, name in filenames):
        raise ValueError('Setup38 bounded literal filename assumptions differ')
    registers = [rng.getrandbits(32) for unused in range(13)]
    for register, value in zip(REGS, registers):
        machine.reg_write(register, value)
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    starts, ranges = inventory()
    cache_entries, pending, returned, provided, seen = {}, [], [], [], set()
    counts = dict(instructions=0, writes=0)
    trace, write_trace = hashlib.sha256(), hashlib.sha256()
    caller_low, final_sdk_return = None, None
    caller_bytes = overlay[ENTRY - 0x021D7240:] if source_bytes is None else source_bytes
    pushed_bytes = (int.from_bytes(caller_bytes[:4], 'little') & 0xFFFF).bit_count() * 4

    def step(engine, pc, size, unused):
        nonlocal caller_low, final_sdk_return
        while pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['sp']:
                raise ValueError('Setup38 native dependency stack differs')
            if item['address'] == 0x0201D444:
                value = bytes(engine.mem_read(item['output'], len(item['filename']) + 1))
                if value != item['filename'] + b'\0':
                    raise ValueError('Setup38 actual formatted filename differs')
            if item['address'] == 0x02048308:
                final_sdk_return = engine.reg_read(REGS[0])
            returned.append(dict(address=hex(item['address']), actualReturn=True, physicalR0=engine.reg_read(REGS[0])))
        if pc == STOP:
            engine.emu_stop()
            return
        if counts['instructions'] >= 100000:
            raise ValueError('Setup38 instruction bound exceeded')
        counts['instructions'] += 1
        trace.update(struct.pack('<I', pc))
        if pc == ENTRY + 8:
            caller_low = engine.reg_read(UC_ARM_REG_SP)
        if pc == 0x0202A8E0:
            index = len(provided)
            if index >= 2:
                raise ValueError('Setup38 unexpected file-length provider')
            pointer = engine.reg_read(REGS[0])
            filename = filenames[index][1]
            if bytes(engine.mem_read(pointer, len(filename) + 1)) != filename + b'\0':
                raise ValueError('Setup38 supplied length lookup received wrong filename')
            provided.append(dict(address=hex(pc), filename=filename.decode('ascii'), suppliedLength=0))
            engine.reg_write(REGS[0], 0)
            for register in (1, 2, 3, 12):
                engine.reg_write(REGS[register], (recipe['seed'] * 0x9E3779B9 + index * 17 + register) & 0xFFFFFFFF)
            engine.reg_write(UC_ARM_REG_PC, engine.reg_read(UC_ARM_REG_LR))
            return
        if pc not in cache_entries:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Setup38 escaped qualified native inventory', hex(pc)))
            cache_entries[pc] = ranges[index]
        entry = cache_entries[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Setup38 entered wrong native mode')
        seen.add(entry)
        if pc in NATIVE:
            item = dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), sp=engine.reg_read(UC_ARM_REG_SP))
            if pc == 0x0201D444:
                pointer, format_pointer = engine.reg_read(REGS[0]), engine.reg_read(REGS[1])
                index = sum(row['address'] == '0x201d444' for row in returned)
                if index >= 2 or format_pointer != filenames[index][0]:
                    raise ValueError('Setup38 unexpected native filename formatter')
                if caller_low is None or pointer < caller_low + 2 or pointer + 32 > SP - pushed_bytes:
                    raise ValueError('Setup38 filename buffer escapes caller locals')
                item.update(output=pointer, filename=filenames[index][1])
            pending.append(item)

    def written(engine, access, address, size, value, unused):
        allowed = [(0x03000000, 0x20000), (0x04000000, 0x2000), (0x05000000, 0x800),
            (0x06000000, 0x80000), (STATE, 0xA0), (MODE, 2), (GATE, 2)]
        if not any(start <= address <= start + length - size for start, length in allowed):
            raise ValueError(('Setup38 unexpected native write', hex(address), size))
        counts['writes'] += 1
        write_trace.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    try:
        machine.emu_start(ENTRY, STOP + 4, count=100001)
    except Exception as error:
        raise ValueError(dict(nativeFaultPc=hex(machine.reg_read(UC_ARM_REG_PC)),
            instructions=counts['instructions'], nativeReturns=returned, providedCalls=provided,
            registers=[hex(machine.reg_read(register)) for register in REGS])) from error
    actual = [machine.reg_read(register) for register in REGS]
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != SP or pending or len(returned) != 6 or len(provided) != 2:
        raise ValueError('Setup38 actual return/stack/call-completion gate differs')
    if actual[4:12] != registers[4:12] or actual[0] != final_sdk_return:
        raise ValueError('Setup38 preserved registers/final SDK return propagation differ')
    if bytes(machine.mem_read(0x01FF8000, len(itcm))) != itcm:
        raise ValueError('Setup38 changed native ITCM image')
    for address, data in [(0x02000000, bytes(expected_ram)), (0x04000000, bytes(expected_io)),
        (0x05000000, bytes(expected_palette)), (0x06000000, bytes(0x80000))]:
        actual_data = bytes(machine.mem_read(address, len(data)))
        if actual_data != data:
            offset = next(i for i, pair in enumerate(zip(actual_data, data)) if pair[0] != pair[1])
            raise ValueError(('Setup38 complete memory model differs', hex(address + offset), actual_data[offset:offset + 8].hex(), data[offset:offset + 8].hex()))
    return dict(actualReturn=True, returnWord=actual[0], **counts, nativeDependencyActualReturns=returned,
        providedCalls=provided, nativeEntries=[[hex(start), end - start, module, mode] for start, end, module, mode in sorted(seen)],
        registers=actual, cpsr=machine.reg_read(UC_ARM_REG_CPSR), pcTraceSha256=trace.hexdigest(), writeTraceSha256=write_trace.hexdigest(),
        ramSha256=hashlib.sha256(expected_ram).hexdigest(), ioSha256=hashlib.sha256(expected_io).hexdigest(),
        paletteSha256=hashlib.sha256(expected_palette).hexdigest(), vramSha256=hashlib.sha256(bytes(0x80000)).hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
