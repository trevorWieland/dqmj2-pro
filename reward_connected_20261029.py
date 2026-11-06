import json
import random
import struct
import sys
from project import ROOT, configuration, native_dependencies, now, read_json, sha256, write_json

native_dependencies(configuration())
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR, UC_CPU_ARM_946
from link_runtime_unit import measured_module
from reward_state_fixture_20261029 import BASE, ENTRY, CONTEXT, MARKER, ITEMS, INPUT, ENTITY, STACK, STOP, digest, model, vectors

CALLER, CALLER_BYTES = 0x021E65A8, 336


def execute(main, overlay, parent, bindings, vector):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.ctl_set_cpu_model(UC_CPU_ARM_946)
    machine.mem_map(BASE, 0x400000)
    machine.mem_map(0x03000000, 0x20000)
    machine.mem_map(STOP, 0x1000)
    machine.mem_write(BASE, main)
    machine.mem_write(0x021D7240, overlay)
    machine.mem_write(ENTRY, parent)
    machine.mem_write(CONTEXT, vector['context'])
    machine.mem_write(MARKER, vector['marker'])
    machine.mem_write(ITEMS, struct.pack('<256H', *vector['items'], *([0] * 253)))
    machine.mem_write(INPUT, struct.pack('<HH', 0, vector['keys']))
    entity = bytearray(0x40)
    struct.pack_into('<I', entity, 0x1C, vector['entityWord'])
    entity[0x23] = 7
    machine.mem_write(ENTITY, bytes(entity))
    rng = random.Random(vector['seed'])
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    initial = [rng.getrandbits(32) for unused in range(13)]
    for i, value in enumerate(initial):
        machine.reg_write(UC_ARM_REG_R0 + i, value)
    machine.reg_write(UC_ARM_REG_SP, STACK + 0xFFF0)
    machine.reg_write(UC_ARM_REG_LR, STOP)
    providers = {int(row['address'], 0): name for name, row in bindings.items() if row['kind'] == 'function'}
    calls, trace, writes = [], [], []

    def step(engine, pc, size, unused):
        trace.append(pc)
        if pc in providers:
            calls.append(pc)
            engine.reg_write(UC_ARM_REG_R0, vector['returns'].get(pc, 0))
            lr = engine.reg_read(UC_ARM_REG_LR)
            engine.reg_write(UC_ARM_REG_CPSR, engine.reg_read(UC_ARM_REG_CPSR) & ~32 | (32 if lr & 1 else 0))
            engine.reg_write(UC_ARM_REG_PC, lr & ~1)
        elif not (ENTRY <= pc < ENTRY + len(parent) or CALLER <= pc < CALLER + CALLER_BYTES):
            raise ValueError('Connected reward execution escaped its two measured functions')

    def written(engine, access, address, size, value, unused):
        if not any(start <= address and address + size <= start + length for start, length in
                   [(STACK, 0x10000), (CONTEXT, 0x38), (MARKER, 4), (ENTITY, 0x40)]):
            raise ValueError('Connected reward execution wrote outside fixture state')
        writes.append((address, size, value))

    machine.hook_add(UC_HOOK_CODE, step)
    machine.hook_add(UC_HOOK_MEM_WRITE, written)
    machine.emu_start(CALLER, STOP, timeout=2000000, count=10000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_R0) != 0:
        raise ValueError('Connected reward caller did not return the modeled zero result')
    if ENTRY not in trace or 0x021E6630 not in trace or trace.count(ENTRY) != 1:
        raise ValueError('Connected reward dispatch did not execute exactly one native parent call')
    actual = (bytes(machine.mem_read(CONTEXT, 0x38)), bytes(machine.mem_read(MARKER, 4)),
              bytes(machine.mem_read(ENTITY, 0x40)), calls)
    if actual != model(vector):
        raise ValueError('Connected caller differs from independent reward state/call-order model')
    if [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(4, 12)] != initial[4:12]:
        raise ValueError('Connected caller failed preserved-register ABI')
    return {'actualReturn': True, 'parentCalls': 1, 'initialState': vector['context'][4],
            'finalState': actual[0][4], 'instructions': len(trace), 'calls': [hex(pc) for pc in calls],
            'registers': [machine.reg_read(UC_ARM_REG_R0 + i) for i in range(13)],
            'sp': machine.reg_read(UC_ARM_REG_SP), 'lr': machine.reg_read(UC_ARM_REG_LR),
            'pc': machine.reg_read(UC_ARM_REG_PC), 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'wholeRamSha256': digest(bytes(machine.mem_read(BASE, 0x400000))),
            'wholeStackSha256': digest(bytes(machine.mem_read(0x03000000, 0x20000))),
            'pcTraceSha256': digest(json.dumps(trace).encode()), 'writeTraceSha256': digest(json.dumps(writes).encode())}


