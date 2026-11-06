import hashlib
import random
from project import ROOT, read_json, write_json, configuration, native_dependencies, sha256
native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_CPU_ARM_946, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_ARM_REG_SP, UC_ARM_REG_LR
from match_runtime import REGISTERS
from link_runtime_unit import measured_module

STACK, STOP = 0x03030000, 0x0F000000
SP = STACK + 0x800


def execute(main, caller, target, code, count, tag):
    rng = random.Random(0xF047000 + tag)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(0x02000000, 0x400000)
    machine.mem_write(0x02000000, main)
    machine.mem_write(caller, code)
    machine.mem_map(STACK, 4096)
    machine.mem_map(STOP, 4096)
    stack = rng.randbytes(4096)
    machine.mem_write(STACK, stack)
    machine.reg_write(UC_ARM_REG_CPSR, ((tag & 15) << 28) | 0x1F)
    for reg in REGISTERS:
        machine.reg_write(reg, rng.getrandbits(32))
    values = [rng.getrandbits(32) for _ in range(4)]
    edges = [0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF]
    if tag % 32 < 5:
        values = [edges[(tag + index) % 5] for index in range(4)]
    for reg, value in zip(REGISTERS[:4], values):
        machine.reg_write(reg, value)
    machine.reg_write(UC_ARM_REG_SP, SP)
    machine.reg_write(UC_ARM_REG_LR, STOP | (tag & 1))
    saved = [machine.reg_read(reg) for reg in REGISTERS[4:12]]
    expected_return = rng.getrandbits(32)
    state = dict(actualOuterReturns=0, suppliedCalleeCompletions=0, instructions=0)
    observed = []

    def step(uc, pc, width, user):
        state['instructions'] += 1
        if pc == STOP:
            state['actualOuterReturns'] += 1
            uc.emu_stop()
            return
        assert width == 4 and not uc.reg_read(UC_ARM_REG_CPSR) & 32
        if caller <= pc < caller + len(code):
            return
        assert pc == target and not observed
        args = [uc.reg_read(reg) for reg in REGISTERS[:count]]
        assert args == values[:count]
        observed.append(args)
        for index in [1, 2, 3, 12]:
            uc.reg_write(REGISTERS[index], rng.getrandbits(32))
        uc.reg_write(REGISTERS[0], expected_return)
        uc.reg_write(UC_ARM_REG_CPSR, (((tag * 3) & 15) << 28) | 0x1F)
        uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        state['suppliedCalleeCompletions'] += 1

    def write(uc, access, address, size, value, user):
        assert SP - 8 <= address and address + size <= SP

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.emu_start(caller, STOP + 4, count=32)
    assert state['actualOuterReturns'] == 1 and state['suppliedCalleeCompletions'] == 1
    assert machine.reg_read(REGISTERS[0]) == expected_return and machine.reg_read(UC_ARM_REG_SP) == SP
    assert [machine.reg_read(reg) for reg in REGISTERS[4:12]] == saved
    final_stack = bytes(machine.mem_read(STACK, 4096))
    assert final_stack[:0x7F8] == stack[:0x7F8] and final_stack[0x800:] == stack[0x800:]
    return dict(state=state, forwarded=observed, registers=[machine.reg_read(reg) for reg in REGISTERS] +
        [machine.reg_read(UC_ARM_REG_CPSR)], stackSha256=hashlib.sha256(final_stack).hexdigest())


def main():
    profile_path = ROOT / 'evidence/attempts/forwarded-interfaces-20261031.json'
    profile = read_json(profile_path)
    _, original, _ = measured_module('main')
    results = []
    for index, row in enumerate(profile['candidates']):
        compiled = row['compiled']
        assert compiled.get('exactAfterRealMwLink')
        caller, target = row['previous']['address'], row['callee']['address']
        source = ROOT / compiled['source']
        assert sha256(source) == compiled['sourceSha256']
        payload_path = ROOT / f'work/forwarded-interfaces-20261031/linked/{row["previous"]["name"]}/caller.bin'
        payload = payload_path.read_bytes()
        native = original[caller - 0x02000000:caller - 0x02000000 + 12]
        assert payload == native and len(payload) == 12
        count = len(row['parameterView'].split(','))
        for tag in range(32):
            a = execute(original, caller, target, native, count, index * 32 + tag)
            b = execute(original, caller, target, payload, count, index * 32 + tag)
            assert a == b
        results.append(dict(caller=row['previous'], callee=row['callee'], source=compiled['source'],
            sourceSha256=compiled['sourceSha256'], pairs=32, actualOuterReturns=64,
            suppliedCalleeCompletions=64, nativeCalleeBodyReturns=0, verifiedReturn=True, isolatedState=True))
    write_json(ROOT / 'evidence/verification/forwarded-interfaces-native-20261031.json', dict(
        profile=profile_path.relative_to(ROOT).as_posix(), profileSha256=sha256(profile_path), results=results,
        actualOuterReturns=64 * len(results), suppliedCalleeCompletions=64 * len(results), sourceCredit=0,
        registered=False, generator='prove_forwarded_interfaces_20261031.py', generatorSha256=sha256(__file__),
        limitations=['Caller forwarding contract only; each complete target body is an explicit supplied boundary',
            'Raw pointer words are forwarded without dereference or a valid-object claim',
            'No source-interface migration is published by this proof; full acceptance and source-language controls remain separate']))
    print(dict(typedCandidates=len(results), actualOuterReturns=64 * len(results), sourceCredit=0))


if __name__ == '__main__':
    main()
