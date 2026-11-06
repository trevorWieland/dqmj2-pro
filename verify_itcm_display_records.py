import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/large54/native_itcm_01ffbbcc.c'
HEADER = SOURCE.with_name('context.h')
REPORT = ROOT / 'evidence/matches/itcm-large54.json'
ADDRESS = 0x01FFBBCC
FRAME = 0x0301FF78
FIRST, SECOND, TEXT = FRAME + 16, FRAME + 12, FRAME + 20
STATES = [0, 9, 10, 11, 12, 41, 42, 43, 44, 45, 46, 47, 48, 49, 0xffffffff, 0x80000000, 0x7fffffff]
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def model(state, scenario, points, descriptors, objects, attributes, keys, colors):
    count = [0, 1, 2, 3, 6, 8][scenario % 6]
    first, second = list(points[2:]), list(points[:2])
    calls = []
    descriptor_index, text, font = 0, None, 0
    def call(address, *arguments, point=None, check_text=None):
        nonlocal descriptor_index, font
        result = (address * 2654435761 + len(calls) * 40503 + scenario) & 0xffffffff
        if address == 0x01ffb340:
            result = 0x03002000
        elif address == 0x01ffb334:
            result = 0x03003000 + descriptor_index * 32
            descriptor_index += 1
        elif address == 0x02049ad0:
            result = 0x03008000 + (arguments[0] & 255) * 256
        elif address == 0x02063b40:
            result = [0, 1, 2][scenario % 3]
        elif address == 0x01ffa978:
            font += 1
            result = 0xf00d0000 + font
        elif address == 0x020685f0:
            result = 0x03006000
        elif address == 0x022238c0:
            index = (arguments[0] + 128) & 255
            result = 127 if index % 3 == scenario % 3 else (index * 17 + scenario) & 255
        elif address == 0x02223c40:
            result = (0x7a000000 + (arguments[0] & 255)) & 0xffffffff
        elif address == 0x02049604:
            result = 0x67000000 | scenario
        calls.append({'address': address, 'arguments': [value & 0xffffffff for value in arguments],
                      'result': result, 'point': None if point is None else list(point), 'text': check_text})
        return result
    def descriptor():
        pointer = call(0x01ffb334)
        return descriptors[(pointer - 0x03003000) // 32]
    def draw(arguments, point, is_text=False):
        call(0x0204a808 if is_text else 0x0204a574, *arguments, point=point, check_text=text if is_text else None)
        if scenario & 1:
            point[:] = [(point[0] + 19) & 65535, (point[1] - 31) & 65535]
    if state == 43:
        return {'calls': calls, 'return': 43, 'first': first, 'second': None, 'count': count}
    call(0x01ffb340)
    for index in range(count):
        call(0x02049ad0, index + 5)
        call(0x02049f4c)
        call(0x01ffb340)
    call(0x01ffb340)
    style = 1
    for index in range(count):
        if state == 42:
            if keys[index] != 255:
                resource = call(0x020685f0)
                call(0x02046af4, 0x021c9698, resource, 31, 0, TEXT, 255)
                text = bytes((scenario * 17 + index * 31 + offset) & 255 for offset in range(64))
                calls[-1]['fill'] = text
                color = {1: 1, 2: 5, 3: 3}.get(colors[keys[index]])
                if color is not None:
                    draw([index + 5, FIRST, color, TEXT, 1], first, True)
            else:
                handle = call(0x01ffa978)
                first_record, second_record = descriptor(), descriptor()
                draw([index + 5, FIRST, handle, first_record[0], struct.unpack_from('<H', second_record, 2)[0], 3, 1], first)
        elif state in (10, 11):
            status = call(0x02063b40, 0x11d)
            if status == 0 and index == 1:
                style = 3
            handle = call(0x01ffa978)
            first_record, second_record = descriptor(), descriptor()
            position = (index + struct.unpack_from('<h', second_record, 2)[0]) & 65535
            draw([index + 5, FIRST, handle, first_record[0], position, style, 1], first)
        elif state not in (43, 45, 46, 48):
            handle = call(0x01ffa978)
            first_record, second_record = descriptor(), descriptor()
            position = (index + struct.unpack_from('<h', second_record, 2)[0]) & 65535
            draw([index + 5, FIRST, handle, first_record[0], position, 1, 1], first)
        call(0x01ffb340)
    for index, record in enumerate(objects):
        call(0x02049ad0, index)
        if struct.unpack_from('<I', record, 0)[0]:
            value = call(0x022238c0, struct.unpack_from('<b', record, 5)[0])
            if value != 127:
                signed = value if value < 128 else value - 256
                handle = call(0x02223c40, signed)
                fields = struct.unpack_from('<bbbb', attributes[index], 28)
                call(0x0206006c, handle, *fields)
    if struct.unpack_from('<h', descriptor(), 4)[0] != -1:
        handle = call(0x01ffa978)
        first_record, second_record = descriptor(), descriptor()
        draw([0, SECOND, handle, struct.unpack_from('<h', first_record, 4)[0] & 255,
              struct.unpack_from('<H', second_record, 6)[0], 1, 1], second)
    context = call(0x01ffb340)
    returned = call(0x02049604, context, 0)
    return {'calls': calls, 'return': returned, 'first': first, 'second': second, 'count': count}


def execute(code, state, scenario):
    rng = random.Random(20261027 + state + scenario * 65537)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    for address, size in [(0x01ff8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x05000000, 0x1000)]:
        machine.mem_map(address, size)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(ADDRESS, code)
    points = [rng.randrange(65536) for _ in range(4)]
    machine.mem_write(0x020dc88c, struct.pack('<HHHH', *points))
    machine.mem_write(0x021d4110, struct.pack('<I', state))
    keys = [255 if (index + scenario) % 3 == 0 else (index + scenario) % 8 for index in range(8)]
    colors = [(index + scenario) % 5 for index in range(8)]
    machine.mem_write(0x021d41f4, bytes(keys + colors))
    descriptors, objects, attributes = [], [], []
    for index in range(64):
        record = bytearray(rng.randbytes(32))
        record[0] = (scenario * 31 + index * 7) & 255
        struct.pack_into('<h', record, 2, [-32768, -1, 0, 1, 32767][(index + scenario) % 5])
        struct.pack_into('<h', record, 4, [-1, -128, 0, 127, 255, 32767][(index + scenario) % 6])
        struct.pack_into('<H', record, 6, [0, 1, 32767, 32768, 65535][(index + scenario) % 5])
        descriptors.append(bytes(record))
        machine.mem_write(0x03003000 + index * 32, bytes(record))
    for index in range(31):
        record = bytearray(rng.randbytes(16))
        struct.pack_into('<I', record, 0, 0 if (scenario + index) % 4 == 0 else 0x0300c000 + index * 256)
        record[5] = [128, 255, 0, 127, 1, 254][(scenario + index) % 6]
        data = bytearray(rng.randbytes(64))
        data[28:32] = bytes([128, 255, 0, 127][(scenario + index + offset) % 4] for offset in range(4))
        objects.append(bytes(record))
        attributes.append(bytes(data))
        machine.mem_write(0x03008000 + index * 256, bytes(record))
        machine.mem_write(0x0300c004 + index * 256, struct.pack('<I', 0x03010000 + index * 64))
        machine.mem_write(0x03010000 + index * 64, bytes(data))
    required = model(state, scenario, points, descriptors, objects, attributes, keys, colors)
    machine.mem_write(0x0300200c, struct.pack('<H', required['count']))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[-2:] = [0x0301fff0, 0x05000000]
    flags = rng.getrandbits(4) << 28 | 0x10 | (0x80 if scenario & 1 else 0)
    machine.reg_write(UC_ARM_REG_CPSR, flags)
    for register, value in zip(matcher.REGISTERS, registers):
        machine.reg_write(register, value)
    readonly = [(0x020dc88c, 8), (0x021d4100, 256), (0x03003000, 2048), (0x03008000, 0x1f00),
                (0x0300c000, 0x1f00), (0x03010000, 31 * 64)]
    originals = [bytes(machine.mem_read(address, size)) for address, size in readonly]
    calls, writes, visited = [], [], set()
    def write(uc, access, address, size, value, user):
        if not (FRAME <= address and address + size <= 0x0301fff0):
            raise ValueError('Display routine wrote outside its measured native stack frame')
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
        actual = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        stack = struct.unpack('<III', bytes(uc.mem_read(uc.reg_read(matcher.REGISTERS[-2]), 12)))
        if expected is None or address != expected['address'] or (actual + list(stack))[:len(expected['arguments'])] != expected['arguments']:
            raise ValueError({'failure': 'Independent display/record API contract differs', 'state': hex(state),
                              'scenario': scenario, 'stage': stage, 'address': hex(address),
                              'actual': actual + list(stack), 'expected': expected})
        if expected['point'] is not None:
            if bytes(uc.mem_read(actual[1], 4)) != struct.pack('<HH', *expected['point']):
                raise ValueError('Helper-visible point fields or previous helper mutations differ')
            if scenario & 1:
                values = [(expected['point'][0] + 19) & 65535, (expected['point'][1] - 31) & 65535]
                store(uc, actual[1], struct.pack('<HH', *values))
        if expected['text'] is not None and bytes(uc.mem_read(TEXT, 64)) != expected['text']:
            raise ValueError('Frame text record differs from independent bounded helper output')
        if 'fill' in expected:
            store(uc, TEXT, expected['fill'])
        result = expected['result']
        store(uc, 0x03014000 + stage * 4, struct.pack('<I', result))
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': actual, 'stack': list(stack)})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (flags & 0x80))
        uc.reg_write(UC_ARM_REG_PC, returned)
    machine.hook_add(UC_HOOK_MEM_WRITE, write)
    machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(ADDRESS, 0x05000000, count=20000)
    if machine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(required['calls']):
        raise ValueError('Display routine did not return after the independent expected protocol')
    if machine.reg_read(matcher.REGISTERS[0]) != required['return']:
        raise ValueError('Display return differs from independent terminal-helper/early-state model')
    if bytes(machine.mem_read(FIRST, 4)) != struct.pack('<HH', *required['first']):
        raise ValueError('Final first-point record differs')
    if required['second'] is not None and bytes(machine.mem_read(SECOND, 4)) != struct.pack('<HH', *required['second']):
        raise ValueError('Final second-point record differs')
    if [bytes(machine.mem_read(address, size)) for address, size in readonly] != originals:
        raise ValueError('Readonly display globals, descriptor records or entity data changed')
    return {'registers': [machine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(machine.mem_read(address, size))) for address, size in
                             [(0x01ff8000, 0x8000), (0x03000000, 0x20000)]]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Display C compiler pin changed')
    dependencies = [{'path': HEADER.relative_to(ROOT).as_posix(), 'sha256': matcher.sha(HEADER.read_bytes())}]
    report = json.loads(REPORT.read_text()) if REPORT.exists() else {'schemaVersion': 1, 'module': 'itcm', 'matches': [],
             'romSha256': matcher.sha((ROOT / 'inputs/game.nds').read_bytes()), 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if report['matches'] and (matcher.sha(SOURCE.read_bytes()) != report['matches'][0]['sourceSha256'] or dependencies != report['matches'][0]['sourceDependencies']):
        raise ValueError('Frozen display C source or dependency changed')
    attempts, matches = matcher.compare(SOURCE, 'itcm', 2, 'off', True)
    if 'native_itcm_01ffbbcc' not in matches:
        raise ValueError('Ordinary C display routine stopped matching all native bytes')
    entry, compiled = matches['native_itcm_01ffbbcc']
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01ff8000:ADDRESS - 0x01ff8000 + entry['bytes']]
    records, visited, external = [], set(), 0
    for state in STATES:
        for scenario in range(12):
            expected, actual = execute(native, state, scenario), execute(compiled, state, scenario)
            if expected != actual:
                raise ValueError('Native and recompiled display/record effects differ')
            visited.update(expected['visited'])
            external += len(expected['calls']) * 2
            records.append({'state': hex(state), 'scenario': scenario,
                            'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['sourceDependencies'] = dependencies
    entry['stackFrameModel'] = {'localAllocationBytes': 84, 'outgoingArgumentBytes': 12, 'secondPointOffset': 12,
                                'firstPointOffset': 16, 'textOffset': 20, 'textHalfwordCount': 32,
                                'historicalSourceTypesProven': False}
    entry['oracle'] = {'vectors': len(records), 'nativeAndRecompiledCalls': len(records) * 2, 'syntheticExternalCalls': external,
                       'nativeCalleeCalls': 0, 'verifiedReturn': True, 'independentDisplayAndRecordAssertions': True,
                       'instructionAddressesVisited': [hex(address) for address in sorted(visited)], 'records': records,
                       'limitations': ['State10/11,42,43/45/46/48 and signed/default selectors are checked with bounded counts0,1,2,3,6,8',
                                       'Independent assertions cover64-byte helper text, two native stack points, persistent draw style,31 entity records, signed attributes and seventh outgoing argument',
                                       'Distinct descriptors are returned by repeated getter calls; synthetic draw helpers mutate point records between calls',
                                       'Native helper bodies, display hardware, historical source types and behavior beyond bounded valid record counts remain unproven']}
    report.update(matches=[entry], attempts=attempts, moduleInputSha256=matcher.sha(binary),
                  nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': len(records), 'nativeAndRecompiledCalls': len(records) * 2,
           'syntheticExternalCalls': external, 'visitedInstructions': len(visited)})


if __name__ == '__main__':
    main()
