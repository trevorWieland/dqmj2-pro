import bisect
import hashlib
import random
import struct

from ov001_damage_pipeline_fixture_20261030 import inventory
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_CPSR, UC_CPU_ARM_946

STOP, STACK, ENTRY_SP = 0x08000000, 0x03000000, 0x0301FF00
ADDRESS = 0x021F0F98
NATIVE_ENTRIES = {0x0204BBEC, 0x020848D0, 0x021F1A08, 0x0205F998, 0x02008C14, 0x021F0F60,
                  0x0204518C, 0x02045128, 0x0204514C}
PROVIDERS = {0x0203CC2C, 0x020481B8, 0x0202A498, 0x02046150,
             0x020462E0, 0x020489F0, 0x02045654, 0x020462CC, 0x02048308}


def execute(main, overlay, seed, span_length, initial_state, opaque_result):
    metadata, itcm, starts, ranges = inventory()
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for start, size in ((0x01FF8000, 0x8000), (0x02000000, 0x400000), (STACK, 0x20000), (STOP, 0x1000)):
        machine.mem_map(start, size)
    machine.mem_write(0x01FF8000, itcm)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    randomizer = random.Random(seed)
    machine.mem_write(STACK, randomizer.randbytes(0x20000))
    resource = 0x02350000 + seed % 8 * 0x100
    payload, object_address, object_data = 0x02360000, 0x02378000, 0x02378100
    machine.mem_write(resource, struct.pack('<III', 1, payload - resource, payload - resource + span_length))
    machine.mem_write(payload, randomizer.randbytes(max(span_length, 1)))
    machine.mem_write(object_address, struct.pack('<III', 0, 0, object_data))
    changed = [(0x02102994, bytes(0x30)), (0x02238F58, bytes([3])),
               (0x02238F6C, struct.pack('<IIII', *([object_data + 0x20] * 4)))]
    row = bytearray(0x48)
    struct.pack_into('<I', row, 0, 0x7F)
    row[8:13] = bytes([0x7F]) * 5
    changed.append((0x02238F9C, bytes(row) * 32))
    for location, final in changed:
        machine.mem_write(location, randomizer.randbytes(len(final)))
    machine.mem_write(0x02238F58, bytes([initial_state]))
    expected_ram = bytearray(machine.mem_read(0x02000000, 0x400000))
    for location, final in changed:
        expected_ram[location - 0x02000000:location - 0x02000000 + len(final)] = final
    registers = [randomizer.getrandbits(32) for unused in range(13)]
    for index, word in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, word)
    machine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
    machine.reg_write(UC_ARM_REG_SP, ENTRY_SP)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    frame = ENTRY_SP - 24
    calls = [(0x0203CC2C, [0x0222ECB4, 1]), (0x020481B8, [payload, 0, span_length]), (0x0202A498, [1, resource]),
             (0x02046150, [0, 1, 2]), (0x020462E0, [0, 2, 1]), (0x020489F0, [0]),
             (0x020481B8, [frame, 0, 2]), (0x02045654, [1]), (0x02045654, [2]),
             (0x020462CC, [0]), (0x02048308, [])]
    provided, native_returns, pending, seen = [], [], [], set()
    trace, writes = hashlib.sha256(), hashlib.sha256()
    counts = dict(nativeInstructions=0, nativeWrites=0, providerEntries=0)
    cache = {}

    def step(engine, pc, size, unused):
        trace.update(struct.pack('<I', pc))
        if pending and pc == pending[-1]['returnPc']:
            item = pending.pop()
            if engine.reg_read(UC_ARM_REG_SP) != item['entrySp']:
                raise ValueError('Native display dependency did not restore its stack')
            if 'expectedR0' in item and engine.reg_read(UC_ARM_REG_R0) != item['expectedR0']:
                raise ValueError('Native two-word span dependency result differs')
            native_returns.append(dict(address=hex(item['address']), actualReturn=True,
                                       physicalR0=hex(engine.reg_read(UC_ARM_REG_R0))))
        if pc not in cache:
            index = bisect.bisect_right(starts, pc) - 1
            if index < 0 or not ranges[index][0] <= pc < ranges[index][1]:
                raise ValueError(('Display caller escaped qualified native inventory', hex(pc)))
            cache[pc] = ranges[index]
        entry = cache[pc]
        if bool(engine.reg_read(UC_ARM_REG_CPSR) & 32) != (entry[3] == 'thumb'):
            raise ValueError('Display caller entered an incorrect native mode')
        seen.add(entry)
        if pc in PROVIDERS:
            counts['providerEntries'] += 1
            index = len(provided)
            if index >= len(calls) or calls[index][0] != pc:
                raise ValueError(('Unexpected provided display call', hex(pc), index))
            arguments = [engine.reg_read(UC_ARM_REG_R0 + n) for n in range(len(calls[index][1]))]
            if arguments != calls[index][1] or engine.reg_read(UC_ARM_REG_SP) != frame:
                raise ValueError(('Provided display arguments/stack differ', hex(pc), arguments))
            effects = []
            if pc == 0x020481B8 and index == 6 and bytes(engine.mem_read(arguments[0], 2)) != bytes(2):
                raise ValueError('Display caller did not initialize the exact two-byte zero input')
            if pc == 0x02045654:
                if bytes(engine.mem_read(0x02238F58, 1)) != bytes([3]) or bytes(engine.mem_read(0x02238F9C, 32 * 0x48)) != bytes(row) * 32:
                    raise ValueError('Native record reset/state transition did not precede display enable')
            destination = engine.reg_read(UC_ARM_REG_LR)
            for n in (0, 1, 2, 3, 12):
                engine.reg_write(UC_ARM_REG_R0 + n, randomizer.getrandbits(32))
            result = resource if pc == 0x0203CC2C else object_address if pc == 0x020462CC else opaque_result if pc == 0x02048308 else randomizer.getrandbits(32)
            engine.reg_write(UC_ARM_REG_R0, result)
            engine.reg_write(UC_ARM_REG_CPSR, randomizer.getrandbits(4) << 28 | 0x10)
            engine.reg_write(UC_ARM_REG_PC, destination)
            provided.append(dict(address=hex(pc), arguments=arguments, effects=effects, suppliedPhysicalR0=hex(result), nativeCalleeExecuted=False))
            return
        counts['nativeInstructions'] += 1
        if pc in NATIVE_ENTRIES:
            item = dict(address=pc, returnPc=engine.reg_read(UC_ARM_REG_LR), entrySp=engine.reg_read(UC_ARM_REG_SP))
            if pc in (0x0204518C, 0x02045128, 0x0204514C):
                expected_args = [frame + 4, resource, 0] if pc == 0x0204518C else [resource, 0]
                actual_args = [engine.reg_read(UC_ARM_REG_R0 + n) for n in range(len(expected_args))]
                if actual_args != expected_args:
                    raise ValueError('Native two-word span dependency arguments differ')
                item['expectedR0'] = frame + 4 if pc == 0x0204518C else payload if pc == 0x02045128 else span_length
            pending.append(item)

    def written(engine, access, address, size, value, unused):
        if not (STACK <= address < address + size <= STACK + 0x20000 or
                any(start <= address < address + size <= start + len(final) for start, final in changed)):
            raise ValueError(('Native display write outside independent effects', hex(address), size))
        counts['nativeWrites'] += 1
        writes.update(struct.pack('<IIQ', address, size, value & 0xFFFFFFFFFFFFFFFF))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(ADDRESS, STOP, count=100000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != ENTRY_SP or pending:
        raise ValueError('Native display caller did not actually return')
    if len(provided) != len(calls) or len(native_returns) != 71:
        raise ValueError(('Display dependency coverage differs', len(provided), len(native_returns)))
    if machine.reg_read(UC_ARM_REG_R0) != opaque_result:
        raise ValueError('Opaque terminal physical R0 was not preserved')
    if any(machine.reg_read(UC_ARM_REG_R0 + index) != registers[index] for index in range(4, 12)):
        raise ValueError('Display caller damaged preserved registers')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected_ram) or bytes(machine.mem_read(0x01FF8000, len(itcm))) != itcm:
        raise ValueError('Native display caller full RAM/ITCM differs from independent effects')
    return dict(actualReturn=True, physicalR0=hex(opaque_result), sourceDeclaration='void(void); original return meaning unknown', **counts,
                providerCalls=provided, nativeDependencyReturns=native_returns,
                nativeEntries=[[hex(begin), end - begin, module, mode] for begin, end, module, mode in sorted(seen)],
                registers=[machine.reg_read(UC_ARM_REG_R0 + index) for index in range(13)], cpsr=machine.reg_read(UC_ARM_REG_CPSR),
                wholeRamSha256=hashlib.sha256(ram).hexdigest(), writeTraceSha256=writes.hexdigest(),
                pcTraceSha256=trace.hexdigest(), stackSha256=hashlib.sha256(bytes(machine.mem_read(STACK, 0x20000))).hexdigest())
