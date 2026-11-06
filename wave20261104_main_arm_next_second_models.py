import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'0202841c': {}, '020284f4': {}}
SP, STOP, CAMERA0, CAMERA1, CURRENT = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x020edd0c


def fixtures(name):
    return [dict(provided=not bool(n % 2), angle=angle, ordinal=n)
            for n, angle in enumerate([0, 1, -1, 4096, -4096, 2147483647, -2147483648, 368640])]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    cameras = {}
    for index, location in enumerate([CAMERA0, CAMERA1]):
        data = bytearray((i * 17 + ordinal + index) & 255 for i in range(128))
        struct.pack_into('<I', data, 24, 0x89ab0000 + ordinal + index)
        struct.pack_into('<3I', data, 28, 0x80000000 + ordinal, 0x7fffffff - index, 0x12340000 + index)
        struct.pack_into('<3I', data, 40, 0x7fffffff - ordinal, 0x80000000 + index, 0xfffffff0 + ordinal)
        cameras[location] = data
        vm.mem_write(location, bytes(data))
    current = bytearray((i * 29 + ordinal) & 255 for i in range(16))
    struct.pack_into('<I', current, 8, CAMERA1)
    vm.mem_write(CURRENT, bytes(current))
    expected = {location: bytearray(data) for location, data in cameras.items()}
    expected[CURRENT] = bytearray(current)
    chosen = CAMERA0 if fixture['provided'] else CAMERA1
    previous = struct.unpack_from('<I', cameras[chosen], 24)[0]
    position = struct.unpack_from('<3I', cameras[chosen], 28)
    target = struct.unpack_from('<3I', cameras[chosen], 40)
    difference = [(left - right) & 0xffffffff for left, right in zip(position, target)]
    angle = fixture['angle'] & 0xffffffff
    if name == '0202841c':
        struct.pack_into('<I', expected[chosen], 24, angle)
    frame = SP - (64 if name == '0202841c' else 72)
    matrix0 = [0x11110000 + i + ordinal for i in range(9)]
    matrix1 = [0x22220000 + i + ordinal for i in range(9)]
    result_vector = [0x7fffffff - ordinal, 0x80000000 + ordinal, 0x12340000 + ordinal]
    new_target = [0x10000000 + ordinal, 0x7fffffff - ordinal, 0xfffffffe - ordinal]
    vm.mem_write(SP - 256, bytes((i * 23 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:2] = [CAMERA0 if fixture['provided'] else 0, angle]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    returned = False

    def put(location, data):
        vm.mem_write(location, data)
        for base, region in expected.items():
            if base <= location and location + len(data) <= base + len(region):
                region[location - base:location - base + len(data)] = data
                break
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def memory(uc, access, location, size, word, user):
        writes.append(dict(provider=False, address=location, size=size, value=word))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
        elif location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Original ARM matrix provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            call = dict(symbol=imports[location], address=location, words=args)
            calls.append(call)
            if location == 0x02000ce8:
                if args[0] != frame:
                    raise ValueError('Actual36-byte matrix stack boundary differs')
                at = frame + (36 if name == '0202841c' else 48)
                call['inputVectorBeforeInit'] = bytes(uc.mem_read(at, 12)).hex()
                wanted = [0, 4096, 0] if name == '0202841c' else difference
                if call['inputVectorBeforeInit'] != struct.pack('<3I', *wanted).hex():
                    failures.append('Independent pre-provider fixed up-vector or modulo32 position-target difference')
                if name == '0202841c' and struct.unpack('<I', bytes(uc.mem_read(chosen + 24, 4)))[0] != angle:
                    failures.append('Independent angle store before first provider')
                put(frame, struct.pack('<9I', *matrix0))
                put(CURRENT + 8, struct.pack('<I', CAMERA1 if chosen == CAMERA0 else CAMERA0))
                if name == '0202841c':
                    put(chosen + 24, struct.pack('<I', 0xcafe0000 + ordinal))
                else:
                    put(chosen + 28, struct.pack('<3I', 7 + ordinal, 8 + ordinal, 9 + ordinal))
            elif location in [0x020280a0, 0x02028044]:
                wanted = 0x020280a0 if name == '0202841c' else 0x02028044
                if location != wanted or args[:2] != [frame, angle]:
                    failures.append('Independent original angle and same matrix pointer forwarding')
                call['matrixBeforeUpdate'] = bytes(uc.mem_read(frame, 36)).hex()
                if call['matrixBeforeUpdate'] != struct.pack('<9I', *matrix0).hex():
                    failures.append('Independent complete matrix provider lifetime')
                put(frame, struct.pack('<9I', *matrix1))
            elif location == 0x0200103c:
                wanted = [frame + 36, frame, chosen + 52] if name == '0202841c' else [frame + 48, frame, frame + 36]
                if args[:3] != wanted:
                    raise ValueError('Original matrix/vector/output stack and object boundaries differ')
                call['inputVector'] = bytes(uc.mem_read(args[0], 12)).hex()
                call['matrix'] = bytes(uc.mem_read(args[1], 36)).hex()
                vector = [0, 4096, 0] if name == '0202841c' else difference
                if call['inputVector'] != struct.pack('<3I', *vector).hex() or call['matrix'] != struct.pack('<9I', *matrix1).hex():
                    failures.append('Independent cached vector and post-provider matrix contents')
                put(args[2], struct.pack('<3I', *result_vector))
                if name == '020284f4':
                    put(chosen + 40, struct.pack('<3I', *new_target))
                    position_after = [(left + right) & 0xffffffff for left, right in zip(new_target, result_vector)]
                    struct.pack_into('<3I', expected[chosen], 28, *position_after)
            else:
                raise ValueError('Unexpected matrix-provider boundary')
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, 0xdead0000 + ordinal)
            uc.reg_write(R.UC_ARM_REG_CPSR, ((ordinal + 7) % 16) << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native provider/body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=1000)
    if not returned:
        raise ValueError('Actual caller failed to return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Callee-saved registers/SP differ')
    wanted = [0x02000ce8, 0x020280a0 if name == '0202841c' else 0x02028044, 0x0200103c]
    if [call['address'] for call in calls] != wanted:
        failures.append('Independent complete three-provider sequence')
    if name == '0202841c' and registers[0] != previous:
        failures.append('Independent pre-provider previous-angle return despite callback mutation')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete camera/current state and post-callback target reload: ' + hex(location))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
