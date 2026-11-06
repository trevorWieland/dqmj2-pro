import bisect
import hashlib
import random
import re
import struct
from functools import cache

from link_runtime_unit import measured_module
from ov001_award_fixture_20261029 import functions
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

STOP, STACK, RNG = 0x07000000, 0x03010000, 0x020F6044


@cache
def inventory():
    metadata, image, config = measured_module('itcm')
    ranges = list(functions()[1])
    ranges += [(int(address, 0), int(address, 0) + int(size, 0), 'itcm', mode)
               for mode, size, address in re.findall(r'kind:function\((arm|thumb),size=(0x[0-9a-f]+)\) addr:(0x[0-9a-f]+)', config)]
    ranges.sort()
    return metadata, image, [row[0] for row in ranges], ranges


def execute(main, overlay, blobs, address, arguments, memory, patches, expected, seed, draws, protocols=()):
    metadata, itcm, starts, ranges = inventory()
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in ((0x01FF8000, 0x8000), (0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(start, size)
    machine.mem_write(0x01FF8000, itcm)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(0x02300000, blobs['EnmyKindTbl.bin'][8:])
    machine.mem_write(0x02310000, blobs['AbilityTbl.bin'])
    machine.mem_write(0x020F69F0, struct.pack('<I', 0x02300000))
    machine.mem_write(0x02238D58, struct.pack('<I', 0x02310000))
    machine.mem_write(0x020F69E4, bytes(4))
    for location, payload in memory:
        machine.mem_write(location, payload)
    randomizer = random.Random(seed)
    machine.mem_write(0x03000000, randomizer.randbytes(0x20000))
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    registers[:len(arguments)] = [word & 0xFFFFFFFF for word in arguments]
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for location, payload in patches:
        expected_ram[location - 0x02000000:location - 0x02000000 + len(payload)] = payload
    state = struct.unpack('<I', machine.mem_read(RNG, 4))[0]
    cache_entries, seen, pending, rng_returns = {}, set(), [], []
    protocol_pending, protocol_returns, protocol_entries = [], [], []
    protocol_addresses = {row["address"] for row in protocols}
    trace, writes, counts = hashlib.sha256(), hashlib.sha256(), dict(instructions=0, writes=0)

    def step(engine, pc, size, unused):
        nonlocal state
        counts['instructions'] += 1
        if protocol_pending and pc == protocol_pending[-1]['returnPc']:
            item = protocol_pending.pop()
            recipe = item['recipe']
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp']:
                raise ValueError('Native turn-start dependency returned with a changed stack')
            if 'returnWord' in recipe and engine.reg_read(UC_ARM_REG_R0) != recipe['returnWord']:
                raise ValueError('Native turn-start dependency returned a different modeled word')
            if 'setRng' in recipe:
                state = recipe['setRng']
                if struct.unpack('<I', engine.mem_read(RNG, 4))[0] != state:
                    raise ValueError('Native scene seed setter stored a different state')
            protocol_returns.append(dict(address=hex(recipe['address']), actualReturn=True,
                                         returnBits=hex(engine.reg_read(UC_ARM_REG_R0)),
                                         arguments=recipe.get('arguments', [])))
        trace.update(struct.pack('<I', pc))
        if pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp'] or engine.reg_read(UC_ARM_REG_R0) != item['draw']:
                raise ValueError('Original RNG did not return its independently modeled value')
            if struct.unpack('<I', engine.mem_read(RNG, 4))[0] != state:
                raise ValueError('Original RNG state differs after actual return')
            rng_returns.append(dict(limit=item['limit'], result=item['draw'], actualReturn=True))
        if pc not in cache_entries:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Order fixture escaped qualified native inventory', hex(pc)))
            cache_entries[pc] = ranges[index]
        entry = cache_entries[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Order fixture entered an incorrect native mode')
        seen.add(entry)
        if pc in protocol_addresses:
            index = len(protocol_entries)
            if index >= len(protocols) or pc != protocols[index]['address']:
                raise ValueError('Unexpected native turn-start protocol call or order')
            recipe = protocols[index]
            arguments = [engine.reg_read(UC_ARM_REG_R0 + i) for i in range(len(recipe.get('arguments', [])))]
            if arguments != recipe.get('arguments', []):
                raise ValueError(('Native turn-start dependency arguments differ', hex(pc), arguments))
            protocol_entries.append(dict(address=hex(pc), arguments=arguments))
            protocol_pending.append(dict(recipe=recipe, entrySp=engine.reg_read(UC_ARM_REG_SP),
                                         returnPc=engine.reg_read(UC_ARM_REG_LR)))
        if pc == 0x0203D294:
            index, limit = len(rng_returns), engine.reg_read(UC_ARM_REG_R0)
            state = (state * 0x41C64E6D + 0x3039) & 0xFFFFFFFF
            draw = (state >> 16) % limit if limit > 0 else 0
            if index >= len(draws) or (limit, draw) != tuple(draws[index]):
                raise ValueError('Unexpected native RNG call/value in order fixture')
            pending.append(dict(returnPc=engine.reg_read(UC_ARM_REG_LR), entrySp=engine.reg_read(UC_ARM_REG_SP),
                                limit=limit, draw=draw))

    def written(engine, access, location, size, word, unused):
        if not (STACK <= location < location + size <= STACK + 0x10000 or
                any(start <= location < location + size <= start + len(payload) for start, payload in patches)):
            raise ValueError(('Order fixture wrote outside modeled effects', hex(location)))
        counts['writes'] += 1
        writes.update(struct.pack('<IIQ', location, size, word & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(address, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Order fixture did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != expected or pending or len(rng_returns) != len(draws) or protocol_pending or len(protocol_returns) != len(protocols):
        raise ValueError('Order return or nested RNG completion differs')
    if any(machine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError('Order fixture damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram) or bytes(machine.mem_read(0x01FF8000, len(itcm))) != itcm:
        raise ValueError('Order fixture full RAM/ITCM differs from independent model')
    return dict(actualReturn=True, returnBits=hex(expected), **counts, rngReturns=rng_returns, protocolReturns=protocol_returns, protocolEntries=protocol_entries,
                nativeEntries=[[hex(begin), end - begin, module, mode] for begin, end, module, mode in sorted(seen)],
                registers=[machine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)],
                wholeRamSha256=hashlib.sha256(ram).hexdigest(), writeTraceSha256=writes.hexdigest(),
                pcTraceSha256=trace.hexdigest(), cpsr=machine.reg_read(UC_ARM_REG_CPSR),
                stackSha256=hashlib.sha256(bytes(machine.mem_read(0x03000000, 0x20000))).hexdigest())
