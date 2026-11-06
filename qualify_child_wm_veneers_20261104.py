from pathlib import Path
import random
import struct
from project import ROOT, configuration, native_dependencies, read_json, write_json, sha256


PROGRAM = 'dwc/utility.bin/move/child.srl'
MODULE = 'utility-child-arm7-main'
IMAGE = 'extract/utility/runtime/utility-child-arm7-main.bin'
INVENTORY = 'evidence/utility/ghidra-arm7.json'
IMAGE_SHA = 'a5838c09ff9e04d2ffbdf780b3d1bbd5b5875dda9f2ea7d7f8eed74a60d1920a'
CASES = [dict(entry=0x027E10C8, target=0x027E1038, caller=0x027E10D4, extent=624, offset=620,
              body='00c09fe51cff2fe138107e02', truncate=False),
         dict(entry=0x027E1830, target=0x027E17A8, caller=0x027E18C4, extent=872, offset=868,
              body='0008a0e12008a0e100c09fe51cff2fe1a8177e02', truncate=True)]


def qualify(entry, program=PROGRAM, processor='arm7', module=MODULE, mode='arm', data=None, inventory=None):
    if (program, processor, module, mode) != (PROGRAM, 'arm7', MODULE, 'arm'):
        raise ValueError('Veneer namespace or ARM mode differs')
    case = next((row for row in CASES if row['entry'] == entry), None)
    if case is None:
        raise ValueError('Unqualified callback entry')
    data = (ROOT / IMAGE).read_bytes() if data is None else data
    inventory = read_json(ROOT / INVENTORY) if inventory is None else inventory
    if (inventory['program'], inventory['processor']) != (PROGRAM, 'arm7'):
        raise ValueError('Target inventory namespace differs')
    offset = entry - 0x027E0000
    body = bytes.fromhex(case['body'])
    if data[offset:offset + len(body)] != body:
        raise ValueError('Original veneer instructions or literal differ')
    pointer = struct.unpack_from('<I', data, case['caller'] - 0x027E0000 + case['offset'])[0]
    if pointer != entry or case['offset'] + 4 != case['extent']:
        raise ValueError('Measured original caller pointer or complete extent differs')
    target = next((row for row in inventory['functions'] if int(row['address'], 0) == case['target']), None)
    if target is None or (target['module'], target['processor'], target['mode']) != (MODULE, 'arm7', 'arm'):
        raise ValueError('Veneer destination lacks canonical same-program ARM entry')
    return dict(case, targetInventoryEntry=target['address'], targetInventoryBodyBytes=target['bodyBytes'],
        veneerBytes=len(body), sourceCredit=0, calleeSourceCredit=0)


