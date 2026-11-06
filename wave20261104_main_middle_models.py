import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'0204740c': {}, '02047428': {}, '0204815c': {}, '02048188': {}}
SP, STOP, INPUT = 0x027f0000, 0x027e0000, 0x02400000
GLOBALS, CURSOR, OUTPUT = 0x020fae64, 0x020fb2e4, 0x020fae64


def expected_call(opcode, cursor):
    if opcode in [0x22, 0x24]:
        return 0x02047ac0, [0 if opcode == 0x22 else 32]
    fixed = {0x28: (0, 0, 255), 0x29: (0, 1, 255), 0x2a: (2, 0, 255),
             0x2b: (1, 0, 255), 0x2c: (2, 1, 255), 0x2d: (1, 1, 255),
             0x38: (0, 0, 255), 0x39: (0, 1, 255), 0x3a: (2, 0, 255),
             0x3b: (1, 0, 255), 0x3c: (2, 1, 255), 0x3d: (1, 1, 255)}
    if opcode in fixed:
        return (0x02047b90 if opcode < 0x30 else 0x02047bfc), [OUTPUT + 2 * cursor, *fixed[opcode]]
    for start, target, kind, flag in [(0x8e, 0x02047b90, 2, 0), (0x92, 0x02047b90, 1, 0),
                                     (0x96, 0x02047b90, 2, 1), (0x9a, 0x02047b90, 1, 1),
                                     (0x9e, 0x02047bfc, 2, 0), (0xa2, 0x02047bfc, 1, 0),
                                     (0xa6, 0x02047bfc, 2, 1), (0xaa, 0x02047bfc, 1, 1)]:
        if start <= opcode < start + 4:
            return target, [OUTPUT + 2 * cursor, kind, flag, opcode - start]
    return None


def fixtures(name):
    if name == '02047428':
        result = [dict(opcode=n, cursor=42, providerReturn=0) for n in range(256)]
        for opcode in range(256):
            if expected_call(opcode, 0):
                result.extend(dict(opcode=opcode, cursor=cursor, providerReturn=returned)
                              for cursor, returned in [(0, 1), (511, 127), (65535, 254), (1, 255)])
        return result
    if name == '0204740c':
        return [dict(value=n) for n in list(range(33)) + [255, 256, 257, 32768, 65535]]
    return [dict(offset=offset, value=value, providerReturn=returned) for offset, value, returned in
            [(0, 0, 0), (1, 1, 1), (511, 255, 255), (512, 256, 0xffffffff),
             (0xffffffff, 257, 7), (0x80000000, 0xffffffff, 3), (17, 0x80000000, 0xdeadbeef), (63, 0x12345678, 2)]]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    region = bytearray((index * 17 + ordinal) & 255 for index in range(0x1000))
    struct.pack_into('<H', region, CURSOR - GLOBALS, fixture.get('cursor', 42))
    vm.mem_write(GLOBALS, bytes(region))
    input_bytes = struct.pack('<H', fixture.get('opcode', fixture.get('value', 0)) & 65535) + bytes(range(2, 32))
    vm.mem_write(INPUT, input_bytes)
    stack = bytes((index * 29 + ordinal) & 255 for index in range(512))
    vm.mem_write(SP - 256, stack)
    initial = [0x11220000 + index * 0x100 + ordinal for index in range(15)]
    initial[:4] = [INPUT, 0x12345678, 0x87654321, 0xa5a55a5a]
    if name in ['0204815c', '02048188']:
        initial[:2] = [fixture['offset'], fixture['value']]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, (ordinal % 16) << 28 | 0x10)
    for register, value in zip(C.REGISTERS, initial):
        vm.reg_write(register, value)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items()
               if binding['kind'] == 'function'}
    returned = False
    calls, writes, pcs = [], [], []

    def memory(uc, access, location, size, value, user):
        writes.append(dict(address=location, size=size, value=value))

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
            call = dict(symbol=imports[location], address=location, words=args)
            if location == 0x02047ff0:
                if args[1] not in [2, 3]:
                    raise ValueError('Unexpected marker payload extent')
                call['payload'] = bytes(uc.mem_read(args[0], args[1])).hex()
            calls.append(call)
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, fixture.get('providerReturn', 0))
            uc.reg_write(R.UC_ARM_REG_CPSR, ((ordinal + 7) % 16) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native callee/body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=1000)
    if not returned:
        raise ValueError('Actual caller failed to return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers/SP differ')
    failures = []
    if name == '02047428':
        expected = expected_call(fixture['opcode'], fixture['cursor'])
        expected_return = (2 + fixture['providerReturn']) & 255 if expected else 2
        if expected:
            target, args = expected
            if len(calls) != 1 or calls[0]['address'] != target or calls[0]['words'][:len(args)] != args:
                failures.append('Independent complete discriminator/provider/field/argument protocol')
        elif calls:
            failures.append('Default discriminator must not call a provider')
    elif name == '0204740c':
        expected_return = int(fixture['value'] in [10, 20, 21])
        if calls:
            failures.append('Halfword predicate must not call a provider')
    else:
        length = 2 if name == '0204815c' else 3
        expected_return = length
        payload = bytes([0xe3, 0x15] if length == 2 else [0xe3, 0x1c, fixture['value'] & 255]).hex()
        if len(calls) != 1 or calls[0]['address'] != 0x02047ff0 or calls[0]['words'][1:3] != [length, fixture['offset']] or calls[0].get('payload') != payload:
            failures.append('Independent stack payload, byte truncation, length and offset forwarding')
        elif not SP - 128 <= calls[0]['words'][0] < SP:
            failures.append('Marker payload is not caller stack-local')
    if registers[0] != expected_return:
        failures.append('Independent caller return and unsigned-byte wrapping')
    if bytes(vm.mem_read(GLOBALS, len(region))) != region or bytes(vm.mem_read(INPUT, len(input_bytes))) != input_bytes:
        failures.append('Caller modified input or read-only modeled global region')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
