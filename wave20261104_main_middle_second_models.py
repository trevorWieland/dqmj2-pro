import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'02047ac0': {}, '0204837c': {}, '020483c0': {}}
SP, STOP, TEXT, RECORDS = 0x027f0000, 0x027e0000, 0x020fb264, 0x020fbae8


def fixtures(name):
    if name != '02047ac0':
        return [dict(record=record, seed=seed) for record, seed in [(0, 1), (1, 255), (2, 17), (3, 63)]]
    result = [dict(start=start, text={}, providers=[]) for start in [128, 255, 256, 0xffffffff]]
    scenarios = [(0, {}, []), (0, {0: 0xe3, 1: 0x1b}, []),
                 (127, {127: 0xe3, 128: 0x1b}, []),
                 (0, {0: 65, 1: 66}, [(0x02046e68, 0, 1), (0x02046e68, 1, 1)]),
                 (0, {0: 0xe3, 1: 0x15}, [(0x02046fc8, None, 2)]),
                 (0, {0: 0xe3, 1: 0x1c, 2: 255}, [(0x02047018, 255, 3)]),
                 (0, {0: 0xe3, 1: 0x99}, [(0x02046e68, 0, 2)]),
                 (127, {127: 0xe3, 128: 0x15}, [(0x02046fc8, None, 1)]),
                 (127, {0: 65, 127: 0xe3, 128: 0x1c, 129: 17}, [(0x02047018, 17, 129), (0x02046e68, 0, 1)]),
                 (127, {127: 65}, [(0x02046e68, 127, 0xffffffff)]),
                 (127, {127: 0xe3, 128: 0x15}, [(0x02046fc8, None, 257)])]
    for start, text, providers in scenarios:
        result.append(dict(start=start, text=text, providers=[dict(address=a, argument=arg, returned=returned) for a, arg, returned in providers]))
    result.append(dict(start=127, text={127: 65}, providers=[dict(address=0x02046e68, argument=127, returned=0, mutateAt=127)]))
    return result


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    text = bytearray(132)
    for at, value in fixture.get('text', {}).items():
        text[int(at)] = value
    vm.mem_write(TEXT, bytes(text))
    region = bytearray((index * 17 + fixture.get('seed', 1)) & 255 for index in range(4 * 0x3744))
    vm.mem_write(RECORDS, bytes(region))
    initial = [0x11220000 + index * 0x100 + ordinal for index in range(15)]
    initial[0] = fixture.get('start', fixture.get('record', 0))
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, (ordinal % 16) << 28 | 0x10)
    for register, value in zip(C.REGISTERS, initial):
        vm.reg_write(register, value)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    returned = False
    expected_text = bytearray(text)

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Original ARM provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            index = len(calls)
            call = dict(symbol=imports[location], address=location, words=args)
            calls.append(call)
            expected = fixture.get('providers', [])
            if index >= len(expected):
                raise ValueError('Unexpected provider would leave finite model domain')
            item = expected[index]
            argument = item['argument']
            if location != item['address'] or argument is not None and args[0] != (TEXT + argument if item['address'] == 0x02046e68 else argument):
                failures.append('Independent full text-provider sequence/byte/pointer argument')
            if 'mutateAt' in item:
                at = item['mutateAt']
                expected_text[at] = 0
                uc.mem_write(TEXT + at, b'\0')
                writes.append(dict(provider=True, address=TEXT + at, hex='00'))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, item['returned'])
            uc.reg_write(R.UC_ARM_REG_CPSR, ((ordinal + 7) % 16) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=5000)
    if not returned:
        raise ValueError('Actual native/source caller failed to return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers/SP differ')
    expected_region = bytearray(region)
    if name == '02047ac0':
        if registers[0] != 0 or len(calls) != len(fixture['providers']):
            failures.append('Independent zero return and complete text-provider sequence')
    else:
        offset = fixture['record'] * 0x3744 + 0x3544
        expected_region[offset:offset + 512] = bytes(512)
        if calls:
            failures.append('Record clear must execute no provider')
        stores = [write for write in writes if RECORDS <= write['address'] < RECORDS + len(region)]
        if len(stores) != 128 or any(write['size'] != 4 or write['value'] != 0 or write['address'] != RECORDS + offset + 4 * index for index, write in enumerate(stores)):
            failures.append('Independent exactly128 ascending zero word stores in selected record')
    if bytes(vm.mem_read(RECORDS, len(region))) != expected_region:
        failures.append('Independent full record region, selected field bounds and stride')
    if bytes(vm.mem_read(TEXT, len(text))) != expected_text:
        failures.append('Independent text prefix, prescribed provider mutation and guard bytes')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
