import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R

SPECS = {'020294cc': {}}
SP, STOP, STATE, GLOBAL, MODEL = 0x027f0000, 0x027e0000, 0x02400000, 0x020edf90, 0x02410000


def fixtures(name):
    return [dict(dirty=dirty, material=material, angle=angle)
            for dirty in [0, 1, 0x80, 0xff] for material in [0, 0xff]
            for angle in [0, -1, -2147483648, 2147483647]]


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    state = bytearray((i * 17 + ordinal) & 255 for i in range(96))
    graphics = bytearray((i * 23 + ordinal) & 255 for i in range(256))
    state[13], state[15] = fixture['material'], fixture['dirty']
    struct.pack_into('<I', state, 8, MODEL + 0x100)
    struct.pack_into('<3I', state, 40, *[(fixture['angle'] + n) & 0xffffffff for n in range(3)])
    expected = {STATE: state, GLOBAL: graphics}
    for location, region in expected.items():
        vm.mem_write(location, bytes(region))
    vm.mem_write(SP - 256, bytes((i * 29 + ordinal) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[0] = STATE
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for register, word in zip(C.REGISTERS, initial):
        vm.reg_write(register, word)
    imports = {int(binding['address'], 0): symbol for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    actions = []
    returned = False
    frame = SP - 160

    def words(values):
        return struct.pack('<' + 'I' * len(values), *[value & 0xffffffff for value in values])

    def action(location, args, mutations=(), reads=()):
        actions.append(dict(address=location, args=args, mutations=list(mutations), reads=list(reads)))
        for at, data in mutations:
            for base, region in expected.items():
                if base <= at and at + len(data) <= base + len(region):
                    region[at - base:at - base + len(data)] = data
                    break

    matrices = [words([0x11110000 * (n + 1) + i + ordinal for i in range(9)]) for n in range(6)]
    if fixture['dirty']:
        action(0x02000ce8, [frame], [(frame, matrices[0]), (STATE + 40, words([0x3100 + ordinal, 0x3200 + ordinal, 0x3300 + ordinal]))])
        action(0x020280a0, [frame + 36, 0x3300 + ordinal], [(frame + 36, matrices[1]), (STATE + 40, words([0x5100 + ordinal, 0x5200 + ordinal, 0x5300 + ordinal]))])
        action(0x02028044, [frame + 72, 0x5200 + ordinal], [(frame + 72, matrices[2]), (STATE + 40, words([0x7100 + ordinal, 0x7200 + ordinal, 0x7300 + ordinal]))])
        action(0x02027fe8, [frame + 108, 0x7100 + ordinal], [(frame + 108, matrices[3])])
        action(0x02000e1c, [frame + 72, frame + 36, frame], [(frame, matrices[4])], [(frame + 72, matrices[2]), (frame + 36, matrices[1])])
        action(0x02000e1c, [frame + 108, frame, STATE + 52], [(STATE + 52, matrices[5]), (STATE + 15, b'\xab')], [(frame + 108, matrices[3]), (frame, matrices[4])])
        expected[STATE][15] = 0
    copy = bytes(expected[STATE][52:88])
    flags_before = 0xfedcba98 | 0xa4
    action(0x02008d0c, [STATE + 52, GLOBAL + 188], [(GLOBAL + 188, copy), (GLOBAL + 252, words([flags_before])),
                                               (STATE + 16, words([0x9001, 0x9002, 0x9003])), (STATE + 28, words([0xa001, 0xa002, 0xa003]))], [(STATE + 52, copy), (STATE + 15, b'\x00')])
    struct.pack_into('<I', expected[GLOBAL], 252, flags_before & ~0xa4)
    action(0x0202e69c, [STATE + 16], [(GLOBAL + 252, words([0x11223344])), (STATE + 28, words([0xb001, 0xb002, 0xb003]))],
           [(GLOBAL + 252, words([flags_before & ~0xa4])), (STATE + 16, words([0x9001, 0x9002, 0x9003]))])
    action(0x0202e6cc, [STATE + 28], reads=[(STATE + 28, words([0xb001, 0xb002, 0xb003]))])
    action(0x0202e66c, [], [(STATE + 8, words([MODEL]))])
    commands = [(0x0202f5c8, [MODEL, 0, 0]), (0x0202f730, [MODEL, 0, 0]), (0x0202f6b8, [MODEL, 0, 1]),
                (0x0202f7a8, [MODEL, 0, 0xff]), (0x0202f640, [MODEL, 0, 3]), (0x0202dafc, [MODEL, 0, 0, 1]),
                (0x0202f730, [MODEL, 0, 1]), (0x0202f6b8, [MODEL, 0, 3]), (0x0202dafc, [MODEL, 0, 0, 1])]
    for n, (location, args) in enumerate(commands):
        mutations = [(STATE + 8, words([MODEL + 0x400 + n * 4]))]
        if n == 2:
            mutations.append((STATE + 13, b'\xff'))
        action(location, args, mutations)

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
                raise ValueError('Measured matrix/render provider entered as Thumb')
            args = [uc.reg_read(register) for register in C.REGISTERS[:4]]
            call = dict(address=location, symbol=imports[location], words=args, stack=uc.reg_read(R.UC_ARM_REG_SP))
            n = len(calls)
            calls.append(call)
            current = actions[n] if n < len(actions) else dict(address=0, args=[], mutations=[], reads=[])
            if location != current['address'] or args[:len(current['args'])] != current['args']:
                failures.append('Independent complete matrix/graphics/command order and typed argument ABI')
            for at, data in current['reads']:
                if bytes(uc.mem_read(at, len(data))) != data:
                    failures.append('Independent matrix lifetime/dirty clear/aliased graphics mask/provider reload')
            for at, data in current['mutations']:
                uc.mem_write(at, data)
                writes.append(dict(provider=True, address=at, hex=data.hex()))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, register in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(register, 0xcafe0000 + len(calls) * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, [0, 1, 0x80000000, 0xffffffff][n % 4])
            uc.reg_write(R.UC_ARM_REG_CPSR, (ordinal + len(calls)) % 16 << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('Unmodeled native provider/body execution forbidden', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=2000)
    if not returned:
        raise ValueError('Actual render caller did not return')
    registers = [vm.reg_read(register) for register in C.REGISTERS]
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual render caller callee-saved registers/SP differ')
    if registers[0] != 1 or len(calls) != len(actions):
        failures.append('Independent complete render provider sequence and literal success result')
    for location, region in expected.items():
        if bytes(vm.mem_read(location, len(region))) != region:
            failures.append('Independent complete caller state and single graphics/matrix alias union')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures, actualTopReturn=True)
