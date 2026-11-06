import bisect
import hashlib
import random
import struct
from itertools import product

from ov001_damage_pipeline_fixture_20261030 import inventory
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR, UC_CPU_ARM_946

STOP, STACK, ENTRY_SP = 0x08000000, 0x03000000, 0x0301FF00
STATE, AGGREGATE, CONTEXT, ROSTER = 0x02238F58, 0x02239C10, 0x020F69C4, 0x022362AC
PROVIDERS = {0x02044FF4, 0x021F153C, 0x021F18D8, 0x021F1684, 0x021F1804}
NATIVE = {0x021F1508, 0x021F0F88, 0x021DB438, 0x021DB8D0, 0x020443EC,
          0x02044424, 0x021E2C10, 0x022033F8, 0x021F15D8, 0x021F1604, 0x021F1634}


def recipes():
    return [dict(enabled=enabled, mode=mode, flags=flags, invalid=invalid, metric=metric, seed=2210000 + index)
            for index, (enabled, mode, flags, invalid, metric) in enumerate(product(range(8), (0, 1, 6, 255),
                (0, 0x08000000, 0x10000000, 0x18000000), (0, 2, 5), (-33, 65)))]


def execute(main, overlay, recipe):
    metadata, itcm, starts, ranges = inventory()
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in ((0x01FF8000, 0x8000), (0x02000000, 0x400000), (STACK, 0x20000), (STOP, 0x1000)):
        machine.mem_map(start, size)
    machine.mem_write(0x01FF8000, itcm)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    randomizer = random.Random(recipe['seed'])
    machine.mem_write(STACK, randomizer.randbytes(0x20000))
    machine.mem_write(STATE, randomizer.randbytes(0x2C))
    machine.mem_write(STATE + 0x14, struct.pack('<i', recipe['metric']))
    machine.mem_write(AGGREGATE + 0x1C, randomizer.randbytes(4))
    machine.mem_write(CONTEXT + 0x20, struct.pack('<I', recipe['flags']))
    machine.mem_write(CONTEXT + 0x24, bytes([recipe['mode']]))
    actors, saved, eligibility = bytearray(3 * 1088), [], []
    expected_providers = []
    enabled_count = recipe['enabled'].bit_count()
    positions = overlay[0x0222E0F4 - 0x021D7240:0x0222E0F4 - 0x021D7240 + 9]
    for slot in range(3):
        address, record_address = ROSTER + slot * 1088, 0x02352000 + slot * 0x100
        record = bytearray(randomizer.randbytes(192))
        struct.pack_into('<I', record, 0xAC, 0)
        kind, gender = slot - 1, slot
        struct.pack_into('<h', record, 0x2A, kind)
        record[0x2C] = gender
        struct.pack_into('<I', actors, slot * 1088 + 0x1E8, record_address)
        actors[slot * 1088 + 0x31C] = (1, 255)[slot % 2] if recipe['enabled'] >> slot & 1 else 0
        actors[slot * 1088 + 0x1FF] = 1 if recipe['invalid'] >> slot & 1 else 0
        eligible = bool(actors[slot * 1088 + 0x31C] and not actors[slot * 1088 + 0x1FF])
        eligibility.append(eligible)
        initial = bytes(record)
        if eligible:
            if recipe['mode'] in (0, 6):
                supplied = bytes((slot * 17 + index) & 255 for index in range(14))
                record[0xB2:0xC0] = supplied
                expected_providers.append(dict(address=0x02044FF4, arguments=[record_address + 0xB2, kind & 0xFFFFFFFF, gender],
                                               writeAddress=record_address + 0xB2, writeBytes=supplied.hex()))
            x = positions[(enabled_count - 1) * 3 + slot]
            y = 20 + (slot % 2) * 2 if enabled_count & 1 else 20
            expected_providers.append(dict(address=0x021F153C, arguments=[record_address + 0xB2, x, y],
                                           opaqueLabelSha256=hashlib.sha256(bytes(record[0xB2:0xC0])).hexdigest()))
        machine.mem_write(record_address, initial)
        saved.append((record_address, bytes(record)))
    machine.mem_write(ROSTER, bytes(actors))
    expected_providers.append(dict(address=0x021F18D8, arguments=[0, 2, 2, 16], stackArguments=[2, 0]))
    if recipe['flags'] & 0x18000000:
        expected_providers.append(dict(address=0x021F18D8, arguments=[1, 20, 2, 12], stackArguments=[2, 0]))
    if recipe['mode'] == 6:
        expected_providers += [dict(address=0x021F18D8, arguments=[2, 0, 0, 32], stackArguments=[2, 0]),
                               dict(address=0x021F1804, arguments=[])]
    expected_providers.append(dict(address=0x021F1684, arguments=[]))
    quotient = abs(recipe['metric']) // 32 * (-1 if recipe['metric'] < 0 else 1)
    changes = [(STATE + 0x24, bytes(4)), (STATE + 0x28, struct.pack('<I', (quotient + 1) & 0xFFFFFFFF))]
    if recipe['flags'] & 0x18000000:
        changes.append((AGGREGATE + 0x1C, struct.pack('<I', 15 if recipe['flags'] & 0x08000000 else 30)))
    changes += saved
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for address, payload in changes:
        expected_ram[address - 0x02000000:address - 0x02000000 + len(payload)] = payload
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, ENTRY_SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    provided, returned, pending, seen, cache = [], [], [], set(), {}
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = dict(nativeInstructions=0, nativeWrites=0)

    def step(engine, pc, size, unused):
        trace.update(struct.pack('<I', pc))
        if pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp']:
                raise ValueError('Native roster dependency changed its stack')
            returned.append(dict(address=hex(item['address']), actualReturn=True, physicalR0=hex(engine.reg_read(UC_ARM_REG_R0))))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Roster fixture escaped native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Roster fixture native mode differs')
        seen.add(entry)
        if pc in PROVIDERS:
            index = len(provided)
            if index >= len(expected_providers) or expected_providers[index]['address'] != pc:
                raise ValueError(('Unexpected roster rendering boundary', hex(pc), index))
            expected = expected_providers[index]
            arguments = [engine.reg_read(UC_ARM_REG_R0 + n) for n in range(len(expected['arguments']))]
            if arguments != expected['arguments']:
                raise ValueError(('Roster rendering arguments differ', hex(pc), arguments, expected['arguments']))
            stack = expected.get('stackArguments', [])
            if list(struct.unpack('<' + 'I' * len(stack), bytes(engine.mem_read(engine.reg_read(UC_ARM_REG_SP), len(stack) * 4)))) != stack:
                raise ValueError('Roster rendering stack arguments differ')
            if 'opaqueLabelSha256' in expected and hashlib.sha256(bytes(engine.mem_read(arguments[0], 14))).hexdigest() != expected['opaqueLabelSha256']:
                raise ValueError('Provided label data/order differs')
            if 'writeBytes' in expected:
                engine.mem_write(expected['writeAddress'], bytes.fromhex(expected['writeBytes']))
            destination = engine.reg_read(UC_ARM_REG_LR)
            for n in (0, 1, 2, 3, 12):
                engine.reg_write(UC_ARM_REG_R0 + n, randomizer.getrandbits(32))
            engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
            engine.reg_write(UC_ARM_REG_PC, destination)
            provided.append({**expected, 'address': hex(pc), 'nativeCalleeExecuted': False})
            return
        counts['nativeInstructions'] += 1
        if pc in NATIVE:
            pending.append(dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), entrySp=engine.reg_read(UC_ARM_REG_SP)))

    def written(engine, access, address, size, value, unused):
        if not (STACK <= address < address + size <= STACK + 0x20000 or
                any(start <= address < address + size <= start + len(payload) for start, payload in changes)):
            raise ValueError(('Native roster write outside independent effects', hex(address), size))
        counts['nativeWrites'] += 1
        writes.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(0x02210E18, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != ENTRY_SP or pending:
        raise ValueError('Roster caller did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != sum(eligibility) or len(provided) != len(expected_providers):
        raise ValueError('Roster return/boundaries differ')
    if any(machine.reg_read(UC_ARM_REG_R0 + n) != registers[n] for n in range(4, 12)):
        raise ValueError('Roster caller damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram) or bytes(machine.mem_read(0x01FF8000, len(itcm))) != itcm:
        raise ValueError('Roster complete RAM/ITCM differs')
    return dict(actualReturn=True, returnBits=hex(sum(eligibility)), **counts, providerCalls=provided, nativeDependencyReturns=returned,
        registers=[machine.reg_read(UC_ARM_REG_R0 + n) for n in range(13)], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
        wholeRamSha256=hashlib.sha256(ram).hexdigest(), writeTraceSha256=writes.hexdigest(), pcTraceSha256=trace.hexdigest(),
        stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK, 0x20000))).hexdigest(),
        nativeEntries=[[hex(begin), end - begin, module, mode] for begin, end, module, mode in sorted(seen)])