def main():
    config = configuration()
    native_dependencies(config)
    import unicorn as un
    from unicorn import arm_const as ar
    assert sha256(ROOT / IMAGE) == IMAGE_SHA
    data = (ROOT / IMAGE).read_bytes()
    inventory = read_json(ROOT / INVENTORY)
    regs = [getattr(ar, 'UC_ARM_REG_R' + str(index)) for index in range(13)] + [ar.UC_ARM_REG_SP, ar.UC_ARM_REG_LR]
    rng = random.Random(0x20261104)
    values = [0, 1, 0xffff, 0x10000, 0x10001, 0x7fffffff, 0x80000000, 0xffffffff]
    values += [1 << bit for bit in range(32)] + [rng.getrandbits(32) for _ in range(24)]
    proofs = []
    for case in CASES:
        qualified = qualify(case['entry'], data=data, inventory=inventory)
        reached = 0
        for value in values:
            for flags in [0, 0x20000000, 0x60000000, 0xF0000000]:
                cpu = un.Uc(un.UC_ARCH_ARM, un.UC_MODE_ARM | un.UC_MODE_LITTLE_ENDIAN)
                cpu.mem_map(0x027E0000, (len(data) + 0xFFF) & ~0xFFF)
                cpu.mem_write(0x027E0000, data)
                initial = [rng.getrandbits(32) for _ in regs]
                initial[0], initial[13], initial[14] = value, 0x02010000, 0x02002000
                cpu.reg_write(ar.UC_ARM_REG_CPSR, flags | 0x10)
                for reg, current in zip(regs, initial):
                    cpu.reg_write(reg, current)
                pcs, reads, writes = [], [], []

                def code_hook(machine, address, size, user):
                    pcs.append(address)
                    if address == case['target']:
                        machine.emu_stop()
                    elif address not in range(case['entry'], case['entry'] + qualified['veneerBytes'] - 4, 4):
                        raise AssertionError('Execution escaped measured veneer')

                cpu.hook_add(un.UC_HOOK_CODE, code_hook)
                cpu.hook_add(un.UC_HOOK_MEM_READ, lambda machine, access, address, size, value, user: reads.append((address, size)))
                cpu.hook_add(un.UC_HOOK_MEM_WRITE, lambda machine, access, address, size, value, user: writes.append((address, size)))
                cpu.emu_start(case['entry'], 0, count=8)
                expected = list(initial)
                expected[0] = value & 0xFFFF if case['truncate'] else value
                expected[12] = case['target']
                assert [cpu.reg_read(reg) for reg in regs] == expected
                assert cpu.reg_read(ar.UC_ARM_REG_CPSR) == flags | 0x10
                assert cpu.reg_read(ar.UC_ARM_REG_PC) == case['target'] and pcs[-1] == case['target']
                assert len(pcs) == (5 if case['truncate'] else 3)
                assert reads == [(case['entry'] + qualified['veneerBytes'] - 4, 4)] and not writes
                assert bytes(cpu.mem_read(0x027E0000, len(data))) == data
                reached += 1
        proofs.append(dict(qualified, actualVeneerTransfers=reached, calleeInstructionsExecuted=0,
            nativeCallerExecutions=0, nativeFunctionReturns=0, registersAndCpsrPreservedExceptDeclared=True,
            originalMemoryUnchanged=True))
    controls = []

    def reject(name, **kwargs):
        try:
            qualify(**kwargs)
        except ValueError:
            controls.append(dict(name=name, rejected=True))
        else:
            raise AssertionError('Invalid veneer qualification accepted: ' + name)

    for key, value in [('program', 'other'), ('processor', 'arm9'), ('module', 'arm7-main'), ('mode', 'thumb')]:
        reject('wrong-' + key, entry=CASES[0]['entry'], **{key: value})
    reject('unmeasured-interior-entry', entry=CASES[0]['entry'] + 4)
    for case in CASES:
        for label, offset in [('instruction', case['entry'] - 0x027E0000),
                              ('literal', case['entry'] - 0x027E0000 + len(bytes.fromhex(case['body'])) - 4),
                              ('caller-pointer', case['caller'] - 0x027E0000 + case['offset'])]:
            changed = bytearray(data)
            changed[offset] ^= 1
            reject(hex(case['entry']) + '-changed-' + label, entry=case['entry'], data=bytes(changed))
    changed = dict(inventory, functions=[row for row in inventory['functions'] if int(row['address'], 0) != CASES[0]['target']])
    reject('missing-canonical-destination', entry=CASES[0]['entry'], inventory=changed)
    output = ROOT / 'evidence/lanes/parallel-wave20261104/child-wm-veneer-qualification.json'
    write_json(output, dict(passed=True, sourceCredit=0, romSha256=config['romSha256'],
        generator=Path(__file__).name, generatorSha256=sha256(__file__),
        image=dict(path=IMAGE, sha256=IMAGE_SHA), inventory=dict(path=INVENTORY, sha256=sha256(ROOT / INVENTORY)),
        entries=proofs, controls=controls, originalInputsOrAcceptedSourcesChanged=False,
        limitation='Measured callback veneer entry qualification only; no veneer source, caller behavior, destination execution or callee reconstruction credit'))
    print(dict(passed=True, entries=len(proofs), transfers=sum(row['actualVeneerTransfers'] for row in proofs), controls=len(controls)))


if __name__ == '__main__':
    main()
