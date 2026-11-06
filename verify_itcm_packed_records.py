import json
import random
import struct
from pathlib import Path
import match_lowlevel as matcher
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_CPSR, UC_ARM_REG_PC

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'src/itcm/control51/native_itcm_01fff278.c'
REPORT = ROOT / 'evidence/matches/itcm-native_itcm_01fff278.json'
ADDRESS = 0x01FFF278
OUTPUT = 0x02246780
PIN = '7150fa4fe4cb6db6867ac530ec1a0754f6ca4df92868d963a7875196f9222880'


def transformed(original, source, extra, present):
    output = bytearray(original)
    if not present:
        output[4:6] = b'\xff\xff'
        return bytes(output)
    output[0:4] = source[0x14:0x18]
    output[4:6] = source[0x18:0x1a]
    output[6:0x1a] = source[:20]
    for index in range(5):
        output[0x1a + index] = source[0x7a + index * 2]
        output[0x1f + index] = source[0x7b + index * 2]
    output[0x24:0x28] = source[0x20:0x24]
    output[0x28:0x2c] = source[0x28:0x2c]
    output[0x2c:0x30] = source[0x2c:0x30]
    flags = ((source[0x1b] & 3) | ((source[0x30] & 127) << 2) | ((source[0x32] & 7) << 9)
             | ((extra & 7) << 12) | ((source[0x1a] & 3) << 23) | ((source[0x1c] & 127) << 25))
    struct.pack_into('<I', output, 0x30, flags)
    return bytes(output)


def execute(code, vector):
    rng = random.Random(20261027 + vector)
    engine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    ranges = [(0x01FF8000, 0x8000), (0x02000000, 0x500000), (0x03000000, 0x20000), (0x05000000, 0x1000)]
    for first, size in ranges:
        engine.mem_map(first, size)
    engine.mem_write(0x03000000, rng.randbytes(0x20000))
    engine.mem_write(ADDRESS, code)
    context = 0x03008000
    ids = [(vector << 8) + index + 1 for index in range(6)]
    engine.mem_write(context + 28, struct.pack('<6I', *ids))
    pointers = [0x03002000 + index * 0x200 for index in range(6)]
    records, outputs, required_records, extra = [], [], [], []
    for index in range(6):
        record = bytearray(rng.randbytes(0x100))
        old = rng.randbytes(0x34)
        for offset in (0x18, 0x20, 0x22, 0x28, 0x2a, 0x2c, 0x2e):
            struct.pack_into('<H', record, offset, [0, 0x7fff, 0x8000, 0xffff][(vector + index + offset) % 4])
        value = rng.getrandbits(32)
        records.append(bytes(record))
        outputs.append(old)
        extra.append(value)
        required_records.append(transformed(old, record, value, bool(vector & (1 << index))))
        engine.mem_write(pointers[index], bytes(record))
        engine.mem_write(OUTPUT + index * 0x34, old)
    expected = [(0x020633B0, [])]
    for index in range(6):
        expected.append((0x02062A10, [ids[index]]))
        if vector & (1 << index):
            expected.append((0x02008E0C, [pointers[index], OUTPUT + index * 0x34 + 6, 20]))
            expected.append((0x02063E44, [pointers[index]]))
    registers = [rng.getrandbits(32) for _ in matcher.REGISTERS]
    registers[-2:] = [0x0301FFF0, 0x05000000]
    engine.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
    for register, initial in zip(matcher.REGISTERS, registers):
        engine.reg_write(register, initial)
    calls, writes, visited = [], [], set()
    engine.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, address, size, value, user: writes.append([address, size, value & ((1 << (size * 8)) - 1)]))
    def trace(uc, address, size, user):
        if ADDRESS <= address < ADDRESS + len(code):
            visited.add(address)
            return
        required = expected[len(calls)] if len(calls) < len(expected) else None
        arguments = [uc.reg_read(register) for register in matcher.REGISTERS[:4]]
        if required is None or address != required[0] or arguments[:len(required[1])] != required[1]:
            raise ValueError('Packed record conversion called the wrong helper or arguments')
        result = rng.getrandbits(32)
        if address == 0x020633B0:
            result = context
        elif address == 0x02062A10:
            index = ids.index(arguments[0])
            result = pointers[index] if vector & (1 << index) else 0
        elif address == 0x02008E0C:
            payload = bytes(uc.mem_read(arguments[0], arguments[2]))
            uc.mem_write(arguments[1], payload)
            writes.append([arguments[1], len(payload), payload.hex()])
        elif address == 0x02063E44:
            result = extra[pointers.index(arguments[0])]
        returned = uc.reg_read(matcher.REGISTERS[-1])
        calls.append({'address': hex(address), 'arguments': arguments})
        for register in matcher.REGISTERS[:4] + [matcher.REGISTERS[12]]:
            uc.reg_write(register, rng.getrandbits(32))
        uc.reg_write(matcher.REGISTERS[0], result)
        uc.reg_write(UC_ARM_REG_CPSR, rng.getrandbits(4) << 28 | 0x10)
        uc.reg_write(UC_ARM_REG_PC, returned)
    engine.hook_add(UC_HOOK_CODE, trace)
    engine.emu_start(ADDRESS, 0x05000000, count=4000)
    if engine.reg_read(UC_ARM_REG_PC) != 0x05000000 or len(calls) != len(expected):
        raise ValueError('Packed record conversion did not finish the expected protocol')
    if bytes(engine.mem_read(OUTPUT, 6 * 0x34)) != b''.join(required_records):
        raise ValueError('Packed fields, halfword pairs, text, interleaved bytes or absent-record sentinel differ')
    return {'registers': [engine.reg_read(register) for register in matcher.REGISTERS], 'cpsr': engine.reg_read(UC_ARM_REG_CPSR),
            'calls': calls, 'writes': writes, 'visited': sorted(visited),
            'memoryHashes': [matcher.sha(bytes(engine.mem_read(first, size))) for first, size in ranges]}


