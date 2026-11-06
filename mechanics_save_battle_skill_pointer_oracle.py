import hashlib
import random
import time

from ndspy.rom import NintendoDSRom
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR

MODULE_BASE = 0x021d7240
ADDRESS = 0x021e9164
BLOCKS = 0x02238d5c
STOP = 0x027ff800

def sha(data):
    return hashlib.sha256(data).hexdigest()

def validate(module, save, matches, root):
    overlays = NintendoDSRom((root / 'inputs/game.nds').read_bytes()).loadArm9Overlays()
    target = bytes(overlays[1].data)
    if target != module or overlays[1].ramAddress != MODULE_BASE:
        raise AssertionError('Battle skill getter module identity differs')
    conflicting = []
    for identity in (0, 6):
        other = overlays[identity]
        offset = ADDRESS - other.ramAddress
        span = bytes(other.data[offset:offset + 20])
        if span == module[ADDRESS - MODULE_BASE:ADDRESS - MODULE_BASE + 20]:
            raise AssertionError('Cross-overlay negative control unexpectedly identical')
        conflicting.append({'module': f'ov{identity:03}', 'moduleSha256': sha(other.data), 'address': hex(ADDRESS), 'spanSha256': sha(span), 'rejectedAsThisGetter': True})
    machines = []
    for rebuilt in (False, True):
        machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
        machine.mem_map(0x02000000, 0x800000)
        machine.mem_write(MODULE_BASE, module)
        if rebuilt:
            for row, code in matches.values():
                if row['module'] != 'ov001':
                    raise AssertionError('Battle getter module qualifier differs')
                machine.mem_write(int(row['address'], 16), code)
        machines.append(machine)
    rng = random.Random(20261027)
    vectors = [*range(-3, 9), 127, 255, 65535, -0x80000000, 0x7fffffff]
    vectors += [rng.randint(-0x80000000, 0x7fffffff) for _ in range(1024)]
    guard = rng.randbytes(0x1000)
    cases = calls = 0
    for index in vectors:
        expected = (BLOCKS + index * 10) & 0xffffffff
        for machine in machines:
            machine.mem_write(0x02238000, guard)
            machine.reg_write(UC_ARM_REG_R0, index & 0xffffffff)
            machine.reg_write(UC_ARM_REG_SP, 0x027ff000)
            machine.reg_write(UC_ARM_REG_LR, STOP)
            began = time.monotonic()
            machine.emu_start(ADDRESS, STOP, count=5000)
            if time.monotonic() - began > 1 or machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != 0x027ff000:
                raise AssertionError('Battle skill pointer bounds/stack differs')
            if machine.reg_read(UC_ARM_REG_R0) != expected or bytes(machine.mem_read(0x02238000, len(guard))) != guard:
                raise AssertionError(('Battle pointer/guard differs', index))
            calls += 1
        cases += 1
    return {'engine': 'Unicorn', 'cases': cases, 'nativeAndRecompiledCalls': calls, 'testedFunctions': list(matches), 'instructionLimitPerCall': 5000, 'elapsedSecondsLimit': 1, 'returnPcAndStackVerified': True, 'independentExpectedPointerAndReadOnlyGuard': True, 'platformStubs': {}, 'module': 'ov001', 'moduleSha256': sha(module), 'sameRamOtherModules': conflicting, 'observations': ['Qualified ov001 getter returns02238D5C + index*10 without loading saved skill bytes or performing an index guard.', 'The same RAM address021E9164 contains unrelated code in ov000 and ov006; neither image is accepted for this getter.', 'Main020650C0/020650DC invoke this RAM address with an index; the connected mode1 fixture must explicitly load ov001.'], 'limitations': ['Valid index bounds and complete overlay-load transitions remain unestablished; negative/overflow pointer values are isolated ARM probes.', 'No field meanings, availability or ownership are inferred from the returned pointer.', 'No original ROM/save/overlay file is modified and no full emulator is executed.']}
