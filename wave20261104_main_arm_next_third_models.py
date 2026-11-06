import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'0202882c': {}, '020289cc': {}}
SP, STOP, OUTPUT, RESOURCE, TEXTURE, MODEL = 0x027f0000, 0x027e0000, 0x02400000, 0x02401000, 0x02402000, 0x02403000
TEXSLOT, PALSLOT = 0x020dd8c0, 0x020dd8b8
DEFAULTS = [0x0203c05c, 0x0203c04c]


def fixtures(name):
    if name == '020289cc':
        return [dict(signature=signature, mode=mode, parsed=parsed, texture=texture)
                for signature, mode, parsed, texture in [(0, 0, 1, 1), (0x30585442, 1, 1, 1)] +
                [(0x30444d42, mode, parsed, texture) for mode in [0, 1, 0x80000000]
                 for parsed, texture in [(0, 1), (1, 0), (0x80000000, 1)]]]
    result = [dict(signature=signature, texture=texture, sizes=[17, 33, 49], failed=0, flags=0xffff, model=1, reassign=False)
              for signature, texture in [(0, 1), (0x30444d42, 0)]]
    result += [dict(signature=0x30585442 if n % 2 else 0x30444d42, texture=1,
                    sizes=[17 if n & 1 else 0, 33 if n & 2 else 0, 49 if n & 4 else 0],
                    failed=failed, flags=0x7fff if n % 2 else 0xffff, model=n % 3 != 0, reassign=bool(n & 2))
               for n in range(8) for failed in [0, n]]
    result += [dict(signature=0x30444d42, texture=1, sizes=[0x80000001, 0x7fffffff, 0xffffffff],
                    failed=failed, flags=0xffff, model=model, reassign=True)
               for failed in range(8) for model in [0, 1]]
    return result


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    name = format(address, '08x')
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    initial_context = bytearray((i * 17 + ordinal) & 255 for i in range(96))
    header = bytearray((i * 29 + ordinal) & 255 for i in range(32))
    texture = bytearray((i * 23 + ordinal) & 255 for i in range(64))
    struct.pack_into('<I', header, 0, fixture['signature'])
    struct.pack_into('<H', texture, 32, fixture.get('flags', 0xffff))
    expected = {OUTPUT: bytearray(initial_context), RESOURCE: header, TEXTURE: texture,
                TEXSLOT: bytearray(struct.pack('<I', DEFAULTS[0])), PALSLOT: bytearray(struct.pack('<I', DEFAULTS[1]))}
    for location, region in expected.items():
        vm.mem_write(location, bytes(region))
    vm.mem_write(SP - 256, bytes((i * 31 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[:3] = [OUTPUT, RESOURCE, fixture.get('mode', 0)]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    imports.update({target: 'modeled-default-callable' for target in DEFAULTS})
    calls, writes, pcs, failures = [], [], [], []
    returned = False
    sizes = fixture.get('sizes', [0, 0, 0])
    keys = [0 if not size or fixture.get('failed', 0) & (1 << n) else 0x80001001 + n * 0x10000 + ordinal for n, size in enumerate(sizes)]
    wanted = []
    result = 0

    def put(location, data):
        vm.mem_write(location, data)
        for base, region in expected.items():
            if base <= location and location + len(data) <= base + len(region):
                region[location - base:location - base + len(data)] = data
                break
        writes.append(dict(provider=True, address=location, hex=data.hex()))

    def word(location, value):
        put(location, struct.pack('<I', value))

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))

    def code(uc, location, size, user):
        nonlocal returned
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
            return
        if location in imports:
            if uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                raise ValueError('Measured resource provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            call = dict(address=location, symbol=imports[location], words=args, returnAddress=lr)
            calls.append(call)
            returned_word = 0xcafe0000 + ordinal
            if name == '020289cc':
                if location in [0x02031fa4, 0x0202882c]:
                    wanted_args = [RESOURCE] if fixture['mode'] else [OUTPUT, RESOURCE]
                    if args[:len(wanted_args)] != wanted_args:
                        failures.append('Independent parser pointer/mode ABI')
                    put(OUTPUT + 0x38, b'\xa4\x76')
                    returned_word = fixture['parsed']
                elif location == 0x0202beec:
                    if args[0] != RESOURCE or bytes(uc.mem_read(OUTPUT, 4)) != struct.pack('<I', RESOURCE):
                        failures.append('Resource pointer committed before query provider')
                    word(OUTPUT, 0x02404000)
                    put(OUTPUT + 0x38, b'\xf2\x99')
                    returned_word = TEXTURE if fixture['texture'] else 0
                else:
                    raise ValueError('Unexpected parser/query boundary')
            else:
                if location == 0x0202beec:
                    if args[0] != RESOURCE or bytes(uc.mem_read(OUTPUT + 0x4c, 12)) != bytes(12):
                        failures.append('All three sizes cleared before resource provider')
                    word(RESOURCE, 0xfeed0000 + ordinal)
                    returned_word = TEXTURE if fixture['texture'] else 0
                elif location in [0x0202ec30, 0x0202ec44, 0x0202ed70]:
                    stage = [0x0202ec30, 0x0202ec44, 0x0202ed70].index(location)
                    if args[0] != TEXTURE:
                        failures.append('Independent texture size-provider pointer')
                    returned_word = sizes[stage]
                elif location in DEFAULTS:
                    stages = [n for n, requested in enumerate(sizes) if requested]
                    index = sum('allocationStage' in prior for prior in calls[:-1])
                    if index >= len(stages):
                        raise ValueError('Extra unexpected indirect allocation boundary')
                    stage = stages[index]
                    if row['realLink']['exactCallerBytes'] and lr - address != [164, 208, 256][stage]:
                        raise ValueError('Exact caller indirect allocation return site differs')
                    palette_flag = struct.unpack_from('<H', expected[TEXTURE], 32)[0] & 0x8000
                    wanted_args = [sizes[stage], [0, 1, palette_flag][stage], 0]
                    target = DEFAULTS[1] if stage == 2 or stage == 1 and fixture['reassign'] and sizes[0] else DEFAULTS[0]
                    if args[:3] != wanted_args or location != target:
                        failures.append('Independent callback size/raw flag/zero argument/reloaded slot target')
                    if stage == 0 and fixture['reassign']:
                        word(TEXSLOT, DEFAULTS[1])
                    put(TEXTURE + 32, struct.pack('<H', fixture['flags'] ^ 0x8000))
                    returned_word = keys[stage]
                    call['allocationStage'] = stage
                elif location in [0x0202ec58, 0x0202ed84]:
                    wanted_args = [TEXTURE, keys[0], keys[1]] if location == 0x0202ec58 else [TEXTURE, keys[2]]
                    if args[:len(wanted_args)] != wanted_args:
                        failures.append('Independent cached texture allocation keys')
                    if bytes(uc.mem_read(OUTPUT + 0x3c, 16)) != initial_context[0x3c:0x4c]:
                        failures.append('No output key/texture commit before bind providers')
                    put(OUTPUT + 4, b'\x93')
                elif location == 0x0202bedc:
                    if args[0] != RESOURCE or bytes(uc.mem_read(OUTPUT + 0x3c, 28)) != struct.pack('<7I', TEXTURE, *keys, *sizes):
                        failures.append('Texture/keys/sizes committed before captured-BMD model lookup')
                    returned_word = MODEL if fixture['model'] else 0
                elif location == 0x0202f3dc:
                    if args[:2] != [MODEL, TEXTURE]:
                        failures.append('Independent model/texture binding pointer ABI')
                else:
                    raise ValueError('Unexpected texture resource provider')
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, returned_word)
            uc.reg_write(R.UC_ARM_REG_CPSR, (ordinal + len(calls)) % 16 << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native provider/body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=1500)
    if not returned:
        raise ValueError('Actual resource caller did not return')
    if name == '020289cc':
        if fixture['signature'] == 0x30444d42:
            wanted = [0x02031fa4 if fixture['mode'] else 0x0202882c]
            if fixture['parsed']:
                wanted += [0x0202beec]
                expected[OUTPUT][4] = int(bool(fixture['texture']))
                expected[OUTPUT][0x38] |= 1
                expected[OUTPUT][0x39] = 1
                result = 1
    else:
        expected[OUTPUT][0x4c:0x58] = bytes(12)
        if fixture['signature'] in [0x30444d42, 0x30585442]:
            wanted = [0x0202beec]
            if fixture['texture']:
                wanted += [0x0202ec30, 0x0202ec44, 0x0202ed70]
                for n, size in enumerate(sizes):
                    if size:
                        wanted += [DEFAULTS[1] if n == 2 or n == 1 and fixture['reassign'] and sizes[0] else DEFAULTS[0]]
                if all(not size or keys[n] for n, size in enumerate(sizes)):
                    wanted += [0x0202ec58, 0x0202ed84]
                    struct.pack_into('<7I', expected[OUTPUT], 0x3c, TEXTURE, *keys, *sizes)
                    result = 1
                    if fixture['signature'] == 0x30444d42:
                        wanted += [0x0202bedc]
                        if fixture['model']:
                            wanted += [0x0202f3dc]
                        else:
                            result = 0
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual resource caller callee-saved registers/SP differ')
    if registers[0] != result or [call['address'] for call in calls] != wanted:
        failures.append('Independent complete provider sequence and resource result')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete resource/header/texture/slot state: ' + hex(location))
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