def main():
    if matcher.sha(matcher.COMPILER.read_bytes()) != PIN:
        raise ValueError('Packed record compiler pin changed')
    report = json.loads(REPORT.read_text())
    old = report['matches'][0]
    if matcher.sha(SOURCE.read_bytes()) != old['sourceSha256']:
        raise ValueError('Frozen packed record C changed')
    flags = old['compilerFlags']
    attempts, matches = matcher.compare(SOURCE, 'itcm', int(flags[0][2:]), flags[flags.index('-inline') + 1], 'speed' in flags)
    if old['name'] not in matches:
        raise ValueError('Typed C records/bitfields stopped matching the complete native function')
    entry, compiled = matches[old['name']]
    binary = (ROOT / 'extract/arm9/itcm.bin').read_bytes()
    native = binary[ADDRESS - 0x01FF8000:ADDRESS - 0x01FF8000 + entry['bytes']]
    cases = []
    external = 0
    for vector in range(64):
        expected, actual = execute(native, vector), execute(compiled, vector)
        if expected != actual:
            raise ValueError('Native and compiled packed record conversion effects differ')
        external += len(expected['calls']) * 2
        cases.append({'recordPresenceMask': vector, 'stateSha256': matcher.sha(json.dumps(expected, sort_keys=True).encode())})
    entry['sourceCallAliases'] = {'native_fn_first_02062a10': '0x02062a10', 'native_fn_second_02062a10': '0x02062a10'}
    entry['oracle'] = {'vectors': 64, 'nativeAndRecompiledCalls': 128, 'syntheticExternalCalls': external, 'nativeCalleeCalls': 0,
                       'verifiedReturn': True, 'independentPackedRecordAssertions': True, 'records': cases,
                       'limitations': ['Bitfield layout and unsigned-to-signed narrowing are pinned to the measured MW target ABI, not portable layout claims',
                                       'All64 presence patterns, signed halfword extrema, all32 packed output bits,20 text bytes and two five-byte sequences are independently checked',
                                       'Separate C lookup declarations bind to the same measured ARM address; historical identities and application field meanings remain unknown',
                                       'External helpers use synthetic contracts and receive no native execution/source credit; registers/CPSR,writes,call arguments and initialized memory are compared']}
    report.update(matches=[entry], attempts=attempts, nativeSymbols={rel['symbol']: rel['target'] for rel in entry['relocations']})
    REPORT.write_text(json.dumps(report, indent=2) + '\n')
    print({'functions': 1, 'bytes': entry['bytes'], 'cases': 64, 'nativeAndRecompiledCalls': 128, 'syntheticExternalCalls': external})


if __name__ == '__main__':
    main()
