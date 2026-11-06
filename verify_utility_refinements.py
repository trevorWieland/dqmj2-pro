import json
import random
import struct
from pathlib import Path
import utility_code
import utility_runtime
import match_lowlevel
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
TARGETS = {0x027EA5EC: 'unsigned-halfword-device-and-state-write',
           0x037FA9A0: 'unsigned-threshold-relative-offset',
           0x027EAFE0: 'bounded-one-bit-setting',
           0x027EB2C0: 'bounded-two-bit-setting'}
VALUES = [0, 1, 2, 3, 4, 7, 0x7FFF, 0x8000, 0xFFFF, 0x04805F5F, 0x04805F60, 0xFFFFFFFF]


def execute(code, spec, argument, stored, vector, layout, files):
    rng = random.Random(20261027 + spec['address'] + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x800000), (0x03000000, 0x20000),
              (0x037F8000, 0x18000), (0x04000000, 0x2000), (0x04800000, 0x10000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    snapshots = [(0x03000000, 0x20000), (0x04800000, 0x10000), (0x037F8000, 0x18000)]
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(0x04800000, rng.randbytes(0x10000))
    for module in layout['modules']:
        if module['processor'] != spec['processor']:
            continue
        first = int(module['base'], 0)
        payload = bytes(files[ROOT / module['binary']])
        engine.mem_write(first, payload)
        snapshots.append((first, len(payload)))
        if module['bssBytes']:
            engine.mem_write(int(module['bssStart'], 0), bytes(module['bssBytes']))
            snapshots.append((int(module['bssStart'], 0), module['bssBytes']))
    engine.mem_write(0x0380FFF4, struct.pack('<I', 0x03004000))
    engine.mem_write(0x030043DE, struct.pack('<H', stored))
    engine.mem_write(spec['address'], code)
    registers = [rng.getrandbits(32) for _ in match_lowlevel.REGISTERS]
    registers[0], registers[-2], registers[-1] = argument, 0x0301FFF0, 0x05000000
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x13 | (0x20 if spec['mode'] == 'thumb' else 0) | (0x80 if vector % 2 else 0))
    for register, value in zip(match_lowlevel.REGISTERS, registers):
        engine.reg_write(register, value)
    writes, visited = [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value]))
    def trace(uc, address, size, user):
        if not spec['address'] <= address < spec['address'] + len(code):
            raise ValueError('Leaf fixture escaped its complete native source unit')
        visited.add(address)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(spec['address'] | int(spec['mode'] == 'thumb'), 0x05000000, count=1000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000:
        raise ValueError('Fixture did not return within its instruction bound')
    result = engine.reg_read(match_lowlevel.REGISTERS[0])
    if spec['address'] == 0x027EA5EC:
        expected, effects = 0, [[0x03004354, 2, argument >> 1], [0x0480803C, 2, argument]]
    elif spec['address'] == 0x037FA9A0:
        expected = (argument - stored if argument >= 0x04805F60 else argument) & 0xFFFFFFFF
        effects = []
    else:
        bound, offset = (1, 0x332) if spec['address'] == 0x027EAFE0 else (3, 0x336)
        expected = 5 if argument > bound else 0
        effects = [] if argument > bound else [[0x03004000 + offset, 2, argument]]
    if result != expected or writes != effects:
        raise ValueError({'address': hex(spec['address']), 'actualReturn': result, 'expectedReturn': expected, 'actualWrites': writes, 'expectedWrites': effects})
    return {'registers': [engine.reg_read(register) for register in match_lowlevel.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'writes': writes, 'visited': sorted(visited), 'memoryHashes': [utility_runtime.sha(bytes(engine.mem_read(first, size))) for first, size in snapshots]}


def main():
    report = json.loads((ROOT / 'evidence/matches/utility-refined02.json').read_text())
    layout, files = utility_runtime.derive()
    results = []
    for entry in report['matches']:
        address = int(entry['address'], 0)
        if address not in TARGETS:
            continue
        source = ROOT / entry['source']
        if utility_runtime.sha(source.read_bytes()) != entry['sourceSha256']:
            raise ValueError('Frozen fixture C identity changed')
        spec = utility_code.accepted_spec(entry)
        flags = entry['compilerFlags']
        settings = dict(spec, compilerPath=ROOT / entry['compiler'], compilerProc=flags[flags.index('-proc') + 1], interworking='-nointerworking' not in flags)
        rebuilt, compiled = utility_code.compile_compare(source, settings, int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
        if compiled is None:
            raise ValueError('Fixture C stopped matching its native span')
        binary = bytes(files[ROOT / spec['binary']])
        native = binary[address - spec['base']:address - spec['base'] + spec['bytes']]
        cases = []
        arguments = [value for value in VALUES if address != 0x027EA5EC or value <= 0xFFFF]
        for argument in arguments:
            for stored in (0, 1, 0xFFFF):
                for irq in range(2):
                    vector = len(cases)
                    expected = execute(native, spec, argument, stored, vector, layout, files)
                    actual = execute(compiled, spec, argument, stored, vector, layout, files)
                    if actual != expected:
                        raise ValueError('Recompiled C leaf effects differ from native')
                    cases.append({'argument0': hex(argument), 'storedHalfword': stored, 'vector': vector,
                                  'stateSha256': utility_runtime.sha(json.dumps(expected, sort_keys=True).encode())})
        results.append({'program': utility_runtime.PROGRAM, 'processor': entry['processor'], 'module': entry['module'], 'address': entry['address'],
                        'mode': entry['mode'], 'bytes': entry['bytes'], 'source': entry['source'], 'sourceSha256': entry['sourceSha256'],
                        'objectSha256': rebuilt['objectSha256'], 'nativeSha256': entry['targetSha256'], 'inputModuleSha256': entry['inputModuleSha256'],
                        'fixture': TARGETS[address], 'cases': cases, 'nativeAndRecompiledCalls': len(cases) * 2, 'independentExpectedWritesAndReturn': True})
    if {int(entry['address'], 0) for entry in results} != set(TARGETS):
        raise ValueError('Required fixture source set changed')
    output = {'schemaVersion': 1, 'romSha256': report['romSha256'], 'program': utility_runtime.PROGRAM, 'results': results,
              'cases': sum(len(entry['cases']) for entry in results), 'nativeAndRecompiledCalls': sum(entry['nativeAndRecompiledCalls'] for entry in results),
              'fixtureInputs': {'sharedPointerSlot': '0x0380fff4', 'controlledScratchTarget': '0x03004000', 'mmioRange': ['0x04800000', '0x04810000']},
              'limitations': ['MMIO is synthetic isolated memory; wireless device responses and physical bus timing are not modeled', 'No native callee or unaccepted source bytes execute in these leaf fixtures', 'Only ABI-valid zero-extended argument values are used for the unsigned16 parameter; full32-bit values exercise the other leaves']}
    path = ROOT / 'evidence/verification/utility-refinement-fixtures.json'
    path.write_text(json.dumps(output, indent=2) + '\n')
    print({'functions': len(results), 'cases': output['cases'], 'nativeAndRecompiledCalls': output['nativeAndRecompiledCalls']})


if __name__ == '__main__':
    main()
