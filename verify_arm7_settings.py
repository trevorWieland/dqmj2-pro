import argparse
import json
import random
import struct
from pathlib import Path
import match_arm7 as matcher
import match_lowlevel as lowlevel
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/arm7/settings26/native_arm7_main_027e8428.c'
REPORT = ROOT / 'evidence/matches/arm7-settings26.json'
ADDRESS = 0x027E8428
GLOBAL = 0x027F8DD4
INPUT, OUTPUT, STATE, SECONDARY = 0x03001000, 0x03001200, 0x03002000, 0x03006000
COMPILER = ROOT / 'tools/mwccarm/mwccarm/2.0/base/mwccarm.exe'
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def fixture(vector, flags, original_state, original_input, original_output, irq):
    state, request, output = bytearray(original_state), bytearray(original_input), bytearray(original_output)
    old_mode = [0, 8, 9, 10, 11, 65535][vector % 6]
    struct.pack_into('<H', state, 0, old_mode)
    for index, offset in enumerate((4, 6, 8)):
        struct.pack_into('<H', request, offset, [0, 1, 15, 16, 32767, 32768, 65535, 2][(vector + index) % 8])
    for index, offset in enumerate((10, 12)):
        struct.pack_into('<H', request, offset, [0, 1, 511, 512, 513, 65534, 65535, 2][(vector + index) % 8])
    for index, offset in enumerate((14, 16)):
        struct.pack_into('<H', request, offset, [0, 1, 63, 64, 1023, 1024, 9999, 10000, 10001, 65535][(vector + index) % 10])
    for index, offset in enumerate((18, 20)):
        struct.pack_into('<H', request, offset, [0, 190, 191, 219, 220, 262, 263, 65535][(vector + index) % 8])
    struct.pack_into('<H', request, 22, (vector * 257) & 65535)
    struct.pack_into('<I', request, 0, flags)
    struct.pack_into('<H', state, 0x34, [0, 1, 2, 16, 511, 512, 65535, 513][vector % 8])
    struct.pack_into('<h', state, 0x62, [-32768, -1, 0, 1, 15, 16, 32767, 200][vector % 8])
    destination = [0, OUTPUT, INPUT, OUTPUT][vector % 4]
    if destination == INPUT:
        output = request
    initial_state, initial_input, initial_output = bytes(state), bytes(request), bytes(output)
    result = 0
    selected = flags
    if old_mode in (9, 10) and selected & 0x2c00:
        selected &= ~0x2c00
        result = 3
    calls = []
    global_pointer = STATE
    def half(data, offset):
        return struct.unpack_from('<H', data, offset)[0]
    def store(offset, value, kind='H'):
        struct.pack_into('<' + kind, state, offset, value)
    def call(address, *arguments):
        nonlocal global_pointer
        mutations = []
        calls.append({'address': address, 'arguments': list(arguments), 'state': bytes(state),
                      'input': bytes(request), 'output': bytes(output), 'mutations': mutations})
        if address == 0x037fdd00 and vector % 3 == 0:
            store(0, 0x1234)
            global_pointer = SECONDARY
            mutations.extend([(STATE, struct.pack('<H', 0x1234)), (GLOBAL, struct.pack('<I', SECONDARY))])
        if address == 0x027e0840 and vector % 3 == 1:
            value = [63, 10000, 10001, 65535][vector % 4]
            struct.pack_into('<H', request, 14, value)
            struct.pack_into('<I', request, 0, flags ^ 0x3fff)
            mutations.extend([(INPUT + 14, struct.pack('<H', value)), (INPUT, struct.pack('<I', flags ^ 0x3fff))])
        if address == 0x027e086c and vector % 3 == 2:
            value = [64, 10000, 10001, 65535][vector % 4]
            position = [190, 191, 262, 263][vector % 4]
            struct.pack_into('<HH', request, 16, value, position)
            mutations.append((INPUT + 16, struct.pack('<HH', value, position)))
    call(0x037fdd00)
    if destination:
        struct.pack_into('<I', output, 0, 0x3fff)
        for target, source in zip(range(4, 24, 2), (0x58, 0x5a, 0x5c, 0x30, 0x32, 0x44, 0x46, 0x40, 0x42, 0x98)):
            struct.pack_into('<H', output, target, half(state, source))
        for target, source in zip(range(24, 28), (0x92, 0x94, 0x9a, 0x9c)):
            output[target] = half(state, source) & 255
    for bit, source, target, backup in ((1, 4, 0x58, 0x7c0), (2, 6, 0x5a, 0x7c2), (4, 8, 0x5c, 0x7c4)):
        if selected & bit:
            value = half(request, source) or 16
            store(target, value)
            store(backup, value)
            if bit != 1 and struct.unpack_from('<h', state, 0x62)[0] > value:
                store(0x62, value)
    if selected & 8:
        value = half(request, 10)
        if half(state, 0x34) < ((value + 1) & 0xfffe):
            result = 6
        else:
            call(0x027e0840, value)
    if selected & 16:
        value = half(request, 12)
        if ((value + 1) & 0xfffe) > 512:
            result = 6
        else:
            call(0x027e086c, value)
    for bit, source, target, ticks in ((32, 14, 0x44, 0x48), (64, 16, 0x46, 0x50)):
        if selected & bit:
            value = half(request, source)
            if value > 10000:
                result = 6
            else:
                store(target, value)
                store(ticks, value * 33514 // 65536, 'Q')
    for bit, source, target in ((128, 18, 0x40), (256, 20, 0x42)):
        if selected & bit:
            value = half(request, source)
            if value <= 190 or 220 <= value <= 262:
                store(target, value)
            else:
                result = 6
    if selected & 512:
        store(0x98, half(request, 22))
        store(0x7ca, half(request, 22))
    for bit, source, target in ((1024, 24, 0x92), (2048, 25, 0x94), (4096, 26, 0x9a), (8192, 27, 0x9c)):
        if selected & bit:
            store(target, request[source])
            if bit == 4096:
                store(0x7cc, half(state, 0x9a))
    call(0x037fdd14, irq)
    return {'initialState': initial_state, 'initialInput': initial_input, 'initialOutput': initial_output,
            'state': bytes(state), 'input': bytes(request), 'output': bytes(output), 'calls': calls,
            'destination': destination, 'result': result, 'globalPointer': global_pointer}


def execute(code, vector, flags):
    rng = random.Random(20261027 + vector * 65537 + flags)
    irq = 0x80 if vector & 1 else 0
    required = fixture(vector, flags, rng.randbytes(0x900), rng.randbytes(28), rng.randbytes(28), irq)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    regions = [(0x027e0000, 0x20000), (0x037f8000, 0x10000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for address, size in regions:
        machine.mem_map(address, size)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(ADDRESS, code)
    machine.mem_write(GLOBAL, struct.pack('<I', STATE))
    machine.mem_write(STATE, required['initialState'])
    secondary = bytes(machine.mem_read(SECONDARY, 0x900))
    machine.mem_write(INPUT, required['initialInput'])
    if required['destination'] == OUTPUT:
        machine.mem_write(OUTPUT, required['initialOutput'])
    registers = [rng.getrandbits(32) for _ in lowlevel.REGISTERS]
    registers[:2] = [INPUT, required['destination']]
    registers[-2:] = [0x0301fff0, 0x05000000]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | irq)
    for register, value in zip(lowlevel.REGISTERS, registers):
        machine.reg_write(register, value)
    calls, writes, visited = [], [], set()
    def write(uc, access, address, size, value, user):
        allowed = STATE <= address and address + size <= STATE + 0x900
        allowed |= bool(required['destination'] and required['destination'] <= address and address + size <= required['destination'] + 28)
        allowed |= 0x0301f000 <= address and address + size <= 0x0301fff0
        if not allowed:
            raise ValueError('Settings caller wrote outside its primary state, optional snapshot or bounded stack')
        writes.append([address, size, value & ((1 << (size * 8)) - 1)])
    def store(uc, address, payload):
        uc.mem_write(address, payload)
        writes.append([address, len(payload), payload.hex()])
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        stage = len(calls)
        expected = required['calls'][stage] if stage < len(required['calls']) else None
        actual = [uc.reg_read(register) for register in lowlevel.REGISTERS[:4]]
        if expected is None or address != expected['address'] or actual[:len(expected['arguments'])] != expected['arguments']:
            raise ValueError({'failure': 'Independent settings API contract differs', 'vector': vector,
                              'flags': hex(flags), 'address': hex(address), 'actual': actual, 'expected': expected})
        if bytes(uc.mem_read(STATE, 0x900)) != expected['state'] or bytes(uc.mem_read(INPUT, 28)) != expected['input']:
            actual_state, actual_input = bytes(uc.mem_read(STATE, 0x900)), bytes(uc.mem_read(INPUT, 28))
            raise ValueError({'failure': 'Independent settings ordering/input-reload model differs before helper',
                              'vector': vector, 'flags': hex(flags), 'stage': stage,
                              'state': [(hex(index), first, last) for index, (first, last) in enumerate(zip(actual_state, expected['state'])) if first != last][:16],
                              'input': [(index, first, last) for index, (first, last) in enumerate(zip(actual_input, expected['input'])) if first != last]})
        if required['destination'] and bytes(uc.mem_read(required['destination'], 28)) != expected['output']:
            raise ValueError('Old-value snapshot differs before helper')
        for destination, payload in expected['mutations']:
            store(uc, destination, payload)
        result = irq if address == 0x037fdd00 else rng.getrandbits(32)
        store(uc, 0x03010000 + stage * 4, struct.pack('<I', result))
        returned = uc.reg_read(lowlevel.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': actual})
        for register in lowlevel.REGISTERS[:4] + [lowlevel.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(lowlevel.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (irq if address == 0x037fdd14 else 0x80))
        uc.reg_write(UC_ARM_REG_PC, returned)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(ADDRESS, 0x05000000, count=3000)
    if machine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(required['calls']):
        raise ValueError('Settings caller did not return after the expected protocol')
    if machine.reg_read(lowlevel.REGISTERS[0]) != required['result'] or machine.reg_read(UC_ARM_REG_CPSR) & 0x80 != irq:
        raise ValueError('Independent settings return/interrupt restoration model differs')
    if bytes(machine.mem_read(STATE, 0x900)) != required['state'] or bytes(machine.mem_read(INPUT, 28)) != required['input']:
        raise ValueError('Independent final settings/tick/input model differs')
    if required['destination'] and bytes(machine.mem_read(required['destination'], 28)) != required['output']:
        raise ValueError('Independent final old-value/aliased snapshot model differs')
    if bytes(machine.mem_read(SECONDARY, 0x900)) != secondary:
        raise ValueError('Caller reloaded a changed work-area pointer and modified the wrong allocation')
    if struct.unpack('<I', bytes(machine.mem_read(GLOBAL, 4)))[0] != required['globalPointer']:
        raise ValueError('Synthetic shared-work pointer mutation was lost')
    return {'registers': [machine.reg_read(register) for register in lowlevel.REGISTERS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'writes': writes, 'calls': calls, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(machine.mem_read(address, size))) for address, size in regions]}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--exhaustive-flags', action='store_true')
    args = parser.parse_args()
    report = json.loads(REPORT.read_text()) if REPORT.exists() else {'schemaVersion': 1, 'processor': 'arm7',
        'runtimeMappingCanonical': True, 'matches': [], 'romSha256': matcher.sha((ROOT / 'inputs/game.nds').read_bytes()),
        'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if report['matches'] and matcher.sha(SOURCE.read_bytes()) != report['matches'][0]['sourceSha256']:
        raise ValueError('Frozen ordinary C settings source changed')
    spec = matcher.accepted_spec(report['matches'][0]) if report['matches'] else next(item for item in matcher.candidates(10000) if item['address'] == ADDRESS)
    entry, compiled = matcher.compare(SOURCE, spec, COMPILER, PIN, 2, 'off', False)
    if compiled is None:
        raise ValueError('Ordinary C64-bit tick arithmetic stopped matching all804 native bytes')
    binary = (ROOT / spec['binary']).read_bytes()
    native = binary[ADDRESS - spec['base']:ADDRESS - spec['base'] + spec['bytes']]
    vectors = [(index * 16 + scenario, 1 << index) for index in range(14) for scenario in range(16)]
    vectors += [(1000 + index, mask) for index, mask in enumerate([0, 0x3fff, 0x2c00, 0x1000, 0x3c00, 0xffffffff] * 16)]
    rng = random.Random(20261027)
    vectors += [(2000 + index, rng.getrandbits(32)) for index in range(192)]
    if args.exhaustive_flags:
        vectors += [(10000 + mask, mask) for mask in range(0x4000)]
    records, visited, external = [], set(), 0
    for vector, flags in vectors:
        expected, actual = execute(native, vector, flags), execute(compiled, vector, flags)
        if expected != actual:
            raise ValueError('Native and recompiled settings effects differ')
        visited.update(expected['visited'])
        external += len(expected['calls']) * 2
        records.append({'vector': vector, 'flags': hex(flags), 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['oracle'] = {'vectors': len(records), 'nativeAndRecompiledCalls': len(records) * 2, 'syntheticExternalCalls': external,
        'nativeCalleeCalls': 0, 'exhaustive14BitFlagWords': args.exhaustive_flags, 'verifiedReturn': True,
        'independentConfigurationAndTickAssertions': True, 'records': records,
        'instructionAddressesVisited': [hex(address) for address in sorted(visited)],
        'limitations': ['Independent assertions cover14 control bits, blocked modes9/10, optional and aliased28-byte old-value snapshots, even-length wrap, signed clamps and inclusive coordinate/time bounds',
                        '64-bit time fields are checked by unbounded Python multiplication and integer division; synthetic helpers mutate later input fields and the shared work pointer to check reload/caching behavior',
                        'IRQ disable/restore and two length setters are synthetic explicit ABI contracts; their native bodies and physical wireless/timer behavior are not executed or credited']}
    report.update(matches=[entry], nativeSymbols={item['symbol']: item['target'] for item in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'vectors': len(records), 'nativeAndRecompiledCalls': len(records) * 2,
           'syntheticExternalCalls': external, 'visitedInstructions': len(visited)})


if __name__ == '__main__':
    main()
