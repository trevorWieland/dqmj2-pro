import hashlib
import json
import random
import struct
import sys
from pathlib import Path

import match_runtime as compiler
import save_link_snapshots
from link_runtime_unit import measured_module, validate
from project import ROOT, configuration, now, sha256, write_json
from recover_linked_runtime import qualified_bindings
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn import __version__ as unicorn_version
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946

ADDRESS, DESTINATION, INPUT, STACK, STOP = 0x021E6720, 0x02238D18, 0x02300100, 0x03010000, 0x07000000
SOURCE = 'src/overlays/ov001_20261029_reward_copy_fa9be2cc0322.c'
WORK = ROOT / 'work/ov001-reward-copy/20261029'


def execute(main, overlay, code, source, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    for base, size in ((0x02000000, 0x400000), (0x03000000, 0x20000), (STOP, 0x1000)):
        machine.mem_map(base, size)
    machine.mem_write(0x02000000, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ADDRESS, code)
    rng = random.Random(202610306720 + vector)
    machine.mem_write(DESTINATION - 16, rng.randbytes(35))
    machine.mem_write(INPUT, rng.randbytes(8))
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    before = bytes(machine.mem_read(0x02000000, 0x400000))
    expected = bytearray(before)
    expected_writes = []
    for index in range(3):
        value = expected[source - 0x02000000 + index]
        expected[DESTINATION - 0x02000000 + index] = value
        expected_writes.append([DESTINATION + index, 1, value])
    registers = [rng.getrandbits(32) for unused in range(13)]
    registers[0] = source
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for index, value in enumerate(registers):
        machine.reg_write(UC_ARM_REG_R0 + index, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    stack = bytes(machine.mem_read(0x03000000, 0x20000))
    writes, trace = [], []

    def step(engine, pc, size, unused):
        if not ADDRESS <= pc < ADDRESS + 32 or engine.reg_read(UC_ARM_REG_CPSR) & 32:
            raise ValueError('Reward copy escaped verified ARM instructions')
        trace.append(pc)

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda engine, access, destination, size, value, unused: writes.append([destination, size, value]))
    machine.emu_start(ADDRESS, STOP, count=100)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK + 0xFFF0:
        raise ValueError('Reward copy did not actually return')
    if machine.reg_read(UC_ARM_REG_R0) != source or any(machine.reg_read(UC_ARM_REG_R0 + i) != registers[i] for i in range(4, 13)):
        raise ValueError('Reward copy return or preserved registers differ')
    ram = bytes(machine.mem_read(0x02000000, 0x400000))
    if ram != bytes(expected) or writes != expected_writes or bytes(machine.mem_read(0x03000000, 0x20000)) != stack:
        raise ValueError('Reward copy differs from sequential forward byte/alias model')
    return {'actualReturn': True, 'sourceAddress': hex(source), 'vector': vector, 'instructions': len(trace),
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'writes': writes, 'wholeRamSha256': hashlib.sha256(ram).hexdigest(),
            'wholeStackSha256': hashlib.sha256(stack).hexdigest(), 'pcTraceSha256': compiler.sha(json.dumps(trace).encode())}


def run():
    if sys.version_info[:3] != (3, 13, 5) or unicorn_version != '2.1.4':
        raise ValueError('Pinned Python/Unicorn required')
    metadata, overlay, unused = measured_module('ov001')
    main_metadata, main, unused = measured_module('main')
    compiler.WORK = WORK / 'compiler'
    records, code = compiler.compare(ROOT / SOURCE, 'ov001', '2', 'off', True)
    if len(records) != 1 or not records[0].get('exactAfterDeclaredRelocation'):
        raise ValueError('Frozen reward copy does not match every native byte')
    entry = records[0]
    bindings = qualified_bindings(entry)
    directory = WORK / 'link' / entry['objectSha256']
    proof = validate(entry, bindings, directory)
    linked = (directory / 'caller.bin').read_bytes()
    save_link_snapshots.DIRECTORY = WORK / 'link-artifacts'
    entry.update(save_link_snapshots.freeze_link(proof))
    original = overlay[ADDRESS - 0x021D7240:ADDRESS - 0x021D7240 + entry['bytes']]
    results = []
    for vector in range(96):
        source = [INPUT, INPUT + 1, INPUT + 2, *range(DESTINATION - 4, DESTINATION + 5)][vector % 12]
        native = execute(main, overlay, original, source, vector)
        rebuilt = execute(main, overlay, linked, source, vector)
        if native != rebuilt:
            raise ValueError('Native/source reward copy machine states differ')
        results.append(native)
    entry.update(processor='arm9', sourceLanguage='C', ordinaryCBytes=entry['bytes'], justifiedAssemblyBytes=0,
                 nativeSymbolEntries=bindings, isolatedCallerLink=proof,
                 oracle={'vectors': len(results), 'executions': len(results) * 2, 'actualReturnRequired': True,
                         'freshMachinePerExecution': True, 'hostCalleeStubs': False, 'instructionBound': 100,
                         'independentSequentialForwardByteAndOverlapModel': True,
                         'wholeMappedRamAndStackCompared': True, 'results': results,
                         'limitations': ['Three-byte forward copy only; no meaning assigned to destination selectors',
                                         'Invalid/unmapped input pointers and concurrent mutation are unsupported']})
    result = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'module': 'ov001', 'processor': 'arm9', 'moduleInputSha256': metadata['sha256'],
              'mainInputSha256': main_metadata['sha256'], 'matches': [entry],
              'sourceHashes': {SOURCE: sha256(ROOT / SOURCE)}, 'generator': Path(__file__).name,
              'generatorSha256': sha256(Path(__file__)), 'nativeSymbols': {row['symbol']: row['target'] for row in entry['relocations']},
              'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    write_json(ROOT / 'evidence/matches/ov001-20261029-reward-copy01.json', result)
    print(json.dumps({'functions': 1, 'bytes': entry['bytes'], 'executions': len(results) * 2}))


if __name__ == '__main__':
    run()