def main():
    native_dependencies(configuration())
    report_path = 'evidence/matches/ov001-20261029-reward-state.json'
    row = read_json(ROOT / report_path)['matches'][0]
    if sha256(ROOT / row['source']) != row['sourceSha256']:
        raise ValueError('Connected reward source identity changed')
    binary = ROOT / row['isolatedCallerBinary']
    if sha256(binary) != row['isolatedCallerBinarySha256']:
        raise ValueError('Connected reward linked caller identity changed')
    metadata, overlay, unused = measured_module('ov001')
    unused, main_code, unused = measured_module('main')
    native = overlay[ENTRY - 0x021D7240:ENTRY - 0x021D7240 + row['bytes']]
    source = binary.read_bytes()
    if native != source:
        raise ValueError('Connected reward source-only link differs from native parent')
    results = []
    for vector in vectors():
        context = bytearray(vector['context'])
        context[0x16] = 1
        vector = {**vector, 'context': bytes(context)}
        original = execute(main_code, overlay, native, row['nativeSymbolEntries'], vector)
        rebuilt = execute(main_code, overlay, source, row['nativeSymbolEntries'], vector)
        if original != rebuilt:
            raise ValueError('Connected native/recompiled reward state, registers or traces differ')
        results.append(original)
    output = {'schemaVersion': 1, 'createdUtc': now(), 'romSha256': configuration()['romSha256'],
              'processor': 'arm9', 'module': 'ov001', 'mode': 'arm', 'moduleInputSha256': metadata['sha256'],
              'caller': hex(CALLER), 'callerBytes': CALLER_BYTES,
              'callerSpanSha256': digest(overlay[CALLER - 0x021D7240:CALLER - 0x021D7240 + CALLER_BYTES]),
              'selectedParent': hex(ENTRY), 'parentBytes': row['bytes'],
              'contextSelectorAddress': hex(CONTEXT + 0x16), 'contextSelectorValue': 1,
              'parentSource': row['source'], 'parentSourceSha256': row['sourceSha256'],
              'parentLinkedSha256': row['isolatedCallerBinarySha256'],
              'cases': len(results), 'actualReturns': len(results) * 2, 'sourceCredit': 0,
              'generator': Path(__file__).name, 'generatorSha256': sha256(Path(__file__)),
              'dependencies': [{'path': report_path, 'sha256': sha256(ROOT / report_path)},
                               {'path': 'reward_state_fixture_20261029.py', 'sha256': sha256(ROOT / 'reward_state_fixture_20261029.py')}],
              'results': results, 'limits': {'instructions': 10000, 'timeoutMicroseconds': 2000000},
              'limitations': ['Only native caller selector 1 and one parent invocation are certified',
                              'All parent external callees retain explicit return-only synthetic providers',
                              'The existing 336-byte dispatch source is unchanged and receives no new source credit',
                              'Native dependency state initialization, rendering and ordinary game lifecycle remain unsupported']}
    write_json(ROOT / 'evidence/application/reward-connected-20261029.json', output)
    print({'cases': len(results), 'actualReturns': len(results) * 2, 'sourceCredit': 0})


if __name__ == '__main__':
    from pathlib import Path
    main()
