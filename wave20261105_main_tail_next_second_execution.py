import struct
import match_runtime as C
import unicorn
from unicorn import arm_const as R
from wave20261105_main_tail_next_second_models import SP, STOP, POSITION, DESCRIPTOR, scenario


def run(row, body, fixture, main, ordinal=0):
    address = int(row['address'], 0)
    plan = scenario(fixture)
    vm = unicorn.Uc(unicorn.UC_ARCH_ARM, unicorn.UC_MODE_ARM)
    vm.ctl_set_cpu_model(R.UC_CPU_ARM_946)
    vm.mem_map(0x02000000, 0x800000)
    vm.mem_write(0x02000000, main)
    vm.mem_write(address, body)
    for base, raw in plan['initial'].items():
        vm.mem_write(base, raw)
    vm.mem_write(SP - 256, bytes((i * 31 + ordinal * 7) & 255 for i in range(512)))
    initial = [0x11220000 + i * 0x100 + ordinal for i in range(15)]
    initial[-2:] = [SP, STOP]
    vm.reg_write(R.UC_ARM_REG_CPSR, ordinal % 16 << 28 | 0x10)
    for reg, word in zip(C.REGISTERS, initial):
        vm.reg_write(reg, word)
    imports = {int(binding['address'], 0): (symbol, binding) for symbol, binding in row['nativeSymbolEntries'].items() if binding['kind'] == 'function'}
    calls, writes, pcs, failures = [], [], [], []
    returned, rejected = False, False

    def memory(uc, access, location, size, value, user):
        writes.append(dict(provider=False, address=location, size=size, value=value))
        if not SP - 64 <= location or not location + size <= SP:
            failures.append('Caller wrote outside its measured64-byte frame')

    def code(uc, location, size, user):
        nonlocal returned, rejected
        pcs.append(location)
        if location == STOP:
            returned = True
            uc.emu_stop()
            return
        if location in imports:
            symbol, binding = imports[location]
            n = len(calls)
            action = plan['actions'][n] if n < len(plan['actions']) else dict(address=0, args=[], checks=[], mutations=[], returned=0)
            count = len(action['args'])
            actual = [uc.reg_read(reg) for reg in C.REGISTERS[:min(4, count)]]
            frame = uc.reg_read(R.UC_ARM_REG_SP)
            if count > 4:
                actual += list(struct.unpack('<' + 'I' * (count - 4), bytes(uc.mem_read(frame, 4 * (count - 4)))))
            calls.append(dict(symbol=symbol, address=location, arguments=actual, program=binding.get('program') or '', processor=binding['processor'], module=binding['module'], mode=binding['mode']))
            if location != action['address'] or actual != action['args'] or uc.reg_read(R.UC_ARM_REG_CPSR) & 32:
                failures.append('Independent ordered widget/format/draw/numeric/state provider addresses and all observed ABI words')
                rejected = True
                uc.emu_stop()
                return
            for at, raw in action['checks']:
                if bytes(uc.mem_read(at, len(raw))) != raw:
                    failures.append('Independent initial Vec2, aliased text16, bounded UTF16 descriptor32 or provider-position persistence differs')
            for at, raw in action['mutations']:
                uc.mem_write(at, raw)
                writes.append(dict(provider=True, address=at, hex=raw.hex()))
            lr = uc.reg_read(R.UC_ARM_REG_LR)
            for index, reg in enumerate(C.REGISTERS[:4] + [R.UC_ARM_REG_R12]):
                uc.reg_write(reg, 0xcafe0000 + n * 16 + index)
            uc.reg_write(R.UC_ARM_REG_R0, action['returned'])
            uc.reg_write(R.UC_ARM_REG_CPSR, (ordinal + n) % 16 << 28 | 0x10)
            uc.reg_write(R.UC_ARM_REG_PC, lr)
        elif not address <= location < address + len(body):
            raise ValueError(('No actual widget/formatter/game/SDK body execution authorized', hex(location)))

    vm.hook_add(unicorn.UC_HOOK_CODE, code)
    vm.hook_add(unicorn.UC_HOOK_MEM_WRITE, memory)
    vm.emu_start(address, STOP + 4, count=12000)
    registers = [vm.reg_read(reg) for reg in C.REGISTERS]
    if not returned:
        if not rejected:
            raise ValueError('Actual summary caller did not return')
        return dict(modelFailures=failures, actualTopReturn=False, rejectedAtObservedProtocolBoundary=True, calls=calls)
    if registers[4:12] != initial[4:12] or registers[13] != SP:
        raise ValueError('Actual summary caller callee-saved registers/SP differ')
    if registers[0] != plan['result'] or len(calls) != len(plan['actions']):
        failures.append('Independent final full-word provider result or complete callback count differs')
    for base, raw in plan['regions'].items():
        if bytes(vm.mem_read(base, len(raw))) != raw:
            failures.append('Independent complete unified summary/text alias, widget handles/objects or padding differs')
    if bytes(vm.mem_read(POSITION, 4)) != plan['position'] or bytes(vm.mem_read(DESCRIPTOR, 32)) != plan['descriptor']:
        failures.append('Independent full live local position/descriptor provider mutations differ')
    return dict(registers=registers, cpsr=vm.reg_read(R.UC_ARM_REG_CPSR), calls=calls, writes=writes, pcs=pcs,
                ramSha256=C.sha(bytes(vm.mem_read(0x02000000, 0x800000))), modelFailures=failures,
                actualTopReturn=True, rejectedAtObservedProtocolBoundary=False)
