import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control52/native_itcm_01fff43c.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01fff43c.json'
ADDRESS = 0x01FFF43C
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'
FRAME = 0x0301FFB0
ENTRIES = FRAME + 32


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    regions = [(0x01FF8000, 0x8000), (0x02000000, 0x200000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for address, size in regions:
        machine.mem_map(address, size)
    machine.mem_write(0x03000000, rng.randbytes(0x20000))
    machine.mem_write(ADDRESS, code)
    source, output = 0x03002000, 0x03004000
    record = bytearray(rng.randbytes(52))
    index = [-32768, -1, 0, 32767, -2, 123][vector % 6]
    struct.pack_into('<h', record, 4, index)
    machine.mem_write(source, bytes(record))
    source_argument = 0 if vector % 10 == 0 else source
    valid = bool(source_argument and index != -1)
    original = rng.randbytes(0x140)
    machine.mem_write(output, original)
    required_output = bytearray(original)
    word = struct.unpack_from('<I', record, 0x30)[0]
    group = (word >> 23) & 3
    arguments = [source_argument, output, rng.getrandbits(32), rng.getrandbits(32)]
    entries = bytes(value for i in range(5) for value in (record[0x1a + i], record[0x1f + i]))
    point1 = [(0x8000 + vector) & 65535, (0xffff - vector) & 65535]
    point2 = [(0x7fff - vector) & 65535, vector & 65535]
    results = [rng.getrandbits(32), rng.getrandbits(32)]
    fills = [bytes((vector + phase * 31 + i) & 255 for i in range(count)) for phase, count in enumerate((64, 62, 44))]
    if valid:
        struct.pack_into('<i', required_output, 0, index)
        required_output[4:8] = record[:4]
        required_output[0x2e:0x30] = record[4:6]
        required_output[0x30] = group
        required_output[0xb6:0xca] = record[6:0x1a]
        for destination, start in ((0x11c, 0x24), (0x124, 0x28), (0x128, 0x2c)):
            required_output[destination:destination + 4] = record[start:start + 4]
        for location, value in ((0x12c, word >> 2 & 127), (0x12e, word >> 9 & 7), (0x12d, word >> 15 & 255),
                                (0xaf, word >> 25), (0xac, word >> 12 & 7)):
            required_output[location] = value
        struct.pack_into('<II', required_output, 0x130, *arguments[2:])
        for i in range(5):
            required_output[0xd6 + i * 2] = record[0x1a + i]
        initial_output = bytes(required_output)
        for location, payload in ((0x4a, fills[0]), (0xc, fills[1]), (0x8a, fills[2])):
            required_output[location:location + len(payload)] = payload
        struct.pack_into('<HH', required_output, 0x11c, *point1)
        struct.pack_into('<HH', required_output, 0x120, *(value & 65535 for value in results))
        expected = [(0x02008E0C, [source + 6, output + 0xb6, 20]),
                    (0x0207B460, [index & 0xffffffff, group, ENTRIES, output + 0x4a]),
                    (0x0207B1C4, [ENTRIES, output + 0x4a, output + 0xc]),
                    (0x0207C078, [struct.unpack_from('<h', required_output, 0x2e)[0] & 0xffffffff,
                                  required_output[0x30], output + 0x4a, output + 0x8a]),
                    (0x0207C2B8, [FRAME, output + 0x4a]), (0x0207C3D8, [FRAME, output + 0x4a])]
    else:
        required_output[0:8] = bytes([255]) * 8
        required_output[0x2e:0x30] = b'\xff\xff'
        expected = []
    padding = bytes(machine.mem_read(FRAME + 4, 28)) + bytes(machine.mem_read(FRAME + 42, 2))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[:4] = arguments
    registers[-2:] = [0x0301FFF0, 0x05000000]
    machine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector & 1 else 0))
    for register, value in zip(matcher.REGISTERS, registers):
        machine.reg_write(register, value)
    calls, writes, visited = [], [], set()
    machine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def store(uc, address, payload):
        uc.mem_write(address, payload)
        writes.append([address, len(payload), payload.hex()])
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        stage = len(calls)
        required = expected[stage] if stage < len(expected) else None
        actual = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if required is None or address != required[0] or actual[:len(required[1])] != required[1]:
            raise ValueError({'failure': 'Record expansion helper contract differs', 'vector': vector, 'stage': stage,
                              'address': hex(address), 'actual': actual, 'required': required})
        result = rng.getrandbits(32)
        if stage == 0:
            store(uc, actual[1], bytes(uc.mem_read(actual[0], actual[2])))
        if stage in (1, 2):
            if bytes(uc.mem_read(ENTRIES, 10)) != entries:
                raise ValueError('Stack entry pairs do not match independent interleaving')
        if stage == 1 and bytes(uc.mem_read(output, 0x140)) != initial_output:
            raise ValueError('Initial expanded fields differ before any synthetic output helper can overwrite them')
        if stage in (1, 2, 3):
            destination = [output + 0x4a, output + 0xc, output + 0x8a][stage - 1]
            store(uc, destination, fills[stage - 1])
        if stage == 3:
            store(uc, output + 0x11c, struct.pack('<HH', *point1))
        if stage in (4, 5):
            if bytes(uc.mem_read(FRAME, 4)) != struct.pack('<HH', *(point1 if stage == 4 else point2)):
                raise ValueError('Point local failed to reload output fields or preserve callee-updated coordinates')
            result = results[stage - 4]
            if stage == 4:
                store(uc, FRAME, struct.pack('<HH', *point2))
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': actual})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10 | (0x80 if vector & 1 else 0))
        uc.reg_write(UC_ARM_REG_PC, returned)
    machine.hook_add(UC_HOOK_CODE, trace)
    machine.emu_start(ADDRESS, 0x05000000, count=3000)
    if machine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected):
        raise ValueError('Record expansion did not return after its expected protocol')
    if bytes(machine.mem_read(output, 0x140)) != bytes(required_output):
        raise ValueError('Expanded record fields, byte sequences, scalar arguments or helper results differ')
    actual_padding = bytes(machine.mem_read(FRAME + 4, 28)) + bytes(machine.mem_read(FRAME + 42, 2))
    if padding != actual_padding:
        raise ValueError('Unreferenced stack padding was changed')
    return {'registers': [machine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': machine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(machine.mem_read(first, size))) for first, size in regions]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Expansion C compiler pin changed')
    report = json.loads(REPORT.read_text()) if REPORT.exists() else {'schemaVersion': 1, 'module': 'itcm', 'matches': [],
             'romSha256': matcher.sha((ROOT / 'inputs/game.nds').read_bytes()), 'wholeModuleLinked': False, 'sourceReconstructionComplete': False}
    if report['matches'] and matcher.sha(SOURCE.read_bytes()) != report['matches'][0]['sourceSha256']:
        raise ValueError('Frozen expansion C source changed')
    attempts, matches = matcher.compare(SOURCE, 'itcm', 2, 'all', True)
    if 'native_itcm_01fff43c' not in matches:
        raise ValueError('Normal C and inlined zip helper stopped matching all native bytes')
    entry, compiled = matches['native_itcm_01fff43c']
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases, external = [], 0
    for vector in range(80):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and recompiled expansion effects differ')
        external += len(expected['calls']) * 2
        cases.append({'vector': vector, 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['inlinedSourceHelpers'] = ['zip_one']
    entry['additionalNativeFunctionCredit'] = 0
    entry['stackFrameModel'] = {'localAllocationBytes': 44, 'pointOffset': 0, 'pointBytes': 4,
                                'entryArrayOffset': 32, 'entryStride': 2, 'entryCount': 5,
                                'unreferencedReservedBytes': 28, 'tailAlignmentBytes': 2, 'historicalSourceTypesProven': False}
    entry['oracle'] = {'vectors': 80, 'nativeAndRecompiledCalls': 160, 'syntheticExternalCalls': external, 'nativeCalleeCalls': 0,
                       'verifiedReturn': True, 'independentExpandedRecordAndFrameAssertions': True, 'records': cases,
                       'limitations': ['NULL and invalid-index paths, signed indices, packed source fields and complete336-byte destination effects are checked',
                                       'Both helper-visible entry-pair and point records have explicit native stack locations; reserved and alignment storage remains unchanged',
                                       'Synthetic helpers change output coordinates before the caller reload and mutate the shared point before its second use',
                                       'The inline helper has no separate native function/byte credit; native external bodies and historical allocation types remain unproven',
                                       'Void-source values are not assigned semantics; all registers/CPSR,writes,call arguments and initialized memory are compared']}
    report.update(matches=[entry], attempts=attempts, moduleInputSha256=matcher.sha(binary),
                  nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 80, 'nativeAndRecompiledCalls': 160, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
